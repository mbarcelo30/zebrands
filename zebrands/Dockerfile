FROM python:3.10.8

RUN pip install --upgrade pip
RUN pip install pipenv

ENV PROJECT_DIR /code
WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
RUN pipenv install --system --deploy
RUN pip install psycopg2-binary
