---
name: co-working-hour-guide-rebuild
description: Bring the published AI Co-Working Hour Guide up to date with any sessions processed since the last run
---

> **Schedule:** Tuesday, 1:00 AM ET, weekly
> **Needs:** Gmail, workspace files, Zoom, Drive
> **Helper scripts (yours, not included):** none

# AI Co-Working Hour Guide — Catch-Up Rebuild

## What changed and why (2026-08-11)

This task previously described writing `co-working-hour-guide-YYYY-MM.md` to Google Drive
`outputs/`. **No such file has ever existed** — the audit on 2026-08-11 found zero matches in
any month across Drive, Playground, and the repo. The task was writing a document nobody
reads to a location nobody checks.

The artifact that actually matters is:

```
{{WORKSPACE_ROOT}}/sbdc-advising/AI-Co-Working-Hour-Guide.html
```

It is served publicly at `marylandsbdcwiki.netlify.app/ai-co-working-hour-guide` (allow-listed
in `sbdc-advising/_redirects`) and **embedded in the SBDC Claromentis intranet for the AI
team.** Before 2026-08-11 it had gone unmaintained since 2026-06-30 while sessions continued —
two full sessions (2026-07-27, 2026-08-10) were missing from a page the team was actively
reading.

The manual chain that keeps breaking is: Gmail Zoom link → download into the raw transcript
folder → process into a wiki-input packet → **update the HTML page** → commit and push. The
first three steps happen. This task exists to close the last two.

## Objective

Find every co-working session that has been processed into a wiki-input packet but is **not
yet on the published HTML page**, add it, and publish. This task is a catch-up, not a
regeneration: it is idempotent, it never rewrites existing cards, and running it twice in a
row is a no-op.

## Step 1 — Find the gap

Newest session already on the page:

```
Select-String -Path '{{WORKSPACE_ROOT}}/sbdc-advising/AI-Co-Working-Hour-Guide.html' -Pattern 'class="session-date"' | Select-Object -First 1
```

Available session packets:

```
Get-ChildItem '{{WORKSPACE_ROOT}}/sbdc-advising/raw/training-media/zoom-archive/05_Wiki Inputs\' -Filter '*chatgpt-co-working-hour*'
```

Every packet dated **after** the newest card on the page is a gap to fill. If there are none,
stop and report "no gap — page is current." That is a successful run, not a failure.

`raw/` is Playground-only and deliberately not in git — use the Playground path for packets and
the `[wiki repo]` path for the HTML.

## Step 2 — Read the primary sources

For each missing session, read **both**:

- `05_Wiki Inputs\<SESSIONID>-wiki-input.md` — the structured packet
- `03_Reviewed Summaries\<SESSIONID>-reviewed-summary.md` — has the participant roster

Get participants from the reviewed summary or the transcript speaker list. **Do not infer
attendance from who was mentioned** — people are discussed who were not in the room. If a
first name has no surname in the summary, resolve it from the transcript rather than guessing
or omitting.

**Honor the packet's own handling notes.** Packets flag items as unverified — the 2026-08-10
packet says of the Claude security-level change: "Do not write it into the wiki as settled
until the internal owner confirms it." Carry that hedge onto the page in the same words'
spirit. Draft policies get summarized, never published as final. A confident wrong fact here
reaches the whole AI team through Claromentis.

## Step 3 — Add the cards

The page is **hand-maintained HTML with no builder script.** Edit it directly, adding content
only, using the classes that are already there.

Session Log is **newest first**. Insert new cards immediately after `<h2>2. Session Log</h2>`,
matching the existing card structure exactly:

```html
<div class="session-card">
  <div class="session-date">Month D, YYYY</div>
  <div class="session-title">Session N — Title</div>
  <div class="participants">Names</div>
  <p>Two paragraphs, matching the density of the existing cards.</p>
  <p><span class="badge badge-tool">Tool</span><span class="badge badge-theme">Theme</span></p>
</div>
```

Then add a matching `evolution-step` at the **end** of the Evolution Arc section (that one is
oldest-first — opposite of the Session Log), and update the header `<div class="meta">` line
and the session count in the Overview paragraph.

> **Never touch the `<style>` block.** Per the root `CLAUDE.md` style rule, the theme is not to
> be changed without an explicit request. Verify after editing that no diff hunk falls before
> the closing `</style>` tag:
> `git -C {{WORKSPACE_ROOT}} diff -U0 -- sbdc-advising/AI-Co-Working-Hour-Guide.html | Select-String '^@@'`

## Step 4 — Verify before publishing

All four must pass:

- Session-card count increased by exactly the number of sessions added
- Evolution-step count matches the session-card count
- `<div>` open/close counts balance, and `<section>` open/close counts balance
- No diff hunk lands inside the `<style>` block

If any check fails, stop and report. Do not push a broken page — it is embedded in an intranet
the team reads.

## Step 5 — Publish

The page is **only live once it is pushed.** Netlify auto-deploys from `main`, and Claromentis
iframes the deployed page — editing the file locally changes nothing that anyone sees.

Run git from `[wiki repo]`, never from Playground, and add the **explicit path only** so an
unrelated dirty file cannot ride along:

```
& 'C:\Program Files\Git\cmd\git.exe' -C '{{WORKSPACE_ROOT}}' add sbdc-advising/AI-Co-Working-Hour-Guide.html
& 'C:\Program Files\Git\cmd\git.exe' -C '{{WORKSPACE_ROOT}}' commit -m "Add <dates> sessions to AI Co-Working Hour Guide"
& 'C:\Program Files\Git\cmd\git.exe' -C '{{WORKSPACE_ROOT}}' push origin main
```

Check `git status --porcelain` first. If a wiki ingest run is mid-flight, wait rather than
committing its partial work.

## Step 6 — Report

State plainly: which sessions were added, which packets were skipped and why, any fact carried
onto the page that the packet flagged as unverified (name it explicitly so {{USER}} can confirm
it), and whether the push succeeded. If there was no gap, say so in one line.

## Cadence

**Tuesday, 1:00 AM ET, weekly** (set 2026-08-11). The previous monthly-on-the-18th schedule
matched nothing — sessions are weekly on Mondays, so a monthly run guaranteed the page trailed
its source by up to four sessions.

Tuesday 1:00 AM lands the run the night after each Monday session. It will often find no packet
yet, because the transcript has not been processed — that is expected and correct. The task is
catch-up-based, so it simply reports "no gap" and picks the session up on a later run once the
packet exists. No session gets skipped by running early.
