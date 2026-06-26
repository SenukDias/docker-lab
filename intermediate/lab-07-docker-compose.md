# 🐳 Lab 07 — Docker Compose


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Networking-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../beginner/lab-06-networking.md)
[![Intermediate_Index](https://img.shields.io/badge/Intermediate_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Multi-Container_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-08-multi-container.md)

</div>

---

<div align="center">

**Jump to section:**

[![Why_Compose](https://img.shields.io/badge/Why_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](#why-compose)
[![docker-compose.yml_Structure](https://img.shields.io/badge/docker-compose.yml_Structure-2496ED?style=flat-square&logo=docker&logoColor=white)](#docker-composeyml-structure)
[![Compose_Commands](https://img.shields.io/badge/Compose_Commands-2496ED?style=flat-square&logo=docker&logoColor=white)](#compose-commands)
[![Environment_Variables_%26_.e](https://img.shields.io/badge/Environment_Variables_%26_.e-2496ED?style=flat-square&logo=docker&logoColor=white)](#environment-variables-env-file)
[![Health_Checks_in_Compose](https://img.shields.io/badge/Health_Checks_in_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](#health-checks-in-compose)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
> **Level:** Intermediate | **Time:** ~35 min | **Goal:** Orchestrate multi-container apps

---

## Why Compose?

Managing multiple containers with individual `docker run` commands becomes complex:

```bash
# Without Compose — error-prone, hard to maintain
docker network create app-net
docker run -d --name db --network app-net -e POSTGRES_PASSWORD=secret postgres:16
docker run -d --name redis --network app-net redis:7
docker run -d --name app --network app-net -p 5000:5000 -e DB_URL=... my-app
docker run -d --name nginx --network app-net -p 80:80 nginx
```

With Compose → **one YAML file, one command**.

---

## docker-compose.yml Structure

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - app

  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://admin:secret@db:5432/appdb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

---

## Compose Commands

```bash
# Start all services (build if needed)
docker compose up

# Start in background (detached)
docker compose up -d

# Build images without starting
docker compose build

# Rebuild and restart
docker compose up --build

# Scale a specific service
docker compose up --scale app=3

# View running services
docker compose ps

# View logs (all services)
docker compose logs

# Follow logs for specific service
docker compose logs -f app

# Execute command in a service
docker compose exec app bash

# Stop all services
docker compose down

# Stop and remove volumes (data loss!)
docker compose down -v
```

---

## Environment Variables & .env File

```bash
# .env file (auto-loaded by Compose)
POSTGRES_PASSWORD=mysecretpassword
APP_PORT=5000
NODE_ENV=production
```

```yaml
# docker-compose.yml — references .env
services:
  app:
    environment:
      - NODE_ENV=${NODE_ENV}
      - PORT=${APP_PORT}
  db:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

---

## Health Checks in Compose

```yaml
services:
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build: .
    depends_on:
      db:
        condition: service_healthy   # waits for DB health check
```

---

## 📋 Lab Tasks

1. Write a `docker-compose.yml` with Flask app + PostgreSQL + Redis
2. Use a `.env` file for all passwords/ports
3. Run `docker compose up -d`, verify all services are `running` with `docker compose ps`
4. Run `docker compose logs -f app` while making a request — watch the log entry appear
5. Run `docker compose down -v` then `up` again — confirm data is gone (volumes removed)

> 💡 **Next:** [Lab 08 — Multi-Container App Stack →](lab-08-multi-container.md)
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Networking-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../beginner/lab-06-networking.md)
[![Intermediate_Index](https://img.shields.io/badge/Intermediate_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Multi-Container_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-08-multi-container.md)

</div>