FROM python:3.11-buster

RUN pip install poetry==1.4.2

WORKDIR /apoenastack_api

COPY pyproject.toml poetry.lock ./
COPY apoenastack_api ./apoenastack_api
RUN touch README.md

RUN poetry install --without dev

EXPOSE 8080

ENTRYPOINT ["poetry", "run", "fastapi", "run", "apoenastack_api/app.py", "--port", "8080"]