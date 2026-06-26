# 🔴 Lab 12 — Docker Hub & Container Registries


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Multistage-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-11-multistage-builds.md)
[![Pro_Index](https://img.shields.io/badge/Pro_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/CI%2FCD_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-13-cicd-docker.md)

</div>

---

<div align="center">

**Jump to section:**

[![Registries_Overview](https://img.shields.io/badge/Registries_Overview-2496ED?style=flat-square&logo=docker&logoColor=white)](#registries-overview)
[![Docker_Hub_Push_%26_Pull](https://img.shields.io/badge/Docker_Hub_Push_%26_Pull-2496ED?style=flat-square&logo=docker&logoColor=white)](#docker-hub-push-pull)
[![GitHub_Container_Registry_GH](https://img.shields.io/badge/GitHub_Container_Registry_GH-2496ED?style=flat-square&logo=docker&logoColor=white)](#github-container-registry-ghcr)
[![Semantic_Versioning_with_Tag](https://img.shields.io/badge/Semantic_Versioning_with_Tag-2496ED?style=flat-square&logo=docker&logoColor=white)](#semantic-versioning-with-tags)
[![Automated_Multi-Arch_Builds](https://img.shields.io/badge/Automated_Multi-Arch_Builds-2496ED?style=flat-square&logo=docker&logoColor=white)](#automated-multi-arch-builds)
[![Scanning_Images_for_Vulnerab](https://img.shields.io/badge/Scanning_Images_for_Vulnerab-2496ED?style=flat-square&logo=docker&logoColor=white)](#scanning-images-for-vulnerabilities)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
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
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Multistage-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-11-multistage-builds.md)
[![Pro_Index](https://img.shields.io/badge/Pro_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/CI%2FCD_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-13-cicd-docker.md)

</div>