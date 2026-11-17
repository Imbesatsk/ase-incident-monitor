# Incident Response Runbook: High 500/503 Error Rate

## 1. Alert Trigger
Triggered automatically by `incident_monitor.py` when >= 3 `[ERROR]` entries occur.

## 2. L1/L2 Triage Steps
1. Filter recent errors in logs:
   `grep "ERROR" app.log | tail -n 10`
2. Test upstream gateway health:
   `curl -I https://httpbin.org`
3. Inspect generated incident tickets:
   `cat incidents.log`

## 3. Escalation Matrix
- **503 Gateway Unavailable:** Monitor upstream recovery for 5 minutes and update status page.
- **500 DB Timeout:** Restart connection pool; escalate to L3 Backend Engineering if unresolved after 10 minutes.
