"""
应用配置模块

使用 Pydantic Settings 管理应用配置，支持从环境变量和 .env 文件加载配置。
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类

    从环境变量或 .env 文件加载配置项。
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # 服务器配置
    # -------------------------------------------------------------------------
    host: str = "0.0.0.0"  # 监听地址
    port: int = 9009  # 监听端口
    debug: bool = False  # 调试模式
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # -------------------------------------------------------------------------
    # 服务器标识
    # -------------------------------------------------------------------------
    server_guid: str = "a1b4aea8-b031-4302-b602-670a990272cb"  # 服务器 GUID
    server_version: str = "3.2.4"  # 服务器版本
    server_protocol_version: str = "1.1"  # 协议版本

    # -------------------------------------------------------------------------
    # 许可证配置
    # -------------------------------------------------------------------------
    license_valid_days: int = 180  # 许可证有效天数
    prolongation_period: str = "607875500"  # 延长周期（约 19 年）

    @property
    def license_valid_ms(self) -> int:
        """获取许可证有效期（毫秒）"""
        return self.license_valid_days * 24 * 60 * 60 * 1000


@lru_cache
def get_settings() -> Settings:
    """
    获取应用配置（带缓存）

    Returns:
        Settings: 应用配置实例
    """
    return Settings()
