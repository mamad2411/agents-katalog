---
name: facebook-research-grow
version: 1.0.0
description: |
  Follower growth engine ("page audience stealer"). Grows a Facebook page's
  follower count by deep-researching the audience of target pages in the same
  niche, then engaging that audience with comments/replies on competitor posts
  so they discover and follow our page. Runs as a goal-driven campaign (e.g.
  "+200 followers in 24h") with progress snapshots, adaptive plan pivots, and
  checkpoint/resume cycles every 2-3 hours. Built for the Mexican/Hispanic
  football community in the USA. Prioritizes volume of human-like engagement
  while strictly avoiding Facebook bans/flags.

allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - ChromeDevTools
  - WebSearch
  - Question
  - Task
---

# Facebook Research — Grow State (v1.0.0)

## What This Skill Does

**Grow our page's followers by stealing the audience of other pages.**

The core loop:

1. **Campaign setup** — define the growth goal (default: **+200 followers in 24h**) and the target audience (default: **Mexican/Hispanic football community in the USA**).
2. **Own-page audit** — deep research of OUR page: current followers, what content pulls the most followers, our brand voice, our conversion hooks.
3. **Audience reconnaissance** — for each target page, learn everything about its followers: who they are, what they argue about, what slang they use, which posts get the most comments.
4. **Engagement execution** — comment/reply on competitor posts AS our page, matching the audience's voice so people click through and follow us. Volume-first, but human-like and ban-safe.
5. **Progress tracking** — snapshot follower count each checkpoint; compare against goal.
6. **Checkpoint & pivot** — report to the user every 2-3 hours and ask them to resume. If growth is off-track, change the plan (new target pages, new comment style, different timing) and re-run.

**You are the brain.** Decide what to comment, where, when, and whether to shift strategy — don't ask the user to make micro-decisions. Only surface big pivots at checkpoints.

## Preconditions

- Chrome DevTools is logged into Facebook as the page profile (or profile with page access).
- Project config exists: `.fb-research/projects/<page-name>/config.json`
- Engagement subskill (facebook-research-engage) may have already created `engagement-opportunities.json` — reuse it if present.

## Project Structure (Growth Data)

```
.fb-research/projects/<page-name>/
├── config.json                     # Page config (niche, keywords, language)
├── growth-campaign.json            # Active campaign: goal, deadline, status
├── growth-targets.json             # Pages/posts/accounts identified as follower sources
├── growth-log.json                 # Append-only log of EVERY engagement action (anti-spam ledger)
├── growth-progress.json            # Follower count snapshots over time
├── growth-strategy.md              # Current engagement strategy (rewritten on each pivot)
└── screenshots-growth/             # Screenshots of target posts + our comments
```

## Campaign Definition

When the user says "grow to N followers" or "get to N by <time>", create/load the campaign:

```bash
cat > .fb-research/projects/<page-name>/growth-campaign.json << 'EOF'
{
  "pageName": "<page-name>",
  "niche": "<niche>",
  "targetAudience": "Mexican/Hispanic football community in the USA",
  "goalFollowers": 200,
  "startFollowers": <current_followers>,
  "startTime": "<YYYY-MM-DD HH:MM:SS>",
  "deadline": "<YYYY-MM-DD HH:MM:SS> (default start+24h)",
  "status": "active",
  "checkpointIntervalHours": 3,
  "currentPlan": "<short plan label>"
}
EOF
```

Get the current follower count by navigating to our page and reading it:

```javascript
() => { const m = document.body.innerText.match(/([\d.,]+[KMB]?)\s*followers/); return m ? m[1] : 'unknown'; }
```

**Default goal:** +200 followers in 24h. **Default audience:** Mexican/Hispanic football fans in the USA. If the user gives different numbers, use theirs.

## Anti-Ban Safety Rules (NON-NEGOTIABLE)

These keep the page alive. Volume without these rules = permanent ban.

| Rule | Limit |
|------|-------|
| Comments per hour (hard cap) | Max **12/hour** across all pages |
| Comments per day (hard cap) | Max **60/day** first campaign; never exceed 100/day |
| Comments on one post | Max **1** top-level comment per post |
| Pages engaged per hour | Max **3 different pages/hour** |
| Identical comments | **Never** reuse the same text; every comment must be unique |
| Links / @mentions of our page in comments | **Never** — Facebook treats it as self-promotion spam |
| Reply depth | Reply to replies on our comments (good), but stop after 3 levels |
| Timing | Space comments by **4-8 minutes**; never burst |
| Same post twice | Never comment on a post you already commented on |
| First campaign warm-up | First 24h: stay under 30 comments; ramp up day 2+ |

**Why:** Facebook's spam classifier flags (a) repetition, (b) link dropping, (c) fast bursts, (d) @mentioning your own page everywhere. Comments convert followers purely via the visible page name next to the comment — no links needed.

## Steps

### 1. Load or Create Campaign + Own-Page Audit

Load existing campaign state:

```bash
cat .fb-research/projects/<page-name>/growth-campaign.json 2>/dev/null
cat .fb-research/projects/<page-name>/growth-progress.json 2>/dev/null
cat .fb-research/projects/<page-name>/growth-strategy.md 2>/dev/null
cat .fb-research/projects/<page-name>/growth-targets.json 2>/dev/null
cat .fb-research/projects/<page-name>/growth-log.json 2>/dev/null
```

If no campaign file exists, do the **own-page audit**:

1. Navigate to our page (`<pageUrl>` from config).
2. Record: current followers, posts/reels visible, what the most recent 5 posts are about, the overall tone of our content.
3. Identify **conversion hooks** — why would someone follow us?
   - Historic football moments ("historian" angle)
   - Match analysis with hot takes
   - Referee controversy content
   - The "we were robbed" / "history repeats" angle (World Cup 2026, Leagues Cup 2026)
4. Write these into `growth-strategy.md` under "OUR HOOKS".

### 2. Build the Follower-Source Target List

We grow by commenting on posts where **our exact audience already hangs out**. Two source types:

#### 2a. Niche competitor pages (primary)

Small-to-mid pages (10K-500K followers) in the football/history/controversy niche whose followers are Mexican/Hispanic football fans. From the initial recon these include:

- **Leyenda Escarlata** (66K) — Toluca history, "Nuestra Grandeza Tiene Su Historia". Perfect audience overlap. Hot posts: TOLUCA vs Seattle Sounders (Leagues Cup 2026, tonight 20:00), "El primer campeón de Liga 66/67" (history post with active comments).
- **Mundo Info Sport** (168K) — "contamos historias que nacen de las noticias" (historian angle). Hot post: Vinicius Jr cleans his Instagram (current drama).
- **Mundo Deportivo Nicaragua** (257K) — baseball-heavy; deprioritize unless football posts appear.

Exclude big pages (>1M) for commenting — our comment drowns and the audience is diluted. Reuse `discovered-competitors.json` and `engagement-opportunities.json` if they exist.

For each target page, capture and save to `growth-targets.json`:

- page name + URL + follower count
- **Audience profile**: what the commenters argue about, their slang, their favorite topics (from reading comments)
- candidate posts (URL + topic + comment count)

#### 2b. Trending niche posts (supplementary)

Search Facebook for hot topics in the niche and add posts with **active comment threads (10+ comments)** from pages of any size (even big pages here are OK for volume — the goal is stealing audience from the commenters themselves, who get notified of our reply):

```bash
chrome-devtools navigate_page --url "https://www.facebook.com/search/posts/?q=<URL_ENCODED_KEYWORD>"
```

Hot-search keywords to try (Aug 2026): `leagues cup`, `toluca`, `arbitraje`, `vinicius`, `seleccion mexico`, `messi`, `liga mx`.

### 3. Audience Reconnaissance (per target post)

For each candidate post, navigate to it, extract the top comments, and learn the audience:

```javascript
() => {
  const els = document.querySelectorAll('[role="article"]');
  const out = [];
  els.forEach(el => {
    const t = el.innerText?.trim();
    if (!t || t.length < 10) return;
    const like = t.match(/(\d+[KMB]?)\s*(reactions?|likes?)/i);
    const nameEl = el.querySelector('a[href*="/user/"], a[href*="/profile.php"]');
    out.push({ name: nameEl?.innerText?.trim() || '?', text: t.substring(0, 200), likes: like ? like[1] : '0' });
  });
  return JSON.stringify(out.slice(0, 15), null, 2);
}
```

Record per post:
- Top 5 most-liked comments and WHY they got likes
- The audience's hot button (anger at referee, nostalgia, team pride, transfers)
- Slang actually used by THIS audience (not the generic list — the real voice)

### 4. Craft Comments That Convert

A comment converts a follower when it makes someone think **"this guy gets it"** and click our name. Formulas that work:

| Type | Formula |
|------|---------|
| **Nostalgia historian** | "[Historic parallel to current match/player] ... y así fue como [history repeats]". Uses our historian angle to stand out. |
| **Shared anger** | Agree with the audience's rage in their exact slang, then one-up it with a fresh angle. |
| **Insider knowledge** | Drop a stat/detail nobody mentioned → authority → people check your page. |
| **Contrarian humor** | Playful take against the crowd that still shows we're one of them. |
| **Replies to real users** | Reply to an existing commenter — they get a notification, click your name. Highest conversion. |

Rules:
- Match the post's topic 100%. Never comment off-topic.
- Use the audience's actual slang (Mexican: wey, no mames, qué pedo, neta, chale, ándale).
- 1-3 sentences. Short wins.
- **Unique every time.** Vary structure, not just words.
- End with something that invites replies (rhetorical question / hot take).

Write the plan for this burst into `growth-strategy.md` (target pages, posts, comment angles, order, spacing).

### 5. Execute the Engagement Burst

For each target post:

1. Navigate to the post permalink.
2. Confirm the thread is active (has comments).
3. Post **1 comment** (either top-level or a reply to a real user — prefer replies early in the campaign, they convert better).
4. Wait 4-8 minutes between comments.
5. Stop at the hourly caps (12/hr, 3 pages/hr).
6. Screenshot the post with our comment visible → `screenshots-growth/`.

**Posting a comment** (as the page):

```bash
# Use the comment textbox snapshot uid (find it first):
#   chrome-devtools take_snapshot
#   -> textbox "Comment as <page-name>"
chrome-devtools fill --uid "<textbox_uid>" --value "<comment text>"
# Verify text, then press Enter:
chrome-devtools press_key --key "Enter"
# Confirm the comment posted (check snapshot for our comment text)
```

**Log EVERY action** to `growth-log.json` immediately (append):

```json
{
  "time": "<YYYY-MM-DD HH:MM:SS>",
  "action": "comment" ,
  "targetPage": "<page>",
  "targetUrl": "<post permalink>",
  "type": "top_level|reply",
  "text": "<exact comment text>",
  "result": "posted|failed|skipped"
}
```

The log is the anti-spam ledger — if you ever consider reusing a comment, the log tells you not to.

### 6. Checkpoint & Resume (every 2-3 hours)

After a burst, or when a checkpoint interval elapses:

1. Navigate to our page, read the follower count.
2. Append a snapshot to `growth-progress.json`:

```json
{
  "time": "<YYYY-MM-DD HH:MM:SS>",
  "followers": <count>,
  "deltaSinceStart": <count - startFollowers>,
  "goal": 200,
  "onTrack": true/false,
  "commentsPosted": <count from growth-log>
}
```

3. **Pivot logic** — read the trend and change the plan if needed:
   - **On track** (projected to hit goal): keep the same targets, maybe increase volume within caps.
   - **Off track** (delta < expected, or 0): change at least 2 of these — target pages (new ones), comment style (switch from top-level to replies or vice versa), post types (video posts vs photo), timing (evening 7-10pm = peak).
   - **Negative delta**: STOP commenting for 2h (possible shadowban), post on our own page instead, then resume.
   - Rewrite `growth-strategy.md` with the new plan and note WHY you pivoted.
4. **Report to the user** (concise):
   - Current followers / goal
   - Delta since last checkpoint
   - Comments posted this session
   - What's working / what you changed
   - **Ask them to resume in 2-3 hours** (that's the checkpoint loop).

### 7. Completion

When `followers >= goal` (or deadline hits):

- Mark campaign `status: "completed"`.
- Write a short summary to `growth-strategy.md`: final count, total comments, what converted, what to repeat next campaign.
- Report to the user: 🎉 goal reached, what worked, suggested next goal.

If deadline hits without reaching goal: report honestly, summarize what was tried, and propose a new goal/plan for the next 24h.

## Decision Cheat Sheet

| Situation | Action |
|-----------|--------|
| User says "engage until we get 200 followers" | Create campaign, audit own page, build targets, start burst |
| A post has no comments yet | Skip (no audience to steal) |
| Hourly caps reached | Pause, report checkpoint, ask to resume later |
| Comment not posting | Check it's as the PAGE profile, not a personal profile |
| Growth stalled | Pivot: new pages + switch comment type + peak-time posting |
| User asks "is the task complete?" | Check progress, run a checkpoint, report |
| Follower count dropped | Suspect shadowban → stop commenting, post own content 2h, resume |
| Campaign completed | Summarize + propose next goal |

## Fallback: If Chrome DevTools Fails

If Facebook won't load in Chrome DevTools:

```bash
websearch "site:facebook.com <niche_keyword> 2026"
```

Use search results to identify hot posts and target pages, craft the comments per the formulas above, and give the user a ready-to-paste comment list with the post URLs. Log them as `result: "manual"` so they don't get re-commented.
