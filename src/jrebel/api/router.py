"""API 路由配置。"""

from fastapi import APIRouter

from jrebel.api.routes import health, jrebel, rpc

api_router = APIRouter()

# 注册路由模块
api_router.include_router(jrebel.router, tags=["JRebel"])
api_router.include_router(rpc.router, prefix="/rpc", tags=["RPC"])
api_router.include_router(health.router, tags=["Health"])
