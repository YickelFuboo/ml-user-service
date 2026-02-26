"""initial

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2025-02-25

"""
import uuid
from datetime import datetime
from typing import Union

import bcrypt
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_name", sa.String(50), nullable=False),
        sa.Column("user_full_name", sa.String(100), nullable=True),
        sa.Column("avatar", sa.String(255), nullable=True),
        sa.Column("email", sa.String(100), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("hashed_password", sa.String(255), nullable=True),
        sa.Column("registration_method", sa.String(20), server_default="email"),
        sa.Column("github_id", sa.String(100), nullable=True),
        sa.Column("google_id", sa.String(100), nullable=True),
        sa.Column("wechat_id", sa.String(100), nullable=True),
        sa.Column("alipay_id", sa.String(100), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("is_superuser", sa.Boolean(), server_default="false"),
        sa.Column("email_verified", sa.Boolean(), server_default="false"),
        sa.Column("phone_verified", sa.Boolean(), server_default="false"),
        sa.Column("language", sa.String(10), server_default="en-US"),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_login_ip", sa.String(45), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_user_name", "users", ["user_name"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_phone", "users", ["phone"], unique=True)
    op.create_index("ix_users_github_id", "users", ["github_id"], unique=True)
    op.create_index("ix_users_google_id", "users", ["google_id"], unique=True)
    op.create_index("ix_users_wechat_id", "users", ["wechat_id"], unique=True)
    op.create_index("ix_users_alipay_id", "users", ["alipay_id"], unique=True)

    op.create_table(
        "roles",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_roles_name", "roles", ["name"], unique=True)

    op.create_table(
        "permissions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("resource", sa.String(50), nullable=False),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_permissions_name", "permissions", ["name"], unique=True)

    op.create_table(
        "file_metadata",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("file_id", sa.String(255), nullable=False),
        sa.Column("original_filename", sa.String(255), nullable=False),
        sa.Column("content_type", sa.String(100), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("bucket_name", sa.String(50), server_default="default", nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("category", sa.String(20), server_default="general"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_file_metadata_file_id", "file_metadata", ["file_id"], unique=True)

    op.create_table(
        "user_roles",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role_id", sa.String(36), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "role_permissions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("role_id", sa.String(36), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("permission_id", sa.String(36), sa.ForeignKey("permissions.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "tenants",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("owner_id", sa.String(36), nullable=False),
        sa.Column("member_count", sa.Integer(), server_default="1"),
        sa.Column("status", sa.String(1), server_default="1", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_tenants_name", "tenants", ["name"])
    op.create_index("ix_tenants_owner_id", "tenants", ["owner_id"])
    op.create_index("ix_tenants_member_count", "tenants", ["member_count"])
    op.create_index("ix_tenants_status", "tenants", ["status"])

    op.create_table(
        "tenant_members",
        sa.Column("tenant_id", sa.String(36), sa.ForeignKey("tenants.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("user_id", sa.String(36), primary_key=True),
        sa.Column("joined_at", sa.DateTime(), nullable=False),
    )

    admin_id = str(uuid.uuid4())
    hashed = bcrypt.hashpw(b"admin", bcrypt.gensalt(rounds=12)).decode("utf-8")
    now = datetime.utcnow()
    conn = op.get_bind()
    conn.execute(
        text(
            "INSERT INTO users (id, user_name, hashed_password, is_superuser, registration_method, is_active, created_at, updated_at) "
            "VALUES (:id, :user_name, :hashed_password, :is_superuser, :registration_method, :is_active, :created_at, :updated_at)"
        ),
        {
            "id": admin_id,
            "user_name": "admin",
            "hashed_password": hashed,
            "is_superuser": True,
            "registration_method": "password",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        },
    )


def downgrade() -> None:
    conn = op.get_bind()
    try:
        conn.execute(text("DELETE FROM users WHERE user_name = 'admin'"))
    except Exception:
        pass
    op.drop_table("tenant_members")
    op.drop_index("ix_tenants_status", "tenants")
    op.drop_index("ix_tenants_member_count", "tenants")
    op.drop_index("ix_tenants_owner_id", "tenants")
    op.drop_index("ix_tenants_name", "tenants")
    op.drop_table("tenants")
    op.drop_table("role_permissions")
    op.drop_table("user_roles")
    op.drop_index("ix_file_metadata_file_id", "file_metadata")
    op.drop_table("file_metadata")
    op.drop_index("ix_permissions_name", "permissions")
    op.drop_table("permissions")
    op.drop_index("ix_roles_name", "roles")
    op.drop_table("roles")
    op.drop_index("ix_users_alipay_id", "users")
    op.drop_index("ix_users_wechat_id", "users")
    op.drop_index("ix_users_google_id", "users")
    op.drop_index("ix_users_github_id", "users")
    op.drop_index("ix_users_phone", "users")
    op.drop_index("ix_users_email", "users")
    op.drop_index("ix_users_user_name", "users")
    op.drop_table("users")
