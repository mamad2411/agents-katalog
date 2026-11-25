---
name: repo-glossary
description: Audit and reconcile the shared project glossary — find stale terms, missing definitions, conflicts, shadows, inheritance gaps, and cross-path divergences across research docs
type: research
version: v0.3
argument-hint: "[optional: focus area e.g. \"tooling\", \"business\", \"workflow\"]"
---

# Repo Glossary — Glossary Audit & Reconciliation

Invoke as `$repo-glossary`.

Scans all research documents, CLAUDE.md, and docs for domain-specific terminology, then audits the shared glossary for accuracy, conflicts, staleness, shadows, inheritance gaps, and cross-path divergences. In multi-path repos, glossaries form a two-level hierarchy: a parent glossary (`research/glossary.md`) with shared terms and scoped glossaries (`research/{slug}/glossary.md`) that inherit parent terms and can override them. This is the look-back complement to the write-forward glossary convention: research skills add terms during their alignment flow, and this skill periodically reviews the full glossary hierarchy for drift and gaps.

## Prerequisites

- **Hard**: At least 2 files must exist in `research/` (or `research/{slug}/`). If fewer exist, tell the user to run more research skills first and stop.
- **Soft**: `research/glossary.md` may or may not exist. If it does not exist, the skill runs in bootstrap mode — all discovered terms are treated as proposed additions.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 1. Load Sources

Read every file in scope and extract terminology. Load glossary files hierarchy-aware:

**Parent glossary** (`research/glossary.md`):
- Always load when it exists, even when running in scoped mode
- Parse all existing entries from the Terms table (Term, Definition, Source, Category, Status, and optional Scope)
- Parse Acronyms table and Recently Added table
- Tag each term with origin `parent`

**Scoped glossary** (`research/{slug}/glossary.md`):
- Load the target scoped glossary when running in product-path mode
- Parse Terms table (Term, Definition, Source, Category, Status — no Scope column)
- Tag each term with origin `scoped:{slug}`

**Sibling glossaries** (cross-path audit mode):
- When auditing across all product paths, also load `research/{other-slug}/glossary.md` for each active product path
- Tag each sibling term with origin `scoped:{other-slug}`

**Research documents** (`research/*.md` or `research/{slug}/*.md`):
- Extract terms that appear with inline definitions, parenthetical expansions, or "i.e." / "a.k.a." markers
- Extract capitalized compound nouns or quoted terms used as domain jargon
- Extract acronyms used without expansion

**Convention and documentation files** (`CLAUDE.md`, `docs/*.md`, `packs/*/PACK.md`):
- Extract terms defined in glossary-like sections, definition lists, or tables
- Extract tool/workflow/concept names that carry project-specific meaning

Build a combined term index: `{ term, definition (if found), sources[], category (inferred) }`.

### 2. Surface & Interrogate

Cross-reference the combined term index against the existing glossary to classify every term into one of four groups:

**Existing terms** — present in glossary.md:
- Check whether the current definition still matches how the term is used across research docs
- Flag terms whose usage has drifted from the glossary definition
- Show source count and last-seen document

**Missing terms** — used in research docs but absent from glossary:
- Propose a definition based on context where the term appears
- Infer category (business / tooling / workflow / technical / domain)
- Rank by frequency and number of distinct source documents

**Conflicting terms** — same term defined or used differently across documents:
- List each conflicting definition with its source
- Ask user to select the canonical definition or provide a new one

**Stale terms** — present in glossary but no longer appear in any scanned document:
- Show the term, its glossary definition, and original source
- Ask whether to keep, update, or remove

**Shadowed terms** — same term defined in both parent and scoped glossary with different definitions:
- Show parent definition and scoped definition side by side
- Ask: intentional override (set `status: confirmed-override` in scoped) / promote scoped definition to parent / align scoped definition to match parent

**Cross-path divergences** — same term defined differently in sibling scoped glossaries:
- List each sibling's definition with its slug
- Ask: all valid in context (each scope uses its own meaning) / reconcile to a shared parent definition / provide a new shared definition

**Inheritance gaps** — hierarchy inconsistencies between parent and scoped glossaries:
- Parent terms with Scope references to removed or archived product paths
- Scope-restricted parent terms that conflict with their target scoped glossary's definition
- Scoped terms that duplicate a parent term identically (candidate for removal from scoped glossary)

If `$ARGUMENTS` specifies a focus area, filter findings to that category.

### 3. Present in Alignment Page

Build the alignment page with findings grouped by the four categories above. Each category is a gate section with inline approval questions:

**For missing terms**: per-term radio — Approve proposed definition / Edit definition / Reject / Needs clarification
**For existing terms**: per-term radio — Confirm accurate / Update definition / Remove / Needs clarification
**For conflicting terms**: per-term radio showing each conflicting definition — select canonical / Provide new / Needs clarification
**For stale terms**: per-term radio — Keep / Remove / Needs clarification

**For shadowed terms**: per-term radio — Intentional override (confirm shadow) / Promote scoped to parent / Align scoped to parent / Needs clarification
**For cross-path divergences**: per-term radio showing each sibling definition — All valid in context / Reconcile to parent / Provide new shared definition / Needs clarification
**For inheritance gaps**: per-term radio — Fix scope reference / Remove duplicate from scoped / Update conflicting definition / Needs clarification

Include an evidence matrix mapping each proposed change to the source documents that support it.

### 4. Write Output

After final compiled YAML approval, apply approved changes to the appropriate glossary file(s):

**Base write rules** (apply to both parent and scoped glossaries):
- Add approved new terms to the Terms table with `status: confirmed`
- Update definitions for terms marked "Update definition"
- Remove terms marked "Remove"
- Resolve conflicts by writing the user-selected canonical definition
- Update the Acronyms table for any new acronym expansions
- Update the Recently Added table with terms added in this run
- Update the header metadata (last updated date, source count, term count)

**Hierarchy-aware write rules:**
- **Promote scoped → parent**: add the term to the parent glossary with `Scope: shared`, remove the term from the scoped glossary
- **Align scoped → parent**: update the scoped definition to match the parent, or remove the scoped entry entirely
- **Acknowledge shadow**: set `status: confirmed-override` in the scoped glossary entry; future audits skip the shadow warning for that term
- **Reconcile cross-path divergence**: write the reconciled definition to the parent glossary, remove or update sibling scoped entries
- **Fix inheritance gap**: remove stale Scope references from parent, remove duplicate scoped entries that match parent identically
- **Add Scope column**: add the Scope column to the parent glossary only when the repo has multiple active product paths; omit for flat repos

If a target glossary does not exist, create it with the appropriate standard format before writing entries.

**Standard parent glossary format** (multi-path repos — includes Scope column):

```markdown
# Glossary

> Last updated: YYYY-MM-DD | Sources: [count] docs | Terms: [count]

## Terms

| Term | Definition | Source | Category | Status | Scope |
|------|-----------|--------|----------|--------|-------|

## Acronyms

| Acronym | Expansion | Source |
|---------|-----------|--------|

## Recently Added

| Term | Added | Source Skill | Approved In |
|------|-------|-------------|-------------|
```

**Standard glossary format** (flat repos and scoped glossaries — no Scope column):

```markdown
# Glossary

> Last updated: YYYY-MM-DD | Sources: [count] docs | Terms: [count]

## Terms

| Term | Definition | Source | Category | Status |
|------|-----------|--------|----------|--------|

## Acronyms

| Acronym | Expansion | Source |
|---------|-----------|--------|

## Recently Added

| Term | Added | Source Skill | Approved In |
|------|-------|-------------|-------------|
```

### 5. Populate Next Steps

Include 3–5 applicable items with "Pick one:" framing:

- IF conflicting terms remain unresolved: `$repo-glossary` — Re-run to resolve remaining conflicts
- IF assumption-tracker exists and references undefined terms: `$assumption-tracker` — Update assumption register with clarified terminology
- IF research docs have many undefined terms: run more research skills to build context, then `$repo-glossary` again
- IF glossary is comprehensive: `$reconcile-research` — Check cross-document consistency now that terms are aligned
- ALWAYS: `$research-roadmap` — Check overall project status

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page with the full preliminary packet, evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Output

### `research/glossary.md` (parent glossary)

The shared cross-path project glossary in the standard parent format shown in Section 4. Includes the Scope column only in multi-path repos.

### `research/{slug}/glossary.md` (scoped glossary, when product-path mode is active)

The scoped glossary for a specific product path, inheriting all parent terms. Uses the standard format without the Scope column.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Read-only on research docs.** Extract terms from existing research — do not modify source documents. Only glossary files (`research/glossary.md` and `research/{slug}/glossary.md`) are writable.
- **Be specific.** "A thing" is not a term. "Pack — a collection of related skills installed together via pack.sh" is.
- **Trace to source.** Every term must reference the specific document it was extracted from.
- **Update, don't duplicate.** If a glossary already exists, merge new findings with existing entries. When updating, preserve confirmation status, `confirmed-override` status, and Recently Added history.
- **Present before writing.** Never write output files until findings have been presented and validated via the alignment page.
- **Respect write-forward.** Terms added by research skills during their alignment flow have `status: confirmed`. Do not downgrade confirmed terms to `proposed` during audit.
- **Hierarchy consistency.** A scoped glossary entry with `status: confirmed-override` is an acknowledged shadow — do not re-flag it as a conflict in future audits. When promoting or reconciling terms, ensure the parent and scoped glossaries remain consistent.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/repo-glossary-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
