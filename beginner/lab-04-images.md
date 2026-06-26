# 🐳 Lab 04 — Images & Layers

> **Level:** Beginner | **Time:** ~25 min | **Goal:** Understand image layers, tags, and optimization

---

## How Docker Images Work

Images are **read-only stacked layers**. Each instruction in a Dockerfile adds a layer:

```
Layer 5: COPY . .             ← your code
Layer 4: RUN pip install      ← dependencies
Layer 3: COPY requirements.txt
Layer 2: WORKDIR /app
Layer 1: FROM python:3.11-slim ← base OS + Python
```

Layers are **cached and shared** between images that share the same base.

---

## Image Commands

```bash
# List all local images
docker images
docker image ls

# Pull a specific tag
docker pull ubuntu:22.04
docker pull node:20-alpine
docker pull python:3.11-slim

# Show image layers (history)
docker history flask-app:v1

# Inspect image metadata (JSON)
docker image inspect flask-app:v1

# Tag an existing image
docker tag flask-app:v1 flask-app:latest
docker tag flask-app:v1 myusername/flask-app:v1

# Remove an image
docker rmi flask-app:v1
docker image rm flask-app:v1

# Remove all unused images
docker image prune -a
```

---

## Image Naming Convention

```
[registry/][username/]image-name[:tag]

docker.io/library/nginx:latest       # Official Docker Hub image
docker.io/username/my-app:v2.0       # User image on Docker Hub
ghcr.io/orgname/api:sha-abc123       # GitHub Container Registry
myregistry.com:5000/app:production   # Private registry
```

---

## Choosing the Right Base Image

| Base | Size | Use Case |
|------|------|---------|
| `python:3.11` | ~900MB | Dev, needs compilers |
| `python:3.11-slim` | ~125MB | Production Python |
| `python:3.11-alpine` | ~55MB | Smallest, musl libc |
| `node:20` | ~950MB | Dev |
| `node:20-alpine` | ~125MB | Production Node.js |
| `ubuntu:22.04` | ~77MB | General purpose |
| `debian:bookworm-slim` | ~74MB | Lean Debian |
| `scratch` | 0MB | Static binaries only |

---

## Build Cache Optimization

```bash
# Build with cache (default)
docker build -t myapp .

# Build with no cache
docker build --no-cache -t myapp .

# Build with specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build args
docker build --build-arg VERSION=2.0 -t myapp:2.0 .

# Show build progress
docker build --progress=plain -t myapp .
```

---

## Dive Tool — Inspect Image Layers

```bash
# Install dive (image layer explorer)
# macOS: brew install dive
# Linux: https://github.com/wagoodman/dive

dive flask-app:v1
```

---

## 📋 Lab Tasks

1. Run `docker history flask-app:v1` — identify what each layer does
2. Compare sizes: `docker images python:3.11` vs `python:3.11-slim` vs `python:3.11-alpine`
3. Rebuild your Dockerfile by intentionally putting `COPY . .` before `pip install` — measure the difference when you change one line of code
4. Tag your image as `yourusername/flask-app:v1` (don't push yet — we'll do that in Lab 12)

> 💡 **Next:** [Lab 05 — Volumes & Persistent Storage →](lab-05-volumes.md)
