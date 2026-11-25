---
name: create-adr
description: >
  Author, in-place-edit (in-flight), or supersede (published Accepted)
  Architectural Decision Records under docs/adr/ with shipped mechanics
  headings; classify cited prior ADRs as supersede vs relate; update
  docs/adr/index.md; rebuild at-a-glance HTML catalog. Use when a decision is
  costly to reverse, alternatives were real, someone will ask why months later,
  an in-flight ADR needs refinement, a published Accepted ADR must be replaced,
  or when visualizing the decision log.
disable-model-invocation: true
---

# create-adr

Record **one** significant decision per file under `docs/adr/`. Markdown is
authoritative; the HTML catalog is a generated view.

This skill is **self-contained** (ships in the skills release artifact). Do not
require this library’s `knowledge/` to author ADRs in a consumer repo.

When **`writing-for-agents`** is installed, apply its levers to ADR prose
(hierarchy, completion criteria, pruning). Soft-skip when absent.

## Boundaries

- Do **not** put feature scope, journeys, MVP phases, or sprint plans in an ADR
  — those belong in a PRD (via **`create-prd`** when present).
- Do **not** paste standing ops or glossary text into an ADR — link consumer
  `AGENTS.md` / `CONTEXT.md` / `knowledge/` (when they exist) or another ADR.
- Do **not** invent Implementation Notes checklists (security/CI/ops) unless
  that topic *is* the decision — see [references/mechanics.md](references/mechanics.md).
- **In-flight vs published (edit gate):**
  - **In-flight** = the ADR file is not yet on the remote default branch (typical:
    untracked, or only on a local/unpushed commit; never merged/pushed to
    `origin/<default>`). While in-flight, **edit the same file in place** —
    refine Outcome, Consequences, Implementation Notes, Status. Do **not**
    invent a superseding `NNNN+1` for the same decision.
  - **Published** = the ADR path exists on the remote default branch (pushed /
    merged). Then **Accepted** is immutable: change means a **new** file that
    **supersedes** the old path. Never rewrite published Accepted ADRs in place.
  - Detect with evidence (`git status`, `git log origin/<default> -- <path>`,
    or equivalent) — do not assume “Accepted in Status” alone means published.

## Warrant (before a new file)

Create only if at least one is true:

- costly to reverse
- reasonable people could have chosen differently
- someone will ask “why this way?” later

If none apply, point at an existing ADR or a doc section to edit instead. User
insistence after a failed warrant → ask once; default remains no file.

## Workflow

### 1. Resolve intent

Classify the target ADR as **in-flight** or **published** (see Boundaries).

| Situation | Action |
|-----------|--------|
| New decision, no file yet | Create new `NNNN-ADR-…` |
| In-flight file needs a better outcome / notes | **Edit that file in place** (same `NNNN`) |
| Published **Accepted** decision must change | New file that **supersedes** the old path |
| Ambiguous publish state | Ask once; prefer in-place edit when evidence shows not on remote default |

Do **not** supersede solely because Status says Accepted while the file is still
local-only / unpushed.

**Done when:** create vs in-place edit vs supersede is clear.

### 2. Classify cited prior ADRs

For every older ADR this decision mentions, pick exactly one:

| Class | Meaning | Status links |
|-------|---------|--------------|
| **supersede** | New **outcome replaces** the old decision | New: `Supersedes` → old. Old: Status → `Superseded`, `Superseded by` → new. Index both rows. |
| **relate** | New decision **preserves or extends** the old one | Status `Supersedes` / `Superseded by` stay `—`. Index **Related** column (and optional Status **Related ADRs**). |
| **reject-option-cost** | Old ADR is a reason an **option fails** (pros/cons), not a replaced decision | Same as **relate** — never write `Superseded by` on the old ADR. |

Citing “breaks ADR NNNN” under a rejected option is **reject-option-cost** /
**relate**, not **supersede**.

**Done when:** every cited prior ADR has one class; supersede pairs get
bidirectional Status updates in the same run.

### 3. Number and path

- Home: `docs/adr/` (create if missing)
- Name: `NNNN-ADR-<slug>.md` (four digits, no project-key prefix)
- Next `NNNN`: max existing index + 1 (first is `0001`)

**Done when:** path does not collide.

### 4. Write body

Load [references/mechanics.md](references/mechanics.md) for headings, placement,
and anti-bloat rules. Status values: Proposed | Accepted | Deprecated |
Superseded. Link supersedes / superseded-by / related with Markdown paths.
Prefer cite under **References** over paste.

**Done when:** required headings present; decision outcome is assertive; Status
links match the class from step 2; Implementation Notes (if any) are
outcome-entailed only; any autonomous/ill-defined judgment is flagged under
Assumptions per mechanics **Human review (autonomous judgment)**.

### 5. Update index

Add or revise the row in `docs/adr/index.md`. Put **relate** /
**reject-option-cost** targets in the Related column; for **supersede**, set
Status on both rows.

**Done when:** index row matches the file(s).

### 6. Visualize (at-a-glance)

After create/supersede (or when the user asks for the decision log / catalog):

1. If **`.scratch/adr-optics/`** is missing, run **`setup-bmurrtech-skills`**
   (creates `.scratch/`, `.scratch/visuals/`, `.scratch/adr-optics/`, and the
   rest of the scaffold) — then continue.
2. Rebuild and **open** the catalog with this skill’s **repo-local** helper
   (ships beside this `SKILL.md`; no remote install):

| | |
|--|--|
| **Script** | `scripts/build_catalog.py` under this skill directory (library path: `skills/create-adr/scripts/build_catalog.py`; harness installs: same relative path on the installed skill) |
| **Reads** | Markdown ADRs under `--home` (default: `docs/adr/`); template `scripts/visualizer_template.html` |
| **Writes** | Always: slim tracked `docs/adr/catalog.json` (`schema_version` 2: decisions + `lineage_edges` + `issues`). Optional `--write-index`: refresh `docs/adr/index.md` (incl. lineage-review notes). With `--visualize`: fat `.scratch/adr-optics/adr-catalog.json` + `adr-at-a-glance.html` (gitignored) |
| **Side effects** | `--open` may launch the default browser on a `file://` URI; no network font/CDN loads (system fonts only). Exit **non-zero** only for `invalid_lineage` (self-target / cycle) after still writing catalog artifacts |

```bash
python3 skills/create-adr/scripts/build_catalog.py --home docs/adr --visualize --open
```

If this skill lives outside `skills/create-adr/` (harness install path), point at
this skill’s `scripts/build_catalog.py` instead.

`--open` launches the default browser (`file://`). If the harness cannot open a
browser, report the absolute path and the `file://` URI from the script JSON.

Markdown under `docs/adr/` remains SoT. Tracked slim `catalog.json` is a
rebuildable decision-catalog cache for git history; scratch HTML/JSON are local
glance only. Supersession is the only lineage edge (Previous walks predecessors;
Next is a return stack — not “the successor”).

**Done when:** script exits 0 (or non-zero only for invalid lineage, with
catalog still written); browser opened or `file://` path reported; soft-skip
only if Python unavailable (still leave Markdown + index correct).
