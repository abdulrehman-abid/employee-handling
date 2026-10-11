FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change 'API' to match the exact name of your python file containing FastAPI()
CMD ["sh", "-c", "uvicorn API:app --host 0.0.0.0 --port ${PORT:-8000}"]