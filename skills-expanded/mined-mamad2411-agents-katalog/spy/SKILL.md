---
name: spy
description: "Instant competitive hook intelligence — scrape any Instagram accounts, find their viral outliers, transcribe the hooks, and get proven templates you can steal."
---

# /spy

Instant competitive hook intelligence. Give it Instagram handles — it scrapes their content, finds viral outliers, transcribes the hooks, templatizes them, and shows you exactly what's working in any niche. Zero setup, no database required.

## Usage
`/spy @handle1 @handle2 @handle3`
`/spy https://www.instagram.com/handle1/ https://www.instagram.com/handle2/`

Examples:
- `/spy @hormozi @garyvee @danmartell`
- `/spy @levelsio @marc_louvion @yaboroda_`

Minimum 2 handles, maximum 10.

## Step 0 — First-Time Setup

Check if config exists at `~/.claude/skills/spy/config.json`.

**If config exists:** Load tool paths from it. Skip to Step 1.

**If config does NOT exist:**

```
Welcome to /spy! Let me check your tools real quick. This only happens once.
```

### Check Apify MCP
Try calling `mcp__apify__search-actors` with query "instagram". 
- If it works: "Apify connected."
- If it fails:
  ```
  Apify is not connected. To set it up:
  1. Create a free account at https://apify.com
  2. Go to Settings → Integrations and copy your API token
  3. Exit Claude Code (type /exit)
  4. Run: claude mcp add apify -- npx -y @anthropic-ai/apify-mcp-server
  5. When prompted, paste your API token
  6. Reopen Claude Code and run /spy again
  ```
  Stop here until Apify is connected.

### Check CLI Tools

```bash
YT_DLP=$(which yt-dlp 2>/dev/null)
WHISPER=$(which whisper 2>/dev/null)
FFMPEG=$(which ffmpeg 2>/dev/null)
```

For each missing tool:
- `yt-dlp`: "Run: `pip3 install yt-dlp`"
- `whisper`: "Run: `pip3 install openai-whisper`"
- `ffmpeg`: "Run: `brew install ffmpeg` (Mac) or `sudo apt install ffmpeg` (Linux)"

Stop here until all tools are installed.

### Save Config

```json
{
  "toolPaths": {
    "ytDlp": "/path/from/which",
    "whisper": "/path/from/which",
    "ffmpeg": "/path/from/which"
  },
  "setupComplete": true,
  "setupDate": "YYYY-MM-DD"
}
```

Then proceed.

---

## Step 1 — Parse Handles

Extract Instagram handles from the input. Accept formats:
- `@handle`
- `handle`
- `https://www.instagram.com/handle/`
- `https://www.instagram.com/handle/reels/`

Strip everything down to just the handle (no @, no URL).

## Step 2 — Scrape via Apify

Use `apify/instagram-scraper` to scrape each handle:
- `resultsType: "posts"`
- `resultsLimit: 50`
- Batch handles in groups of 5-6

For each post, extract: `ownerUsername`, `url`, `videoViewCount`, `likesCount`, `commentsCount`, `timestamp`, `caption`, `type`

Filter to VIDEO posts only (reels). Ignore carousels and images for this analysis.

## Step 3 — Calculate Outliers

For each handle:
1. Calculate **median views** from all posts returned (up to 50)
2. Find posts with **5x+ median views** — these are the outliers
3. Also note the **top 3 posts by views** even if they're not technically 5x (in case the account is consistently high)

Filter to **last 30 days only** for outlier candidates.

Print a quick summary:
```
Scraping complete:
  @handle1: 42 posts, median 12K, found 3 outliers (5x+)
  @handle2: 38 posts, median 8K, found 5 outliers (5x+)
  @handle3: 29 posts, median 3K, found 7 outliers (5x+)

Total outliers to process: 15
```

## Step 4 — Process Each Outlier

For each outlier, in order of views (highest first). Max 20 outliers.

### 4a. Download
```bash
$YT_DLP "[url]" -o /tmp/spy_reel.mp4 --merge-output-format mp4 -q
```
Use the yt-dlp path from config.json.

### 4b. Transcribe (spoken hook)
```bash
$WHISPER /tmp/spy_reel.mp4 --model base --output_format txt --output_dir /tmp/ --fp16 False
```
Extract the first 1-3 sentences as the **spoken hook**.

### 4c. Screenshot (on-screen text hook)
```bash
$FFMPEG -i /tmp/spy_reel.mp4 -vframes 1 -ss 00:00:01 /tmp/spy_thumb.png -y
```
Read the screenshot with vision to extract the **on-screen text hook**.

### 4d. Caption hook
Extract the first 1-2 sentences of the post caption as the **caption hook**.

### 4e. Analyze & Templatize
For each outlier, generate:
- **Spoken hook template** — abstract the spoken hook into `[BRACKET]` framework
- **On-screen text template** — abstract the on-screen text into `[BRACKET]` framework
- **Caption template** — abstract the caption hook into `[BRACKET]` framework
- **Hook type** — classify: Tool Discovery, Replace + Kill Claim, Viewer Callout, Speed Tutorial, Framework, Contrarian, Comparison, Fear/Warning, Controversy/News, Listicle, POV/Meme, Raw Energy, Absurd Escalation, etc.
- **Why it works** — 1-2 sentence psychological analysis

### 4f. Clean up
```bash
rm -f /tmp/spy_reel.mp4 /tmp/spy_reel.txt /tmp/spy_thumb.png
```

## Step 5 — Display Results

### Summary Stats
```
╔══════════════════════════════════════════╗
║  SPY REPORT — [N] outliers from [N]     ║
║  accounts in the [NICHE] niche          ║
╚══════════════════════════════════════════╝

Accounts analyzed: [N]
Total posts scanned: [N]
Outliers found (5x+): [N]
Top hook type: [TYPE] ([N] occurrences)
```

### For each outlier, show a card:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#1 — @handle (1.2M views, 70.7x outlier)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎙️ SPOKEN HOOK:
"Here are five secret codes for Claude."

📱 ON-SCREEN TEXT:
"Secret Codes for Claude 😳"

📝 CAPTION:
"Comment 'Codes' and I'll send you 100 more 👇"

🧩 TEMPLATES:
  Spoken:    Here are [NUMBER] secret codes for [TOOL]
  On-screen: Secret Codes for [TOOL] [EMOJI]
  Caption:   Comment '[KEYWORD]' and I'll send you [NUMBER] more

🏷️ Type: Listicle / Secret Codes
💡 Why: "Secret codes" implies hidden insider knowledge.
        Numbered list promises quick scannable value.

🔗 https://www.instagram.com/p/xxxxx/
```

### After all outliers, show the Template Leaderboard:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOP TEMPLATES (ranked by total views)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [TOOL] just killed [PROFESSION]
   Used by: @creator1, @creator2, @creator3
   Combined: 1.2M views across 4 posts
   Works for: Reels ✓  Carousels ✓

2. Here are [NUMBER] secret codes for [TOOL]
   Used by: @creator1
   Combined: 1.4M views across 2 posts
   Works for: Reels ✓  Carousels ✓
```

Mark each template as carousel-friendly or not:
- ✓ Carousel: Replace + Kill Claim, Listicle, Framework, Tool Discovery, Viewer Callout, Comparison, Don't Say / Instead Say
- ✗ Carousel: POV/Meme, Comment Reply, Speed Tutorial Rapid Steps, Contrarian rants, Celebrity/News, Raw Energy

## Step 6 — Offer Next Steps

After showing results, ask:

> "Want me to:
> 1. **Save these to a file** — markdown report you can reference later
> 2. **Set up full tracking** — install `/hook-intel` for weekly auto-refresh + database
> 3. **Generate scripts** — pick a template and I'll write a script using it in your voice"

## Important Rules

- **This skill is READ-ONLY** — it never saves to any database. Output only.
- **Process max 20 outliers** — if there are more, take the top 20 by views
- **Always show all three hook versions** — spoken, on-screen, caption. The spoken hook is the most important, on-screen text is second, caption is last.
- **Don't skip meme/POV posts** — include them but note they're "high views, low follow conversion"
- **Detect the niche automatically** — look at the content angles across all outliers and identify the common thread

---

Built by [@tenfoldmarc](https://instagram.com/tenfoldmarc). Follow for daily AI automation builds — real systems, not theory.
