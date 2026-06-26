# 🟢 Beginner Docker Tasks


---

<div align="center">

[![← Beginner Labs](https://img.shields.io/badge/←_Beginner_Labs-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](../beginner/README.md)
[![All Tasks](https://img.shields.io/badge/All_Tasks-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../README.md#-all-labs)
[![Intermediate Tasks →](https://img.shields.io/badge/Intermediate_Tasks_→-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](intermediate-tasks.md)

</div>

---

<div align="center">

**Jump to section:**

[![Task_1_Run_and_Explore](https://img.shields.io/badge/Task_1_Run_and_Explore-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-1-run-and-explore)
[![Task_2_Build_Your_First_Imag](https://img.shields.io/badge/Task_2_Build_Your_First_Imag-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-2-build-your-first-image)
[![Task_3_Web_Server](https://img.shields.io/badge/Task_3_Web_Server-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-3-web-server)
[![Task_4_Persistent_Data](https://img.shields.io/badge/Task_4_Persistent_Data-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-4-persistent-data)
[![Task_5_Cleanup_Challenge](https://img.shields.io/badge/Task_5_Cleanup_Challenge-2496ED?style=flat-square&logo=docker&logoColor=white)](#task-5-cleanup-challenge)

</div>

---

> Complete all 5 tasks to progress to Intermediate level.

---

## Task 1 — Run and Explore

1. Pull the `alpine:latest` image
2. Run it interactively: `docker run -it alpine sh`
3. Inside the container: install curl with `apk add curl`, then `curl https://httpbin.org/get`
4. Exit and verify the container is stopped with `docker ps -a`

**Deliverable:** Screenshot of `curl` output from inside the container.

---

## Task 2 — Build Your First Image

Create a Python script that prints your name and the current time:

```python
# hello.py
import datetime
print(f"Hello from Docker! Built by: YOUR_NAME")
print(f"Time: {datetime.datetime.now()}")
```

Write a `Dockerfile` using `python:3.11-slim` and build it as `hello:v1`.

**Deliverable:** `docker run hello:v1` output showing your name.

---

## Task 3 — Web Server

1. Run `nginx` on port `9090`
2. Create a custom `index.html` with your name
3. Use a bind mount to serve it from nginx
4. Verify in browser or with `curl http://localhost:9090`

**Deliverable:** Screenshot of your custom page.

---

## Task 4 — Persistent Data

1. Run PostgreSQL with a named volume
2. Create a table and insert 3 rows
3. Delete the container, recreate it with the same volume
4. Verify data persists with a SELECT query

**Deliverable:** Screenshot showing data after container recreation.

---

## Task 5 — Cleanup Challenge

Without using `docker system prune`, manually:
1. List and remove all stopped containers
2. Remove images you created in tasks 1-4
3. Remove the postgres named volume
4. Show final `docker ps -a`, `docker images`, `docker volume ls` — all clean

**Deliverable:** Clean output of all three commands.
---

<div align="center">

[![← Beginner Labs](https://img.shields.io/badge/←_Beginner_Labs-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](../beginner/README.md)
[![All Tasks](https://img.shields.io/badge/All_Tasks-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../README.md#-all-labs)
[![Intermediate Tasks →](https://img.shields.io/badge/Intermediate_Tasks_→-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](intermediate-tasks.md)

</div>