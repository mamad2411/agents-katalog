---
name: find-github-repo
description: Search GitHub repositories by functionality using gh CLI, iteratively refining the query until the user finds the right one. Use when user wants to find a GitHub repository, library, or tool for a specific purpose, or says things like "is there a repo that does X", "find me a library for Y", or "recommend a tool for Z".
---

# GitHub Repository Finder

## Quick Start

Extract 2–4 keywords from user's description, then search:

```bash
gh search repos "<keywords>" --sort stars --limit 10 \
  --json name,description,url,stargazerCount,updatedAt
```

## Workflow

1. **Extract keywords** — pick nouns/verbs most specific to the desired functionality
2. **Search** with `gh search repos`
3. **Present results** as list (see Output Format)
4. **Ask** with choices:
   > "Did any of these match?
   > A) Wrong language or runtime
   > B) Too generic — need something more specific
   > C) Wrong category (library / CLI / framework)
   > D) Let me describe what I need
   > E) Show more results"
5. **Refine** based on answer → repeat from step 2
6. **No limit** on rounds — keep going until user confirms they found it

## Refinement Strategy

| Choice | Action |
|--------|--------|
| A | Add `--language <lang>` filter, ask which language |
| B | Add more specific terms to query |
| C | Append "library" / "cli" / "framework" to query |
| D | Re-extract keywords from user's new description |
| E | Re-run with `--limit 20`, show next 10 results |

## gh Search Options

```bash
# Basic
gh search repos "<query>" --sort stars --limit 10

# With language filter
gh search repos "<query>" --language typescript --sort stars --limit 10

# More results
gh search repos "<query>" --sort stars --limit 20

# Full JSON output
gh search repos "<query>" --sort stars --limit 10 \
  --json name,description,url,stargazerCount,updatedAt
```

## Output Format

Present results as:

- **owner/name** — description (⭐ N,NNN · updated YYYY-MM)  
  https://github.com/owner/name

Sort by star count descending. If description is empty, note "(no description)".
Format `updatedAt` as `YYYY-MM` (year and month only).
