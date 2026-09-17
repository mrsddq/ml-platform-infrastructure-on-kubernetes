from __future__ import annotations

from threading import Lock


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = Lock()
        self.requests = 0
        self.errors = 0
        self.drift_warnings = 0

    def observe(self, ok: bool, warnings: int = 0) -> None:
        with self._lock:
            self.requests += 1
            if not ok:
                self.errors += 1
            self.drift_warnings += warnings

    def prometheus_text(self) -> str:
        with self._lock:
            requests, errors, warnings = self.requests, self.errors, self.drift_warnings
        return "\n".join(
            [
                "# HELP model_api_requests_total Total prediction requests.",
                "# TYPE model_api_requests_total counter",
                f"model_api_requests_total {requests}",
                "# HELP model_api_errors_total Total failed prediction requests.",
                "# TYPE model_api_errors_total counter",
                f"model_api_errors_total {errors}",
                "# HELP model_api_drift_warnings_total Total input drift warnings.",
                "# TYPE model_api_drift_warnings_total counter",
                f"model_api_drift_warnings_total {warnings}",
                "",
            ]
        )
