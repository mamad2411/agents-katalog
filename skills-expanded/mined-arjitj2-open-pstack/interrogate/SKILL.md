---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
---

# Interrogate

Spawn one reviewer per configured model to adversarially review code changes. The adversarial signal comes from model diversity, not assigned personas. The deliverable is a synthesized verdict. Do NOT auto-apply changes.

**Dispatch contract.** Read [`provider-dispatch.md`](../poteto-mode/references/provider-dispatch.md) before launching reviewers. Configured entries are provider-qualified descriptors; the parent starts native and external read-only lanes directly. On Codex, resolve remaining Claude tool names via [`codex-tools.md`](../poteto-mode/references/codex-tools.md).

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents with any surrounding context files the reviewers need to understand the code.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit messages, the PR description if one exists, and the code. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Start all reviewers in one fan-out phase. Use `interrogate reviewers` from the current harness's pstack model sheet when present, one reviewer per entry, extending or shrinking the Reviewer A/B/C labels below to the configured entry count. If the sheet or that line is missing, use the table defaults. Native reviewers use the parent subagent primitive. External reviewers use the launcher directly and must return a complete, model-verified receipt.

| Subagent | Default model |
|----------|---------------|
| Reviewer A | `codex:gpt-5.6-sol@max` |
| Reviewer B | `grok:grok-4.7@xhigh` |
| Reviewer C | `claude:opus@max` |

For each reviewer, route the configured descriptor with `read-only` access and a unique output/receipt path. If the descriptor is `inherit-parent` or `auto`, use the parent subagent primitive without a model override. Each reviewer seat runs its saved attempt chain from the model sheet: a terminal outcome the sheet's `# fallback` policy authorizes advances to the next saved attempt per provider-dispatch's fallback state machine (`usage-exhausted` only when no policy is saved); every other failure records a dropout and continues with the completed reviewers. Label each finding by the provider and model that actually ran, and say when fallbacks collapse provider diversity — two reviewers on one provider are not cross-provider agreement. Never pick the closest model or fall back outside the saved chain.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with the stated intent, the diff or file contents, the rubric from `references/rubric.md`, and the code-quality lens from `references/code-quality-review.md`.

## Step 4, Synthesize

As results come back, build a unified picture. Retain native terminal results and external task/session handles and verified receipts. Wait for every configured seat to reach a verified terminal result or recorded dropout before the final lead verdict; process startup, progress, and self-reported completion do not count. Parse every reviewer's full findings. Merge findings that describe the same issue differently, and note which models raised each one. Findings two or more models raised independently are the highest signal. Read a lone model's finding, but weight it accordingly. Note disagreements. If one model flags something and another explicitly says the opposite, that is context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read `references/lead-judgment.md` for the full framework. Rerun each supplied repro command inside a disposable copy of the checkout, never in the working tree, and never against live services, credentials, or the network. Rank a rerun-confirmed finding first in its bucket and label it `run-proven`. Keep a source- or policy-cited finding that was not run, labeled `not run`. Put every finding in one of four buckets, with the model(s) that raised it and a one-line rationale.

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. They would block a real PR.
- **Consider**. Legitimate, but you're not sure they outweigh the cost of addressing them now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, or missing context, with a brief reason.

## Output Format

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)

### Act On
[Each: description, which models raised it, why it matters.]

### Consider
[Each: description, which models raised it, the tradeoff.]

### Noted
[Brief list.]

### Dismissed
[Each with a brief rationale.]

### Agreement Map
[Where models agreed and diverged, and what that pattern tells us.]
