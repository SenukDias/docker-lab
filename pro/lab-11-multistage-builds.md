# 🔴 Lab 11 — Multi-Stage Builds


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Debugging-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../intermediate/lab-10-debugging.md)
[![Pro_Index](https://img.shields.io/badge/Pro_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Docker_Hub_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-12-docker-hub.md)

</div>

---

<div align="center">

**Jump to section:**

[![The_Problem_with_Single-Stag](https://img.shields.io/badge/The_Problem_with_Single-Stag-2496ED?style=flat-square&logo=docker&logoColor=white)](#the-problem-with-single-stage-builds)
[![Multi-Stage_Build_Pattern](https://img.shields.io/badge/Multi-Stage_Build_Pattern-2496ED?style=flat-square&logo=docker&logoColor=white)](#multi-stage-build-pattern)
[![Node.js_Multi-Stage](https://img.shields.io/badge/Node.js_Multi-Stage-2496ED?style=flat-square&logo=docker&logoColor=white)](#nodejs-multi-stage)
[![Go_True_Static_Binary](https://img.shields.io/badge/Go_True_Static_Binary-2496ED?style=flat-square&logo=docker&logoColor=white)](#go-true-static-binary)
[![Build_Secrets_BuildKit](https://img.shields.io/badge/Build_Secrets_BuildKit-2496ED?style=flat-square&logo=docker&logoColor=white)](#build-secrets-buildkit)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
> **Level:** Pro | **Time:** ~35 min | **Goal:** Create slim, secure production images

---

## The Problem with Single-Stage Builds

```dockerfile
# Single-stage — includes compilers, dev dependencies, source code
FROM python:3.11          # 900MB base
COPY . .
RUN pip install build-tools ...
RUN python setup.py build  # compiles native extensions
CMD ["python", "app.py"]

# Final image: 1.2GB — includes everything used during build
```

---

## Multi-Stage Build Pattern

```dockerfile
# Stage 1: Build
FROM python:3.11 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY . .
RUN python -m compileall app/    # compile to .pyc

# Stage 2: Production image (only runtime, no build tools)
FROM python:3.11-slim AS production
WORKDIR /app

# Copy only what's needed from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /build/app ./app

# Security: run as non-root user
RUN useradd -r -s /bin/false appuser
USER appuser

EXPOSE 5000
CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:5000", "app.main:app"]
```

Build and compare:
```bash
docker build --target builder    -t myapp:dev  .
docker build --target production -t myapp:prod .
docker images myapp
# dev:  ~1.1GB
# prod: ~145MB
```

---

## Node.js Multi-Stage

```dockerfile
# Stage 1: Build TypeScript
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build           # transpile TS → JS

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production  # no devDependencies
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

---

## Go — True Static Binary

```dockerfile
# Stage 1: Compile
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/server .

# Stage 2: Scratch (0MB base image!)
FROM scratch AS production
COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
ENTRYPOINT ["/server"]
```

Go binary image: ~8MB vs ~1.1GB build image.

---

## Build Secrets (BuildKit)

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Dockerfile — mount secret (never stored in layer)
RUN --mount=type=secret,id=npmrc cat /run/secrets/npmrc > ~/.npmrc && \
    npm install && \
    rm ~/.npmrc
```

```bash
# Build with secret
docker build --secret id=npmrc,src=.npmrc -t myapp .
```

---

## 📋 Lab Tasks

1. Convert your Flask Dockerfile to multi-stage — measure image size difference
2. Build with `--target builder` and inspect its size vs final image
3. Add a non-root `USER` to your production image — verify with `docker exec whoami`

> 💡 **Next:** [Lab 12 — Docker Hub →](lab-12-docker-hub.md)
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Debugging-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../intermediate/lab-10-debugging.md)
[![Pro_Index](https://img.shields.io/badge/Pro_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Docker_Hub_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-12-docker-hub.md)

</div>