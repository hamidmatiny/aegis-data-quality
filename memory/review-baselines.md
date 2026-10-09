---
name: review-baselines
description: Schema rules and prior clean/flagged baselines
metadata:
  type: reference
---

# Review Baselines

- 2026-09-16T12:10:00Z: Reviewed 12 reports. 
  - Flagged: `8b015d78-...`, `dcbdfe16-...` (MRR arithmetic contradiction, $0 vs $29 endpoint conflict).
  - Clean: `f234c1dd-...`, `d6e16194-...`, etc.

- 2026-09-17T00:10:00Z: Reviewed MRR contradiction escalations `eb404515-98f3-444e-ae5e-3982daece376` and `3410edb1-aabe-4939-aa0f-6adcfaafd3f6`.
  - Clean: Both reports indicate the issue is now RESOLVED via corp-orchestrator fix.

- 2026-09-17T12:44:00Z: Reviewed recent batch of 23 reports (including aegis-ceo escalation triage and trajectory reports).
  - Clean: MRR contradiction confirmed resolved; security vulnerability reports (`c44a56dd`) correctly triaged; no new unflagged drift or schema violations.

- 2026-09-18T12:44:00Z: Reviewed recent fleet reports (aegis-ceo escalation triage `c44a56dd` and `3410edb1`).
  - Clean: Security triage report valid; MRR resolution documentation consistent. No new drift or schema violations.

- 2026-09-18T00:05:00Z: Reviewed recent batch of reports (since last review).
  - Clean: No new reports found in last 24h; existing security/MRR escalations remain stable/resolved.

- 2026-09-19T12:05:00Z: Reviewed recent fleet reports (`5bdcebdd-8731-483c-8131-4b52395180e1` trajectory review & `4c6d4ed2-a908-476d-a0e1-c570fa5273e8` GitHub pulse).
  - Clean: MRR stable at $0.00 (no contradiction), GitHub pulse and CI statuses consistent. No drift or schema violations.

- 2026-09-20T00:10:00Z: Reviewed recent fleet reports (`5bdcebdd-8731-483c-8131-4b52395180e1` & `4c6d4ed2-a908-476d-a0e1-c570fa5273e8`).
  - Clean: MRR stable at $0.00, no schema drift, GitHub pulse consistent with last reported status. No new drift found.

- 2026-09-20T12:00:00Z: Reviewed recent fleet report `ae68ba5f-9ee2-4b18-92ee-8f89570672a7` (Trajectory Review 2026-09-20).
  - Clean: MRR stable at $0.00, 0 paying subscribers, CI green (commit ad446a46), CVE count stable at 21. No fabricated comparison fields or MRR contradiction detected.

- 2026-09-20T12:09:21Z: Verified latest report sweep.
  - Clean: No new reports published since 2026-09-20T12:02:38Z.

- 2026-09-21T00:15:00Z: Reviewed recent fleet reports (`c5adafba-3392-4b4c-aafd-07da2e027d0a` escalation triage for pii-03-retest & `ae68ba5f-9ee2-4b18-92ee-8f89570672a7` trajectory review).
  - Clean: Escalation triage report correctly structured with valid metadata and citation; trajectory review confirms stable $0.00 MRR with zero schema drift or fabricated MRR comparisons. No new drift found.

- 2026-09-21T13:30:00Z: Reviewed `a58083e5-9ce1-4e75-9749-6e5eb3f04c1d` (Escalation Triage — aegis-redteam 2 confirmed live bypasses).
  - Clean: Schema version 1, display hint markdown, valid metadata, consistent source and tracking. Escalation triage correctly structured. No fabricated MRR or metrics.

- 2026-09-22T00:00:00Z: Reviewed recent fleet report `a58083e5-9ce1-4e75-9749-6e5eb3f04c1d` (Escalation Triage — aegis-redteam 2 confirmed live bypasses).
  - Clean: Schema version 1, display hint markdown, valid metadata, consistent source and tracking. No new unflagged drift or schema violations.

- 2026-09-22T12:00:00Z: Reviewed recent fleet reports (`a1d4604c-2e5f-47f7-9600-e7eaff8f8e3d` trajectory review & `2dbfc4f7-dd6e-4253-b04d-95e2c4627b07` GitHub pulse).
  - Clean: Trajectory review stable with consistent MRR/signup metrics; GitHub pulse accurately reports recent commits and PR activities with valid schema. No new drift or schema violations found.

- 2026-09-23T00:02:46Z: Reviewed recent fleet reports (`ce43cfb4-33ad-4d33-899d-d8b879edaa44` escalation triage for novel-15-terraform-hcl, `a1d4604c` trajectory review, and `2dbfc4f7` GitHub pulse).
  - Clean: Escalation triage report correctly documents novel-15-terraform-hcl live bypass with policy pack 0.3.1 and slack delivery confirmation; trajectory review maintains verified $0.00 MRR and 32 CVEs; GitHub pulse matches commit history. No fabricated comparisons or schema violations.

- 2026-09-23T12:15:00Z: Reviewed recent fleet reports (trajectory review `1b7dfc5a`, GitHub pulse `962a13fa`, escalation triage `daf02bda` + `c8e45e90`).
  - Clean: Reports correctly reflect the status of novel-15-terraform-hcl bypass and its IaC scope update; trajectory review and GitHub pulse remain consistent with established stable baselines ($0 MRR, 32 CVEs). No schema drift or fabricated metric comparisons detected.

- 2026-10-08T17:00:00Z: Reviewed recent fleet reports (`ab7f50a6-2648-44dc-a68e-6af1a12912a7` escalation triage, `2ac63f95-c795-4773-b9df-682219980a1a` trajectory review).
  - Clean: Escalation triage report correctly structures persistence of BYPASS-005/006, consecutive batch count, and Slack confirmation; trajectory review KPIs ($0 MRR, 32 CVEs) are consistent and maintain established baseline. No fabricated comparisons or schema violations detected.

# Schema Rules

- MRR Arithmetic: All `mrr` and `paying_subscribers` fields must be consistent across endpoints within a single report. If one endpoint returns a value and another returns null/0 for the same metric, flag as arithmetic contradiction.
- Timestamp Integrity: All report timestamps and period boundaries must be explicitly validated against upstream generation times to prevent stale data re-emission.
- Threat Intel Severity Enum & Optional Metadata: Security and threat-intel reports (`aegis-threat-intel`) must use strict enum values for severity (`critical`, `high`, `medium`, `low`). Optional fields like `cve_id` may be null for internal findings, but schema validation must not invent default CVE IDs or inflate severity when metadata is missing.
- Display Hint & Schema Version Consistency: Every published specialist report must declare a valid `schema_version` (>= 1) and matching `display_hint` (`table`, `kpi`, `markdown`, `timeline`, or `json`).
- CVE Delta Tracking: Security/vulnerability scans must report CVE counts with explicit deltas relative to the previous scan to avoid ambiguity. If delta is missing but count changed, flag as ambiguous.
  - **Why:** Prevents dashboard rendering failures and silent schema degradation when payloads do not match declared view hints, and ensures security metric changes are explicitly auditable.
  - **How to apply:** Verify report metadata and payload keys match the expected display hint schema and ensure security metrics have explicit deltas before confirming a clean review sweep.
