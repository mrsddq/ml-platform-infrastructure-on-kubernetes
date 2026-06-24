# Cost Estimate

This repo can run locally or on any Kubernetes cluster. Costs depend on where the cluster runs.

## Local Demo

| Component | Cost |
|---|---:|
| Python scoring tests | Free |
| Local MLflow Docker Compose | Free except local machine resources |

## Kubernetes Demo

| Resource | Cost driver | Control |
|---|---|---|
| Model API pods | CPU and memory requests | Keep replicas at 2 for demo |
| Prometheus/Grafana | Metrics storage | Limit retention |
| MLflow | Storage and database | Use local compose for portfolio demo |

## Guardrails

- Keep model API replicas low for demos.
- Use short-lived namespaces.
- Tag cloud resources if using managed Kubernetes.
- Destroy demo releases with `make destroy`.
