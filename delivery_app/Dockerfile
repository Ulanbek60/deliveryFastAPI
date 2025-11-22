FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /delivery_app

COPY req.txt /delivery_app/
RUN pip install -r req.txt && \
    pip install --upgrade pip \

COPY . /delivery_app/