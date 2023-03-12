FROM python:3.8.16-buster

RUN set -e \
    && pip install pipenv

WORKDIR /opt/api
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

COPY main.py ./
ADD src ./src
ADD bin ./bin

EXPOSE 8000
CMD ./bin/entrypoint.sh
