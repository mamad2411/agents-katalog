---
name: summarize-repo
description: Produce an evidence-based codebase map covering architecture, entry points, dependencies, and risks.
category: development
aliases:
- summarize
- repo-overview
- codebase-summary
- on boarding
triggers:
- Summarize this repo
- What is this project
- Give me an overview
- Onboard me to this codebase
keywords:
- summarize
- repo
- codebase
- overview
- tour
- onboarding
- readme
- architecture
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- summarize-repo
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- codebase
- development
- overview
- repo
- summarize
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Summarize Repo

## Purpose
Read a repository and produce a **single, scannable summary** that answers: *what is
this, what stack, where is the entry point, where is the work done, and how do I
run it*. The output is shaped to onboard a new contributor in five minutes.

## When to Use
- The user is new to a repo
- A user is switching to a new project
- The agent needs context before making changes

## When NOT to Use
- The repo is a private, sensitive codebase (redact before producing the summary)
- The summary would exceed the user's context budget (decompose)

## Capabilities
- Read `README.md`, `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`, `LICENSE`
- Detect the language and framework from manifest + file extensions
- Map the top-level directory layout with one-line per-dir descriptions
- Identify the entry point, the test runner, the build command, the dev command
- Surface the most-changed files in the last 90 days as a proxy for "hot spots"
- Detect CI providers (`.github/workflows`, `.circleci`, etc.) and required checks
- Produce a 1-paragraph, 1-list, 1-faq triplet — never a wall of text

## Inputs
- A repo path (or remote URL that is shallow-cloned)
- Optional: `--max-depth 2` for top-level summary only
- Optional: `--format md|json` (default `md`)

## Workflow
1. **Resolve** the path; shallow-clone if a URL is given.
2. **Read top-level** files (`README*`, `LICENSE*`, manifest, lockfile).
3. **Walk the tree** to depth 2; classify directories by purpose (`src`, `tests`, `docs`, `scripts`).
4. **Find the entry** — `package.json` `main`/`bin`, `pyproject` `scripts`, `src/index.*`, `cmd/`, `bin/`.
5. **Find the test runner** — `*test*` scripts, `__tests__`, `tests/`, `spec/`.
6. **Compute hot files** with `git log --since=90d --name-only --pretty=format:` ranked.
7. **Compose the summary** in three blocks:
   - **What it is** — 2 to 4 sentences.
   - **How to run it** — 3 to 6 commands.
   - **Where to look first** — 5 file paths, annotated.
8. **Print** and offer to drill into any section.

## Tools
- Filesystem
- `git` (for `git log`)
- Optional: `tokei`, `cloc` for size stats

## Examples
**User:** "Summarize this repo."
**Response:**

> **What it is** — `openclaw/clawhub` is a self-hosted skill registry with a
> Convex backend, Next.js frontend, and a curated catalog of agent skills.
>
> **How to run it** — `bun install && bun run dev` (local). `bun run setup:worktree`
> for detached worktrees.
>
> **Where to look first** — `convex/schema.ts`, `src/routes/_index.tsx`,
> `.agents/skills/`, `convex/CLAUDE.md`, `package.json`.

## Safety
- Redact secrets, env files, and private keys before any summary
- Never include raw `package-lock.json` content in the summary
- Honor a `.summarizerignore` file when present

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
