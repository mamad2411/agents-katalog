---
name: sparc
description: Run a SPARC-style implementation workflow: Specification, Pseudocode, Architecture, Refinement, Completion, mapped to OpenCrabs plan/tasks/tools.
---

# SPARC Skill

Use this for complex implementation work, migrations, unfamiliar systems, or when the user asks for SPARC/spec-first development.

Inspired by Ruflo's SPARC/coordinator skills. OpenCrabs-native version: no second harness, no fake swarm theater.

## SPARC phases

1. **Specification**
   - Restate objective as checkable acceptance criteria.
   - If the repository uses openspeq (`specs/mission.md`, `specs/_plans/`, or openspeq templates), run `/openspeq-plan` during this phase so durable spec artifacts are staged before implementation.
   - Identify constraints, project directives, security gates, and external side effects.

2. **Pseudocode**
   - Sketch data flow, state changes, edge cases, and failure modes.
   - Keep it language-neutral unless repo conventions require specifics.

3. **Architecture**
   - Identify files/modules/functions to touch.
   - Choose the simplest shape that fits; avoid incidental framework sprawl.

4. **Refinement**
   - Create an OpenCrabs `plan` with concrete tasks.
   - Implement with `read_file` before `edit_file`.
   - Run the repo's native tests/lints/builds.

5. **Completion**
   - Verify acceptance criteria.
   - Summarize files changed, tests run, and remaining risks.
   - If this is a bug fix/improvement and GitHub is available, follow issue/PR tracking rules.

## Tool routing

- `plan` is mandatory for 3+ tasks or multi-file work.
- `glob`, `grep`, `read_file` before edits.
- `edit_file`/`write_file` for changes.
- `bash` for native tooling.
- Optional `spawn_agent` only for genuinely parallel review/research, never as decoration.

## Safety

Ask before destructive operations, external posting, pushing, or deleting. Use `trash` over `rm` if deletion is explicitly approved.
