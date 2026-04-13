"""
RSA 签名工具模块

提供 JRebel 许可证响应的 RSA 签名功能：
- JRebelSigner: 用于现代 JRebel API 的签名（SHA1withRSA）
- RpcSigner: 用于旧版 RPC API 的签名（MD5withRSA）
"""

from __future__ import annotations

import base64
from typing import ClassVar

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPrivateNumbers,
    RSAPublicNumbers,
)

from jrebel.core.crypto.keys import (
    JREBEL_PRIVATE_KEY_B64,
    RPC_PRIVATE_KEY_B64,
    SERVER_RANDOMNESS,
)


class JRebelSigner:
    """
    JRebel 租约签名器

    使用 SHA1withRSA 算法签名租约响应。
    用于现代 JRebel 许可证 API 端点（/jrebel/leases, /agent/leases）。
    """

    _private_key: ClassVar[RSAPrivateKey | None] = None
    server_randomness: ClassVar[str] = SERVER_RANDOMNESS

    @classmethod
    def _get_private_key(cls) -> RSAPrivateKey:
        """
        加载并缓存 RSA 私钥

        Returns:
            RSAPrivateKey: RSA 私钥对象
        """
        if cls._private_key is None:
            key_bytes = base64.b64decode(JREBEL_PRIVATE_KEY_B64)
            cls._private_key = serialization.load_der_private_key(
                key_bytes, password=None, backend=default_backend()
            )
        return cls._private_key  # type: ignore

    @classmethod
    def sign_lease(
        cls,
        client_randomness: str,
        guid: str,
        offline: bool,
        valid_from: str,
        valid_until: str,
    ) -> str:
        """
        为租约响应生成签名

        Args:
            client_randomness: 客户端随机字符串
            guid: 客户端安装 GUID
            offline: 是否为离线许可证
            valid_from: 许可证有效期开始时间戳（毫秒）
            valid_until: 许可证有效期结束时间戳（毫秒）

        Returns:
            str: Base64 编码的 RSA 签名
        """
        # 构建待签名字符串
        if offline:
            parts = [
                client_randomness,
                cls.server_randomness,
                guid,
                str(offline).lower(),
                valid_from,
                valid_until,
            ]
        else:
            parts = [
                client_randomness,
                cls.server_randomness,
                guid,
                str(offline).lower(),
            ]

        sign_string = ";".join(parts)

        # 使用 SHA1withRSA 签名
        private_key = cls._get_private_key()
        signature = private_key.sign(
            sign_string.encode("utf-8"),
            padding.PKCS1v15(),
            hashes.SHA1(),  # noqa: S303 - 为兼容性需要使用 SHA1
        )

        return base64.b64encode(signature).decode("utf-8")


class RpcSigner:
    """
    RPC XML 响应签名器

    使用 MD5withRSA 算法签名 XML 响应。
    用于旧版 JRebel RPC 端点：
    - /rpc/obtainTicket.action
    - /rpc/releaseTicket.action
    - /rpc/ping.action
    """

    _private_key: ClassVar[RSAPrivateKey | None] = None

    @classmethod
    def _get_private_key(cls) -> RSAPrivateKey:
        """
        从 ASN.1 格式加载并缓存 RSA 私钥

        Returns:
            RSAPrivateKey: RSA 私钥对象
        """
        if cls._private_key is None:
            key_bytes = base64.b64decode(RPC_PRIVATE_KEY_B64)
            cls._private_key = cls._load_asn1_private_key(key_bytes)
        return cls._private_key  # type: ignore

    @classmethod
    def _load_asn1_private_key(cls, key_bytes: bytes) -> RSAPrivateKey:
        """
        从 ASN.1 DER 格式加载 RSA 私钥

        密钥采用传统 RSA 私钥格式（非 PKCS#8）。
        需要手动解析 ASN.1 结构。

        Args:
            key_bytes: DER 编码的私钥字节

        Returns:
            RSAPrivateKey: RSA 私钥对象
        """

        def parse_asn1_integer(data: bytes, offset: int) -> tuple[int, int]:
            """
            解析 ASN.1 INTEGER 类型

            Args:
                data: ASN.1 数据
                offset: 当前偏移量

            Returns:
                Tuple[int, int]: (整数值, 新偏移量)
            """
            if data[offset] != 0x02:
                raise ValueError(f"期望 INTEGER 标签 (0x02)，得到 {hex(data[offset])}")
            offset += 1
            length = data[offset]
            offset += 1
            if length & 0x80:
                num_bytes = length & 0x7F
                length = int.from_bytes(data[offset : offset + num_bytes], "big")
                offset += num_bytes
            value = int.from_bytes(data[offset : offset + length], "big", signed=False)
            # 处理负数（前导 0x00 字节）
            if data[offset] & 0x80:
                value = int.from_bytes(data[offset : offset + length], "big", signed=True)
            return value, offset + length

        offset = 0
        # 解析 SEQUENCE
        if key_bytes[offset] != 0x30:
            raise ValueError("期望 SEQUENCE 标签")
        offset += 1

        # 解析长度
        length = key_bytes[offset]
        offset += 1
        if length & 0x80:
            num_bytes = length & 0x7F
            offset += num_bytes

        # 解析 RSA 私钥各组件
        version, offset = parse_asn1_integer(key_bytes, offset)  # 版本
        n, offset = parse_asn1_integer(key_bytes, offset)  # 模数
        e, offset = parse_asn1_integer(key_bytes, offset)  # 公钥指数
        d, offset = parse_asn1_integer(key_bytes, offset)  # 私钥指数
        p, offset = parse_asn1_integer(key_bytes, offset)  # 素数 p
        q, offset = parse_asn1_integer(key_bytes, offset)  # 素数 q
        dmp1, offset = parse_asn1_integer(key_bytes, offset)  # d mod (p-1)
        dmq1, offset = parse_asn1_integer(key_bytes, offset)  # d mod (q-1)
        iqmp, offset = parse_asn1_integer(key_bytes, offset)  # q^(-1) mod p

        # 构建私钥对象
        public_numbers = RSAPublicNumbers(e, n)
        private_numbers = RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, public_numbers)

        return private_numbers.private_key(default_backend())

    @classmethod
    def sign_xml(cls, xml_content: str) -> str:
        """
        签名 XML 内容并返回带签名注释的完整响应

        Args:
            xml_content: XML 响应内容

        Returns:
            str: 在开头添加签名注释的 XML 内容
        """
        signature = cls._sign_content(xml_content.encode("utf-8"))
        return f"<!-- {signature} -->\n{xml_content}"

    @classmethod
    def _sign_content(cls, content: bytes) -> str:
        """
        使用 MD5withRSA 签名内容

        Args:
            content: 待签名内容

        Returns:
            str: 十六进制编码的签名
        """
        private_key = cls._get_private_key()

        # MD5withRSA：先计算 MD5 哈希，然后使用 RSA PKCS#1 v1.5 签名
        signature = private_key.sign(
            content,
            padding.PKCS1v15(),
            hashes.MD5(),  # noqa: S303 - 为兼容性需要使用 MD5
        )

        return signature.hex()
