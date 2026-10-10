FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py heart_engine.py keys.py ./
RUN useradd -m heart && chown -R heart /app
USER heart
EXPOSE 8501
HEALTHCHECK CMD curl -fsS http://localhost:8501/_stcore/health || exit 1
CMD ["streamlit", "run", "app.py", "--server.headless", "true", "--server.address", "0.0.0.0", "--server.port", "8501"]
