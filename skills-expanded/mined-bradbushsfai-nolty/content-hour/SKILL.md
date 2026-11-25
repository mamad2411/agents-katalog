---
name: content-hour
description: Weekly content planning — ranks ideas from your idea library, selects N posts, then drafts collaboratively with the user. EXAMPLE.
---

# Content Hour (example)

> **EXAMPLE.** Heavy multi-step skill demonstrating: file-walking, ranking, news-research, interactive draft, file write-back, sheet write-back, Telegram. Most complex example in the toolkit.

Spawn an Opus sub-agent (high effort) if `[cron ...]` suffix present.

## Setup

This skill assumes you maintain an Obsidian-style content idea library:

```
YOUR_OBSIDIAN_VAULT/Marketing/Content/
├── Personal_Stories.md
├── Ideas/
│   ├── Personal Stories or Ideas.md
│   ├── Pillar-A/
│   │   └── *.md   (one idea per file)
│   ├── Pillar-B/
│   └── Pillar-C/
├── Planned/       (drafted, not yet published — files: YYYYMMDD - Title.md)
└── Published/     (live posts)
```

You also maintain a Google Sheet tracking each post's metadata (`YOUR_SHEET_ID`, sheet `Post Tracking`).

## Procedure

### STEP 0 — Check if already done

Compute the upcoming Tue/Wed/Thu dates (or your publishing cadence):

```bash
TZ='America/Chicago' python3 -c "
from datetime import datetime, timedelta
now = datetime.now()
days_ahead = (1 - now.weekday()) % 7
if days_ahead == 0: days_ahead = 7
tue = now + timedelta(days=days_ahead)
wed = tue + timedelta(days=1)
thu = tue + timedelta(days=2)
for d in [tue, wed, thu]:
    print(d.strftime('%Y%m%d'))
"
```

Check BOTH folders for posts matching those dates:

```bash
ls YOUR_OBSIDIAN_VAULT/Marketing/Content/Planned/ | grep -E "^(D1|D2|D3)"
ls YOUR_OBSIDIAN_VAULT/Marketing/Content/Published/ | grep -E "^(D1|D2|D3)"
```

**If ANY posts for the upcoming week already exist → exit silently.** Content is already created or shipped.

### STEP 1 — Read every idea file

Read EVERY file (don't skim, don't guess from filenames). Use Read tool on each.

- `Personal_Stories.md` — your story library
- `Ideas/Personal Stories or Ideas.md` — loose ideas
- Every `.md` in each pillar subfolder

For each idea, extract: title, pillar, core angle, whether it references a personal story.

### STEP 2 — Read ALL published posts

List ALL `.md` files in `Published/`. Read EVERY one. Note title and topic.

**CRITICAL: Any candidate whose topic substantially overlaps with ANY published post is ELIMINATED.** No time cutoff. If you wrote about it 6 months ago, don't pick it again.

### STEP 3 — Research current news hooks

Use Web search to find this week's news in your industry/niche. Verify claims before presenting — don't relay unverified search results as fact.

Pick 3-5 specific news hooks with sources.

### STEP 4 — Rank and pick

Rank surviving candidates by:
- **ICP fit** — who you're writing for
- **Timeliness** — connects to a news hook?
- **Personal story** — real experiences > generated ideas
- **Variety** — don't pick 3 of the same angle

Pick the best 3 for the upcoming Tue/Wed/Thu slots, plus 3 backups.

### STEP 5 — Telegram the user with picks

```
🎙 *Content Hour — Ready for our weekly session!*

*I read:*
• [N] idea files across [N] pillars
• Personal Stories ([N] stories)
• [N] published posts (ALL time) to avoid repeats

*Top shortlist, ranked:*
1. [title] — [one-line angle]
...

*My picks for Tue/Wed/Thu:*
• *Tue [date] (carousel):* [title] — [why]
• *Wed [date] (text+image):* [title] — [why]
• *Thu [date] (data-image):* [title] — [why]

*Timely hooks this week:*
• [news 1]
• [news 2]

*Intentionally avoided:*
• [topic] — [reason]

Reply `go` to draft all 3, or tell me what to swap.
```

`reply` MCP with `chat_id` from `USER.md`. Wait for the user's response.

### STEP 6 — Draft (when user says `go`)

For each pick:

a. **Read source material** — the idea file + any referenced personal story.
b. **Draft + humanize** — write a first draft. If you've installed a "humanizer" skill that removes AI tells (em-dash overuse, rule-of-three patterns, vague attributions, etc.), run the draft through it. The [`humanizer`](https://github.com/anthropics/claude-code-skills) skill on Anthropic's marketplace is a good starting point. Skip if you don't have one — the draft is still useful, just less polished.
c. **Format** — apply your platform's formatting (Unicode bold, hashtags, your CTA footer).
d. **Iterate with the user** — present the formatted draft, get feedback, iterate until approved.
e. **Save** to `Planned/YYYYMMDD - Title.md` with frontmatter (post_date, check_date, title, pillar, format, hook_style, length).
f. **Write tracking sheet row** via `/opt/homebrew/bin/gog sheets append`.

### STEP 7 — After all approved

Telegram:

```
✅ *Content Hour — 3 posts drafted*

Saved to Planned/:
• Tue [date] — [title]
• Wed [date] — [title]
• Thu [date] — [title]

[Next steps: create graphics, schedule, move to Published/.]
```

End with `CONTENT_HOUR_DONE`.

## Hard rules

1. **Never fabricate personal stories.** Only use details explicitly written in source files. Use `[USER: add your experience here]` for missing specifics.
2. **Quiet hours don't apply** — content hour is time-triggered and the user expects it.
3. **Fail loud, not silent.** If something breaks, Telegram with specifics.
4. **Read ALL published posts.** No time cutoff.
5. **Verify news claims** before presenting.
