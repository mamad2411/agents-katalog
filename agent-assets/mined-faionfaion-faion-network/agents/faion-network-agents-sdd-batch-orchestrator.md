# SDD Batch Orchestrator

## Summary

A reusable pattern for delivering a batch of related tracker tickets end-to-end inside one Claude Code session: study → clarify → plan → wave-execute → verify → review → fix → visual-deliver → close. The orchestrator agent never re-types long instructions; it hands each subagent a **path to a versioned prompt file** plus a small parameter block. Per-phase prompts, per-domain playbooks, and shared reference docs live as files, so behaviour is reproducible across runs.

## Why

Multi-ticket batches drift when the orchestrator improvises long prompts each time: instructions evolve, drift becomes invisible, and parallelism collapses to "one ticket at a time, manually narrated." Versioned prompt files turn each phase into a deterministic capability the orchestrator composes; isolated git worktrees turn unrelated tickets into safe parallel waves; a final visual-delivery phase produces evidence the human reviewer can scan in seconds.

## When To Use

- A batch (≥3) of related tickets that share a delivery surface (templates, UI, rules, ETL).
- Bug-fix or small-feature work that benefits from spec/design/test-plan artifacts before code.
- Visual changes where before/after screenshots are the expected proof of done.
- Multi-repo or multi-file batches where parallel waves shorten wall-clock time.

## When NOT To Use

- Single one-off ticket — the planning/wave overhead is not worth it.
- Pure exploratory research — there is nothing to merge or visually verify.
- Cross-cutting refactor where every ticket touches the same lines — wave parallelism gives nothing; do it sequentially.
- Anything where the user has not authorized writes (this orchestrator commits, merges, and optionally deploys).

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Core principle, role split, language convention |
| `content/02-phases.xml` | The 12 phases and which prompt file fronts each |
| `content/03-prompt-files.xml` | How a subagent prompt file is structured |
| `content/04-parallelism.xml` | Wave rules, worktree pattern, conflict handling |
| `content/05-defaults-constraints.xml` | No-push / no-verify / no-destructive defaults |
| `content/06-clarification-batching.xml` | Aggregating open questions into one ask |
| `content/07-verify-review-fix-loop.xml` | Iterative quality gate with hard cap |
| `content/08-recapture-and-deliver.xml` | Focused before/after screenshots + out-of-band delivery |
| `content/09-anti-patterns.xml` | What to avoid and why |
| `content/10-playbook-adaptation.xml` | How to specialize the pattern per delivery surface |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-skeleton.md` | Skeleton for any subagent prompt file under `prompts/` |
| `templates/playbook-skeleton.md` | Skeleton for a domain-specific playbook under `playbooks/` |
| `templates/orchestrator-dispatch.txt` | Format of the spawn message the orchestrator sends to a subagent |
| `templates/focused-screenshot.py` | Element-focused Playwright capture with CSS outline injection |
