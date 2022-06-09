# from typing import List
#
# import pytest as pytest
#
# from src import db
# from src.models import ArticleOrm
# from src.tasks import news, scraper
#
#
# class FakeScraper(news.NewsScraper):
#     def get_headers(self) -> List[news.Article]:
#         return [
#             news.Article(header="a", url="some-url"),
#             news.Article(header="b", url="some-url"),
#         ]
#
#
# class FailingScraper(news.NewsScraper):
#     def get_headers(self) -> List[news.Article]:
#         raise Exception("Error when scraping")
#
# def test_scrape_news() -> None:
#     # mock news scrapers and clean DB
#     scraper.SCRAPERS = [FakeScraper(), FailingScraper()]
#     db.create_empty_db()
#
#     # test
#     for sc in scraper.SCRAPERS:
#         scraper.scrape_news(sc, db.session())
#
#     # check
#     articles = db.session.query(ArticleOrm).all()
#     assert len(articles) == 1
#     article = articles[0]
#     assert article.header == "a"
#     assert article.url == "some-url"
