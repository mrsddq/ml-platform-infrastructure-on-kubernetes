from __future__ import annotations

import argparse
import json
import math
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
    model = ModelMetadata(
        name=payload["name"],
        version=payload["version"],
        intercept=float(payload["intercept"]),
        coefficients={
            key: float(value) for key, value in payload["coefficients"].items()
        },
        training_ranges={
            key: (float(value[0]), float(value[1]))
            for key, value in payload["training_ranges"].items()
        },
    )

    if not model.name or not model.version:
        raise ValueError("model name and version must be nonempty")
    if set(model.coefficients) != {"rooms", "sqft"} or set(
        model.training_ranges
    ) != set(model.coefficients):
        raise ValueError(
            "model must define rooms and sqft coefficients and training ranges"
        )
    if not all(
        math.isfinite(value)
        for value in [model.intercept, *model.coefficients.values()]
    ):
        raise ValueError("model parameters must be finite")
    for minimum, maximum in model.training_ranges.values():
        if (
            not math.isfinite(minimum)
            or not math.isfinite(maximum)
            or minimum > maximum
        ):
            raise ValueError("training ranges must be finite and ordered")
    return model


def predict(model: ModelMetadata, features: dict[str, float]) -> float:
    if set(features) != set(model.coefficients):
        raise ValueError("features must match model coefficients")
    if any(
        not math.isfinite(float(value)) or float(value) <= 0
        for value in features.values()
    ):
        raise ValueError("feature values must be positive and finite")
    score = model.intercept
    for feature, coefficient in model.coefficients.items():
        score += coefficient * float(features[feature])
    if not math.isfinite(score):
        raise ValueError("prediction exceeds the finite numeric range")
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


def prediction_payload(
    model: ModelMetadata, features: dict[str, float]
) -> dict[str, Any]:
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
    print(
        json.dumps(
            prediction_payload(model, {"rooms": args.rooms, "sqft": args.sqft}),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
