from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ModelMetadata:
    name: str
    version: str
    intercept: float
    coefficients: dict[str, float]
    training_ranges: dict[str, tuple[float, float]]


def load_model(path: str | Path) -> ModelMetadata:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return ModelMetadata(
        name=payload["name"],
        version=payload["version"],
        intercept=float(payload["intercept"]),
        coefficients={key: float(value) for key, value in payload["coefficients"].items()},
        training_ranges={key: (float(value[0]), float(value[1])) for key, value in payload["training_ranges"].items()},
    )


def predict(model: ModelMetadata, features: dict[str, float]) -> float:
    score = model.intercept
    for feature, coefficient in model.coefficients.items():
        score += coefficient * float(features[feature])
    return round(score, 2)


def drift_warnings(model: ModelMetadata, features: dict[str, float]) -> list[str]:
    warnings = []
    for feature, value in features.items():
        minimum, maximum = model.training_ranges[feature]
        if value < minimum:
            warnings.append(f"{feature}={value} is below training minimum {minimum}")
        if value > maximum:
            warnings.append(f"{feature}={value} is above training maximum {maximum}")
    return warnings


def prediction_payload(model: ModelMetadata, features: dict[str, float]) -> dict[str, Any]:
    return {
        "model_name": model.name,
        "model_version": model.version,
        "prediction": predict(model, features),
        "warnings": drift_warnings(model, features),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score a sample rental model payload.")
    parser.add_argument("--model", default="models/sample_model.json")
    parser.add_argument("--rooms", type=float, required=True)
    parser.add_argument("--sqft", type=float, required=True)
    args = parser.parse_args()
    model = load_model(args.model)
    print(json.dumps(prediction_payload(model, {"rooms": args.rooms, "sqft": args.sqft}), indent=2))


if __name__ == "__main__":
    main()
