"""
RSA 私钥配置

这些密钥用于签名 JRebel 许可证响应。
包含两种格式的私钥：
- PKCS#8 格式：用于 JRebel 租约签名（SHA1withRSA）
- ASN.1 格式：用于 RPC XML 响应签名（MD5withRSA）
"""

# =============================================================================
# JRebel 许可证服务器私钥（PKCS#8 格式，Base64 编码）
# 用于使用 SHA1withRSA 算法签名租约响应
# =============================================================================
JREBEL_PRIVATE_KEY_B64 = (
    "MIICXAIBAAKBgQDQ93CP6SjEneDizCF1P/MaBGf582voNNFcu8oMhgdTZ/N6qa6O"
    "7XJDr1FSCyaDdKSsPCdxPK7Y4Usq/fOPas2kCgYcRS/iebrtPEFZ/7TLfk39HLuT"
    "Ejzo0/CNvjVsgWeh9BYznFaxFDLx7fLKqCQ6w1OKScnsdqwjpaXwXqiulwIDAQAB"
    "AoGATOQvvBSMVsTNQkbgrNcqKdGjPNrwQtJkk13aO/95ZJxkgCc9vwPqPrOdFbZa"
    "ppZeHa5IyScOI2nLEfe+DnC7V80K2dBtaIQjOeZQt5HoTRG4EHQaWoDh27BWuJoi"
    "p5WMrOd+1qfkOtZoRjNcHl86LIAh/+3vxYyebkug4UHNGPkCQQD+N4ZUkhKNQW7m"
    "pxX6eecitmOdN7Yt0YH9UmxPiW1LyCEbLwduMR2tfyGfrbZALiGzlKJize38shGC"
    "1qYSMvZFAkEA0m6psWWiTUWtaOKMxkTkcUdigalZ9xFSEl6jXFB94AD+dlPS3J5g"
    "NzTEmbPLc14VIWJFkO+UOrpl77w5uF2dKwJAaMpslhnsicvKMkv31FtBut5iK6GW"
    "eEafhdPfD94/bnidpP362yJl8Gmya4cI1GXvwH3pfj8S9hJVA5EFvgTB3QJBAJP1"
    "O1uAGp46X7Nfl5vQ1M7RYnHIoXkWtJ417Kb78YWPLVwFlD2LHhuy/okT4fk8LZ9L"
    "eZ5u1cp1RTdLIUqAiAECQC46OwOm87L35yaVfpUIjqg/1gsNwNsj8HvtXdF/9d30"
    "JIM3GwdytCvNRLqP35Ciogb9AO8ke8L6zY83nxPbClM="
)

# =============================================================================
# RPC 响应私钥（ASN.1 格式，Base64 编码）
# 用于使用 MD5withRSA 算法签名 XML RPC 响应
# =============================================================================
RPC_PRIVATE_KEY_B64 = (
    "MIIBOgIBAAJBALecq3BwAI4YJZwhJ+snnDFj3lF3DMqNPorV6y5ZKXCiCMqj8OeO"
    "mxk4YZW9aaV9ckl/zlAOI0mpB3pDT+Xlj2sCAwEAAQJAW6/aVD05qbsZHMvZuS2A"
    "a5FpNNj0BDlf38hOtkhDzz/hkYb+EBYLLvldhgsD0OvRNy8yhz7EjaUqLCB0juIN"
    "4QIhAOeCQp+NXxfBmfdG/S+XbRUAdv8iHBl+F6O2wr5fA2jzAiEAywlDfGIl6acn"
    "akPrmJE0IL8qvuO3FtsHBrpkUuOnXakCIQCqdr+XvADI/UThTuQepuErFayJMBSA"
    "sNe3NFsw0cUxAQIgGA5n7ZPfdBi3BdM4VeJWb87WrLlkVxPqeDSbcGrCyMkCIFSs"
    "5JyXvFTreWt7IQjDssrKDRIPmALdNjvfETwlNJyY"
)

# =============================================================================
# 固定的服务器随机数
# 用于生成一致的签名
# =============================================================================
SERVER_RANDOMNESS = "H2ulzLlh7E0="
