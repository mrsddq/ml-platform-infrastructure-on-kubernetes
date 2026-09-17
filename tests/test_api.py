import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "model_api", ROOT / "services/model-api/app.py"
)
API = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(API)


class ModelAPITest(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "candidate.json"
        self.artifact = json.loads((ROOT / "models/sample_model.json").read_text())
        self.artifact.update(version="2.0.0", intercept=900.0)
        self.path.write_text(json.dumps(self.artifact))

    def test_configured_artifact_changes_predictions_and_health_identity(self):
        with patch.dict(
            os.environ,
            {
                "MODEL_PATH": str(self.path),
                "MODEL_NAME": self.artifact["name"],
                "MODEL_VERSION": "2.0.0",
            },
        ):
            client = TestClient(API.create_app())
            response = client.post("/predict", json={"rooms": 3, "sqft": 1100})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["prediction"], 2925.0)
        self.assertEqual(response.json()["model_version"], "2.0.0")
        self.assertEqual(client.get("/healthz").json()["version"], "2.0.0")

    def test_wrong_artifact_identity_fails_before_serving(self):
        for key, value in (("MODEL_VERSION", "3.0.0"), ("MODEL_NAME", "wrong-model")):
            with (
                self.subTest(key=key),
                patch.dict(os.environ, {key: value}),
                self.assertRaisesRegex(ValueError, "does not match artifact"),
            ):
                API.create_app(self.path)

    def test_missing_artifact_fails_before_serving(self):
        with self.assertRaises(FileNotFoundError):
            API.create_app(self.path.with_name("missing.json"))

    def test_request_body_is_schema_not_query_parameter(self):
        client = TestClient(API.create_app(self.path))
        operation = client.get("/openapi.json").json()["paths"]["/predict"]["post"]
        self.assertIn("requestBody", operation)
        self.assertNotIn("parameters", operation)

    def test_invalid_requests_count_as_errors_but_probes_do_not(self):
        client = TestClient(API.create_app(self.path))
        cases = [
            {},
            {"rooms": 0, "sqft": 1100},
            {"rooms": 1, "sqft": -1},
            {"rooms": 1, "sqft": "NaN"},
            {"rooms": 1, "sqft": "Infinity"},
            {"rooms": 1, "sqft": 1000, "unexpected": 5},
            {"rooms": 1e308, "sqft": 1e308},
        ]
        for body in cases:
            with self.subTest(body=body):
                self.assertEqual(client.post("/predict", json=body).status_code, 422)
        self.assertEqual(
            client.post(
                "/predict",
                content='{"rooms":NaN,"sqft":1000}',
                headers={"content-type": "application/json"},
            ).status_code,
            422,
        )
        client.get("/healthz")
        text = client.get("/metrics").text
        self.assertIn("model_api_requests_total 8", text)
        self.assertIn("model_api_errors_total 8", text)

    def test_corrupt_artifact_rejected(self):
        for update in (
            {"coefficients": {"rooms": 1}},
            {"intercept": float("nan")},
            {"training_ranges": {"rooms": [5, 1], "sqft": [1, 2]}},
        ):
            with self.subTest(update=update):
                self.path.write_text(json.dumps(self.artifact | update))
                with self.assertRaises(ValueError):
                    API.create_app(self.path)


if __name__ == "__main__":
    unittest.main()
