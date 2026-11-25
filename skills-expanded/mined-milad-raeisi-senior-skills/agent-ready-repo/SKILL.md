---
name: agent-ready-repo
description: Make a codebase easy and safe for AI coding agents (agent experience, AX) as well as for humans. Use when creating or improving AGENTS.md or CLAUDE.md, onboarding a repository to Claude Code, Codex, Cursor, Gemini CLI, or Copilot, when agents keep making the same mistakes in a repo, when the feedback loop (build, test, lint) is slow or unclear, or when the user asks to improve developer or agent experience. Produces one-command feedback loops, a concise agent guide, explicit conventions, and guardrails against destructive actions.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Agent-Ready Repo

Agents are new team members who join every session with no memory. Whatever a new hire would have to ask about, an agent will either guess or rediscover, both slowly. A repo that's ready for agents is one where the answers are written down, the feedback loop is a single fast command, and mistakes are caught automatically. Every improvement here helps human developers just as much.

## Step 1: Watch where agents struggle

Before writing anything, gather evidence. Look at recent agent sessions, PR review comments, or try a small representative task yourself. Typical friction:

- Not knowing how to run tests, or running the whole slow suite for a one-line change.
- Using the wrong package manager, Node or Python version, or formatter.
- Editing generated files, vendored code, or lockfiles by hand.
- Following an outdated pattern that still exists in old code.
- Breaking a convention that lives only in people's heads.

Fix the friction you observed, not a generic checklist.

## Step 2: One-command feedback loops

The biggest single AX win is that `test`, `lint`, `typecheck`, `build`, and `format` each work with one obvious command, are fast, and give clear output.

- Expose them through the project's standard entry point (`package.json` scripts, `Makefile`, `justfile`, `tox`/`nox`, `cargo` aliases).
- Support targeted runs: a single file or test name (`npm test -- path/to/file`, `pytest path::test_name`, `go test ./pkg/... -run Name`).
- Make tests deterministic and hermetic: no real network, no shared state, seeded randomness.
- Error messages should say how to fix the problem, not just what failed.

## Step 3: Write a short AGENTS.md

`AGENTS.md` is the cross-tool convention for agent instructions (Codex, Cursor, Copilot, and others read it). Claude Code reads `CLAUDE.md`, and Gemini CLI reads `GEMINI.md` by default (its `context.fileName` setting can point it at `AGENTS.md`). Keep one source of truth and point the others at it, for example a `CLAUDE.md` that contains `@AGENTS.md`.

Keep it **short and specific**, under about 150 lines. Agents load it on every session, so every line costs attention. Include only what an agent can't infer quickly from the code:

- What the project is, in two sentences.
- Exact commands for setup, test (including a single test), lint, typecheck, build, and run.
- Repository map: where things live, and which directories are generated or vendored.
- Conventions that differ from the ecosystem default.
- Gotchas: the traps that have actually bitten people.
- Hard rules: what never to do (edit migrations after release, commit secrets, touch `vendor/`).

A template is in [references/agents-md-template.md](references/agents-md-template.md). Nested `AGENTS.md` files in subdirectories can hold area-specific rules for large monorepos.

## Step 4: Make the code self-explaining

- Explicit types and states instead of booleans and magic strings (see `state-machine-hunter`).
- Greppable, domain-consistent names: one name per concept across code, docs, and UI.
- One obvious place for each kind of thing (routes, migrations, feature flags).
- Short README files in complex modules explaining *why*, plus ADRs for significant decisions.
- Delete or clearly mark deprecated patterns so agents don't copy them.

## Step 5: Guardrails

- Pre-commit hooks or CI checks for formatting, lint, types, and tests, so mistakes are caught mechanically rather than in review.
- Protected branches and required checks.
- Agent harness settings: allow safe read-only and test commands, require confirmation for destructive ones (`rm -rf`, `git push --force`, database drops, deploys).
- Secrets out of the repo and out of agent-readable logs.

## Step 6: Verify

Give a fresh agent session a small, representative task using only the repo's documentation. Note where it hesitated, guessed, or went wrong, and fix the docs or tooling there. Repeat until a cold start is smooth.
