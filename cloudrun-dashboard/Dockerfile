FROM python:3.9-slim

RUN pip install poetry==1.4.2

WORKDIR /cloudrun_dashboard

COPY pyproject.toml poetry.lock ./
COPY cloudrun_dashboard ./cloudrun_dashboard
RUN touch README.md

RUN poetry install --without dev

EXPOSE 8080

ENTRYPOINT ["poetry", "run", "streamlit", "run", "cloudrun_dashboard/app.py"]