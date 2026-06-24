# Runbook

## Deploy New Model Version

1. Confirm the model was registered in MLflow.
2. Update `helm/ml-platform/values.yaml` with the model version and image tag.
3. Review CI results.
4. Merge and let Argo CD sync.
5. Watch request latency, error rate, and prediction warnings.

## Rollback

1. Revert the values change.
2. Confirm Argo CD sync completes.
3. Compare metrics before and after rollback.
4. Record the incident or change review.

## Incident Checks

- API health endpoint
- ServiceMonitor scrape status
- Pod restarts
- Request p95 latency
- Model version annotation
- Input drift warnings
