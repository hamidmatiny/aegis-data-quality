---
name: trial-review
description: One-time initial validation — confirm free-pool dependency awareness, review the most recent real report from each specialist, produce one real findings-or-clean report before cadence.
allowed-tools: Read, Write, Bash, mcp__trinity__list_reports, mcp__trinity__get_report, mcp__trinity__list_agents, mcp__trinity__report, mcp__trinity__chat_with_agent, mcp__trinity__list_channel_groups, mcp__trinity__send_group_message
user-invocable: true
metadata:
  version: "1.0"
  created: 2026-09-14
  author: aegis-data-quality
---

# Trial Review

Narrow initial-scope run before any recurring schedule.

## Process

### Step 1: Dependencies

State clearly whether OmniRoute free-pool is confirmed for this agent. If unknown, say so and recommend Hamid ask `aegis-infra` for `/audit-omniroute` (you do not message infra directly unless an approved A2A edge exists — today route via CEO or Hamid).

### Step 2: Roster

Call `mcp__trinity__list_agents` if available; otherwise use Hamid's known roster and say the list is not live-verified.

### Step 3: One real pass

Run the same checks as `/review-fleet-outputs` against the **most recent** report from each other specialist that has published anything. If a specialist has no reports, say "no report available" — do not invent.

### Step 4: Output

Produce one real result: findings (then `/flag-data-drift` if warranted) or honest clean. Publish Trinity report `aegis_data_quality.trial_review` when available.

### Step 5: Onboarding

Remind Hamid: enable schedules only after he has reviewed this trial output.

### Step 6: Slack completed-task close-out (mandatory)

Post to `#aegis-data-quality` via `list_channel_groups` + `send_group_message`: what asked, who asked, what done, real outcome (findings or clean + report id), who reported to. Trinity `report` is not a substitute. See CLAUDE.md HARD GATE — Slack completed-task close-out.

Obey **CLAUDE.md HARD GATE — Slack / chat text hygiene** (universal): no `Co-Authored-By` / `Generated with Claude Code` / commit trailers — including on SI-slot runs.
