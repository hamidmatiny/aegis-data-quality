---
name: flag-data-drift
description: Package a concrete fleet-output data/quality finding and deliver it to aegis-ceo; claim escalated only after confirmed chat_with_agent delivery.
allowed-tools: Read, Write, Bash, mcp__trinity__chat_with_agent, mcp__trinity__report, mcp__trinity__list_reports
user-invocable: true
metadata:
  version: "1.0"
  created: 2026-09-14
  author: aegis-data-quality
---

# Flag Data Drift

Escalate a **specific** inconsistency (report id/title, field, expected vs actual, why it matters for honesty). Advisory only — no remediation.

## Process

### Step 1: Package the finding

Include at minimum:

- Source report_type / report id / title / agent if known
- Field or schema issue
- Expected vs actual (or "field absent in source")
- Why this is drift / fabrication-class / schema break — one sentence

### Step 2: Deliver to aegis-ceo

```
mcp__trinity__chat_with_agent
  name: aegis-ceo
  message: /handle-anomaly (or plain escalation) + the packaged finding
```

Requires live A2A permission `aegis-data-quality` → `aegis-ceo` (grant at onboard; manager hub).

**Fail-closed:** claim **"escalated to aegis-ceo"** only after confirmed successful delivery. On failure: **"flagged, delivery failed"** (+ what failed). Optionally append operator-queue alert if delivery failed.

### Step 3: Memory

Append to `memory/findings.md` with delivery status and execution_id if returned.

### Step 4: Trinity report

If available: `report_type` `aegis_data_quality.drift_flag`, `display_hint` `markdown`.

## Known failure modes

- Claiming escalated when `chat_with_agent` failed or returned Access denied.
- Messaging the authoring specialist directly instead of `aegis-ceo` (forbidden by hybrid A2A protocol).
