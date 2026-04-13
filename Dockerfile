# =============================================================================
# JRebel License Server - Docker 镜像构建文件
# =============================================================================
# 使用多阶段构建以减小最终镜像体积
# 基于 Python 3.12 slim 镜像，使用 uv 管理依赖

# -----------------------------------------------------------------------------
# 第一阶段：构建阶段
# -----------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:0.6-python3.12-bookworm-slim AS builder

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 设置工作目录
WORKDIR /app

# 复制 uv 配置文件
COPY pyproject.toml uv.lock .python-version ./

# 安装项目依赖（仅生产依赖，不安装项目本身）
RUN uv sync --frozen --no-dev --no-install-project

# 复制源代码并安装项目
COPY src/ ./src/
RUN uv sync --frozen --no-dev

# -----------------------------------------------------------------------------
# 第二阶段：运行阶段
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

# 镜像元数据
LABEL maintainer="developer@example.com" \
      version="2.0.0" \
      description="JRebel License Server - 基于 FastAPI 的现代化许可证服务器"

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=9009 \
    DEBUG=false \
    LOG_LEVEL=INFO \
    PATH="/app/.venv/bin:$PATH"

# 创建非 root 用户以提高安全性
RUN groupadd --gid 1000 jrebel && \
    useradd --uid 1000 --gid jrebel --shell /bin/bash --create-home jrebel

# 设置工作目录
WORKDIR /app

# 从构建阶段复制虚拟环境和源代码
COPY --from=builder --chown=jrebel:jrebel /app/.venv /app/.venv
COPY --from=builder --chown=jrebel:jrebel /app/src /app/src

# 切换到非 root 用户
USER jrebel

# 暴露端口
EXPOSE 9009

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:9009/health')" || exit 1

# 启动命令
CMD ["python", "-m", "jrebel.main"]
