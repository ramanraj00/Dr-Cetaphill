FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy project
COPY . .

# Install python deps
RUN pip install fastapi uvicorn httpx

# Pull model
RUN ollama pull phi3

EXPOSE 8000

CMD ollama serve & uvicorn main:app --host 0.0.0.0 --port 8000