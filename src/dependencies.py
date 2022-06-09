from typing import Any

from fastapi.requests import Request


async def get_logger(request: Request) -> Any:
    """

    :param request:
    :return: logger
    """
    return request.state.logger
