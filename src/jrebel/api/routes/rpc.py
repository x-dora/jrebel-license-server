"""旧版 RPC 接口，用于支持旧版 JRebel 客户端。"""

from fastapi import APIRouter, HTTPException, Query, Request, Response, status

from jrebel.api.deps import LicenseServiceDep

router = APIRouter()


def xml_response(content: str) -> Response:
    """创建 XML 响应，设置正确的 Content-Type。"""
    return Response(
        content=content,
        media_type="text/html; charset=utf-8",
    )


async def get_param(
    request: Request,  # noqa: ARG001
    name: str,  # noqa: ARG001
    query_value: str | None,
    form_value: str | None,
) -> str | None:
    """
    从请求中获取参数，优先使用查询参数，其次使用表单参数。

    同时支持 GET 和 POST 请求：
    - GET 请求：从 URL 查询参数获取
    - POST 请求：优先查询参数，其次表单数据
    """
    if query_value is not None:
        return query_value
    if form_value is not None:
        return form_value
    return None


@router.api_route("/obtainTicket.action", methods=["GET", "POST"])
async def obtain_ticket(
    request: Request,
    license_service: LicenseServiceDep,
    salt: str | None = Query(default=None),
    userName: str | None = Query(default=None),
) -> Response:
    """
    获取许可证票据（旧版接口）。

    此接口用于 JRebel 7.1 及更早版本。
    同时支持 GET 和 POST 请求。

    参数:
        salt: 用于签名的盐值
        userName: 用户名
    """
    # 如果是 POST 请求，也尝试从表单获取参数
    if request.method == "POST":
        try:
            form_data = await request.form()
            if salt is None:
                salt = form_data.get("salt")
            if userName is None:
                userName = form_data.get("userName")
        except Exception:
            pass  # 忽略表单解析错误

    if not salt or not userName:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="缺少必需参数: salt, userName",
        )

    response_xml = license_service.generate_obtain_ticket_response(salt, userName)
    return xml_response(response_xml)


@router.api_route("/releaseTicket.action", methods=["GET", "POST"])
async def release_ticket(
    request: Request,
    license_service: LicenseServiceDep,
    salt: str | None = Query(default=None),
) -> Response:
    """
    释放许可证票据（旧版接口）。

    同时支持 GET 和 POST 请求。

    参数:
        salt: 用于签名的盐值
    """
    # 如果是 POST 请求，也尝试从表单获取参数
    if request.method == "POST":
        try:
            form_data = await request.form()
            if salt is None:
                salt = form_data.get("salt")
        except Exception:
            pass  # 忽略表单解析错误

    if not salt:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="缺少必需参数: salt",
        )

    response_xml = license_service.generate_release_ticket_response(salt)
    return xml_response(response_xml)


@router.api_route("/ping.action", methods=["GET", "POST"])
async def ping(
    request: Request,
    license_service: LicenseServiceDep,
    salt: str | None = Query(default=None),
) -> Response:
    """
    心跳检测接口（旧版）。

    同时支持 GET 和 POST 请求。

    参数:
        salt: 用于签名的盐值
    """
    # 如果是 POST 请求，也尝试从表单获取参数
    if request.method == "POST":
        try:
            form_data = await request.form()
            if salt is None:
                salt = form_data.get("salt")
        except Exception:
            pass  # 忽略表单解析错误

    if not salt:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="缺少必需参数: salt",
        )

    response_xml = license_service.generate_ping_response(salt)
    return xml_response(response_xml)
