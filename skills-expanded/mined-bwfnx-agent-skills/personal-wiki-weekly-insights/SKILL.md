---
name: personal-wiki-weekly-insights
description: Incremental personal wiki synthesis + rebuild (early-exit if no changes)
---

> **Schedule:** set in your scheduler
> **Needs:** workspace files
> **Helper scripts (yours, not included):** _wiki-infrastructure/pending-push.ps1, raw-to-wiki-ingest.py, wiki-build.py

## Weekly Personal Wiki Insight Synthesis — INCREMENTAL

**Objective:** Synthesize NEW cross-cutting insights from articles that changed since the last synthesis, append to synthesis-journal.md, rebuild the HTML with the existing builder. Designed to be a cheap no-op on weeks with no changes.

### Step 0 — Repo path
Workspace = the git repo itself: `{{WORKSPACE_ROOT}}`.
All paths below are relative to it — `personal/wiki/`, `{{WORKSPACE_ROOT}}/wiki-build.py`, `{{WORKSPACE_ROOT}}/raw-to-wiki-ingest.py`.

Run every command in this task on Windows (`mcp__Windows-MCP__PowerShell`, or Desktop Commander). Do NOT use the Linux sandbox: it reaches this content only through `{{WORKSPACE_ROOT}}`, where `personal/wiki` is a Windows directory junction the sandbox cannot traverse (`Input/output error`), and that path is not a git repo at all.
Confirm with `git -C [workspace] rev-parse --show-toplevel` before proceeding.

### Step 1 — Early-exit check (BEFORE reading any articles)
1. Find the date of the most recent `## Synthesis Update — YYYY-MM-DD` heading in `personal/wiki/synthesis-journal.md` (Select-String; don't read the whole file). The separator is an em dash (—), not a hyphen.
2. List wiki articles changed since that date:
   `git -C [workspace] log --since="[date]" --name-only --pretty=format: -- personal/wiki/ | Sort-Object -Unique`
   Also check `git -C [workspace] status --porcelain personal/wiki/` for uncommitted changes. Exclude synthesis-journal.md and INDEX.md themselves.
3. **If no articles changed: STOP.** Report "No wiki changes since last synthesis — skipped." Do not rebuild, do not push, do not write a status entry.

### Step 2 — Read ONLY what's needed
- The changed articles (full text).
- The 2 most recent Synthesis Update entries in synthesis-journal.md (not the whole file).
- The headings of all older entries (`Select-String -Path personal\wiki\synthesis-journal.md -Pattern '^## |^### '`) so you don't duplicate prior insights.
- Do NOT re-read CLAUDE.md (it loads automatically). Read unchanged articles only when a specific cross-reference requires one (max 2-3).

### Step 3 — Synthesize NEW insights
Identify patterns that span the changed articles and the rest of the wiki, are not in any prior entry heading, and are actionable or worth {{USER}} knowing. Ground every insight in specific data; use [[article-name]] links. Do not fabricate insights to fill space — one strong insight beats three thin ones.

### Step 4 — Append to synthesis-journal.md
Newest entry first (insert after the journal intro, before the previous entry):

```
## Synthesis Update — YYYY-MM-DD

*[One-sentence framing of what changed since last time.]*

### [Insight Title]
[2-4 grounded paragraphs.]
```

Update the "Last updated" date at the top of `personal/wiki/INDEX.md`.

### Step 5 — Rebuild HTML
Run: `cd [workspace]; python {{WORKSPACE_ROOT}}/wiki-build.py personal` (on Windows it is `python`, not `python3` — `python3` resolves to the Microsoft Store stub and fails)
**NEVER write a new build script. NEVER modify the theme or template.** The builder reads the frozen template and is the only correct rebuild path.
Verify `personal/Personal-Wiki.html` mtime is fresh and size > 50KB.

### Step 6 — Commit and push
Run `python {{WORKSPACE_ROOT}}/raw-to-wiki-ingest.py push` (from `[workspace]`) to write `{{WORKSPACE_ROOT}}/_wiki-infrastructure/pending-push.ps1`, then execute that script via the `mcp__Windows-MCP__PowerShell` tool (Windows git has the credentials; sandbox git does not). It exits cleanly if nothing to commit.

### Step 7 — Report
One short paragraph: which articles changed, insight titles added, HTML rebuilt yes/no, pushed yes/no.