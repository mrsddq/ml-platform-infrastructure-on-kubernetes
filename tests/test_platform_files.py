import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PlatformFilesTest(unittest.TestCase):
    def test_helm_chart_has_operational_controls(self):
        deployment = (ROOT / "helm" / "ml-platform" / "templates" / "deployment.yaml").read_text(encoding="utf-8")
        self.assertIn("readinessProbe:", deployment)
        self.assertIn("livenessProbe:", deployment)
        self.assertIn("resources:", deployment)

    def test_argocd_points_to_chart_path(self):
        app = (ROOT / "kubernetes" / "argocd" / "application.yaml").read_text(encoding="utf-8")
        self.assertIn("path: helm/ml-platform", app)

    def test_mlflow_compose_exists(self):
        compose = (ROOT / "mlflow" / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("mlflow server", compose)


if __name__ == "__main__":
    unittest.main()
