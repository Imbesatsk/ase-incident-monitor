# Automated API & Log Incident Responder

A lightweight Python and Linux CLI monitoring solution designed to simulate production payment traffic, detect HTTP 500/503 error spikes in real time, verify external API health, and automate incident ticketing.

## Architecture & Components
- `app_simulator.py`: Simulates a live production payment service generating timestamped `INFO`, `WARN`, and `ERROR` logs.
- `incident_monitor.py`: Tails live application logs, enforces error-rate thresholds (3 errors/window), verifies upstream API availability (`200 OK`), logs incident tickets (`incidents.log`), and dispatches webhook alerts.
- `docs/RUNBOOK.md`: L1/L2 Standard Operating Procedure (SOP) for incident triage and escalation.
- `docs/POST_MORTEM_RCA.md`: Root Cause Analysis report documenting a simulated SEV-2 outage.

## Quick Start
```bash
# Terminal 1: Start mock service
python app_simulator.py

# Terminal 2: Start incident monitor
python incident_monitor.py
```
