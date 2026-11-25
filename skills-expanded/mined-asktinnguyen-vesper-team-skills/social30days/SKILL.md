---
name: social30days
description: Research a topic from the last 30 days on social media (TikTok, Instagram, Facebook, Google Trends), become an expert on what's viral, and write copy-paste-ready prompts. Triggers include "social media research", "what's trending on", "social30days", "viral trends".
---

# social30days: Research Any Topic from the Last 30 Days on Social Media

Research ANY topic across TikTok, Instagram, Facebook, and Google Trends. Surface what's going viral, trending hashtags, popular creators, and engagement patterns.

Use cases:
- **Viral Trends**: "AI art trends", "dance challenges" → find what's going viral now
- **Creator Research**: "cooking TikTok", "fitness Instagram" → discover top creators and content
- **Brand Research**: "Nike social media", "product launches" → track brand engagement
- **Hashtag Research**: "trending hashtags for travel" → find effective hashtags
- **General**: any topic → understand the social media landscape

## CRITICAL: Parse User Intent

Before doing anything, parse the user's input for:

1. **TOPIC**: What they want to learn about
2. **TARGET TOOL** (if specified): Where they'll use the prompts
3. **QUERY TYPE**: What kind of research:
   - **VIRAL** - "trending X", "viral X" → current viral content
   - **CREATOR** - "best X creators", "top X accounts" → popular creators
   - **HASHTAG** - "hashtags for X", "trending tags" → effective hashtags
   - **BRAND** - "X social media", "X engagement" → brand tracking
   - **GENERAL** - anything else → broad social understanding

**Store these variables:**
- `TOPIC = [extracted topic]`
- `TARGET_TOOL = [extracted tool, or "unknown" if not specified]`
- `QUERY_TYPE = [VIRAL | CREATOR | HASHTAG | BRAND | GENERAL]`

---

## Setup Check

The skill works in multiple modes:

1. **Full Mode** (CrowdTangle token): TikTok Creative + Google Trends + CrowdTangle + WebSearch
2. **Free Mode** (no keys): TikTok Creative + Google Trends + WebSearch (still excellent)

**API keys are OPTIONAL.** The skill works great with zero keys.

### First-Time Setup (Optional)

```bash
mkdir -p ~/.config/social30days
cat > ~/.config/social30days/.env << 'ENVEOF'
# social30days API Configuration
# CrowdTangle is optional - skill works with free sources

# For Facebook/Instagram engagement data
CROWDTANGLE_TOKEN=
ENVEOF

chmod 600 ~/.config/social30days/.env
```

**DO NOT stop if no keys are configured.** Proceed with free mode.

---

## Research Execution

**Step 1: Run the research script**
```bash
python3 ~/.claude/skills/social30days/scripts/social30days.py "$ARGUMENTS" --emit=compact 2>&1
```

The script will automatically:
- Scrape TikTok Creative Center trends (free)
- Query Google Trends for interest data (free)
- Query CrowdTangle for FB/IG posts (if token exists)
- Signal that WebSearch should supplement results

**Step 2: Do WebSearch for platform-targeted coverage**

Choose search queries based on QUERY_TYPE:

**If VIRAL** ("trending X", "viral X"):
- Search for: `"{TOPIC}" viral tiktok`
- Search for: `"{TOPIC}" instagram viral reel`
- Search for: `"{TOPIC}" site:tiktok.com`
- Search for: `#{TOPIC_NO_SPACES} trending`

**If CREATOR** ("best X creators", "top X accounts"):
- Search for: `"{TOPIC}" top creators tiktok`
- Search for: `"{TOPIC}" popular influencer instagram`
- Search for: `"{TOPIC}" best accounts follow`

**If HASHTAG** ("hashtags for X"):
- Search for: `"{TOPIC}" best hashtags`
- Search for: `"{TOPIC}" trending hashtags tiktok instagram`
- Search for: `"{TOPIC}" hashtag strategy`

**If BRAND** ("X social media"):
- Search for: `"{TOPIC}" social media strategy`
- Search for: `"{TOPIC}" engagement viral post`
- Search for: `"{TOPIC}" site:facebook.com`

**If GENERAL**:
- Search for: `"{TOPIC}" social media 2026`
- Search for: `"{TOPIC}" tiktok instagram trending`
- Search for: `"{TOPIC}" viral`

For ALL query types:
- **USE THE USER'S EXACT TERMINOLOGY**
- INCLUDE: TikTok, Instagram, Facebook content + aggregator coverage
- **DO NOT output "Sources:" list**

**Depth options:**
- `--quick` → Faster, fewer sources
- (default) → Balanced
- `--deep` → Comprehensive

---

## Synthesize All Sources

After all searches complete, internally synthesize:

1. Weight items with **high engagement** (views, likes, shares) HIGHEST
2. Weight **trend data** (TikTok Creative, Google Trends) MEDIUM
3. Identify **cross-platform patterns** (strongest signals)
4. Note **platform-specific differences** (what works on TikTok vs IG)
5. Extract top 3-5 actionable insights

---

## Show Summary + Invite Vision

**Display in this EXACT sequence:**

**FIRST - What's trending (based on QUERY_TYPE):**

**If VIRAL** - Show viral content:
```
🔥 What's going viral:
1. [Content description] - [Platform] [engagement numbers]
2. [Content description] - [Platform] [engagement numbers]
3. [Content description] - [Platform] [engagement numbers]

Trending hashtags: #tag1 #tag2 #tag3
```

**If CREATOR/HASHTAG/BRAND/GENERAL** - Show synthesis:
```
What I found:

[2-4 sentences synthesizing key insights FROM THE ACTUAL RESEARCH.]

KEY PATTERNS:
1. [Pattern from research]
2. [Pattern from research]
3. [Pattern from research]
```

**THEN - Stats:**
```
---
✅ Social research complete!
├─ 🎵 TikTok Creative: {n} trends
├─ 📊 Google Trends: {n} topics
├─ 📘 CrowdTangle: {n} posts (if used)
├─ 🌐 WebSearch: {n} pages
└─ Top platforms: TikTok, Instagram, Facebook
```

**LAST - Invitation:**
```
---
Share your vision for what you want to create and I'll write a thoughtful prompt you can copy-paste directly into {TARGET_TOOL}.
```

---

## WAIT FOR USER'S VISION

After showing stats, **STOP and wait** for the user to respond.

---

## WHEN USER SHARES THEIR VISION: Write ONE Perfect Prompt

Write a **single, highly-tailored prompt** grounded in social media research.

### Output Format:

```
Here's your prompt for {TARGET_TOOL}:

---

[The actual prompt, informed by social media trends and patterns]

---

This uses [brief 1-line explanation of what social insight you applied].
```

---

## AFTER EACH PROMPT: Stay in Expert Mode

> Want another prompt? Just tell me what you're creating next.

---

## CONTEXT MEMORY

Remember:
- **TOPIC**: {topic}
- **TARGET_TOOL**: {tool}
- **TRENDING**: {top trends and viral content}
- **SOCIAL FINDINGS**: Key insights from research

**After research, you are an EXPERT on this topic's social media landscape.**

When the user asks follow-up questions:
- **DO NOT run new WebSearches** unless about a DIFFERENT topic
- **Answer from what you learned**
- **If they ask for a prompt** - write one using your expertise

---

## Output Summary Footer

```
---
📱 Expert in: {TOPIC} social media trends
📊 Based on: {n} TikTok trends + {n} Google Trends + {n} posts + {n} web pages
🔥 Platforms: TikTok, Instagram, Facebook

Want another prompt? Just tell me what you're creating next.
```
