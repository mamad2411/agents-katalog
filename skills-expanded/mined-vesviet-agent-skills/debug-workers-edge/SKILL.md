---
name: debug-workers-edge
description: Diagnose Cloudflare Pages and Workers failures at the edge — 5xx, binding errors, Wrangler deploy failures, DNS/cache issues, and context loss. Use when symptoms appear after deploy or only on Cloudflare runtime, not in local dev alone.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Debug Workers Edge

Use with the **Cloudflare Engineer** role for platform-layer failures. Escalate to `troubleshoot-service` when evidence points to application logic inside API handlers.

## When to Use

- 5xx or binding errors on Cloudflare runtime
- Wrangler deploy failures
- DNS/cache issues only on edge
- context loss after deploy

## Core Rules

- compare local preview vs deployed behavior before changing production
- read Workers/Pages logs and request IDs — do not guess from status codes alone
- separate binding misconfiguration from application exceptions
- prefer rollback or route disable for production incidents when blast radius is unclear
- get approval for production DNS, cache purge, or binding deletes per policy
- **WRANGLER-V4-REMOTE**: In Wrangler v4, `wrangler dev` defaults to local mode — use `--remote` flag explicitly to bind against real production D1/R2/KV resources; update any CI runbooks that assumed `--remote` as the default.
- **WORKERS-OBSERVABILITY-DASHBOARD**: Use the Workers Observability dashboard for custom P99 CPU charts, JSON/CSV log export, and shareable trace URLs — requires `"observability": { "enabled": true }` in `wrangler.jsonc` to persist logs.
- **OBSERVABILITY-BLOCK-REQUIRED**: `wrangler tail` does NOT persist logs without the `observability` block enabled in `wrangler.jsonc`. Add this block to all production Workers before any debugging session.

## Suggested Process

### 1. Capture Symptom

Record:

- URL, status code, environment (preview/production)
- time of first failure vs last deploy
- whether static assets vs API/Worker routes fail

### 2. Check Deploy And Config Drift

Verify:

- last successful deployment ID / commit
- wrangler config vs dashboard bindings
- secret presence (names only) in Dashboard vs `.dev.vars` locally
- `nodejs_compat` and compatibility date issues

### 3. Isolate Layer

| Signal | Likely layer |
| ------ | ------------- |
| Binding not found | Wrangler / env types |
| 1101 / script error | Worker code — collaborate with dev |
| SSL / DNS | dns_and_routing in edge spec |
| Stale asset | cache rules or purge scope |
| Turnstile failure | turnstile site keys / domains |

### 4. Apply Smallest Safe Fix

Examples:

- fix binding name or resource ID in repo
- redeploy previous artifact
- narrow cache purge (not whole zone without approval)
- adjust route pattern

### 5. Verify And Document

Run smoke_tests from edge-deployment-spec; update residual_risks for SRE/DevOps.

## Checklist

- [ ] environment and route scope captured
- [ ] deploy revision compared to failing window
- [ ] bindings and secrets checked (names only in notes)
- [ ] platform vs application layer decided
- [ ] smallest safe fix applied
- [ ] smoke tests pass after recovery

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and 
alidation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Failure Modes

- **Local-only assumption**: a fix is made locally and shipped without verifying on the deployed edge. Mitigation: always compare `wrangler dev --remote` against the deployed behavior before changing production.
- **Status code guessing**: a 5xx is "fixed" based on the status alone without reading logs. Mitigation: read Workers Observability logs and request IDs first; never guess.
- **Whole-zone cache purge**: a single-route cache issue triggers a full-zone purge. Mitigation: narrow the purge to the affected URL pattern; require approval for full-zone purges.
- **Missing observability block**: `wrangler tail` is used to debug a production issue but logs are not persisted. Mitigation: require `"observability": { "enabled": true }` in `wrangler.jsonc` for all production Workers.
- **Wrangler v4 default surprise**: a CI runbook assumes `wrangler dev` defaults to `--remote`; in v4 it defaults to local. Mitigation: pass `--remote` explicitly; update runbooks.
- **Secret leaked in notes**: secret names (or values) are pasted into debug notes or chat. Mitigation: reference secrets by name only; never log values.
- **Rollback skipped**: an incident is "fixed" without confirming the previous artifact is still available for rollback. Mitigation: verify the previous deployment ID is rollbackable before applying the new fix.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a debug session may drift into changing application code outside the incident's scope. Mitigation: scope every debug change to the failing layer; open a separate task for unrelated fixes.
- **ASI03 Identity & Privilege Abuse**: a debug command that requires elevated scopes (e.g., secret rotation, DNS update) must be approved; reject ad-hoc privilege escalation.
- **ASI04 Supply Chain**: Wrangler CLI, observability agents, and edge config must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI07 Inter-Agent Communication**: the incident report is consumed by SRE and DevOps; emit a structured contract so each role can validate the remediation.
- **ASI09 Human-Agent Trust Exploitation**: do not present a fix as "resolved" without a smoke test on the deployed edge; surface the residual risk honestly.

## Related Skills

- **wrangler**: Wrangler CLI for deploying, developing, and managing Workers
- **debug-runtime-platform**: Broader platform issues shared with DevOps/SRE
- **troubleshoot-service**: Application-level API or Astro handler bugs
