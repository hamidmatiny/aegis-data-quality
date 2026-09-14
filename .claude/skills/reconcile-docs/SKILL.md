---
name: reconcile-docs
description: Check that CLAUDE.md, README, ARCHITECTURE/TARGET-ARCHITECTURE, skills, and subagents are mutually consistent — reports drift and applies approved fixes.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
user-invocable: true
metadata:
  version: "1.0"
  created: 2026-09-14
  author: aegis-data-quality
  changelog:
    - "1.0: Initial version — dependency-graph-driven coherence check"
---

# Reconcile Docs

> reconcile-docs v1.0 — recent: Initial version — dependency-graph-driven coherence check

Keep documentation honest. Read the Artifact Dependency Graph in `CLAUDE.md`. Source wins; descriptive targets (`README.md`, `ARCHITECTURE.md`) get fixed; prescriptive sources are flagged for humans.

## Process

1. Parse artifacts/sync_skills from CLAUDE.md
2. List skills, README, ARCHITECTURE, TARGET-ARCHITECTURE, template schedules
3. Check CLAUDE↔skills, README↔reality, ARCHITECTURE↔reality, TARGET↔ARCHITECTURE, schedules↔template
4. Report CONSISTENT / DRIFT / MISSING
5. Interactive only: apply approved descriptive-target fixes

## Outputs

Drift report; optional approved edits to descriptive targets.
