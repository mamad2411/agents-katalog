---
name: project-discovery
description: Explore and summarize an unfamiliar or existing project before planning, editing, onboarding, architecture review, migration, stack choice, or implementation. Use when the user asks to understand a repo, inspect architecture, map a codebase, discover project conventions, or prepare a project overview.
---

# Project Discovery

Build a practical understanding of a project before proposing or making changes.

## Workflow

1. Identify the goal
   - Determine whether the user needs an overview, architecture summary, stack analysis, risk assessment, implementation plan, migration direction, or onboarding notes.

2. Inspect high-signal files
   - Read `README.md`, project instructions, package manifests, lockfiles, docs, architecture notes, CI config, test config, and main entry points.
   - Prefer actual files over guesses — the [research-methodology](../research-methodology/SKILL.md) source-tier idea applies here too: a file in the repo outranks a README's description of what the repo does, which outranks an outside blog post about the project.

3. Map the system
   - Identify core modules, data flow, user-facing surfaces, external services, build commands, test commands, deployment hints, and local conventions.
   - Note areas that need follow-up inspection instead of pretending certainty.

4. Assess readiness
   - Call out missing docs, unclear ownership, brittle tests, risky dependencies, weak validation, or hidden configuration.
   - Keep recommendations incremental.

5. Report
   - Respond in the user's language.
   - Link to files when possible.
   - End with a practical next step.

## Output Format

```markdown
# Project Discovery

## What This Project Does

## Stack

## Important Files

## Architecture Notes

## Development Workflow

## Risks And Unknowns

## Recommended Next Steps
```

## Rules

- Do not propose broad rewrites before understanding local patterns.
- Distinguish verified facts from assumptions.
- Keep the report useful for the next action, not encyclopedic.
