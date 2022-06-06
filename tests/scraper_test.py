from typing import List

from src.core import db, news, scraper
from src.core.model import Article


class FakeScraper(news.NewsScraper):
    def get_headers(self) -> List[news.Article]:
        return [
            news.Article(header="a", url="some-url"),
            news.Article(header="b", url="some-url"),
        ]


class FailingScraper(news.NewsScraper):
    def get_headers(self) -> List[news.Article]:
        raise Exception("Error when scraping")


def test_scrape_news() -> None:
    # mock news scrapers and clean DB
    scraper.SCRAPERS = [FakeScraper(), FailingScraper()]
    db.create_empty_db()

    # test
    scraper.scrape_news()

    # check
    articles = db.session.query(Article).all()
    assert len(articles) == 1
    article = articles[0]
    assert article.header == "a"
    assert article.url == "some-url"
