# 🐳 Lab 05 — Volumes & Persistent Storage


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Images-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-04-images.md)
[![Beginner_Index](https://img.shields.io/badge/Beginner_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Networking_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-06-networking.md)

</div>

---

<div align="center">

**Jump to section:**

[![The_Problem_Containers_Are_E](https://img.shields.io/badge/The_Problem_Containers_Are_E-2496ED?style=flat-square&logo=docker&logoColor=white)](#the-problem-containers-are-ephemeral)
[![Three_Types_of_Mounts](https://img.shields.io/badge/Three_Types_of_Mounts-2496ED?style=flat-square&logo=docker&logoColor=white)](#three-types-of-mounts)
[![Named_Volumes](https://img.shields.io/badge/Named_Volumes-2496ED?style=flat-square&logo=docker&logoColor=white)](#named-volumes)
[![Bind_Mounts_Live_Code_Reload](https://img.shields.io/badge/Bind_Mounts_Live_Code_Reload-2496ED?style=flat-square&logo=docker&logoColor=white)](#bind-mounts-live-code-reload)
[![Database_with_Persistent_Vol](https://img.shields.io/badge/Database_with_Persistent_Vol-2496ED?style=flat-square&logo=docker&logoColor=white)](#database-with-persistent-volume)
[![Volume_in_Dockerfile](https://img.shields.io/badge/Volume_in_Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white)](#volume-in-dockerfile)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
> **Level:** Beginner | **Time:** ~25 min | **Goal:** Persist data beyond container lifecycle

---

## The Problem: Containers Are Ephemeral

```bash
# Any data written inside a container is LOST when the container is removed
docker run -it ubuntu bash
echo "Hello" > /tmp/data.txt
exit
docker rm <container_id>
# /tmp/data.txt is gone forever!
```

**Volumes** solve this by mounting storage outside the container's filesystem.

---

## Three Types of Mounts

| Type | Syntax | Managed by | Use Case |
|------|--------|-----------|---------|
| **Named Volume** | `-v mydata:/app/data` | Docker | DB data, app state |
| **Bind Mount** | `-v $(pwd):/app` | Host OS | Dev (live code changes) |
| **tmpfs Mount** | `--tmpfs /tmp` | Memory | Secrets, temp files |

---

## Named Volumes

```bash
# Create a named volume
docker volume create mydata

# List volumes
docker volume ls

# Use a volume in a container
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:16

# Inspect a volume
docker volume inspect postgres-data

# Remove a volume (data is permanently deleted!)
docker volume rm mydata

# Remove all unused volumes
docker volume prune
```

---

## Bind Mounts — Live Code Reload

```bash
# Mount current directory into container
docker run -d \
  -p 5000:5000 \
  -v $(pwd):/app \          # Linux/Mac
  flask-app:v1

# Windows PowerShell
docker run -d `
  -p 5000:5000 `
  -v ${PWD}:/app `
  flask-app:v1

# Now edit app.py on your host — changes reflect immediately inside the container
```

---

## Database with Persistent Volume

```bash
# Start PostgreSQL with persistent data
docker run -d \
  --name mydb \
  -e POSTGRES_DB=labdb \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

# Connect and create a table
docker exec -it mydb psql -U admin -d labdb
CREATE TABLE users (id SERIAL, name TEXT);
INSERT INTO users(name) VALUES ('Alice');
\q

# Remove and recreate container — data survives!
docker rm -f mydb
docker run -d --name mydb \
  -e POSTGRES_DB=labdb \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

docker exec -it mydb psql -U admin -d labdb -c "SELECT * FROM users;"
# Alice is still there!
```

---

## Volume in Dockerfile

```dockerfile
# Declare a volume (creates anonymous volume at runtime if not mounted)
FROM python:3.11-slim
WORKDIR /app
VOLUME /app/data    # Docker auto-creates an anonymous volume here
```

---

## 📋 Lab Tasks

1. Run PostgreSQL with a named volume, insert data, delete container, recreate — verify data persists
2. Use a bind mount with your Flask app — change `app.py` text and refresh the browser without rebuilding
3. Run `docker volume ls` and `docker volume inspect` — understand where the data is stored on host

> 💡 **Next:** [Lab 06 — Docker Networking →](lab-06-networking.md)
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Images-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-04-images.md)
[![Beginner_Index](https://img.shields.io/badge/Beginner_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Networking_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-06-networking.md)

</div>