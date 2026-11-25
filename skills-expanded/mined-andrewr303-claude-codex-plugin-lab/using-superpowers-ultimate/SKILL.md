---
name: using-superpowers-ultimate
description: Entry router for non-trivial coding, design, engineering, debugging, review, planning, frontend, performance, dependency, plugin/skill, or ML experiment tasks in Codex.
---

# Using Superpowers Ultimate

Use this skill as the first explicit workflow choice for non-trivial technical work. It routes the request, sizes rigor by risk, and picks the smallest skill sequence that can prove the outcome.

## Codex First

- Use Codex-native tools and current thread instructions.
- Use `update_plan` for visible task tracking when work has multiple steps.
- Use `apply_patch` for manual edits.
- Use `multi_tool_use.parallel` for independent reads and searches.
- Use shell commands for focused verification.
- Use web only when facts are current, unstable, or source documentation is required.

## Entry Sequence

1. Restate the literal ask in one sentence.
2. Name the decision or action the user likely needs to unblock.
3. Check repo instructions before edits: `AGENTS.md`, `CLAUDE.md`, README, package manifests, docs maps, and nearby tests as relevant.
4. Classify the task:
   - `micro`: one obvious reversible edit or answer.
   - `lightweight`: small scope, no new architecture, no cross-module contract risk, no data/auth/money/production boundary.
   - `full`: anything else, plus all UI, auth, data, ML, performance, dependency, workflow, plugin, release, or multi-file design work.
5. Route to skills:
   - unclear premise: `premise-and-scope`
   - fuzzy product/feature: `design-brief`
   - implementation plan: `implementation-planning`
   - plan execution: `execution-engine`
   - completion claim: `verification-gates`
   - bug or failing test: `systematic-debugging` then `test-driven-development`
   - review/audit: `code-review-red-team`
   - UI/frontend: `frontend-design-engineering`
   - performance or dependency work: `performance-dependency`
   - ML/data experiments: `ml-experiment-engineering`
   - independent parallel work: `parallel-agent-orchestration`
   - context memory: `context-continuity`
   - finish/handoff: `delivery-handoff`
   - skills/plugins/instructions: `skill-and-agent-authoring`

## Risk Scaling

- Put depth where being wrong is quiet, costly, or late detected.
- Move quickly on reversible local edits.
- Stop for approval before destructive, outward-facing, production, auth, billing, legal, financial, or data-loss actions.
- Label load-bearing claims as `verified`, `inferred`, or `assumed`.

## Completion Rule

Do not claim done until one check that could have failed has run, or the final handoff explicitly lists why verification was not run.

