"""
FastAPI 主应用入口
提供 GET /api/users 接口 —— 获取用户列表。
支持 Mock 模式（内存数据）和真实 MySQL 两种模式。
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from config import settings
from database import get_session
from models import SysUser
from schemas import ApiResponse, UserOut
from mock_data import get_mock_users

app = FastAPI(
    title="用户管理 API",
    description="基于 FastAPI + MySQL 的用户列表接口",
    version="1.0.0",
)

# CORS 配置：允许前端跨域调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """服务启动提示"""
    if settings.USE_MOCK:
        print("⚡ Mock 模式已启用，使用内存数据运行，无需数据库。")
    else:
        print(f"🔗 数据库连接目标: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


@app.get("/api/users", response_model=ApiResponse)
def get_users():
    """
    获取用户列表

    优先级：
    1. 若 USE_MOCK=true → 返回内存 Mock 数据
    2. 否则连接 MySQL → 返回 sys_user 表数据
    3. 若数据库连接失败 → 自动降级为 Mock 数据
    """
    # ---- Mock 模式 ----
    if settings.USE_MOCK:
        users = get_mock_users()
        return ApiResponse(code=200, message="success (mock)", data=users)

    # ---- 数据库模式 ----
    session = get_session()
    if session is None:
        # 降级：数据库不可用时自动使用 Mock
        print("⚠️  数据库连接失败，自动降级为 Mock 数据")
        users = get_mock_users()
        return ApiResponse(code=200, message="success (fallback to mock)", data=users)

    try:
        stmt = select(SysUser).order_by(SysUser.id)
        rows = session.execute(stmt).scalars().all()
        users = [
            UserOut(
                id=row.id,
                username=row.username,
                email=row.email,
                status=row.status,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]
        return ApiResponse(code=200, message="success", data=users)
    except Exception as e:
        print(f"❌ 数据库查询异常: {e}")
        users = get_mock_users()
        return ApiResponse(code=200, message="success (db error, fallback to mock)", data=users)
    finally:
        session.close()


@app.get("/api/health")
def health_check():
    """健康检查端点"""
    return {"status": "ok", "mock_mode": settings.USE_MOCK}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
