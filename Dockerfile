FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends procps iproute2 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -r bot && mkdir -p results && chown bot results
USER bot
EXPOSE 8000
CMD ["uvicorn", "runbookbot.server:app", "--host", "0.0.0.0", "--port", "8000"]
