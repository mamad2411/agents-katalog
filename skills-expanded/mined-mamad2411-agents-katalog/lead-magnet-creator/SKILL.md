---
name: lead-magnet-creator
description: Build a generous, on-brand lead magnet in any format. Notion page, Google Doc, PDF, Google Sheet, Claude Code Skills repo, GitHub starter, custom GPT, web tool, video, or a vault bundle of several. Format is the first decision, not a default. After the asset is built, the skill logs it in the Notion Content DB, mirrors it to Drive's "Lead Magnets" folder where it makes sense, and offers to chain into /linkedin-copywriter for the launch post. Use when asked to "create a lead magnet", "build a free guide / playbook / checklist / template / GPT / sheet / repo", "make a vault asset", "ship a free resource", "drop a free thing on LinkedIn", or "/lead-magnet-creator".
---

# lead-magnet-creator

Build a free asset you can give away on LinkedIn / X / your website
without holding anything back. Generosity is the brand. The asset answers
the question. The CTA at the end is soft.

**Format is a decision, not a default.** A lead magnet can be:

- a Notion page
- a Google Doc
- a designed PDF
- a Google Sheet (calculator, scorecard, tracker)
- a Claude Code Skills repo (installable into a reader's `.claude/skills/`)
- a GitHub starter repo (code drop, n8n template, agent template)
- a custom GPT
- a small interactive web tool (audit, calculator)
- a recorded video / Loom (the asset IS the video)
- a vault bundle (3-5 of the above behind one CTA)

Voice anchors live in `corpus.md`. Creative magnet ideas live in
`ideas.md`. If you have an existing vault, paste 2-4 of its strongest
components into `corpus.md` so the skill grounds new magnets in your
voice.

---

## When to invoke

Triggers:
- "create a lead magnet for X"
- "build a free guide / playbook / checklist / template"
- "make a vault asset"
- "drop a free PDF / Notion / sheet / GPT / repo on Y"
- "ship a free resource"
- "/lead-magnet-creator"

Skip for:
- Sales proposals → `/proposal-creator`
- Slide decks → use a deck template
- LinkedIn / X posts → `/linkedin-copywriter` or `/x-copywriter`
- Motion videos → `/launch-video`
- Live talking-head edits → `/video-use`

If the user asks for the magnet AND the launch post, do the magnet here,
then chain to `/linkedin-copywriter` at step 7.

---

## The generosity contract

Hard rules that hold across every format:

- **No gated middle.** The asset answers its own headline. Don't tease
  ("download to learn the 3 secrets"). Put the 3 secrets on the page.
- **Real prompts, real tools, real URLs, real numbers.** Verbatim. Inline
  the entire ChatGPT system prompt, the GitHub repo URL, the live
  pricing.
- **Working artifacts, not screenshots of working artifacts.** If the
  magnet promises a Notion template, link the public Notion URL. If it
  promises a GPT, link the GPT. If a Sheet, link the Sheet.
- **One soft CTA at the end, not interrupting.** Default close:
  > Stuck? Hit me up: <YOUR_EMAIL> · <YOUR_CAL_LINK>
- **Distribution defaults to ungated** when "be generous" is the brief.
  Comment-keyword DMs are fine for the launch post (engagement boost),
  but the asset should also live at a public URL anyone can grab without
  commenting.

If a brief asks you to gate the middle, push back once. Then comply.

---

## Workflow

The envelope is the same regardless of format. Step 2 forks into the
per-format pipelines below.

### 1. Brief (single batched ask)

```
Quick brief.

1. What's the magnet about? Outcome promise in one sentence. Not the
   topic, the result. ("Book 14 sales calls in 2 weeks on LinkedIn"
   beats "LinkedIn outbound guide".)
2. The single specific story or number that anchors it. ("85 calls /
   80k emails / 1 client / Claude Code repo.")
3. Format. Pick one or stack: Notion page · Google Doc · PDF · Sheet ·
   Claude Code Skills repo · GitHub starter · custom GPT · web tool ·
   video / Loom · vault bundle.
4. Distribution: ungated public link, gated comment-keyword DM, or both?
5. Voice: operator-voice body (default) or AUTHOR-voice throughout?
6. Anything off-limits (NDA, pre-launch features, client names)?
```

If the user already gave enough context, skip the prompt and parse.
Only ask follow-ups for missing fields.

### 2. Pick the format(s)

See **Format catalogue** below. Multiple formats stack into a vault
bundle (e.g., "PDF + Notion template + GPT" is fine, treat as a bundle).
There is **no default**; ask if it isn't in the brief.

### 3. Make the folder

Create one folder per magnet at `lead-magnets/<magnet-slug>/`. The
folder holds the source files (HTML, .md, .py, .json, etc.) and any
local renders. The slug is kebab-case, descriptive, no date.

```bash
mkdir -p lead-magnets/<magnet-slug>
```

### 4. Author the content

See the per-format pipelines below. Apply the voice rules from
`corpus.md`. Run the slop scrub before report-done.

### 5. Publish

Each format has its own destination. The skill should always end with a
**single canonical public URL** that you can paste into LinkedIn, the
website, or a comment-keyword DM. That URL goes in the Notion row and
in the launch post.

### 6. Log in Drive + Notion

**Drive** (when the format produces a file):
- Destination: your Lead Magnets folder
  (folder id `<YOUR_DRIVE_LEAD_MAGNETS_FOLDER>`)
- Filename: `<YOUR_BRAND> · <Title> · YYYY-MM-DD.<ext>`
- Upload via `mcp__claude_ai_Google_Drive__create_file`. Capture the
  `viewUrl`.

For formats that don't produce a file (live Notion page, GPT, repo, web
tool), skip the Drive step. The Notion row holds the public URL
directly.

**Notion Content DB** (always):
- Data source ID: `<YOUR_NOTION_CONTENT_DB_ID>`
- **Title**: same as the file name minus the date and extension (or the
  magnet's display title for non-file formats)
- **Format**: `Lead Magnet`
- **Channel**: `LinkedIn` default · ask if multi-channel
- **Pillar**: `Educational / Tactical` default · see `ideas.md` for
  the full pillar map
- **Status**: `Idea` if no launch yet · `Scripting` if launch post in
  draft · `Scheduled` if launch post queued
- **Drive Assets**: Drive `viewUrl` if Drive-backed, else the canonical
  public URL of the asset
- **Page body**: 1-paragraph summary, the comment-keyword (if gated),
  the public URL, and the magnet's outcome promise. Leave space below
  for the launch-post draft, hooks, and metrics.

### 7. Offer to chain into the launch post

Once the magnet is live, ask:

> Want me to draft the launch post? `/linkedin-copywriter` can pick the
> right hook (R.I.P. for vault drops, "concrete result + tool" for
> playbooks). I'll seed it with the magnet's outcome promise, the
> public URL, and the comment-keyword if gated.

Same offer for `/x-copywriter` and `/repurpose`.

### 8. Report back

Closing summary, max 5 lines:
- Path to local source folder
- Canonical public URL of the magnet
- Drive URL (if applicable)
- Notion row URL
- Suggested next action (chain a launch post · queue another magnet ·
  add to bio / featured section / website)

---

## Format catalogue

Each format is fully self-contained: its own authoring path, its own
distribution, its own publish step. Pick the format that fits the
content. **None of these is the default.**

### A. Notion page

The most native long-form format. If you have an existing Notion-based
vault, link it here so new magnets inherit its structure.

**Pick when:** the content is naturally hyperlinked, includes screenshots
inline, references other Notion pages, or is going to be updated as
state changes. Long-form playbooks are very natural here.

**Authoring:**
- Source of truth lives at `lead-magnets/<slug>/page.md` (markdown so
  the source is reviewable in git and the LLM can refactor it without
  hitting Notion's API for every paragraph).
- Use the section structure from `corpus.md` (outcome-promise headers,
  empathy opener, stats blocks, two-tier framings, verbatim prompts).
- Link companions inline (GPT URL, Sheet URL, GitHub repo, Cal link).

**Publish:**
1. Use `mcp__claude_ai_Notion__notion-create-pages` to create the
   Notion page under a parent you control (your Marketing Content
   parent: `https://www.notion.so/<YOUR_NOTION_MARKETING_PARENT_ID>`).
2. Convert the markdown to Notion blocks (the MCP accepts enhanced
   markdown).
3. Make the page public-shareable via the Notion UI (currently manual
   from the Share menu) or, if the MCP supports it, via the API.
4. Capture the public Notion URL.

**Drive logging:** export the page to PDF (Notion UI) once it's stable
and upload that PDF as a snapshot. The live URL is the canonical asset;
the PDF is just a backup.

**Notion row Drive Assets:** the public Notion URL (not the PDF).

### B. Google Doc

Pick when the magnet wants to feel like a Doc you can scribble in.
Comments enabled, version history visible. Reads as collaborative.

**Authoring:**
- Source: `lead-magnets/<slug>/doc.md`
- Same voice rules as the Notion page. Use plain markdown headings,
  bullets, code blocks. No HTML.

**Publish:**
1. Render the markdown to a clean `.docx` via `python-docx` (the same
   library `proposal-creator` uses for clean-text proposals).
2. Upload to Drive (Lead Magnets folder) with
   `mimeType: application/vnd.google-apps.document` so Drive converts
   to a native Google Doc on ingest.
3. Set sharing to "anyone with the link can view" via the Drive
   `permissions` API.
4. Capture the Doc's `viewUrl`. That's the canonical public URL.

**Drive logging:** the Doc itself lives in Drive.

**Notion row Drive Assets:** the Drive view URL.

### C. PDF

Designed brand asset. Use this when the magnet doubles as a portfolio
piece (cover that looks great in a screenshot, dot-grid backdrop,
brand mark in the header, accent moment per page).

**Authoring:**
- Source: HTML at `lead-magnets/<slug>/magnet.html` plus
  `_print.css`. If you have a proposal/print template, mirror it.
- 6-10 letter pages, one `<section class="page">` each.
- Component classes from `<YOUR_BRAND_TOKENS_PATH>` if you have a
  tokens file (cards, kicker rules, mini table, pills, two-col,
  three-col).
- Inline your brand mark SVG in each page header.

**Publish:**
1. Render to PDF via headless Chrome:
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
     --headless --disable-gpu --no-pdf-header-footer \
     --print-to-pdf-no-header \
     --print-to-pdf="lead-magnets/<slug>/magnet.pdf" \
     --virtual-time-budget=2000 \
     "file://$PWD/lead-magnets/<slug>/magnet.html"
   ```
2. Smoke checks:
   - `grep -c '—' lead-magnets/<slug>/magnet.html` must be 0
   - `grep -n '{{' lead-magnets/<slug>/magnet.html` must be empty
   - Visual: cover headline 2 lines, second line muted; one accent
     moment per page max; footer page numbers correct.
3. Upload PDF to Drive Lead Magnets folder.

**Drive logging:** the PDF file.

**Notion row Drive Assets:** Drive view URL of the PDF.

**Brand defaults** (cover page):
- Edition pill: `<YOUR_BRAND> Vault · NN`
- Two-line hero: `[outcome].<br/><em>[mechanism].</em>`
  (period at end of each line)
- One accent moment max per page.

### D. Google Sheet

Pick for calculators, scorecards, signal trackers, ICP definers,
acquisition models · anything where the value is "punch in your numbers
and see your answer".

**Authoring:**
- Source: `lead-magnets/<slug>/sheet.py` builds the `.xlsx` via
  `openpyxl`. Sheet structure (column headers, formulas, validation,
  named ranges) lives in code so it's diffable.
- Add a "Read me first" tab with the outcome promise, instructions,
  and the Cal-link CTA.

**Publish:**
1. Run `python3 sheet.py` → produces `<slug>.xlsx`.
2. Upload to Drive (Lead Magnets folder) with
   `mimeType: application/vnd.google-apps.spreadsheet` so Drive converts
   to a native Google Sheet.
3. Set sharing to "anyone with the link can VIEW" (not edit · the
   reader makes a copy to use).
4. Capture the Sheet `viewUrl`.

**Drive logging:** the Sheet lives in Drive.

**Notion row Drive Assets:** the Drive view URL.

### E. Claude Code Skills repo

A public GitHub repo of installable Claude Code skills. The most
operator-grade magnet for the AI-engineering ICP. Reader runs `git clone`
into their `~/.claude/skills/` and instantly has the same patterns you
use.

**Pick when:** the value is repeatable behavior, not a one-off
artifact. Examples: a `/cold-email` skill that drafts cold emails in a
specific style, a `/icp-audit` skill that scores a website against a
checklist, a `/gtm-stack-picker` skill.

**Authoring:**
- Source: `lead-magnets/<slug>/skills/<skill-name>/SKILL.md` per skill,
  plus a top-level `README.md` explaining the install and the
  catalog.
- Each `SKILL.md` follows the standard structure (frontmatter `name` +
  `description`, body with When-to-invoke, Workflow, Voice rules, Don'ts,
  Reference files).
- Include voice / brand rules so installed skills produce
  on-brand output for the reader.
- Add a `LICENSE` (MIT or 0BSD) so reuse is unambiguous.

**Publish:**
1. Create the GitHub repo manually, push the code from the local
   folder, mark it public.
2. The README links your Cal and `<YOUR_EMAIL>` for support.
3. Optional: open-source license badge, install instructions
   (`git clone … ~/.claude/skills/<name>`), version tags.

**Drive logging:** none. The repo URL is the canonical asset.

**Notion row Drive Assets:** the GitHub repo URL.

### F. GitHub starter repo

Code drop. Different from Skills repos: this is one project the reader
clones, sets up, and runs (e.g., a cold-email system, an n8n template,
a Trigger.dev agent template, a Notion-to-LinkedIn syncer).

**Authoring:**
- Source: full project tree at `lead-magnets/<slug>/repo/`.
- README explains setup, env vars, run command, expected output.
- Working `.env.example`, no real keys.
- A 1-page PDF or Notion page may accompany the repo as a high-level
  walkthrough · that's a vault bundle, see format J.

**Publish:**
- Create the GitHub repo manually, push from the local folder, mark
  it public.
- Optional: include a Loom walkthrough URL in the README.

**Drive logging:** none. Repo URL is the asset.

**Notion row Drive Assets:** the repo URL.

### G. Custom GPT

A repeat-use tool the reader pins in their ChatGPT sidebar. Audits,
rewriters, coaches, idea generators.

**Authoring:**
- Source: `lead-magnets/<slug>/gpt-spec.md` with all OpenAI fields:
  - Name, description (under 300 chars), instructions (the full system
    prompt · this is the asset, write it carefully)
  - 4 conversation starters
  - Knowledge files to upload (list by relative path · the actual files
    sit in `lead-magnets/<slug>/knowledge/`)
  - Capabilities toggles (Web · Image · Code Interpreter · Canvas)
- The system prompt should reference your brand by name, link
  `<YOUR_DOMAIN>`, and end with the soft Cal CTA.

**Publish:**
- The skill cannot create GPTs (OpenAI requires the manual UI).
- Output: a `gpt-spec.md` you copy-paste into the GPT builder. After
  you hit "Publish", paste the GPT URL back into the magnet's
  notes file (or the Notion row directly).

**Drive logging:** upload `gpt-spec.md` as a backup to Drive.

**Notion row Drive Assets:** the live GPT URL once published.

### H. Web tool

Small interactive page hosted at a public URL. Examples: cold-email
score, acquisition calculator, profile audit submit-form, "battle
royale" rewrite-vote.

**Authoring:**
- Source: `lead-magnets/<slug>/web/` (single-page or a tiny app).
- Stack: Next.js + Vercel deploy, or static HTML + a webhook for any
  backend logic.
- Use your brand tokens if you have a `<YOUR_BRAND_TOKENS_PATH>`.

**Publish:**
- Deploy to Vercel under `<YOUR_DOMAIN>/free/<slug>` or a subdomain.
- Link must be the canonical URL (no `*.vercel.app` in production).

**Drive logging:** none. Public URL is the asset.

**Notion row Drive Assets:** the production URL.

### I. Video / Loom

The asset is the video. Examples: a 5-minute Loom walkthrough of a
system, a 30-minute recorded webinar, a "roast my profile" Loom each
applicant gets back.

**Authoring:**
- For polished motion graphics → use `/launch-video` instead, that's
  the right tool.
- For Loom-style walkthroughs → record manually. The skill produces a
  `script.md` outline (hook, beats, close) and a thumbnail brief.
- For talking-head edits of raw footage → use `/video-use` instead.

**Publish:**
- Loom: record, set to "public" sharing, capture the share URL.
- YouTube: upload as Unlisted (default) or Public, capture URL.
- Vimeo: same.

**Drive logging:** upload the MP4 to your Videos folder
(folder id `<YOUR_DRIVE_VIDEOS_FOLDER>`) for archival. The live
URL (Loom / YouTube / Vimeo) is the canonical asset.

**Notion row Drive Assets:** the public video URL.

### J. Vault bundle

3-5 of the formats above behind one comment-keyword. A classic vault
shape is 5 PDFs (or a mix of PDF + Notion + GPT) gated behind one
comment-keyword.

**Authoring:**
- Each component lives in its own subfolder under
  `lead-magnets/<vault-slug>/`. E.g.,
  `lead-magnets/vault-v2/{playbook-pdf, signal-library-notion, stack-picker-sheet, audit-gpt-spec, content-system-skills}/`.
- A top-level `index.md` (or one wrapping Notion page) lists all
  components with one-line outcome promises and public URLs.

**Publish:**
- Each component publishes via its own format's pipeline.
- The wrapper Notion page (or PDF) ties them together.
- Distribution is one comment-keyword that DMs the wrapper URL.

**Drive logging:** mirror each component to Drive per its format. Add a
top-level "vault index" PDF or Notion page as the wrapper.

**Notion row Drive Assets:** the wrapper URL. Add per-component URLs in
the page body.

---

## Voice rules (apply to every format)

The voice has two registers. Switch happens between sections, not
mid-paragraph.

- **AUTHOR voice** = the founder/operator voice from your
  `linkedin-copywriter` corpus. Personal. Story-led. Hook-driven.
  Use this on the cover, the opening page, and the closing CTA.
- **OPERATOR voice** = more runbook than LinkedIn post. Outcome-promise
  headers, imperative verbs, numerals, bullets, verbatim prompts and
  screenshots. Use this in the body.

### Cover / opening (AUTHOR voice)

Read `corpus.md` first. Pull the hook pattern from a matched anchor
magnet. Default patterns:

- **Concrete result + tool** ("85 sales calls. From 80,000 cold emails.")
- **Achievement + timeframe** ("How to book 14 sales calls in 2 weeks
  on LinkedIn without needing to go viral.")
- **R.I.P. [Role/Industry]** for vault drops.
- **Stat opener with payoff** ("Last month I generated +110k impressions.
  Here's the profile system that converted them.")

### Body (OPERATOR voice)

The body is closer to a runbook than a LinkedIn post. Anchor on the
operator-voice register from `corpus.md`.

- **Section headers are outcome promises**, not feature labels.
- **Numerals beat adjectives.**
- **Imperative verbs.** Drop hedges.
- **One thought per paragraph.** Most paragraphs 1-3 lines.
- **Bullets carry the load.** Pick `-`, `→`, or `•` and stay
  consistent within the magnet.
- **Real screenshots / examples / prompts.** Verbatim. No paraphrase.

### Close (AUTHOR voice)

Steal verbatim:

> **Stuck?** Hit me up. `<YOUR_EMAIL>` · `<YOUR_CAL_LINK>`

Optionally append `:)` if the magnet has a casual register.

### Slop scrub (mandatory before report-done)

Run the linkedin-copywriter blacklist against the magnet content.
Highlights: no em dashes (—), no "leverage", no "robust", no "delve",
no "powerful", no curly quotes, no `…` ellipsis, no TL;DR headers, no
keycap emoji as numbered headers (1️⃣).

---

## Brand and design

When the format renders into a designed surface (PDF, web tool, Sheet
header, video thumbnail, Notion cover image), inherit from
`<YOUR_BRAND_TOKENS_PATH>` if you have a tokens file. Recommended token
set if starting from scratch:

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#fafafa` | page bg |
| `--surface` | `#ffffff` | cards, callouts |
| `--ink` | `#0a0a0a` | primary text + numerals |
| `--ink-soft` | `#3f3f46` | body copy |
| `--muted` | `#71717a` | captions, micro-labels, "em" half of two-line headlines |
| `--line` | `#e4e4e7` | borders |
| `--accent` | `#10b981` | the one accent, used once per surface |

Adapt the palette to your brand. The pattern that matters is **one
accent moment per surface**, used for meaning.

For non-designed formats (Google Doc, plain GitHub README), don't try
to brand the body. Brand stamps are the title, the closing CTA, and
the link to `<YOUR_DOMAIN>`.

If you have a brand mark SVG, inline it when needed (PDF, web,
Sheet header image, video).

---

## Distribution modes

**Ungated public link** (default for "be generous" briefs):
- A canonical URL anyone can grab without commenting.
- Examples per format:
  - Notion page: the public Notion URL.
  - Google Doc / Sheet: the Drive view URL.
  - PDF: the Drive view URL OR a public route on `<YOUR_DOMAIN>/free`
    once that route exists.
  - GitHub repo: the repo URL.
  - GPT: the GPT share URL.
  - Web tool: the production URL.
  - Video: the Loom / YouTube / Vimeo URL.
- Linked from LinkedIn featured section, X bio, and the launch post.

**Gated comment-keyword DM**:
- Reader comments a keyword (`Claude GTM`, `BOOKS`, `GROWTH VAULT`).
  Bot or you DM the canonical URL.

**Both** (recommended default for launch posts):
- Public URL in bio / website / featured section.
- Comment-keyword on the launch post specifically, for engagement lift.

The skill records the comment-keyword and the canonical URL in the
Notion row's page body so `/linkedin-copywriter` can pull both into the
launch post draft.

---

## Defaults

| Field | Default |
|---|---|
| Edition pill (PDF / Notion cover) | `<YOUR_BRAND> Vault · NN` (count Notion Content rows where Format=Lead Magnet, increment) |
| Date | Today's ISO date on file names; written-out date on cover |
| Cal link | `<YOUR_CAL_LINK>` |
| Email | `<YOUR_EMAIL>` |
| Distribution | Both (ungated link + comment-keyword) |
| Voice mix | AUTHOR voice on opening + close, OPERATOR voice on body |
| Banned-word check | Mandatory before report-done |
| Repo license | MIT or 0BSD for Skills / starter repos |

---

## Don'ts

- **Don't default to PDF** when the content is more naturally a Notion
  page, a Sheet, a repo, or a GPT. Pick the format that fits the
  content; ask the user if it's not in the brief.
- **Don't gate the middle.** The asset answers its own headline.
- **Don't use em dashes.** Replace with periods, commas, colons,
  middot, or parens.
- **Don't fabricate stats or client names.** If a number is a benchmark
  range, label it as such.
- **Don't ship without the canonical public URL.** Every magnet ends
  with one URL the launch post can paste.
- **Don't promise URLs that don't exist yet** (e.g.,
  `<YOUR_DOMAIN>/free/<slug>`). Use the actual host until the route is
  live.
- **Don't ship a screenshot when you could ship the artifact.** A
  screenshot of a Notion template is worse than a public Notion link.
- **Don't write "TL;DR" or "key takeaways".** The magnet is the
  takeaway.
- **Don't cross voice registers within a body section.** Switch happens
  between sections, not mid-paragraph.

---

## Reference files

- `corpus.md`. Voice anchors pulled from your existing vault. Re-read
  before drafting. If empty, see `corpus.md.example` for the format.
- `ideas.md`. 30+ magnet ideas, indexed by format.
- Sister skills:
  - `proposal-creator/SKILL.md` for the .docx + Drive upload pattern.
  - `linkedin-copywriter/SKILL.md` for hook patterns and the slop
    scrub.
  - `launch-video/SKILL.md` for motion-graphics videos.
  - `video-use/` for talking-head edits of raw footage.
- Brand tokens: `<YOUR_BRAND_TOKENS_PATH>` (if you have one).
- Brand design system: `<YOUR_BRAND_DOC>` (if you have one).

---

## After the magnet ships

Offer (don't auto-do):

- Draft the launch post via `/linkedin-copywriter`
- Draft the X version via `/x-copywriter`
- Spin up additional channels via `/repurpose`
- Add to LinkedIn featured section, X bio, website footer
- Schedule a 2-week metrics check via `/schedule`
- Commit the magnet folder (`git add lead-magnets/<slug>/ && git commit`)
- Update a future "Vault index" Notion page when the magnet count
  crosses 5
