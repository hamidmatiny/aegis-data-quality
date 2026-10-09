---
name: review-fleet-outputs
description: Review recent published fleet reports for drift, schema inconsistency, or invented fields; produce findings or an honest clean result. Never messages other specialists directly.
allowed-tools: Read, Write, Bash, Grep, mcp__trinity__list_reports, mcp__trinity__get_report, mcp__trinity__list_agents, mcp__trinity__report, mcp__trinity__list_reports
user-invocable: true
metadata:
  version: "1.0"
  created: 2026-09-14
  author: aegis-data-quality
---

# Review Fleet Outputs

Pull recent published reports from other personal-fleet specialists, check consistency and schema honesty, and record baselines. Escalate concrete issues with `/flag-data-drift` — do not invent findings.

## Process

### Step 1: Confirm sources

Prefer Trinity report APIs when available:

- `mcp__trinity__list_reports` (filter by known `report_type` prefixes / recent hours)
- `mcp__trinity__get_report` for full payloads

Target report families (adjust from live list — do not invent agents):

- `aegis_analyst.*` (`aegis-analyst`)
- `aegis_threat_intel.*` (`aegis-threat-intel`)
- `aegis_core_infra.*` (`aegis-core-infra`)
- VP / brain reports if present (`the-brain`)

If Trinity reports are unavailable locally, say so and stop or limit to any files Hamid explicitly provided — never fabricate a review.

### Step 2: Field-existence rule (non-negotiable)

Before treating a mismatch as real:

1. Confirm the cited source actually returns / contains that field.
2. If the field is absent, flag **fabricated/defaulted comparison** (or missing schema), not a numeric delta.

**MRR / paying subscribers specifically:** Live numbers live only on `mrr_snapshot` (from `/bev/summary` and, after the SSOT fix, also `/bev/trajectory`). Never treat CEO `report.result` narrative text (e.g. "MRR: $29") as an endpoint field — that is narrative-only and caused false $29 vs $0 escalations. If a report compares narrative text to `mrr_snapshot`, flag **fabricated comparison**, not an MRR integrity bug.

This is the class of bug this role exists to catch.

### Step 3: Checks

For each report in the batch:

1. **Schema** — expected keys present? Types look right? Silent omissions?
2. **Drift** — vs `memory/review-baselines.md` (or prior report of same type): unexplained jump/drop/contradiction?
3. **Citation honesty** — does the report claim a source field that the payload/sources do not include?

### Step 4: Record

Append a short entry to `memory/review-baselines.md` (create if missing): timestamp, reports reviewed, clean vs flagged ids.

### Step 5: Escalate or clean

- Concrete issues → run `/flag-data-drift` (or hand off that skill) with citations.
- Clean batch → say so plainly: "reviewed N reports, no drift found."

### Step 6: Trinity report

If `mcp__trinity__report` available:

- `report_type`: `aegis_data_quality.fleet_review`
- `display_hint`: `markdown` or `kpi`
- payload object with counts + finding summaries

Skip silently if unavailable.

### Step 7: Slack completed-task close-out (mandatory)

Post to `#aegis-data-quality` via `list_channel_groups` + `send_group_message`: what asked, who asked, what done, real outcome, who reported to. Trinity `report` is not a substitute.

Obey **CLAUDE.md HARD GATE — Slack / chat text hygiene** (universal): no `Co-Authored-By` / `Generated with Claude Code` / commit trailers — including on SI-slot runs.

## Outputs

- Updated `memory/review-baselines.md`
- Optional escalation via `/flag-data-drift`
- Optional Trinity report
- Slack close-out (hygiene HARD GATE applies)
