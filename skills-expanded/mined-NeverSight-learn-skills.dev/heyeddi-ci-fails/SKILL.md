---
name: heyeddi-ci-fails
description: "Diagnose failing GitHub Checks for a PR head: fetch evidence, write ephemeral ci-fails report, optional local fix loop. Never merge without authorize merge. Companion to /heyeddi fails."
version: 1.0.0
product-version: 3.4.2
author: HeyEddi-com
disable-model-invocation: true
---

# HeyEddi CI Fails

Local agent counterpart to App `/heyeddi fails`: fetch failing Checks, write a diagnosis report, optionally fix with evidenced verify. **Stack-agnostic** (log-driven).

## Ephemeral artifacts (do not commit)

| File | Role |
|------|------|
| `pr-<N>-ci-fails-raw.json` | Raw gh evidence |
| `pr-<N>-ci-fails.md` | Diagnosis report |

Never commit these. GitHub Checks remain SSOT.

## Pipeline

```
fetch_failing_checks --pr <N>
write_ci_fails_report --pr <N> --force
→ fill likely cause / proposed fix from logs
(optional) apply fixes when user asks
discover_and_verify [--run]
assert_no_merge --check
```

Also tell the user they can comment `/heyeddi fails` on the PR for hosted App analysis (billable when that path applies).

## Hard rules

- Never invent failure causes without citing check evidence
- Never merge without **authorize merge**
- Never claim Spot runners ran

## Tools

| Tool | Purpose |
|------|---------|
| `fetch_failing_checks` | Read-only failing Checks rollup |
| `write_ci_fails_report` | Write `pr-<N>-ci-fails.md` |
| `discover_and_verify` | Evidenced verify after fixes |
| `assert_no_merge` | Merge hard gate |

## When complete

```bash
python .agents/skills/heyeddi-orchestrator/scripts/suggest_next_skill.py \
  --current-skill heyeddi-ci-fails --project-root .
```
