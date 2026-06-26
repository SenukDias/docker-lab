# 🔴 Lab 14 — Docker Security


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_CI%2FCD-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-13-cicd-docker.md)
[![Pro_Index](https://img.shields.io/badge/Pro_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)

</div>

---

<div align="center">

**Jump to section:**

[![Security_Checklist](https://img.shields.io/badge/Security_Checklist-2496ED?style=flat-square&logo=docker&logoColor=white)](#security-checklist)
[![1._Non-Root_User](https://img.shields.io/badge/1._Non-Root_User-2496ED?style=flat-square&logo=docker&logoColor=white)](#1-non-root-user)
[![2._Read-Only_Filesystem](https://img.shields.io/badge/2._Read-Only_Filesystem-2496ED?style=flat-square&logo=docker&logoColor=white)](#2-read-only-filesystem)
[![3._Resource_Limits](https://img.shields.io/badge/3._Resource_Limits-2496ED?style=flat-square&logo=docker&logoColor=white)](#3-resource-limits)
[![4._Drop_Linux_Capabilities](https://img.shields.io/badge/4._Drop_Linux_Capabilities-2496ED?style=flat-square&logo=docker&logoColor=white)](#4-drop-linux-capabilities)
[![5._Secrets_Never_in_ENV_or_L](https://img.shields.io/badge/5._Secrets_Never_in_ENV_or_L-2496ED?style=flat-square&logo=docker&logoColor=white)](#5-secrets-never-in-env-or-layers)
[![6._Image_Scanning_in_CI](https://img.shields.io/badge/6._Image_Scanning_in_CI-2496ED?style=flat-square&logo=docker&logoColor=white)](#6-image-scanning-in-ci)
[![7._Content_Trust_Sign_Images](https://img.shields.io/badge/7._Content_Trust_Sign_Images-2496ED?style=flat-square&logo=docker&logoColor=white)](#7-content-trust-sign-images)
[![Security_Benchmark](https://img.shields.io/badge/Security_Benchmark-2496ED?style=flat-square&logo=docker&logoColor=white)](#security-benchmark)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
> **Level:** Pro | **Time:** ~40 min | **Goal:** Harden containers for production

---

## Security Checklist

| Area | Best Practice |
|------|--------------|
| Images | Use minimal base (slim/alpine), scan for CVEs |
| Users | Never run as root — use `USER appuser` |
| Secrets | Use Docker secrets or env-files, never bake into layers |
| Networking | Limit exposed ports, use custom networks |
| Capabilities | Drop all Linux capabilities, add only needed |
| Read-only FS | Use `--read-only` flag |
| Resource limits | Set memory + CPU limits |

---

## 1. Non-Root User

```dockerfile
FROM python:3.11-slim

# Create a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app
COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

# Switch to non-root
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
# Verify
docker exec myapp whoami
# appuser  (not root!)
```

---

## 2. Read-Only Filesystem

```bash
# Container filesystem is read-only — prevents malware from writing
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /var/run \
  -p 5000:5000 \
  myapp

# In docker-compose.yml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

---

## 3. Resource Limits

```bash
docker run \
  --memory="256m" \
  --memory-swap="256m" \     # no swap
  --cpus="0.5" \             # half a core
  --pids-limit 50 \          # max 50 processes
  myapp
```

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
```

---

## 4. Drop Linux Capabilities

```bash
# Drop ALL capabilities, add only what's needed
docker run \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \   # needed to bind port <1024
  myapp

# In docker-compose.yml
services:
  app:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

---

## 5. Secrets — Never in ENV or Layers

```bash
# ❌ BAD — visible in docker history and docker inspect
ENV DB_PASSWORD=mysecret
RUN pip install -r requirements.txt --extra-index-url https://user:TOKEN@private.pypi.org/simple/

# ✅ GOOD — BuildKit secret mount (never stored in layer)
RUN --mount=type=secret,id=pip_token \
    pip install -r requirements.txt \
      --extra-index-url https://user:$(cat /run/secrets/pip_token)@private.pypi.org/simple/
```

```bash
# Build with secret
DOCKER_BUILDKIT=1 docker build \
  --secret id=pip_token,src=.pip-token \
  -t myapp .
```

---

## 6. Image Scanning in CI

```yaml
# .github/workflows
- name: Scan image with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:latest
    exit-code: 1          # fail CI if CRITICAL found
    severity: CRITICAL,HIGH
    ignore-unfixed: true  # skip issues with no fix yet
```

---

## 7. Content Trust (Sign Images)

```bash
# Enable content trust (only run signed images)
export DOCKER_CONTENT_TRUST=1

# Sign and push
docker push yourusername/myapp:v1
# Prompts for signing key passphrase

# Pull — Docker verifies signature
docker pull yourusername/myapp:v1
```

---

## Security Benchmark

```bash
# Docker Bench Security — automated CIS benchmark check
docker run -it --net host --pid host --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro \
  -v /lib/systemd/system:/lib/systemd/system:ro \
  -v /usr/bin/containerd:/usr/bin/containerd:ro \
  -v /usr/bin/runc:/usr/bin/runc:ro \
  -v /usr/lib/systemd:/usr/lib/systemd:ro \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --label docker_bench_security \
  docker/docker-bench-security
```

---

## 📋 Lab Tasks

1. Convert your Flask image to run as non-root — verify with `docker exec whoami`
2. Run with `--read-only --tmpfs /tmp` — confirm the app still starts
3. Run with `--memory=128m` and load-test it — observe OOM kill
4. Run `trivy image myapp:v1` — document findings and upgrade base image to fix

> 🎓 **Congratulations! You've completed the Docker Lab!**
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_CI%2FCD-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-13-cicd-docker.md)
[![Pro_Index](https://img.shields.io/badge/Pro_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)

</div>