# Portfolio Evidence

This repo proves ML platform infrastructure awareness: serving, packaging, GitOps deployment, metrics and rollback. It does not claim a complete production MLOps lifecycle.

## Verified Locally

```bash
python -m unittest discover -s tests
python scripts/validate_layout.py
python -m ml_platform.scoring --model models/sample_model.json --rooms 3 --sqft 1100
```

Sample score output:

```json
{
  "model_name": "rental-price-baseline",
  "model_version": "1.0.0",
  "prediction": 2475.0,
  "warnings": []
}
```

## Reviewer Evidence

| Evidence | Location | What it proves |
|---|---|---|
| CI badge | `README.md` | Scoring tests and platform layout validation pass. |
| Model API | `services/model-api/` | FastAPI serving contract with health, predict and metrics endpoints. |
| Helm chart | `helm/ml-platform/` | Kubernetes deployment, service, HPA and ServiceMonitor. |
| Argo CD app | `kubernetes/argocd/application.yaml` | GitOps deployment path. |
| MLflow compose | `mlflow/docker-compose.yml` | Tracking and registry handoff concept. |
| Rollback docs | `docs/RUNBOOK.md` | Model-version rollback and operational checks. |
