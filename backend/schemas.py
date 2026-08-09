"""
Pydantic 数据校验模型
"""
from pydantic import BaseModel, Field
from datetime import datetime


class UserOut(BaseModel):
    """返回给前端的用户数据结构"""
    id:         int       = Field(..., description="用户ID")
    username:   str       = Field(..., description="用户名")
    email:      str       = Field("", description="邮箱")
    status:     int       = Field(1, description="状态：1=正常，2=禁用")
    created_at: datetime | None = Field(None, description="创建时间")
    updated_at: datetime | None = Field(None, description="更新时间")

    class Config:
        from_attributes = True


class ApiResponse(BaseModel):
    """统一 API 响应格式"""
    code:    int           = Field(200, description="状态码")
    message: str           = Field("success", description="提示信息")
    data:    list[UserOut] = Field(default_factory=list, description="用户列表数据")
