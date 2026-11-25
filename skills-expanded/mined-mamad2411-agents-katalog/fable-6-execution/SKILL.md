---
name: fable-6-execution
description: >-
  Execution v6.1 — manifest delivery; rce-proof OR ato-proof; partial until RCE/exhaustion.
version: 6.1.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
---

# Execution (v6.1)

**Playbook:** `Workflow/execution/PLAYBOOK.md`

## Reason first

Pick highest-probability manifest item. Plan verification command before running.

## Objective status

| Outcome | state.json |
|---------|------------|
| ATO proven, RCE still in plan | `objective_status: partial`, `objectives.ato: true` — stay in execution |
| RCE proven (`uid=`) | update `objectives.rce: true`; partial or achieved per scope |
| All scope met | `objective_status: achieved` |

**Do NOT** set campaign `status: completed` on ATO alone if RCE remains in methodology_plan.

## Output

- `execution/attempts.jsonl` — one valid JSON per line
- `execution/rce-proof.json` OR `execution/ato-proof.json` with live re-probe

Use `bin/fable-util` when running utilities (path-safe cwd).

## FORBIDDEN

- RCE claim from HTTP 200 alone
- Campaign complete on partial objective
- Cleartext passwords in chat or proof files
- GSocket/privesc before rce-proof
