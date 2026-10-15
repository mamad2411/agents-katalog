---
name: project-x-ray
description: >
  Deep-scan a project's structure, dependencies, architecture, conventions, and domain,
  then write the findings into a structured PROJECT_ANALYSIS.md file that any human or agent
  can use for fast orientation. Use when the user says "analyze this project", "x-ray the codebase",
  "write a project overview", "onboard me", "what does this project do", "map this repo",
  or when a new agent session needs to understand an unfamiliar codebase before doing real work.
---

# Project X-Ray

Scan a codebase once and write `PROJECT_ANALYSIS.md`: a durable orientation file that tells a human or agent what the project does, how it is built, where the important pieces live, and which conventions matter.

The goal is context reuse. A good x-ray saves future sessions from rediscovering directory layout, framework versions, entry points, test runners, and naming conventions.

## Operating rules

- **Reuse fresh analysis.** If `PROJECT_ANALYSIS.md` exists, is less than 7 days old, and no major structural changes are obvious, load it and ask whether the user wants a refresh instead of rescanning.
- **Read selectively.** Prefer `rg --files` or `git ls-files` for file discovery. Read manifests, configs, entry points, routers, schemas, dependency-injection setup, representative tests, and representative source files. Do not read every file.
- **Respect ignore boundaries.** Skip generated, vendored, and ignored content: `.git`, `node_modules`, `dist`, `build`, `.next`, `target`, `vendor`, `__pycache__`, coverage outputs, lockfile caches, and other project-specific generated directories.
- **Keep the artifact bounded.** Keep `PROJECT_ANALYSIS.md` under about 2,000 lines. Expand key directories to 2-3 levels, summarize dense leaf directories, and use one-line summaries for obvious boilerplate.
- **Report, do not review.** Describe what exists. Do not rate quality, propose refactors, or prescribe architecture changes.
- **Avoid secrets.** Note that `.env`, secret stores, vault configs, or credential directories exist, but never read or reproduce their contents.
- **Create exactly one file.** Write or overwrite `PROJECT_ANALYSIS.md` in the repository root unless the user specifies another path.

## Scan workflow

Run the phases in order. Earlier phases provide evidence for later ones.

### 1. Structure

Map the project shape:

- Annotate every root-level file and directory with a one-line purpose.
- Expand important directories such as `src`, `app`, `lib`, `packages`, `cmd`, `internal`, `services`, and `tests` to 2-3 levels.
- Identify entry points such as `main.go`, `index.ts`, `app.py`, `Program.cs`, `Main.java`, `Cargo.toml [[bin]]`, `package.json#main`, CLI definitions, server bootstrap files, workers, and scheduled jobs.
- Detect monorepos via `workspaces`, `pnpm-workspace.yaml`, `Cargo.toml [workspace]`, `go.work`, `lerna.json`, `nx.json`, or similar signals. List packages/apps with one-line responsibilities.

### 2. Dependencies and toolchain

Read **[references/ecosystems.md](references/ecosystems.md)** when doing this phase. It lists ecosystem signal files, what to extract, and how to group dependencies.

Summarize:

- Runtime and language versions.
- Frameworks and key dependencies grouped by role: framework, data, HTTP/API, auth, test, dev tooling, infra/deploy.
- Build tools, test runners, linters, formatters, package managers, and lockfiles.
- Version constraints that future agents must know before choosing APIs.

### 3. Architecture

Infer architecture from structure, imports, framework conventions, and representative code:

- Classify the dominant pattern only when evidence supports it: MVC, layered, hexagonal/ports-and-adapters, microservices, CLI, library/SDK, monolith, serverless functions, plugin system, pipeline/ETL, or mixed.
- If the pattern is mixed or unclear, say so and cite both sides. A useful hybrid description beats a clean but false label.
- List major modules/packages/namespaces with a single-sentence responsibility.
- Trace request, command, event, job, or library-call flow from entry point to side effects. Cover each major entry point separately when the project has more than one.
- Note enforced boundaries such as separate packages, interface layers, dependency injection, API versioning, schema contracts, or generated clients. Also note absent or porous boundaries when visible.
- Include a mermaid diagram only when it adds structure beyond the module list. For large systems, diagram top-level package relationships only.

### 4. Conventions and tooling

Extract conventions from config and samples:

- Code style: indentation, naming, file naming, module organization, and test layout.
- Commit/PR conventions from config and templates only; do not scan git history or branches.
- CI/CD from `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`, `bitbucket-pipelines.yml`, `azure-pipelines.yml`, and similar files. Summarize jobs without dumping YAML.
- Documentation: README, CONTRIBUTING, CHANGELOG, ADRs, API docs, OpenAPI/Swagger specs, architecture docs.
- Agent instructions: `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `GEMINI.md`, and similar files. Note each one with a one-line summary.

### 5. Domain

Write a 2-4 paragraph plain-language overview grounded in evidence from README content, route definitions, exported APIs, CLI help, tests, docs, and domain model names.

Answer:

- What problem does this project solve, and for whom?
- What are the core domain concepts or entities?
- What are the primary user-facing features, APIs, commands, or library surfaces?
- How is the project deployed or consumed?

Put genuine unknowns in Open Questions instead of guessing.

### 6. Consumption

End the analysis with guidance for reuse:

- Agents should load `PROJECT_ANALYSIS.md` at session start and skip full rescans while it is fresh.
- Humans should read Overview and Architecture first, then use the rest as reference.
- Staleness is based on the `Generated by` date plus major structural, dependency, or architecture changes.

## Output format

Write the analysis to `PROJECT_ANALYSIS.md` in the repository root (or another path if the user specifies one). Use this structure:

```markdown
# Project Analysis: {project name}

> Generated by project-x-ray · {YYYY-MM-DD}

## Overview

{Phase 5 domain summary — 2-4 paragraphs}

## Directory Structure

{Phase 1 annotated tree + entry points}

## Tech Stack & Dependencies

{Phase 2 ecosystem, versions, grouped deps, build/test/lint tooling}

## Architecture

{Phase 3 pattern, module map, data flow, optional diagram}

## Conventions & Tooling

{Phase 4 code style, commits, CI/CD, docs, agent files}

## Using This Analysis

{Phase 6 consumption guidance}

## Open Questions

{Things the scan couldn't determine — missing docs, ambiguous patterns,
 decisions that need a human to clarify}
```

When rescanning, overwrite `PROJECT_ANALYSIS.md`; it is a point-in-time snapshot, not a log. Tell the user what you wrote and where.

## Skill pairing

X-Ray output composes well with other skills:

- **context-canary** — load `PROJECT_ANALYSIS.md` as session context; canary monitors whether the agent's grip on that context degrades.
- **junior-to-senior** — feed the analysis into a plan review so the senior reviewer has codebase grounding without re-scanning.
- **loop-factory** — use the architecture and convention sections to write better task specs.

## Final checks

- Ensure every non-obvious claim is grounded in a file, config, route, export, test, or doc.
- Move unresolved facts to Open Questions.
- Confirm the output contains the six required sections in order.
- Confirm no secret values, generated file dumps, or source-code rewrites were included.
