FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY ml_platform /app/ml_platform
COPY models /app/models
COPY services/model-api/app.py /app/app.py

RUN pip install --no-cache-dir "fastapi>=0.115" "uvicorn[standard]>=0.30"
RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
