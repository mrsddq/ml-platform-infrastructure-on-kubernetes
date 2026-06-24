from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "ml_platform/scoring.py",
    "ml_platform/metrics.py",
    "services/model-api/app.py",
    "services/model-api/Dockerfile",
    "helm/ml-platform/Chart.yaml",
    "helm/ml-platform/values.yaml",
    "helm/ml-platform/templates/deployment.yaml",
    "kubernetes/argocd/application.yaml",
    "kubernetes/monitoring/grafana-dashboard.json",
    "mlflow/docker-compose.yml",
    "docs/MODEL_REGISTRY_FLOW.md",
]


def main() -> None:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        raise SystemExit(f"missing required files: {', '.join(missing)}")
    print("ml platform layout validation passed")


if __name__ == "__main__":
    main()
