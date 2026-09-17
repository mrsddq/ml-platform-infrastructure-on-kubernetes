# Artifact and model registry contract

## Implemented

The API loads `MODEL_PATH` once during startup and validates its coefficients,
feature schema, numeric ranges, name, and version. `MODEL_NAME` and `MODEL_VERSION`
are optional identity assertions. Helm passes all three. Readiness succeeds only
after model loading; a missing artifact or mismatch prevents the service starting.
Changing a version label alone does not promote a model.

## Release and rollback

1. Export a validated JSON artifact with the scorer's rooms/sqft schema.
2. Package it inside an image (or arrange an immutable volume mount).
3. Test `/predict`, `/healthz`, and the expected identity against that artifact.
4. Publish the image and update its tag plus Helm model path/name/version together.
5. Deploy through the chosen GitOps process and inspect workload readiness.
6. Roll back the complete image/artifact configuration, then check predictions.

## Proposed integration

MLflow tracking/registry export, model-quality promotion gates, image publishing,
cluster rollout, and rollback observation are not automated by this repository.
The local MLflow compose server is a separate demonstration service.
