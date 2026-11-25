---
name: generic-memory-policy
description: Apply when writing to or reading from any memory store (user-level auto-memory under ~/.claude/projects/.../memory/, or project-local memory/). Defines what goes where, what NOT to save, and how to handle "remember X" requests.
metadata:
  stack: [generic]
---

# Memory policy

Two memory layers exist. The toolbox doesn't replace either — it documents who owns what.

| Layer | Location | Owner | Use for |
|---|---|---|---|
| User-level auto-memory | `~/.claude/projects/<project-slug>/memory/` (with `MEMORY.md` index) | Claude Code harness (rules in the harness system message) | Persistent across sessions — user role, feedback, project-level facts not in the repo, external references |
| Project-local `memory/` | `<repo>/memory/` (already exists) | `dev-team` plugin's three-phase workflow | Phase progress files (research/plan/implementation), `decisions.md` (DEC-YYYY-MM-DD-NNN entries), session continuation state |

## What to save where

### User-level auto-memory

Save when the harness rules say so — typically:

- User identity, role, preferences ("user prefers branch-per-feature", "user owns commit/PR flow").
- Feedback ("don't summarise at the end of every reply").
- External references ("Linear project INGEST tracks pipeline bugs", "Grafana dashboard at internal/d/api-latency").
- Surprising or non-obvious project facts that would help future sessions.

### Project-local `memory/`

Use during a feature's lifecycle, owned by the plugin's three-phase workflow:

- `memory/<feature>/research.md` — Phase 1 progress file.
- `memory/<feature>/plan.md` — Phase 2 plan and review summary.
- `memory/<feature>/implementation.md` — Phase 3 step-by-step progress.
- `memory/decisions.md` — `DEC-YYYY-MM-DD-NNN` entries: significant routing or scope decisions.

When a feature ships, archive its phase files (or let the plugin do so if it offers an equivalent end-of-feature step) and append the final decision entry to `decisions.md`.

## What NOT to save in either layer

These exclusions apply even when the user explicitly asks:

- **Code patterns, conventions, architecture, file paths, project structure** — derivable by reading the project. They belong in skills or design docs, not memory.
- **Git history, recent changes, who-changed-what** — `git log`, `git blame` are authoritative.
- **Debugging solutions or fix recipes** — the fix is in the code; the commit message has the context.
- **Anything already in CLAUDE.md or a skill** — duplication rots.
- **Ephemeral task details** — in-progress work and current conversation context.

If the user asks "save this", ask back: *what was surprising or non-obvious about it?* That's the part worth keeping.

## Handling "remember X" / "forget X"

- "Remember X" / "save X" → user-level auto-memory, following the harness rules for type classification (user / feedback / project / reference) and frontmatter.
- "Forget X" → find the matching memory file in `~/.claude/projects/.../memory/` and remove it; update the `MEMORY.md` index pointer.
- "Recall X" / "what do you remember about Y" → look at `MEMORY.md` first, then the relevant memory files.

## Handling decisions (`memory/decisions.md`)

Append a `DEC-YYYY-MM-DD-NNN` entry when:

- Routing to a non-default agent for a non-obvious reason.
- Choosing between two valid architectural / implementation approaches.
- Overriding a routing table default or established convention.
- Resolving a conflict between agent recommendations.
- Making a scope call that constrains future phases.

Skip routine decisions (standard routing, normal code patterns, expected behaviour). Don't pad the decision log.

## Anti-patterns

- Writing project-derivable facts to user-level memory ("the API listens on :5001"). That's in CLAUDE.md and Docker config.
- Treating project-local `memory/` as a long-term store. After ship, archive.
- Storing secrets or PII in either memory. Both are unencrypted; Key Vault is the secret store.
- Updating memory based on a passing comment without checking whether the underlying claim is still true. Memory ages; verify before acting on it.
- Auto-recording every chat exchange. Memory is for surprising/non-obvious truths, not chat history.
