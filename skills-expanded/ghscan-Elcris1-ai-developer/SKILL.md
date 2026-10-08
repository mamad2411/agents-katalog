---
name: notes-workflow
description: Work on notes-cli's note lifecycle (create, search, archive,
  format migration). Use when the task mentions notes, archiving, search,
  frontmatter, or editing src/store.go, or when a spec or plan references
  the note format.
---

<!--
  SKILL (practice 04) — real path: .agents/skills/notes-workflow/SKILL.md.
  This location is deliberate: it is read NATIVELY by Codex (repo skill
  scope) and by opencode via its compatibility scan (.agents/skills is one
  of opencode's documented sources) — one skill file, two agents, zero
  duplication.

  How triggering works:
  - opencode: at each step, permitted skills are advertised to the model by
    ID + name + description only (~nothing standing in context); the body
    loads when the model calls skill({name: "notes-workflow"}). The
    `skill` permission in opencode.jsonc gates loading; deny removes the
    skill from discovery entirely.
  - Codex: repo skills are scanned from CWD up to the repo root; implicit
    invocation can be gated, explicit invocation always works.
  - The description above is the trigger — write it for the matching task
    (what + when + keywords), then test it both ways (practice 04).
-->
# Notes workflow

Implement changes to the note lifecycle against its plan in
`docs/plans/` — this skill exists so the lifecycle rules do not have to be
rediscovered every session.

## Before touching code

1. Read the plan task you are implementing; it declares files and the
   verify command.
2. Locate code by map — do not search blindly:

| Concern | File |
|---|---|
| CLI dispatch | `src/main.go` |
| Store + format | `src/store.go` |

3. The on-disk format is the interface: never break it silently. Format
   changes need a migration task in the plan first.

## Steps

1. Implement within the task's declared file list.
2. Add or update the table-driven test for the behavior.
3. Run `go vet ./... && go test -count=1 ./...` — iterate until green.
4. Check off the task in the plan only with green output noted.

## Gotchas

- Notes may be edited by hand in any editor; tolerate missing or malformed
  frontmatter on read (log-and-skip), never crash.
- Timestamps: parse RFC 3339 with UTC fallback; do not use local time.
- Per-note writes only (AGENTS.md prohibition): batch archiving loops
  per-note, it does not rewrite the directory.
- The store takes `ctx` on every method; respect cancellation in loops.

## Done when

- [ ] Declared tests green, no other files touched
- [ ] Task checkbox updated with the verify command output
