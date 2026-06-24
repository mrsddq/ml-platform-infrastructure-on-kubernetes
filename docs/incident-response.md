# Incident Response

## SLO Sketch

| SLI | Target |
|---|---:|
| Successful prediction responses | 99.5% |
| p95 prediction latency | < 500 ms |
| Drift-warning rate | Investigate sustained increase |

## Failure Scenarios

| Scenario | Detection | Mitigation |
|---|---|---|
| Bad model version | Prediction warnings or business validation failures | Revert Helm model version |
| API crash loop | Pod restart alerts | Roll back image tag |
| Metrics missing | Prometheus scrape failure | Check ServiceMonitor labels and service port |
| Input range shift | Drift warning counter increase | Review data profile and retraining need |

## RCA Notes

- Record deployed image tag and model version.
- Capture request sample, warning count and metrics window.
- Compare with previous model version.
- Add a regression test or quality gate before re-promoting.
