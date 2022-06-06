"""
Web scraping service.
"""
import logging

from app.news import IdnesScraper, IhnedScraper, BbcScraper

logger = logging.getLogger(__name__)
SCRAPERS = [IdnesScraper(), IhnedScraper(), BbcScraper()]


def scrape_news():
    """Gets articles from news servers and saves new ones into our DB.
    If any scraper fails, it must be logged but continue in operation.
    """
    for scraper in SCRAPERS:
        logger.info(f"Scraping news using {type(scraper).__name__}")
        # todo implement logic using already implemented scrapers and app.service.save_article_if_new()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='{asctime} {levelname:<8} {name}:{module}:{lineno} - {message}',
                        style='{')
    # todo: implement regular calling of scrape_news()
