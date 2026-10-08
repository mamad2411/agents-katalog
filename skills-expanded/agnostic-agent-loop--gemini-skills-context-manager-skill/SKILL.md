---
name: context-manager
description: Enforce mandatory context workflow before code changes: read local AGENTS.md files, respect architecture boundaries, and update context docs after structural changes.
---

# skill:context-manager

## Does exactly this

Enforces mandatory context workflow: read local AGENTS.md files before edits, respect architecture boundaries, and update context docs after structural changes.

---

## When to use

Apply this skill when a task includes any of the following:

- Editing files.
- Creating, moving, or deleting source directories.
- Changing dependencies between architectural layers.

## Required Workflow

1. Identify all directories that will be edited.
2. For each directory, check whether `AGENTS.md` exists.
3. If `AGENTS.md` exists, read it before editing.
4. If `AGENTS.md` does not exist and the directory contains source files, create documentation context first.
5. Validate dependency direction against architecture boundaries.
6. Perform edits.
7. If structure, entrypoints, or boundaries changed, update the affected `AGENTS.md` files in the same turn.

## Stop Conditions

Stop and fix context before proceeding if any of these occur:

- Editing starts before reading applicable `AGENTS.md`.
- A new source directory is added without context documentation.
- A dependency violates layer boundaries.
- Architectural changes are made without updating context docs.

### Hexagonal Architecture Boundaries

| Layer | Can Depend On | Cannot Depend On |
|-------|--------------|-------------------|
| Core/Domain | Nothing | Application, Infrastructure, Config |
| Core/Application | Domain only | Infrastructure, Config |
| Infrastructure/Adapters | Domain, Application | Other adapters directly |
| Infrastructure/Config | All layers | — |

## References

- `AGENT_RULES.md`: Unknown - verify (file not found in current repository).
- `CLAUDE.md`: Available in repository root for tool-specific guidance.
- `OPENCODE.md`: Unknown - verify (file not found in current repository).
- `COPILOT.md`: Unknown - verify (file not found in current repository).

## Execution Checklist

- [ ] Read all relevant `AGENTS.md` files before editing.
- [ ] Confirm imports respect architecture boundaries.
- [ ] Apply code changes.
- [ ] Update context documentation for structural changes.

---

## If you need more detail

No additional resources — this skill is self-contained. Use the workflow above as your checklist.