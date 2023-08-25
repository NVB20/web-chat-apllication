FROM python:3.10.12-alpine3.18

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt && \
    rm -rf test_requirements.txt && \
    rm -rf /var/cache/apk/* && \
    rm -rf /root/.cache

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]