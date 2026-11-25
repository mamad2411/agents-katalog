# Skill: onboarding-docs

Generates developer onboarding documentation for a module or feature area.

## When to Use
- When a new developer joins and needs context on a subsystem
- After a major refactor that makes existing docs stale
- When preparing handoff documentation for a feature

## Steps

1. **Read the module structure**
   - Entry points (routes, tasks, CLI commands)
   - Key service functions and their purpose
   - Models and their relationships
   - External dependencies (third-party APIs, queues, external DBs)

2. **Trace a key flow end-to-end**
   - Pick the most important or complex workflow
   - Document the call chain: request → handler → service → repo → DB → response

3. **Identify gotchas**
   - Non-obvious constraints or invariants
   - Known technical debt with a ticket reference
   - Anything that has caused bugs before

4. **Generate the doc** using `docs-outline.md` as the template

## Output
A filled-out developer guide for the target module, saved to `docs/<module>.md`.
