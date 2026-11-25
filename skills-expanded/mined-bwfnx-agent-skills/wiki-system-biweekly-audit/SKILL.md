---
name: wiki-system-biweekly-audit
description: Biweekly SBDC wiki health audit — orphans, broken links, stale entries, synthesis gaps
---

> **Schedule:** Every two weeks
> **Needs:** workspace files, Drive
> **Helper scripts (yours, not included):** _backup-2026-07-28/linkaudit.py, build-sbdc-wiki-fieldmanual.py, check-wiki-publish.py, handoff_prepend.py, wikisync.py

# SBDC Wiki System Biweekly Audit

## Objective

Audit the health of the SBDC wiki system. Identify orphaned files, broken internal links, stale articles, synthesis gaps, and structural issues. Report-only — do not auto-fix.

**Scope: SBDC wiki only.**

**Audit the CANONICAL copy, not Google Drive** (architecture changed 2026-07-28): the wiki lives at `{{WORKSPACE_ROOT}}/sbdc-advising/wiki/`. Drive's `wiki\` is a read-only ingest inbox and will legitimately lag the repo — auditing it produces false findings. `python3` is not on PATH; use `py`.

**Run the real tooling first — it answers most of this audit mechanically:**

```
cd "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/wikisync.py check                    # junction, shadows, undrained Drive, git, stale HTML, render coverage
py {{WORKSPACE_ROOT}}/check-wiki-publish.py                # NAV_SECTIONS coverage, built HTML, dangling [[wikilinks]], publish guard (Step 6)
```

`{{WORKSPACE_ROOT}}/_backup-2026-07-28/linkaudit.py` used to sit here; it no longer exists anywhere in the
Playground (confirmed 2026-09-13) and its checks are covered by the two scripts above plus
the three-way INDEX.md compare in Step 1. Do not go looking for it.

- The markdown folder is **not** what gets published. The builder renders only slugs listed in `NAV_SECTIONS`; trust the "render coverage" section of `{{WORKSPACE_ROOT}}/wikisync.py check` and the publish guard for what is actually live.
- An article may use `## Related Wiki Articles` instead of `## Related Topics`. Either is fine; do not flag the heading name.
- `synthesis-journal` is a deliberate exception to both the orphan and Related-Topics rules. Do not flag it.

## Step 1 — Inventory

1. List all files in `{{WORKSPACE_ROOT}}/sbdc-advising/wiki/`.
2. Read `INDEX.md` to get the advertised article list.
3. Compare three sets, not two: files on disk, INDEX.md rows, and `NAV_SECTIONS` slugs in `{{WORKSPACE_ROOT}}/build-sbdc-wiki-fieldmanual.py`. A file missing from NAV_SECTIONS is invisible in the published Field Manual even if INDEX.md advertises it — that is the more serious finding, and it is what the "render coverage" check reports.

## Step 2 — Link integrity

For each wiki article, scan for internal wiki links (`[[article-name]]` style references). Check that every referenced article exists in the wiki/ folder. Flag broken links.

## Step 3 — Staleness check

Check each article's last-modified date via git in the repo (`git log -1 --format=%ad -- <file>`), not Drive mtimes — Drive lags by design now and its timestamps are meaningless for staleness. Flag articles not modified in 60+ days as potentially stale. Cross-reference with `synthesis-journal.md` — if the journal references an article that hasn't been updated, that's a stronger staleness signal.

## Step 4 — Synthesis coverage

Read the last 3 entries in `synthesis-journal.md`. Identify wiki articles that are never referenced in any synthesis entry — these may represent gaps in cross-cutting analysis.

## Step 5 — Structural consistency

Spot-check 5-10 articles for:
- Missing or inconsistent heading structure
- Articles that are very short (< 200 words) and may need expansion
- Articles that are very long (> 3000 words) and may need splitting
- Missing `<!-- Source: ... -->` provenance comments

## Step 6 — Publish guard (automated, MUST run)

Steps 1–5 are largely manual and judgment-based. This step is neither: it is a
script that exits non-zero, and it covers the two failures that are **silent by
construction** — the repo looks healthy, git is clean, the deploy is green, and
the thing is still wrong.

- **Committed but invisible.** An article renders only if its slug is in
  `NAV_SECTIONS`. On 2026-08-10, `agentic-ai`, `small-business-cybersecurity`, and
  `data-security-and-client-file-handling` had been committed and deployed for
  weeks while rendering nowhere, with 23 inbound `[[wikilinks]]` pointing at them.
- **Committed and therefore public.** Every tracked file under the publish dir is
  fetchable by direct URL unless `sbdc-advising/_redirects` blocks it. That guard
  drifted three times as a deny-list before being inverted to a default-closed
  allow-list on 2026-08-10.

```
cd "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/check-wiki-publish.py
```

- **Exit 0** — record "publish guard: OK" plus the warning count.
- **Non-zero** — this is the headline finding. Reproduce every `[FAIL]` line
  verbatim under "Publish Guard" and list it first under Recommended Actions. Do
  not summarize or soften them; each names the exact file and the fix.
- **`WARN` lines never fail the run** but still belong in the report. A dangling
  `[[wikilink]]` blanks the reading pane silently rather than showing an error.

The guard supersedes the "render coverage" caveat noted above: it reconciles files
on disk, `NAV_SECTIONS`, and the article divs actually present in the built HTML,
so it catches a stale build that the other two checks would pass.

## Output

Save to `{{WORKSPACE_ROOT}}/sbdc-advising/outputs/wiki-audit-YYYY-MM-DD.md`
(every run since 2026-08-17 has landed there; Drive has no git and is not the canonical home):

```
# SBDC Wiki System Audit — YYYY-MM-DD

## Summary
- Publish guard: OK / **FAIL (X failures, Y warnings)**   <- lead with this
- Total articles: X
- Orphaned files: X
- Broken INDEX.md references: X
- Broken internal links: X
- Unreachable articles (exist but do not render): X
- Stale articles (60+ days): X
- Never-synthesized articles: X
- Structural issues: X

## Publish Guard
[Verbatim [FAIL] and [WARN] lines from {{WORKSPACE_ROOT}}/check-wiki-publish.py, or "exit 0 — OK".
 Empty only if the script could not be run, in which case say why.]

## Orphaned Files
[Files in wiki/ not listed in INDEX.md]

## Broken References
[INDEX.md entries with no corresponding file]

## Broken Internal Links
| Source article | Broken link | Suggested fix |
|----------------|-------------|---------------|

## Stale Articles
| Article | Last modified | Days stale | Notes |
|---------|--------------|------------|-------|

## Synthesis Gaps
[Articles never referenced in synthesis-journal.md]

## Structural Issues
| Article | Issue | Suggestion |
|---------|-------|------------|

## Recommended Actions
[Prioritized list of fixes {{USER}} should consider]
```

## Safety Rules
- Read-only. Do not modify any wiki files.
- Do not rebuild HTML or push to GitHub — this is an audit only.
- **HANDOFF-LOG.md:** write your entry to a temp file and run
  `py "{{WORKSPACE_ROOT}}/handoff_prepend.py" <that-file>`.
  Never open HANDOFF-LOG.md with PowerShell `Get-Content` / `Set-Content` / `Add-Content` /
  `Out-File`, and never rewrite it with any editor. The 2026-09-13 run did, and Windows
  PowerShell re-encoded the whole file (every em dash became mojibake, plus a BOM). If the
  helper is missing, append your entry as a separate file `handoffs/<date>-wiki-audit.md` instead.