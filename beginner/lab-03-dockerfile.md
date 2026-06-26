# 🐳 Lab 03 — Writing a Dockerfile


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_First_Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-02-first-container.md)
[![Beginner_Index](https://img.shields.io/badge/Beginner_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Images_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-04-images.md)

</div>

---

<div align="center">

**Jump to section:**

[![What_is_a_Dockerfile](https://img.shields.io/badge/What_is_a_Dockerfile-2496ED?style=flat-square&logo=docker&logoColor=white)](#what-is-a-dockerfile)
[![Dockerfile_Instructions_Refe](https://img.shields.io/badge/Dockerfile_Instructions_Refe-2496ED?style=flat-square&logo=docker&logoColor=white)](#dockerfile-instructions-reference)
[![Your_First_Dockerfile_Python](https://img.shields.io/badge/Your_First_Dockerfile_Python-2496ED?style=flat-square&logo=docker&logoColor=white)](#your-first-dockerfile-python-flask-app)
[![CMD_vs_ENTRYPOINT](https://img.shields.io/badge/CMD_vs_ENTRYPOINT-2496ED?style=flat-square&logo=docker&logoColor=white)](#cmd-vs-entrypoint)
[![.dockerignore_File](https://img.shields.io/badge/.dockerignore_File-2496ED?style=flat-square&logo=docker&logoColor=white)](#dockerignore-file)
[![Layer_Caching_Best_Practices](https://img.shields.io/badge/Layer_Caching_Best_Practices-2496ED?style=flat-square&logo=docker&logoColor=white)](#layer-caching-best-practices)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
> **Level:** Beginner | **Time:** ~30 min | **Goal:** Build your own custom Docker image

---

## What is a Dockerfile?

A **Dockerfile** is a text file of instructions that Docker reads to build an image layer by layer.

```
Dockerfile → docker build → Image → docker run → Container
```

---

## Dockerfile Instructions Reference

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Base image (always first) | `FROM python:3.11-slim` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from host | `COPY . .` |
| `ADD` | Copy + auto-extract archives | `ADD app.tar.gz /app` |
| `RUN` | Execute command during build | `RUN pip install -r requirements.txt` |
| `ENV` | Set environment variable | `ENV PORT=8000` |
| `EXPOSE` | Document port (informational) | `EXPOSE 8000` |
| `CMD` | Default command when container starts | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Fixed executable (CMD appends args) | `ENTRYPOINT ["gunicorn"]` |
| `ARG` | Build-time variable | `ARG VERSION=1.0` |
| `VOLUME` | Declare mount point | `VOLUME /data` |
| `USER` | Set runtime user | `USER appuser` |

---

## Your First Dockerfile — Python Flask App

Create a project:
```bash
mkdir flask-app && cd flask-app
```

`app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Docker! 🐳</h1>"

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

`requirements.txt`:
```
flask==3.0.0
```

`Dockerfile`:
```dockerfile
# 1. Base image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy and install dependencies first (caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application code
COPY . .

# 5. Document the port
EXPOSE 5000

# 6. Run the app
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t flask-app:v1 .
docker run -d -p 5000:5000 --name flask flask-app:v1
curl http://localhost:5000
```

---

## CMD vs ENTRYPOINT

```dockerfile
# CMD — can be overridden by arguments to docker run
CMD ["python", "app.py"]
docker run myapp python other.py   # overrides CMD

# ENTRYPOINT — cannot be overridden (without --entrypoint flag)
ENTRYPOINT ["python", "app.py"]
docker run myapp                   # always runs python app.py

# Together: ENTRYPOINT is the executable, CMD provides defaults
ENTRYPOINT ["gunicorn"]
CMD ["--bind", "0.0.0.0:8000", "app:app"]
docker run myapp --workers 4      # becomes: gunicorn --workers 4
```

---

## .dockerignore File

Prevents unnecessary files from being copied into the build context:

```
.git
.gitignore
__pycache__/
*.pyc
*.pyo
.env
.venv/
node_modules/
*.log
Dockerfile
.dockerignore
README.md
```

---

## Layer Caching Best Practices

```dockerfile
# ✅ GOOD — dependencies cached separately from code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .                          # Only this layer re-runs when code changes

# ❌ BAD — any code change invalidates the pip install layer
COPY . .
RUN pip install -r requirements.txt
```

---

## 📋 Lab Tasks

1. Create the Flask app above, build image, run it — visit `localhost:5000`
2. Change the message in `app.py`, rebuild, and run version `:v2`
3. Add a `.dockerignore` and verify `docker build` output shows fewer files
4. Try `docker run flask-app:v1 python -c "print('hello')"` — observe CMD override

> 💡 **Next:** [Lab 04 — Images & Layers →](lab-04-images.md)
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_First_Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-02-first-container.md)
[![Beginner_Index](https://img.shields.io/badge/Beginner_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Images_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-04-images.md)

</div>