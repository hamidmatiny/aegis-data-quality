# AEGIS Data/Quality Target Architecture

**Last updated:** 2026-09-14

## Direction

Stay narrow and cheap: catch fabrication/schema/drift class errors in fleet *outputs*. Never gain write access, never message specialists cross-branch directly, never leave free-pool without `aegis-infra` reassignment.

## Planned Capabilities

- **Schema registry per report_type** — structured expected fields for `aegis_analyst.*`, `aegis_threat_intel.*`, `aegis_core_infra.*`, VP reports — so reviews are deterministic. Depends on: stable report_type contracts from each specialist.
- **Baseline deltas** — lightweight memory of last accepted values per report_type so unexplained jumps are flaggable without re-reading the entire history every run.
- **Cadence after trial** — enable `/review-fleet-outputs` schedule only after Hamid reviews `/trial-review` output and free-pool is confirmed.
- **A2A table update** — when this agent is live on Trinity, add it under Data/Quality in `aegis-infra` `docs/a2a-routing.md` (manager still `aegis-ceo` until a Data head exists).
