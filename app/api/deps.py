import logging
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.factory import get_db
from app.models.user import User
from app.services.auth_mgmt.jwt_service import JWTService
from app.constants.language import get_default_language, is_supported_language


bearer_scheme = HTTPBearer(auto_error=True)

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        user = await JWTService.get_current_user(session, token.credentials)
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账户已被禁用"
        )
    return current_user


def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    """获取当前超级管理员用户"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user


def get_request_language(request: Request) -> str:
    """
    从请求头获取语言设置
    
    优先级：
    1. X-Language 自定义请求头
    2. Accept-Language 请求头
    3. 默认语言
    """
    # 检查自定义语言头
    custom_language = request.headers.get("X-Language")
    if custom_language and is_supported_language(custom_language):
        return custom_language
    
    # 检查标准 Accept-Language 头
    accept_language = request.headers.get("Accept-Language")
    if accept_language:
        # 解析 Accept-Language 头，格式如: "zh-CN,zh;q=0.9,en;q=0.8"
        languages = accept_language.split(",")
        for lang in languages:
            # 提取语言代码，去除质量值
            lang_code = lang.split(";")[0].strip()
            # 标准化语言代码
            if lang_code.startswith("zh"):
                lang_code = "zh-CN"
            elif lang_code.startswith("en"):
                lang_code = "en-US"
            
            if is_supported_language(lang_code):
                return lang_code
    
    # 返回默认语言
    return get_default_language()
