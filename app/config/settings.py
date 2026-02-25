import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from app.utils.common import get_project_meta, get_project_base_directory


# 定义全局配置常量
_meta = get_project_meta()
APP_NAME = _meta["name"]
APP_VERSION = _meta["version"]
APP_DESCRIPTION = _meta["description"]

PROJECT_BASE_DIR = get_project_base_directory()

class Settings(BaseSettings):
    """应用配置类 - 平铺结构"""
    
    # =============================================================================
    # 应用基础配置
    # =============================================================================
    service_host: str = Field(default="0.0.0.0", description="服务主机地址", env="SERVICE_HOST")
    service_port: int = Field(default=8001, description="服务端口", env="SERVICE_PORT")
    debug: bool = Field(default=False, description="调试模式", env="DEBUG")
    app_log_level: str = Field(default="INFO", description="日志级别", env="APP_LOG_LEVEL")
    
    # 数据库配置
    db_name: str = Field(default="knowledge_service", description="数据库名称", env="DB_NAME")
    database_type: str = Field(default="postgresql", description="数据库类型: postgresql 或 mysql", env="DATABASE_TYPE")
    db_pool_size: int = Field(default=10, description="连接池大小", env="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, description="最大溢出连接数", env="DB_MAX_OVERFLOW")
    
    # PostgreSQL 配置
    postgresql_host: str = Field(default="localhost", description="PostgreSQL主机地址", env="POSTGRESQL_HOST")
    postgresql_port: int = Field(default=5432, description="PostgreSQL端口", env="POSTGRESQL_PORT")
    postgresql_user: str = Field(default="postgres", description="PostgreSQL用户名", env="POSTGRESQL_USER")
    postgresql_password: str = Field(default="your_password", description="PostgreSQL密码", env="POSTGRESQL_PASSWORD")
    
    # MySQL 配置
    mysql_host: str = Field(default="localhost", description="MySQL主机地址", env="MYSQL_HOST")
    mysql_port: int = Field(default=3306, description="MySQL端口", env="MYSQL_PORT")
    mysql_user: str = Field(default="root", description="MySQL用户名", env="MYSQL_USER")
    mysql_password: str = Field(default="your_password", description="MySQL密码", env="MYSQL_PASSWORD")
    
    # 文件存储配置
    storage_type: str = Field(default="minio", description="存储类型: minio, s3, local", env="STORAGE_TYPE")
    
    # MinIO 配置
    minio_endpoint: str = Field(default="localhost:9000", description="MinIO端点", env="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="minioadmin", description="MinIO访问密钥", env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="minioadmin", description="MinIO秘密密钥", env="MINIO_SECRET_KEY")
    minio_secure: bool = Field(default=False, description="MinIO是否使用HTTPS", env="MINIO_SECURE")
    
    # S3 配置
    s3_region: str = Field(default="us-east-1", description="S3区域", env="S3_REGION")
    s3_endpoint_url: str = Field(default="https://your-s3-endpoint.com", description="S3端点URL", env="S3_ENDPOINT_URL")
    s3_access_key_id: str = Field(default="your_access_key", description="S3访问密钥ID", env="S3_ACCESS_KEY_ID")
    s3_secret_access_key: str = Field(default="your_secret_key", description="S3秘密访问密钥", env="S3_SECRET_ACCESS_KEY")
    s3_use_ssl: bool = Field(default=True, description="S3是否使用SSL", env="S3_USE_SSL")

    
    # 本地存储配置
    local_upload_dir: str = Field(default="./uploads", description="本地上传目录", env="LOCAL_UPLOAD_DIR")
    
    # Azure Blob Storage SAS配置
    azure_account_url: str = Field(default="https://yourstorageaccount.blob.core.windows.net", description="Azure存储账户URL", env="AZURE_ACCOUNT_URL")
    azure_sas_token: str = Field(default="your_sas_token", description="Azure SAS令牌", env="AZURE_SAS_TOKEN")
    
    # Azure Blob Storage SPN配置
    azure_spn_account_url: str = Field(default="https://yourstorageaccount.dfs.core.windows.net", description="Azure SPN存储账户URL", env="AZURE_SPN_ACCOUNT_URL")
    azure_spn_client_id: str = Field(default="your_client_id", description="Azure SPN客户端ID", env="AZURE_SPN_CLIENT_ID")
    azure_spn_client_secret: str = Field(default="your_client_secret", description="Azure SPN客户端密钥", env="AZURE_SPN_CLIENT_SECRET")
    azure_spn_tenant_id: str = Field(default="your_tenant_id", description="Azure SPN租户ID", env="AZURE_SPN_TENANT_ID")
    azure_spn_container_name: str = Field(default="your_container", description="Azure SPN容器名称", env="AZURE_SPN_CONTAINER_NAME")
    
    # OSS配置
    oss_access_key: str = Field(default="your_access_key", description="OSS访问密钥ID", env="OSS_ACCESS_KEY")
    oss_secret_key: str = Field(default="your_secret_key", description="OSS秘密访问密钥", env="OSS_SECRET_KEY")
    oss_endpoint_url: str = Field(default="https://oss-cn-hangzhou.aliyuncs.com", description="OSS端点URL", env="OSS_ENDPOINT_URL")
    oss_region: str = Field(default="cn-hangzhou", description="OSS区域", env="OSS_REGION")
    oss_prefix_path: str = Field(default="", description="OSS前缀路径", env="OSS_PREFIX_PATH")
    
    # Redis配置
    redis_host: str = Field(default="localhost", description="Redis主机地址", env="REDIS_HOST")
    redis_port: int = Field(default=6379, description="Redis端口", env="REDIS_PORT")
    redis_db: int = Field(default=0, description="Redis数据库编号", env="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, description="Redis密码", env="REDIS_PASSWORD")
    redis_ssl: bool = Field(default=False, description="是否使用SSL连接", env="REDIS_SSL")
    redis_decode_responses: bool = Field(default=True, description="是否自动解码响应", env="REDIS_DECODE_RESPONSES")
    redis_socket_connect_timeout: int = Field(default=5, description="连接超时时间(秒)", env="REDIS_SOCKET_CONNECT_TIMEOUT")
    redis_socket_timeout: int = Field(default=5, description="读写超时时间(秒)", env="REDIS_SOCKET_TIMEOUT")
    redis_retry_on_timeout: bool = Field(default=True, description="超时时是否重试", env="REDIS_RETRY_ON_TIMEOUT")
    redis_max_connections: int = Field(default=5, description="每个数据库的最大连接数", env="REDIS_MAX_CONNECTIONS")

    # =============================================================================
    # JWT 认证配置
    # =============================================================================
    jwt_secret_key: str = Field(default="your-secret-key", description="JWT密钥", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", description="JWT算法", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, description="访问令牌过期时间(分钟)", env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_days: int = Field(default=7, description="刷新令牌过期时间(天)", env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    auth_use_local_jwt: bool = Field(default=True, description="本服务是否使用本地JWT验证(不HTTP自调); 发token的本服务为True, 其他业务服务为False", env="AUTH_USE_LOCAL_JWT")
    auth_user_service_url: Optional[str] = Field(default=None, description="认证服务地址(仅当auth_use_local_jwt=False时必填)", env="AUTH_USER_SERVICE_URL")
    auth_jwks_endpoint: str = Field(default="/api/v1/jwt/.well-known/jwks.json", description="JWKS端点路径", env="AUTH_JWKS_ENDPOINT")
    auth_jwt_config_endpoint: str = Field(default="/api/v1/jwt/jwt-config", description="JWT配置端点路径", env="AUTH_JWT_CONFIG_ENDPOINT")
    auth_blacklist_endpoint: str = Field(default="/api/v1/jwt/blacklist", description="黑名单端点路径", env="AUTH_BLACKLIST_ENDPOINT")

    # =============================================================================
    # 短信配置
    # =============================================================================
    sms_provider: str = Field(default="", description="短信服务提供商", env="SMS_PROVIDER")
    sms_api_key: str = Field(default="", description="短信API密钥", env="SMS_API_KEY")
    sms_api_secret: str = Field(default="", description="短信API秘密", env="SMS_API_SECRET")
    sms_from_number: str = Field(default="", description="发件人号码", env="SMS_FROM_NUMBER")
    sms_access_key_id: str = Field(default="", description="短信访问密钥ID", env="SMS_ACCESS_KEY_ID")
    sms_access_key_secret: str = Field(default="", description="短信访问密钥秘密", env="SMS_ACCESS_KEY_SECRET")
    sms_sign_name: str = Field(default="", description="短信签名", env="SMS_SIGN_NAME")
    sms_template_code: str = Field(default="", description="短信模板代码", env="SMS_TEMPLATE_CODE")

    # =============================================================================
    # 邮件服务配置（用于邮箱验证等）
    # =============================================================================
    email_host: str = Field(default="smtp.gmail.com", description="邮件主机", env="EMAIL_HOST")
    email_port: int = Field(default=587, description="邮件端口", env="EMAIL_PORT")
    email_username: str = Field(default="", description="邮件用户名", env="EMAIL_USERNAME")
    email_password: str = Field(default="", description="邮件密码", env="EMAIL_PASSWORD")
    email_use_tls: bool = Field(default=True, description="邮件是否使用TLS", env="EMAIL_USE_TLS")
    email_from: str = Field(default="", description="发件人邮箱", env="EMAIL_FROM")
    
    # =============================================================================
    # OAuth 配置
    # =============================================================================
    oauth_enabled: bool = Field(default=False, description="是否启用OAuth", env="OAUTH_ENABLED")
    oauth_base_url: str = Field(default="http://localhost:8001", description="OAuth基础URL", env="OAUTH_BASE_URL")
    
    github_client_id: str = Field(default="", description="GitHub客户端ID", env="GITHUB_CLIENT_ID")
    github_client_secret: str = Field(default="", description="GitHub客户端秘密", env="GITHUB_CLIENT_SECRET")
    github_redirect_uri: str = Field(default="", description="GitHub重定向URI", env="GITHUB_REDIRECT_URI")
    
    google_client_id: str = Field(default="", description="Google客户端ID", env="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(default="", description="Google客户端秘密", env="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(default="", description="Google重定向URI", env="GOOGLE_REDIRECT_URI")
    
    # 微信配置
    wechat_app_id: str = Field(default="", description="微信应用ID", env="WECHAT_APP_ID")
    wechat_app_secret: str = Field(default="", description="微信应用秘密", env="WECHAT_APP_SECRET")
    wechat_redirect_uri: str = Field(default="", description="微信重定向URI", env="WECHAT_REDIRECT_URI")
    
    # 支付宝配置
    alipay_app_id: str = Field(default="", description="支付宝应用ID", env="ALIPAY_APP_ID")
    alipay_private_key: str = Field(default="", description="支付宝私钥", env="ALIPAY_PRIVATE_KEY")
    alipay_public_key: str = Field(default="", description="支付宝公钥", env="ALIPAY_PUBLIC_KEY")
    alipay_redirect_uri: str = Field(default="", description="支付宝重定向URI", env="ALIPAY_REDIRECT_URI")
    
    # OIDC配置
    oidc_client_id: str = Field(default="", description="OIDC客户端ID", env="OIDC_CLIENT_ID")
    oidc_client_secret: str = Field(default="", description="OIDC客户端秘密", env="OIDC_CLIENT_SECRET")
    oidc_redirect_uri: str = Field(default="", description="OIDC重定向URI", env="OIDC_REDIRECT_URI")
    oidc_issuer: str = Field(default="", description="OIDC发行者", env="OIDC_ISSUER")
    
    # =============================================================================
    # 验证码配置
    # =============================================================================
    verification_code_expire_minutes: int = Field(default=5, description="验证码过期时间(分钟)", env="VERIFICATION_CODE_EXPIRE_MINUTES")
    verification_code_length: int = Field(default=6, description="验证码长度", env="VERIFICATION_CODE_LENGTH")
    
    # =============================================================================
    # 安全配置
    # =============================================================================
    password_min_length: int = Field(default=8, description="密码最小长度", env="PASSWORD_MIN_LENGTH")
    password_require_uppercase: bool = Field(default=True, description="密码是否需要大写字母", env="PASSWORD_REQUIRE_UPPERCASE")
    password_require_lowercase: bool = Field(default=True, description="密码是否需要小写字母", env="PASSWORD_REQUIRE_LOWERCASE")
    password_require_digits: bool = Field(default=True, description="密码是否需要数字", env="PASSWORD_REQUIRE_DIGITS")
    password_require_special_chars: bool = Field(default=True, description="密码是否需要特殊字符", env="PASSWORD_REQUIRE_SPECIAL_CHARS")
    
    # =============================================================================
    # 文件上传配置
    # =============================================================================
    max_file_size_mb: int = Field(default=10, description="最大文件大小(MB)", env="MAX_FILE_SIZE_MB")
    allowed_file_types: list = Field(default=["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"], description="允许的文件类型", env="ALLOWED_FILE_TYPES")
    
    class Config:
        env_file = os.path.join(PROJECT_BASE_DIR, "env")
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    @property
    def database_url(self) -> str:
        """生成数据库连接URL"""
        if self.database_type.lower() == "postgresql":
            return f"postgresql+asyncpg://{self.postgresql_user}:{self.postgresql_password}@{self.postgresql_host}:{self.postgresql_port}/{self.db_name}"
        elif self.database_type.lower() == "mysql":
            return f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.db_name}"
        else:
            return "sqlite+aiosqlite:///./koalawiki.db"
    
    @property
    def redis_url(self) -> str:
        """生成Redis连接URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @property
    def app_name(self) -> str:
        """应用名称(用于JWT issuer等)"""
        return APP_NAME


# 全局配置实例
settings = Settings() 