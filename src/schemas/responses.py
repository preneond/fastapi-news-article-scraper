from pydantic import BaseModel


class ServiceBaseResponse(BaseModel):
    """Response model that is sent when Image Evaluation is requested"""

    success: bool


# class UserListResponse(ServiceBaseResponse):
#     data: List[User]
#
#
# class UserResponse(ServiceBaseResponse):
#     data: User
