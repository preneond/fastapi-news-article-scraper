"""
Service layer.
"""
import logging
from typing import List

from src.core.models import Article

logger = logging.getLogger(__name__)


def get_articles_with_keywords(keywords: List[str]) -> List[Article]:
    """
    Returns all articles from DB where at least one of given keywords is in article's header.
    The newest articles will be first. If no keywords were given, should return an empty list.
    """
    # TODO: implement using db.session.query()


def save_article_if_new(a: Article) -> None:
    """Saves an article, if it is not in our DB already. Existence is checked by URL of the article."""
    # TODO: implement using db.session.query(), db.session.add(), db.session.commit() etc.
