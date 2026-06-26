# 🔴 Lab 13 — CI/CD with Docker & GitHub Actions


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Docker_Hub-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-12-docker-hub.md)
[![Pro_Index](https://img.shields.io/badge/Pro_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Security_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-14-security.md)

</div>

---

<div align="center">

**Jump to section:**

[![Complete_CICD_Pipeline](https://img.shields.io/badge/Complete_CICD_Pipeline-2496ED?style=flat-square&logo=docker&logoColor=white)](#complete-cicd-pipeline)
[![Docker_Compose_in_CI_Integra](https://img.shields.io/badge/Docker_Compose_in_CI_Integra-2496ED?style=flat-square&logo=docker&logoColor=white)](#docker-compose-in-ci-integration-tests)
[![Cache_Optimization](https://img.shields.io/badge/Cache_Optimization-2496ED?style=flat-square&logo=docker&logoColor=white)](#cache-optimization)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
> **Level:** Pro | **Time:** ~45 min | **Goal:** Automate build, test, scan, and push in CI

---

## Complete CI/CD Pipeline

`.github/workflows/docker-build.yml`:
```yaml
name: Docker CI/CD Pipeline

on:
  push:
    branches: [main]
    tags: ['v*.*.*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install and test
        run: |
          pip install -r requirements.txt pytest
          pytest tests/ -v

  build-and-push:
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,format=short
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  security-scan:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.event_name != 'pull_request'
    steps:
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          format: sarif
          output: trivy-results.sarif
          severity: CRITICAL,HIGH

      - name: Upload to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: trivy-results.sarif
```

---

## Docker Compose in CI (Integration Tests)

```yaml
  integration-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start services
        run: docker compose -f docker-compose.test.yml up -d

      - name: Wait for healthy
        run: |
          for i in {1..30}; do
            curl -sf http://localhost:5000/health && break
            sleep 2
          done

      - name: Run integration tests
        run: pytest tests/integration/ -v

      - name: Tear down
        if: always()
        run: docker compose -f docker-compose.test.yml down -v
```

---

## Cache Optimization

```yaml
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          cache-from: type=gha         # use GitHub Actions cache
          cache-to: type=gha,mode=max  # save all layers
```

Pipeline time: **5 min → 90 sec** after cache warms up.

---

## 📋 Lab Tasks

1. Set up the CI pipeline in your GitHub repo — push to `main` and watch it run
2. Push with a tag `v1.0.0` — verify the versioned image appears in GHCR
3. Add Trivy scan — find and fix at least one HIGH CVE by updating a base image
4. Measure cache impact: time run 1 (cold) vs run 2 (warm cache)

> 💡 **Next:** [Lab 14 — Docker Security →](lab-14-security.md)
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Docker_Hub-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-12-docker-hub.md)
[![Pro_Index](https://img.shields.io/badge/Pro_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Security_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-14-security.md)

</div>