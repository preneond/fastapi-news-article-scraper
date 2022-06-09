from typing import List

from pydantic import BaseModel
from pydantic.networks import HttpUrl


class ServiceBaseResponse(BaseModel):
    """Service response base model"""

    success: bool


class FindArticleRequest(BaseModel):
    """Request Body Model of /find/articles request"""

    keywords: List[str]


class ArticleItemResponse(BaseModel):
    """ArticleItem response model in ArticleListResponse"""

    text: str
    url: HttpUrl


class ArticleListResponse(ServiceBaseResponse):
    """List of Articles that are returned for /find/articles request"""

    articles: List[ArticleItemResponse]
