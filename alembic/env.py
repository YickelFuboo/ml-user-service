import os
import re
import sys
import urllib.parse
from logging.config import fileConfig

from sqlalchemy import create_engine, pool, text
from alembic import context

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database.model_base import Base
from app.domains.models.user import User, FileMetadata
from app.domains.models.role import Role, UserInRole
from app.domains.models.permission import Permission, RolePermission
from app.domains.models.tenant import Tenant, tenant_members

config = context.config
target_metadata = Base.metadata

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if config.config_file_name:
    _PROJECT_ROOT = os.path.dirname(os.path.abspath(config.config_file_name))


def _load_env() -> dict:
    """从项目根（alembic.ini 所在目录）的 env 或 .env 读取，优先 env；使用 utf-8-sig 以兼容 BOM。"""
    out = {}
    for name in ("env", ".env"):
        path = os.path.join(_PROJECT_ROOT, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, _, v = line.partition("=")
                    key = k.strip().lstrip("\ufeff")
                    out[key] = v.strip().strip('"').strip("'")
        except Exception:
            pass
        break
    return out


_ENV = _load_env()


def _get(key: str, default: str = "") -> str:
    return _ENV.get(key, os.environ.get(key, default))


def _build_database_url() -> str:
    """根据配置构建数据库 URL。PostgreSQL 迁移使用 pg8000（纯 Python）避免 Windows 下 psycopg2 编码问题。"""
    db_type = _get("DATABASE_TYPE", "postgresql").strip().lower()
    db_name = _get("DB_NAME", "pando_user_service")

    def q(s: str) -> str:
        return urllib.parse.quote(str(s), safe="")

    if db_type == "postgresql":
        user = q(_get("POSTGRESQL_USER", "postgres"))
        password = q(_get("POSTGRESQL_PASSWORD", ""))
        host = q(_get("POSTGRESQL_HOST", "localhost"))
        port = _get("POSTGRESQL_PORT", "5432")
        return f"postgresql+pg8000://{user}:{password}@{host}:{port}/{q(db_name)}"
    if db_type == "mysql":
        user = q(_get("MYSQL_USER", "root"))
        password = q(_get("MYSQL_PASSWORD", ""))
        host = q(_get("MYSQL_HOST", "localhost"))
        port = _get("MYSQL_PORT", "3306")
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{q(db_name)}"
    return "sqlite:///./user_service.db"


database_url = os.environ.get("ALEMBIC_DATABASE_URL") or _build_database_url()
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name:
    fileConfig(config.config_file_name)


def _ensure_postgres_database() -> None:
    """PostgreSQL 时：若目标库不存在则连 postgres 库并创建，避免 3D000。"""
    if _get("DATABASE_TYPE", "postgresql").strip().lower() != "postgresql":
        return
    db_name = _get("DB_NAME", "pando_user_service")
    if not re.match(r"^[a-zA-Z0-9_]+$", db_name):
        return
    url = config.get_main_option("sqlalchemy.url") or database_url
    if "/" not in url or "+pg8000" not in url:
        return
    base_url = url.rsplit("/", 1)[0] + "/postgres"
    engine = create_engine(base_url, poolclass=pool.NullPool)
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            r = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = :n"), {"n": db_name}).fetchone()
            if not r:
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
    finally:
        engine.dispose()


def run_migrations_offline() -> None:
    """离线模式：仅生成 SQL，不连接数据库。"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在线模式：连接数据库并执行迁移。"""
    url = config.get_main_option("sqlalchemy.url")
    if _get("DATABASE_TYPE", "postgresql").strip().lower() == "postgresql":
        h, p, db = _get("POSTGRESQL_HOST", "localhost"), _get("POSTGRESQL_PORT", "5432"), _get("DB_NAME", "pando_user_service")
        print(f"[alembic] 连接: host={h} port={p} database={db}", file=sys.stderr)
    connectable = create_engine(url, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    _ensure_postgres_database()
    run_migrations_online()
