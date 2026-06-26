# 🐳 Lab 01 — Docker Installation

> **Level:** Beginner | **Time:** ~20 min | **Goal:** Install Docker and verify it works

---

## Prerequisites

| Requirement | Minimum |
|-------------|---------|
| OS | Windows 10/11, macOS 10.15+, Ubuntu 18.04+ |
| RAM | 4 GB |
| Disk | 10 GB free |

---

## 🪟 Windows — Docker Desktop

```powershell
# Option 1: winget (recommended)
winget install Docker.DockerDesktop

# Option 2: Chocolatey
choco install docker-desktop

# Option 3: Download installer
# https://www.docker.com/products/docker-desktop/
```

After install → **Enable WSL 2 backend** in Docker Desktop settings.

---

## 🍎 macOS — Docker Desktop

```bash
# Option 1: Homebrew (recommended)
brew install --cask docker

# Option 2: Download .dmg
# https://www.docker.com/products/docker-desktop/
```

---

## 🐧 Linux — Docker Engine

```bash
# Ubuntu / Debian
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Add Docker's GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add repository
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add your user to docker group (no sudo needed)
sudo usermod -aG docker $USER
newgrp docker
```

---

## ✅ Verify Installation

```bash
# Check version
docker --version
# Docker version 25.0.x, build xxxxxxx

# Run hello-world container
docker run hello-world

# Check Docker info
docker info

# List running containers
docker ps
```

Expected output from `hello-world`:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| `permission denied` on Linux | Run `sudo usermod -aG docker $USER` then log out/in |
| Docker Desktop won't start | Enable Virtualization in BIOS |
| WSL 2 error on Windows | Run `wsl --update` in PowerShell as Admin |

---

## 📋 Lab Task

1. Install Docker using your OS method above
2. Run `docker run hello-world` — screenshot the output
3. Run `docker run -it ubuntu bash` — explore the container
4. Exit with `exit`, then run `docker ps -a` to see stopped containers

> 💡 **Next:** [Lab 02 — Your First Container →](lab-02-first-container.md)
