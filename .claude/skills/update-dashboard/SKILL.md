---
name: update-dashboard
description: Refresh dashboard.yaml with the most recent fleet quality review counts
allowed-tools: Read, Bash, mcp__trinity__report, mcp__trinity__list_channel_groups, mcp__trinity__send_group_message
user-invocable: true
metadata:
  version: "1.1"
  created: 2026-09-14
  updated: 2026-10-09
  author: aegis-data-quality
---

# Update Dashboard

Refresh `dashboard.yaml` from `memory/review-baselines.md` and `memory/findings.md`.

The refresh is deterministic, so a script does it. Do **not** hand-edit `dashboard.yaml`, re-read the memory files to recount, or call `list_reports` / `get_report`. On 2026-10-09 the 12:00 and 18:00 UTC scheduled runs, and the retry, hit the 3600s limit while doing that work in the LLM.

## Process

### Step 1: Run the script (one call)

```bash
python3 scripts/update_dashboard.py
```

It prints one JSON line: `updated`, `last_review`, `reports_reviewed`, `flags_raised`, `findings_escalated`, `recent`, `changed`.

- Unknown counts stay `—`. The script never invents a number.
- `changed: false` means nothing new since the last refresh. That is a valid outcome. Do not retry.
- Non-zero exit or `error` in the JSON → report the error as-is and go to Step 3. Do not hand-edit as a fallback.

### Step 2: Optional KPI report

If `mcp__trinity__report` is available and `changed` is true: `report_type` `aegis_data_quality.kpi_snapshot`, `display_hint` `kpi`, payload = the script's JSON. Skip silently if the tool is unavailable.

### Step 3: Slack completed-task close-out (mandatory)

Post one short message to `#aegis-data-quality` with `list_channel_groups` + `send_group_message`. Include: who asked (the schedule name or Hamid), that the script ran, the JSON summary or the error, and whether anything changed. Obey the CLAUDE.md text-hygiene HARD GATE: no `Co-Authored-By` lines and no Claude Code footers.

Stop after the close-out. This skill has no other steps.
