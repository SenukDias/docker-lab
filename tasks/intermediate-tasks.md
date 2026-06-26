# 🟡 Intermediate Docker Tasks

> Complete all 5 tasks to progress to Pro level.

---

## Task 1 — Flask + Redis with Compose

Build a Compose stack:
- Flask app that tracks page visits using Redis
- Redis service
- Accessible on port `5000`
- Data persists across `docker compose down` and `up`

**Deliverable:** `docker compose ps` output showing both healthy services + visit counter working.

---

## Task 2 — Environment Isolation

Create two identical Compose stacks (dev + staging):
- Use different `.env` files for each
- Different database names and ports
- Both running simultaneously without port conflicts

**Deliverable:** Both stacks running at different ports, showing different DB names in `/health` endpoint.

---

## Task 3 — Multi-Container Dependency Chain

Build: `nginx → flask → postgres` with:
- `nginx` on port 80, proxying to `flask`
- `flask` depends on `postgres` health check
- `postgres` only starts after volume is ready

**Deliverable:** `curl http://localhost/` returns Flask response via Nginx.

---

## Task 4 — Debug a Broken Stack

Given:
```yaml
# This compose file has 3 intentional bugs
services:
  app:
    image: python:3.11-slim
    command: python app.py
    ports:
      - "5000:5000"
  db:
    image: postgres
    # Missing: environment, healthcheck, volume
```

Find and fix all bugs. Document each fix with explanation.

---

## Task 5 — Volume Backup & Restore

1. Run PostgreSQL, create a database with sample data
2. Back up the volume data to a `.tar.gz` file using a temporary Alpine container
3. Delete the volume and container
4. Restore from your backup
5. Verify data is intact

**Deliverable:** Backup and restore commands used + final SELECT output.
