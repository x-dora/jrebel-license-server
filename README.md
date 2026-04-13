# JRebel License Server

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

**基于 FastAPI 构建的现代化 JRebel 许可证服务器**

[功能特性](#功能特性) •
[快速开始](#快速开始) •
[使用方法](#使用方法) •
[API 文档](#api-文档) •
[部署指南](#部署指南)

</div>

---

## 功能特性

- **异步高性能** - 基于 FastAPI 和 uvicorn，支持高并发请求
- **现代化架构** - 采用分层架构设计，代码结构清晰易维护
- **完整兼容** - 支持 JRebel 7.1 及更早版本，以及 JRebel 2018.1+ 版本
- **离线激活** - 支持离线许可证，有效期 180 天
- **精美界面** - 现代化的 Web UI，深色主题设计
- **Docker 支持** - 提供 Dockerfile 和 docker-compose，一键部署
- **类型安全** - 完整的类型注解，支持 mypy 静态检查

## 项目结构

```
jrebel-license-server/
├── pyproject.toml          # 项目配置和依赖管理
├── Dockerfile              # Docker 镜像构建文件
├── docker-compose.yml      # Docker Compose 编排文件
├── .env.example            # 环境变量示例
├── README.md               # 项目说明文档
│
├── src/
│   └── jrebel/
│       ├── __init__.py     # 包初始化
│       ├── main.py         # 应用入口点
│       ├── app.py          # FastAPI 应用工厂
│       ├── config.py       # 配置管理
│       │
│       ├── api/            # API 层
│       │   ├── __init__.py
│       │   ├── router.py   # 路由聚合
│       │   ├── deps.py     # 依赖注入
│       │   └── routes/     # 路由模块
│       │       ├── jrebel.py   # JRebel 许可证端点
│       │       ├── rpc.py      # RPC 端点（旧版）
│       │       └── health.py   # 健康检查
│       │
│       ├── core/           # 核心模块
│       │   └── crypto/     # 加密签名
│       │       ├── keys.py     # RSA 密钥
│       │       └── signer.py   # 签名工具
│       │
│       ├── models/         # 数据模型
│       │   └── schemas.py  # Pydantic 模型
│       │
│       ├── services/       # 业务逻辑
│       │   └── license.py  # 许可证服务
│       │
│       └── templates/      # 页面模板
│           └── index.html  # 主页
│
└── tests/                  # 测试目录
    └── ...
```

## 快速开始

### 环境要求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/your-repo/jrebel-license-server.git
cd jrebel-license-server
```

2. **安装依赖**

```bash
uv sync
```

3. **启动服务**

```bash
uv run jrebel-server
```

服务将在 `http://localhost:9009` 启动。

### 使用 Docker

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 使用方法

### JRebel 2018.1+ 版本

1. 打开 JRebel 激活窗口
2. 选择 **"Team URL"** 或 **"License Server"**
3. 输入服务器地址：`http://localhost:9009/{GUID}`
   - 其中 `{GUID}` 为任意 UUID，例如：`http://localhost:9009/a1b4aea8-b031-4302-b602-670a990272cb`
4. 邮箱填写任意有效格式的邮箱地址

### JRebel 7.1 及更早版本

1. 打开 JRebel 激活窗口
2. 输入服务器地址：`http://localhost:9009/{tokenname}`
   - 其中 `{tokenname}` 为任意字符串
3. 邮箱填写任意有效格式的邮箱地址

## API 文档

### 主要端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 主页（使用说明） |
| `/health` | GET | 健康检查 |
| `/jrebel/leases` | POST | 创建许可证租约 |
| `/jrebel/leases/1` | POST | 获取租约信息 |
| `/jrebel/validate-connection` | POST | 验证连接 |
| `/rpc/obtainTicket.action` | POST | 获取票据（旧版） |
| `/rpc/releaseTicket.action` | POST | 释放票据（旧版） |
| `/rpc/ping.action` | POST | Ping 检测（旧版） |

### 开发模式

启用调试模式后可访问 Swagger 文档：

```bash
DEBUG=true uv run python -m jrebel.main
```

- Swagger UI: `http://localhost:9009/docs`
- ReDoc: `http://localhost:9009/redoc`

## 部署指南

### 环境变量

| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| `HOST` | `0.0.0.0` | 监听地址 |
| `PORT` | `9009` | 监听端口 |
| `DEBUG` | `false` | 调试模式 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `LICENSE_VALID_DAYS` | `180` | 许可证有效天数 |

### 生产部署

推荐使用 Docker 或 systemd 进行部署：

```bash
# 复制环境变量配置
cp .env.example .env

# 修改配置
vim .env

# 使用 Docker Compose 启动
docker-compose up -d
```

## 开发指南

### 安装开发依赖

```bash
uv sync  # dev 依赖默认包含
```

### 代码检查

```bash
# 代码格式化
uv run ruff format .

# 代码检查
uv run ruff check .
```

### 运行测试

```bash
uv run pytest
```

## 许可证

本项目仅供学习研究使用，请勿用于商业用途。

---

<div align="center">

**如果这个项目对你有帮助，请给个 Star ⭐**

</div>
