import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from starlette import status
from starlette.requests import Request

from src import db, responses
from src.config.settings import get_settings
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


@app.post("/articles/find")
async def find_articles() -> JSONResponse:
    """
    If query in request.json is not valid, returns HTTP 422.
    If query is valid, returns result with articles matching given keywords.
    """
    # todo: implement validation of data received in request.json, get keywords from the query
    # keywords: List[str] = []
    # todo: implement searching for articles by keywords in app.service.get_articles_with_keywords() and
    #  use it below. If no keywords were given, should return an empty list.
    return responses.success_response(
        {
            "articles": [
                # {"text": i.header, "url": i.url}
                # for i in get_articles_with_keywords(keywords)
            ]
        }
    )


# exception handling
@app.exception_handler(RequestValidationError)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"{exc}")
    return responses.error_response(
        errors=str(exc), status_code=status.HTTP_400_BAD_REQUEST
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
