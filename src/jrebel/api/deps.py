"""FastAPI 依赖注入模块。"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from jrebel.config import Settings, get_settings
from jrebel.services.license import LicenseService


@lru_cache
def get_license_service() -> LicenseService:
    """获取缓存的许可证服务实例。"""
    return LicenseService()


# 依赖注入类型别名
SettingsDep = Annotated[Settings, Depends(get_settings)]
LicenseServiceDep = Annotated[LicenseService, Depends(get_license_service)]
