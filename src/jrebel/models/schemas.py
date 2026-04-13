"""
Pydantic 数据模型

定义 API 请求和响应的数据结构。
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ServerInfo(BaseModel):
    """
    服务器基本信息

    包含在所有响应中的服务器标识信息。
    """

    server_version: str = Field(alias="serverVersion")
    server_protocol_version: str = Field(alias="serverProtocolVersion")
    server_guid: str = Field(alias="serverGuid")
    group_type: str = Field(default="managed", alias="groupType")
    status_code: str = Field(default="SUCCESS", alias="statusCode")

    model_config = {"populate_by_name": True}


class ValidationResponse(ServerInfo):
    """
    连接验证响应

    用于 /jrebel/validate-connection 端点。
    """

    company: str = "Administrator"
    can_get_lease: bool = Field(default=True, alias="canGetLease")
    license_type: int = Field(default=1, alias="licenseType")
    evaluation_license: bool = Field(default=False, alias="evaluationLicense")
    seat_pool_type: str = Field(default="standalone", alias="seatPoolType")


class LeaseRequest(BaseModel):
    """
    租约请求参数

    客户端请求许可证租约时提交的参数。
    """

    randomness: str | None = None  # 客户端随机数
    username: str | None = None  # 用户名/邮箱
    guid: str | None = None  # 客户端 GUID
    offline: bool = True  # 是否离线模式
    client_time: str | None = Field(default=None, alias="clientTime")  # 客户端时间戳

    model_config = {"populate_by_name": True}


class LeaseResponse(ServerInfo):
    """
    租约响应

    用于 /jrebel/leases 端点的响应数据。
    """

    id: int = 1
    license_type: int = Field(default=1, alias="licenseType")
    evaluation_license: bool = Field(default=False, alias="evaluationLicense")
    signature: str  # RSA 签名
    server_randomness: str = Field(alias="serverRandomness")  # 服务器随机数
    seat_pool_type: str = Field(default="standalone", alias="seatPoolType")
    offline: bool = True  # 离线模式
    valid_from: str | None = Field(default=None, alias="validFrom")  # 有效期开始
    valid_until: str | None = Field(default=None, alias="validUntil")  # 有效期结束
    company: str = "Administrator"  # 公司名称
    order_id: str = Field(default="", alias="orderId")
    zero_ids: list[Any] = Field(default_factory=list, alias="zeroIds")
    license_valid_from: str | None = Field(default=None, alias="licenseValidFrom")
    license_valid_until: str | None = Field(default=None, alias="licenseValidUntil")


class Lease1Response(ServerInfo):
    """
    简化租约响应

    用于 /jrebel/leases/1 端点。
    """

    msg: str | None = None
    status_message: str | None = Field(default=None, alias="statusMessage")
    company: str | None = None


class RpcResponse(BaseModel):
    """
    RPC 响应基类

    所有 RPC XML 响应的基础结构。
    """

    message: str = ""
    response_code: str = "OK"
    salt: str


class ObtainTicketResponse(RpcResponse):
    """
    获取票据响应

    用于 /rpc/obtainTicket.action 端点。
    """

    prolongation_period: str  # 延长周期
    ticket_id: str = "1"  # 票据 ID
    ticket_properties: str  # 票据属性


class ReleaseTicketResponse(RpcResponse):
    """
    释放票据响应

    用于 /rpc/releaseTicket.action 端点。
    """

    pass


class PingResponse(RpcResponse):
    """
    Ping 响应

    用于 /rpc/ping.action 端点。
    """

    pass
