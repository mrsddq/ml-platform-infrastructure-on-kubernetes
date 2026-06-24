# Security Controls

## Implemented

- Helm-managed service account with token automount disabled.
- Resource requests and limits.
- Health checks.
- CI validation.
- Optional Trivy config scan through `make security-scan`.

## Recommended Production Additions

- Image signing and vulnerability scanning.
- NetworkPolicy around model API and MLflow.
- External Secrets for registry credentials.
- Model artifact integrity checks.
- Argo CD sync windows and required reviews for model promotion.

## Security Review Questions

- Who can update the model version?
- Where are model artifacts stored?
- Can the API call external services?
- Are request logs free of sensitive input values?
- Which controls prevent unreviewed model rollout?
