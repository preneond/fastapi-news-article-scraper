FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

MAINTAINER ondra.prenek@gmail.com

COPY ./src /app/src
COPY Pipfile /app
COPY Pipfile.lock /app
COPY appsettings.yaml /app

WORKDIR /app
ENV PYTHONPATH=/app

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy

EXPOSE 80

CMD ["uvicorn", "src.api:app"]
