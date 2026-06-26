# 🔴 Pro Docker Tasks

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
