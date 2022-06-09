from src import db, service
from src.models import ArticleOrm


def test_get_articles_with_keywords() -> None:
    # setup
    db.create_empty_db()
    db.session.add(ArticleOrm(header="a b c", url=""))
    db.session.add(ArticleOrm(header="b c d", url=""))
    db.session.add(ArticleOrm(header="x y z", url=""))
    db.session.commit()

    # test
    assert not service.get_articles_with_keywords(
        keywords=["aaa"], db_session=db.session()
    )

    assert (
        service.get_articles_with_keywords(keywords=["a"], db_session=db.session())[
            0
        ].header
        == "a b c"
    )
    assert (
        service.get_articles_with_keywords(keywords=["d"], db_session=db.session())[
            0
        ].header
        == "b c d"
    )
    assert (
        service.get_articles_with_keywords(keywords=["y"], db_session=db.session())[
            0
        ].header
        == "x y z"
    )

    assert "a b c" in [
        a.header
        for a in service.get_articles_with_keywords(
            keywords=["b", "c"], db_session=db.session()
        )
    ]
    assert "b c d" in [
        a.header
        for a in service.get_articles_with_keywords(
            keywords=["b", "c"], db_session=db.session()
        )
    ]
