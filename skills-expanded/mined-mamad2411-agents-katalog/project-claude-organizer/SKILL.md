---
name: project-claude-organizer
description: >
  Reads the project .claude/ folder, compares observed contents against the canonical SDD
  structure, presents a dry-run reorganization plan, and applies it additively after user
  confirmation. After successful migration, offers to delete source files from
  .claude/<category>/ with explicit user confirmation. Produces claude-organizer-report.md.
  Trigger: /project-claude-organizer, organize .claude folder, fix project claude structure,
  align project .claude to canonical SDD layout.
format: procedural
---

# project-claude-organizer

> Reads the project `.claude/` folder, compares it against the canonical SDD structure,
> presents a reorganization plan, applies migrations after user confirmation, and optionally
> deletes source files from `.claude/` after successful migration with explicit user confirmation.

**Triggers**: `/project-claude-organizer`, organize .claude folder, fix project claude structure, align .claude to canonical SDD layout, project claude organizer

> **Scope note**: This skill reads the **live `.claude/` folder state** directly — it does NOT
> read from `audit-report.md`. The skill that reads `audit-report.md` and applies its
> corrections is `project-fix`. This skill targets `PROJECT_ROOT/.claude/` only — it MUST
> NOT be run against `~/.claude/` (the user-level runtime).

---

## Organizer Kernel

`project-claude-organizer` operates as a stable organizer kernel with four stages:

| Stage                     | Responsibility                                                                                         | Output                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| Detect                    | Read the live `.claude/` folder shape and resolve the target paths                                     | Observed items, resolved project-local target           |
| Classify                  | Split observed items into canonical, legacy-migration, documentation-candidate, and unexpected buckets | Buckets that define the possible organizer actions      |
| Propose                   | Present a dry-run plan before any writes                                                               | Explicit user-visible plan and confirmation gate        |
| Apply additive migrations | Perform the allowed create/copy/append/scaffold operations after confirmation                          | Updated project files plus `claude-organizer-report.md` |

The kernel is intentionally stable. Migration strategies may evolve, but they operate inside this detect, classify, propose, apply-additive flow rather than redefining the command.

---

## Scope Boundaries

`project-claude-organizer` uses three behavior classes.

| Class                      | Typical examples                                                                         | Mutation scope                                                 | Confirmation model                            |
| -------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------- | --------------------------------------------- |
| Core additive migrations   | create missing required items, copy docs/templates, append routed content                | Additive writes only                                           | Runs inside the approved plan                 |
| Explicit opt-in operations | commands/ scaffolding, readme.md user-choice migration, cleanup deletion prompts         | Limited writes after explicit category or cleanup confirmation | Requires explicit user choice or confirmation |
| Advisory-only outcomes     | unexpected items, skills-audit findings, ambiguous routing, non-qualifying command files | No automatic mutation                                          | Report only                                   |

Notes:

- The organizer is not a generalized transformation engine. If an item does not map cleanly to a supported path, it remains advisory-only.
- Cleanup deletion is a follow-up path after successful migration, not part of the organizer kernel itself.
- Skills audit findings may be important, but they do not expand the organizer's write authority automatically.

---

## Compatibility Policy

Compatibility behavior is a separate policy layer of `project-claude-organizer`, not an implicit side effect of individual migration handlers.

Compatibility rules currently include:

- **Legacy-shape compatibility**: known legacy directories and files are treated as migration candidates so projects can be normalized incrementally.
- **Advisory compatibility**: unsupported or ambiguous structures remain manual-review outcomes instead of forcing speculative organizer mutations.
- **Opt-in compatibility**: scaffolding, user-choice branches, and cleanup deletion remain explicit opt-in paths even when they are available.
- **Audit-adjacent compatibility**: skills audit may surface organizer-relevant findings, but those findings remain diagnostic rather than granting organizer permission to rewrite `.claude/skills/` automatically.

This policy MUST be explicit whenever compatibility behavior affects whether an item is migrated, preserved, or only reported.

---

## Process

### Step 1 — Resolve paths

Determine the project root and the target `.claude/` directory.

**1.1 — Resolve CWD as project root:**

`PROJECT_ROOT` = current working directory (absolute path).

Normalize all paths to forward slashes for display.

**1.2 — Resolve home directory (Windows-compatible):**

Use the following priority chain (same as `install.sh` and `claude-folder-audit`):

1. If `$HOME` is set and non-empty → `HOME_DIR = $HOME`
2. Else if `$USERPROFILE` is set and non-empty → `HOME_DIR = $USERPROFILE`
3. Else if `$HOMEDRIVE` and `$HOMEPATH` are both set → `HOME_DIR = $HOMEDRIVE$HOMEPATH`
4. Else → output error: "Cannot resolve home directory." and stop.

**1.3 — Set target directory:**

`PROJECT_CLAUDE_DIR = PROJECT_ROOT/.claude`

**1.4 — Guard: verify `.claude/` exists:**

Check whether `PROJECT_CLAUDE_DIR` exists as a directory.

If it does NOT exist:

```
No .claude/ folder found at <PROJECT_ROOT>.
This skill targets project .claude/ folders only — not the ~/.claude/ runtime.
It requires a project with an existing .claude/ directory.
Exiting without changes.
```

Stop. Do not write any files.

**1.5 — Guard: prevent targeting `~/.claude/`:**

If `PROJECT_CLAUDE_DIR` resolves to the same path as `HOME_DIR/.claude`, output:

```
This skill targets project .claude/ folders only — not the ~/.claude/ runtime.
Exiting without changes.
```

Stop.

---

### Step 2 — Enumerate observed items

List all items (files and directories) **one level deep** under `PROJECT_CLAUDE_DIR`.
Do not recurse into subdirectories.

Record each item as:

- `<name>` — for files
- `<name>/` — for directories

Collect the result as `OBSERVED_ITEMS`.

---

### Step 3 — Compare against canonical expected item set

The canonical expected item set for a project `.claude/` folder is defined below.
This set is cross-referenced to `claude-folder-audit` Check P8 and MUST remain consistent with it.

**Canonical expected item set (V1):**

```
# Cross-reference: claude-folder-audit Check P8
#
# Required (absence triggers a create action):
CLAUDE.md
skills/
#
# Optional (absence is informational only — not an error):
hooks/
audit-report.md
claude-folder-audit-report.md
claude-organizer-report.md
settings.json
settings.local.json
openspec/
ai-context/
```

**Classification rules:**

- `MISSING_REQUIRED` = items in the Required subset that are NOT in `OBSERVED_ITEMS`
  - Required items: `CLAUDE.md`, `skills/`
- `UNEXPECTED` = items in `OBSERVED_ITEMS` that are NOT in the full canonical expected set
- `PRESENT` = items in `OBSERVED_ITEMS` that ARE in the canonical expected set

**DOCUMENTATION_CANDIDATES classification (runs after the three-bucket classification above):**

```
KNOWN_AI_CONTEXT_TARGETS = [
  "stack",
  "architecture",
  "conventions",
  "known-issues",
  "changelog-ai",
  "onboarding",
  "quick-reference",
  "scenarios"
]

KNOWN_HEADING_PATTERNS = [
  "## Tech Stack",
  "## Architecture",
  "## Known Issues",
  "## Conventions",
  "## Changelog",
  "## Domain Overview"
]

DOCUMENTATION_CANDIDATES = []
```

For each `.md` file currently in `UNEXPECTED`:

**(a) Signal 1 — Filename stem match (case-insensitive):**
Extract the file's stem (filename without `.md` extension). If the stem matches any entry in `KNOWN_AI_CONTEXT_TARGETS` (case-insensitive):

- Add to `DOCUMENTATION_CANDIDATES` with `source = PROJECT_CLAUDE_DIR/<filename>.md`, `destination = PROJECT_ROOT/ai-context/<filename>.md`, `reason = "filename-match"`.
- Remove from `UNEXPECTED`.
- Do NOT apply Signal 2 for this file.

**(b) Signal 2 — Content heading match (for remaining `.md` files in UNEXPECTED only):**
Read the file's content. If any line starts with one of the `KNOWN_HEADING_PATTERNS` entries (case-sensitive, line-starts-with match):

- Add to `DOCUMENTATION_CANDIDATES` with `source = PROJECT_CLAUDE_DIR/<filename>.md`, `destination = PROJECT_ROOT/ai-context/<filename>.md`, `reason = "heading-match"`.
- Remove from `UNEXPECTED`.

Files matching neither signal remain in `UNEXPECTED` — no false promotion.

> **Scope note**: Only root-level `.md` files from `OBSERVED_ITEMS` are eligible. Subdirectory entries (e.g. `extra/`) are not scanned recursively — only the top-level directory entry is considered.

---

### Step 3b — Legacy Directory Intelligence

After the DOCUMENTATION_CANDIDATES classification completes, run a second pass over the remaining
items in `UNEXPECTED`. For each item whose name matches a known legacy directory or file pattern,
reclassify it into `LEGACY_MIGRATIONS` and remove it from `UNEXPECTED`. Items that match no known
pattern are left in `UNEXPECTED` unchanged — the existing "review manually" behavior is preserved
for genuinely unknown items.

```
LEGACY_MIGRATIONS = []
```

Items reclassified into `LEGACY_MIGRATIONS` are removed from `UNEXPECTED`. Each entry in
`LEGACY_MIGRATIONS` carries: `source` (absolute path), `destination` (one or more proposed
destination paths), `strategy` (see table below), and `confirmation_required = true`.

**LEGACY_PATTERN_TABLE** — quick-scan index (match order top-to-bottom, name match first):

| Pattern name    | Match condition                                             | Migration strategy                      | Destination summary                                                                                                                                                                                                                                                                                                                                    |
| --------------- | ----------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `commands/`     | Directory named `commands` (case-insensitive)               | `scaffold` — active SKILL.md generation | For each qualifying `.md` file: derive skill name from stem (kebab-case), infer format type via 4-signal heuristic, check idempotency (skip if `.claude/skills/<stem>/SKILL.md` already exists), write SKILL.md skeleton to `.claude/skills/<stem>/SKILL.md`; non-qualifying files receive advisory notes only; source files NEVER modified or deleted |
| `docs/`         | Directory named `docs` (case-insensitive)                   | `copy` — per `.md` file                 | `ai-context/features/<name>.md` for each `.md` at immediate `docs/` level                                                                                                                                                                                                                                                                              |
| `system/`       | Directory named `system` (case-insensitive)                 | `append` — route by filename            | `architecture.md` → `ai-context/architecture.md`; `database.md` + `api-overview.md` → `ai-context/stack.md`                                                                                                                                                                                                                                            |
| `plans/`        | Directory named `plans` (case-insensitive)                  | `copy` — route by status                | Active plans → `openspec/changes/<plan-name>/`; archived plans → `openspec/changes/archive/<plan-name>/`                                                                                                                                                                                                                                               |
| `requirements/` | Directory named `requirements` (case-insensitive)           | `scaffold` — idempotent                 | `openspec/changes/<YYYY-MM-DD>-<slug>/proposal.md` per `.md` file at immediate level                                                                                                                                                                                                                                                                   |
| `sops/`         | Directory named `sops` (case-insensitive)                   | `user-choice` — per file                | Option A: append section to `ai-context/conventions.md`; Option B: copy to `docs/sops/<filename>`                                                                                                                                                                                                                                                      |
| `templates/`    | Directory named `templates` (case-insensitive)              | `copy`                                  | `docs/templates/<filename>` for each file at immediate `templates/` level                                                                                                                                                                                                                                                                              |
| `project.md`    | Root-level `.md` file named `project.md` (case-insensitive) | `section-distribute`                    | Sections routed to `ai-context/stack.md`, `ai-context/architecture.md`, `ai-context/known-issues.md` by heading signal                                                                                                                                                                                                                                 |
| `readme.md`     | Root-level `.md` file named `readme.md` (case-insensitive)  | `user-choice`                           | Option A: append full content to `PROJECT_ROOT/CLAUDE.md` under marker `<!-- .claude/readme.md -->`; Option B: copy to `PROJECT_ROOT/docs/README-claude.md`; idempotency: if marker already present in CLAUDE.md → record "already integrated (skipped)"                                                                                               |

**Classification loop:**

For each item in `UNEXPECTED`:

- Match item name (case-insensitive) against `LEGACY_PATTERN_TABLE` (top-to-bottom):
  - **On hit**: add entry to `LEGACY_MIGRATIONS` (`source`, `destination(s)`, `strategy`, `confirmation_required = true`); remove item from `UNEXPECTED`.
  - **On miss**: item stays in `UNEXPECTED` — "review manually" behavior unchanged.

> **Scope rule**: Only top-level items (directories and root-level files enumerated in
> `OBSERVED_ITEMS`) are evaluated. Step 3b MUST NOT recurse into subdirectories — a directory
> named `commands/` nested inside another unexpected directory (e.g. `extra/commands/`) is NOT
> matched by the pattern.

#### Pattern detail blocks

##### Pattern: `commands/`

- **Match condition**: Directory named `commands` (case-insensitive)
- **Strategy**: `scaffold` — active SKILL.md generation per qualifying `.md` file
- **Destination**: `.claude/skills/<stem>/SKILL.md` — one SKILL.md skeleton per qualifying file

**Scaffold procedure** (runs when `commands/` category is confirmed in Step 5.7):

1. List all `.md` files at the **immediate** `commands/` level only (no recursion into subdirectories).
2. If no `.md` files are found → output:
   `commands/ — no .md files found at immediate level; nothing to scaffold`
   Stop; no further processing for this category.
3. For each `.md` file found, apply the **4 qualifying markers** (any one marker is sufficient to qualify):
   - **(a) Step-numbered sections**: the file contains lines matching `### Step N`, `- Step N`, or `N.` where N is a number (numbered/bulleted process sections)
   - **(b) Trigger / invocation patterns**: the file contains lines starting with `/command-name` (slash-command references) or lines containing `**Triggers**` or `trigger:` (trigger definitions)
   - **(c) Process headings**: the file contains a section heading that is exactly `## Process`, `## Steps`, `## How to`, or `## Instructions`
   - **(d) Filename-stem keyword match**: the file's stem (case-insensitive) matches one of: `deploy`, `rollback`, `setup`, `onboard`, `audit`, `install`, `release`, `build`, `migrate`, `sync`
4. **Qualifying file** (at least one marker matched):
   - **(4a) Derive skill name**: extract the filename stem; normalize to kebab-case (lowercase, spaces and underscores replaced with hyphens). `<stem>` = normalized stem.
   - **(4b) Infer format type** using the 4-signal heuristic (first match wins; precedence: anti-pattern > reference > procedural):
     - If the source file contains a heading starting with `## Anti-patterns` → `anti-pattern`
     - Else if the source file contains a heading starting with `## Patterns` or `## Examples` → `reference`
     - Otherwise (step-numbered sections, process headings, trigger patterns, keyword stem, or no signals) → `procedural` (default)
   - **(4c) Idempotency guard**: check whether `PROJECT_CLAUDE_DIR/skills/<stem>/SKILL.md` already exists.
     - **If it exists**: record `<filename>.md — [already exists — not overwritten]`. Skip to the next file; do NOT write anything.
     - **If it does not exist**: proceed to 4d.
   - **(4d) Generate SKILL.md skeleton** based on inferred format type. Create directory `PROJECT_CLAUDE_DIR/skills/<stem>/` if absent. Write the appropriate skeleton to `PROJECT_CLAUDE_DIR/skills/<stem>/SKILL.md`:

     **For `procedural` format:**

     ```markdown
     ---
     name: <stem>
     description: >
       Scaffold description. Replace this text with what the skill does and when to trigger it.
     format: procedural
     ---

     # <stem>

     **Triggers**: Replace this scaffold text with the slash command and natural-language triggers.

     ---

     ## Process

     ### Step 1 — Replace with a concrete step name

     Replace this scaffold text with the first concrete action the skill should perform.

     ---

     ## Rules

     - Replace this scaffold rule with a real constraint or invariant.
     ```

     **For `reference` format:**

     ```markdown
     ---
     name: <stem>
     description: >
       Scaffold description. Replace this text with what the skill does and when to trigger it.
     format: reference
     ---

     # <stem>

     **Triggers**: Replace this scaffold text with the slash command and natural-language triggers.

     ---

     ## Patterns

     ### Pattern 1 — Replace with a concrete pattern name

     Replace this scaffold text with the pattern description.

     ---

     ## Rules

     - Replace this scaffold rule with a real constraint or invariant.
     ```

     **For `anti-pattern` format:**

     ```markdown
     ---
     name: <stem>
     description: >
       Scaffold description. Replace this text with what the skill does and when to trigger it.
     format: anti-pattern
     ---

     # <stem>

     **Triggers**: Replace this scaffold text with the slash command and natural-language triggers.

     ---

     ## Anti-patterns

     ### Anti-pattern 1 — Replace with a concrete anti-pattern name

     Replace this scaffold text with the anti-pattern description.

     ---

     ## Rules

     - Replace this scaffold rule with a real constraint or invariant.
     ```

   - **(4e) Record outcome**: `<filename>.md → .claude/skills/<stem>/SKILL.md — scaffolded (format: <format>)`.

5. **Non-qualifying file** (no marker matched):
   Record: `<filename>.md — advisory only (no qualifying signals)`.
   Do NOT create or modify any file.

> **Invariant**: Source files in `commands/` are NEVER deleted, moved, or modified — regardless of scaffold outcome. The scaffold strategy writes only to `PROJECT_CLAUDE_DIR/skills/<stem>/SKILL.md`. No deletion prompt is ever issued for the `commands/` category.

---

##### Pattern: `docs/`

- **Match condition**: Directory named `docs` (case-insensitive)
- **Strategy**: `copy` — per `.md` file
- **Destination**: `PROJECT_ROOT/ai-context/features/<name>.md` for each `*.md` file at the immediate `docs/` level

**Copy procedure** (runs when `docs/` category is confirmed in Step 5.7):

1. List all `.md` files at the **immediate** `docs/` level only (no recursion).
2. Ensure `PROJECT_ROOT/ai-context/features/` directory exists; create it if absent before copying.
3. For each `.md` file:
   - Derive `<name>` = filename including `.md` extension.
   - Destination = `PROJECT_ROOT/ai-context/features/<name>.md`.
   - **If destination exists**: record `<name> — skipped (destination exists)`. Do NOT overwrite.
   - **If destination does not exist**: copy source to destination; record `<name> — copied to ai-context/features/<name>.md`.
4. Source files are NEVER deleted, moved, or modified.

---

##### Pattern: `system/`

- **Match condition**: Directory named `system` (case-insensitive)
- **Strategy**: `append` — route by filename to appropriate `ai-context/` file
- **Routing table**:
  - `architecture.md` → `PROJECT_ROOT/ai-context/architecture.md`
  - `database.md` → `PROJECT_ROOT/ai-context/stack.md`
  - `api-overview.md` → `PROJECT_ROOT/ai-context/stack.md`
  - All other files at the immediate `system/` level → record as `<filename> — no routing rule; skipped`

**Append procedure** (runs when `system/` category is confirmed in Step 5.7):

1. List all files at the **immediate** `system/` level only (no recursion).
2. For each file matched by the routing table:
   - Destination = the mapped `ai-context/` file.
   - **If destination does not exist**: create it with the appended content.
   - **Merge strategy**: append the entire file content to the destination, preceded by the labeled separator:
     `<!-- appended from .claude/system/<filename> YYYY-MM-DD -->`
     (Replace `YYYY-MM-DD` with the current date at apply time.)
   - Record: `<filename> — appended to <destination> (separator added)`.
3. Source files are NEVER deleted, moved, or modified.

---

##### Pattern: `plans/`

- **Match condition**: Directory named `plans` (case-insensitive)
- **Strategy**: `copy` — route by active / archived status
- **Routing**:
  - Active plans → `PROJECT_ROOT/openspec/changes/<plan-name>/`
  - Archived plans → `PROJECT_ROOT/openspec/changes/archive/<plan-name>/`

**Active vs. archived determination**: The skill does NOT apply any heuristic to classify a plan item as active or archived. For **each item** at the immediate `plans/` level, the skill MUST ask the user at apply time:
`Is "<plan-name>" an active plan or an archived plan? (active/archived)`

**Copy procedure** (runs when `plans/` category is confirmed in Step 5.7):

1. List all items at the **immediate** `plans/` level only (no recursion).
2. For each item, prompt the user to classify it as active or archived (per item).
3. Determine destination directory:
   - Active → `PROJECT_ROOT/openspec/changes/<plan-name>/`
   - Archived → `PROJECT_ROOT/openspec/changes/archive/<plan-name>/`
4. **If destination directory already exists**: record `<plan-name> — skipped (destination exists)`. Do NOT overwrite.
5. **If destination directory does not exist**: create the directory; copy the item's contents into it; record `<plan-name> — copied to <destination>`.
6. Source files and directories are NEVER deleted, moved, or modified.

---

##### Pattern: `requirements/`

- **Match condition**: Directory named `requirements` (case-insensitive)
- **Strategy**: `scaffold` — idempotent
- **Destination**: `openspec/changes/<YYYY-MM-DD>-<slug>/proposal.md` — one proposal stub per `.md` file at the immediate `requirements/` level. `<slug>` is derived from the filename stem (filename without the `.md` extension). `<YYYY-MM-DD>` is the current date at apply time.

**Scaffold procedure** (runs when `requirements/` category is confirmed in Step 5.7):

1. List all `.md` files at the **immediate** `requirements/` level only (no recursion into subdirectories).
2. For each `.md` file:
   - Derive `<slug>` = filename stem (case-preserved, e.g. `auth-requirements.md` → `auth-requirements`).
   - Construct scaffold path: `PROJECT_ROOT/openspec/changes/<YYYY-MM-DD>-<slug>/proposal.md`.
   - **If `proposal.md` already exists at that path**: record `<slug> — scaffold skipped (proposal.md already exists)`. Do NOT overwrite.
   - **If `proposal.md` does not exist**: create the directory `openspec/changes/<YYYY-MM-DD>-<slug>/` and write the following minimal scaffold:

     ```markdown
     # Proposal: <slug>

     ## Problem Statement

     <!-- Describe the problem to be solved. -->

     ## Proposed Solution

     <!-- Describe the proposed approach. -->

     ## Success Criteria

     - [ ]
     ```

   - Record: `<slug> — scaffolded to openspec/changes/<date>-<slug>/proposal.md`.

3. Source files are NEVER deleted, moved, or modified.

---

##### Pattern: `sops/`

- **Match condition**: Directory named `sops` (case-insensitive)
- **Strategy**: `user-choice` — per file
- **Destinations**:
  - **Option A**: Append file content as a named section to `PROJECT_ROOT/ai-context/conventions.md`. Section heading: `## <stem>` (filename stem). If `ai-context/conventions.md` does not exist, create it. Append under labeled separator: `<!-- appended from .claude/sops/<filename> YYYY-MM-DD -->`.
  - **Option B**: Copy file to `PROJECT_ROOT/docs/sops/<filename>`. Create `docs/sops/` directory if absent. If destination already exists: record `<filename> — skipped (destination exists)`. Do NOT overwrite.

**User-choice procedure** (runs when `sops/` category is confirmed in Step 5.7):

1. List all `.md` files at the **immediate** `sops/` level only (no recursion).
2. Present the list to the user with both destination options.
3. The user selects per file, or can use global shortcuts:
   - `apply option A to all` — applies Option A to all files in `sops/`
   - `apply option B to all` — applies Option B to all files in `sops/`
4. Execute the selection for each file according to the chosen option.
5. Source files are NEVER deleted, moved, or modified.

---

##### Pattern: `templates/`

- **Match condition**: Directory named `templates` (case-insensitive)
- **Strategy**: `copy`
- **Destination**: `PROJECT_ROOT/docs/templates/<filename>` — one copy per file at the immediate `templates/` level (no recursion into subdirectories of `templates/`).

**Copy procedure** (runs when `templates/` category is confirmed in Step 5.7):

1. List all files at the **immediate** `templates/` level only (no recursion).
2. Ensure `PROJECT_ROOT/docs/templates/` directory exists; create it if absent before copying.
3. For each file:
   - Destination = `PROJECT_ROOT/docs/templates/<filename>`.
   - **If destination exists**: record `<filename> — skipped (destination exists)`. Do NOT overwrite.
   - **If destination does not exist**: copy source to destination; record `<filename> — copied to docs/templates/<filename>`.
4. Source files are NEVER deleted, moved, or modified.

---

##### Pattern: `project.md`

- **Match condition**: Root-level `.md` file named `project.md` (case-insensitive match on the full filename).
- **Strategy**: `section-distribute`
- **Section routing heuristic**: read the file's section headings and route each section to a destination using the following signal lists:

  ```
  STACK_HEADING_SIGNALS    = ["## Tech Stack", "## Stack", "## Dependencies", "## Tools"]
  ARCH_HEADING_SIGNALS     = ["## Architecture", "## System Design", "## Overview"]
  ISSUES_HEADING_SIGNALS   = ["## Known Issues", "## Issues", "## Gotchas", "## Limitations"]
  ```

  - A heading matching any entry in `STACK_HEADING_SIGNALS` → routes that section to `ai-context/stack.md`
  - A heading matching any entry in `ARCH_HEADING_SIGNALS` → routes that section to `ai-context/architecture.md`
  - A heading matching any entry in `ISSUES_HEADING_SIGNALS` → routes that section to `ai-context/known-issues.md`
  - Headings matching no signal list are not routed and not appended to any file.

**Section-distribute procedure** (runs when `project.md` category is confirmed in Step 5.7):

1. Read the file's section headings.
2. For each heading matched by a signal list, extract the section content (from the heading to the next same-level or higher heading).
3. **Per-section user confirmation**: present each matched section's content to the user and request explicit confirmation before appending. Do NOT append any section that the user does not confirm.
4. **Append strategy**: append each confirmed section to the destination file under the labeled separator:
   `<!-- appended from .claude/<filename> YYYY-MM-DD -->`
   (Replace `<filename>` with the actual filename, e.g. `project.md`. Replace `YYYY-MM-DD` with the current date.)
   If the destination file does not exist, create it with the appended content.
5. Source file is NEVER deleted or modified.

---

##### Pattern: `readme.md`

- **Match condition**: Root-level `.md` file named `readme.md` (case-insensitive match on the full filename).
- **Strategy**: `user-choice`
- **Classification**: `LEGACY_MIGRATION` — `readme.md` is NOT classified as `section-distribute` and is NOT subject to heading-signal routing.
- **Destinations**:
  - **Option A**: Append full file content to `PROJECT_ROOT/CLAUDE.md` under the marker `<!-- .claude/readme.md -->`. Create `CLAUDE.md` if absent (unlikely but guarded).
  - **Option B**: Copy `readme.md` to `PROJECT_ROOT/docs/README-claude.md`. Create `docs/` directory if absent.

**Idempotency guard**: Before presenting options to the user, check whether `PROJECT_ROOT/CLAUDE.md` already contains the string `<!-- .claude/readme.md -->`.

- If the marker IS present → record `readme.md — already integrated (skipped)` and skip this pattern entirely. Do NOT present options.
- If the marker is NOT present → proceed to present Option A and Option B.

**User-choice procedure** (runs when `readme.md` category is confirmed in Step 5.7):

See Step 5.7.2b below for the full execution procedure.

---

### Step 3c — Skills Audit

After Step 3b completes, perform a skills audit over the `.claude/skills/` directory.

**Skip condition**: If `PROJECT_CLAUDE_DIR/skills/` does not exist as a directory, skip this step entirely. Do not produce an error.

Initialize the findings list:

```
SKILL_AUDIT_FINDINGS = []
```

**Scope-overlap detection — read the CLAUDE.md Skills Registry:**

1. Read `PROJECT_CLAUDE_DIR/CLAUDE.md`.
2. Locate the Skills Registry section (look for the comment `<!-- Skills Registry` or headings containing `Skills Registry`).
3. Extract all lines matching the pattern `~/.claude/skills/<name>/SKILL.md` (where `<name>` is a non-empty path segment with no slashes).
4. Build `GLOBAL_REGISTRY_NAMES` = set of `<name>` values extracted (case-sensitive stems).

If `PROJECT_CLAUDE_DIR/CLAUDE.md` does not exist or the Skills Registry section cannot be located, treat `GLOBAL_REGISTRY_NAMES` as an empty set (scope-overlap detection produces no findings, but other rules still run).

**Detection loop:**

Enumerate all **immediate subdirectories** of `PROJECT_CLAUDE_DIR/skills/` (one level deep only — do not recurse).

For each subdirectory `D`:

**Detection Rule 1 — scope_overlap (HIGH):**
If `D.name` is present in `GLOBAL_REGISTRY_NAMES` (case-sensitive string equality):

```
SKILL_AUDIT_FINDINGS.append({
  skill_name:   D.name,
  finding_type: "scope_overlap",
  severity:     "HIGH",
  detail:       "also referenced as ~/.claude/skills/" + D.name + "/ in CLAUDE.md Skills Registry"
})
```

**Detection Rule 2 — broken_shell (MEDIUM):**
If `PROJECT_CLAUDE_DIR/skills/D.name/SKILL.md` does NOT exist as a file:

```
SKILL_AUDIT_FINDINGS.append({
  skill_name:   D.name,
  finding_type: "broken_shell",
  severity:     "MEDIUM",
  detail:       "no SKILL.md found in directory"
})
```

**Detection Rule 3 — suspicious_name (LOW):**
If `D.name` does NOT match the kebab-case convention — i.e., it contains at least one of:

- An uppercase letter (`A`–`Z`)
- A space character
- An underscore character (`_`)

```
SKILL_AUDIT_FINDINGS.append({
  skill_name:   D.name,
  finding_type: "suspicious_name",
  severity:     "LOW",
  detail:       "name does not follow kebab-case convention (contains spaces, uppercase letters, or underscores)"
})
```

> **Multiple findings per directory**: all three rules are applied independently to each subdirectory. A single directory may produce multiple `SKILL_AUDIT_FINDINGS` entries — one per rule that fires.

> **SKILL_AUDIT_FINDINGS entry structure:**
>
> | Field          | Type                                                         | Description                                             |
> | -------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
> | `skill_name`   | string                                                       | The immediate subdirectory name under `.claude/skills/` |
> | `finding_type` | `"scope_overlap"` \| `"broken_shell"` \| `"suspicious_name"` | Which detection rule fired                              |
> | `severity`     | `"HIGH"` \| `"MEDIUM"` \| `"LOW"`                            | Severity corresponding to finding type                  |
> | `detail`       | string                                                       | Human-readable explanation of the finding               |
>
> Findings are advisory only — this step NEVER modifies, deletes, or moves any file.

---

### Step 4 — Build and present dry-run plan

Build the reorganization plan from the three categories above.

**If `MISSING_REQUIRED` is empty AND `UNEXPECTED` is empty AND `DOCUMENTATION_CANDIDATES` is empty AND `LEGACY_MIGRATIONS` is empty:**

Output:

```
No reorganization needed — .claude/ already matches the canonical SDD structure.
```

Proceed directly to Step 6 to write the report (no confirmation prompt needed).

**Otherwise**, display the plan in this format:

```
Reorganization Plan for: <PROJECT_CLAUDE_DIR>
─────────────────────────────────────────────

To be created (missing required items):
  + CLAUDE.md    — stub file (5 section headings)
  + skills/      — empty directory

Documentation to migrate → ai-context/:
  → stack.md      → ai-context/stack.md       (copy only — source preserved)
  → notes.md      → ai-context/notes.md       (copy only — source preserved)

  Note: individual files can be excluded before confirmation — list them as
  exclusions when responding to the prompt below.

Legacy migrations (source files offered for deletion after successful migration):
  ~ commands/    — strategy: scaffold — active SKILL.md generation per qualifying .md file
                   Files to scaffold:
                     deploy.md → .claude/skills/deploy/ [format: procedural]
                     auth.md   → [already exists — will skip]
                     misc.md   — non-qualifying (no structured workflow detected)
                   (Source files in commands/ are NEVER deleted or modified.)
  ~ docs/        — strategy: copy — each .md file → ai-context/features/<name>.md
  ~ system/      — strategy: append — architecture.md → ai-context/architecture.md;
                   database.md + api-overview.md → ai-context/stack.md
  ~ plans/       — strategy: copy — active → openspec/changes/<name>/;
                   archived → openspec/changes/archive/<name>/
  ~ requirements/ — strategy: scaffold — openspec/changes/<date>-<slug>/proposal.md per .md file
  ~ sops/        — strategy: user-choice — Option A: ai-context/conventions.md section;
                   Option B: docs/sops/<filename>
  ~ templates/   — strategy: copy — each file → docs/templates/<filename>
  ~ project.md   — strategy: section-distribute → ai-context/stack.md,
                   ai-context/architecture.md, ai-context/known-issues.md
  ~ readme.md    — strategy: user-choice
                   Option A: append full content to CLAUDE.md (marker: <!-- .claude/readme.md -->)
                   Option B: copy to docs/README-claude.md

  Note: each legacy migration category requires explicit per-category confirmation in Step 5.7
  before any write occurs. Source files are offered for deletion after successful migration —
  deletion requires explicit user confirmation. scaffold (commands/) and section-distribute
  strategies are exempt from cleanup prompts. readme.md (user-choice) deletion requires explicit
  confirmation after successful migration only.

Skills audit:
  (Displayed only when SKILL_AUDIT_FINDINGS is non-empty and .claude/skills/ exists)

  | Skill | Finding | Severity |
  |-------|---------|----------|
  | `react-19` | scope_overlap — also referenced as `~/.claude/skills/react-19/` | HIGH |
  | `_draft-auth` | suspicious_name — name does not follow kebab-case convention | LOW |
  | `my-broken-skill` | broken_shell — no SKILL.md found in directory | MEDIUM |

  (When SKILL_AUDIT_FINDINGS is empty: "Skills audit: no issues detected.")
  (When .claude/skills/ was absent: omit the Skills audit section entirely.)

Unexpected items (will be flagged, NOT deleted or moved):
  ! commands/    — not part of canonical SDD .claude/ structure (review manually)

Already correct:
  ✓ hooks/
  ✓ ai-context/
  ✓ openspec/

These items will NOT be deleted or moved — unexpected items receive a warning
comment in the report only.
```

Omit any category that has zero items (applies to all four categories).

**Skills audit rendering rules (applies to the `Skills audit:` section in the plan):**

- If `PROJECT_CLAUDE_DIR/skills/` does NOT exist → omit the `Skills audit:` section entirely from the plan display.
- If `PROJECT_CLAUDE_DIR/skills/` exists AND `SKILL_AUDIT_FINDINGS` is non-empty → render the table with one row per finding.
- If `PROJECT_CLAUDE_DIR/skills/` exists AND `SKILL_AUDIT_FINDINGS` is empty → display: `Skills audit: no issues detected.` (no table).

After displaying the plan, prompt:

```
Apply this plan? (yes/no)
```

Wait for user input before proceeding.

- If the user responds with `yes`, `y`, `proceed`, or `apply` (case-insensitive) → proceed to Step 5.
- If the user responds with `no`, `n`, `cancel`, or `abort`, or provides no answer → output:
  ```
  Reorganization cancelled. No changes were made.
  ```
  Stop. Do not write any files (including the report).

---

### Step 5 — Apply plan (strictly additive)

Apply ONLY the operations listed in the plan. No additional operations.

**5.1 — Create missing `skills/` directory:**

If `skills/` is in `MISSING_REQUIRED`:

- Create an empty directory at `PROJECT_CLAUDE_DIR/skills/`.
- Do NOT place any files inside it.
- Record: `skills/ — directory created`.

**5.2 — Create missing `hooks/` directory:**

If `hooks/` is in `MISSING_REQUIRED` (hooks/ is optional, but if explicitly listed in plan):

- Create an empty directory at `PROJECT_CLAUDE_DIR/hooks/`.
- Record: `hooks/ — directory created`.

**5.3 — Create missing `CLAUDE.md` stub:**

If `CLAUDE.md` is in `MISSING_REQUIRED`:

- Verify `PROJECT_CLAUDE_DIR/CLAUDE.md` does NOT already exist (idempotency guard).
  If it already exists → skip this operation, record as `CLAUDE.md — already exists (skipped)`.
- Write the following minimal stub to `PROJECT_CLAUDE_DIR/CLAUDE.md`:

```markdown
# [Project Name] — Claude Configuration

## Tech Stack

<!-- Add your project tech stack here. -->

## Architecture

<!-- Describe the project architecture here. -->

## Unbreakable Rules

<!-- Add project-specific rules here. -->

## Plan Mode Rules

<!-- Add plan mode rules here. -->

## Skills Registry

<!-- List skills used by this project here.
     Global skills: ~/.claude/skills/<name>/SKILL.md
     Local skills:  .claude/skills/<name>/SKILL.md
     Run /project-setup for full initialization. -->
```

- Record: `CLAUDE.md — stub file created`.

**5.4 — Copy documentation candidates to ai-context/:**

Process each file in `DOCUMENTATION_CANDIDATES`:

**(a) Ensure `PROJECT_ROOT/ai-context/` exists:**
If the directory does not exist, create it before attempting any copy.

**(b) For each file NOT excluded by the user:**

- Check whether the destination (`PROJECT_ROOT/ai-context/<filename>.md`) already exists.
  - If destination **exists**: do not write anything. Record: `<filename>.md — skipped (destination exists — review manually)`. Leave both source and destination untouched.
  - If destination **does not exist**: copy source to destination. After the copy, verify that the source file still exists at `PROJECT_CLAUDE_DIR/<filename>.md`.
    - If source still exists → record: `<filename>.md — copied to ai-context/<filename>.md`.
    - If source no longer exists after copy → record: `<filename>.md — failed — source missing after copy` and do NOT mark as success.
  - On any other copy failure: record `<filename>.md — failed — <error reason>` and continue processing remaining candidates.

**(c) For each file excluded by the user:**

- Do NOT copy or modify the file.
- Record: `<filename>.md — excluded by user`.

**Source preservation invariant**: NEVER delete or modify the source file under any circumstance. The source file at `PROJECT_CLAUDE_DIR/<filename>.md` must exist and be unmodified after this step completes.

**5.5 — Flag unexpected items:**

For each item in `UNEXPECTED`:

- Do NOT touch the file or directory in any way.
- Record it as `<name> — unexpected item flagged in report (not modified)`.

**5.6 — Acknowledge already-correct items:**

For each item in `PRESENT`:

- No operation performed.
- Record it as `<name> — already correct (no change)`.

**5.7 — Apply legacy migrations (per-category confirmation gates):**

Process categories in strategy execution order: scaffold (commands/) → section-distribute (project.md) → user-choice (readme.md) → copy → append → scaffold (requirements/) → user-choice (sops/).

For each category in `LEGACY_MIGRATIONS` (grouped by strategy, processed in the order above):

1. Present the full list of files in the category and their proposed destinations.
2. Prompt: `Apply <category> migrations? (yes/no/all)`
3. If the user responds `no`: skip the category entirely; record `<category> — skipped by user (no files written)`. Do NOT write any files for this category.
4. If the user responds `yes` or `all`: apply the strategy for this category (see sub-steps below). The `all` response also confirms all remaining unprocessed categories — no further per-category prompts are required for those.

**5.7.1 — scaffold strategy (`commands/`):**

1. List all `.md` files at the **immediate** `commands/` level (no recursion into subdirectories).
2. If no `.md` files are found at the immediate level:
   Output: `commands/ — no .md files found at immediate level; nothing to scaffold`
   Stop processing this category.
3. For each `.md` file found, apply the **4 qualifying markers** (any one is sufficient to qualify):
   - **(a) Step-numbered sections**: the file contains lines matching `### Step N`, `- Step N`, or `N.` where N is a number
   - **(b) Trigger / invocation patterns**: the file contains lines starting with `/command-name` or lines containing `**Triggers**` or `trigger:`
   - **(c) Process headings**: the file contains a section heading that is exactly `## Process`, `## Steps`, `## How to`, or `## Instructions`
   - **(d) Filename-stem keyword match**: the file's stem (case-insensitive) matches one of: `deploy`, `rollback`, `setup`, `onboard`, `audit`, `install`, `release`, `build`, `migrate`, `sync`
4. **Qualifying file** (at least one marker matched):
   - **(4a) Derive skill name**: extract the filename stem; normalize to kebab-case (lowercase, spaces and underscores replaced with hyphens). `<stem>` = normalized stem.
   - **(4b) Infer format type** using the 4-signal heuristic (first match wins; precedence: anti-pattern > reference > procedural):
     - If the source file contains a heading starting with `## Anti-patterns` → `anti-pattern`
     - Else if the source file contains a heading starting with `## Patterns` or `## Examples` → `reference`
     - Otherwise (step-numbered sections, process headings, trigger patterns, keyword stem, or no signals) → `procedural` (default)
   - **(4c) Idempotency guard**: check whether `PROJECT_CLAUDE_DIR/skills/<stem>/SKILL.md` already exists.
     - **If it exists**: record `<filename>.md — already exists (not overwritten). Review .claude/skills/<stem>/SKILL.md manually.` Skip to the next file; do NOT write anything.
     - **If it does not exist**: proceed to 4d.
   - **(4d) Generate SKILL.md skeleton** based on inferred format type. Create directory `PROJECT_CLAUDE_DIR/skills/<stem>/` if absent. Write the appropriate skeleton to `PROJECT_CLAUDE_DIR/skills/<stem>/SKILL.md`:

     **For `procedural` format:**

     ```markdown
     ---
     name: <stem>
     description: >
       <stem> — migrated from .claude/commands/<filename>.md
     format: procedural
     ---

     # <stem>

     > <stem> procedure.

     **Triggers**: <stem>

     ---

     ## Process

     <source file content copied here>

     ---

     ## Rules

     - <!-- Add rules and constraints here. -->
     ```

     **For `reference` format:**

     ```markdown
     ---
     name: <stem>
     description: >
       <stem> — migrated from .claude/commands/<filename>.md
     format: reference
     ---

     # <stem>

     > <stem> reference.

     **Triggers**: <stem>

     ---

     ## Patterns

     <source file content copied here>

     ---

     ## Rules

     - <!-- Add rules and constraints here. -->
     ```

     **For `anti-pattern` format:**

     ```markdown
     ---
     name: <stem>
     description: >
       <stem> — migrated from .claude/commands/<filename>.md
     format: anti-pattern
     ---

     # <stem>

     > <stem> anti-patterns.

     **Triggers**: <stem>

     ---

     ## Anti-patterns

     <source file content copied here>

     ---

     ## Rules

     - <!-- Add rules and constraints here. -->
     ```

   - **(4e) Record outcome**: `<filename>.md — scaffolded to .claude/skills/<stem>/SKILL.md (format: <format>)`.

5. **Non-qualifying file** (no marker matched):
   Record: `<filename>.md — non-qualifying (no structured workflow detected). Recommend manual archival.`
   Do NOT create or modify any file.

> **Invariant**: Source files in `commands/` are NEVER deleted, moved, or modified — regardless of scaffold outcome. No deletion prompt is ever issued for the `commands/` category.

**5.7.2 — section-distribute strategy (`project.md`):**

1. Read the file's section headings.
2. For each heading, apply **emoji normalization** before comparing against any signal list:
   - Strip leading Unicode emoji characters (including all Unicode emoji ranges and variation selectors) and any following whitespace from the heading text.
   - Use the normalized form for all signal-list comparisons.
   - The original heading text is preserved — the source file is NEVER modified.
   - Any per-section confirmation prompt shown to the user MUST display the original heading text (including emoji prefix), not the normalized form.
3. Map each heading (using normalized text) to a destination file using the signal lists:
   - `STACK_HEADING_SIGNALS = ["## Tech Stack", "## Stack", "## Dependencies", "## Tools"]` → `ai-context/stack.md`
   - `ARCH_HEADING_SIGNALS = ["## Architecture", "## System Design", "## Overview"]` → `ai-context/architecture.md`
   - `ISSUES_HEADING_SIGNALS = ["## Known Issues", "## Issues", "## Gotchas", "## Limitations"]` → `ai-context/known-issues.md`
   - Headings matching no signal list (even after normalization) are not routed.
4. **Per-section user confirmation**: for each mapped section, present the section content to the user (with original heading text including any emoji) and request explicit confirmation before appending. Do NOT append any section the user does not confirm.
5. **Append strategy**: append each confirmed section to the destination file under the labeled separator:
   `<!-- appended from .claude/<filename> YYYY-MM-DD -->`
   (Replace `<filename>` with the actual filename, e.g. `project.md`. Replace `YYYY-MM-DD` with the current date.)
   If the destination file does not exist, create it with the appended content.
6. Source file is NEVER deleted or modified.
7. **Advisory — zero matches**: after processing all headings, if zero headings matched any signal list (even after emoji normalization), output:
   `Advisory: no headings in <filename> matched any signal list after emoji normalization — file content was not distributed. Recommend manual migration.`
   (Replace `<filename>` with the actual filename.)

**5.7.2b — user-choice strategy (`readme.md`):**

This step runs only when `readme.md` is present in `LEGACY_MIGRATIONS`.

1. **Idempotency guard**: Check whether `PROJECT_ROOT/CLAUDE.md` already contains the string `<!-- .claude/readme.md -->`.
   - **If the marker IS present**: record `readme.md — already integrated (skipped)`. Skip all remaining sub-steps. Do NOT present any options to the user.
   - **If the marker is NOT present**: proceed to step 2.

2. Present the following prompt to the user:

   ```
   readme.md migration — choose an option:
     Option A: Append full content to PROJECT_ROOT/CLAUDE.md
               (marker: <!-- .claude/readme.md --> will be added)
     Option B: Copy to PROJECT_ROOT/docs/README-claude.md
     Skip: leave readme.md in place (manual review recommended)
   ```

3. **If user selects Option A**:
   - **Idempotency guard** (double-check at write time): re-verify that `PROJECT_ROOT/CLAUDE.md` does NOT already contain `<!-- .claude/readme.md -->`. If it does → record `readme.md — already integrated (skipped)` and stop.
   - Append the following block to `PROJECT_ROOT/CLAUDE.md`:
     ```
     <!-- .claude/readme.md -->
     <full content of readme.md>
     ```
     (If `PROJECT_ROOT/CLAUDE.md` does not exist, create it before appending.)
   - Record: `readme.md — appended to CLAUDE.md (Option A)`.

4. **If user selects Option B**:
   - Ensure `PROJECT_ROOT/docs/` directory exists; create it if absent.
   - Copy `readme.md` to `PROJECT_ROOT/docs/README-claude.md`.
   - **If `PROJECT_ROOT/docs/README-claude.md` already exists**: record `readme.md — skipped (docs/README-claude.md already exists)`. Do NOT overwrite.
   - **If it does not exist**: copy and record `readme.md — copied to docs/README-claude.md (Option B)`.

5. **If user skips**: record `readme.md — skipped by user. Recommend manual review.` Do NOT write any file.

6. **Source preservation**: The source file `.claude/readme.md` is NEVER deleted or modified as part of this step. Cleanup follows the standard cleanup prompt flow only when the migration was successful (Option A or Option B applied) AND the user explicitly confirms cleanup.

7. **Cleanup prompt** (only when migration was successful — outcome recorded as "appended" or "copied"):

   ```
   Cleanup available for .claude/readme.md:
     Will be deleted (successfully migrated): readme.md
   Delete source file .claude/readme.md? (yes/no)
   ```

   - If user responds `yes`: delete `PROJECT_CLAUDE_DIR/readme.md`. Record `.claude/readme.md — deleted`.
   - If user responds `no`: record `readme.md — cleanup declined by user`.

> **Invariant**: Source file `.claude/readme.md` is NEVER deleted unless the migration step was successful AND the user explicitly confirmed the cleanup prompt above.

**5.7.3 — copy strategy (`docs/` and `templates/`):**

For **`docs/`**:

1. List all `.md` files at the **immediate** `docs/` level only (no recursion).
2. Ensure `PROJECT_ROOT/ai-context/features/` directory exists; create it if absent before copying.
3. For each `.md` file:
   - Destination = `PROJECT_ROOT/ai-context/features/<name>.md`.
   - **If destination exists**: record `<name>.md — skipped (destination exists)`. Do NOT overwrite.
   - **If destination does not exist**: copy source to destination; record `<name>.md — copied to ai-context/features/<name>.md`.
4. Source files are NEVER deleted, moved, or modified.

For **`templates/`**:

1. List all files at the **immediate** `templates/` level only (no recursion).
2. Ensure `PROJECT_ROOT/docs/templates/` directory exists; create it if absent before copying.
3. For each file:
   - Destination = `PROJECT_ROOT/docs/templates/<filename>`.
   - **If destination exists**: record `<filename> — skipped (destination exists)`. Do NOT overwrite.
   - **If destination does not exist**: copy source to destination; record `<filename> — copied to docs/templates/<filename>`.
4. Source files are NEVER deleted, moved, or modified.

**5.7.3-cleanup — source file cleanup after copy strategy (`docs/` and `templates/`):**

For each category processed by 5.7.3 (`docs/` and `templates/`):

1. **Guard — strategy eligibility**: copy strategy is eligible for cleanup. Proceed.
2. **Guard — success count**: count files with outcome "copied to ...". If count = 0 (all files were skipped or failed), skip cleanup for this category — do NOT present a prompt.
3. **Build lists**:
   - `WILL_DELETE` = files whose outcome was "copied to ..." (successful migration)
   - `WILL_PRESERVE` = files whose outcome was "skipped (destination exists)", "failed", or any non-success outcome
4. **Present both lists to the user**:
   ```
   Cleanup available for .claude/<category>/:
     Will be deleted (successfully migrated): <filename>, <filename>, ...
     Will be preserved (skipped — destination exists): <filename>, ...
   ```
5. **Prompt**: `Delete source files from .claude/<category>/? (yes/no)`
6. **If user responds `yes`**: delete each file in `WILL_DELETE` from its source path under `PROJECT_CLAUDE_DIR/<category>/`. Record each deletion as `.claude/<category>/<filename> — deleted`. Do NOT delete the parent directory.
7. **If user responds `no`**: record `<category>/ — cleanup declined by user`. Do NOT delete any file.

> **Invariant**: Only files in `WILL_DELETE` (confirmed successful migration) may be deleted. `WILL_PRESERVE` files are NEVER deleted regardless of user input.

**5.7.4 — append strategy (`system/`):**

1. List all files at the **immediate** `system/` level only (no recursion).
2. Apply routing table:
   - `architecture.md` → `PROJECT_ROOT/ai-context/architecture.md`
   - `database.md` → `PROJECT_ROOT/ai-context/stack.md`
   - `api-overview.md` → `PROJECT_ROOT/ai-context/stack.md`
   - All other files → record as `<filename> — no routing rule; skipped`
3. For each file matched by the routing table:
   - **If destination does not exist**: create it with the appended content.
   - **Append block**: append the entire file content to the destination, preceded by:
     `<!-- appended from .claude/system/<filename> YYYY-MM-DD -->`
     (Replace `YYYY-MM-DD` with the current date at apply time.)
   - Record: `<filename> — appended to <destination> (separator added)`.
4. Source files are NEVER deleted, moved, or modified.

**5.7.4-cleanup — source file cleanup after append strategy (`system/`):**

1. **Guard — strategy eligibility**: append strategy is eligible for cleanup. Proceed.
2. **Guard — success count**: count files with outcome "appended to ...". If count = 0, skip cleanup — do NOT present a prompt.
3. **Build lists**:
   - `WILL_DELETE` = files whose outcome was "appended to ... (separator added)"
   - `WILL_PRESERVE` = files whose outcome was "no routing rule; skipped" or any non-success outcome
4. **Present both lists to the user**:
   ```
   Cleanup available for .claude/system/:
     Will be deleted (successfully appended): <filename>, ...
     Will be preserved (no routing rule or skipped): <filename>, ...
   ```
5. **Prompt**: `Delete source files from .claude/system/? (yes/no)`
6. **If user responds `yes`**: delete each file in `WILL_DELETE` from `PROJECT_CLAUDE_DIR/system/<filename>`. Record each deletion as `.claude/system/<filename> — deleted`. Do NOT delete the `system/` directory itself.
7. **If user responds `no`**: record `system/ — cleanup declined by user`. Do NOT delete any file.

> **Invariant**: Only files in `WILL_DELETE` (confirmed successful append) may be deleted. `WILL_PRESERVE` files are NEVER deleted.

**5.7.5 — scaffold strategy (`requirements/`):**

1. List all `.md` files at the **immediate** `requirements/` level only (no recursion).
2. For each `.md` file:
   - Derive `<slug>` = filename stem (filename without the `.md` extension).
   - Construct scaffold path: `PROJECT_ROOT/openspec/changes/<YYYY-MM-DD>-<slug>/proposal.md` (use current date).
   - **If `proposal.md` already exists at that path**: record `<slug> — scaffold skipped (proposal.md already exists)`. Do NOT overwrite.
   - **If `proposal.md` does not exist**: create the directory `openspec/changes/<YYYY-MM-DD>-<slug>/` and write the following minimal scaffold:

     ```markdown
     # Proposal: <slug>

     ## Problem Statement

     <!-- Describe the problem to be solved. -->

     ## Proposed Solution

     <!-- Describe the proposed approach. -->

     ## Success Criteria

     - [ ]
     ```

   - Record: `<slug> — scaffolded to openspec/changes/<date>-<slug>/proposal.md`.

3. Source files are NEVER deleted, moved, or modified.

**5.7.5-cleanup — source file cleanup after scaffold strategy (`requirements/`):**

1. **Guard — strategy eligibility**: scaffold strategy is eligible for cleanup. Proceed.
2. **Guard — success count**: count files with outcome "scaffolded to ...". If count = 0, skip cleanup — do NOT present a prompt.
3. **Build lists**:
   - `WILL_DELETE` = files whose outcome was "scaffolded to ..."
   - `WILL_PRESERVE` = files whose outcome was "scaffold skipped (proposal.md already exists)" or any non-success outcome
4. **Present both lists to the user**:
   ```
   Cleanup available for .claude/requirements/:
     Will be deleted (successfully scaffolded): <filename>.md, ...
     Will be preserved (scaffold skipped — proposal already exists): <filename>.md, ...
   ```
5. **Prompt**: `Delete source files from .claude/requirements/? (yes/no)`
6. **If user responds `yes`**: delete each file in `WILL_DELETE` from `PROJECT_CLAUDE_DIR/requirements/<filename>`. Record each deletion as `.claude/requirements/<filename> — deleted`. Do NOT delete the `requirements/` directory itself.
7. **If user responds `no`**: record `requirements/ — cleanup declined by user`. Do NOT delete any file.

> **Invariant**: Only files in `WILL_DELETE` (confirmed successful scaffold) may be deleted. `WILL_PRESERVE` files are NEVER deleted.

**5.7.6 — user-choice strategy (`sops/`):**

1. List all `.md` files at the **immediate** `sops/` level only (no recursion).
2. Present the list to the user with both destination options:
   - **Option A**: Append file content as a named section (`## <stem>`) to `ai-context/conventions.md` under labeled separator `<!-- appended from .claude/sops/<filename> YYYY-MM-DD -->`; create `ai-context/conventions.md` if absent.
   - **Option B**: Copy file to `docs/sops/<filename>`; create `docs/sops/` directory if absent; skip if destination exists and record.
3. The user selects per file, or can use global shortcuts:
   - `apply option A to all` — applies Option A to all files in `sops/`
   - `apply option B to all` — applies Option B to all files in `sops/`
4. Execute the selection for each file according to the chosen option. Record each operation outcome.
5. Source files are NEVER deleted, moved, or modified.

**5.7.6-cleanup — source file cleanup after user-choice strategy (`sops/`):**

1. **Guard — strategy eligibility**: user-choice strategy is eligible for cleanup. Proceed.
2. **Guard — success count**: count files with outcome "copied to ..." (Option B) or "appended to ..." (Option A). If count = 0, skip cleanup — do NOT present a prompt.
3. **Build lists**:
   - `WILL_DELETE` = files whose outcome was "copied to ..." or "appended to ..."
   - `WILL_PRESERVE` = files whose outcome was "skipped (destination exists)" or any non-success outcome
4. **Present both lists to the user**:
   ```
   Cleanup available for .claude/sops/:
     Will be deleted (successfully processed): <filename>.md, ...
     Will be preserved (skipped — destination exists): <filename>.md, ...
   ```
5. **Prompt**: `Delete source files from .claude/sops/? (yes/no)`
6. **If user responds `yes`**: delete each file in `WILL_DELETE` from `PROJECT_CLAUDE_DIR/sops/<filename>`. Record each deletion as `.claude/sops/<filename> — deleted`. Do NOT delete the `sops/` directory itself.
7. **If user responds `no`**: record `sops/ — cleanup declined by user`. Do NOT delete any file.

> **Invariant**: Only files in `WILL_DELETE` (confirmed successful user-choice migration) may be deleted. `WILL_PRESERVE` files are NEVER deleted.

**5.7.7 — copy strategy (`plans/`):**

1. List all items at the **immediate** `plans/` level only (no recursion).
2. For each item, present it to the user and ask:
   `Is "<plan-name>" an active plan or an archived plan? (active/archived)`
3. Determine destination directory:
   - Active → `PROJECT_ROOT/openspec/changes/<plan-name>/`
   - Archived → `PROJECT_ROOT/openspec/changes/archive/<plan-name>/`
4. **If destination directory already exists**: record `<plan-name> — skipped (destination exists)`. Do NOT overwrite.
5. **If destination directory does not exist**: create the directory; copy the item's contents into it; record `<plan-name> — copied to <destination>`.
6. Source files and directories are NEVER deleted, moved, or modified.

**5.7.7-cleanup — source file cleanup after copy strategy (`plans/`):**

1. **Guard — strategy eligibility**: copy strategy is eligible for cleanup. Proceed.
2. **Guard — success count**: count items with outcome "copied to ...". If count = 0 (all items were skipped), skip cleanup — do NOT present a prompt.
3. **Build lists**:
   - `WILL_DELETE` = items whose outcome was "copied to ..." (successful migration)
   - `WILL_PRESERVE` = items whose outcome was "skipped (destination exists)" or any non-success outcome
4. **Present both lists to the user**:
   ```
   Cleanup available for .claude/plans/:
     Will be deleted (successfully migrated): <plan-name>, <plan-name>, ...
     Will be preserved (skipped — destination exists): <plan-name>, ...
   ```
5. **Prompt**: `Delete source files from .claude/plans/? (yes/no)`
6. **If user responds `yes`**: delete each item in `WILL_DELETE` from `PROJECT_CLAUDE_DIR/plans/<plan-name>`. Record each deletion as `.claude/plans/<plan-name> — deleted`. Do NOT delete the parent `plans/` directory.
7. **If user responds `no`**: record `plans/ — cleanup declined by user`. Do NOT delete any file.

> **Invariant**: Only items in `WILL_DELETE` (confirmed successful migration) may be deleted. `WILL_PRESERVE` items are NEVER deleted regardless of user input.

---

### Step 6 — Write report

Write `claude-organizer-report.md` to `PROJECT_CLAUDE_DIR`. Overwrite any previous file.

Use this format:

```markdown
# Claude Organizer Report

Run date: <YYYY-MM-DD>
Project root: <PROJECT_ROOT>
Target: <PROJECT_CLAUDE_DIR>
Summary: <N> item(s) created, <N> documentation file(s) copied, <N> legacy migration(s) applied, <N> unexpected item(s) flagged, <N> already correct

---

## Plan Executed

### Created

<!-- List items created, or state "Nothing to create — no required items were missing." -->

- `skills/` — empty directory created
- `CLAUDE.md` — stub file created with 5 section headings (Tech Stack, Architecture, Unbreakable Rules, Plan Mode Rules, Skills Registry)

> CLAUDE.md stub note: the file contains the 5 required section headings only.
> Populate this file with project-specific SDD configuration.
> Run /project-setup for full initialization.

### Documentation copied to ai-context/

<!-- Omit this subsection entirely when DOCUMENTATION_CANDIDATES was empty for the run. -->
<!-- List each candidate with its outcome: -->

- `stack.md` — copied to ai-context/stack.md
- `architecture.md` — skipped (destination exists — review manually)
- `notes.md` — excluded by user

### Legacy migrations

<!-- Omit this subsection entirely when LEGACY_MIGRATIONS was empty for the run. -->
<!-- List each legacy category processed with per-file outcome lines. -->
<!-- Valid outcome labels: applied, skipped, advisory, non-qualifying, user-skipped -->

**commands/** (strategy: scaffold):

- `deploy.md` — scaffolded to .claude/skills/deploy/SKILL.md (format: procedural)
- `auth.md` — already exists (not overwritten). Review .claude/skills/auth/SKILL.md manually.
- `misc.md` — non-qualifying (no structured workflow detected). Recommend manual archival.

**docs/** (strategy: copy):

- `auth.md` — copied to ai-context/features/auth.md
- `payments.md` — skipped (destination exists)

**system/** (strategy: append):

- `architecture.md` — appended to ai-context/architecture.md (separator added)
- `database.md` — appended to ai-context/stack.md (separator added)

**requirements/** (strategy: scaffold):

- `auth-requirements` — scaffolded to openspec/changes/2026-03-04-auth-requirements/proposal.md

**sops/** (strategy: user-choice):

- `deployment.md` — copied to docs/sops/deployment.md (Option B)

**templates/** (strategy: copy):

- `prd-template.md` — copied to docs/templates/prd-template.md

**project.md** (strategy: section-distribute):

- `## Tech Stack` section — appended to ai-context/stack.md
- `## Architecture` section — appended to ai-context/architecture.md

**readme.md** (strategy: user-choice):

<!-- Omit this block entirely when readme.md was absent from the project's .claude/ for the run. -->
<!-- One of the following outcome lines applies: -->
<!-- - readme.md — appended to CLAUDE.md (Option A) -->
<!-- - readme.md — copied to docs/README-claude.md (Option B) -->
<!-- - readme.md — skipped by user. Recommend manual review. -->
<!-- - readme.md — already integrated (skipped) -->

- `readme.md` — appended to CLAUDE.md (Option A)

<!-- Source-preservation footer — CONDITIONAL:
     - When NO files were deleted: display the preservation note below.
     - When files WERE deleted: omit the preservation note; the "Deleted from .claude/" subsection below serves as the deletion summary. -->

> All source files in legacy categories were preserved — no files were deleted or moved

### readme.md migration

<!-- Omit this subsection entirely when readme.md was absent from the project's .claude/ for the run. -->
<!-- One of the following outcome lines applies: -->
<!-- Valid outcome labels: appended to CLAUDE.md (Option A), copied to docs/README-claude.md (Option B), skipped by user, already integrated (skipped) -->

- `readme.md` — appended to CLAUDE.md (Option A)

### Commands scaffolded

<!-- Omit this subsection entirely when commands/ was absent from the project's .claude/ for the run. -->
<!-- List per-file scaffold outcomes using the labels below. -->
<!-- Valid outcome labels: scaffolded (format: <type>), [already exists — not overwritten], advisory only (no qualifying signals) -->

- `deploy.md` — scaffolded to .claude/skills/deploy/SKILL.md (format: procedural)
- `misc.md` — advisory only (no qualifying signals). Recommend manual archival.
- `auth.md` — [already exists — not overwritten]. Review .claude/skills/auth/SKILL.md manually.

### Skills audit

<!-- Omit this subsection entirely when .claude/skills/ was absent for the run. -->
<!-- When SKILL_AUDIT_FINDINGS is non-empty: render table below. -->
<!-- When SKILL_AUDIT_FINDINGS is empty: write "No issues detected in .claude/skills/." -->

| Skill             | Finding                                                                                                           | Severity |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- | -------- |
| `react-19`        | scope_overlap — also referenced as `~/.claude/skills/react-19/`                                                   | HIGH     |
| `_draft-auth`     | suspicious_name — name does not follow kebab-case convention (contains spaces, uppercase letters, or underscores) | LOW      |
| `my-broken-skill` | broken_shell — no SKILL.md found in directory                                                                     | MEDIUM   |

> Findings are advisory only. No files were deleted or modified as part of skills audit.
> Remediate scope_overlap findings by removing the local copy or de-registering the global path from CLAUDE.md.

### Deleted from .claude/

<!-- Omit this subsection entirely when no cleanup prompts were presented during the run. -->
<!-- List each deleted file and each declined cleanup category. -->

- `.claude/docs/auth.md` — deleted
- `templates/ — cleanup declined by user`

### Unexpected items (not modified)

<!-- List unexpected items, or state "None." -->

- `commands/` — This item is not part of the canonical SDD .claude/ structure.
  Review manually — it was NOT deleted or moved.

### Already correct

<!-- List items that were already present and expected, or state "None." -->

- `hooks/`
- `ai-context/`
- `openspec/`

---

## Recommended Next Steps

<!-- Conditional content — include only the applicable items: -->

1. Review the unexpected item(s) listed above — if intentional, document them in
   .claude/CLAUDE.md; if not, remove them manually.
2. Populate the created stub files with project-specific content.
3. Review skipped documentation files — a file was skipped because its destination in
   ai-context/ already exists. Compare source and destination manually and merge if needed.
4. Project .claude/ structure is now aligned with the canonical SDD layout.

<!-- Legacy migration conditional guidance — include only when the condition was true for this run: -->
<!-- If commands/ scaffold was run: -->

5. Review the commands/ scaffold outcomes above — check generated .claude/skills/<name>/SKILL.md
files and populate content. For files already existing (not overwritten), compare and merge manually.
<!-- If section-distribute applied to project.md or readme.md: -->
6. Review the distributed sections in the destination ai-context/ files — verify content is
correctly placed.
<!-- If append applied to system/: -->
7. Review the appended content in the ai-context/ destination file(s) — merge or deduplicate
manually if the appended section overlaps with existing content.
<!-- If scaffold produced proposals from requirements/: -->
8. Populate the scaffold proposals in openspec/changes/ before running /sdd-apply.
<!-- If sops/ was processed: -->
9. Verify the conventions section or docs/sops/ directory was correctly populated.

<!-- For a no-op run where nothing was missing: -->
<!-- No action required — .claude/ is already canonical. -->

---

> This file is a runtime artifact. Add `.claude/claude-organizer-report.md` to `.gitignore`
> to prevent accidental commits.
```

After writing the report, emit:

```
Report written to: <PROJECT_CLAUDE_DIR>/claude-organizer-report.md
```

Use the expanded absolute path (no tilde or relative segments).

---

## Rules

1. **Target is `PROJECT_ROOT/.claude/` only — NEVER `~/.claude/`.**
   This skill MUST NOT be invoked against the user-level runtime directory. If the resolved
   `PROJECT_CLAUDE_DIR` matches `~/.claude/`, the skill MUST exit immediately without changes.

2. **Apply step is strictly additive.**
   Only `mkdir` for missing directories and write stubs for missing files. No delete, move,
   rename, or overwrite operations are permitted under any circumstances. Existing files and
   directories are never touched, regardless of content.

3. **User confirmation gate MUST NOT be skipped.**
   The plan MUST be presented in full before any file write occurs. The skill MUST pause and
   wait for explicit user confirmation. If the user does not confirm affirmatively, the skill
   exits without writing any files (including the report).

4. **Canonical expected item set MUST remain consistent with `claude-folder-audit` Check P8.**
   The inline expected set defined in Step 3 is the single source of truth for this skill.
   Whenever `claude-folder-audit` Check P8 expected items are updated, this skill's inline
   set MUST be updated in sync to prevent false-positive MEDIUM findings.

5. **Source files MUST NOT be deleted without BOTH conditions being true:**
   **(a)** The file was successfully migrated (copied, appended, scaffolded, or user-choice applied) AND **(b)** the user explicitly confirmed the deletion prompt for that category.
   The `scaffold` strategy for `commands/` and the `section-distribute` strategy (`project.md`) are permanently exempt from cleanup prompts — their source files are unconditionally preserved. The `user-choice` strategy for `readme.md` offers cleanup only after successful migration AND explicit user confirmation.
   Any file whose migration outcome was "skipped", "failed", or "excluded" MUST NOT be offered for deletion regardless of user input.

6. **Unexpected, unsupported, or ambiguous items remain advisory-first.**
   If an observed item does not map cleanly to the canonical expected set, a supported legacy strategy, or a safe additive migration path, the organizer MUST report it for manual review instead of inventing a mutation.

7. **Skills audit does not expand organizer mutation scope.**
   Findings from `SKILL_AUDIT_FINDINGS` are diagnostic only — even HIGH-severity findings such as scope overlap MUST NOT trigger automatic rewrites, deletions, or relocations under `.claude/skills/`.

8. **Cleanup deletion is a follow-up opt-in step, not core organizer behavior.**
   The organizer's kernel ends at successful additive migration and report writing. Any deletion prompt is a post-migration choice applied only to explicitly eligible files after explicit user confirmation.
