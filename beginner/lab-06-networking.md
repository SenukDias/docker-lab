# 🐳 Lab 06 — Docker Networking


---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Volumes-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-05-volumes.md)
[![Beginner_Index](https://img.shields.io/badge/Beginner_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Docker_Compose_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../intermediate/lab-07-docker-compose.md)

</div>

---

<div align="center">

**Jump to section:**

[![Docker_Network_Types](https://img.shields.io/badge/Docker_Network_Types-2496ED?style=flat-square&logo=docker&logoColor=white)](#docker-network-types)
[![Bridge_Network_Default](https://img.shields.io/badge/Bridge_Network_Default-2496ED?style=flat-square&logo=docker&logoColor=white)](#bridge-network-default)
[![Custom_Bridge_Network_DNS_Re](https://img.shields.io/badge/Custom_Bridge_Network_DNS_Re-2496ED?style=flat-square&logo=docker&logoColor=white)](#custom-bridge-network-dns-resolution)
[![Network_Commands](https://img.shields.io/badge/Network_Commands-2496ED?style=flat-square&logo=docker&logoColor=white)](#network-commands)
[![Port_Mapping_Deep_Dive](https://img.shields.io/badge/Port_Mapping_Deep_Dive-2496ED?style=flat-square&logo=docker&logoColor=white)](#port-mapping-deep-dive)
[![Practical_App__Database_Netw](https://img.shields.io/badge/Practical_App__Database_Netw-2496ED?style=flat-square&logo=docker&logoColor=white)](#practical-app-database-network)
[![Host_Network_Mode_Linux_only](https://img.shields.io/badge/Host_Network_Mode_Linux_only-2496ED?style=flat-square&logo=docker&logoColor=white)](#host-network-mode-linux-only)
[![Lab_Tasks](https://img.shields.io/badge/Lab_Tasks-2496ED?style=flat-square&logo=docker&logoColor=white)](#lab-tasks)

</div>

---
> **Level:** Beginner | **Time:** ~25 min | **Goal:** Connect containers via networks

---

## Docker Network Types

| Driver | Isolation | Use Case |
|--------|-----------|---------|
| `bridge` | Isolated from host | Default, single-host containers |
| `host` | Shares host network | Maximum performance, Linux only |
| `none` | No network | Fully isolated container |
| `overlay` | Multi-host | Docker Swarm, distributed apps |

---

## Bridge Network (Default)

```bash
# Containers on default bridge communicate by IP only
docker run -d --name app1 nginx
docker run -d --name app2 nginx

# Get IP of app1
docker inspect -f '{{.NetworkSettings.IPAddress}}' app1

# app2 can reach app1 by IP but NOT by name on default bridge
docker exec app2 curl http://172.17.0.2   # works
docker exec app2 curl http://app1         # fails on default bridge
```

---

## Custom Bridge Network — DNS Resolution

```bash
# Create a custom network
docker network create mynet

# Containers on custom network resolve each other by NAME
docker run -d --name frontend --network mynet nginx
docker run -d --name backend  --network mynet nginx

# DNS works! Use container names as hostnames
docker exec frontend curl http://backend
docker exec backend  curl http://frontend
```

This is the **recommended approach** for container communication.

---

## Network Commands

```bash
# List networks
docker network ls

# Create networks
docker network create mynet
docker network create --driver bridge --subnet 172.20.0.0/16 custom-net

# Inspect network
docker network inspect mynet

# Connect a running container to a network
docker network connect mynet my-container

# Disconnect
docker network disconnect mynet my-container

# Remove network
docker network rm mynet
docker network prune   # remove all unused networks
```

---

## Port Mapping Deep Dive

```bash
# Host port : Container port
docker run -p 8080:80 nginx        # localhost:8080 maps to container:80

# Bind to specific interface (more secure)
docker run -p 127.0.0.1:8080:80 nginx   # only accessible locally

# Multiple ports
docker run -p 8080:80 -p 8443:443 nginx

# All interfaces, random host port
docker run -P nginx    # capital P = auto-map all EXPOSE'd ports

# Check mappings
docker port <container_name>
```

---

## Practical: App + Database Network

```bash
# Create isolated network
docker network create app-net

# Start database (no port exposed to host — only app can reach it)
docker run -d \
  --name db \
  --network app-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:16

# Start Flask app connected to same network
docker run -d \
  --name app \
  --network app-net \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://postgres:secret@db:5432/postgres \
  flask-app:v1

# App connects to db using hostname "db" — thanks to custom network DNS
```

---

## Host Network Mode (Linux only)

```bash
# Container shares host's network namespace
docker run --network host nginx
# nginx now listens on host's port 80 directly (no port mapping needed)
```

---

## 📋 Lab Tasks

1. Create a custom network, run two `nginx` containers, verify they can `curl` each other by name
2. Run postgres on the network (no `-p`) + a client container, confirm client connects by hostname
3. Demonstrate the difference: run two containers on the **default** bridge and try name-based DNS (it should fail)

> 💡 **Next:** [Intermediate Track →](../intermediate/README.md)
---

<div align="center">

[![← Prev](https://img.shields.io/badge/←_Volumes-2496ED?style=for-the-badge&logo=docker&logoColor=white)](lab-05-volumes.md)
[![Beginner_Index](https://img.shields.io/badge/Beginner_Index-0ea5e9?style=for-the-badge&logo=docker&logoColor=white)](README.md)
[![Next →](https://img.shields.io/badge/Docker_Compose_→-2496ED?style=for-the-badge&logo=docker&logoColor=white)](../intermediate/lab-07-docker-compose.md)

</div>