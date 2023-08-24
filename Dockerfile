FROM python:3.10.12-alpine3.18

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]