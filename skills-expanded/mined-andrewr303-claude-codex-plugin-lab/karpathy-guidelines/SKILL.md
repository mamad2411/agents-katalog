---
name: karpathy-guidelines
description: Behavioral coding-agent guardrails adapted from the Karpathy-inspired Claude/Cursor skill archive. Use when writing, reviewing, refactoring, debugging, or planning code changes where Codex should surface assumptions, avoid overengineering, keep diffs surgical, preserve unrelated user work, and define verifiable success criteria before declaring the task done.
---

# Karpathy Guidelines

Use this skill as a lightweight behavioral overlay for coding work. It does not replace project instructions, PRDs, schemas, security rules, or local harness docs. In HypeStake, repo-specific AGENTS/CLAUDE/wiki guidance always wins when there is a conflict.

## Operating Loop

1. Name the target in implementation terms.
2. State assumptions that affect scope, data access, permissions, or user-visible behavior.
3. If the request has materially different interpretations, surface the tradeoff before editing. Ask only when a reasonable assumption would be risky, destructive, or product-defining.
4. Choose the smallest source-backed change that solves the target.
5. Define success criteria and verification before calling the task done.

## Four Guardrails

### 1. Think Before Coding

- Do not silently choose between plausible meanings when the difference matters.
- Make uncertainty visible early.
- Push back when the user's requested path is broader, riskier, or more complex than needed.
- Read the relevant source files before inventing behavior.

### 2. Simplicity First

- Do not add features, switches, abstractions, or configuration that the task did not require.
- Prefer existing local helpers and patterns.
- Avoid one-use abstractions unless they remove real complexity.
- If a solution feels large for the ask, pause and simplify.

### 3. Surgical Changes

- Touch only files and lines needed for the requested behavior.
- Match the surrounding style even when another style would be personally preferred.
- Clean up imports, variables, tests, and comments made obsolete by your own changes.
- Mention unrelated dead code or drift separately instead of deleting it.
- Preserve user changes in a dirty worktree.

### 4. Goal-Driven Execution

- Convert vague requests into observable outcomes.
- For bug fixes, prefer a reproduction or focused test before the fix when feasible.
- For refactors, verify behavior before and after when practical.
- Run the strongest relevant checks available and report skipped or unrelated failures.

## HypeStake Adaptation

- Do not let "simple" mean under-specified for finance, equity, valuation, AI provenance, auth, RLS, or contracts.
- Before implementation, read the relevant HypeStake PRD/wiki/schema/service/component when available.
- Favor compatibility adapters over breaking payload, route, table, or prompt contracts.
- Keep AI, valuation, deal, and portfolio outputs inspectable, caveated, and evidence-grounded.
- For UI work, verify desktop and mobile parity before declaring completion.

## Quick Checklist

- What assumptions did I make, and are they safe?
- Is there a smaller change that satisfies the same target?
- Does every changed line trace to the request?
- Did I preserve unrelated user work?
- What command, test, build, screenshot, or runtime check proves this is done?

## Reference

Read `references/examples.md` when the user asks for examples, wants to evaluate agent behavior, or wants to turn these guidelines into review criteria.
