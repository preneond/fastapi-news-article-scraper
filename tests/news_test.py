import re

from src.tasks.news import BbcScraper, IdnesScraper, IhnedScraper, NewsScraper


def check_provider(provider: NewsScraper) -> None:
    articles = provider.get_headers()
    assert len(articles) > 0
    for a in articles:
        assert len(a.header) > 0
        assert a.header.strip() == a.header
        assert re.fullmatch(r"http(s)?://.*", a.url)


def test_idnes() -> None:
    check_provider(IdnesScraper())


def test_ihned() -> None:
    check_provider(IhnedScraper())


def test_bbc() -> None:
    check_provider(BbcScraper())
