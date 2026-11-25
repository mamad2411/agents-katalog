---
name: deploy-watch
description: Deploy and cluster health — read CI/CD pipeline state and monitoring alerts, assess a rollout or a k8s cluster (nodes, pods, events) as healthy, degraded or failing, triage the alerts, and recommend an action, recorded as a deploy-status handoff. Use to check deploy, rollout, pipeline or cluster health. Not an active incident (incident-response), cutting a release (release), or fixing code or manifests (develop).
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Deploy watch (phase workflow)

The rollout-observability phase: read an environment's CI/CD pipeline state and active alerts,
assess rollout health, and recommend an action — recorded as a `deploy-status` handoff. The
assessment lives in the plugin's `bin/af.py`; external state arrives through the
**adapter seam** (`PipelineSource` / `AlertSource`), so this skill is provider-agnostic. (Design:
`docs/architecture/quality-ops.md` in the agentic-forge repository.)

> **Scope:** a **point-in-time snapshot** — one assessment pass over the current state, not a
> continuous watch; re-run it to re-check. Continuous poll-until-terminal-state is out of scope
> for now.

## When to use

When the task is to assess a deploy/rollout/pipeline's health or status for an environment. **Not**
for handling an active incident (`incident-response`), cutting a release (`release`), or building
(`develop`).

## Process

The assessment prints one JSON object and needs nothing installed:

```
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" deploy-status --environment <environment> --repo .
python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" deploy-status --environment <environment> --snapshot <file>
```

1. **Get the state through a source.** In a live repo, the first form above reads it (it auto-detects
   the `gh` CLI; see [references/connectors.md](references/connectors.md)), and alerts from an MCP
   connector go beside it with `--alerts-json` —
   recent deploys + active alerts for the environment. When handed a recorded snapshot (JSON of
   `deploys` + `alerts`), pass it to the second form; a status or severity outside the vocabulary is
   refused rather than read as healthy. Its deploys are ordered by `at`, whatever order the file has,
   and more than one without an `at` is refused, since nothing then says which is latest. When the environment is a **Kubernetes cluster/namespace** (nodes, pods,
   deployments, events — live `kubectl` reads or a recorded snapshot), follow
   [references/k8s-health.md](references/k8s-health.md): the observation→verdict mapping and the
   scheduled/headless recipe live there; the output is the same `deploy-status` handoff.
2. **Assess.** `deploy-status` returns the
   `deploy-status` mapping: `pipeline` health, from the latest run of each workflow (failing on a
   failed one or a `critical` alert; degraded on one in flight or cancelled, or a `warning`; else
   healthy), the deploy list, the alert counts, and a `recommended_action`. **`unavailable` names
   what was not read**: no `gh`, or a source that failed, is `unavailable.pipeline`; no alert source
   is `unavailable.alerts`. A missing pipeline, or an alert source that is set and fails, makes health
   `unknown` unless what was read says worse; with no alert source at all the pipeline's reading stands.
   Say so in the report: never "no deploys" or "no alerts" for what was not read. It does not know which branch a
   run was on.
3. **Record.** Write a `deploy-status` handoff artifact (frontmatter `type` (= `deploy-status`),
   `environment`, `pipeline`, `deploys`, `alerts`, `action`) plus a short report; lead with the
   health and the recommended action. Validate the header
   (the read-back below; see
   [handoff.md](../../patterns/handoff.md)).
   Then **read the file back** — `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type deploy-status` —
   and fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).
4. **Recommend, don't act.** Never trigger a rollback or deploy — surface the action for a human.

## Output

A `deploy-status` handoff: environment, pipeline health, recent deploys, alert triage, and the
recommended action. No rollout action is executed.

## Definition of done

- Health is assessed via `deploy-status` (failing > degraded > healthy) from the real state, and
  what `unavailable` names is reported as not read.
- Alerts are triaged; the recommended action matches the health (roll back on failing; continue on
  healthy).
- A valid `deploy-status` artifact is produced; no rollout action is executed.
