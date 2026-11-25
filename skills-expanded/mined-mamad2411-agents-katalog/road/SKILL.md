---
name: road
description: >
  Manages project roadmaps — ordered lists of Work Items (WI) that point to specs.
  Activates in two situations. (A) Explicit roadmap operations via `/road <action>`
  (create / edit / show / sync / branch) or natural language — create/edit/show/sync
  roadmaps, manage work items. (B) Spec-change side effects — whenever the user
  performs an action that moves, archives, or creates a spec file that could be
  referenced by a roadmap WI (e.g. `mv openspec/changes/add-x openspec/changes/archive/`,
  completing a superpowers task, creating a new spec directory), check whether any
  roadmap WI references that spec and update its status accordingly. Tool-neutral —
  links to any spec-writing tool (openspec, superpowers, plans, issues, URLs).
user-invocable: true
---

# Roadmap Skill

Tool-neutral roadmap management. A roadmap is an ordered list of Work Items (WI) pointing to specs. The spec tool owns implementation state; the roadmap **derives** WI status from the spec's location.

## When this skill activates

- **A. Explicit roadmap operations** — `/road <action>` or natural-language phrasing for create / edit / show / sync / branch / archive (archive = plain `mv`).
- **B. Spec-change side effects (automatic)** — whenever the user's action moves, creates, or deletes a spec file that a roadmap WI could reference, check every WI's `Spec:` field and apply Sync rules without needing an explicit roadmap command.

Examples triggering B:

- `mv openspec/changes/add-auth openspec/changes/archive/` → sync WI referencing it
- "I archived the add-auth change" → same
- User creates `openspec/changes/new-feature/` where a WI had `Spec: TBD` pointing there → prompt user to update the WI's Spec
- Deleting a spec directory → do NOT auto-skip; warn the user

## Sync rules

Status is derived from Spec location.

| Spec resolves to | Action |
| --- | --- |
| `openspec/changes/archive/<name>/` — directory exists | Set `[v] Done` |
| `openspec/changes/<name>/` — directory exists (not under archive) | Ensure `[ ] Pending` (no demotion of Done) |
| Generic path — any file or directory at that path exists | Ensure `[ ] Pending` |
| Spec path does not resolve | **Keep existing status**; emit warning |
| `Spec: TBD`, URL (http/https), or issue link | Never auto-synced |

### Safety principles

1. **Promote only, don't demote**. Pending → Done is automatic. Done → Pending is never automatic (an archive being moved back out is ambiguous; warn and let the user decide).
2. **Never auto-skip**. A missing spec dir is ambiguous (could be "not created yet" vs "abandoned"). Warn; let the user decide.
3. **Respect manual Skipped**. `[~] Skipped` WI are never touched by sync, even if the spec later reappears. It was the user's deliberate choice.
4. **`Spec: TBD`** is a manual marker ("I will fill this in later"). Sync ignores these WI.

## Spec tool detection

When the skill needs to know which spec tool the project uses (creating a roadmap, adding a WI, running sync), it decides via this precedence:

1. **Explicit user statement.** If the user has said "I use openspec" / "this project tracks specs in `docs/plans/`", use that. Don't ask again in the same session.
2. **Auto-detect from existing directories.** Scan the repo root for known markers:
    - `openspec/changes/` → openspec adapter
    - `docs/plans/` → generic plans
    - (more adapters can be added over time)
   If exactly one match, use it silently.
3. **Ask the user.** If nothing is detected, or more than one marker matches, ask which to use as the primary. Remember the choice for the session.

When adding a WI, pre-fill `Spec:` with a path based on the detected tool (e.g. `openspec/changes/<kebab-title>/` for openspec); user confirms or overrides with `TBD` / URL / anything else. Internal reasoning — no flags, no config files.

## Manual override

The user can always override status via natural language or `/road edit`:

- "WI-03 不做了" / "Skip WI-03" → `[~] Skipped`, ask for reason → Notes
- "WI-05 is actually done" → `[v] Done`, even if no archive is detected
- "Revert WI-02 to Pending" → `[ ] Pending`, ask for reason → Notes

Manual edits are honored. Sync does not undo them.

## File layout

```text
roadmaps/
├── {slug}.md           # active roadmap (kebab-case filename)
└── archived/           # archived roadmaps
    └── old-thing.md
```

No index file. The filesystem is the index; summary is computed on demand by `/road show`.

## Roadmap header schema

Optional metadata line placed directly below the `# {Title} Roadmap` H1 (before `## Legend`):

| Field | Required | Format |
| --- | --- | --- |
| Branched from | no | `{src-slug} @ WI-XX` — src is the source roadmap slug (no path, no extension); WI-XX is the anchor WI in src that this roadmap diverges after |

Example:

```markdown
# Backend V2 Roadmap
**Branched from:** backend @ WI-05
```

Semantics: src's WI-01 through WI-XX are shared history; this roadmap's own WI list starts after the divergence. `/road show <slug> --full` renders the stitched view.

## Work Item schema

| Field | Required | Format |
| --- | --- | --- |
| ID | yes | `WI-NN` (or `WI-NNN` past 99); unique per roadmap; never recycled |
| Title | yes | kebab-case verb phrase, in H3 header (`### WI-01 add-foo`) |
| Status | yes | `[ ] Pending` / `[v] Done` / `[~] Skipped` |
| Delivers | yes | 1-3 sentences — **what capability the user/system gains** (not task description) |
| Spec | yes | free string (URL / path / issue link / `TBD`) |
| Phase | no | integer; must exist in the Overview table |
| Notes | no | free text |

Required fields always appear. Optional fields: omit the entire line when empty (do not write `—`).

## States

Three symbols, used both on WI (per-item) and roadmap (aggregate):

- `[ ]` **Pending** — default for a new WI
- `[v]` **Done** — completed (usually set by sync when the spec is archived)
- `[~]` **Skipped** — decided not to do

**Skipped stub rule**: when a WI moves to Skipped, strip all fields except `Status` and `Notes`. The Title stays in the H3 header. Required-fields rule does not apply to Skipped WI.

**"Currently in progress"** is inferred, not stored: the first `[ ]` WI in file order. For that WI's detailed progress, check its Spec tool.

**Roadmap aggregate status** (for show / list):

- `[ ]` — at least one Pending WI remains
- `[v]` — all WI are Done / Skipped AND total >= 1 ("closed", includes the all-Skipped case)

## Intents

`/road <action> [args...]` or natural language. `<action>` ∈ {`create`, `edit`, `show`, `sync`, `branch`}. Omitted action = `/road show` (list roadmaps). Everything else flows through natural language.

### 1. Create roadmap

Trigger: `/road create <slug>` or "create a new {slug} roadmap"

Create `roadmaps/{slug}.md` with this exact skeleton:

```markdown
# {Title} Roadmap

## Legend
- [ ] Pending  [v] Done  [~] Skipped
- First `[ ]` WI is currently in progress; check its Spec for details

## Work Items
```

`{Title}` is title-case of the slug (`backend` → `Backend`); user may override. Self-bootstrap `roadmaps/` if missing; ask for slug if missing.

### 2. Edit roadmap (conversational modification)

Trigger: `/road edit [slug]` or natural language ("add a WI to backend", "WI-03 不做了", "change WI-02's delivers to...").

Any modification happens here:

- **Add a WI**: auto-assign next ID (max + 1), Status `[ ] Pending`. Elicit Title, Delivers, Spec. For Delivers, ask **"what capability does the user/system gain?"** (not "what does it do"). If Spec is unknown, allow `TBD`.
- **Skip a WI**: set Status `[~] Skipped`, strip to stub per the Skipped stub rule, ask for reason → Notes.
- **Un-skip a WI** (`[~] → [ ]`): requires user confirmation; re-fill Delivers and Spec.
- **Manual Done** (`[ ] → [v]` without archive): allow; no confirmation needed. For reverting Done (`[v] → [ ]`), require confirmation and write reason to Notes.
- **Edit a field**: change Delivers / Spec / Phase / Notes / Title of a specific WI.
- **Phase / Overview**: add or rename a phase row in the Overview table; reassign a WI's Phase.

No "delete WI" operation — use Skip + Notes for mistakes. IDs are never recycled.

### 3. Show / summarize

Trigger: `/road show [slug] [--full]` or "show all roadmaps" / "{slug} progress"

- **No arg**: scan `roadmaps/*.md` (not `archived/`), output a summary table of all roadmaps with Status + Progress.
- **With slug**: show that roadmap's WI list with statuses; highlight the first `[ ]` as "currently in progress". If the roadmap has a `Branched from` header, note it at the top.
- **With slug + `--full`**: if the roadmap has `Branched from: {src} @ WI-XX`, prepend src's WI-01 through WI-XX as "inherited from {src}" (read-only display), then the roadmap's own WI. Without `--full`, only own WI are shown.
- Progress format: `{done}/{total}[, {skipped} skipped]` — `skipped` clause shown only when skipped > 0. Branched roadmaps compute progress over own WI, not inherited history.

### 4. Sync (manual fallback)

Trigger: `/road sync [slug]` or "resync roadmaps"

- Scan every WI in every active roadmap (or the given slug).
- Apply the Sync rules.
- Report: promotions made, warnings about unresolved specs, any ambiguity needing user decision, plus format/validation issues (see below).

**Manual fallback** — the skill normally stays in sync via section-B triggers. Use explicit sync for: initial adoption (bringing an existing roadmap up to date), after batch operations done outside the AI session, periodic audit.

### 5. Branch roadmap

Trigger: `/road branch <src-slug> <dst-slug> [--at WI-XX]` or "branch {src} into {dst}".

Diverges a new roadmap from an existing one at a specific WI — explore alternative paths without disturbing src.

Behavior:

1. Verify `roadmaps/{src}.md` exists; fail otherwise.
2. Resolve the anchor WI: if `--at WI-XX` is given, use that; otherwise use src's last `[v] Done` WI. If src has no Done WI and `--at` is not given, ask the user which WI to branch at.
3. Verify the anchor WI exists in src; fail otherwise.
4. Create `roadmaps/{dst}.md` with this skeleton:

   ```markdown
   # {Dst Title} Roadmap
   **Branched from:** {src-slug} @ WI-XX

   ## Legend
   - [ ] Pending  [v] Done  [~] Skipped
   - First `[ ]` WI is currently in progress; check its Spec for details

   ## Work Items
   ```

5. Do **not** copy any WI from src — dst starts empty. Shared history is referenced via `Branched from`, not duplicated.
6. dst's WI numbering starts fresh at WI-01 in its own namespace. Cross-roadmap refs (`{dst}/WI-XX` vs `{src}/WI-XX`) don't collide.

No merge operation — branches are one-way. Reconciling two roadmaps is manual (copy WI content between files).

### 6. Archive / Unarchive roadmap

No dedicated command — natural language only: "archive the backend roadmap" → `mv roadmaps/backend.md roadmaps/archived/`. Pure `mv`, no side effects.

## Behavior rules (unique to this skill)

- **Users may edit roadmap files directly**. The skill must handle any valid file state on the next operation; don't assume the skill itself made all prior changes.
- **Renaming a roadmap file is not a supported intent**. If the user does it manually, the next sync will flag any dangling `Branched from` references pointing at the old slug.
- **Branch reference resolution is "warn but don't block"**: on write, warn if the target src roadmap or anchor WI doesn't exist but allow; sync reports dangling refs.
- **No time tracking in files** (no `Last updated`, no Changelog). Use `git log` for history.

## Format / validation checks (run during sync)

- `error` — Status symbol matches text (`[v] Done`, `[~] Skipped`, `[ ] Pending`; no legacy `Shipped` / `Cancelled` / `In Progress`)
- `error` — Required fields present (ID / Title / Status / Delivers / Spec) — except Skipped WI (stub exception)
- `error` — Skipped WI are stubs (Status + Notes only)
- `error` — IDs unique, no duplicates
- `error` — `Phase:` value exists in the Overview table
- `error` — Overview `Items` range matches actual Phase distribution
- `warning` — `Spec: TBD` (remind the user to fill in)
- `warning` — WI in file in ID ascending order
- `warning` — `Branched from` src roadmap exists and anchor WI exists in src

## Example roadmap file

```markdown
# Backend Roadmap

## Legend
- [ ] Pending  [v] Done  [~] Skipped
- First `[ ]` WI is currently in progress; check its Spec for details

## Overview
| Phase | Goal | Items |
| --- | --- | --- |
| 0 | Foundation | WI-01 ~ WI-02 |
| 1 | Core features | WI-03 ~ WI-04 |

## Work Items

### WI-01 add-config-loader
**Status:** [v] Done
**Phase:** 0
**Delivers:** Configuration is loaded from a single source of truth; environment overrides are predictable
**Spec:** `openspec/changes/archive/add-config-loader/`

### WI-02 add-logging-infrastructure
**Status:** [ ] Pending
**Phase:** 0
**Delivers:** All modules emit structured logs with consistent fields; log level is runtime-configurable
**Spec:** `openspec/changes/add-logging-infrastructure/`
**Notes:** Must be in place before any feature work starts

### WI-03 add-user-authentication
**Status:** [ ] Pending
**Phase:** 1
**Delivers:** Users can sign in and receive a session token; protected routes reject unauthenticated requests
**Spec:** `openspec/changes/add-user-authentication/`

### WI-04 experiment-cache-layer
**Status:** [~] Skipped
**Notes:** Evaluated and abandoned; benchmarks showed no meaningful gain at current scale
```

## Out of scope

- Spec content management (this skill links to specs, doesn't write them)
- Git operations (the user commits manually)
- Owner / deadline / label / workload tracking
- Visualization (Gantt charts, Kanban boards)
- Cross-project sync (each repo has its own `roadmaps/`)
