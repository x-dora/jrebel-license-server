"""
许可证服务模块

提供 JRebel 许可证生成和 RPC 请求处理的业务逻辑。
"""

from __future__ import annotations

import html
from dataclasses import dataclass

from jrebel.config import Settings, get_settings
from jrebel.core.crypto import JRebelSigner, RpcSigner


@dataclass
class LeaseData:
    """
    租约数据容器

    存储生成的租约信息。
    """

    signature: str  # RSA 签名
    server_randomness: str  # 服务器随机数
    valid_from: str  # 有效期开始时间
    valid_until: str  # 有效期结束时间
    offline: bool  # 是否离线许可证
    company: str  # 公司/用户名


class LicenseService:
    """
    许可证服务

    处理 JRebel 许可证生成和 RPC 请求。
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """
        初始化许可证服务

        Args:
            settings: 应用配置，默认使用全局配置
        """
        self.settings = settings or get_settings()

    def generate_lease(
        self,
        client_randomness: str,
        guid: str,
        username: str,
        client_time: str | None = None,
        offline: bool = True,
    ) -> LeaseData:
        """
        生成许可证租约

        Args:
            client_randomness: 客户端随机字符串
            guid: 客户端安装 GUID
            username: 用户名或邮箱
            client_time: 客户端时间戳（毫秒）
            offline: 是否生成离线许可证

        Returns:
            LeaseData: 包含签名的租约信息
        """
        valid_from = ""
        valid_until = ""

        # 计算有效期
        if client_time:
            try:
                client_time_ms = int(client_time)
                valid_from = client_time
                valid_until = str(client_time_ms + self.settings.license_valid_ms)
            except ValueError:
                pass

        # 生成签名
        signature = JRebelSigner.sign_lease(
            client_randomness=client_randomness,
            guid=guid,
            offline=offline,
            valid_from=valid_from,
            valid_until=valid_until,
        )

        return LeaseData(
            signature=signature,
            server_randomness=JRebelSigner.server_randomness,
            valid_from=valid_from,
            valid_until=valid_until,
            offline=offline,
            company=username,
        )

    def generate_obtain_ticket_response(self, salt: str, username: str) -> str:
        """
        生成获取票据的 XML 响应

        Args:
            salt: 请求中的盐值
            username: 许可证用户名

        Returns:
            str: 带签名的 XML 响应字符串
        """
        # 转义 XML 特殊字符
        escaped_salt = html.escape(salt)
        escaped_username = html.escape(username)

        xml_content = (
            f"<ObtainTicketResponse>"
            f"<message></message>"
            f"<prolongationPeriod>{self.settings.prolongation_period}</prolongationPeriod>"
            f"<responseCode>OK</responseCode>"
            f"<salt>{escaped_salt}</salt>"
            f"<ticketId>1</ticketId>"
            f"<ticketProperties>licensee={escaped_username}\tlicenseType=0\t</ticketProperties>"
            f"</ObtainTicketResponse>"
        )

        return RpcSigner.sign_xml(xml_content)

    def generate_release_ticket_response(self, salt: str) -> str:
        """
        生成释放票据的 XML 响应

        Args:
            salt: 请求中的盐值

        Returns:
            str: 带签名的 XML 响应字符串
        """
        escaped_salt = html.escape(salt)

        xml_content = (
            f"<ReleaseTicketResponse>"
            f"<message></message>"
            f"<responseCode>OK</responseCode>"
            f"<salt>{escaped_salt}</salt>"
            f"</ReleaseTicketResponse>"
        )

        return RpcSigner.sign_xml(xml_content)

    def generate_ping_response(self, salt: str) -> str:
        """
        生成 Ping 的 XML 响应

        Args:
            salt: 请求中的盐值

        Returns:
            str: 带签名的 XML 响应字符串
        """
        escaped_salt = html.escape(salt)

        xml_content = (
            f"<PingResponse>"
            f"<message></message>"
            f"<responseCode>OK</responseCode>"
            f"<salt>{escaped_salt}</salt>"
            f"</PingResponse>"
        )

        return RpcSigner.sign_xml(xml_content)
