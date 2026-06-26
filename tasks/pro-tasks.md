# 🔴 Pro Docker Tasks


---

<div align="center">

[![← Intermediate Tasks](https://img.shields.io/badge/←_Intermediate_Tasks-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](intermediate-tasks.md)
[![All Tasks](https://img.shields.io/badge/All_Tasks-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../README.md#-all-labs)

</div>

---

<div align="center">

**Jump to section:**

[![Task_1_Multi-Stage_Optimizat](https://img.shields.io/badge/Task_1_Multi-Stage_Optimizat-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-1-multi-stage-optimization-challenge)
[![Task_2_Full_CICD_Pipeline](https://img.shields.io/badge/Task_2_Full_CICD_Pipeline-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-2-full-cicd-pipeline)
[![Task_3_Secrets_Management](https://img.shields.io/badge/Task_3_Secrets_Management-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-3-secrets-management)
[![Task_4_Production_Hardening](https://img.shields.io/badge/Task_4_Production_Hardening-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-4-production-hardening)
[![Task_5_Observability_Stack](https://img.shields.io/badge/Task_5_Observability_Stack-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-5-observability-stack)

</div>

---

> Real-world engineering challenges.

---

## Task 1 — Multi-Stage Optimization Challenge

Take any existing Dockerfile (or create one) for a Node.js or Python app.
- Implement multi-stage build
- Final image must be under 150MB
- Must run as non-root user
- Must pass security scan with no CRITICAL CVEs

**Deliverable:** Before/after image sizes, `docker scout` or `trivy` scan output.

---

## Task 2 — Full CI/CD Pipeline

Set up GitHub Actions pipeline that:
1. Runs unit tests on every PR
2. Builds multi-arch image (linux/amd64, linux/arm64)
3. Pushes to GHCR on merge to main
4. Tags with `v*.*.*` on release
5. Runs Trivy scan and blocks on CRITICAL CVEs
6. Uses GHA cache for fast rebuilds

**Deliverable:** Link to passing pipeline run + GHCR image URL.

---

## Task 3 — Secrets Management

Implement proper secrets handling:
1. Build an image that requires a private PyPI token
2. Use BuildKit `--mount=type=secret` — token must NOT appear in `docker history`
3. Use Docker secrets for runtime credentials
4. Demonstrate the difference between ENV-based (bad) and secrets-based (good) approaches

**Deliverable:** `docker history myimage` showing no secret values.

---

## Task 4 — Production Hardening

Harden an existing container:
- Non-root user
- Read-only filesystem (`--read-only`)
- Drop all capabilities, add back only needed ones
- Memory limit: 256MB, CPU: 0.5
- No new privileges (`--security-opt no-new-privileges`)
- Pass Docker Bench Security check with no WARN on target container

**Deliverable:** Docker Bench output for your container.

---

## Task 5 — Observability Stack

Build a monitoring stack with Compose:
- Your Flask app with Prometheus metrics endpoint (`/metrics`)
- Prometheus scraping the app
- Grafana visualizing the metrics
- All accessible via Nginx on port 80 with path-based routing:
  - `/` → Flask app
  - `/metrics` → Prometheus
  - `/grafana` → Grafana dashboard

**Deliverable:** Grafana dashboard screenshot showing request rate and latency.
---

<div align="center">

[![← Intermediate Tasks](https://img.shields.io/badge/←_Intermediate_Tasks-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](intermediate-tasks.md)
[![All Tasks](https://img.shields.io/badge/All_Tasks-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../README.md#-all-labs)

</div>