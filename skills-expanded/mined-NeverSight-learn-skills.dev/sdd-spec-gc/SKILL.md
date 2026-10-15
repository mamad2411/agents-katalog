---
name: sdd-spec-gc
description: >
  Audits master specs for PROVISIONAL, ORPHANED_REF, CONTRADICTORY, SUPERSEDED, and DUPLICATE
  requirements. Presents a dry-run report, requires user confirmation, then removes confirmed
  candidates and records changes in the spec and changelog.
  Trigger: /sdd-spec-gc <domain>, /sdd-spec-gc --all, spec garbage collection, clean up stale specs.
format: procedural
---

# sdd-spec-gc

> Spec garbage collection: audit master specs for stale requirements and remove confirmed candidates.

**Triggers**: `/sdd-spec-gc <domain>`, `/sdd-spec-gc --all`, spec garbage collection, clean up stale specs, remove obsolete requirements

---

## Purpose

Over time, master specs accumulate stale requirements: provisional items that were never finalized, requirements referencing artifacts that no longer exist, contradictory constraints from multiple refactors, and duplicates introduced across changes. `sdd-spec-gc` identifies these candidates, presents them for user review, and removes confirmed items while preserving all other spec content.

**Run cadence**: every 5–10 archived SDD changes, or whenever specs feel stale.

---

## Process

### Step 0a — Load project context

This step is **non-blocking**: any failure MUST produce at most an INFO-level note.

1. Read `ai-context/stack.md` — tech stack, key tools
2. Read `ai-context/architecture.md` — architectural decisions
3. Read `ai-context/conventions.md` — naming patterns
4. Read project `CLAUDE.md` — governance and unbreakable rules; extract governance log line:
   `Governance loaded: [N] unbreakable rules, tech stack: [language], intent classification: [enabled|disabled]`

For each file: if absent, log `INFO: [filename] not found — proceeding without it.`

---

### Step 1 — Discovery: resolve domain list

**Single-domain mode** (`/sdd-spec-gc <domain>`):

1. Check if `openspec/specs/<domain>/spec.md` exists
2. If yes: proceed with that single domain
3. If no: surface error `"Domain '<domain>' not found in openspec/specs/"`, list available domains from `openspec/specs/index.yaml` or directory listing, then exit

**All-domains mode** (`/sdd-spec-gc --all`):

1. If `openspec/specs/index.yaml` exists: read the index and extract the canonical domain list
2. If `openspec/specs/index.yaml` is absent: scan `openspec/specs/` directory and treat each subdirectory as a domain
3. Proceed with the full domain list

**Active change guard**: before scanning, check `openspec/changes/` for any active (non-archived) change directories that contain `specs/<domain>/spec.md`. If a domain's delta spec is in an active change, log `INFO: Domain <domain> has active delta spec in openspec/changes/ — master spec may be updated soon. Proceeding with scan.` (non-blocking; user decides).

---

### Step 2 — Candidate detection

For each domain in the resolved list, read `openspec/specs/<domain>/spec.md` and scan each **requirement block** (from `### Requirement:` heading to the next `### Requirement:` heading or end of file) for the following patterns:

#### PROVISIONAL
Requirement text contains any of:
`"provisional"`, `"temporary"`, `"will be replaced"`, `"pending "`, `"when X is ready"`, `"TODO"`, `"scaffold"`, `"placeholder"`

#### ORPHANED_REF
Requirement text references a named artifact (file, function, type, component) that appears to no longer exist in the codebase.

Detection procedure:
1. Extract potential artifact references: patterns like `\`<name>\``, `<Name>.ts`, `use<Name>`, `<Name>Hook`, `<Name>Service`, `<Name>Type`
2. For each extracted name: run a best-effort codebase search (grep/ripgrep from project root)
3. If search finds no match → candidate for ORPHANED_REF; flag as `UNCERTAIN`
4. If search times out or fails → mark as `UNCERTAIN` (do not remove automatically)
5. UNCERTAIN items are included in the report but suggestion reads "REVIEW for removal" not "REMOVE"

#### SUPERSEDED
A later requirement in the same spec explicitly contradicts or replaces this one. Look for language like `"supersedes"`, `"replaces"`, `"instead of"`, or two requirements expressing mutually exclusive constraints.

#### DUPLICATE
Two requirements in the same spec express the same constraint with different wording. Look for requirements where the core constraint (must/must not + subject) is semantically identical.

#### CONTRADICTORY
Two requirements in the same spec cannot both be satisfied. Look for requirements where one requires X and another requires NOT X (or requires Y where Y is incompatible with X).

**If no candidates found** for a domain: record `0 candidates found` for that domain and continue.

---

### Step 3 — Present dry-run report

Produce a Markdown report. **No files are modified at this step.**

```markdown
## Spec GC Report — openspec/specs/<domain>/spec.md

### PROVISIONAL ([N] found)
- **[Requirement title or REQ-N]**: "[text excerpt]"
  Detection: [keyword found, e.g., "contains 'provisional'"]
  → Suggestion: REMOVE

### ORPHANED_REF ([N] found)
- **[Requirement title or REQ-N]**: references `[artifact-name]`
  Detection: Codebase search did not find `[artifact-name]`
  Status: UNCERTAIN
  → Suggestion: REVIEW for removal

### SUPERSEDED ([N] found)
- **[Requirement title or REQ-N]**: "[text excerpt]"
  Detection: Contradicts [later requirement title]
  → Suggestion: REMOVE

### DUPLICATE ([N] found)
- **[Requirement title or REQ-N]**: "[text excerpt]"
  Detection: Same constraint as [other requirement title]
  → Suggestion: REMOVE

### CONTRADICTORY ([N] found)
- **[Requirement title or REQ-N]**: "[text excerpt]"
  Detection: Conflicts with [other requirement title]
  → Suggestion: REVIEW

Total: [N] candidates for removal, [M] candidates for review
```

In **--all mode**: present a combined report with one section per domain before the confirmation gate.

---

### Step 4 — User confirmation gate

After presenting the report, present options:

```
What would you like to do?
  1. Remove all candidates ([N] items)
  2. Review each candidate individually
  3. Cancel — make no changes
```

**Wait for user response.**

- If user selects **3** or does not respond → exit without modifying any file. Report: "No changes made."
- If user selects **1** → mark all listed candidates as confirmed; proceed to Step 5
- If user selects **2** → enter individual review loop (see below)

#### Individual review loop (option 2)

For each candidate, present:

```
[Requirement title] [CATEGORY]
Text: "[excerpt]"
Detection: [reason]
Suggestion: [REMOVE|REVIEW]

Remove this requirement? (yes / no / skip):
```

- `yes` → add to confirmed removals list
- `no` → skip this candidate (do not remove)
- `skip` → same as `no`

After all candidates reviewed: if confirmed list is empty → exit without modifying any file. Otherwise proceed to Step 5.

---

### Step 5 — Apply removals

For each domain with confirmed removals:

1. Read the current `openspec/specs/<domain>/spec.md`
2. For each confirmed requirement:
   - Locate the requirement block (from its `### Requirement:` heading to the next heading at the same or higher level, or end of file)
   - Remove the entire block including the heading
3. Preserve:
   - Spec header (frontmatter, title, `Change:`, `Date:`, `Base:` lines)
   - All other requirement blocks, scenarios, and sections
   - Markdown structure, line spacing, section order
4. Write the modified content back to the same file path
5. Do NOT rewrite, consolidate, or rephrase any retained content

---

### Step 6 — Record changes

For each domain modified:

1. **Add GC comment to spec header** (insert after the first `---` separator or after the title block):
   ```markdown
   <!-- Last GC: YYYY-MM-DD — [N] requirements removed ([categories: provisional/orphaned/contradictory/etc.]) -->
   ```

2. **Update `ai-context/changelog-ai.md`** with a new entry at the top of the log:
   ```markdown
   - YYYY-MM-DD: Spec GC cleanup — removed [N] stale requirements from openspec/specs/<domain>/spec.md
     Categories: [provisional: X, orphaned: Y, contradictory: Z]
     Run by: /sdd-spec-gc [domain|--all]
   ```

3. Present a summary to the user:
   ```
   Spec GC complete.
   Domains modified: [list]
   Total requirements removed: [N]
   Changelog updated: ai-context/changelog-ai.md
   ```

---

## Rules

- **Dry-run first**: MUST NOT modify any spec file before presenting the report and receiving user confirmation
- **Confirmation required**: MUST NOT apply removals without explicit user selection of option 1 or 2
- **UNCERTAIN candidates**: MUST NOT be removed automatically; suggestion is always "REVIEW for removal"
- **Format preservation**: MUST preserve all non-removed content exactly — no rewrites, consolidation, or rephrasing
- **Active delta specs**: MUST NOT skip scanning but MUST log INFO when a domain has an active change in `openspec/changes/`
- **Non-blocking failures**: index.yaml absent → INFO and fallback to directory scan; spec.md unreadable → WARNING, skip domain, continue (especially in --all mode); grep error → mark UNCERTAIN, do not remove
- **Project-agnostic**: works on any project with `openspec/specs/` structure — not tied to this project's domains
- **Changelog discipline**: MUST update `ai-context/changelog-ai.md` after every successful apply step
