FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt



FROM python:3.11-slim AS final

WORKDIR /app

COPY --from=builder /install /usr/local

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup --no-create-home appuser

COPY --chown=appuser:appgroup . .

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import redis,os; r=redis.Redis(host=os.getenv('REDIS_HOST','redis'),port=int(os.getenv('REDIS_PORT',6379)),password=os.getenv('REDIS_PASSWORD')); r.ping()" || exit 1

CMD ["python", "-u", "worker.py"]