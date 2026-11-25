---
name: content-pattern-intelligence
description: >
  Analyze top-performing posts across three performance lenses — engagement, impressions,
  and engagement rate — to identify content patterns and give the user specific hypotheses
  to test in their next posts. Use this skill whenever the user asks things like "what's
  working in my content", "what should I post more of", "why are some posts doing better",
  "what patterns do you see", "give me content ideas based on my best posts", "what content
  works best for [client]", "analyze my top posts", or "what should I try next month".
  Also activate when the user wants to understand performance beyond just numbers — when
  they're asking for creative direction, not just a report. Always use this skill instead
  of a generic performance summary when the user's goal is to improve future content.
---

# Content pattern intelligence

Look at what's actually working — then tell the user why, and what to try next.

This skill analyzes top posts across three performance lenses, finds patterns in the content itself (format, hook, topic, tone, structure), and translates them into specific, testable hypotheses for future posts.

**This is not a performance report.** It's a content brief grounded in data.

---

## Step 0: Detect input mode

**Mode A — Planable connector**
User has Planable connected and wants to pull live post data.

**Mode B — CSV upload**
User has uploaded a CSV export with post-level data (text, date, platform, metrics).

**How to detect:**
- File uploaded → Mode B
- Mentions "CSV", "export", "file", "spreadsheet" → Mode B
- Mentions workspace name, client, or Planable → Mode A
- Unclear → ask: "Do you have a CSV with your post data, or should I pull it from Planable?"

---

## Mode A: Planable connector

### Step 1: Gather inputs

- **Workspace / client** — which workspace to analyze
- **Platform(s)** — default to all; narrow if requested
- **Date range** — default to last 60–90 days (needs enough posts to find patterns; warn if fewer than 15 posts available)

### Step 2: Fetch data — with Instagram-safe refresh logic

Instagram metrics sync is async and slow. Always follow this sequence to avoid timeouts.

**Always call `get_post_metrics` with exactly one `pageId` per request. Multi-page calls compound timeouts — never bundle multiple pages into a single call.**

#### Step 2a: Read first, check freshness

```
list_workspaces → find workspaceId
list_pages(workspaceId) → get pageIds
get_page_metrics(workspaceId, pageIds, startDate, endDate)
```

For each page in the response, check `lastMetricAt` (the timestamp of the last successful metrics fetch).

- If `lastMetricAt` is **within the last 3 hours** — data is fresh. Skip the refresh entirely. Proceed to Step 2c.
- If `lastMetricAt` is **older than 3 hours** or missing — data is stale. Proceed to Step 2b.

The `posts` field in the `get_page_metrics` response tells you the post count per page for the window. Record it now — use it to plan chunk size in Step 2c so you're not choosing a strategy inside the fetch loop.

#### Step 2b: Refresh stale data — with platform-aware patience

Call `refresh_page_metrics` for the stale pages.

For **Instagram pages specifically**, tell the user before refreshing:
> "Instagram metrics are syncing — this can take 1-2 minutes. I'll check back once the data is ready."

Then wait before re-reading:
- **Instagram:** wait 60 seconds before calling `get_page_metrics` again
- **All other platforms:** wait 15-20 seconds

After waiting, call `get_page_metrics` again and re-check `lastMetricAt`:
- If `lastMetricAt` is now more recent than the refresh call — sync completed. Proceed to Step 2c.
- If `lastMetricAt` is still older — sync is still in progress. Wait another 30 seconds and retry once more.
- After 2 retries with no update — tell the user: "Instagram data is still syncing. You can try again in a few minutes, or I can run the analysis now using the most recent available data." Let the user decide.

#### Step 2c: Fetch post-level metrics (volume-aware)

Process each page individually — never bundle multiple pages in one call.

For each page, follow this sequence:

**1. Check post volume**
Use the `posts` field already captured in Step 2a for this page. If it wasn't available there, call:
```
get_post_metrics_summary(workspaceId, [pageId], startDate, endDate)
```
→ read `totalPosts` for the window.

**2. Choose chunk size based on `totalPosts`**

| Posts in window | Strategy |
|---|---|
| ≤ 20 | Fetch full window in one call |
| 21–40 | Two 45-day chunks |
| 41–80 | ~6 chunks of 2 weeks each |
| 80+ | 1-week chunks |

**3. Run all chunks for that page in parallel.**

**4. On timeout for any chunk — bisect:**
- Halve the failing window and retry both halves.
- If a window shrinks below 48 hours and still times out, **stop bisecting**.
  - Skip that range entirely.
  - Record it in Data notes: e.g. "1 IG post in May 12–14 likely missing — endpoint timed out at < 48h window."
  - Do not retry further — the rest of the dataset is still usable.

Repeat for each page before moving on to Step 3.

### Step 3: Sort into three ranked lists -> go to [Analysis](#analysis)

---

## Mode B: CSV upload

### Step 1: Accept the file

If no file uploaded yet: "Please upload a CSV with your post data — it should include post text, platform, and at least one of: likes, comments, shares, impressions, or engagement rate."

Supported sources: Planable Analytics export, Meta Business Suite, LinkedIn Analytics, Hootsuite, Sprout Social, or any post-level CSV.

### Step 2: Parse the CSV

Identify:
- **Post text column** — `text`, `caption`, `message`, `content`, or similar
- **Platform column** — `platform`, `channel`, `network`, `page`
- **Engagement columns** — likes, comments, shares, reactions, saves, clicks → sum into total engagement if not pre-summed
- **Impressions column** — `impressions`, `reach`, `views`
- **Engagement rate column** — `engagement_rate`, `eng_rate`, or calculate as `total_engagement / impressions`
- **Date column** — for context; not required for pattern analysis

If post text is missing or too short to analyze (under 10 chars average), tell the user — pattern analysis won't be meaningful without the actual content.

### Step 3: Sort into three ranked lists → go to [Analysis](#analysis)

---

## Analysis

### Step 1: Build three ranked lists

Take all posts with available data and produce:

1. **Top 10 by total engagement** (likes + comments + shares + saves)
2. **Top 10 by impressions** (or reach)
3. **Top 10 by engagement rate** (engagement / impressions — best signal for content quality independent of distribution)

If fewer than 10 posts exist for a lens, use all available. Minimum 5 posts per lens to draw patterns. Fewer than 5 → note the limitation but still try.

---

### Step 2: Analyze each list for content patterns

For each ranked list, read the actual post text and look for recurring patterns across the top performers. Analyze along these dimensions:

**Format signals**
- Does the post open with a question?
- Does it use a numbered list or bullet structure?
- Is it short (1–3 lines) or long-form?
- Does it start with a bold statement, statistic, or provocative claim?
- Does it use line breaks for rhythm (one sentence per line)?
- Does it include a call to action or question at the end?
- Does it use emojis? How many and where?

**Hook patterns**
- What's the first line structure? (Question / Statement / Number / "If you..." / "Most [X]..." / Story opener)
- Is the hook about the audience, the brand, or a problem?

**Topic/theme signals**
- What subject matter appears repeatedly? (behind the scenes, tips, opinions, product, social proof, storytelling, data/stats, trends)
- Is it educational, entertaining, promotional, or conversational?

**Tone signals**
- Personal/informal vs. professional/polished?
- Opinionated vs. neutral?
- Short and punchy vs. detailed?

**Timing / context signals** (if date data is available)
- Do top posts cluster around certain days or times?
- Do they align with a campaign, trend, or event?

---

### Step 3: Find the delta

Compare the top-performing posts against the bottom performers (or average performers) in the dataset. What do the worst posts have that the best ones don't? What's missing?

This is the most valuable part — patterns only matter if they're actually differentiating.

---

### Step 4: Write the output

Produce the analysis in this format:

---

## 🔍 Content patterns for [Client / Workspace] — [Platform(s)] — [Date range]

*Based on [X] posts analyzed across [date range]*

---

### ⚡ TL;DR

Open with this section every time, before any pattern detail. It should be readable in 20 seconds.

**What's working:**
- [One-line summary of the single strongest pattern across all lenses]
- [Second most consistent finding]
- [Third if clearly supported by data — skip if not]

**Try these next:**
1. [Most actionable hypothesis — one sentence, specific]
2. [Second hypothesis]
3. [Third hypothesis]

**Skip more of:**
- [One-line on the clearest underperforming pattern]

Keep the TL;DR to 8–10 lines max. No examples, no explanations — just the signal. The detail sections below support every point made here.

---

### 📣 What drives engagement

*Top posts by total likes, comments, shares, and saves*

Assign each pattern a descriptive emoji that reflects its nature. Pick the emoji based on what the pattern actually is — don't default to generic ones. Examples: 🙋 for question-openers, 📋 for list formats, 💬 for conversational tone, 📊 for data/stats posts, 🎭 for storytelling, 🔥 for opinionated takes, 🪞 for audience-mirror posts (about the reader, not the brand), 🧵 for thread-style structure, 🎯 for direct CTAs. Choose what fits — these are examples, not a fixed list.

**[emoji] Pattern [#]: [Short name for the pattern]**
What it is: [One sentence describing the pattern]
Example: "[First 80 chars of a top post that shows this]..."
Why it likely works: [One sentence of honest reasoning — don't overclaim]
➡️ Try this: [Specific, actionable thing to test in the next post or batch]

*(Repeat for each distinct pattern found — aim for 2–4 patterns per lens, not more)*

---

### 👀 What drives impressions

*Top posts by reach and views*

Same emoji logic as above — pick one per pattern that reflects what that pattern actually is.

**[emoji] Pattern [#]: [Short name]**
What it is: [One sentence]
Example: "[Post preview]..."
Why it likely works: [One sentence]
➡️ Try this: [Specific test]

*(2–4 patterns)*

---

### 💡 What drives engagement rate

*Top posts by engagement relative to reach — the best signal for content that genuinely resonates*

Same emoji logic — one per pattern, chosen to reflect the pattern's nature.

**[emoji] Pattern [#]: [Short name]**
What it is: [One sentence]
Example: "[Post preview]..."
Why it likely works: [One sentence]
➡️ Try this: [Specific test]

*(2–4 patterns)*

---

### ⚠️ What's not working

1–2 observations from the lower performers. Keep it honest and specific.

---

### 📝 Data notes

Always include all of the following in this section:

- **(a) Posts attempted vs. fetched** — e.g. "47 posts attempted, 44 fetched (3 in skipped ranges)"
- **(b) Skipped date ranges** — list any range that was skipped due to timeout, with the reason and an estimate of how many posts may be missing
- **(c) Fetch strategy per page** — note which pages used a single call vs. chunked fetching

Plus flag anything else that affects confidence: small sample size, one platform only, missing post text, etc.

---

**Emoji usage rule:** Emojis appear in two places only — (1) once per pattern label, chosen to reflect the pattern's content, and (2) in section headers. Never inline within sentences or used decoratively. The TL;DR has no emojis except the ⚡ header.

---

### HTML visual report

After delivering the in-chat text analysis, generate a self-contained HTML file saved to `/mnt/user-data/outputs/[client]-content-patterns-[month].html` and present it with `present_files`.

The HTML report is the visual companion to the text output — same structure, same data, but charts replace walls of text. Design it to be shareable with a client or team lead.

**Aesthetic:** Clean, modern, data-forward. Use Planable green `#3BBA7B` as the primary accent. Card layout. Clear hierarchy. Feels like a real agency deliverable, not a generated doc.

**Font:** Load `Plus Jakarta Sans` from Google Fonts for body; `Bricolage Grotesque` for headings.

**Color palette:**
```css
:root {
  --green: #3BBA7B;
  --green-light: #EAF7F0;
  --green-mid: #2a9d63;
  --amber: #F59E0B;
  --amber-light: #FEF3C7;
  --red: #EF4444;
  --red-light: #FEE2E2;
  --blue: #3B82F6;
  --blue-light: #EFF6FF;
  --purple: #8B5CF6;
  --purple-light: #F5F3FF;
  --text: #1A1A2E;
  --text-muted: #6B7280;
  --bg: #F8FAFC;
  --card: #FFFFFF;
  --border: #E5E7EB;
}
```

---

#### Required sections and charts

**1. Header**
- Client name, date range, "Content Pattern Analysis"
- Stat strip: total posts analyzed, platforms covered, date range

**2. ⚡ TL;DR card**
Render the TL;DR as a highlighted card — green left border, slightly tinted background. Three columns: "What's working" / "Try next" / "Skip more of." This is the first thing a client sees.

**3. 📣 Engagement patterns — bar chart**

Horizontal bar chart comparing average engagement per post for each pattern identified.

- X axis: average engagement (likes + comments + shares)
- Y axis: pattern names (e.g. "Question opener", "List format", "Storytelling")
- Each bar labeled with its value
- Color: green bars for patterns in top half, muted gray for lower performers
- Below the chart: one card per pattern with the example post preview and "Try this" action

Data to use: calculate average engagement for posts that match each pattern vs. posts that don't. If exact pattern-level data isn't available, use the top-10 vs. bottom-10 split as a proxy and label it clearly.

**4. 👀 Impressions patterns — bar chart**

Same structure as above but for impressions data.

- X axis: average impressions per post
- Color: blue (`--blue`) for top patterns, muted for lower
- Pattern cards below with examples

**5. 💡 Engagement rate patterns — horizontal comparison bars**

For engagement rate, use a visual that shows relative performance — e.g. grouped bars or a dot/lollipop chart showing engagement rate % per pattern.

- Color: purple (`--purple`) for this lens
- Show the platform average as a reference line or marker so patterns can be compared against baseline
- Pattern cards below with examples

**6. 🏆 Triple performers (if any)**

If any posts appear in all three top-10 lists, give them a dedicated card with a gold/amber treatment. Show the post text, and its scores across all three metrics. Label clearly: "This post did everything right."

**7. ⚠️ What's not working**

Two-column layout: left side shows the underperforming pattern with its average metric; right side shows the contrast against the top pattern in the same lens. Makes the gap visible.

**8. 🧪 What to test next**

Three action cards in a row. Each card:
- Hypothesis number + emoji
- Bold hypothesis name
- One-sentence description
- "Test in your next batch →" as a subtle footer label

**9. Footer**
"Generated with Planable + Claude · [date]"

---

#### Chart implementation

Build all charts in pure HTML/CSS — no external JS chart libraries. Use CSS-only techniques:

**Bar charts:** `div` elements with `width` set as a percentage of the max value, using CSS variables. Animate bars on load with a `width` transition from 0 to final value (`animation: grow 0.8s ease-out forwards` with `animation-delay` staggered per bar).

```css
@keyframes grow {
  from { width: 0; }
  to { width: var(--bar-width); }
}
```

Set `--bar-width` as an inline style per bar based on the actual data values.

**Lollipop / dot chart for engagement rate:** horizontal line (`border-top: 2px dashed`) with a dot at the end (`border-radius: 50%`), same CSS animation approach.

**Reference line:** a vertical `div` with `position: absolute` and `border-left: 2px dashed var(--text-muted)` to mark the platform average.

**Labels:** always show the actual number on or beside each bar. Don't make users guess from axis position alone.

**Responsive:** bars scale correctly at 600px–1200px. Cards wrap to single column below 700px.

---

#### HTML technical requirements

- Single self-contained `.html` file — no external dependencies except Google Fonts
- All chart data hardcoded from the actual analysis — no JS data fetching
- `@media print` block: hides nothing, keeps colors (use `-webkit-print-color-adjust: exact`)
- No JavaScript required — pure HTML/CSS
- Accessible: `aria-label` on chart containers, sufficient color contrast

**Be specific.** "Posts that start with a question get more comments" beats "engaging content performs well." If you can't be specific, you don't have enough data — say so.

**Show the evidence.** Every pattern must reference actual posts from the data. Don't name a pattern you can't point to.

**Honest about uncertainty.** These are hypotheses, not conclusions. Use "likely", "seems to", "worth testing" — not "definitely" or "proven."

**One actionable test per pattern.** The `➡️ Try this` line must be something the user could actually put in a brief tomorrow. Not "post more questions" — but "open your next LinkedIn post with a direct question to your audience, and end with a second question in the last line."

**Don't invent patterns.** If the top posts have nothing in common, say so. Sometimes the data is noisy.

**Length:** As long as the data warrants. 3 lenses × 2–4 patterns each = typically 600–1,000 words of output. Don't pad; don't compress if the patterns are real.

---

## Edge cases

- **Fewer than 15 posts total**: Run the analysis but caveat heavily — patterns from small samples are directional at best.
- **All posts are similar format**: Note this — it means you can't identify differentiating patterns from format alone. Look harder at topic and tone.
- **No post text available**: Can't do pattern analysis. Tell the user clearly and suggest re-exporting with post text included.
- **Single platform only**: Fine — just note that patterns are platform-specific and may not transfer.
- **Overlapping top posts** (same post appears in all three lists): Highlight this as a "triple performer" — a post that does everything right — and analyze it separately as the strongest signal in the dataset.
- **Boosted / paid posts in data**: If detectable, flag them separately — paid distribution skews impressions and may inflate engagement; organic patterns are more useful for content strategy.
