FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5052

CMD ["gunicorn", "-b", "0.0.0.0:5052", "app:app"]
