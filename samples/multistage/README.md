# Multi-Stage Build Sample

## Build comparison

```bash
# Single stage
docker build --target builder -t myapp:fat .
docker images myapp:fat
# ~1.1GB

# Multi-stage production
docker build --target production -t myapp:slim .
docker images myapp:slim
# ~145MB
```

## Run

```bash
docker build -t myapp:prod .
docker run -p 5000:5000 myapp:prod
curl http://localhost:5000
```
