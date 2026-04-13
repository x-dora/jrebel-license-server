"""JRebel 许可证 API 接口。"""

from typing import Any

from fastapi import APIRouter, Form, HTTPException, status

from jrebel.api.deps import LicenseServiceDep, SettingsDep

router = APIRouter()


@router.post("/jrebel/validate-connection")
@router.post("/agent/validate-connection")
async def validate_connection(settings: SettingsDep) -> dict[str, Any]:
    """
    验证服务器连接。

    JRebel 客户端调用此接口来验证许可证服务器是否可用。
    """
    return {
        "serverVersion": settings.server_version,
        "serverProtocolVersion": settings.server_protocol_version,
        "serverGuid": settings.server_guid,
        "groupType": "managed",
        "statusCode": "SUCCESS",
        "company": "Administrator",
        "canGetLease": True,
        "licenseType": 1,
        "evaluationLicense": False,
        "seatPoolType": "standalone",
    }


@router.post("/jrebel/leases")
@router.post("/agent/leases")
async def create_lease(
    settings: SettingsDep,
    license_service: LicenseServiceDep,
    randomness: str | None = Form(default=None),
    username: str | None = Form(default=None),
    guid: str | None = Form(default=None),
    offline: bool = Form(default=True),
    clientTime: str | None = Form(default=None),
) -> dict[str, Any]:
    """
    创建新的许可证租约。

    这是 JRebel 2018.1+ 版本的主要激活接口。

    参数:
        randomness: 客户端随机字符串，用于签名
        username: 用户名或邮箱
        guid: 客户端安装 GUID
        offline: 是否生成离线许可证
        clientTime: 客户端时间戳（毫秒）
    """
    if not randomness or not username or not guid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="缺少必需参数: randomness, username, guid",
        )

    lease_data = license_service.generate_lease(
        client_randomness=randomness,
        guid=guid,
        username=username,
        client_time=clientTime,
        offline=offline,
    )

    response: dict[str, Any] = {
        "serverVersion": settings.server_version,
        "serverProtocolVersion": settings.server_protocol_version,
        "serverGuid": settings.server_guid,
        "groupType": "managed",
        "id": 1,
        "licenseType": 1,
        "evaluationLicense": False,
        "signature": lease_data.signature,
        "serverRandomness": lease_data.server_randomness,
        "seatPoolType": "standalone",
        "statusCode": "SUCCESS",
        "offline": lease_data.offline,
        "company": lease_data.company,
        "orderId": "",
        "zeroIds": [],
        "licenseValidFrom": lease_data.valid_from,
        "licenseValidUntil": lease_data.valid_until,
    }

    if lease_data.offline:
        response["validFrom"] = lease_data.valid_from
        response["validUntil"] = lease_data.valid_until

    return response


@router.post("/jrebel/leases/1")
@router.post("/agent/leases/1")
async def get_lease_info(
    settings: SettingsDep,
    username: str | None = Form(default=None),
) -> dict[str, Any]:
    """
    获取租约信息（简化版）。

    返回基本的服务器信息。
    """
    response: dict[str, Any] = {
        "serverVersion": settings.server_version,
        "serverProtocolVersion": settings.server_protocol_version,
        "serverGuid": settings.server_guid,
        "groupType": "managed",
        "statusCode": "SUCCESS",
        "msg": None,
        "statusMessage": None,
    }

    if username:
        response["company"] = username

    return response
