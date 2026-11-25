---
name: vault-lint
description: |
  Obsidian vault health checker. Detects broken links, orphan pages, index.md inconsistencies, cross-reference gaps, and frontmatter validation. Inspired by Karpathy's LLM Wiki lint pattern.
  Triggers: "/vault-lint", "check vault", "vault health", "lint notes"
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Edit
  - Bash(ls *)
  - AskUserQuestion
---

# Vault Lint — Knowledge Base Health Check

Inspired by Karpathy's "Lint" philosophy: periodically scan the vault to surface inconsistencies, broken links, orphan pages, and data gaps.

## Workflow

### Step 1: Environment Detection

**1a. Detect vault root** — follow [../../_shared/common-steps.md](../../_shared/common-steps.md) "Vault Detection" section.

**1b. Scan all article files:**

```
Glob("**/*.md", path="$VAULT_ROOT")
```

Exclude `.claude/`, `.git/`, `.playwright-mcp/`, `reviews/`, `node_modules/` directories.
Build the file list `$ALL_ARTICLES`.

### Step 2: Six Checks

#### Check 1: Broken Links

Scan all articles for `[[wikilink]]` and `[[wikilink|alias]]`:

```
Grep("\\[\\[.*?\\]\\]", path="$VAULT_ROOT", glob="**/*.md", output_mode="content")
```

For each wikilink:
1. Extract the link target (the part before `|`)
2. Look for a matching file in `$ALL_ARTICLES` (filename without `.md` extension)
3. No match → record as broken link, note the source file and line number

#### Check 2: Orphan Pages

For each file in `$ALL_ARTICLES`:
1. Extract the filename (without path and extension)
2. Search all other articles for `[[filename]]` or `[[filename|`
3. No inbound links → record as orphan page

Exclude index.md, README.md, CLAUDE.md (these naturally have no inbound links).

#### Check 3: index.md Consistency

1. Read `$VAULT_ROOT/index.md`
2. Compare against `$ALL_ARTICLES`:
   - Entry in index.md but file doesn't exist → **ghost entry**
   - File exists but no entry in index.md → **missing entry**
3. Check whether `total_articles` count in the index.md header is accurate

#### Check 4: Cross-Reference Suggestions

For each article:
1. Extract 3-5 core keywords (from title and tags)
2. Search other articles for these keywords
3. If article A frequently mentions core concepts of article B but has no `[[B]]` link → suggest adding a cross-reference

This check is time-intensive; limit to 10 most recently modified articles per run.

#### Check 5: Summary Quality

Check entries in index.md:
- Summary is empty or too short (< 10 chars) → flag as "insufficient summary"
- Summary doesn't match actual article content (compare against first 50 lines) → flag as "stale summary"

#### Check 6: Frontmatter Completeness

For each file in `$ALL_ARTICLES` (excluding index.md, README.md, CLAUDE.md):

1. Check for YAML frontmatter (starts and ends with `---`)
2. Validate required fields are present and non-empty: `title`, `date`, `tags`, `type`, `confidence`, `related`, `summary`
3. Validate `type` value is in the allowed set: `concept`, `deep-dive`, `comparison`, `practice`, `guide`, `overview`
4. Validate `confidence` value is in the allowed set: `high`, `medium`, `low`
5. Validate `related` is a list with each item in `"[[...]]"` format (empty list `[]` is acceptable)

Issue severity:
- **Missing frontmatter** — file has no YAML frontmatter block
- **Missing field** — a required field is absent
- **Invalid value** — type or confidence is not in the allowed enum

### Step 3: Generate Health Report

Aggregate results into a structured report, output to terminal:

```markdown
# Vault Health Report — {date}

## Overview
- Total articles: {count}
- Health status: {healthy / needs attention / needs repair}

## Broken Links ({count})
| Source File | Broken Target | Line |
|------------|---------------|------|
| ... | ... | ... |

## Orphan Pages ({count})
- {filename} — no other article links to this page

## index.md Consistency
- Ghost entries: {list}
- Missing entries: {list}
- Count drift: index says {n}, actual {m}

## Suggested Cross-References
- [[A]] <-> [[B]] (shared keywords: {keywords})

## Summary Quality
- Insufficient: {list}
- Possibly stale: {list}

## Frontmatter Issues ({count})
| File | Issue Type | Details |
|------|-----------|---------|
| ... | ... | ... |
```

### Step 4: Auto-Fix (Optional)

Provide auto-fix for these issues:

1. **Missing index.md entries**: read the missing article's frontmatter, append to index.md per the **Index Update** steps in [../../_shared/common-steps.md](../../_shared/common-steps.md)
2. **Count drift in index.md**: update `total_articles` and `last_updated`
3. **Ghost entries**: remove from index.md

No confirmation needed before auto-fix (these are low-risk metadata corrections).

Broken link fixes, orphan page handling, cross-reference additions — report only, do not auto-modify article content.

4. **Missing or incomplete frontmatter** — report only, do not auto-modify (requires content understanding to correctly infer type/confidence).
