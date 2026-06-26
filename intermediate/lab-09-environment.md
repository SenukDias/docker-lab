# 🐳 Lab 09 — Environment Variables & Secrets

> **Level:** Intermediate | **Time:** ~25 min | **Goal:** Manage config and secrets safely

---

## Environment Variables in Docker

```bash
# Pass single env var
docker run -e APP_ENV=production myapp

# Pass multiple
docker run -e DB_HOST=db -e DB_PORT=5432 -e DB_PASS=secret myapp

# Read from a file
docker run --env-file .env myapp

# In Dockerfile
ENV APP_PORT=8000
ENV LOG_LEVEL=info
```

---

## .env File Pattern

```bash
# .env (NEVER commit this file!)
DATABASE_URL=postgresql://admin:secretpass@db:5432/mydb
REDIS_URL=redis://redis:6379
SECRET_KEY=super-secret-jwt-key-change-in-prod
API_KEY=sk-prod-xxxxxxxxxxxxxxxx
DEBUG=false
```

```yaml
# docker-compose.yml
services:
  app:
    env_file:
      - .env          # loads all vars from .env
    environment:
      - NODE_ENV=production   # can override individual vars
```

---

## Docker Secrets (Swarm / Best Practice)

```bash
# Create a Docker secret from file
echo "my-super-secret-password" | docker secret create db_password -

# Create from a file
docker secret create ssl_cert ./cert.pem

# Use in service
docker service create \
  --name myapp \
  --secret db_password \
  myimage
```

In the container, secrets appear as files:
```bash
cat /run/secrets/db_password
# my-super-secret-password
```

---

## Reading Secrets in Code

```python
# Python — read Docker secret
import os

def get_secret(name):
    secret_file = f"/run/secrets/{name}"
    if os.path.exists(secret_file):
        with open(secret_file) as f:
            return f.read().strip()
    # Fallback to env var for local dev
    return os.environ.get(name.upper())

db_password = get_secret("db_password")
```

---

## Override for Dev vs Prod

```yaml
# docker-compose.yml (base)
services:
  app:
    image: myapp
    environment:
      - LOG_LEVEL=warn

# docker-compose.override.yml (auto-loaded in dev)
services:
  app:
    build: .                # build locally in dev
    environment:
      - LOG_LEVEL=debug
    volumes:
      - .:/app              # live reload in dev

# Run in dev (merges both files)
docker compose up

# Run in prod (only base file)
docker compose -f docker-compose.yml up
```

---

## 📋 Lab Tasks

1. Create a `.env` file and use `--env-file` to run a container — print env vars with `env` command
2. Demonstrate a **security mistake**: `docker run -e SECRET=mypassword alpine env | grep SECRET` — see how env vars are visible
3. Use `docker compose.override.yml` for dev (bind mount) vs prod (no bind mount)

> 💡 **Next:** [Lab 10 — Debugging Containers →](lab-10-debugging.md)
