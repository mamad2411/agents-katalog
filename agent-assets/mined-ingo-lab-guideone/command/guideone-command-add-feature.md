---
description: Add a feature to an existing Atelier project — design, implement, test, and verify.
argument-hint: [feature description]
allowed-tools: Read, Write, Edit, Bash, Agent, TodoWrite
---

Add a new feature to the current project.

Feature request: $ARGUMENTS

## Your plan

1. Call **progress-keeper** first to load current state (PRD, features.json, DECISIONS.md).
2. Invoke **orchestrator** with the "Add a feature" workflow:
   - `solution-architect` writes a short design note for the feature
   - Relevant build specialist(s) implement — parallel if independent
   - `test-engineer` adds coverage
   - `code-reviewer` + `security-auditor` (if the feature touches auth or data) run in parallel
   - `qa-verifier` verifies against acceptance criteria
   - `progress-keeper` flips `passing: true` only after qa-verifier confirms
3. Report back with: feature ID added, files changed, tests added, verification status.
