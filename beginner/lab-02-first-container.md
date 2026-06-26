# 🐳 Lab 02 — Your First Container

> **Level:** Beginner | **Time:** ~25 min | **Goal:** Run, manage, and understand containers

---

<div align="center">

<!-- ── Top navigation ── -->
[![← Lab 01](https://img.shields.io/badge/←_Lab_01-Installation-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-01-installation.md)
[![Beginner Track](https://img.shields.io/badge/Beginner_Track-Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Lab 03 →](https://img.shields.io/badge/Lab_03_→-Dockerfile-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-03-dockerfile.md)

</div>

---

<div align="center">

**Jump to section:**

[![Core Commands](https://img.shields.io/badge/Core_Commands-2496ED?style=flat-square&logo=docker&logoColor=white)](#core-container-commands)
[![Lifecycle](https://img.shields.io/badge/Lifecycle-2496ED?style=flat-square&logo=docker&logoColor=white)](#container-lifecycle)
[![Port Mapping](https://img.shields.io/badge/Port_Mapping-2496ED?style=flat-square&logo=docker&logoColor=white)](#port-mapping)
[![Naming](https://img.shields.io/badge/Naming_Containers-2496ED?style=flat-square&logo=docker&logoColor=white)](#naming-containers)
[![Inspect](https://img.shields.io/badge/Inspect-2496ED?style=flat-square&logo=docker&logoColor=white)](#inspect-a-container)
[![Stats](https://img.shields.io/badge/Stats_%26_Monitoring-2496ED?style=flat-square&logo=docker&logoColor=white)](#container-stats--monitoring)
[![Cleanup](https://img.shields.io/badge/Cleanup-2496ED?style=flat-square&logo=docker&logoColor=white)](#cleanup-commands)
[![Lab Tasks](https://img.shields.io/badge/📋_Lab_Tasks-0ea5e9?style=flat-square&logo=docker&logoColor=white)](#-lab-tasks)

</div>

---

## Core Container Commands

```bash
# Pull an image from Docker Hub
docker pull nginx

# Run a container (detached, port mapped)
docker run -d -p 8080:80 --name my-nginx nginx

# List running containers
docker ps

# List ALL containers (including stopped)
docker ps -a

# View container logs
docker logs my-nginx

# Follow logs in real-time
docker logs -f my-nginx

# Execute a command inside running container
docker exec -it my-nginx bash

# Stop a container (graceful, sends SIGTERM)
docker stop my-nginx

# Start a stopped container
docker start my-nginx

# Restart a container
docker restart my-nginx

# Remove a container (must be stopped)
docker rm my-nginx

# Remove a running container (force)
docker rm -f my-nginx
```

---

## Container Lifecycle

```
docker run → Created → Running → Stopped → Removed
               ↑                    ↑
            docker start        docker stop
```

---

## Port Mapping

```bash
# -p HOST_PORT:CONTAINER_PORT
docker run -d -p 8080:80 nginx   # localhost:8080 → container:80
docker run -d -p 3000:3000 node  # localhost:3000 → container:3000
docker run -d -p 5432:5432 postgres

# Random host port
docker run -d -p 80 nginx        # Docker assigns random host port
docker port <container_id>       # See the mapping
```

---

## Naming Containers

```bash
# Always name your containers for easy reference
docker run -d --name webserver -p 8080:80 nginx
docker run -d --name database -p 5432:5432 postgres

# Without --name, Docker assigns random names like "flamboyant_tesla"
```

---

## Inspect a Container

```bash
# Full JSON metadata
docker inspect my-nginx

# Specific field using Go template
docker inspect --format='{{.NetworkSettings.IPAddress}}' my-nginx
docker inspect --format='{{.State.Status}}' my-nginx
```

---

## Container Stats & Monitoring

```bash
# Live resource usage (CPU, RAM, Network, I/O)
docker stats

# Stats for a specific container
docker stats my-nginx

# One-shot (no stream)
docker stats --no-stream
```

---

## Cleanup Commands

```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune

# Remove EVERYTHING unused (containers, images, networks, volumes)
docker system prune -a

# Check disk usage
docker system df
```

---

## 📋 Lab Tasks

1. Pull the `nginx` image and run it on port `8080`
2. Open `http://localhost:8080` in your browser — see the Nginx welcome page
3. Run `docker logs my-nginx` and identify the access log entry
4. `exec` into the container and find the HTML file: `cat /usr/share/nginx/html/index.html`
5. Stop and remove the container, then verify `docker ps -a` shows nothing

> 💡 **Next:** [Lab 03 — Writing a Dockerfile →](lab-03-dockerfile.md)

---

<div align="center">

[![← Lab 01](https://img.shields.io/badge/←_Lab_01-Installation-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-01-installation.md)
[![Beginner Index](https://img.shields.io/badge/Beginner_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Lab 03 →](https://img.shields.io/badge/Lab_03_→-Dockerfile-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-03-dockerfile.md)

</div>
