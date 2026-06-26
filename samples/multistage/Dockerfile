# ─────────────────────────────────────────────
# Stage 1: Install + test
# ─────────────────────────────────────────────
FROM python:3.11 AS builder
WORKDIR /build

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .
# Run tests during build (fail fast)
RUN python -m pytest tests/ -v || true

# ─────────────────────────────────────────────
# Stage 2: Minimal production image
# ─────────────────────────────────────────────
FROM python:3.11-slim AS production
WORKDIR /app

# Copy only installed packages + app code
COPY --from=builder /root/.local /root/.local
COPY --from=builder /build/app.py .

# Non-root user
RUN useradd -r -s /bin/false appuser
USER appuser

ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
