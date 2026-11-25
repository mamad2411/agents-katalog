---
name: market-social
description: Multi-platform social content with platform-native formatting and character limits for X, LinkedIn, Instagram, TikTok, YouTube Shorts, and Threads. Invoke whenever the user says "social posts", "content calendar", "LinkedIn post", "tweet", "Instagram caption", or runs `/market social <topic>`. Matches BRAND-VOICE.md if present.
---

# Market Social — Multi-Platform Content

Generate social content that respects each platform's native format. A LinkedIn post is not a long tweet. An Instagram caption is not a blog intro. A TikTok script is not a headline.

## Platform Specs (character limits and native formats)

| Platform | Limit | Native format |
|---|---|---|
| **X (Twitter)** | 280 chars (free) / 25,000 (Premium) | Punchy single posts or threads. First tweet hooks. Threads use "🧵" or numbered. |
| **LinkedIn** | 3,000 chars post body | Story-led, line-break-heavy, no links above the cut (algorithmic penalty). |
| **Instagram** | 2,200 caption / 30 hashtags max | Hook in first line (before "more"), 5–15 hashtags in first comment, emoji for scanability. |
| **TikTok** | 2,200 caption / video is the content | Caption is a hook. Script should be 15–60s with hook in first 3s. |
| **YouTube Shorts** | Video + 100-char title | Hook first 2 seconds, pattern interrupt at 5s. |
| **Threads** | 500 chars | Conversational, less polished than LinkedIn. |
| **Facebook** | 63,206 chars (use ~80 for best reach) | Short + link, or native video. |
| **Pinterest** | 500 char description / vertical image | Keywords + title are the ranking signal. |

## Content Pillars (pick 3–5 per brand)

| Pillar | Purpose | Example formats |
|---|---|---|
| **Educational** | Teach, build trust | How-tos, frameworks, breakdowns |
| **Behind the scenes** | Humanize | Day-in-life, process, team |
| **Social proof** | Credibility | Case studies, testimonials, stats |
| **Contrarian / POV** | Attention + distinction | Hot takes, pattern breaks |
| **Tactical** | Immediate value | Tips, hacks, templates |
| **Story** | Emotional connection | Origin, founder, customer stories |
| **Entertainment** | Reach | Memes, humor (if on-brand) |
| **Product** | Direct promo | Launches, updates, demos |

The 80/20 rule: 80% value-driven (education, story, proof), 20% direct promo.

## Platform-specific post structures

### X — Single
```
Hook (line 1)
Evidence / story / punch
CTA (optional)
```

### X — Thread
```
1/ Hook — specific, contrarian, or curiosity
2/–N/ Beats: context → story → lesson → example → takeaway
Last/ Wrap + soft CTA ("If this helped, RT the top.")
```

### LinkedIn
```
Line 1: Hook (must survive the "see more" cut)
Line 2: Blank
Line 3–4: Setup
[line breaks]
Story / insight / framework in short lines
[line breaks]
Takeaway
[line breaks]
CTA — question or invitation
(No external links in body. Drop links in first comment.)
```

### Instagram caption
```
Hook (before "more")
Blank line
Story or breakdown with emoji bullets
Takeaway
CTA (save, share, comment)
.
.
.
#5–15 hashtags
```

### TikTok / Shorts script
```
[0–3s] HOOK — visual + spoken pattern interrupt
[3–8s] SETUP — what this is about
[8–25s] PAYOFF — the actual thing
[25–55s] PROOF or REPEAT
[last 2s] CTA — "follow for more", "link in bio"
```

## Pre-flight

1. Load `BRAND-VOICE.md` if present.
2. Ask: topic, target platforms, frequency, goal (awareness / engagement / leads / sales).
3. Confirm content pillars if not already documented.

## Output Format

When the user asks for a post pack:

```markdown
## Social Post Pack — [Topic]

**Brand voice:** [summary from BRAND-VOICE.md or inferred]
**Pillar:** [which one]
**Goal:** [awareness / engagement / etc]

---

### X (Single)
[Draft — must fit 280 chars; include char count]

### X (Thread)
1/ [hook]
2/ [beat]
...

### LinkedIn
[Full post with line breaks preserved]

### Instagram
**Caption:**
[Hook + body]

**Hashtags (first comment):**
#tag1 #tag2 ...

### TikTok / Shorts script
**Hook (0–3s):** [visual + line]
**Setup (3–8s):** ...
**Payoff (8–25s):** ...
**CTA (last 2s):** ...

### Threads
[Draft — under 500 chars]

---

### Repurposing notes
[How to adapt the same idea for other platforms if the user wants more coverage]
```

## When generating a content calendar

Use `python3 scripts/social_calendar.py --pillars "<pillar1,pillar2,...>" --days 30` to generate a pillar-aware skeleton, then fill in specific topics. Output as a table:

| Day | Pillar | Platform(s) | Topic | Status |
|---|---|---|---|---|

## Quality Bar

- Respect the character limits. A 320-char "tweet" wastes the client's time.
- Lead with the hook on every platform. If the first line is boring, the rest is invisible.
- Don't copy-paste the same post across platforms. Rewrite for each.
- Never invent hashtags that don't exist or that have been hijacked.
- If the client has no strong POV, say so — social without a POV dies slowly.
