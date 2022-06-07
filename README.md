# Article Web Scraper

Application that periodically scrape news servers and store headers and URL of its articles.
The application stores the data into its own DB, and it publishes a REST API which will allow for browsing 
articles' metadata by keywords. In case a news server is unavailable, the application should handle it gracefully.

## Setup

```bash
# Virtual env creation
python3.8 -m venv .venv

# Dependencies installation
.venv/bin/pip install -U pip
.venv/bin/pip install -U pipenv
.venv/bin/pipenv install

# Run docker container with DB
docker-compose down -t1
docker-compose up -d --build

# Create an empty DB
.venv/bin/python -m app.setup
```

## Launching the whole app

Components:

```bash
.venv/bin/python -m app.scraper
.venv/bin/python -m app.api
```

Testing the REST API:

```bash
curl --request POST 'http://localhost:5000/articles/find' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "keywords": [
            "babiš",
            "prymul"
        ]
    }'
```


## Scraping
- headers and URLs of articles are scraped from: `idnes.cz`, `ihned.cz`, `bbc.com`
    - implement in `app.news`
    - test with `python -m pytest -k news_test`
- it is scraped periodically (e.g. every minute); new articles are stored into DB (check uniqueness of article by its URL)
    - implemented in `app.scraper`
    - tested with `python -m pytest -k scraper_test`
- the following REST API is implemented which will allow to browse the stored articles by keywords
    - implemented in `app.api`
    - tested by HTTP call
    
    `POST /articles/find`

    
        {
            "keywords": ["monkey", "dog", "snail"]
        }
        
    Example result response for these keywords:

        {
            "articles: [
                { "text": "Big monkey got caught in London", "url": "https://www.bbc.com/..." },
                { "text": "Is this dog really cute?", "url": "https://www.bbc.com/..." },
                { "text": "Dog vs Snail – which is better?", "url": "https://www.bbc.com/..." }
            ]
        }
        
## Frameworks and libraries for implementation
- web scraping: `requests`
- ORM: `sqlalchemy`
- web API: `fastapi`
- HTML parsing, REST request validation, scheduling - `beautifulsoup4`
