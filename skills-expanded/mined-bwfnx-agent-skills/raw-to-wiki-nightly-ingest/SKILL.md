---
name: raw-to-wiki-nightly-ingest
description: Scan SBDC raw/ folders for new files, extract into wiki articles in the git repo, rebuild, and publish via the wikisync guard
---

> **Schedule:** Tue/Thu/Sat ~1:30 AM ET (despite the name)
> **Needs:** {{CRM}}, workspace files, Drive, team drive
> **Helper scripts (yours, not included):** _sync-work/navcheck.py, _wiki-infrastructure/pending-push.ps1, build-sbdc-wiki-fieldmanual.py, ledger.py, pending-push.ps1, raw-to-wiki-ingest.py, wikisync.py

# Raw-to-Wiki Nightly Ingest — SBDC Only

> **The name says "nightly"; the task is not nightly and is not meant to be.**
> Actual schedule is **Tue/Thu/Sat ~1:30 AM ET**, confirmed by 45 of 48 runs
> (2026-04-23 → 2026-08-11) and by two independent documents. The three off-weekday
> run folders are hand-run catch-ups, not scheduled fires.
>
> **Do not "fix" the schedule to match the name.** The schedule is correct; the name is
> the stale artifact. The folder name is load-bearing — the scheduler's pointer prompt
> hardcodes this path — so renaming requires updating the scheduler task in the same
> pass, not a file rename alone.

## Objective

Scan the SBDC `raw/` folders for new source files, extract relevant content into the appropriate wiki articles, rebuild the HTML, and publish — using the `{{WORKSPACE_ROOT}}/wikisync.py` guard so the copies cannot silently diverge.

---

## ARCHITECTURE — read this first (rewritten 2026-07-28)

The wiki's sync model changed on 2026-07-28. Older instructions that treat Google Drive as the wiki's source of truth are **wrong**. Current model:

| Copy | Role |
|---|---|
| `{{WORKSPACE_ROOT}}/sbdc-advising/wiki/` | **CANONICAL.** Write articles here. Has git history. Netlify serves it. |
| `{{WORKSPACE_ROOT}}/sbdc-advising/wiki/` | A **directory junction** pointing at the line above. Same bytes, not a second copy. |
| `{{TEAM_DRIVE}}/wiki/` | **Read-only inbox.** Do NOT write wiki articles here any more. |

**Write wiki articles to the `[wiki repo]` path.** The Drive `wiki\` folder is drained *from*, never written *to*.

> **Junction caveat:** if you are running inside a mounted sandbox (a `/sessions/<id>/mnt/...` path), the junction points *outside* the mounted folder and may not resolve. Do not rely on it. Reach the repo through the Windows PowerShell MCP tool using the full `[wiki repo]` path, and verify you can list `sbdc-advising\wiki\*.md` and see ~49 files before writing anything.

### The two rules that prevent the historical bugs

1. **Never use the Google Drive API to update an existing file.** `create_file` cannot update in place — it makes a second file with the same title and Drive's desktop client renames one to `foo (1).md`. This stranded roughly 26 articles' worth of edits in 2026. The Drive API is fine for **read-only discovery**. All writes go through a real filesystem path.
2. **A new article is not published until its slug is in `NAV_SECTIONS`.** See Step 4 — the single easiest way to silently lose work.

### Both raw folders must be scanned

There are **two** raw folders, and older versions of this task only scanned one:

- `{{WORKSPACE_ROOT}}/sbdc-advising/raw/`
- `{{TEAM_DRIVE}}/raw/`

They are substantially different (as of 2026-07-28: 337 vs 234 entries). Scan **both**.

---

## Step 0 — Pre-flight guard

Via PowerShell:

```
cd "{{WORKSPACE_ROOT}}"; py {{WORKSPACE_ROOT}}/wikisync.py check
```

Note: `python3` is NOT on PATH on this machine. Use `py`.

If it reports problems, read them before proceeding. Shadow `(N).md` files or undrained Drive content mean an earlier run misbehaved — resolve those first (`py {{WORKSPACE_ROOT}}/wikisync.py shadows`, `py {{WORKSPACE_ROOT}}/wikisync.py drain`). Do not paper over a failing guard.

### The push gate — scoped, and the ONLY gate (defined 2026-08-11)

**Do not invent a broader gate than this one.** From 2026-07-16 to 2026-08-08 every single
run ended `push held: unrelated dirty worktree`. That phrase appears in no definition file
anywhere — it was agent-invented judgment, reconstructed each run from the sentence above
plus `{{WORKSPACE_ROOT}}/wikisync.py check` output, and it blocked the pipeline for six weeks against a hazard
that had already been removed from the code on 2026-06-10.

Two facts that make a whole-repo cleanliness check wrong:

1. `{{WORKSPACE_ROOT}}/pending-push.ps1` stages an **explicit 9-path list** (the four `wiki/` dirs, the four
   built HTML files, and `_wiki-ingest-state.json`) — never `git add -A`. Dirt anywhere
   else in the monorepo **cannot** ride along on the automated push.
2. `{{WORKSPACE_ROOT}}/wikisync.py` deliberately classifies `"uncommitted"` as `NON_BLOCKING` (see its
   `NON_BLOCKING` tuple). Its `FAIL uncommitted: <file>` lines are **warnings, not
   blockers**. Treating them as blockers is stricter than the tool's own author intended.

**Hold the push only if** a file *inside one of the 9 staged paths* is modified with content
this run did not produce. That is the whole gate.

**Do not hold** for: dirty files outside those 9 paths, untracked scratch folders, deleted
video/project files, CRLF-only diffs (confirm with `git diff -w --numstat` — empty output
means whitespace-only), or the ingest run's own new articles and INDEX rows.

If you do hold, the report must name **the exact file path** and **which of the 9 staged
paths contains it**. A hold that cannot name both is not a real hold — proceed with the push.

> Separate hazard, still live: the *manual* publisher `{{WORKSPACE_ROOT}}/wikisync.py publish` does run
> `git add -A` internally. That is the one path where a whole-repo dirty check is warranted.
> Do not run it while an automated ingest is mid-flight.

## Context Budget Rule

**This task runs in a single session with a finite context window.** The main
threat is reading multiple raw files (meeting notes, policy docs, training
material) in the parent context — each file can be 5-20KB, and with the 20-file
cap that is up to 400KB of raw text accumulating in context before compaction
thrashes.

**The fix: raw file reading and extraction go into isolated subagents.** For each
batch of files to process (group by target wiki article), dispatch a subagent
that reads the raw files and returns a **compact wiki-ready extraction** (target:
under 2,000 tokens per batch). The extraction includes:

```json
{
  "targetArticle": "slug of the wiki article to update",
  "newContentBlocks": [
    {
      "section": "heading where content belongs",
      "prose": "synthesized wiki prose — NOT raw content",
      "sourceFiles": ["filename1.ext", "filename2.ext"],
      "ingestDate": "YYYY-MM-DD"
    }
  ],
  "newArticleNeeded": false,
  "suggestedSlug": null,
  "unclassifiable": ["files that didn't fit any article"]
}
```

The parent uses these compact extractions to update articles, register slugs,
and run the build. It never reads raw file contents directly.

Similarly, when updating an existing wiki article (Step 3), the parent reads only
the article's heading structure (not full text) to decide where to insert. The
subagent's `section` field tells the parent where each block goes.

## Step 1 — Scan both raw/ folders

Look for new or recently modified files in both raw folders. Track processed files via `raw-ingest-log.md` in `{{TEAM_DRIVE}}/outputs/` (append in place via the mounted team drive — never via the Drive API).

**Early exit:** if no new files, report "No new raw files — skipped." and stop.

## Step 2 — Classify and extract (subagent isolation — ALWAYS)

**Do NOT read raw files in the parent context.** Group unprocessed files by
likely target article, then dispatch a subagent per batch (see Context Budget
Rule above). The subagent:

1. Reads the raw file content.
2. Decides which wiki article(s) it belongs in (meeting notes → topic article; policy docs → policy article; training material → training article).
3. Synthesizes into wiki prose. Does NOT paste raw content verbatim.
4. Returns the compact structured JSON extraction described above.

The parent receives only the extraction and uses it in Step 3.

## Step 3 — Update wiki articles **in the git repo**

For each affected article under `{{WORKSPACE_ROOT}}/sbdc-advising/wiki/`:
1. Read the current article.
2. Insert new content in the right section, preserving structure and voice.
3. Add `<!-- Source: filename.ext, ingested YYYY-MM-DD -->` near the insertion.
4. Write in place via PowerShell (`Set-Content`) or the Windows-MCP `FileSystem` tool.

**Safety rules:**
- Never delete existing content — only add or refine.
- **Diff semantically, not line-by-line.** A line that looks new is often a *worse* rewording of something canonical already says better. Check before adding.
- Maintain existing heading structure; every article ends with `## Related Topics`.
- If unsure where content belongs, append under `## Unsorted / Needs Review`.
- Respect PII rules: initials or {{CRM}} case numbers, never full client names with sensitive detail. See the `data-security-and-client-file-handling` wiki article for what must never enter a shared folder at all.

## Step 4 — Register any NEW article (do not skip)

If you created a brand-new article, it is **invisible** until you do both:

1. Add a row to `wiki\INDEX.md` (this only supplies the description text).
2. **Add the slug to `NAV_SECTIONS` in `{{WORKSPACE_ROOT}}/build-sbdc-wiki-fieldmanual.py`** — one entry in the appropriate section's slug list.

`NAV_SECTIONS` is what the builder actually renders from. A file that exists, commits, and deploys but is absent from `NAV_SECTIONS` produces no nav link, no index card, and no article body. Two articles sat unpublished this way for months. Adding a slug to that list is a data edit and is allowed. **Never rewrite the build script otherwise, and never modify the theme or template.**

Verify with `py {{WORKSPACE_ROOT}}/_sync-work/navcheck.py`, or just `py {{WORKSPACE_ROOT}}/wikisync.py check` — its "render coverage" section fails on any file that will not render.

## Step 5 — Rebuild, verify, and publish

Use the **automated** publisher — not `{{WORKSPACE_ROOT}}/wikisync.py publish`:

```
cd "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/raw-to-wiki-ingest.py build-all
py {{WORKSPACE_ROOT}}/raw-to-wiki-ingest.py mark
py {{WORKSPACE_ROOT}}/raw-to-wiki-ingest.py push
```

`mark` refuses to record any manifest file whose extraction was skipped (kind=unknown such
as `.html`, an empty extract, or a `[... error]` sentinel) and prints them under
**"unsupported type, needs a human call"**. Copy that block verbatim into the run report under
the same heading — those files stay out of state and resurface every scan until {{USER}} decides.
Never run `mark --include-held` on your own; that flag records a decision only a human makes.
(Added 2026-09-13 after `HGP SBA Loan/hgp-ablation-report.html` was consumed silently on 09-12;
`py {{WORKSPACE_ROOT}}/raw-to-wiki-ingest.py selfcheck` exercises the rule.)

`push` writes `{{WORKSPACE_ROOT}}/_wiki-infrastructure/pending-push.ps1`; execute that script via the Windows
PowerShell MCP tool (`mcp__Windows-MCP__PowerShell`). It stages only the 9 explicit paths,
commits, and pushes. Sandbox git cannot read `.git/config`, which is why the push must run
through Windows.

> **Why not `{{WORKSPACE_ROOT}}/wikisync.py publish --apply` here:** that is the *manual* publisher and it runs
> `git add -A` internally, which would sweep unrelated monorepo dirt into an automated
> commit. It remains correct for hand-publishing when you have checked the tree yourself.
> Do not run both publishers concurrently.

**Verify the build lost nothing:** confirm the new content appears in `SBDC-Wiki.html` and that the file did not shrink. A build that silently drops an article is exactly what this checks for.

## Step 6 — Update the ingest log

Append each processed filename and date to `raw-ingest-log.md` in `{{TEAM_DRIVE}}/outputs/` via the mounted team drive (`Add-Content`). Never create a fresh log via the Drive API — that orphans the history as a duplicate.

## Step 7 — Duplicate safety net

`py {{WORKSPACE_ROOT}}/wikisync.py check` fails loudly if any `foo (N).md` exists in the Drive wiki folder. If it does:

1. Inspect with `py {{WORKSPACE_ROOT}}/wikisync.py shadows` — for each shadow it prints the lines absent from canonical *and* the closest matching canonical line, so you can tell a genuine addition from a worse reword.
2. Merge only what is genuinely missing. **Never bulk-merge.**
3. Retire the handled file: `py {{WORKSPACE_ROOT}}/wikisync.py retire-shadow "<name>" --apply` — moves it to `{{TEAM_DRIVE}}/delete/` as `<name>-ORIGINAL-superseded-YYYY-MM-DD.md`. **Never permanently delete.**

## Step 8 — Report

Short summary: raw files processed and from which folder, articles updated, any new article and whether its slug was registered in `NAV_SECTIONS`, guard status before and after, rebuilt yes/no, pushed yes/no, unclassifiable files, a **"unsupported type, needs a human call"** section listing every file `mark` held (or "none"), and any shadows found or resolved.

**Write `_wiki-ingest-log\<DATE>\run-report.md` before you finish — always, including when the
run fails or exits early.** Five runs (2026-05-09, 06-29, 07-14, 07-15, 08-11) wrote a
manifest and then no report, so their outcome is permanently unknown; two of them sit
immediately before the 7-day gap of 2026-07-16 → 07-23. A missing report is
indistinguishable from a run that never happened.

If you exit early for any reason — no new files, a failing guard, a held push, an error —
still write the report and state the reason in one line. The report is the only durable
record that the run occurred.

**Heartbeat — last command of every run, including early exits:**
`py {{WORKSPACE_ROOT}}/ledger.py beat raw-to-wiki-nightly-ingest` (append ` fail`
if the run errored). Daily Central reads this stamp; without it the task shows as never-run.
