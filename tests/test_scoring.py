import unittest
from pathlib import Path

from ml_platform.metrics import MetricsRegistry
from ml_platform.scoring import drift_warnings, load_model, prediction_payload


ROOT = Path(__file__).resolve().parents[1]


class ScoringTest(unittest.TestCase):
    def test_prediction_payload_contains_model_version(self):
        model = load_model(ROOT / "models" / "sample_model.json")
        payload = prediction_payload(model, {"rooms": 3, "sqft": 1100})
        self.assertEqual(payload["model_version"], "1.0.0")
        self.assertGreater(payload["prediction"], 0)

    def test_drift_warning_for_out_of_range_input(self):
        model = load_model(ROOT / "models" / "sample_model.json")
        warnings = drift_warnings(model, {"rooms": 8, "sqft": 1100})
        self.assertTrue(any("above training maximum" in item for item in warnings))

    def test_metrics_registry_renders_prometheus_text(self):
        metrics = MetricsRegistry()
        metrics.observe(ok=True, warnings=2)
        text = metrics.prometheus_text()
        self.assertIn("model_api_requests_total 1", text)
        self.assertIn("model_api_drift_warnings_total 2", text)


if __name__ == "__main__":
    unittest.main()
