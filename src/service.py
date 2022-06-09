"""
Service layer.
"""
import logging
from typing import List

from sqlalchemy.orm import Session

from src.models import ArticleOrm
from src.tasks.news import Article

logger = logging.getLogger(__name__)


def _is_article_new(article: Article, db_session: Session) -> bool:
    """
    Checks whether the article with the given url already exists in database or not
    :param article: Article to check
    :param db_session: DB session instance
    :return: flag if the article exists
    """
    return (
        db_session.query(ArticleOrm).filter(ArticleOrm.url == article.url).first()
        is None
    )


def get_articles_with_keywords(
    keywords: List[str], db_session: Session
) -> List[Article]:
    """
    Returns all articles from DB where at least one of given keywords is in article's header.
    The newest articles will be first. If no keywords were given, should return an empty list.

    :param keywords: List of keywords
    :param db_session: DB session instance
    :return: article list with given keywords present
    """
    articles = db_session.query(ArticleOrm).all()
    keywords_lowercase = list(map(str.lower, keywords))

    return [
        article
        for article in articles
        if not set(article.header.lower().split()).isdisjoint(keywords_lowercase)
    ]


def save_article_if_new(article: Article, db_session: Session) -> Article:
    """Saves an article, if it is not in our DB already. Existence is checked by URL of the article.

    :param article: article to save
    :param db_session: DB session instance
    :return: Saved article
    """
    article_orm: ArticleOrm = article.as_orm()
    if not _is_article_new(article, db_session):
        return article_orm

    db_session.add(article_orm)
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logger.error(f"Exception :: {e}")

    db_session.refresh(article_orm)
    return article_orm
