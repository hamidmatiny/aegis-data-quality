---
name: update-dashboard
description: Refresh dashboard.yaml with the most recent fleet quality review counts
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__trinity__list_reports, mcp__trinity__report
user-invocable: true
metadata:
  version: "1.0"
  created: 2026-09-14
  author: aegis-data-quality
---

# Update Dashboard

Refresh `dashboard.yaml` from the latest `/review-fleet-outputs` / `/trial-review` results (memory and/or Trinity reports).

## Process

1. Read `memory/review-baselines.md` and `memory/findings.md` if present; optionally `list_reports` for `aegis_data_quality.*`.
2. Update `updated`, Last Review, reports reviewed, flags raised, Recent Reviews list.
3. Optional KPI report: `aegis_data_quality.kpi_snapshot`.
4. Confirm what changed.
