# 🐳 Lab 10 — Debugging Containers

> **Level:** Intermediate | **Time:** ~30 min | **Goal:** Diagnose and fix container issues

---

## Debug Toolkit

```bash
# View logs (most important first step)
docker logs <container>
docker logs -f --tail 100 <container>    # follow last 100 lines
docker logs --since 10m <container>      # logs from last 10 minutes

# Execute interactive shell
docker exec -it <container> bash
docker exec -it <container> sh   # if bash is not available (alpine)

# Execute a one-off command
docker exec <container> cat /etc/os-release
docker exec <container> printenv
docker exec <container> ps aux

# Inspect full metadata
docker inspect <container>
docker inspect --format='{{json .State}}' <container> | python -m json.tool

# See resource usage
docker stats <container>
docker stats --no-stream           # one-shot snapshot

# See network connections
docker exec <container> netstat -tlnp
docker exec <container> ss -tlnp
```

---

## Common Issues & Fixes

### Container exits immediately

```bash
# View exit code
docker inspect <container> --format='{{.State.ExitCode}}'

# Run interactively to see error
docker run -it myimage bash

# Override CMD to debug
docker run -it --entrypoint bash myimage
```

### Port already in use

```bash
# Find what's using the port
netstat -tulnp | grep 8080      # Linux
Get-NetTCPConnection -LocalPort 8080 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Get-Process -Id $_ }   # Windows

# Use a different host port
docker run -p 8081:80 nginx
```

### Container can't connect to another service

```bash
# Check they're on the same network
docker network inspect mynet

# Test DNS resolution from within container
docker exec myapp nslookup db
docker exec myapp ping db

# Test TCP connectivity
docker exec myapp nc -zv db 5432
docker exec myapp curl -v http://backend:5000/health
```

### Out of disk space

```bash
docker system df              # see disk usage
docker system prune -a        # remove ALL unused resources
docker volume prune           # remove unused volumes
```

---

## Debugging a Crashed Container

```bash
# Container crashed — logs are still accessible
docker logs crashed-container

# Start a stopped container to inspect its filesystem
docker start <container_id>
docker exec -it <container_id> bash

# Or copy files out of stopped container
docker cp <container_id>:/app/error.log ./error.log
```

---

## Docker Events

```bash
# Watch Docker events in real-time
docker events

# Filter by type
docker events --filter type=container
docker events --filter event=die
```

---

## 📋 Lab Tasks

1. Create a Dockerfile with a broken CMD (e.g., `CMD ["python", "nonexistent.py"]`) — use the debug techniques to identify the issue
2. Run two containers on different networks — demonstrate connectivity failure, then fix by adding them to the same network
3. Run `docker stats` while making 100 requests to your Flask app — observe CPU/memory behavior

> 💡 **Next:** [Pro Track →](../pro/README.md)
