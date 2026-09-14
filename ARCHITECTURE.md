# AEGIS Data/Quality Architecture (Current State)

**Last updated:** 2026-09-14

## Overview

Single-agent Trinity scaffold. Reads fleet published reports (Trinity `list_reports` / `get_report` when deployed) and local baselines in `memory/`. Flags to `aegis-ceo` via MCP `chat_with_agent`. No write credentials.

## Components

### Skills
- `/review-fleet-outputs` — drift/schema review of recent specialist reports
- `/flag-data-drift` — escalate a concrete finding to `aegis-ceo`
- `/trial-review` — one-time initial validation
- `/onboarding`, `/update-dashboard`, `/reconcile-docs`

### Subagents
None.

### Data & State
- `onboarding.json` — setup progress
- `dashboard.yaml` — last review snapshot
- `memory/review-baselines.md` — schema/baseline notes (created on first review)
- `memory/findings.md` — escalated findings (created on first flag)

### Schedules
Declared in `template.yaml`, all `enabled: false` until trial approved.

## Trinity Integration

Intended free-pool OmniRoute (`gemini/gemini-3.7-flash`). Resources: 1 CPU / 1g. Report types: `aegis_data_quality.fleet_review`, `aegis_data_quality.trial_review`, `aegis_data_quality.drift_flag`.
