FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONBUFFERED=1

COPY . .

CMD ["python", "-m", "main"]