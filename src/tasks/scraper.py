"""
Web scraping service.
"""
import logging

from sqlalchemy.orm import Session

from src import db
from src.service import save_article_if_new
from src.tasks.news import BbcScraper, IdnesScraper, IhnedScraper, NewsScraper

logger = logging.getLogger(__name__)

SCRAPERS = [IdnesScraper(), IhnedScraper(), BbcScraper()]


def scrape_news(scraper: NewsScraper, db_session: Session) -> None:
    """Gets articles from news servers and saves new ones into our DB.
    If any scraper fails, it must be logged but continue in operation.
    """
    logger.info(f"Scraping news using {type(scraper).__name__}")

    try:
        article_arr = scraper.get_headers()
        for article in article_arr:
            save_article_if_new(article, db_session)
    except Exception as e:
        logger.error(f"Scraping Exception:: {e}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{asctime} {levelname:<8} {name}:{module}:{lineno} - {message}",
        style="{",
    )
    db.create_empty_db()
    for sc in SCRAPERS:
        scrape_news(sc, db.session())
