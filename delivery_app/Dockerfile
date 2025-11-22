FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /delivery_app

COPY req.txt .
RUN pip install --upgrade pip && \
    pip install -r req.txt

COPY . .

CMD ["uvicorn", "main:delivery", "--host", "0.0.0.0", "--port", "8001"]
