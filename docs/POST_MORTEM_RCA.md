# Post-Mortem Root Cause Analysis (RCA)

- **Incident ID:** INC-2026-001
- **Severity:** SEV-2 (Partial Service Degradation)
- **Duration:** 14 Minutes

## Summary
Automated log monitoring detected consecutive `503 Service Unavailable` and `500 Internal Server Error` spikes on the payment gateway.

## Root Cause
Upstream payment gateway rate-limiting combined with unclosed database connections caused cascading timeouts.

## Corrective Actions
1. Deployed real-time log tailing and threshold alerting (`incident_monitor.py`).
2. Added automated external API health verification checks upon alert trigger.
