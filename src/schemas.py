from typing import List

from pydantic import BaseModel
from pydantic.networks import HttpUrl


class ServiceBaseResponse(BaseModel):
    """Service response base model"""

    success: bool


class FindArticleRequest(BaseModel):
    keywords: List[str]


class ArticleItemResponse(BaseModel):
    text: str
    url: HttpUrl


class ArticleListResponse(ServiceBaseResponse):
    articles: List[ArticleItemResponse]
