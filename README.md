# ML Platform Infrastructure on Kubernetes

[![CI](https://github.com/mrsddq/ml-platform-infrastructure-on-kubernetes/actions/workflows/ci.yml/badge.svg)](https://github.com/mrsddq/ml-platform-infrastructure-on-kubernetes/actions/workflows/ci.yml)

ML infrastructure portfolio repo for serving, deploying, observing, and promoting models on Kubernetes. This is intentionally framed as platform engineering for ML workloads, not pure model research.

## What This Builds

- FastAPI-style model serving contract with health, prediction, and metrics endpoints
- Lightweight scoring library and model metadata file for offline tests
- Dockerfile for the model API
- Helm chart for Kubernetes deployment, service, HPA, config, and service account
- Argo CD Application for GitOps delivery
- Prometheus ServiceMonitor and Grafana dashboard starter
- MLflow tracking server local compose file
- Drift-check placeholder and model registry handoff docs
- CI tests that validate code, chart structure, and platform artifacts

## Architecture

```mermaid
flowchart LR
    Data["Training Pipeline"] --> MLflow["MLflow Tracking + Registry"]
    MLflow --> Image["Model API Image"]
    Image --> Helm["Helm Chart"]
    Helm --> Argo["Argo CD"]
    Argo --> K8s["Kubernetes"]
    K8s --> API["FastAPI Model Serving"]
    API --> Metrics["Prometheus Metrics"]
    Metrics --> Grafana["Grafana"]
    API --> Drift["Drift Check Placeholder"]
```

## Local Demo

Run tests:

```bash
make test
```

Score a sample payload:

```bash
python -m ml_platform.scoring --model models/sample_model.json --rooms 3 --sqft 1100
```

Run the API if FastAPI is installed:

```bash
cd services/model-api
PYTHONPATH=../.. uvicorn app:create_app --factory --host 0.0.0.0 --port 8000
```

## Platform Deployment Flow

1. Train and register model in MLflow.
2. Build and scan the model API image.
3. Update image tag and model version in Helm values.
4. Let Argo CD reconcile the chart.
5. Monitor latency, error rate, request volume, and prediction warnings.
6. Roll back by reverting the image tag or model version.

## Portfolio Evidence

See [docs/PORTFOLIO_EVIDENCE.md](docs/PORTFOLIO_EVIDENCE.md) for sample scoring output, platform validation commands, and interview proof points.

## Production Docs

- [Architecture](docs/architecture.md)
- [Runbook](docs/runbook.md)
- [Incident response](docs/incident-response.md)
- [Cost estimate](docs/cost-estimate.md)
- [Security controls](docs/security-controls.md)

## Make Targets

```bash
make test
make lint
make score
make security-scan
make local-demo
make deploy
make destroy
```

## Interview Story

This project demonstrates model-serving infrastructure on Kubernetes: API packaging, Helm deployment, Argo CD promotion, MLflow workflow support, Prometheus metrics, drift-check scaffolding and model-version rollback.

## What This Proves

- Can support ML workloads with Kubernetes, Helm, GitOps, and observability
- Understands model serving as an operational platform concern
- Can separate model metadata, runtime, deployment, and monitoring
- Can discuss model registry handoff and rollback paths
