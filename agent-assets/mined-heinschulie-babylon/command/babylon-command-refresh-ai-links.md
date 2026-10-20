---
description: Discover and curate documentation URLs per technology domain
allowed-tools: Read, Write, Edit, Bash(ls*), WebSearch, WebFetch, Glob
---

# Refresh AI Links

Discover, classify, and curate documentation URLs in `ai_docs/README.md`.
Adds new URLs, flags potentially stale ones — never removes without human confirmation.

## Variables

README_PATH: ai_docs/README.md

## Instructions

- Focus on finding high-quality, authoritative documentation for each technology in the stack
- Classify every URL with `source_type` and `framework_version`
- Preserve existing entries — only ADD or FLAG, never remove
- Prefer official docs > official repos > community repos > blog posts

## Source Type Classification

| source_type | Description | Priority |
|-------------|-------------|----------|
| official_docs | Official documentation site | highest |
| official_repo | Official GitHub repo with agent-relevant rules/plugins | high |
| community_repo | Active community repo with practical guidance | medium |
| npm | npm package page | medium |
| blog | Blog post from framework maintainers | lower |

## Workflow

1. **Read Current State**
   - Read `ai_docs/README.md` to understand existing coverage
   - Note which sections exist and how many URLs each has
   - Read `package.json` files to determine current dependency versions

2. **Discover New URLs Per Section**
   - For each technology section in the README:
     - Search for official documentation pages not yet listed
     - Search for official GitHub repos with agent plugins, rules, or best practices
     - Search for active community repos with practical guidance
     - Search for recent blog posts from framework maintainers (only if highly relevant)
   - For discovered URLs:
     - Classify `source_type` using the table above
     - Set `framework_version` based on the version the docs describe (use `@latest` if version-agnostic, or specific like `svelte@5.x`)

3. **Flag Stale Entries**
   - Check if any existing URLs return 404 or redirect — flag with `<!-- STALE? -->` comment
   - Check if `framework_version` in README mismatches `package.json` versions — flag with `<!-- VERSION_MISMATCH -->` comment

4. **Update README**
   - Add new URLs to the appropriate section table
   - Add flags as HTML comments next to stale or mismatched entries
   - Preserve table format: `| URL | source_type | framework_version |`

5. **Report**

```
Refresh AI Links Report:
- Section: <section name>
  - Added: <count> new URLs
  - Flagged: <count> potentially stale
  - Total: <count> URLs
- ...
- Summary: <total added> new, <total flagged> stale across <section count> sections
```
