---
name: util-ustagger
model: claude-sonnet-4-6
effort: medium
description: >
  Tag new items in PRD.md files with unique ID codes and validate no duplicate tags exist.
  Applies to PRD.md documents structured with module sections containing User Stories, Non
  Functional Requirements, Constraints, References, and Test instructions. Each top-level
  bullet item gets a unique 9-character code with category prefix, application initials,
  and running number (interval of 3).
  Trigger on keywords: "tag user story", "tag user stories", "fix user story tag", "fix user story tags",
  "add IDs to requirements", "tag items in PRD.md", "number the requirements",
  "add requirement codes", "validate tags", "check duplicate tags", "verify tagging completeness".
  Accepts an application name and version as input (e.g., `/util-ustagger hub_middleware v1.0.3`,
  `/util-ustagger "Hub Middleware" v1.0.3`).
---

# Util US Tagger

Tag untagged items in PRD.md files with unique 9-character ID codes and validate no duplicates.
Covers User Stories, Non Functional Requirements, Constraints, References, and Test instructions.

## Version Gate

Before starting any work, resolve the application folder first (see Input Resolution below), then check `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution for this application).
2. If `<app_folder>/CHANGELOG.md` exists, scan all `## vX.Y.Z` headings and determine the **highest version** using semantic versioning comparison.
3. Compare the requested version against the highest version:
   - If requested version **>=** highest version: proceed normally.
   - If requested version **<** highest version: **STOP immediately**. Print: `"Version {requested} is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."` Do NOT proceed with any work.

## Input Resolution

This skill requires two mandatory arguments: `<application>` and `<version>`.

| Argument | Required | Description |
|----------|----------|-------------|
| `<application>` | Yes | Application name — matched against root-level application folders |
| `<version>` | Yes | Version label (e.g., `v1.0.3`). Recorded for traceability but all items are tagged regardless of version. |

### Application Folder Resolution

1. List root-level application folders that have a numeric prefix (e.g., `1_hub_middleware`, `2_hc_adapter`)
2. Strip the leading `<number>_` prefix from each folder name (e.g., `1_hub_middleware` -> `hub_middleware`)
3. Match the provided application name **case-insensitively** against the stripped folder names
4. Accept `snake_case`, `kebab-case`, or title-case input (e.g., `hub_middleware`, `hub-middleware`, `Hub Middleware` all match `1_hub_middleware`)
5. If no match is found, list all available application names and **stop**

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |

Example invocations:
- `/util-ustagger hub_middleware v1.0.3`
- `/util-ustagger "Hub Middleware" v1.0.3`
- `/util-ustagger hub-middleware v1.0.3`

## Workflow

### 1. Detect Application Initials

Derive initials from the parent folder name containing PRD.md:
- Strip leading number and underscore prefix (e.g., `1_` from `1_hub_middleware`)
- Take the first letter of each remaining word, uppercase
- Examples: `1_hub_middleware` -> `HM`, `2_source_country` -> `SC`, `3_hiring_country` -> `HC`

### 2. Compute Tag Prefixes

All codes are exactly **9 characters**. The prefix is category abbreviation + application initials. Remaining length is zero-padded running number.

| Category               | Prefix Formula          | Example (HM)  | Digit Length |
|------------------------|-------------------------|----------------|--------------|
| User Story             | `US` + initials         | `USHM` (4)     | 5 digits     |
| Non Functional Req     | `NFR` + initials        | `NFRHM` (5)    | 4 digits     |
| Constraint             | `CONS` + initials       | `CONSHM` (6)   | 3 digits     |
| Reference              | `REF` + initials        | `REFHM` (5)    | 4 digits     |
| Test                   | `TST` + initials        | `TSTHM` (5)    | 4 digits     |

### 3. Scan Existing Tags

Before tagging, scan the entire document for already-tagged items matching the pattern `[PREFIX + digits]`. Record the highest running number per category to continue from.

### 4. Tag Untagged Items

For each section (User Story / Functional Requirements, Non Functional Requirement, Constraint, Reference, Test):

- Tag only **top-level bullet items** (lines starting with `- ` at the section's base indentation)
- **Skip sub-bullets** (indented lines starting with `  - `)
- **Skip already-tagged items** (lines containing `[USHM`, `[NFRHM`, `[CONSHM`, `[REFHM`, `[TSTHM` etc.)
- Running numbers use **interval of 3**: 3, 6, 9, 12, 15, ...
- Insert tag as `[CODE] ` immediately after the bullet dash: `- [USHM00003] As a...`

Section header recognition (case-insensitive matching):
- User Stories: `### User Story`, `### Functional Requirements`
- NFRs: `### Non Functional Requirement`, `## Non Functional Requirement`
- Constraints: `### Constraint`, `## Constraint`
- References: `### Reference`, `## Reference`
- Tests: `### Test`

### 5. Validate No Duplicates

After tagging, scan the entire document and collect all tag codes. Report:
- Total count per category (US, NFR, CONS, REF, TST)
- Any duplicate codes found (this is an error that must be fixed)
- Confirmation message if no duplicates

### 6. Output Summary

Print a summary table:

```
| Category    | Prefix   | Count | Range                    |
|-------------|----------|-------|--------------------------|
| User Story  | USHM     | 35    | USHM00003 - USHM00105   |
| NFR         | NFRHM    | 39    | NFRHM0003 - NFRHM0117   |
| Constraint  | CONSHM   | 13    | CONSHM003 - CONSHM039   |
| Reference   | REFHM    | 6     | REFHM0003 - REFHM0018   |
| Test        | TSTHM    | 4     | TSTHM0003 - TSTHM0012   |
| Duplicates  | -        | 0     | None                     |
```

## Changelog Append

After all tags are successfully applied, append an entry to `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. Read `<app_folder>/CHANGELOG.md`. If it does not exist, create it with:
   ```markdown
   # Changelog

   - This file tracks all skill executions by version for this application.
   - The highest version recorded here is the current application version.
   - Skills MUST NOT execute for a version lower than the highest version in this file.

   ---
   ```
2. Search for a `## {version}` heading matching the current version.
3. If the section **exists**: append a new row to its table.
4. If the section **does not exist**: insert a new section after the `---` below the context header and before any existing `## vX.Y.Z` section (newest-first ordering), with a new table header and the first row.
5. Row format: `| {YYYY-MM-DD} | {application_name} | util-ustagger | All | Tagged user stories, NFRs, constraints, references and tests |`
6. **Never modify or delete existing rows.**

## Important Rules

- **NEVER remove, modify, or reassign existing tags.** Existing tags are immutable — they may already be referenced by module models, specifications, or other documents. Changing them would break traceability.
- Never tag sub-bullets; only top-level bullets under tagged sections
- Never re-tag items that already have a tag code
- New tags must continue from the highest existing running number per category (not restart from 003)
- All codes must be exactly 9 characters
- Running numbers always use interval of 3
- Tables, blank lines, and version tags (e.g., `[v1.0.0]`) are never tagged
- Preserve all existing content, formatting, and indentation exactly
