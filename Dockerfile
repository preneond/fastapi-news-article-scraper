# set line break type to LF
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

MAINTAINER ondra.prenek@gmail.com

COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src /app/src
COPY appsettings.yaml /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 80

WORKDIR /app

# Sleep few seconds to wait for DB to init
CMD sleep 5 && python src/api.py