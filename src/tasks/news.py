"""
News scrapers.
"""
from abc import abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Article:
    """Represents an article from a news server."""

    header: str
    url: str


class NewsScraper:
    @abstractmethod
    def get_headers(self) -> List[Article]:
        """Returns a list of articles from the news server."""


class IdnesScraper(NewsScraper):
    def get_headers(self) -> List[Article]:
        pass  # todo: implement


class IhnedScraper(NewsScraper):
    def get_headers(self) -> List[Article]:
        pass  # todo: implement


class BbcScraper(NewsScraper):
    def get_headers(self) -> List[Article]:
        pass  # todo: implement
