---
name: kos-trigger-policy-trust-gate
description: Understand the authorize-job trust gate (evaluate-trigger-policy.cjs + policy.json) that decides whether a comment/issue-triggered zai workflow actually runs, and why most such runs show conclusion=skipped.
user-invocable: true
when_to_use: "When a comment/issue/PR-triggered workflow that gates via evaluate-trigger-policy.cjs skipped, or you need to know if a trigger will be trusted."
category: utilities
argument-hint: "[workflow and trigger event]"
keywords: [trigger, policy, trust, authorize, gate, skipped, allowed-bots, non-human, author-association]
related: [kos-zai-run-failure-prevention, kos-gh-automation-tooling]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from evaluate-trigger-policy.cjs + policy.json + skipped-run analysis
  license: repo
  version: "1.1"
---

# Idea

Many comment/issue/PR-triggered workflows gate via `evaluate-trigger-policy.cjs --mode <workflow> --policy-file .github/workflows/policy.json`, which emits `triggered` and `trusted`; the run proceeds only when **both** are `true`, else the downstream job is `skipped`. The current set includes `claude`, `fix-issue`, `fix-review`, `rebase-pr`, `antigravity`(+`-code-review`), `deepseek`, `fix-pr`/`fix-branch`, `approve-auto-fix`, `review-approved`, `planning-intake-repair`, and `pr-flow` — run `grep -l evaluate-trigger-policy.cjs .github/workflows/*.yml` for the authoritative list (it changes as workflows are added). (`gsd-planning` and `triage` have their **own** simpler `authorize` jobs — slash-command presence + `author_association` — and do **not** call it.) Most runs of these workflows are `skipped` — that is the gate working, not a failure.

## When to invoke this skill directly

- A `claude`/`fix-issue`/`fix-review`/`rebase-pr` run showed `skipped` and you need to explain why / whether it should have run.
- You are deciding whether to re-trigger, and from which actor, to be trusted.
- You are editing `policy.json` trust rules or a workflow's `authorize` condition.

## References

- `.github/workflows/scripts/evaluate-trigger-policy.cjs` — the gate logic (`--mode`, `--event-path`, `--event-name`).
- `.github/workflows/policy.json` — `maintainerAssociations` (OWNER/MEMBER/COLLABORATOR), `trustedAutomationBranchPrefixes`, `trustedPlanning`, per-mode rules. **Trust is `author_association`-based; there is no bot allowlist in `policy.json`.**
- Each gated workflow's `authorize` job `if:` + the downstream `needs.authorize.outputs.triggered == 'true' && ... trusted == 'true'`.
- **Trigger signal is per-mode, not a single token:** the `claude` mode keys on the literal `@claude` mention (comment/review/issue title-or-body); `fix-review`/`fix-issue` key on their slash command (`/address-review`, `/fix`); `rebase-pr` keys on `/rebase`. Only `claude` uses `@claude`.

## Communication Style

One sentence on whether the event would be triggered+trusted, then the single condition that flips it. Do not paste the whole policy.

## Core Principles

YAGNI / KISS / DRY. The gate is authoritative — do not work around it; satisfy it. `skipped` is a feature (it saves a run), not a bug to "fix."

## How the gate decides (operator view)

1. **Triggered?** — Did the event contain the mode's required signal? `@claude` for the `claude` mode; the matching slash command for the others (`/address-review`/`/fix`, `/rebase`).
2. **Trusted?** — Is the actor's `author_association` in `policy.json` `maintainerAssociations` (OWNER/MEMBER/COLLABORATOR)? Untrusted actor → not trusted. (Trust is author-association-based — there is no bot allowlist at this layer.)
3. **Both true** → downstream job runs. **Either false** → downstream `skipped` (conclusion `skipped`, not `failure`).

`non_human_actor` (a *run* failure, distinct from *skip*) happens when the gate passed but the `run-zai` runtime then refused the bot because it wasn't in `run-zai: allowed-bots`. That `allowed-bots` list is **runtime-only** (the `run-zai` action input) — it is separate from the `author_association`-based gate trust.

## Your Approach

1. Identify the event type and the actor (+ `author_association`).
2. Check the mode's signal (`@claude` for claude; the slash command otherwise) → `triggered`.
3. Check the actor's `author_association` against `policy.json` `maintainerAssociations` → `trusted`.
4. If a bot dispatched it, confirm it is in `run-zai: allowed-bots` (runtime), else it fails as `non_human_actor` after the gate passes.

## Process Flow (Authoritative)

1. Read the event (comment body / issue title+body / review body).
2. Resolve `triggered` per the mode's signal rule (`@claude` or the slash command).
3. Resolve `trusted` per `author_association` ∈ `maintainerAssociations`.
4. Report `triggered + trusted → RUN` or which of the two is false and the one-line fix (add the signal, or re-trigger as a trusted actor, or extend `maintainerAssociations`).

## Output Format

```text
EVENT=<type> ACTOR=<login>(<assoc>)  TRIGGERED=<yes/no:reason>  TRUSTED=<yes/no:reason>  => RUN|SKIP
```

## Critical Constraints

- Never recommend disabling the gate to force a run; extend `maintainerAssociations` deliberately instead.
- `skipped` ≠ failure; do not file a failure issue for a skipped run.
- Trust is `author_association`-based (no bot allowlist in `policy.json`); a bot the gate passes but `run-zai: allowed-bots` rejects fails as `non_human_actor` — a real (fixable) runtime failure.
