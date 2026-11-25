---
name: init-libra
description: Scaffolds the Libra docs structure for a project by reading the codebase and asking the developer about vision and domain, then writing docs plus root AGENTS.md and ARCHITECTURE.md directly to disk. Use when the user runs /init-libra or asks to scaffold Libra docs, init project docs, or set up docs structure.
---

# init-libra

Scaffold a Libra-compliant docs system for a project:
- root `AGENTS.md`
- root `ARCHITECTURE.md`
- `docs/decisions`, `docs/specs`, `docs/design`, `docs/plans`

Read the codebase first, reason about what you still do not know, ask only those
questions, then write everything directly to disk. No PR.

---

## Phase 1 — Read and reason

Read the following files if they exist:

- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` — name, stack, deps
- `README.md` — description, setup, stated goals
- Entry point files (`main.*`, `index.*`, `app.*`, `server.*`) — what does the
  product actually do at runtime?
- Any existing `docs/`, `AGENTS.md`, `.cursor/rules` — avoid overwriting; note
  what exists

After reading, fill in this checklist internally before moving to Phase 2:

| Question | Can I answer from code? | Answer or "unknown" |
|---|---|---|
| Project name | | |
| Language / stack | | |
| What does the product do? | | |
| Who is it for? | | |
| What phase of dev (exploration / active build / post-launch)? | | |
| Key architectural decisions already visible in code? | | |
| What's the single most important thing a coding agent must know? | | |

Only ask in Phase 2 about rows that say "unknown". If you can answer 6/7 from
the code, ask 1 question, not 5.

---

## Phase 2 — Ask only what code cannot tell you

Ask at most 4 questions. Skip any whose answer you already know.

**Question bank — use only as needed:**

- "What problem does this solve, and who is it for?" — skip if README or
  code makes this clear
- "What phase of development are you in — early exploration, active v1 build,
  or post-launch iteration?" — skip if commit history or README signals this
- "Any key architectural decisions already made that aren't obvious from the
  code?" — e.g. infra choices, explicit non-goals, constraints
- "What's the most important thing a coding agent should know before touching
  this codebase?" — almost always worth asking; agents need orientation, not
  just facts

Do not ask questions you could answer with one more minute of reading the code.
Do not ask for information you will not use in a specific file.

---

## Phase 3 — Write docs

Write the following structure directly to disk. Do not open a PR.
```
AGENTS.md
ARCHITECTURE.md

docs/
├── decisions/
│   ├── INDEX.md
│   └── adr-NNN-slug.md        ← optional; only if a real decision exists
├── specs/
│   ├── INDEX.md
│   └── <feature-slug>.md      ← optional; only if a real spec exists
├── design/
│   ├── INDEX.md
│   └── core-beliefs.md
└── plans/
    ├── INDEX.md
    ├── active/
    └── completed/
```

### Content rules

**Rule 1: Never hallucinate.** If you don't know something, use a stub. A stub
is better than plausible-sounding fiction. Mark every stub with `<!-- TODO -->`.

**Rule 2: Populated > stub > blank.** Prefer a real sentence from code or user
answers over a stub. Prefer a stub over an empty section.

**Rule 3: Short and accurate beats long and vague.** A short, concrete summary
beats generic filler. Coding agents read these files — they need signal, not padding.

**Rule 4: Every doc file has YAML frontmatter.** At minimum include `title`,
`date`, and `status`.

**Rule 5: Cross-link with wiki links.** Use forms like `[[adr-005]]`,
`[[spec:auth-flow]]`, `[[design:core-beliefs]]`.

**Rule 6: Index files are always `INDEX.md` (caps).**

### File specs

#### `docs/decisions/INDEX.md`
Short ADR index:
- one-line folder purpose
- table columns: Name, Description, Status
- include "No decisions recorded yet." when empty

#### `docs/specs/INDEX.md`
Short spec index:
- one-line folder purpose
- table columns: Name, Description, Status
- include "No specs recorded yet." when empty

#### `docs/design/INDEX.md`
Short design index:
- one-line folder purpose
- table columns: Name, Description, Status
- include `core-beliefs.md` entry

#### `docs/design/core-beliefs.md`
Guiding principles — the decision filters that break ties when two approaches
conflict. These are not aspirational values.

If the user's answers or the codebase give you signal on principles, write them.
Otherwise stub the whole file with:
```
<!-- TODO: fill in with 3–5 guiding principles that govern how this project
is built. These should be specific enough to break a tie, not generic values. -->
```

#### `docs/plans/INDEX.md`
Short plan index:
- one-line folder purpose
- table columns: Name, Description, Status
- include "No active plans." if none are present

#### `ARCHITECTURE.md` (repo root)
Scaffold section headers only (stubs allowed):
- System overview
- Major components
- Data flow
- Integrations
- Operational concerns

Use short `<!-- TODO -->` stubs where unknown.

#### `AGENTS.md` (repo root)
This is the orientation file for coding agents. It must answer four questions:

1. **What am I working on?** — one sentence
2. **What should I read before making any change?** — table of file → purpose
3. **What must I never do?** — 3–5 hard constraints visible from the codebase
   or stated by the developer
4. **Where is the current work?** — point to `docs/plans/active/` or equivalent

Structure:
```markdown
# AGENTS.md

You are working on **[project name]** — [one-liner].

## Documentation structure

All project docs live in `docs/`. Read → decide → write.

| You want to...               | Look here                          |
|------------------------------|------------------------------------|
| Understand architecture      | `ARCHITECTURE.md` (repo root)      |
| Check existing decisions     | `docs/decisions/INDEX.md`          |
| Read feature scope           | `docs/specs/INDEX.md`              |
| Understand design principles | `docs/design/INDEX.md`             |
| Check execution status       | `docs/plans/INDEX.md`              |

## Stack

[Language, framework, key dependencies — 3–5 lines max]

## When to CREATE a decision record

Create an ADR in `docs/decisions/` when:
- Choosing between 2+ valid technical approaches
- Adopting a new library, service, or architecture pattern
- Changing existing architecture or team conventions
- Making a tradeoff future developers must understand

## When NOT to create a decision record

Skip ADRs for:
- Minor bug fixes/refactors
- Routine version bumps without architectural impact
- Implementation details inside an existing ADR's direction
- Routine maintenance

## When to CREATE or UPDATE a spec

Create/update a spec in `docs/specs/` when:
- Scoping a new feature or significant behavior change
- Requirements change during implementation
- Out-of-scope boundaries must be explicit

## Conventions

- Read existing docs before writing new docs (start at INDEX files)
- Keep docs under 300 lines
- Use wiki links (`[[adr-005]]`, `[[spec:auth-flow]]`)
- Require frontmatter in every doc
```

---

## Phase 4 — Self-check before summarizing

Before reporting to the user, re-read every file you wrote and check:

- [ ] Do root context files (`AGENTS.md`, `ARCHITECTURE.md`) contain concrete information and not generic filler?
- [ ] Does AGENTS.md answer all four orientation questions?
- [ ] Is every unknown section marked `<!-- TODO -->` rather than left blank or
      filled with plausible fiction?
- [ ] Are there any contradictions between files?
- [ ] Does every doc include frontmatter?
- [ ] Are all index files named `INDEX.md` (caps)?

Fix anything that fails before proceeding.

---

## Phase 5 — Confirm and summarize

Tell the developer:

1. **Populated files** — what was written from code or their answers
2. **Stub files** — what has `<!-- TODO -->` markers and needs human input
3. **Skipped / preserved** — any existing files you left untouched

---

## If docs/ already exists

List what exists. Then offer two options:

- **Fill gaps** — scaffold only missing files and directories; do not touch
  existing content
- **Refresh** — re-read the codebase and update existing files where they look
  stale or incomplete (ask before overwriting anything)

Default to fill gaps unless the user asks for a refresh.
