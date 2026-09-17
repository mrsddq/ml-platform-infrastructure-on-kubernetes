# Runbook

## Prerequisites

- Python 3.11+
- Docker for local MLflow demo
- Helm and kubectl for Kubernetes deployment
- Argo CD installed in the target cluster for GitOps sync

## Validate

```bash
make test
make validate
make score
```

## Local Demo

```bash
make local-demo
```

This starts local MLflow only. The model scoring path is intentionally offline and testable without MLflow.

## Deploy

```bash
make deploy
kubectl get pods -n ml-platform
kubectl port-forward svc/ml-platform-api -n ml-platform 8000:80
```

## Destroy

```bash
make destroy
```

## Rollback

- Revert the image tag and model path/name/version together in `helm/ml-platform/values.yaml`.
- A mismatched artifact identity fails startup and readiness; inspect container logs before retrying.
- Let Argo CD reconcile the previous version.
- Confirm `/healthz`, `/predict` and `/metrics`.
