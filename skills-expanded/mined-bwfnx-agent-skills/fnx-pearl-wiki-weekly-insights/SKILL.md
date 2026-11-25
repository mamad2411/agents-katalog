---
name: fnx-pearl-wiki-weekly-insights
description: Incremental FNX Pearl wiki synthesis + rebuild (early-exit if no changes)
---

> **Schedule:** set in your scheduler
> **Needs:** workspace files
> **Helper scripts (yours, not included):** _wiki-infrastructure/pending-push.ps1, raw-to-wiki-ingest.py, wiki-build.py

## Weekly FNX Pearl Wiki Insight Synthesis — INCREMENTAL

**Objective:** Synthesize NEW cross-cutting insights from articles that changed since the last synthesis, append to the Cross-Context Insights section of INDEX.md, rebuild the HTML with the existing builder. Designed to be a cheap no-op on weeks with no changes.

### Step 0 — Workspace path
Run `ls /sessions/` to find the session directory. Workspace = `/sessions/[session]/mnt/{{WORKSPACE_ROOT}}/`. Do NOT hardcode a session name.

### Step 1 — Early-exit check (BEFORE reading any articles)
1. Find the date of the most recent `## Synthesis Update — YYYY-MM-DD` heading in `fnx-pearl-consulting/wiki/INDEX.md` (grep; don't read the whole file).
2. List wiki articles changed since that date:
   `cd [workspace] && git log --since="[date]" --name-only --pretty=format: -- fnx-pearl-consulting/wiki/ | sort -u`
   Also check `git status --porcelain fnx-pearl-consulting/wiki/` for uncommitted changes. Exclude INDEX.md itself.
3. **If no articles changed: STOP.** Report "No wiki changes since last synthesis — skipped." Do not rebuild, do not push, do not write a status entry.

### Step 2 — Read ONLY what's needed
- The changed articles (full text).
- The 2 most recent Synthesis Update entries in INDEX.md (not the whole file).
- The headings of all older entries (`grep -E '^## |^### ' fnx-pearl-consulting/wiki/INDEX.md`) so you don't duplicate prior insights.
- Do NOT re-read CLAUDE.md (it loads automatically). Read unchanged articles only when a specific cross-reference requires one (max 2-3).

### Step 3 — Synthesize NEW insights
Look for: client pipeline and revenue patterns, proposal-to-close follow-through gaps, service/offering positioning connections, scheduling and capacity patterns. Insights must not duplicate prior entry headings and must be actionable or worth {{USER}} knowing. Ground in specific data; use [[article-name]] links. Do not fabricate insights to fill space.

### Step 4 — Append to INDEX.md
Append a new section to the bottom of the Cross-Context Insights section:

```
---

## Synthesis Update — YYYY-MM-DD

*[One-sentence framing of what changed since last time.]*

### [Insight Title]
[2-4 grounded paragraphs.]
```

Update the "Last updated" date at the top of INDEX.md.

### Step 5 — Rebuild HTML
Run: `cd [workspace] && python3 {{WORKSPACE_ROOT}}/wiki-build.py fnx-pearl`
**NEVER write a new build script. NEVER modify the theme or template.** The builder reads the frozen template and is the only correct rebuild path.
Verify `fnx-pearl-consulting/FNX-Pearl-Wiki.html` mtime is fresh and size > 50KB.

### Step 6 — Commit and push
Run `python3 {{WORKSPACE_ROOT}}/raw-to-wiki-ingest.py push` to write `{{WORKSPACE_ROOT}}/_wiki-infrastructure/pending-push.ps1`, then execute that script via the `mcp__Windows-MCP__PowerShell` tool (Windows git has the credentials; sandbox git does not). It exits cleanly if nothing to commit.

### Step 7 — Report
One short paragraph: which articles changed, insight titles added, HTML rebuilt yes/no, pushed yes/no.