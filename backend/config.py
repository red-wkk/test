"""
应用配置模块
所有配置从环境变量读取，方便不同环境切换。
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """全局配置，从环境变量加载"""

    # 数据库配置
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "test_db")

    # Mock 模式：true 时使用内存数据，不连数据库
    USE_MOCK: bool = os.getenv("USE_MOCK", "true").lower() in ("true", "1", "yes")

    @property
    def database_url(self) -> str:
        """生成 SQLAlchemy 连接字符串"""
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            "?charset=utf8mb4"
        )


settings = Settings()
