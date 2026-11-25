---
name: drive-skill-dogfood
description: Drive cybernetic skill execution end-to-end via the aflow-local MCP as operator + product engineer — deliver a real feature through the platform's OWN skills (open-pr-from-request, review-pull-request, pr-shepherd) while the gap-log (where skills/tasks/evaluators/guidance/MCP fall short) is the deliverable. Use when asked to "drive a feature via the skills", dogfood the coding lane, or stress-test skill execution.
---

# Drive Skill Execution — operator + product-engineer dogfood

You are the **operator + product engineer**, NOT the builder. The platform's cybernetic skills produce every artifact (design doc, code, PRs); your job is to **drive them via the MCP** and keep a running **gap-log** — that log is the real deliverable. Only do what an operator can from the UI: talk to Helmsman, start/approve skill runs, review PRs on GitHub, inspect runs. Do **not** hand-write the feature yourself.

## Setup

1. Connect the MCP: `mcp__aflow-local__auth_status`, then `mcp__aflow-local__space_list`. **Pass `space_id` explicitly on every call** (there is no implicit default).
2. Confirm the target: `run_operation` → `workflow.campaign.list` shows the installed campaigns (their `repo` coordinate) and skills. Reuse the existing campaign's `campaignId`.

## The loop — plan fine, execute coarse

Design → review the design → iterate → implement (in slices) → review → iterate or done.

- **Design first** for anything meaty: drive `open-pr-from-request` to produce a **design doc** (a docs-only PR), not code. The deep discovery runs inside `code.agent.run` (a full checkout) — robust and grounded. Do NOT do broad discovery through conversational Helmsman: it over-parallelizes on wide work and is fragile. Route heavy work through skills.
- **Your involvement point = the `plan-approve` HITL gate.** Pull the framed plan with `workflow.run.detail`, review it, then `workflow.run.resume` with `{resolution:{mode:'replace_output',output:{decision:'approved'}}}` (or reject). Review the harness _brief_ before approving; review the resulting _diff_ rigorously after.
- **Review** with `review-pull-request` (it fact-checks the diff — incl. cited paths). **Iterate** with `open-pr-from-request` in **fix mode** (`prNumber` + the combined review findings). Re-review.
- **Verify security-critical / fail-closed code YOURSELF**, regardless of what the agent or the review reports.
- **Merge is a human action** — the bot tends/confirms readiness; you (or a human) merge.

## Calibrating the execution cycle (who decides, how)

The phase plan is for _understanding + dependencies_ — it is NOT the execution unit. **You** size each `code.agent.run` cycle at run-scoping time. Size to the **MIN** of: (i) what the harness implements _coherently_ in one session (~1–1.5k LOC / one subsystem — quality decays past that), (ii) what passes its own checks as a unit, (iii) what a human reviews in one sitting. **Cut at layer seams** (schema/server vs web) and **dependency boundaries**. Start medium; calibrate the next cycle from observed load — did it finish clean? coherent diff? checks pass? review digestible?

## The gap-log (the deliverable)

Log every place a **skill / task / evaluator / guidance / MCP** falls short. Classify (platform · skill-coverage · MCP-driving) and severity. **Collect, don't fix mid-stream** — implementation is the richest gap source and it tells you whether a gap generalizes; batch-fix afterward on a branch with several green commits (each checks-clean before the next). The exception is a _hard-blocker_ that taxes every cycle. Persist findings to memory (`project_*.md` + a one-line `MEMORY.md` pointer); the gap-log is what makes the dogfood worth running.

## Known MCP-driving recovery

- Long `run.start` / `run.resume` hit a **configured wait timeout — NOT a drop**. The result now carries `timed_out_waiting` + a `note` ("still running, did NOT fail") + the `session_id`. Recover via `workflow.run.list_attention` / `workflow.run.detail`, or re-call with a larger `timeout_seconds`. The orchestrator outlives the client — the run lands server-side even when the response is lost.
- `run.detail` payloads are large; if one exceeds the tool limit it is saved to a file — `grep` it, don't re-fetch.
- `code.agent.run` review can flake "no usable verdict" on prose/docs diffs — retry the failed task (`workflow.run.resume` `retry_failed_task`).

## Improve the MCP driving surface as you go

The MCP server (`apps/aflow-mcp`) is **your own tool** — so it is the exception to "collect, don't fix." When driving surfaces MCP friction (an opaque error, a missing recovery affordance, a payload too large to read, a confusing default), **fix the server then and there** to make the rest of the session — and future sessions — easier and more reliable. Land each as a small typecheck-clean commit. Past fixes: a structured wait-timeout signal (`timed_out_waiting` + `note` + runId), required explicit `space_id` (no stale default). Keep finding and closing these as you discover more cases (e.g. a compact `run.detail` mode, clearer error envelopes, returning the runId on every long call).
