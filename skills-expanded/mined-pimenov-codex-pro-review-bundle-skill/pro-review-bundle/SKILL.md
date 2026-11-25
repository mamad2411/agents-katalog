---
name: pro-review-bundle
description: Package complex plans, architecture decisions, production-adjacent changes, consulting proposals, discovery packets, or nuanced writing for safe GPT Pro review before implementation. Use when the user asks to use GPT Pro, Pro review, oracle-style review, "build a review bundle", "send this to Pro", or when a plan has high cost of missed nuance across code, product, operations, production, trackers, server, auth, data, routing, or client-scope boundaries.
---

# Pro Review Bundle

## Purpose

Prepare a compact, secret-safe markdown bundle that can be pasted into ChatGPT Pro for slow, high-depth review before Codex implements, deploys, publishes, or commits to a risky plan.

This skill is for review and decision quality, not for routine execution. Use it before high-impact implementation, deployment, architecture, consulting, or research decisions where a missed edge case would be expensive.

## Risk Tiers

Tier 0 - no Pro review:

- tiny local edits
- simple copywriting
- single-file non-production bugfixes
- changes fully reversible in local git

Tier 1 - optional Pro review:

- nuanced writing
- discovery synthesis
- non-production architecture notes
- proposal drafts with confidential details removed

Tier 2 - recommended Pro review:

- multi-module refactors
- client-facing commercial plans
- architecture choices with future migration cost
- external integration design
- changes that affect multiple tools, teams, repos, or workflows

Tier 3 - mandatory Pro review before implementation:

- production deploy, routing, DNS, SSL, nginx, certbot, cron, or scheduler changes
- auth, payments, webhooks, billing, credentials, permissions, or access control
- database schema, migration, import, delete, restore, or irreversible cleanup
- external writes to email, CRM, project trackers, GitHub, CMS, cloud services, or public sites
- legal/contract-like language, financial commitments, or client-facing scope commitments

## Privacy Gate

Before building a bundle, classify the intended content:

- `PUBLIC`: safe to paste
- `INTERNAL`: paste only if needed
- `CLIENT-CONFIDENTIAL`: summarize or redact by default
- `PII`: do not paste raw; summarize or redact
- `SECRET`: never paste raw
- `PRODUCTION-SENSITIVE`: include only minimal evidence and no credentials

If any content is `CLIENT-CONFIDENTIAL`, `PII`, `SECRET`, or `PRODUCTION-SENSITIVE`, the task file must explicitly state how it was summarized or redacted.

## Default Workflow

1. Build the local plan first: goal, current state, proposed change, stop-lines, risks, and concrete questions.
2. Classify the data with the privacy gate.
3. Select context by allowlist. Include only files that are needed for the review.
4. Run the bundled script to assemble a markdown bundle:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/pro-review-bundle/scripts/build_bundle.py" \
  --root /path/to/project \
  --title "Short review title" \
  --task-file /path/to/task.md \
  --include AGENTS.md \
  --include README.md \
  --include "docs/**/*.md" \
  --output /path/to/pro-review-bundle.md
```

5. Inspect the bundle before sending it anywhere:

```bash
sed -n '1,220p' /path/to/pro-review-bundle.md
```

6. Give the bundle to ChatGPT Pro only when the bundle manifest says `COMPLETE`. Browser automation should be a separately approved step, especially if authenticated tools or production-capable browser sessions are involved.
7. Bring Pro's answer back into Codex and create a decision log before any implementation.

## Safety Rules

- Use allowlists only. Never dump an entire repository by default.
- Never include raw secrets, tokens, private keys, `.env` files, production dumps, browser profiles, SQLite state, auth state, or full logs with credentials.
- Do not include raw client transcripts, PII, or confidential client details unless they have been summarized or redacted.
- Keep production/server/auth/data work read-only in the bundle unless there is already a bounded approval for mutation.
- If the selected context seems too broad, pause and narrow it.
- Treat skipped files, unmatched includes, possible PII, or redactions as an incomplete bundle until the human accepts the incompleteness.
- If browser automation is requested later, apply an isolation check first.

The script denies common sensitive paths, blocks files outside `--root` by default, scans included files for secret-like strings, and exits non-zero when warnings/skips are present unless `--allow-warnings` is explicit. Treat a warning as a stop sign until reviewed.

## What To Include

Prefer a small packet:

- the user's intent in plain language
- exact current state and source of truth
- proposed plan
- explicit stop-lines and no-touch zones
- risks and assumptions
- 3-7 questions for GPT Pro
- the smallest relevant code/docs/config snippets
- links or identifiers for external artifacts, without raw secrets

Recommended review shape:

```markdown
what we know -> proposed plan -> boundaries -> risks -> questions for Pro -> next safe step
```

## Good Uses

- Production-adjacent route, sync, deploy, or UI contract plans.
- Access, payments, billing, webhook, and permission plans where boundaries matter.
- Data ingestion, automation, or source-policy changes.
- Cloud/VPS cleanup or incident-prevention plans.
- Client discovery packets and commercial proposals after sensitive details are removed.
- Complex codebase refactors across several modules.

## Bad Uses

- Tiny bugfixes.
- Straightforward local edits.
- Simple copywriting.
- Anything where the bundle would contain secrets or private data that cannot be safely summarized.

## Post-Pro Decision Log

After Pro returns, do not treat its answer as approval. Create a short decision log:

```markdown
# Pro Review Decision Log

## Original Verdict From Pro

## Accepted Findings

## Rejected Findings And Why

## Plan Changes

## Remaining Blockers

## Final Implementation Scope

## No-Touch Zones

## Next Safe Step
```

Rules:

- `stop` blocks implementation.
- `revise` requires a revised plan and a diff against the original plan.
- `go` still requires local preflight and human approval for high-risk actions.
- Missing evidence blocks implementation until evidence is collected or the human explicitly accepts the gap.
- Pro may suggest broader scope, but that is not approval to expand scope.

## Review Prompt Skeleton

If no task file exists yet, create one using this shape:

```markdown
# GPT Pro Review Request

## Goal

## Current State

## Proposed Plan

## Stop-Lines / No-Touch Zones

## Risks And Assumptions

## Privacy Classification

## Questions For GPT Pro

1. What hidden flaw or missing edge case would make this plan fail?
2. Which assumption is weakest?
3. What should be simplified before implementation?
4. What should remain explicitly out of scope?
5. What evidence would you require before proceeding?

## Desired Output

Return a concise review with: verdict, top failure modes, weakest assumption, missing evidence, recommended changes, out-of-scope items, safer alternative, and pre-flight checklist.
```
