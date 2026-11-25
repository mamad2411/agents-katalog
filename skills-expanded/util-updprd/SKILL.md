---
name: util-updprd
model: claude-opus-4-8
effort: high
description: >
  Apply a free-form requirement change to the PRD.md files of a CO2 project. Takes a
  human-written prompt describing NEW requirements or updates to existing ones, analyzes
  the PRD.md of every custom application to determine which applications, modules and
  subsections (User Story, Non Functional Requirement, Constraint, Reference, Test) are
  impacted, and decides for each impacted item whether to ADD, CANCEL or MODIFY it.
  Automatically classifies the change complexity per application as major, minor or patch,
  computes the next semantic version, and writes the new/updated items under a NEW version
  tag layered on top of the existing versions in each PRD.md — never rewriting or deleting
  prior versions. Cancelled items are struck through in place and recorded in the new
  version. New items are tagged with unique IDs (via util-ustagger) and a CHANGELOG.md
  entry is appended per impacted application. Presents an impact plan for human
  confirmation before writing (skippable with `--auto-approve` for orchestrated runs).
  ALWAYS stops after updating the PRDs and hands back for human review — it never chains
  into conductor-feature-prepare / -develop / -defect or any generator skill.
  Trigger on keywords: "update PRD", "update the PRD", "add requirement", "new requirement",
  "change requirement", "update requirements", "add user story", "cancel user story",
  "modify user story", "add NFR", "add constraint", "requirement update", "bump PRD version",
  "new version of requirements", "apply this requirement", "we now need", "the client wants".
  Accepts a free-form change prompt as the main argument, with optional `application:<app>`
  and `module:<module>` scope filters
  (e.g., `/util-updprd "Add SSO login for all users"`,
  `/util-updprd "Corridor codes must be unique" application:hub_middleware`).
---

# Util Update PRD

Take a free-form requirement change written by a human and apply it to the PRD.md files across
a CO2 project. The skill figures out **what changed**, **which applications/modules are
impacted**, **whether each change is an add / cancel / modify**, and **how big the change is**
(major / minor / patch) — then layers the change onto each impacted PRD.md as a **new version
on top of the existing versions**, leaving all prior versions untouched.

This skill is the counterpart to the human-authored PRD: instead of a person hand-editing
requirements, they describe the change in plain language and this skill applies it consistently
and traceably across every affected application.

## Inputs

```
/util-updprd "<free-form requirement change>" [application:<app>] [module:<module>] [--auto-approve]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `<prompt>` | Yes | Free-form description of the new requirement(s) or the update(s) to existing ones. May describe multiple discrete changes at once, and may explicitly say something should be removed/cancelled. |
| `application:<app>` | No | Restrict analysis to a single application. If omitted, **all** custom applications are analyzed and only the impacted ones are changed. |
| `module:<module>` | No | Hint/restrict the change to a specific module. If omitted, the impacted modules are inferred. |
| `--auto-approve` | No | Skip the Phase 3 confirmation checkpoint and apply the plan directly. Intended for orchestrated/autonomous runs where interactive confirmation is not possible. Without this flag, the skill presents the plan and waits for the human to confirm before writing. |

Example invocations:
- `/util-updprd "Every user must be able to reset their own password from the login screen"`
- `/util-updprd "Drop the CSV export from the dashboard — it is being replaced by scheduled email reports" application:hub_middleware`
- `/util-updprd "Corridor codes must be globally unique and are now case-insensitive" application:hub_middleware module:corridor`
- `/util-updprd "Add audit logging for all admin actions" --auto-approve`

### Application Resolution

Same rules as the other CO2 skills:
1. List root-level application folders (with or without a numeric prefix, e.g. `1_hub_middleware`, `mainapp`).
2. Strip any leading `<number>_` prefix.
3. Match the `application:` value case-insensitively (accept `snake_case`, `kebab-case`, title-case).
4. If `application:` is given but does not match, list available applications and **stop**.
5. If `application:` is omitted, the candidate set is **every** custom application folder that has a `context/PRD.md`.

### Auto-Resolved Paths (per application)

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |
| CHANGELOG.md | `<app_folder>/CHANGELOG.md` |

## Pre-Requisite: CLAUDE.md (already in context)

CLAUDE.md is loaded automatically at session start. Use it as the **source of truth for what
applications and modules exist**. This skill NEVER invents new applications or modules — modules
are governed by CLAUDE.md and PRD.md is synced from it by `util-projectsync`. If a change
requires a module or application that does not yet exist (see Boundary Rules), report it as a
follow-up action instead of creating it here.

## How Versions Work in PRD.md (read this before editing)

Every subsection in a module carries one or more version tags, each on its own line, with the
items for that version listed below it. New versions are **appended** below older ones —
older version blocks are immutable:

```markdown
### User Story
[v1.0.0]
- [USHM00003] As a user, I want to log in so that I can access my data.
[v1.1.0]
- As a user, I want to reset my own password so that I don't need to call support.
```

The versioning semantics (from the PRD.md `# Context` section) are:

| Level | When to use | Version change |
|-------|-------------|----------------|
| **major** | A significant change that alters the overall understanding of a module or the system — a new module-scale capability, a fundamental behavior/purpose change, cancelling core user stories, or a Design-System / Architecture-Principle change. | `X+1 . 0 . 0` |
| **minor** | A change that affects some details but not the overall understanding — adding new user stories / NFRs / constraints / references / tests to existing modules, or extending existing behavior with new fields or rules. | `X . Y+1 . 0` |
| **patch** | A small change that does not affect understanding — clarifying wording, fixing a typo, tightening a constraint without changing its meaning, or fixing a reference link. | `X . Y . Z+1` |

**One new version per application per run.** All impacted subsections across all impacted
modules of a single application receive the **same** new version tag. The bump level for that
application is the **highest-severity** change among everything affecting it (one major change
makes the whole application bump major, even if the other changes are patches).

## Workflow

### Phase 1 — Understand the Change

1. Read the `<prompt>`. Decompose it into a list of **discrete changes**. A single prompt may
   contain several (e.g., "add password reset AND remove CSV export" is two changes).
2. For each discrete change, determine its **operation** and **artifact type**:
   - **Operation**: `ADD` (a brand-new requirement), `CANCEL` (an existing requirement is no
     longer valid), or `MODIFY` (an existing requirement changes — treated as CANCEL of the old
     wording + ADD of the revised wording so history is preserved).
   - **Artifact type**: which subsection it belongs in — `User Story`, `Non Functional
     Requirement`, `Constraint`, `Reference`, or `Test`. A behavioral feature is usually a User
     Story; a performance/security/availability rule is an NFR; a hard limitation or business
     rule is a Constraint; a pointer to an external doc/message/spec is a Reference; a
     verification instruction is a Test. One discrete change may produce items in more than one
     subsection (e.g., a new feature = a User Story + a Test).
3. If the prompt is genuinely ambiguous about intent (add vs cancel, or which behavior), note
   the ambiguity — it will be surfaced in the Phase 3 plan for the user to resolve. Do not guess
   silently on high-impact interpretations.

### Phase 2 — Impact Analysis

For each candidate application (all, or the `application:`-filtered one):

1. Read `<app_folder>/context/PRD.md`. Parse module sections (`## <Module>` under
   `# System Module` / `# Business Module`) and, within each, the subsections and their
   existing tagged items.
2. Read the application's modules from CLAUDE.md (source of truth) to know the full module set.
3. Map each discrete change to the application's module(s) by matching on:
   - Entities, roles, screens, and domain nouns mentioned in the change vs. those already
     described in each module's user stories / NFRs / constraints.
   - Explicit `module:` hint if provided (restrict to that module but still check cross-module
     references).
   - Cross-application relevance: a change like "all users must use SSO" may impact **several**
     applications — include each one it genuinely affects.
4. For CANCEL / MODIFY operations, locate the **exact existing item(s)** (by ID and wording) that
   the change supersedes. If no matching item exists, downgrade the operation to `ADD` (you can't
   cancel something that isn't there) and note it.
5. Produce, per application, the set of `(module, subsection, operation, item text or target ID)`
   entries. An application with zero entries is **not impacted** and will be left untouched.

### Phase 3 — Classify Version & Present the Plan

For each **impacted** application:

1. Discover the current highest version: scan PRD.md for all `[vX.Y.Z]` tags **and**
   CHANGELOG.md `## vX.Y.Z` headings; take the semantic-version maximum. If none exist, treat
   the baseline as `v1.0.0`.
2. Classify the bump level using the table in "How Versions Work" — pick the highest severity
   across all changes affecting this application.
3. Compute the new version by applying the bump to the highest version
   (e.g., highest `v1.2.3` + minor → `v1.3.0`; + major → `v2.0.0`; + patch → `v1.2.4`).

Then present a consolidated **Impact Analysis & Change Plan** and **wait for confirmation**
before writing anything (this is a cross-cutting, hard-to-reverse edit):

```
## PRD Update Plan

Change prompt: "<the prompt>"

### hub_middleware  (v1.2.3 → v1.3.0, MINOR)
| Module   | Subsection  | Op     | Item |
|----------|-------------|--------|------|
| User     | User Story  | ADD    | As a user, I want to reset my own password ... |
| User     | Test        | ADD    | Verify password reset email is delivered ... |
| Dashboard| User Story  | CANCEL | [USHM00021] ... CSV export ... |

### hc_adapter  (not impacted)

### ⚠ Follow-ups
- Change "add real-time chat module" needs a new module `Chat` that does not exist in CLAUDE.md.
  Add it to CLAUDE.md and run /util-projectsync first, then re-run this skill.
```

**Confirmation gate:**
- If `--auto-approve` is **not** set: present the plan and **stop until the human confirms**. Do
  not write any file before confirmation. If the human amends the plan, apply the amended version.
- If `--auto-approve` **is** set (orchestrated/autonomous run): skip the wait and proceed directly
  to Phase 4, but clearly log every decision and every ambiguity you resolved so the human can
  audit them afterward.

### Phase 4 — Apply the Changes

For each impacted application, edit `<app_folder>/context/PRD.md`. **Never modify or delete any
existing version block, tag, or item** — only append and (for cancellations) strike through.

**ADD** — for each new item:
- Locate the target subsection in the target module.
- If the new version tag `[v{new}]` is not yet present in that subsection, append it on its own
  line **after** the last existing version block of that subsection.
- Append the new item as a plain, **untagged** top-level bullet under `[v{new}]`:
  `- As a user, I want to reset my own password so that I don't need to call support.`
  (User Stories must follow the Agile "As a … I want … so that …" form. Leave the item untagged —
  Phase 5 assigns the ID.)

**CANCEL** — for each cancelled item:
- Find the existing item under its original version block. Wrap its text (keeping its ID) in
  strikethrough and append a cancellation marker, editing it **in place**:
  `- ~~[USHM00021] As a user, I want to export the dashboard to CSV ...~~ [CANCELLED v1.3.0]`
- Under the `[v{new}]` block of the same subsection, add a note bullet recording the removal:
  `- [CANCELLED] [USHM00021] — CSV export removed; superseded by scheduled email reports.`
  (This note already contains the ID, so util-ustagger will skip it.)

**MODIFY** — treat as CANCEL of the old wording plus ADD of the new wording:
- Strike through the old item in place with `[SUPERSEDED v{new}]` instead of `[CANCELLED v{new}]`.
- Add the revised item as a fresh untagged bullet under `[v{new}]` (it gets a new ID in Phase 5).
- Add a note bullet under `[v{new}]` linking them:
  `- [SUPERSEDED] [USHM00007] → revised below (case-insensitive corridor codes).`

Formatting discipline:
- Preserve all existing content, indentation, blank lines, and separators (`---`) exactly.
- Only add top-level bullets for new items; use sub-bullets for their supporting detail if needed.
- Keep the new version tag identical across every subsection you touched in this application.

### Phase 5 — Tag New Items

After all edits for an application are written, assign IDs to the newly added (still untagged)
items by invoking the tagging skill with the application and the **new** version:

```
Skill(skill: "util-ustagger", args: "<application> <new-version>")
```

util-ustagger tags every untagged top-level bullet, continues the running numbers per category,
and skips items that already contain an ID (including the `[CANCELLED]` / `[SUPERSEDED]` notes).
Run it once per impacted application.

### Phase 6 — Record in CHANGELOG.md

For each impacted application, append an entry to `<app_folder>/CHANGELOG.md`:

1. Read `<app_folder>/CHANGELOG.md`. If it does not exist, create it with:
   ```markdown
   # Changelog

   - This file tracks all skill executions by version for this application.
   - The highest version recorded here is the current application version.
   - Skills MUST NOT execute for a version lower than the highest version in this file.

   ---
   ```
2. Search for a `## {new-version}` heading.
3. If it **exists**, append a new row to its table. If it **does not exist**, insert a new
   section after the `---` below the context header and before any existing `## vX.Y.Z` section
   (newest-first ordering), with a table header and the first row.
4. Row format:
   `| {YYYY-MM-DD} | {application_name} | util-updprd | {impacted modules or "All"} | {N added, M cancelled, K modified — one-line summary} |`
5. **Never modify or delete existing rows.** The new version is always higher than the previous
   highest, so it satisfies every downstream skill's version gate.

### Phase 7 — Output Summary

Print a summary table of everything applied:

```
## PRD Update Summary

| Application    | Version        | Level | Added | Cancelled | Modified | Modules Touched      |
|----------------|----------------|-------|-------|-----------|----------|----------------------|
| hub_middleware | v1.2.3 → v1.3.0| MINOR | 2     | 1         | 0        | User, Dashboard      |
| hc_adapter     | (not impacted) | —     | 0     | 0         | 0        | —                    |

### Follow-ups (for the human to run after review — NOT run automatically)
- <any module/application that must be added to CLAUDE.md + util-projectsync first>
- Recommended: run /util-usanalyzer <app> to quality-check the updated requirements.
- When you are satisfied with the updated PRDs, regenerate artifacts with
  /conductor-feature-prepare <app> version:<new-version>, then implement.
```

### STOP — Hand Back to the Human

This skill's job **ends** once the PRD.md files are updated, new items tagged, and CHANGELOG.md
appended. **Do NOT continue into any conductor skill** (`conductor-feature-prepare`,
`conductor-feature-develop`, `conductor-defect`) or any `modelgen-*` / `mockgen-*` / `specgen-*` /
`testgen-*` skill. Requirement changes must be reviewed by a human before any downstream artifact
is generated or code is written. This is true **even under `--auto-approve`** — auto-approve only
skips the *plan* confirmation, it does NOT authorize downstream execution. Print the summary and
the follow-ups (as manual, human-triggered next steps) and stop.

## Boundary Rules (what this skill does NOT do)

- **Never create a new module.** Modules come from CLAUDE.md. If a change needs a module that
  doesn't exist, report it as a follow-up (update CLAUDE.md, run `util-projectsync`, then re-run).
- **Never create a new application.** Out of scope — report it as a follow-up.
- **Never touch downstream artifacts** (models, mockups, specs, tests under `context/*`). This
  skill only edits PRD.md. Regenerating artifacts for the new version is the job of
  `conductor-feature-prepare` — but that is a **separate, human-triggered** run after review, not
  something this skill invokes.
- **Never auto-chain into conductor or generator skills.** After updating the PRDs, stop and hand
  back to the human (see "STOP — Hand Back to the Human"). Even in `--auto-approve` mode, the skill
  applies the PRD changes and stops; it never starts development, preparation, or defect skills.
- **Never rewrite or delete history.** Prior version blocks, tags, and items are immutable;
  cancellations are strikethroughs, not deletions.

## Important Rules

- **Layer, don't overwrite.** Every change lands under a NEW version tag appended below existing
  versions. Existing `[vX.Y.Z]` tags and their items are never modified (except adding
  strikethrough + a cancellation marker to a cancelled item's line).
- **One coherent version per application per run**, applied uniformly to every subsection touched.
- **Bump = highest severity.** If any change to an application is major, the application bumps
  major; otherwise minor if any change is minor; otherwise patch.
- **Leave IDs to util-ustagger.** Insert new items untagged; never hand-assign ID codes — that
  risks collisions with the running counters ustagger maintains.
- **Preserve existing tags and formatting exactly**, including `[USHM…]`/`[NFRHM…]` codes and
  version tags.
- **Only impacted applications are changed.** Applications with no matching modules are reported
  as "not impacted" and left byte-for-byte unchanged.
- **Surface ambiguity, don't bury it.** When intent is unclear, put it in the plan and (when
  interactive) let the user decide before writing.
- **CANCEL requires an existing target.** If the item to cancel/modify can't be found, downgrade
  to ADD and note the discrepancy rather than fabricating a strikethrough.
