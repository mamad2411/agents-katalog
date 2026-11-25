---
name: codebase-onboarding
description: "Maps an unfamiliar software repository before changes: identifies entry points, architecture, commands, tests, conventions, and risks. Use when starting work in an unfamiliar codebase, taking over a project, or preparing a safe change."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Codebase Onboarding

## Goal
Build an evidence-backed mental model of the repository before editing it. Prefer verified facts over guesses and keep the first pass proportional to the task.

## Workflow
1. **Read local instructions first.** Inspect `AGENTS.md`, `README`, contribution guides, package manifests, and directory-specific instructions that govern the target files. Follow repository guidance unless it conflicts with higher-priority instructions or safety.
2. **Identify the project shape.** Determine the languages, frameworks, package managers, build systems, deploy targets, and major application boundaries from manifests and configuration. Do not infer the production stack from directory names alone.
3. **Find entry points.** Locate executable entry points, routes/controllers, application bootstrap, CLI commands, background jobs, and infrastructure definitions relevant to the requested task.
4. **Trace one representative path.** For the user-visible behavior in scope, follow input → validation → domain logic → persistence or external service → output. Note important interfaces and error paths.
5. **Discover the feedback loop.** Identify exact commands for formatting, linting, type checking, unit/integration tests, build, and local run. Prefer commands specified by the repository. Do not run expensive or destructive commands without assessing their impact.
6. **Map the data and dependencies.** Identify primary data models, migrations, external APIs, authentication/authorization boundaries, and generated code. Note files that should not be edited manually.
7. **Check project state.** Inspect the current diff and working tree before any edit. Preserve unrelated and uncommitted user changes.
8. **Validate selectively.** Run the smallest safe read-only or fast command that confirms the map. If commands fail due to missing dependencies or environment, record the blocker instead of silently treating the command as unavailable.

## Output format
Provide:
- **Project summary:** what it appears to do, with evidence.
- **Architecture map:** key directories and responsibilities.
- **Execution path:** relevant entry points and important files.
- **Developer commands:** exact commands and what each verifies.
- **Risks and unknowns:** assumptions that remain unverified.
- **Recommended next step:** the smallest useful action for the current task.

## Rules
- Cite file paths and symbols; avoid vague statements such as “the backend handles it.”
- Distinguish inspected facts from hypotheses.
- Do not rewrite project documentation just to summarize it.
- Do not install dependencies, modify configuration, or run migrations merely to explore unless requested or necessary and safe.
- Stop exploring once you have enough context to act safely; do not inventory every file without a reason.
