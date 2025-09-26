# bot/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8081
CMD ["uvicorn","bot:app","--host","0.0.0.0","--port","8081"]
