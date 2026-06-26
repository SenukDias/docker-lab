# 🟡 Intermediate Docker Tasks


---

<div align="center">

[![← Beginner Tasks](https://img.shields.io/badge/←_Beginner_Tasks-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](beginner-tasks.md)
[![All Tasks](https://img.shields.io/badge/All_Tasks-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../README.md#-all-labs)
[![Pro Tasks →](https://img.shields.io/badge/Pro_Tasks_→-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](pro-tasks.md)

</div>

---

<div align="center">

**Jump to section:**

[![Task_1_Flask__Redis_with_Com](https://img.shields.io/badge/Task_1_Flask__Redis_with_Com-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-1-flask-redis-with-compose)
[![Task_2_Environment_Isolation](https://img.shields.io/badge/Task_2_Environment_Isolation-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-2-environment-isolation)
[![Task_3_Multi-Container_Depen](https://img.shields.io/badge/Task_3_Multi-Container_Depen-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-3-multi-container-dependency-chain)
[![Task_4_Debug_a_Broken_Stack](https://img.shields.io/badge/Task_4_Debug_a_Broken_Stack-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-4-debug-a-broken-stack)
[![Task_5_Volume_Backup_%26_Res](https://img.shields.io/badge/Task_5_Volume_Backup_%26_Res-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-5-volume-backup-restore)

</div>

---

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
---

<div align="center">

[![← Beginner Tasks](https://img.shields.io/badge/←_Beginner_Tasks-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](beginner-tasks.md)
[![All Tasks](https://img.shields.io/badge/All_Tasks-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../README.md#-all-labs)
[![Pro Tasks →](https://img.shields.io/badge/Pro_Tasks_→-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](pro-tasks.md)

</div>