FROM python:3.12.1-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY ./ ./

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --without lint,format,test,dev

CMD [ "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8888" ]
