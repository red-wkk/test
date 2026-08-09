"""
数据库连接模块
基于 SQLAlchemy，支持 Mock 模式跳过真实数据库连接。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import settings

# 仅在非 Mock 模式下创建真实的数据库引擎和会话工厂
engine = None
SessionLocal = None


def get_engine():
    """懒加载数据库引擎（仅非 Mock 模式）"""
    global engine
    if engine is None and not settings.USE_MOCK:
        engine = create_engine(
            settings.database_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,   # 连接前检测可用性
            echo=False,           # 设为 True 可打印 SQL 日志
        )
    return engine


def get_session() -> Session | None:
    """
    获取数据库会话。
    Mock 模式下返回 None；调用方需自行降级处理。
    """
    if settings.USE_MOCK:
        return None

    global SessionLocal
    if SessionLocal is None:
        eng = get_engine()
        if eng is not None:
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=eng)

    if SessionLocal is None:
        return None
    return SessionLocal()
