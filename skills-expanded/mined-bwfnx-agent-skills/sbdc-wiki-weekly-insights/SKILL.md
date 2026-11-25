---
name: sbdc-wiki-weekly-insights
description: Incremental SBDC wiki synthesis + rebuild via the wikisync guard (early-exit if no changes)
---

> **Schedule:** set in your scheduler
> **Needs:** workspace files, Drive
> **Helper scripts (yours, not included):** pending-push.ps1, wikisync.py

## Weekly SBDC Wiki Insight Synthesis — INCREMENTAL

**Objective:** Synthesize NEW cross-cutting insights from articles that changed since the last synthesis, append to `synthesis-journal.md`, rebuild with the existing builder, publish. Designed to be a cheap no-op on weeks with no changes.

---

### ARCHITECTURE — read this first (rewritten 2026-07-28)

**Canonical wiki = `{{WORKSPACE_ROOT}}/sbdc-advising/wiki/`.** That is where you read and where you write.

`{{WORKSPACE_ROOT}}\sbdc-advising\wiki\` is now a **directory junction** pointing at the repo — the same bytes, not a second copy. Google Drive's `wiki\` is a read-only inbox and is **not** a write target.

> **Why this matters to this task specifically.** On 2026-07-27 a synthesis insight was written to the deploy repo while the build read from a separate build-source folder. The next build would have silently reverted it in production; it was caught with one build to spare. The junction removes that failure mode — but only if you write to the canonical path and publish through the guard.

> **Connected folder = the repo root `[wiki repo]` (the folder containing `.git`).** When this task runs in a mounted sandbox, `[wiki repo]` is mounted directly, so git works in-sandbox. Do all **reading** by `cd`-ing into the wiki subdir (`cd "<root>/sbdc-advising/wiki"`), but run **git** from the repo root with `-C`, never a bare `cd`. Determine `<root>` as the mounted `[wiki repo]` path (e.g. `/sessions/<id>/mnt/[wiki repo]`) or `{{WORKSPACE_ROOT}}` on Windows. Sanity check once: `git -C "<root>" rev-parse --is-inside-work-tree` must print `true`.

Note: `python3` is NOT on PATH on this machine. Use `py`.

---

### Step 1 — Early-exit check (BEFORE reading any articles)

1. Find the most recent `## Synthesis Update — YYYY-MM-DD` heading in `wiki\synthesis-journal.md` (grep; don't read the whole file).
2. List wiki articles changed since that date, running git from the repo root with `-C` (not a bare `cd`):
   `git -C "<root>" log --since="[date]" --name-only --pretty=format: -- sbdc-advising/wiki/ | sort -u`
   Equivalently, if you have the SHA this task last synthesized against, diff by numstat:
   `git -C "<root>" diff --numstat <last-run-sha>..HEAD -- sbdc-advising/wiki`
   Also check `git -C "<root>" status --porcelain sbdc-advising/wiki/`. Exclude `synthesis-journal.md` and `INDEX.md` themselves.
3. **If no articles changed: STOP.** Report "No wiki changes since last synthesis — skipped." Do not rebuild, do not push, do not write a status entry.

### Step 2 — Read ONLY what's needed

- The changed articles (full text).
- The 2 most recent Synthesis Update entries in `synthesis-journal.md` (not the whole file).
- The headings of older entries (`grep -E '^## |^### ' synthesis-journal.md`) so you don't duplicate prior insights.
- Read unchanged articles only when a specific cross-reference requires one (max 2–3).

### Step 3 — Synthesize NEW insights

Identify patterns spanning the changed articles and the rest of the wiki — client-pipeline patterns, funding-program timing (TEDCO/SBA/SBIR deadlines vs. client needs), recurring client challenges, process gaps — that are not in any prior entry heading and are actionable. Ground every insight in specific data; use `[[article-name]]` links. Do not fabricate insights to fill space.

**Check your links resolve.** A `[[slug]]` pointing at an article that does not exist becomes a broken link in production. Confirm the target file exists in `wiki\` before writing the link.

### Step 4 — Append to synthesis-journal.md (in the repo)

Newest entry first — insert after the journal intro, before the previous entry:

```
## Synthesis Update — YYYY-MM-DD

*[One-sentence framing of what changed since last time.]*

### [Insight Title]
[2-4 grounded paragraphs.]
```

Update the "Last compiled" date at the top of `wiki\INDEX.md`.

`synthesis-journal` is a journal, not a topic article. It is deliberately exempt from the `## Related Topics` convention and from `NAV_SECTIONS` — the builder renders it as an explicit special case. Do not "fix" either.

### Step 5 — Rebuild, verify, and publish

```
cd "{{WORKSPACE_ROOT}}"; py {{WORKSPACE_ROOT}}/wikisync.py publish --apply -m "weekly synthesis: YYYY-MM-DD"
```

This runs the pre-publish guard, rebuilds with the frozen builder, copies the HTML into the repo, commits and pushes — in one step. It replaces the old build → copy → `{{WORKSPACE_ROOT}}/pending-push.ps1` sequence.

**NEVER write a new build script. NEVER modify the theme or template.**

Verify `sbdc-advising\SBDC-Wiki.html` mtime is fresh, size > 50KB, **and that it did not shrink** — confirm your new insight text appears in the HTML. A build that drops content is the specific thing worth checking here.

### Step 6 — Report

One short paragraph: which articles changed, insight titles added, guard status, HTML rebuilt yes/no, pushed yes/no.
