# Model Registry Flow

1. Training job logs parameters and metrics to MLflow.
2. A candidate model is registered with version metadata.
3. A quality gate approves or rejects promotion.
4. Platform repo receives a pull request updating model version and image tag.
5. Argo CD deploys the model serving runtime.
6. Observability confirms production health.

This keeps model promotion auditable and reversible.
