# Architecture

This repo treats ML serving as a platform problem with clear ownership boundaries.

## Boundaries

- MLflow stores experiment metadata and registered model versions.
- The model API owns request validation, prediction, and metrics.
- Helm owns Kubernetes runtime configuration.
- Argo CD reconciles the desired deployment state.
- Prometheus and Grafana support operational review.

## Promotion Model

Promote model versions by updating chart values and opening a pull request. CI validates repo structure and scoring behavior. Argo CD deploys after merge.
