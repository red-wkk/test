"""
Mock 数据模块
当 USE_MOCK=true 或数据库不可用时，使用内存中的模拟数据。
"""
from schemas import UserOut

# 初始化 Mock 用户数据
_mock_users: list[UserOut] = [
    UserOut(id=1,  username="admin",    email="admin@example.com",    status=1),
    UserOut(id=2,  username="zhangsan", email="zhangsan@example.com", status=1),
    UserOut(id=3,  username="lisi",     email="lisi@example.com",     status=1),
    UserOut(id=4,  username="wangwu",   email="wangwu@example.com",   status=2),
    UserOut(id=5,  username="zhaoliu",  email="zhaoliu@example.com",  status=1),
]


def get_mock_users() -> list[UserOut]:
    """返回 Mock 用户列表（只读副本）"""
    return list(_mock_users)
