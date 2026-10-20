---
name: pbip-changelog
description: Automatically maintains an append-only changelog of Power BI model changes. Triggers at natural stopping points, after commits, after editing TMDL files, or when the user finishes a batch of model work. Also triggers when the user says "log what we did", "update changelog", "what did we change", or "record changes". Use this proactively after any PBIP model modifications — the user expects a running history without having to ask.
---

# PBIP Changelog

Maintain a human-readable, append-only `CHANGELOG.md` in the PBIP project root. The user relies on this to follow what was done later, so entries should be clear enough for someone who wasn't present to understand.

## When to write an entry

- After a logical batch of TMDL edits is complete (not after every single file save)
- After a git commit that includes TMDL changes
- When the session is wrapping up and model files were modified
- When the user explicitly asks

Do NOT write an entry if nothing changed in the model.

## How to find what changed

Use git to discover changes:

```bash
# Uncommitted changes
git diff --name-only -- '*.tmdl' '*.pbir' '*.json'

# Or changes in the most recent commit
git diff --name-only HEAD~1..HEAD -- '*.tmdl' '*.pbir' '*.json'
```

Then read the actual diffs to understand what changed:
```bash
git diff -- '<specific-file>.tmdl'
```

## How to write entries

Parse the diffs to produce TMDL-aware descriptions. Translate file-level changes into model-level descriptions:

**Instead of:** "Modified `Kite Measures.tmdl`"
**Write:** "Added measure 'Uptime Trend 0543' to Kite Measures table"

**Instead of:** "Modified `relationships.tmdl`"
**Write:** "Changed Case→Account relationship to bidirectional cross-filtering"

**Instead of:** "Deleted `Old Calcs.tmdl`"
**Write:** "Removed table 'Old Calcs' (3 measures moved to Kite Measures)"

## Entry format

Append to `CHANGELOG.md` (never rewrite existing entries):

```markdown
## [YYYY-MM-DD] <Brief Session Title>

### Changes
- Added measure 'Total Revenue YTD' to Financial Measures table
- Modified relationship between Sales and Date (set isActive: true)
- Removed unused measure 'Test Calc' from Kite Measures

### Files Modified
- `<Model>.SemanticModel/definition/tables/Financial Measures.tmdl`
- `<Model>.SemanticModel/definition/relationships.tmdl`
- `<Model>.SemanticModel/definition/tables/Kite Measures.tmdl`

---
```

## Rules

- **Append-only** — never edit or reorder existing entries
- **One entry per logical batch** — don't create an entry for every individual file change
- **No sensitive data** — don't log actual business metric values, customer names, or data contents
- **Date format** — always YYYY-MM-DD
- **Session title** — brief imperative phrase describing the overall goal (e.g., "Add fleet uptime trend measures", "Clean up unused calculations")
- **Cross-reference** — if measure-cleanup or data-dictionary ran, note it (e.g., "Ran /measure-cleanup: removed 3 dead measures")

## If CHANGELOG.md doesn't exist

Create it with the header:
```markdown
# Changelog

All notable changes to this Power BI project are documented here.
Format: append-only, grouped by date and session.

---
```

Then append the first entry.
