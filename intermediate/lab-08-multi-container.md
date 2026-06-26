# 🐳 Lab 08 — Multi-Container App Stack


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-07-docker-compose.md)
[![Intermediate_Index](https://img.shields.io/badge/Intermediate_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Environment_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-09-environment.md)

</div>

---

<div align="center">

**Jump to section:**

[![Architecture](https://img.shields.io/badge/Architecture-2496ED?style=flat-square&logo=docker&logoColor=white)](#architecture)
[![Project_Structure](https://img.shields.io/badge/Project_Structure-2496ED?style=flat-square&logo=docker&logoColor=white)](#project-structure)
[![Flask_Application](https://img.shields.io/badge/Flask_Application-2496ED?style=flat-square&logo=docker&logoColor=white)](#flask-application)
[![Dockerfile](https://img.shields.io/badge/Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white)](#dockerfile)
[![Nginx_Configuration](https://img.shields.io/badge/Nginx_Configuration-2496ED?style=flat-square&logo=docker&logoColor=white)](#nginx-configuration)
[![docker-compose.yml](https://img.shields.io/badge/docker-compose.yml-2496ED?style=flat-square&logo=docker&logoColor=white)](#docker-composeyml)
[![Deploy_the_Stack](https://img.shields.io/badge/Deploy_the_Stack-2496ED?style=flat-square&logo=docker&logoColor=white)](#deploy-the-stack)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
> **Level:** Intermediate | **Time:** ~45 min | **Goal:** Build a real Flask + Redis + Nginx stack

---

## Architecture

```
Browser → Nginx (port 80) → Flask App (port 5000) → Redis (port 6379)
                              ↕
                         PostgreSQL (port 5432)
```

---

## Project Structure

```
fullstack-app/
├── app/
│   ├── app.py
│   └── requirements.txt
├── nginx/
│   └── nginx.conf
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## Flask Application

`app/app.py`:
```python
from flask import Flask, jsonify
import redis
import psycopg2
import os

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_db():
    return psycopg2.connect(os.environ['DATABASE_URL'])

@app.route('/')
def index():
    visits = r.incr('visits')
    return jsonify({
        "message": "Hello from Docker Stack! 🐳",
        "visits": visits,
        "service": "Flask"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

`app/requirements.txt`:
```
flask==3.0.0
redis==5.0.1
psycopg2-binary==2.9.9
```

---

## Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## Nginx Configuration

`nginx/nginx.conf`:
```nginx
server {
    listen 80;

    location / {
        proxy_pass http://app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /health {
        proxy_pass http://app:5000/health;
    }
}
```

---

## docker-compose.yml

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - app

  app:
    build: .
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASS}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

`.env`:
```
DB_NAME=appdb
DB_USER=admin
DB_PASS=secret123
```

---

## Deploy the Stack

```bash
# Build and start everything
docker compose up --build -d

# Verify all services are healthy
docker compose ps

# Test the app
curl http://localhost
curl http://localhost  # visit counter increments
curl http://localhost/health
```

---

## 📋 Lab Tasks

1. Build the full stack above
2. Make 5 requests to `/` — verify the visit counter increments
3. Restart only the `app` service: `docker compose restart app` — verify Redis counter survives
4. Add a new endpoint `/metrics` that returns container hostname — test it

> 💡 **Next:** [Lab 09 — Environment & Secrets →](lab-09-environment.md)
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-07-docker-compose.md)
[![Intermediate_Index](https://img.shields.io/badge/Intermediate_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Environment_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-09-environment.md)

</div>