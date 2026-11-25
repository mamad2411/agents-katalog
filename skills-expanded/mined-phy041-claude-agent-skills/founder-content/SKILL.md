---
name: founder-content
description: Complete content creation and multiplication system for founders and indie hackers. Use for writing social posts, repurposing content, creating threads, build-in-public updates, or content planning. Triggers on "write a post", "create content", "repurpose this", "thread", "build in public", "ship update", "content calendar", "turn this into posts".
inputs:
  - name: idea
    type: string
    required: true
    description: The core idea, topic, or update to turn into platform-native content
  - name: target_platforms
    type: list
    required: true
    description: Platforms to generate content for (e.g. ["twitter", "linkedin", "reddit"])
  - name: source_data
    type: json
    required: false
    description: Optional structured data (repo README, stats, metrics) to enrich the content
outputs:
  - name: drafts
    type: json
    description: Dict of platform-native content drafts keyed by platform name (e.g. {"twitter": "...", "linkedin": "..."})
---

# Founder Content System

Everything for creating and multiplying content as a solo founder.

---

## Master Content Creation Workflow

**Core Principle: Research → Extract → Adapt → Write**

Every piece of content must go through this workflow.

### Step 1: Research Hot Content (REQUIRED)

Before writing ANY content, research what's working:

```
1. Search for viral/high-engagement posts on target platform
2. Find 3-5 top-performing posts on similar topic
3. Note: hook structure, format, engagement type, tone
4. Identify what makes them work (specifics, emotion, contrarian angle)
```

**Search patterns:**
- `[platform] [topic] viral`
- `site:[platform].com [topic] lessons learned`
- `[topic] founder thread high engagement`

### Step 2: Extract Winning Patterns

| What to Extract | Why |
|-----------------|-----|
| **Hook formula** | First line determines if people read |
| **Number usage** | Specifics add credibility ($400→$180) |
| **Emotion triggers** | What makes people react (cringe, saved, wasted) |
| **Story arc** | How tension and payoff are structured |
| **CTA design** | What drives comments vs likes |

### Step 3: Adapt with Your Voice

**Core Voice Principles:**
- **Authentic** — real stories, not theory
- **Sharp** — specific numbers, direct claims
- **Self-deprecating** — own failures openly
- **No fluff** — substance over motivation

**Adaptation Rules:**
1. Keep the winning hook structure
2. Replace content with YOUR real stories
3. Add specific numbers ($3,000 wasted, saved $1,000+)
4. Include genuine emotion (still cringe, learned the hard way)
5. Avoid: vague claims, motivational fluff, humblebragging

### Step 4: Platform-Specific Polish

| Platform | Key Adaptation |
|----------|---------------|
| **Twitter/X** | Punchy, <280 chars, threads for depth |
| **LinkedIn** | Longer, professional vulnerability, spaced lines |
| **Xiaohongshu** | Conversational Chinese, emotional words, 2K images |

---

## Build-in-Public Workflow

### Step 1: Gather Context

**From GitHub (auto mode):**
- Recent commits since last post
- PR titles and descriptions
- Release notes if tagged

**From user input (manual mode):**
- What shipped (feature/fix/improvement)
- Who it helps
- Why now
- One metric (optional)
- One lesson learned

### Step 2: Extract the Story

Every post answers 5 questions:
1. **What changed?** (the ship)
2. **Who benefits?** (the user)
3. **Why it matters now?** (the context)
4. **One proof** (metric, example, before/after)
5. **One takeaway** (lesson or insight)

### Step 3: Render for Each Platform

**Twitter/X:** Under 280 chars, concise, slightly spicy, one insight + one proof

**LinkedIn:** 8-20 lines with spacing, narrative + framework + takeaway

**Xiaohongshu:** Chinese-first, structure: 背景→步骤→结果→踩坑→总结

### Step 4: Quality Check

- [ ] No identical cross-posts
- [ ] Each post has a takeaway
- [ ] No banned patterns
- [ ] Metrics/proof included where possible

---

## Repurposing Framework

**Core Principle:** One Excellent Piece → 7-10 Platform-Native Derivatives

### Step 1: Evaluate Source

**High-Value (prioritize):** Evergreen topics, top performers, content with data/frameworks, long-form (>1000 words)

**Skip:** Trend-based, low performers, thin content

### Step 2: Extract Atomic Units

| Element | What to Extract |
|---------|----------------|
| Hook | Opening line, attention-grabber |
| Stats | Numbers, percentages, metrics |
| Frameworks | Step processes, models |
| Quotes | Memorable phrases |
| Stories | Anecdotes, case studies |
| Takeaways | Key lessons, actionable tips |

### Step 3: Apply STEPPS (from Contagious)

Every derivative needs at least one:
1. **Social Currency** — Makes sharer look smart
2. **Triggers** — Connected to daily habits
3. **Emotion** — Evokes awe, surprise, anger
4. **Public** — Visible behavior
5. **Practical Value** — Useful, saves time/money
6. **Stories** — Narrative that carries message

### Step 4: Distribution Schedule

```
Day 0: Original published
Day 1-2: Tease/announcement
Day 3-7: First wave derivatives
Week 2-3: Second wave
Week 4+: Evergreen rotation
```

---

## Content Pillars

Good pillars for a founder/builder:

1. **Your Tech/Product** — What you're building, how it works
2. **Building in Public** — Process > results, real learnings, metrics
3. **Founder Perspective** — Unique angle (background, market, journey)
4. **Systems Thinking** — Workflows, optimization, productivity

**Weekly mix:** 2-3 posts from pillars 1-2, 1 post from pillars 3-4

---

## Voice Rules

**Always:**
- Include one takeaway per post
- Adapt content per platform
- Use metrics when available

**Never:**
- Motivational fluff ("believe in yourself")
- Humblebragging / name-dropping
- Vague claims ("game-changing", "revolutionary")
- Thought-leader cringe
- Dunking on competitors by name

**Voice Summary:**
- Authentic (not performative)
- Direct, earned confidence
- Self-deprecating humor
- Specific details
- No inspirational soup

---

## Thread Formula

```
Tweet 1 (Hook): Surprising stat or contrarian take
Tweet 2-5: One key point per tweet with proof
Tweet 6: Common mistake / "what most get wrong"
Tweet 7: The solution/framework
Tweet 8: CTA + callback to original
```

Write **10-15 versions of hook** before publishing.

---

## Example Transformation

**Input (GitHub commit):**
```
feat: connect MCP to content scheduler
- Added automatic content storage
- Triggers on GitHub push
- Posts to 3 platforms
```

**Output:**

**Twitter/X:**
> Just wired up Claude → DB → auto-posting pipeline.
> GitHub push now triggers content across 3 platforms.
> Surprising part: 80% of the work was tone adaptation, not infra.

**LinkedIn:**
> Shipped: automated "build in public" pipeline
>
> What it does: GitHub commits → AI-adapted posts → 3 platforms
>
> What I learned: The hard part isn't automation—it's maintaining authentic voice at scale.

**Xiaohongshu:**
> 标题：用 Claude + MCP 搭了个自动发帖系统
>
> 背景：每次提交都想分享，但手动发三个平台太累
>
> 做法：Claude 读 commit → 生成三版本 → 自动发
>
> 踩坑：以为难点是技术，其实是语气适配
>
> 总结：自动化不是复制粘贴，是让机器学会"变脸"

---

## Platform Defaults

| Platform | Language | Cadence | Format |
|----------|----------|---------|--------|
| Twitter/X | English | 3-5/week | <280 chars, threads rare |
| LinkedIn | English | 1-2/week | 8-20 lines, spaced |
| Xiaohongshu | Chinese + EN tools | 2/week | 干货 + 踩坑 mix |
