---
name: release-calendar
description: >
  Generate a beautiful "Everything [Team] shipped in X days" release calendar poster —
  like the viral Anthropic/OpenAI/Codex shipping velocity images. Given a company name,
  X handles, and date range, this skill pulls real tweets, identifies product releases,
  and renders a brand-matched HTML calendar with team avatars and click-through tweet links.

  Trigger phrases (Chinese 🇨🇳):
  - "帮我做一个 [公司] 的 release calendar"
  - "做一张 shipped in X days 的图"
  - "复刻那张 Anthropic releases 图" / "复刻那张 OpenAI/Codex 图"
  - "做 [产品] 的发布日历" / "[公司]的发布日历"
  - "[公司] 发了多少东西" / "盘点一下 [公司] 发布了什么"
  - "做个发布速度图" / "做个 shipping velocity 图"
  - "给 [公司] 做个日历图"

  Trigger phrases (English 🌍):
  - "release calendar for [company]"
  - "everything [team] shipped in X days"
  - "shipping velocity poster for [company]"
  - "make a calendar of [company] releases"
  - "track [company] product launches"
  - any mention of "shipped calendar", "release poster", "product releases visualization"
  - "how much has [company] shipped"

  Requires: twitter-cli / x-cli (twitter CLI tool), agent-browser
---

# Release Calendar Skill

Generate a "Everything [Team] shipped in X days" calendar poster from real X data.

## Choose the right mode first

Before running the setup wizard, decide whether this is a **new calendar** or an
**incremental update**.

- Use **New Calendar Mode** when the product is not already represented in the
  project data or the user explicitly asks for a new poster/PNG from scratch.
- Use **Incremental Update Mode** when the user asks to update an existing
  calendar, extend the date range, sync recent releases, refresh x-1.dev, or add
  releases since the last update.

Default to Incremental Update Mode if existing release data is present. Do not
redo discovery work just because the skill can do it.

## Incremental Update Mode

Use this path for follow-up updates such as "sync Apr 6-Apr 20 for every
product".

### Inputs to reuse

Read the existing product data first:

```bash
find ximage/web/data/releases -maxdepth 1 -name '*.ts' -print
```

For each existing product, reuse:

- `teamMembers[].handle` as the canonical X account list.
- `teamMembers[].avatar` as the canonical avatar cache.
- `releases[].authorAvatar` for previously known author avatars.
- `brand`, `bg`, `file`, and `logo` from the product data.

Do **not** fetch avatars, logos, or rediscover team members in incremental mode
unless a new posting handle appears in the incremental tweet data and no cached
avatar exists for that handle.

### Incremental fetch rule

Fetch only the missing time window. If the user says "Apr 6-Apr 20", use:

```bash
SINCE=2026-04-06
UNTIL=2026-04-21 # X search until is exclusive, so this includes Apr 20 UTC
```

For each existing handle, fetch post/search data into a windowed cache directory
instead of scattering raw files in the project root:

```bash
WINDOW=".omx/release-calendar/windows/${SINCE}_${UNTIL}"
mkdir -p "$WINDOW/raw" "$WINDOW/reports"

TWITTER_BROWSER=${BROWSER:-chrome} TWITTER_PROXY=http://127.0.0.1:1082 \
  twitter search --from "$handle" --since "$SINCE" --until "$UNTIL" \
  -t latest --max 100 --json > "$WINDOW/raw/${handle}.search.json"
```

If X returns 429 rate limits, do not restart from scratch. Keep successful cache
files, reduce concurrency, and retry only missing **product/official handles**
first. Prefer `twitter user-posts <handle> --max 100 --json` as the fallback for
key handles when `search` is rate-limited.

### Filtering rule

Only append release items that are new and concrete:

- New product/model/platform launch.
- New feature shipped to users.
- Developer API/SDK/tooling release.
- Integration, connector, marketplace, IDE, or workflow launch.
- Meaningful availability expansion (GA, mobile, desktop, region, plan).
- Major usage/download/customer milestone only if the product account presents
  it as a shipping milestone.

Discard opinions, replies without shipped functionality, event reminders,
podcasts, reposts, tutorials, and engagement posts.

Deduplicate by `tweetUrl` first, then by `(date, normalized text)`.

### Update existing data files

Append releases to the relevant `ximage/web/data/releases/<slug>.ts` file and
update:

- `subtitle` day count from first release date to latest release date.
- `dateRange` to the new first/latest month-day span.
- release count is derived from the array; do not store a separate count.

Keep existing manually curated release labels. Do not regenerate older entries or
overwrite existing avatar URLs.

### PNG/HTML rule

For the web app, the canonical source is `ximage/web/data/releases/*.ts`.
Generating HTML/PNG posters is optional in incremental mode unless the user
explicitly asks for refreshed poster images. If posters are generated, write them
under a dedicated generated-output folder or the existing `ximage/` poster
location intentionally; do not mix raw tweet caches with poster artifacts.

## What this produces

A full-page PNG screenshot of an HTML calendar that shows:
- Header with brand logo + big title ("Everything **OpenAI** shipped in 54 days")
- Team member avatars (2 rows, up to 10 people) with their X handles
- Monthly calendar grid — release days highlighted in brand color with release items
- Each release item has: publisher avatar (tiny circle) + emoji + short description
- Background: either a provided image or a generated gradient, with the calendar as a white rounded card on top

## Step 0: Interactive Setup Wizard

Run this wizard every time — do not skip steps.

### 0a. Check / install x-cli
```bash
which twitter 2>/dev/null || echo "NOT_FOUND"
```
If `NOT_FOUND`, tell the user:
> x-cli is not installed. Run: `npm install -g twitter-cli` (or `brew install twitter-cli` if available).
> Then re-run this skill.

Stop here if x-cli is not installed.

### 0b. Ask which browser the user is logged in to X with

x-cli supports: `chrome`, `firefox`, `safari`, `edge`, `brave`

Ask the user:
> Which browser are you logged in to X (Twitter) with?
> Options: chrome / firefox / safari / edge / brave

Store the answer as `$BROWSER`. Default to `chrome` if they don't say.

### 0c. Ask for the company / product to research

Ask the user:
> Which company or product do you want to make a release calendar for?
> You can give a name ("Vercel"), an X handle ("@vercel"), or a website URL ("vercel.com").

- If a URL is given (e.g. `vercel.com`), infer the company name and look up their X handle via search.
- If a name is given, look up known handles from the Brand Colors reference, or search X for `@<name>` to find the official account.

### 0d. Ask for background style

Ask the user:
> What background do you want for the calendar?
> 1. **Your own image** — drag a file into the folder and give me the path (e.g. `/path/to/bg.jpg`)
> 2. **AI-generated CSS background** — I'll design an HTML/CSS background that matches the brand (gradients, patterns, textures)

If the user provides a file path → use it as `url('file://[abs_path]')` on the `html` element.
If the user picks option 2 (or skips) → generate a CSS background that fits the brand:
- Amp: warm parchment gradient (`#CEC8B8` → `#B8B0A0`) — clean, editorial
- OpenAI: deep dark mesh (`#0a0a0f` → `#111827`)
- Anthropic: warm sunset gradient (`#2d1b0e` → `#1a0a0a`)
- Vercel: pure black
- Unknown: `linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%)`

⚠️ Always put background CSS on `html { }`, not `body { }` — prevents cut-off in full-page screenshots.

### 0e. Ask for date range

Ask the user:
> How far back should we look for releases?
> **30 days** (focused, recent sprint) / **60 days** (default, 2 months) / **90 days** (broader history)

Use their choice to set `$DAYS_BACK`. Default: 60 days.

- The calendar will show months from `(today - $DAYS_BACK)` through the month of the last release found.
- ⚠️ The headline "shipped in N days" is always calculated from **first release date → last release date**, not $DAYS_BACK.

### 0f. Verify x-cli auth with the chosen browser

```bash
TWITTER_BROWSER=$BROWSER twitter whoami 2>/dev/null | head -3
```
If `ok: false`:
> X login not found in $BROWSER. Please open $BROWSER, go to x.com, log in, then try again.

Stop here if auth fails.

### 1a. Confirm team handles to track

Based on the company identified in Step 0c:
- Check the **Brand Colors Reference** at the bottom of this skill first — many popular companies already have a confirmed handle list.
- If the company is in the reference, use those handles directly.
- If not in the reference:
  1. Use `twitter user <company_name> --yaml` to find the official account
  2. Search for founder/core team handles: `twitter search "(from:<handle>) OR (to:<handle>)" --yaml`
  3. Pick up to 10 unique handles: 1 official account + CEO/founder + up to 8 active product team members

Store the final list as `$HANDLES` (space-separated). You will use this in all subsequent steps.

### 1b. Pull posts — use --max 200, ALL handles in parallel

```bash
SINCE=$(date -v-${DAYS_BACK}d +%Y-%m-%d 2>/dev/null || date -d "-${DAYS_BACK} days" +%Y-%m-%d)
UNTIL=$(date +%Y-%m-%d)

# Run ALL handles in parallel, save to temp files
for handle in <handle1> <handle2> <handle3>; do
  TWITTER_BROWSER=$BROWSER twitter user-posts $handle --max 200 --yaml 2>/dev/null \
    | grep -E "^  (text|createdAtISO):" \
    | paste - - \
    | grep -E "$SINCE|$(echo $SINCE | cut -c1-7)" \
    > /tmp/rc_${handle}.txt &
done
wait
```

⚠️ **--max 50 is NOT enough** for a 54-day window. Active accounts post 5-10x/day including replies. Always use `--max 200`.

### 1c. Pull replies too — releases hide in reply threads

Founders often announce features *inside reply threads*, not as standalone posts. Pull replies separately:

```bash
for handle in <handle1> <handle2> <handle3>; do
  TWITTER_BROWSER=$BROWSER twitter search "(from:$handle) since:$SINCE until:$UNTIL" \
    -t Latest --max 100 --yaml 2>/dev/null \
    | grep -E "^  (text|createdAtISO):" \
    | paste - - \
    >> /tmp/rc_${handle}.txt &
done
wait
```

This catches posts that `user-posts` misses (replies, quote-tweets with announcements).

### 1d. Deduplicate and check coverage

```bash
# Count unique dates covered
for f in /tmp/rc_*.txt; do
  cat $f | awk -F'\t' '{print $2}' | cut -c19-28 | sort -u
done | sort -u | wc -l
```

**Self-check rule**: If unique dates < `$DAYS_BACK ÷ 7`, you have too little data. Run additional targeted searches:

```bash
# Targeted product-only search per handle
TWITTER_BROWSER=$BROWSER twitter search "(from:<handle>) (shipped OR launched OR new OR update OR release OR now) since:$SINCE until:$UNTIL" \
  -t Latest --max 100 --yaml 2>/dev/null \
  | grep -E "^  (text|createdAtISO):" | paste - -
```

### 1e. Filter to product releases only

From the raw tweet data, keep only posts that announce:
- Model launches / updates
- New features / products shipped
- Platform integrations (IDE, app, CLI)
- Milestone numbers (downloads, users)
- Acquisitions / key hires
- Beta / GA launches
- UX improvements explicitly mentioned as shipped

Discard: general opinions, engagement bait, podcast announcements without feature content, pure Q&A replies, travel/personal posts, retweets of others' work.

### 1f. Collect tweet URLs for click-through

For every release item you keep, extract the tweet ID so the calendar cells can link to the **exact original post**, not just the account.

```bash
# The yaml structure uses "- id:" (top-level list item), "  text:", "    screenName:", "  createdAtISO:"
# Use awk to group them correctly:
TWITTER_BROWSER=$BROWSER twitter user-posts <handle> --max 200 --yaml 2>/dev/null \
  | awk '
    /^- id:/ { id=substr($0, index($0,$2)) }
    /^  text:/ { text=substr($0, index($0,$2)) }
    /^  createdAtISO:/ { date=substr($0, index($0,$2)) }
    /^    screenName:/ { sn=substr($0, index($0,$2)); print id"\t"sn"\t"date"\t"text }
  ' \
  | grep "YYYY-MM"  # filter to date range
```

Tweet URL format: `https://x.com/<screenName>/status/<id>`

Store each release as: `{ date, text, tweetUrl, posterHandle }`

The HTML `onclick` on each `.day-cell.has-release` must open the **specific tweet URL**, not just `x.com/<handle>`:
```html
<div class="day-cell has-release" onclick="window.open('https://x.com/AmpCode/status/1234567890','_blank')">
```

If you can't recover the exact tweet ID for a release, fall back to `https://x.com/<handle>` with a comment in the HTML explaining why.

### 1g. Organize by date (YYYY-MM-DD)
Build a mental map: `{ "2026-03-05": [{ text: "🚀 GPT-5.4 launch", url: "https://x.com/AmpCode/status/...", poster: "AmpCode" }], ... }`

⚠️ **NO EMOJI rule (global, no exceptions)**: Release text labels must be plain text only — no emoji, no unicode symbols, no decorative characters of any kind. This applies to ALL companies regardless of brand style. The calendar aesthetic relies on clean typography; emoji break the visual rhythm and look unprofessional at small sizes. Write descriptive English words instead.

Keep each release text to **≤ 30 chars** so it fits in the cell.

⚠️ **ENGLISH ONLY rule**: All release text in the calendar cells must be in English. No Chinese, Japanese, Korean, or any other non-Latin script — even if the company or user is Chinese/Japanese/Korean. The calendar is a shareable artifact for international audiences. If a tweet was in another language, translate the release name to English before adding it.

## Step 1.5: Fetch Brand Logo

Use this priority order for the company's brand logo shown in the card header:

### Priority 1: @lobehub/icons (CDN, no install needed)

Check if the company has an icon in lobehub's collection:
```bash
# Try icon variants in order: color → mono → text
curl -s "https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-svg/icons/<id>-color.svg" | head -3
curl -s "https://raw.githubusercontent.com/lobehub/lobe-icons/refs/heads/master/packages/static-svg/icons/<id>.svg" | head -3
```

Where `<id>` is the lowercase company name (e.g. `amp`, `openai`, `anthropic`, `vercel`, `github`, `stripe`).

If the SVG returns valid content (starts with `<svg`), inline it directly in the HTML `<div class="brand-icon">`. Use width/height 28px.

Known lobehub IDs confirmed working:
| Company | id | Color hex |
|---------|-----|-----------|
| Amp | `amp` | `#F34E3F` |
| OpenAI | `openai` | `#000000` |
| Anthropic | `anthropic` | `#D97757` |
| Vercel | `vercel` | `#000000` |
| GitHub | `github` | `#181717` |
| Stripe | `stripe` | `#635BFF` |
| Linear | `linear` | `#5E6AD2` |
| Figma | `figma` | `#F24E1E` |
| Google | `google` | color variant |
| Gemini | `gemini` | color variant |
| DeepSeek | `deepseek` | color variant |

### Priority 2: Official website favicon / logo

If lobehub doesn't have the icon, fetch it from the company's website:
```bash
# Try common logo paths
curl -sI "https://<domain>/favicon.svg"
curl -sI "https://<domain>/logo.svg"
curl -sI "https://<domain>/images/logo.svg"
```

Or use agent-browser to screenshot the site and identify the logo visually, then embed it as an `<img>` tag.

### Priority 3: X profile image fallback

Use the official account's profile image URL from Step 2 as a last resort:
```html
<img src="[profileImageUrl]" width="28" height="28" style="border-radius:6px">
```

## Step 2: Fetch team member profile images

### 2a. Identify up to 10 key people — NO DUPLICATES
- Row 1 (5 people): official accounts + CEO/founder + head of product/devex
- Row 2 (5 people): core team members who actually posted release content

⚠️ **STRICT NO-DUPLICATE RULE**: Each person must appear at most ONCE in the team grid. If fewer than 10 unique people are identified, leave the remaining slots empty (render nothing) rather than repeating anyone. Never show the same avatar/handle twice even if you can't find 10 unique people.

⚠️ **CLICKABLE AVATARS RULE**: Every team member must be wrapped in an `<a href="https://x.com/<handle>" target="_blank">` tag — not a `<div>`. Clicking the avatar or name must open their X profile. This is non-negotiable. Use `a.team-member` CSS selector (not `.team-member`) to style them.

⚠️ **INTERNAL ONLY RULE**: The team avatar row must only include confirmed internal team members (founders, employees, PMs, engineers). Do NOT include external guests, users, partners, or community members in the avatar row — even if they posted content that appears on the calendar. External contributors (e.g. a guest on a livestream, a power user who demoed the product) may appear as the poster avatar inside calendar cells, but never in the team header row. When in doubt, omit rather than include.

```bash
TWITTER_BROWSER=$BROWSER twitter user <handle> --yaml 2>/dev/null \
  | grep -E "^  name:|^  screenName:|^  profileImageUrl:"
```

Run for all team members in parallel.

### 2b. Map handles to avatar URLs
Collect `{ handle: profileImageUrl }` for all team members.

For each release item, assign the avatar of whoever posted it:
- If `@OpenAIDevs` posted → use their avatar
- If `@OpenAI` (main account) posted → use their avatar
- If a specific team member posted → use their avatar
- Default fallback: use the primary official account avatar

## Step 3: Calculate title stats

From the filtered releases:
- **First release date** = date of the earliest release item you collected
- **Last release date** = date of the most recent release item you collected
- **Total days** = (last_release_date − first_release_date).days + 1
- **Total releases** count

⚠️ **Critical**: days span is from FIRST release to LAST release — NOT from first release to today's date. If first=Jan 9 and last=Mar 19, that is 70 days, not 77. Never use today's date as the end.

Title: `"Everything [Product/Brand] shipped in [N] days"`
Subtitle: `"[Start date] — [End date] · Product releases only"`

## Step 4: Generate the HTML

Create the file at `<output_dir>/release-calendar.html`.

### HTML structure

```
body (background image or gradient)
└── .card-wrap (white, border-radius: 24px, padding: 48px 44px)
    ├── .brand (OpenAI icon SVG + "OPENAI RELEASES")
    ├── .headline ("Everything OpenAI shipped in 54 days")
    ├── .subtitle (date range + "Product releases only")
    ├── .team-grid (flex-wrap row, each member is a clickable <a> tag)
    ├── .calendar-section (February)
    │   ├── .month-label
    │   ├── .day-headers (Mon–Sun)
    │   └── .calendar-grid (7 cols)
    │       ├── .day-cell.no-release (gray bg)
    │       ├── .day-cell.has-release (brand color bg)
    │       │   ├── .day-num
    │       │   └── .release-item × N
    │       │       ├── img.avatar (13px circle)
    │       │       └── span.release-text ("🚀 GPT-5.4 launch")
    │       └── .day-cell.empty-month (transparent, no number)
    ├── .calendar-section (March) [if spans 2 months]
    └── .footer (fixed attribution format — see below)
```

### Footer format (fixed — do not deviate)

The footer must always use this exact template, substituting the official account handle(s):

```html
<div class="footer">
  Attribution based on first X announcement by @[PrimaryHandle] / @[SecondaryHandle]. Corrections welcome.
</div>
```

- Use the primary official account as `@[PrimaryHandle]` (e.g. `@augmentcode`, `@OpenAI`, `@cursor_ai`)
- Use the main founder or dev-facing account as `@[SecondaryHandle]` (e.g. `@scott_dietzen`, `@OpenAIDevs`, `@amanrsanger`)
- If there is only one account, use: `Attribution based on first X announcement by @[Handle]. Corrections welcome.`
- Do not add dates, website URLs, or other text — keep it to this one sentence

### Key CSS values

```css
/* Layout */
body { padding: 50px; background: [image or gradient]; }
.card-wrap { background: #fff; border-radius: 24px; max-width: 1040px; padding: 48px 44px; }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; }
.day-cell { min-height: 88px; border-radius: 7px; padding: 7px 6px 6px; }

/* Colors */
.no-release { background: #f9f9f9; border: 1px solid #ebebeb; }
.has-release { background: [brand_color]; border: 1px solid [brand_color_dark]; }

/* Release items */
.avatar { width: 13px; height: 13px; border-radius: 50%; }
.release-text { font-size: 9.5px; color: rgba(255,255,255,0.93); line-height: 1.3; }
.day-num { font-size: 11px; color: var(--text-dim); }
.day-cell.has-release .day-num { color: rgba(255,255,255,0.6); }

/* Month headers */
.month-label { color: [brand_color]; font-size: 11px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; }

/* Team grid — clickable avatar row (Codex style) */
.team-grid { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 36px; padding-bottom: 28px; border-bottom: 1px solid #f0f0f0; }
a.team-member { display: flex; flex-direction: column; align-items: center; gap: 5px; padding: 6px 8px; border-radius: 10px; text-decoration: none; cursor: pointer; transition: background 0.15s; }
a.team-member:hover { background: #f4f4f4; }
a.team-member:hover img { border-color: [brand_color]; transform: scale(1.06); }
a.team-member img { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 2px solid #e8e8e8; transition: border-color 0.15s, transform 0.15s; }
.team-name { font-size: 10.5px; color: #333; font-weight: 500; text-align: center; line-height: 1.2; }
.team-handle { font-size: 9px; color: #aaa; text-align: center; }
```

### Calendar grid rules

February 2026 starts on **Sunday** → pad 6 empty cells before day 1 in a Mon-first grid.
March 2026 starts on **Sunday** → row starts Mon Mar 2.

General rule: for any month, calculate `(dayOfWeek(1st) - 1 + 7) % 7` empty leading cells (Mon=0 offset).

Trailing cells at end of calendar: add `empty-month` divs to complete the last row of 7.

### Background options

**If background image provided:**
```css
html { background-image: url('[path]'); background-size: cover; background-position: center; min-height: 100%; }
body { background: transparent; }
```
⚠️ Put background on `html`, not `body` — this ensures the gradient covers the full scrollable page, not just the viewport height. `body` with `background-attachment: fixed` cuts off at viewport in full-page screenshots.

**If no image (gradient fallback):**
```css
html { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); min-height: 100%; }
```

### Brand-matched card style

Instead of always using a white card, adapt the card background to the company's brand palette:

| Company | Card bg | Empty cell | Release cell | Month label color |
|---------|---------|------------|--------------|-------------------|
| Amp/Ampcode | `#F5F2EB` (warm parchment) | `#EDEAE2` | `#1C1B18` | `#6B6658` |
| OpenAI | `#ffffff` | `#f9fafb` | `#10A37F` | `#10A37F` |
| Anthropic | `#fff9f6` | `#fdf5f2` | `#D97757` | `#D97757` |
| Vercel | `#ffffff` | `#f5f5f5` | `#000000` | `#000000` |
| Default | `#ffffff` | `#f9fafb` | brand_color | brand_color |

**Amp-specific**: outer `html` background is `#CEC8B8` (warm tan, matches ampcode.com). Card is `#F5F2EB`. Release cells dark `#1C1B18`. Empty cells `#EDEAE2`. Month labels `#6B6658`. No colored accent — Amp uses pure dark-on-warm.

### Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600&display=swap" rel="stylesheet">
```
- Headline: `Instrument Serif` (the italic highlight for the product name)
- Body: `Geist` (closest free approximation to OpenAI's Söhne)

## Step 5: Screenshot

```bash
agent-browser --allow-file-access open "file://[absolute_path]/release-calendar.html"
agent-browser wait --load networkidle
agent-browser set viewport 1140 900 2
agent-browser wait 2000
agent-browser screenshot --full [output_dir]/release-calendar.png
agent-browser close
```

The `2` at the end of `set viewport` = 2× retina pixel density for a crisp high-res PNG.

Wait 2000ms after load to allow Google Fonts to render.

## Step 6: Deliver

Tell the user:
- HTML saved to: `[path]/release-calendar.html`
- Screenshot saved to: `[path]/release-calendar.png`
- Open the HTML in browser for live version: `open [path]/release-calendar.html`

If there are obvious issues visible in the screenshot (clipped content, missing fonts, broken background), diagnose and fix before declaring done.

---

## Brand Colors Reference

| Company | Brand Color | Accounts |
|---------|-------------|----------|
| OpenAI | `#10A37F` | @OpenAI, @OpenAIDevs, @sama |
| Anthropic | `#D97757` | @AnthropicAI, @ClaudeAI |
| Augment Code | `#1A9E5C` green (see below) | @augmentcode, @scott_dietzen, @VinayPerneti, @sambreed |
| Amp/Ampcode | warm parchment (see below) | @AmpCode, @sqs, @beyang, @thorstenball |
| Google Gemini | `#1a73e8` Google blue (see below) | @GoogleDeepMind, @OfficialLoganK, @demishassabis, @GoogleAIStudio, @nainar92, @stitchbygoogle, @rustinb, @GeminiApp |
| Cursor | `#c8ff00` neon green on black (see below) | @cursor_ai, @mntruell, @amanrsanger, @ryolu_, @vincentzhuu |
| Vercel | `#000000` | @vercel, @leeerob |
| GitHub | `#238636` | @github, @GitHubEng |
| Stripe | `#635BFF` | @stripe, @StripeDev |
| Linear | `#5E6AD2` | @linear |
| Figma | `#F24E1E` | @figma |

For unknown companies: default to `#6366f1` (indigo) — works well on both light and dark backgrounds.

**Google Gemini palette** (based on Google brand — clean white card on deep blue background):
```css
html { background: linear-gradient(145deg, #0d1b3e 0%, #1a237e 45%, #0d2137 100%); }
.card-wrap { background: #ffffff; }
.day-cell.no-release { background: #f8f9fa; border: 1px solid #f1f3f4; }
.day-cell.has-release { background: #1a73e8; border: 1px solid #1557b0; }
.month-label { color: #1a73e8; }
.headline em { color: #1a73e8; }
/* lobehub id: "gemini" — multicolor gradient star SVG */
```

Key Gemini team accounts and their roles:
- @GoogleDeepMind — model research & launches (primary)
- @OfficialLoganK (Logan Kilpatrick) — AI Studio + Gemini API PM, MTS; most active developer-facing voice
- @demishassabis (Demis Hassabis) — DeepMind CEO; personally announces major launches
- @GoogleAIStudio — developer platform, vibe coding, spend caps, Stitch integration
- @nainar92 (Naina Raisinghani) — Nano Banana PM; avatar: https://pbs.twimg.com/profile_images/2022216331647758338/G6oSvlYC_normal.jpg
- @stitchbygoogle — AI design DNA & UI generation tool; avatar: https://pbs.twimg.com/profile_images/1924895422327463936/V991NnhE_normal.jpg
- @rustinb (Rustin Banks) — Stitch PM; avatar: https://pbs.twimg.com/profile_images/1908246167013793792/SPez5OwV_normal.jpg
- @GeminiApp — consumer app (Lyria, Personal Intelligence, Veo)
- No emoji in release-text labels — text only

**Cursor palette** (dark hacker aesthetic — black card, neon green accent):
```css
html { background: #0a0a0a; }
.card-wrap { background: #111111; box-shadow: 0 0 0 1px #222, 0 32px 80px rgba(0,0,0,0.6); }
.day-cell.no-release { background: #161616; border: 1px solid #1e1e1e; }
.day-cell.has-release { background: #1a1f0a; border: 1px solid #2d3a0a; }
.day-cell.has-release:hover { background: #222d0d; border-color: #c8ff00; }
.month-label { color: #c8ff00; }
.headline em { color: #c8ff00; }
.release-text { color: #aac830; }
.day-cell.has-release .day-num { color: #8aaa20; }
```

Key Cursor team accounts and their roles:
- @cursor_ai — official account, primary release announcements (every major feature)
- @mntruell (Michael Truell) — CEO & co-founder; vision/strategy essays, product direction, growth data; writes deeply thoughtful long-form posts worth reading in full
- @amanrsanger (Aman Sanger) — co-founder; most technically active, posts Composer training reports, model integration details, hard engineering threads
- @ryolu_ (Ryo Lu) — Design lead; UI/UX and vibe coding updates; Chinese team member
- @vincentzhuu (Vincent Zhu) — Growth; user data and marketing-adjacent content

Avatar URLs (verified):
- @cursor_ai: https://pbs.twimg.com/profile_images/1970182748146180096/dhZeXi_X_normal.jpg
- @mntruell: https://pbs.twimg.com/profile_images/1887065642261737472/QdLiAFfD_normal.jpg
- @amanrsanger: https://pbs.twimg.com/profile_images/1407704462265704456/OiDRC7b-_normal.jpg
- @ryolu_: https://pbs.twimg.com/profile_images/1915014653295697921/KmMbglaO_normal.jpg
- @vincentzhuu: https://pbs.twimg.com/profile_images/1990721764654276608/0kyY5WC__normal.jpg

No emoji in release-text labels — text only.

**Cursor X post copy notes** (user preferences for promo tweets):
- Mention Tab key redefinition as a key hook
- Highlight Multi-Agent planning: users focus on outcomes, not code
- Mention Agent Harness + Remote Control as recent infrastructure bets
- @mntruell writes deeply — worth calling out his essays specifically
- Recommend Cursor to non-technical teammates as first choice
- @ryolu_ is the Chinese team member (design lead) — can mention warmly
- After generating the calendar, ALWAYS ask: "要不要我帮你写这次的 X 宣传文案？你可以补充一些内容，我来整合进去。"

**Augment Code palette** (clean white card, green accent on dark background):
```css
html { background: linear-gradient(145deg, #0a0f1e 0%, #0d1a3a 40%, #0a1628 70%, #061020 100%); min-height: 100%; }
.card-wrap { background: #ffffff; }
.day-cell.no-release { background: #f9f9f9; border: 1px solid #ebebeb; }
.day-cell.has-release { background: #1A9E5C; border: 1px solid #158a4e; }
.month-label { color: #1A9E5C; }
.headline em { color: #1A9E5C; }
.brand-label { color: #1A9E5C; }
/* No lobehub icon — use profile image from @augmentcode as brand icon */
```

Key Augment team accounts:
- @augmentcode — official, primary release announcements
- @scott_dietzen — CEO, strategy/productivity posts; mostly retweets official content
- @VinayPerneti — VP Engineering, engineering execution
- @sambreed — Staff Engineer, Intent internals
- No emoji in release-text labels — text only

**Amp brand palette** (based on ampcode.com — warm parchment editorial style):
```css
html { background: #CEC8B8; }           /* outer warm tan */
.card-wrap { background: #F5F2EB; }     /* warm parchment card */
.day-cell.no-release { background: #EDEAE2; border: 1px solid #E4E0D8; }
.day-cell.has-release { background: #1C1B18; border: 1px solid #111; }
.month-label { color: #6B6658; }
.brand-label, .subtitle { color: #9E9888; }
/* No colored accent — Amp uses pure dark-on-warm */
```

---

## Common Issues

**Background cuts off at bottom of screenshot:**
→ Background must be on `html`, not `body`. See Step 4 background CSS.

**Fonts render as fallback sans-serif:**
→ Wait 2000ms after `networkidle` before screenshotting (Step 5). Google Fonts need time.

**Calendar grid misaligned:**
→ Recount leading empty cells. Off-by-one in day-of-week calculation is the usual culprit.

**Release text overflows cell:**
→ Trim text to ≤ 30 chars. Remove subtitles and keep only the main announcement.

**x-cli returns no results:**
→ Try the `user-posts` command instead of `search` for official accounts — it's more reliable for recent posts.
