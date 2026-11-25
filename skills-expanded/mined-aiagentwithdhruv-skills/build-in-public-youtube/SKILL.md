---
name: build-in-public-youtube
description: Use when Dhruv shares a long-form (1-3 hour) team meeting recording or transcript and wants to publish it on YouTube as build-in-public content. Produces title, description, thumbnail prompt, tags, chapters, and pinned comment. Works from RTF, TXT, MD transcripts or audio files (with transcribe.py).
---

# Build-in-Public YouTube — Long-Form Team Meeting → YouTube Episode

## What this skill does

Turns Dhruv's long Saturday/Sunday team sync recordings (Afeefa, Shailendra, Vishal, Navpreet + Dhruv) into a complete YouTube upload pack:

- **Title** (clickable, honest, build-in-public framed)
- **Description** (chapter timestamps, what's covered, links, team credits, hashtags)
- **Thumbnail prompt** (Gemini-paste-ready, brand palette: deep dark + neon cyan #18D1E0 + metallic grey)
- **Tags** (25-30 YouTube tags)
- **Chapters** (with timestamps if known, otherwise structural placeholders)
- **Pinned comment** (CTA + community + product links)

This is the canonical format for the AIwithDhruv "Build-in-Public Diaries" series.

---

## When to invoke

Trigger phrases from Dhruv:
- "Here's the Sunday team recording, write a YouTube post"
- "Make a YouTube title for this transcript"
- "We did 2 hours yesterday, can we upload it"
- "Build-in-public episode from this"
- Or just shares a `.rtf` / `.txt` / `.md` transcript inside `Library/Mobile Documents/com~apple~TextEdit/Documents/` or `inbox/recordings/`

---

## Series identity (locked)

| Field | Value |
|------|------|
| Channel | AIwithDhruv (main) |
| Series name | **Build-in-Public Diaries** |
| Episode prefix | `Build-in-Public Diaries — Ep N` |
| Cadence | 1-2 long-form episodes per week (weekend syncs + Wednesday mid-week sync if any) |
| Duration | 1-3 hours unedited (NO heavy editing — raw is the brand) |
| Voice | First-person from Dhruv ("we built", "I shipped", "we lost", never "the team did") |
| Brand palette | Deep dark `#0A0E1A` + neon cyan `#18D1E0` + metallic grey. NO orange / red / teal-mint. (See `brand_palette.md`) |
| Format | 16:9, 1080p min, thumbnails 1280x720 |

---

## Inputs you need before generating

If any of these are missing, ASK Dhruv before drafting:

1. **Episode number** (default to next sequential: check the channel or ask)
2. **Recording date** (e.g., "Apr 26, 2026") — used in title + filename
3. **Recording length** in HH:MM (estimate from word count if no audio: ~150 words/min)
4. **Path to transcript** (`.rtf` / `.txt` / `.md`)
5. **Public revenue claim allowed?** (default: NO. Don't drop ₹/$ numbers without explicit approval)
6. **Specific milestone to lead with?** (e.g., "Vishal joined", "AutoBOQ shipped", "first paid client")

If you have the transcript path but no metadata, run `wc -w <file>` to estimate length and propose Episode N + date + suggested headline angle. Then wait for confirmation.

---

## Step-by-step process

### Step 1 — Read the transcript fully

Convert RTF if needed: `textutil -convert txt -stdout "input.rtf" > /tmp/transcript.txt`

Read end-to-end. Don't skim. Look for:
- **Strategic decisions** (pivots, hires, product calls)
- **Real numbers** (only use them if Dhruv approved public-revenue mode)
- **Tools/stack mentioned** (Claude, Antigravity IDE, Blotato, Plivo, Flow, Vercel, etc.)
- **Honest losses / blockers** (these make the best build-in-public hooks)
- **Personal moments** (team onboarding, philosophy, framework calls)

### Step 2 — Extract the 5 anchor points

Every episode pack is built on these 5 anchor points pulled from the transcript:

1. **The headline decision** — the one thing this meeting will be remembered for
2. **The week's score** — wins shipped, losses absorbed
3. **The team motion** — who did what, who joined, who graduated
4. **The technical reveal** — one stack/tool/pattern that was tested or chosen
5. **The next-7-days commit** — public commitment so viewers can hold us accountable

Write these 5 lines first. Title and description flow from them.

### Step 3 — Generate the upload pack

Apply the templates in **Reference Templates** below. Always show the full pack to Dhruv for approval before suggesting upload. Never auto-publish (see `feedback_never_auto_publish.md`).

### Step 4 — Save the pack

Write the final pack to `/tmp/<recording-filename>_episode_pack.md` so Dhruv can copy-paste into YouTube directly. Print location at end.

---

## Reference Templates

### Title formulas (pick one, A/B is fine)

**Formula 0 — Setup / Foundation video (use ONCE, for the genesis "operating manual" video):**
```
{$0 MRR / honest current state}, {$tool spend}, {N products}: How {brand} Actually Works ({Setup / Operating Manual / Day 0})
```
Example: `$0 MRR, $400/mo Tools, 4 Products: How AIwithDhruv Actually Works (Build-in-Public Setup)`
Use this only for the first/foundation video that explains how the team and stack are wired. NOT for ongoing weekly episodes.

**Formula A — Decision lead (best for big pivots/hires, ongoing episodes):**
```
Build-in-Public Diaries — Ep {N}: {THE ONE DECISION} | Day {X} of the 45-Day Sprint
```
Example: `Build-in-Public Diaries — Ep 3: We Hired 4 People in One Weekend | Day 12 of the 45-Day Sprint`

**Formula B — Stakes lead (best for weeks with money/risk on the line):**
```
{X Hours} of Real Strategy: How We're Trying to Hit ₹{Y} in {Z} Days (Build-in-Public Diaries Ep {N})
```
Use only if revenue mode = approved.

**Formula C — Team lead (best when a meeting introduces team):**
```
Meet the Team Building 4 AI Products in Public — Sunday Sync Ep {N}
```

**Formula D — Stack lead (best when one tool/tech is the star):**
```
We Replaced {Old Tool} With {New Tool} — Live Decision in Sunday Sync (Build-in-Public Ep {N})
```

**Formula E — Honesty hook (use anytime real numbers are public):**
```
{$honest current state}: Here's the {N-Day} Plan to Change That ({Build-in-Public Ep N})
```
Example: `We're at $0 MRR. Here's the 45-Day Plan to Land Our First Client (Build-in-Public Ep 4)`

**Title rules:**
- 60-70 chars max for full visibility
- No emoji in title (looks unserious for B2B audience)
- Number → real number (no clickbait inflation)
- Episode number always present
- "Build-in-Public Diaries Ep N" recognized somewhere in the title

### Description template

```
{ONE-LINE HOOK — what this episode is actually about, 200 chars max}

This is the unfiltered {duration} Sunday sync from {date}. No edits. Real strategy, real arguments, real pivots.

━━━━━━━━━━━━━━━━━━━━
👥 WHO'S IN THE ROOM
━━━━━━━━━━━━━━━━━━━━
Dhruv Tomar — AI Architect & Founder, AIwithDhruv
{LIST EACH TEAM MEMBER PRESENT WITH 1-LINE ROLE}

━━━━━━━━━━━━━━━━━━━━
📋 WHAT WE COVER
━━━━━━━━━━━━━━━━━━━━
{5 ANCHOR POINTS as bullet list — 1 line each}

━━━━━━━━━━━━━━━━━━━━
⏱️ CHAPTERS
━━━━━━━━━━━━━━━━━━━━
{TIMESTAMPS — see Chapter Generation below}

━━━━━━━━━━━━━━━━━━━━
🛠️ TOOLS & STACK MENTIONED
━━━━━━━━━━━━━━━━━━━━
{LIST OF TOOLS WITH PURPOSE — 1 line each, no affiliate links unless explicitly approved}

━━━━━━━━━━━━━━━━━━━━
🚀 PRODUCTS WE'RE BUILDING
━━━━━━━━━━━━━━━━━━━━
QuotaHit — AI Inbound Revenue OS (CRM + AI calling) | quotahit.com (when live)
AutoBOQ — AI construction estimation for SMB contractors | github.com/aiagentwithdhruv/autoboq
IndianWhisper — Hindi/Hinglish/Indian-English voice-to-text | indianwhisper.com
Angelina-OS — Personal AI OS, 30+ tools

━━━━━━━━━━━━━━━━━━━━
📌 LINKS
━━━━━━━━━━━━━━━━━━━━
🌐 Site: https://aiwithdhruv.com
💼 LinkedIn: https://www.linkedin.com/in/aiwithdhruv/
🐦 X: https://x.com/aiwithdhruv
📸 Instagram: https://instagram.com/aiwithdhruv
🐙 GitHub: https://github.com/aiagentwithdhruv
{PRODUCT-SPECIFIC LINKS RELEVANT TO THIS EPISODE}

━━━━━━━━━━━━━━━━━━━━
👋 ABOUT
━━━━━━━━━━━━━━━━━━━━
We're building 4 AI products in public — QuotaHit, AutoBOQ, IndianWhisper, Angelina-OS — using Claude Code as a workflow engine. This channel is the unfiltered process. If you're building, hiring, or learning AI for real production work — subscribe.

#BuildInPublic #AIwithDhruv #ClaudeCode #AIAgents #SaaS #Founder #Indian{Optional product hashtags — pick 2-3 max}

{TEAM CREDIT BLOCK — only when team appears on camera or is named. ALWAYS check team_linkedin_profiles.md NO-PUBLIC-CREDIT list before adding anyone:}
Team:
- Afeefa Albeena Sheikh — AI Architect | https://www.linkedin.com/in/afeefa-albeena-sheikh-298857192/
- Shailendra Gour — Developer | https://www.linkedin.com/in/shailendra-gour-01922b22b/
- Navpreet Kaur — AI GrowthLead | https://www.linkedin.com/in/navpreet-kaur-b22521305/
```

**CRITICAL: NO-PUBLIC-CREDIT enforcement.** Some team members have explicitly opted out of public promotion (currently: Vishal). NEVER name them in descriptions, NEVER link them, NEVER include them in credit blocks — even if they appear on camera or are mentioned by other speakers in the recording. Refer to "the team" or "an internal teammate" if needed. The full NO-PUBLIC-CREDIT list lives in `team_linkedin_profiles.md`.

**Description rules:**
- First 150 chars are the hook (these show in search snippet)
- Always include chapters — long-form needs them for completion rate
- Always credit team using canonical LinkedIn URLs from `team_linkedin_profiles.md`
- Hashtag count: 6-9 max (YouTube cap = 15, but quality > quantity)
- Never mention source creators (per `feedback_content_voice.md`)
- Don't drop revenue numbers unless Dhruv explicitly opts in for this episode

### Chapter generation

If timestamps aren't provided, build chapters from the transcript's structural sections. For long-form team meetings, default outline:

```
00:00 Cold open / context
{XX:XX} Strategy block — the week's plan
{XX:XX} {PRODUCT 1} update
{XX:XX} {PRODUCT 2} update
{XX:XX} {PRODUCT 3} update
{XX:XX} Team motion (hires, role changes, dispatch)
{XX:XX} Tools / stack discussion
{XX:XX} Content + social media plan
{XX:XX} Open questions and pending decisions
{XX:XX} Action items + commits for next 7 days
{XX:XX} Wrap
```

Mark unknown times with `[XX:XX]` so Dhruv can fill in from YouTube Studio later.

**Min 8 chapters, max 14.** YouTube algorithm rewards 8+ chapters on long-form.

### Thumbnail prompt formula (Gemini-paste-ready)

Always 16:9, 1280×720 minimum. Brand palette: deep dark + neon cyan + metallic grey ONLY.

Template (paste this into Google Gemini, free):

```
Create a 16:9 cinematic YouTube thumbnail (1280x720, sharp print-ready).

SCENE:
{ONE LINE — the scene that anchors the episode. Examples:
- "A founder at a desk surrounded by 4 floating product UIs (CRM, voice app, design tool, dashboard) with team members visible behind glass walls"
- "A whiteboard packed with sticky notes labelled QuotaHit / AutoBOQ / IndianWhisper / Angelina, with a calendar showing 45 DAYS in glowing cyan"
- "A war-room table with 5 laptops open, neon city skyline behind, stack of business cards labelled with the 4 product names"}

STYLE:
- Cinematic photography, shallow depth of field, dramatic lighting
- Color palette STRICTLY: deep dark navy/black background (#0A0E1A) + neon cyan accents (#18D1E0) + metallic grey/silver highlights
- NO orange, NO red, NO teal-mint — these are off-brand
- Slight glow / volumetric light from cyan elements
- Photorealistic, NOT illustrated, NOT cartoon

TYPOGRAPHY OVERLAY:
- Top-left or bottom-right: bold sans-serif "{HEADLINE TEXT — 3-6 words MAX, ALL CAPS}" in cyan or white
- Tiny brand badge bottom-left: "AIwithDhruv • Build-in-Public • Ep {N}"
- TEXT MUST BE SHARP, READABLE, NO BLUR, NO OVERLAP WITH FACES

COMPOSITION:
- Subject(s) in left third, headline text in right two-thirds (or flip)
- Generous safe margin (5% around all edges)
- Mobile preview rule: must read at 200px wide

NEGATIVE PROMPT:
no orange, no red, no warm yellow, no teal mint, no cluttered backgrounds, no stock-photo people, no clipart, no low resolution, no text overlap, no face cutoff, no distorted text
```

**Thumbnail rules:**
- Always 16:9
- Always brand palette (no exceptions)
- Headline text always 3-6 words max
- Always include episode badge
- Test mobile preview before approving

### Tags (25-30 YouTube tags)

Standard pool — pick relevant + add 5-8 episode-specific:

```
build in public, ai with dhruv, claude code, ai agents, multi agent ai,
ai startup, indian founder, saas founder, build in public india, ai workflow,
claude code tutorial, ai automation, n8n automation, ai voice agent,
ai construction estimation, ai crm, ai sales, ai infrastructure,
solo founder, agency owner, indie hacker, anthropic claude,
sunday sync, founder diaries, real startup, no edit founder vlog,
{add 5-8 episode-specific: e.g., quotahit, autoboq, indianwhisper, angelina ai, plivo twilio, blotato, vercel deploy}
```

### Pinned comment (always pin)

```
👋 Thanks for watching the full episode.

What we'd love from you:
1. Reply with the timestamp of the most useful section — helps us know what to dig into next.
2. If you're a SaaS founder / agency in {AU/UK/US/ME/IN} and want to talk AI deployment for your business — DM me on LinkedIn (link in description).
3. Want the agent prompts we mentioned? Star our open-source repo: github.com/aiagentwithdhruv/AI_Lab

We post one of these every Sunday. See you next week. — Dhruv
```

---

## Output format (the "episode pack")

Save the final pack as a single markdown file at `/tmp/<source-filename>_episode_pack.md` with this structure:

```markdown
# Episode Pack — Build-in-Public Diaries Ep {N}
## Source: {transcript filename} · Date: {YYYY-MM-DD} · Length: ~{HH:MM}

## 1. THE 5 ANCHOR POINTS
1. ...
2. ...
3. ...
4. ...
5. ...

## 2. TITLE (3 variants — pick one)
A. ...
B. ...
C. ...

## 3. DESCRIPTION
{full description copy-paste ready}

## 4. CHAPTERS
{full chapter list with placeholder timestamps}

## 5. THUMBNAIL PROMPT (paste into Google Gemini)
{full prompt}

## 6. TAGS (copy comma-separated)
{tags}

## 7. PINNED COMMENT
{full pinned comment}

## 8. UPLOAD CHECKLIST
- [ ] Title set
- [ ] Description pasted (chapters render correctly)
- [ ] Thumbnail uploaded (1280x720, brand palette verified)
- [ ] Tags added
- [ ] Playlist: "Build-in-Public Diaries"
- [ ] Visibility: Public (or Unlisted if first revenue numbers are mentioned and not approved)
- [ ] End screen: subscribe + previous episode + AI_Lab repo
- [ ] Pinned comment posted
- [ ] Cross-post LinkedIn 5-line summary + YouTube link
- [ ] Cross-post X 280-char summary + YouTube link
```

---

## Cross-platform companion (after YouTube upload)

When the YouTube link is live, immediately produce 3 follow-up posts. Use canonical team URLs from `team_linkedin_profiles.md` and apply the brand palette and tone rules.

1. **LinkedIn post (1500-2200 chars):** lead with the headline decision, list the 5 anchor points, embed YouTube link, end with a question. 6-8 hashtags.
2. **X thread (5-7 tweets):** each tweet ≤ 270 chars, last tweet has the YouTube link.
3. **Discord drop** in the AIwithDhruv private server `#weekly-digest` channel: bullet summary + link.

---

## Rules locked

- **Never auto-publish** — always show pack to Dhruv. (`feedback_never_auto_publish.md`)
- **Never invent revenue numbers.** Only use ones Dhruv has approved for public mention this episode.
- **Voice = 100% Dhruv's.** Don't credit research sources, podcast frameworks, etc. (`feedback_content_voice.md`)
- **Real builder claims only.** "I'm planning to" not "I shipped." (`session_handoff_apr26.md` rule 6)
- **Brand palette is non-negotiable.** Cyan + dark + grey. No orange/red/teal-mint. (`brand_palette.md`)
- **Always credit team** using canonical LinkedIn URLs. (`team_linkedin_profiles.md`)
- **Sparse + flowing** in any handwritten companion graphics. (`feedback_handwritten_flow.md`)

---

## Quick reference — file locations

| Asset | Path |
|------|------|
| Source transcripts | `~/Library/Mobile Documents/com~apple~TextEdit/Documents/*.rtf` or `MSBC-Group/inbox/recordings/` |
| Audio transcribe tool | `python3 MSBC-Group/tools/transcribe.py <file>` |
| Brand palette ref | memory: `brand_palette.md` |
| Team LinkedIn URLs | memory: `team_linkedin_profiles.md` |
| Content voice rule | memory: `feedback_content_voice.md` |
| Auto-publish rule | memory: `feedback_never_auto_publish.md` |
| Handwritten flow rule | memory: `feedback_handwritten_flow.md` |
| Output pack location | `/tmp/<source-filename>_episode_pack.md` |
| Skill home (this file) | `aiwithdhruv-skills/build-in-public-youtube/SKILL.md` |

---

## Why this skill exists

Dhruv's competitive moat is showing the work — not the polished version, the actual 2-hour Sunday strategy session. Most founders edit out the boring parts. We don't. Long-form raw is the brand.

But long-form needs structured packaging or YouTube buries it. This skill is the packaging machine — every Sunday recording goes through this same pipeline so the channel develops a recognizable rhythm: Build-in-Public Diaries, Episode N, brand colors, real team, real numbers (when approved), real progress.

The compounding play: 50 episodes in, anyone evaluating Dhruv as a consultant or hire has watched the actual decisions get made. That's a 100x stronger signal than any pitch deck.
