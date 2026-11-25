---
name: text-to-markdown
description: Convert structured plain-text data (delimiter-separated status trackers, lists, tables) into well-formatted Markdown with emoji status indicators, proper tables, and file renaming.
category: Data Formatting & Presentation
---

# Text to Markdown Conversion Skill

> **Skill ID:** `text-to-markdown`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Convert structured plain-text data files into clean, well-formatted
Markdown. This skill detects delimiter-separated status tracking lines,
parses them into structured records, maps textual status indicators to
emoji symbols, generates proper Markdown tables, replaces the file
content in-place, and renames the file from `.txt` to `.md`.

Plain-text status trackers are common in engineering workflows — quick
to create but hard to read at scale. Converting them to Markdown tables
with visual indicators (✅/❌/🔄) makes them scannable, presentable in
wikis and pull requests, and version-control friendly.

## Prerequisites

| Requirement | Minimum |
|---|---|
| Shell | PowerShell 5.1+ or Bash 4+ |
| VCS | Git (optional — for `git mv` rename) |
| Access | Write access to the target file |

## When to Apply

Apply this skill when:

- A user asks to "convert text to markdown" or "make this a markdown table"
- A `.txt` file contains delimiter-separated data (dashes, pipes, commas, tabs)
- A status tracker uses `X` or similar markers for incomplete items
- A user asks to "beautify", "format", or "present" a plain-text data file
- A file contains repeated line patterns with consistent delimiters

Do NOT apply when:

- The file is already valid Markdown (`.md`) with proper tables
- The data is in a structured format (CSV, JSON, YAML) and the user
  wants it to stay in that format
- The user wants a programmatic data transformation (e.g., CSV to JSON)
- The text is freeform prose with no tabular structure

---

## Step-by-Step Procedure

### Step 1 — Analyze the Source File

Read the entire file and identify the structural pattern:

1. **Header lines** — titles, section dividers (`---`, `===`), metadata
2. **Data lines** — repeated rows with a consistent delimiter
3. **Delimiter** — the character separating fields (commonly ` - `,
   ` | `, `, `, or tab)
4. **Status markers** — how completion is indicated

**Example input pattern:**

```text
Project Status Tracker
--------------------------
Section Header
============================
ITEM001 - step a done - step b done - X - X - X
ITEM002 - step a done - (step b in progress) - X - X - X
```

**What to identify:**

| Element | Value in Example |
|---|---|
| Delimiter | ` - ` (space-dash-space) |
| Row identifier | First field (`ITEM001`) |
| Completed step | Named text (e.g., `step a done`) |
| In-progress step | Parenthesized text (e.g., `(step b in progress)`) |
| Incomplete step | `X` |
| Header lines | Lines before first data row |

### Step 2 — Extract Column Headers

Derive column headers from the **most complete data row** — the row with
the most named (non-`X`) fields. Each named field becomes a column header.

**Rules:**

- Use the **longest row** (most non-`X` fields) as the template
- Convert field text to Title Case for headers
- Preserve the original field order
- The first field becomes the **ID** column

**Example extraction from:**

```text
ITEM001 - wiki updated - jira created - jira assigned - code implemented - code working - X - X
```

**Yields columns:**

| # | Column Header |
|---|---|
| 1 | ID |
| 2 | Wiki Updated |
| 3 | Jira Created |
| 4 | Jira Assigned |
| 5 | Code Implemented |
| 6 | Code Working |
| 7 | *(remaining columns from other rows)* |

**Cross-row enrichment:** If another row has named fields in positions
where the template row has `X`, use those names to fill in the remaining
column headers. Scan all rows to build the complete header set.

### Step 3 — Map Status Indicators

Convert each field in every data row to an emoji status indicator:

| Source Pattern | Emoji | Meaning |
|---|---|---|
| Named text (e.g., `wiki updated`) | ✅ | Completed |
| `X` | ❌ | Not done |
| Parenthesized text (e.g., `(code working)`) | (✅) | In progress / partial |

**Mapping rules:**

- A field that matches any **non-`X` text without parentheses** → ✅
- A field that is exactly `X` → ❌
- A field wrapped in parentheses `(...)` → `(✅)` — preserves the
  parentheses to indicate partial/in-progress status
- Empty fields → ❌

### Step 4 — Build the Markdown Table

Construct a proper Markdown table with:

1. **Header row** — column names from Step 2
2. **Separator row** — with center-alignment for status columns (`:---:`)
3. **Data rows** — emoji indicators from Step 3

**Format:**

```markdown
| ID | Column A | Column B | Column C |
|----|:---:|:---:|:---:|
| ITEM001 | ✅ | ✅ | ❌ |
| ITEM002 | ✅ | (✅) | ❌ |
```

**Alignment rules:**

- ID column: left-aligned (`----`)
- All status columns: center-aligned (`:---:`)

### Step 5 — Preserve Header Content

Convert the original header/title lines to proper Markdown:

| Source Pattern | Markdown Output |
|---|---|
| Plain title text | `# Title Text` (H1 heading) |
| `====` underlined section | `**Section Text**` (bold) |
| `----` underlined section | `---` (horizontal rule, if decorative) |
| Metadata line (e.g., `Owner: John`) | `**Owner:** John` |

### Step 6 — Replace File Content

Replace the entire file content with the new Markdown. The file structure
should be:

```markdown
# [Original Title]

**[Section/Metadata from headers]**

| ID | Col A | Col B | ... |
|----|:---:|:---:|:---:|
| ITEM001 | ✅ | ❌ | ... |
```

**Critical:** This is an **in-place replacement** — same file, new content.
Do not create a separate file. Do not add extra sections, summaries,
legends, or notes beyond what was in the original data.

### Step 7 — Rename to Markdown Extension

Rename the file from `.txt` to `.md` so it renders as Markdown in
VS Code preview, GitHub, Azure DevOps, and other platforms.

**With Git (preferred):**

```bash
git mv original_file.txt original_file.md
```

**Without Git:**

**PowerShell:**

```powershell
Rename-Item "original_file.txt" "original_file.md"
```

**Bash:**

```bash
mv original_file.txt original_file.md
```

### Step 8 — Verify Rendering

Open the renamed `.md` file and confirm:

- [ ] Table renders correctly in Markdown preview
- [ ] All rows from the original file are present
- [ ] Status indicators match the original data
- [ ] No extra content was added beyond the original data
- [ ] Column headers are correct and complete

---

## Scope Coverage

This skill handles these input formats:

| Input Format | Delimiter | Example |
|---|---|---|
| Dash-separated | ` - ` | `ID - step1 - step2 - X` |
| Pipe-separated | ` \| ` | `ID \| step1 \| step2 \| X` |
| Comma-separated | `, ` | `ID, step1, step2, X` |
| Tab-separated | `\t` | `ID\tstep1\tstep2\tX` |

And these status indicator patterns:

| Pattern | Interpretation |
|---|---|
| Named text | ✅ Completed |
| `X` or `x` | ❌ Not done |
| `(text)` | (✅) In progress / partial |
| Empty / whitespace | ❌ Not done |
| `N/A` or `n/a` | ➖ Not applicable |
| `?` | ❓ Unknown |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Adding content beyond the original data** — No summaries, legends,
  workflow diagrams, progress overviews, or notes unless the user
  explicitly requests them. The conversion must be data-faithful.
- **Reordering rows** — Rows must appear in the same order as the
  original file. Do not sort, group, or rearrange.
- **Dropping rows** — Every data row in the original must appear in the
  output table. No filtering.
- **Inventing column headers** — Headers must be derived from the actual
  field text in the data rows. Do not guess or add columns that have no
  basis in the data.
- **Creating a separate file** — The conversion is in-place. Do not
  create a new `.md` file alongside the original `.txt`.
- **Changing the filename** (beyond extension) — Only the extension
  changes from `.txt` to `.md`. The base name is preserved exactly.
- **Interpreting ambiguous data** — If a field's status is unclear,
  preserve the original text verbatim rather than guessing an emoji.

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Column count mismatch across rows | Use the row with the most fields as the column template; pad shorter rows with ❌ |
| Parenthesized text treated as completed | Parentheses indicate partial/in-progress — map to `(✅)`, not plain `✅` |
| Header lines mixed into data rows | Identify headers by structural markers (`---`, `===`, lack of delimiter pattern) |
| Extra sections added (legend, notes, summary) | Only convert what exists — do not add content the user did not ask for |
| File created alongside original instead of in-place | Replace content in the same file, then rename the extension |
| Delimiter detection picks wrong character | Check for the most frequent consistent separator across all data lines |
| Rows with different field counts | Some rows may have fewer stages; trailing missing fields become ❌ |
| Mixed delimiters in one file | Choose the dominant delimiter; flag any inconsistent lines to the user |
