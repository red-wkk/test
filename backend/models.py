"""
数据库 ORM 模型
表结构与 Flyway 建表脚本 V1__create_sys_user_table.sql 保持一致。
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SysUser(Base):
    __tablename__ = "sys_user"

    id         = Column(BigInteger, primary_key=True, autoincrement=True, comment="用户ID")
    username   = Column(String(64), nullable=False, unique=True, comment="用户名")
    email      = Column(String(128), nullable=False, default="", comment="邮箱")
    status     = Column(Integer, nullable=False, default=1, comment="状态：1=正常，2=禁用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
