"""
News scrapers.
"""
import dataclasses
import re
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, AnyStr, Dict, List
from urllib.parse import urljoin

import bs4
import requests
from bs4 import BeautifulSoup as bs
from pydantic.networks import HttpUrl

from src.config.settings import get_settings
from src.models import ArticleOrm

settings = get_settings()


@dataclass
class Article:
    """Represents an article from a news server."""

    header: str
    url: str

    def as_orm(self) -> ArticleOrm:
        return ArticleOrm(**dataclasses.asdict(self))


class NewsScraper:
    @abstractmethod
    def get_headers(self) -> List[Article]:
        ...

    @property
    @abstractmethod
    def news_url(self) -> str:
        ...

    def construct_full_url(self, href: str) -> Any:
        return urljoin(self.news_url, href)


class IdnesScraper(NewsScraper):
    @property
    def news_url(self) -> str:
        return settings.news_config.idnes.url

    @property
    def html_parser_find_attributes(self) -> Dict[str, Any]:
        return {}

    @property
    def html_parser_find_name(self) -> List[str]:
        return settings.news_config.idnes.article_header_tags

    def get_article_url(self, header: bs4.Tag) -> str:
        return header.parent.get("href")

    def get_headers(self) -> List[Article]:
        response = requests.get(self.news_url)
        bs_html_parser = bs(response.text, "html.parser")
        bs_header_arr = bs_html_parser.find_all(
            name=self.html_parser_find_name, attrs=self.html_parser_find_attributes
        )
        bs_header_arr = [
            header
            for header in bs_header_arr
            if header.parent.get("score-type") == "Article"
        ]
        article_arr = [
            Article(header=header.get_text(), url=self.get_article_url(header))
            for header in bs_header_arr
        ]
        return article_arr


class IhnedScraper(NewsScraper):
    @property
    def news_url(self) -> str:
        return settings.news_config.ihned.url

    @property
    def html_parser_find_attributes(self) -> Dict[str, Any]:
        return {"class": "article-title"}

    @property
    def html_parser_find_name(self) -> List[str]:
        return settings.news_config.ihned.article_header_tags

    def get_article_url(self, header: bs4.Tag) -> str:
        article_url = header.find("a").get("href")
        return self.construct_full_url(article_url)

    def get_headers(self) -> List[Article]:
        response = requests.get(self.news_url)
        bs_html_parser = bs(response.text, "html.parser")
        bs_header_arr = bs_html_parser.find_all(
            name=self.html_parser_find_name, attrs=self.html_parser_find_attributes
        )
        article_arr = [
            Article(header=header.get_text(), url=self.get_article_url(header))
            for header in bs_header_arr
        ]
        return article_arr


class BbcScraper(NewsScraper):
    @property
    def html_parser_find_attributes(self) -> Dict[str, Any]:
        return {"class": re.compile(".*title.*")}

    @property
    def html_parser_find_name(self) -> List[str]:
        return settings.news_config.bbc.article_header_tags

    @property
    def news_url(self) -> HttpUrl:
        return settings.news_config.bbc.url

    def get_article_url(self, header: bs4.Tag) -> AnyStr:
        href = header.parent.get("href")
        return self.construct_full_url(href)

    def get_headers(self) -> List[Article]:
        response = requests.get(self.news_url)
        bs_html_parser = bs(response.text, "html.parser")
        bs_header_arr = bs_html_parser.find_all(
            name=self.html_parser_find_name, attrs=self.html_parser_find_attributes
        )
        article_arr = [
            Article(header=header.get_text(), url=self.get_article_url(header))
            for header in bs_header_arr
        ]
        return article_arr
