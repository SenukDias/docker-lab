# 🔴 Lab 12 — Docker Hub & Container Registries

> **Level:** Pro | **Time:** ~30 min | **Goal:** Push, pull, and manage images in registries

---

## Registries Overview

| Registry | URL | Free | Best For |
|----------|-----|------|---------|
| Docker Hub | hub.docker.com | 1 private repo | Public images |
| GitHub GHCR | ghcr.io | Unlimited (public) | GitHub-integrated projects |
| AWS ECR | *.ecr.amazonaws.com | Pay-per-use | AWS workloads |
| Azure ACR | *.azurecr.io | Pay-per-use | Azure workloads |
| GCP Artifact Registry | *.pkg.dev | Pay-per-use | GCP workloads |

---

## Docker Hub — Push & Pull

```bash
# Login
docker login
# Enter Docker Hub username and password/PAT

# Tag image for Docker Hub
docker tag flask-app:v1 yourusername/flask-app:v1
docker tag flask-app:v1 yourusername/flask-app:latest

# Push to Docker Hub
docker push yourusername/flask-app:v1
docker push yourusername/flask-app:latest

# Pull from Docker Hub
docker pull yourusername/flask-app:v1

# Pull on any machine (public repo)
docker run -p 5000:5000 yourusername/flask-app:v1
```

---

## GitHub Container Registry (GHCR)

```bash
# Login with GitHub PAT (needs write:packages scope)
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Tag for GHCR
docker tag flask-app:v1 ghcr.io/USERNAME/flask-app:v1

# Push
docker push ghcr.io/USERNAME/flask-app:v1

# Pull
docker pull ghcr.io/USERNAME/flask-app:v1
```

---

## Semantic Versioning with Tags

```bash
# Best practice: always tag with specific version AND latest
docker build -t myapp:1.2.3 .
docker tag myapp:1.2.3 myapp:1.2
docker tag myapp:1.2.3 myapp:1
docker tag myapp:1.2.3 myapp:latest

# GitSHA tag for traceability
GIT_SHA=$(git rev-parse --short HEAD)
docker build -t myapp:$GIT_SHA .
docker tag myapp:$GIT_SHA myapp:latest
```

---

## Automated Multi-Arch Builds

```bash
# Setup buildx (multi-architecture builder)
docker buildx create --name multiarch --use
docker buildx inspect --bootstrap

# Build for multiple architectures (amd64 + arm64)
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag yourusername/flask-app:v1 \
  --push \
  .
```

---

## Scanning Images for Vulnerabilities

```bash
# Docker Scout (built in to Docker Desktop)
docker scout cves flask-app:v1
docker scout recommendations flask-app:v1

# Trivy (open source)
trivy image flask-app:v1

# Snyk
snyk container test flask-app:v1
```

---

## 📋 Lab Tasks

1. Push your Flask image to Docker Hub with both `:v1` and `:latest` tags
2. Pull the image on a different terminal/machine and run it
3. Tag with your git SHA: `$(git rev-parse --short HEAD)` — push it
4. Run `docker scout cves` or `trivy image` — identify any HIGH/CRITICAL CVEs

> 💡 **Next:** [Lab 13 — CI/CD with Docker →](lab-13-cicd-docker.md)
