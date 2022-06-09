import logging

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from starlette import status

from src import db, responses, schemas
from src.config.settings import get_settings
from src.db import get_db_session
from src.schemas import FindArticleRequest
from src.service import get_articles_with_keywords
from src.tasks import scraper

settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.api_config.title,
    description=settings.api_config.description,
    version=settings.api_config.version,
    docs_url=settings.api_config.docs_url,
)


@app.on_event("startup")
async def startup_event() -> None:
    # setup db
    db.create_empty_db()
    app.state.db_session = db.session


@app.on_event("shutdown")
async def shutdown_event() -> None:
    app.state.db_session.remove()


@app.on_event("startup")
@repeat_every(seconds=60)
async def periodic_article_fetcher_event() -> None:
    logger.debug("fetching news..")
    for sc in scraper.SCRAPERS:
        scraper.scrape_news(sc, app.state.db_session())


@app.post("/articles/find", response_model=schemas.ArticleListResponse)
async def find_articles(
    data_in: FindArticleRequest, db_session: Session = Depends(get_db_session)
) -> JSONResponse:
    """
    Searches for articles by keywords
    If query in request is not valid, returns HTTP 422.
    If query is valid, returns result with articles matching given keywords.

    :param data_in: keywords to filter the articles by
    :param db_session: DB session instance
    :returns filtered articles by given keywords
    """
    return responses.success_response(
        {
            "articles": [
                schemas.ArticleItemResponse(text=i.header, url=i.url)
                for i in get_articles_with_keywords(data_in.keywords, db_session)
            ]
        }
    )


# exception handling
@app.exception_handler(RequestValidationError)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"App exception:: {exc}")
    return responses.error_response(
        errors=str(exc), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


if __name__ == "__main__":
    settings = get_settings()
    server = settings.uvicorn
    uvicorn.run(
        app="api:app",
        host=server.host,
        port=server.port,
        log_level=server.log_level,
        reload=server.reload,
    )
