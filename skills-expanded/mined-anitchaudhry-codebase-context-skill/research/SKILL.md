---
name: research
description: "Search docs, resolve errors, check deps, find best practices — cached locally"
category: quality
tags: [docs, errors, best-practices]
depends-on: []
input: "research query or error message"
output: "research findings cached locally"
token-estimate: 3000
parallel-safe: true
argument-hint: "[error message | library name | deps | best-practices topic | breaking-changes pkg]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# Research

Web-powered research with local caching. All results saved to `.ccs/research/` so the same lookup never happens twice.

## Steps

### 1. Determine research type
Parse `$ARGUMENTS`:
- Error message in quotes → error research
- Library/package name → documentation lookup
- `deps` → dependency compatibility check
- `best-practices <topic>` → best practices research
- `breaking-changes <package>` → migration/upgrade research

### 2. Check local cache FIRST
1. Glob `.ccs/research/*.md` for files matching the topic
2. If match exists and is <7 days old → **USE IT. Skip all web calls.**
3. If match exists but >7 days old → re-fetch and update
4. Also check `.ccs/task.md` for recent research entries on this topic

### 3. Gather local context
- Read `.ccs/architecture.md` for tech stack and versions
- Read package manager files for exact dependency versions

### 4. Execute research
**Error mode:** WebSearch exact error + framework + version. Fetch top 3 results. Extract root cause, fix steps, version requirements. Verify fix matches user's versions.

**Documentation mode:** WebSearch for official docs URL. WebFetch relevant API reference pages. Extract signatures, config options, usage examples, gotchas.

**Deps mode:** For each dependency, check latest version, breaking changes, deprecation. Run native audit (`npm audit` / `pip-audit`). Output health report table.

**Best practices mode:** WebSearch topic + best practices + year. Fetch 2-3 authoritative sources. Cross-reference with `.ccs/conventions.md`.

**Breaking changes mode:** WebSearch migration guide for current → latest. WebFetch official migration guide. Output changes required with before/after code.

### 5. Save to `.ccs/research/<topic-slug>.md`
Create `.ccs/research/` directory if needed. Save with format:
```
# Research: <topic>
> Fetched: <timestamp>
> Source: <URLs>
> Query: <search queries used>
## Findings
<actionable content only>
## Version Compatibility
<which versions this applies to>
```

### 6. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: query, findings summary, sources, action items.

## Rules
- **ALWAYS check `.ccs/research/` before ANY web call** — this is non-negotiable
- Save ALL research to `.ccs/research/<topic>.md` — this is non-negotiable
- Search with specific terms (include version numbers, exact error text)
- Fetch only relevant pages, not entire doc sites
- Extract actionable info only, not full page content

## Refs
- Research cache: `.ccs/research/`
- Architecture: `.ccs/architecture.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`
- Strategy: `.claude/skills/_ccs/references/context-strategies.md`

---
*codebase-context-skill v2.0.0*
