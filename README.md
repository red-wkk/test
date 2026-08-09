# 👥 用户管理系统

一个基于 **FastAPI + MySQL** 的全栈用户管理系统，前后端分离架构，支持 Mock 模式与数据库模式的灵活切换。

## 📋 目录

- [技术栈](#-技术栈)
- [项目结构](#-项目结构)
- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [API 接口](#-api-接口)
- [数据库](#-数据库)
- [配置说明](#-配置说明)
- [前端页面](#-前端页面)
- [GitHub Actions](#-github-actions)

## 🛠️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端框架** | FastAPI (>=0.115.0) | 高性能异步 Python Web 框架 |
| **ORM** | SQLAlchemy 2.0+ | 数据库对象关系映射 |
| **数据库驱动** | PyMySQL (>=1.1.0) | MySQL 连接驱动 |
| **数据校验** | Pydantic 2.0+ | 请求/响应模型校验 |
| **数据库** | MySQL | 关系型数据库 |
| **数据库迁移** | Flyway | 管理数据库版本变更 |
| **前端** | 原生 HTML/CSS/JS | 无框架依赖，采用 IIFE 模块模式 |
| **服务部署** | Uvicorn | ASGI 服务器 |

## 📁 项目结构

```
├── backend/                        # 后端 (Python FastAPI)
│   ├── main.py                     # FastAPI 应用入口
│   ├── config.py                   # 环境变量配置管理
│   ├── database.py                 # SQLAlchemy 数据库连接（支持懒加载）
│   ├── models.py                   # ORM 数据模型 —— SysUser 表
│   ├── schemas.py                  # Pydantic 数据校验与 API 响应模型
│   ├── mock_data.py                # Mock 数据模块（5 条测试用户）
│   ├── requirements.txt            # Python 依赖清单
│   └── .env.example                # 环境变量模板
├── frontend/                       # 前端 (原生 HTML/CSS/JS)
│   ├── index.html                  # 用户列表页面
│   ├── js/
│   │   ├── api.js                  # API 请求封装
│   │   └── app.js                  # 页面逻辑、DOM 渲染、事件处理
│   └── css/
│       └── style.css               # 现代化 CSS（变量、Grid/Flexbox、响应式）
├── db/
│   └── migration/
│       └── V1__create_sys_user_table.sql   # Flyway 数据库迁移脚本
├── .github/workflows/              # GitHub Actions 工作流
│   ├── claude.yml                  # Claude Code 自动响应工作流
│   └── claude-review.yml           # Claude Code Review 工作流
├── .gitignore
└── README.md
```

## ✨ 功能特性

### 🔀 Mock 模式
- 通过 `USE_MOCK=true` 环境变量控制，无需安装数据库即可运行
- 内置 5 条测试用户数据，方便本地开发调试

### 🛡️ 自动降级
- 数据库连接失败时自动回退到 Mock 数据
- 保证服务始终可用，不会因数据库问题导致接口不可访问

### 🏥 健康检查
- 提供 `/api/health` 端点用于服务状态监控
- 返回当前运行模式（Mock / 数据库）

### 🔒 XSS 防护
- 前端使用 DOM-safe 方法对用户输入进行 HTML 转义
- 防止跨站脚本攻击

### 📱 响应式设计
- CSS 使用 CSS 变量、Grid/Flexbox 布局
- 完美适配桌面端和移动端

### ⚡ CI/CD 集成
- GitHub Actions 自动化响应 Issue 评论
- 自动化的 PR Code Review

## 🚀 快速开始

### 前置要求

- Python 3.10+
- MySQL 5.7+（可选，Mock 模式下不需要）
- pip

### 1. 启动后端

#### Mock 模式（推荐快速体验）

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 复制环境变量模板（默认 USE_MOCK=true，无需数据库）
cp .env.example .env

# 启动服务
python main.py
```

服务启动后访问：http://localhost:8000

#### 数据库模式

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，设置 USE_MOCK=false 并填写数据库连接信息

# 初始化数据库（使用 Flyway 或手动执行迁移脚本）
# 执行 db/migration/V1__create_sys_user_table.sql

# 启动服务
python main.py
```

服务启动后访问：http://localhost:8000

### 2. 启动前端

```bash
cd frontend

# 使用 Python 内置 HTTP 服务器
python -m http.server 3000
```

前端页面访问：http://localhost:3000

### 3. 验证

在浏览器中打开 http://localhost:3000，如果后端以 Mock 模式运行，你将在页面上看到 5 条测试用户数据。

## 📡 API 接口

### 获取用户列表

```
GET /api/users
```

**响应示例：**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "status": 1,
      "created_at": null,
      "updated_at": null
    }
  ]
}
```

**状态码说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | int | 状态码，200 表示成功 |
| `message` | string | 提示信息，会标注数据来源（mock / fallback to mock / success） |
| `data` | array | 用户对象数组 |

**用户对象字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 用户 ID（主键） |
| `username` | string | 用户名 |
| `email` | string | 邮箱地址 |
| `status` | int | 状态：1=正常，2=禁用 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |

### 健康检查

```
GET /api/health
```

**响应示例：**

```json
{
  "status": "ok",
  "mock_mode": true
}
```

## 🗄️ 数据库

### 数据模型

**sys_user 表结构：**

| 列名 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | BIGINT UNSIGNED | PRIMARY KEY, AUTO_INCREMENT | 用户 ID |
| `username` | VARCHAR(64) | NOT NULL, UNIQUE | 用户名 |
| `email` | VARCHAR(128) | NOT NULL, DEFAULT '' | 邮箱 |
| `status` | TINYINT | NOT NULL, DEFAULT 1 | 状态：1=正常，2=禁用 |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**索引：**

- 主键索引：`id`
- 唯一索引：`username` (`uk_username`)
- 普通索引：`status` (`idx_status`)

### Mock 数据

Mock 模式下内置了 5 条测试用户：

| ID | 用户名 | 邮箱 | 状态 |
|----|--------|------|------|
| 1 | admin | admin@example.com | 正常 |
| 2 | zhangsan | zhangsan@example.com | 正常 |
| 3 | lisi | lisi@example.com | 正常 |
| 4 | wangwu | wangwu@example.com | 禁用 |
| 5 | zhaoliu | zhaoliu@example.com | 正常 |

## ⚙️ 配置说明

所有配置通过 `.env` 文件中的环境变量进行管理：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `DB_HOST` | 127.0.0.1 | MySQL 主机地址 |
| `DB_PORT` | 3306 | MySQL 端口 |
| `DB_USER` | root | 数据库用户名 |
| `DB_PASSWORD` | (空) | 数据库密码 |
| `DB_NAME` | test_db | 数据库名称 |
| `USE_MOCK` | true | Mock 模式开关 |

### Mock 模式 vs 数据库模式

```bash
# Mock 模式 —— 使用内存数据，无需数据库（推荐开发调试使用）
USE_MOCK=true

# 数据库模式 —— 连接真实 MySQL 数据库
USE_MOCK=false
```

## 🎨 前端页面

前端是一个纯粹的用户列表展示页面，包含完整的状态覆盖：

- ✅ **加载状态**：数据请求中显示加载动画
- ✅ **错误状态**：请求失败显示错误提示
- ✅ **空状态**：无数据时显示空状态占位
- ✅ **正常状态**：展示用户列表表格

### 交互特性

- 点击 **🔄 刷新** 按钮可重新加载数据
- 用户状态以彩色徽标展示（🟢 正常 / 🔴 禁用）
- 表格行悬停效果

## 🔄 GitHub Actions

项目集成了两个 GitHub Actions 工作流：

### claude.yml
监听 Issue 评论（含 `@claude` 指令）和 PR Review 评论，自动触发 Claude Code Action 进行处理。

### claude-review.yml
监听 PR 的 `opened` / `synchronize` 事件，自动进行代码审查。

---

> 🤖 本项目使用 [Claude Code](https://claude.ai/code) 辅助开发与维护
