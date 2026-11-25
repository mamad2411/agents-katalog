---
name: demo-runner
description: Route to and run the repo's existing demo, verification, and proof scripts. Use when asked to run the demos, verify the handoff, show the stakeholder demo, or prove a triage path works.
---

# Demo Runner

Every demo and verifier in this repo is already a script. This skill is a
router: pick the right script, run it, interpret failures. `DEMOS.md` at the
repo root is the index — read it first when unsure which demo the user means.

## Script map

| Ask | Run |
|-----|-----|
| Verify the whole v2 handoff package | `scripts/verify-kagent-triage-v2-handoff.sh` |
| Verify one demo statically | `demos/<name>/scripts/verify-demo.sh` (sre-first-contact, byo-agent-showcase, kb-gitlab-mcp-update) |
| Run the BYO agent showcase | `demos/byo-agent-showcase/scripts/run-demo.sh` |
| Smart-triage fan-out proof | `a2a/smart-triage-fanout-demo/scripts/run-smart-triage-demo.sh`, `prove-*.sh`, `replay-alert.sh` |
| HITL / platform-memory demos | `a2a/kagent-hitl-skills-demo/scripts/run-demo.sh`, `a2a/platform-memory-showcase-demo/scripts/run-demo.sh` |
| Chaos demo | `chaos/litmus/run-demo.sh` |
| Verify all work-agent bundles | `work-agent-bundles/scripts/verify-all-bundles.sh` |
| Lifecycle eval scoring | `work-agent-bundles/lifecycle-evaluation-review-manager/` (`score-lifecycle-run.py` and helpers) |
| Grafana MCP / observability smoke | `scripts/observability/smoke-grafana-mcp.sh`, `scripts/observability/verify-k-agent-observability.sh` |
| Invoke an agent live | `scripts/kagent-a2a-invoke.sh --agent <name> --text '...'` |

## Rules

- Static verifiers (`verify-demo.sh`, `verify-bundle.sh`) prove file/marker
  consistency only — never present a static pass as proof of live cluster
  behavior.
- Interpret failures before rerunning: a verifier failure names the missing
  file or marker; fix the cause, not the check.
- **Destructive helper — human confirmation required:**
  `work-agent-bundles/argo-workflow-retention-cleanup/**/delete-completed-workflows-batched.sh`
  deletes workflows. It is gated by `--dry-run`/`--yes`; never run it with
  `--yes` without an explicit human go-ahead in this session.
