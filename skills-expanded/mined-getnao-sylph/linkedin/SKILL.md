# LinkedIn Post Creator

```yaml
name: linkedin-writer
description: >
  Creates LinkedIn posts across all formats - event announcements, product launches,
  thought leadership, and community engagement. Handles the full lifecycle from
  sourcing context through drafting, review, and self-improvement.
triggers:
  - linkedin post
  - LN post
  - write a post about
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| LinkedIn | Publish posts, check engagement metrics |

## When to Use

Use this skill whenever a LinkedIn post is needed:
- Sharing an article, video, or piece of content
- Announcing an event, launch, milestone, or hire
- Sharing a contrarian take or industry observation
- Community engagement (calls for help, celebrations, vulnerability posts)
- Repurposing content from other channels (blog, Substack, talks)

---

## Quick Start

Every LinkedIn post falls into one of four categories. Route to the right sub-file:

| Category | Sub-file | When |
|----------|----------|------|
| Events | `events.md` | Announcing, recapping, or clustering around events |
| Launches | `launches.md` | Product features, milestones, version releases |
| Ideas | `ideas.md` | Contrarian takes, benchmarks, article shares, thought leadership |
| Community | `community.md` | Mobilization, vulnerability, team celebrations |

Read the relevant sub-file for format-specific templates and patterns.

---

## Core Writing Principles

### Tone
- Direct and conversational, never corporate
- First person singular ("I") unless it is a team moment ("we")
- Confident but not arrogant - share what you learned, not what you know
- Short sentences. Fragments are fine.

### Opening Patterns
The first line is the post. If it does not stop the scroll, nothing else matters.

Strong openers:
- **Contrarian hook**: "Most [X] advice is wrong. Here's what actually works."
- **Specific number**: "We went from 0 to 500 users in 3 weeks. No ads."
- **Question**: "Why do analytics teams still spend 80% of their time on data prep?"
- **Confession**: "I almost shut down the company last month."
- **Bold claim**: "[Thing everyone assumes] is dead."

Weak openers (never use):
- "Excited to announce..."
- "Thrilled to share..."
- "I'm delighted to..."
- "Big news!"

### Generic Post Structure
```
[Hook - 1-2 lines that stop the scroll]

[Context - why this matters, what prompted it]

[Substance - the insight, story, data, or takeaway]

[Landing - CTA, question, or forward-looking statement]
```

Keep posts between 150-300 words. LinkedIn truncates after ~210 characters, so the hook must land before the "see more" fold.

---

## Voice Calibration

### Structural Preferences
- Use line breaks liberally - one thought per line
- Bullet points for lists of 3+ items
- No walls of text
- Emojis: sparingly, max 1-2 per post, never as bullet markers
- Hashtags: 3-5 max, at the bottom, relevant to the topic

### Punctuation Rules
- Never use em dashes (--) or en dashes (-) as punctuation. Use a hyphen (-) or colon (:) instead.
- Periods over exclamation marks. One exclamation mark per post maximum.
- No ellipsis (...) for dramatic effect

### Voice Tells to Match
- Short declarative sentences
- "Here's the thing:" as a pivot phrase
- "Turns out" to introduce a surprising finding
- Direct address to the reader ("If you're a [role]...")
- Specific numbers over vague claims

---

## Vocabulary to AVOID

These words and phrases are ghostwriter cliches. Never use them:

| Banned | Why | Use Instead |
|--------|-----|-------------|
| "banger" | Cringe | "strong post", "it performed well" |
| "game-changer" | Overused | Be specific about what changed |
| "nails it" | Vague | Explain what specifically is good |
| "had a blast" | Generic | Describe the actual experience |
| "incredibly" | Filler | Cut it or use a specific adjective |
| "leverage" | Corporate | "use" |
| "synergy" | Corporate | Describe the actual benefit |
| "ecosystem" | Overused | Be specific |
| "thought leader" | Self-aggrandizing | Never self-apply this label |
| "deep dive" | Cliche | "breakdown", "analysis", "walkthrough" |
| "unpack" | Cliche | "explain", "break down" |
| "landscape" | Vague | Name the specific market or space |
| "at the end of the day" | Filler | Cut entirely |

---

## Sourcing Context Before You Write

**Never write a post from thin air.** Always fetch the source material first.

| Source Type | How to Fetch |
|-------------|-------------|
| Article/blog post | Use `WebFetch` to get the full text |
| YouTube video | Use `WebFetch` on the video URL to get metadata; fetch transcript if available |
| GitHub repo/release | Use `gh` CLI to read release notes, README, or issue |
| Internal doc | Read the file from the repo |
| Event page | Use `WebFetch` on the event URL |
| CRM context | Use CRM tools to pull customer/deal context |

Read the source fully before drafting. Extract:
1. The single most interesting claim or data point
2. Why it matters to the target audience
3. What is non-obvious or counterintuitive about it

---

## Full Workflow

### Step 1: Understand the Request
- What is the core message?
- Who is the audience? (founders, data teams, engineers, general tech)
- What is the goal? (awareness, engagement, traffic, hiring)
- Is there source material to fetch?

### Step 2: Pick the Post Type
Route to the appropriate sub-file (events, launches, ideas, community) and select a template.

### Step 3: Draft
- Read `content/linkedin/_insights.md` for channel learnings
- Read `content/linkedin/_examples/` for high-performing references
- Write the draft following the template and voice rules
- Save to `content/linkedin/_drafts/YYYY-MM-DD_slug.md` with frontmatter:

```yaml
---
date: YYYY-MM-DD
channel: linkedin
topic: short-topic
format: post
status: draft
type: event | launch | idea | community
performance:
notes:
---
```

### Step 4: Review Checklist
Before presenting the draft, verify:

- [ ] Hook lands before the "see more" fold (~210 chars)
- [ ] No banned vocabulary
- [ ] No em dashes or en dashes
- [ ] No "Excited to announce" or similar weak openers
- [ ] Post is 150-300 words
- [ ] One clear CTA or question at the end
- [ ] 3-5 relevant hashtags
- [ ] Emojis used sparingly (0-2)
- [ ] First person voice throughout
- [ ] Specific numbers/evidence over vague claims
- [ ] Source material accurately represented
- [ ] No corporate jargon

### Step 5: Self-Improvement
When moving a post from `_drafts/` to `_published/`:

1. Scan the conversation for edits the user made
2. Diff what was drafted vs what the user kept
3. Identify patterns: What did they cut? What did they rewrite? What did they keep?
4. Add learnings to `content/linkedin/_insights.md`
5. If the post performs well later, promote it to `content/linkedin/_examples/`

---

## DO's and DON'Ts

### DO
- Start with the most interesting thing
- Use specific numbers and evidence
- Write like you talk
- Break up long blocks of text
- End with a question or clear next step
- Fetch source material before writing
- Save drafts to `_drafts/` first

### DON'T
- Start with "Excited to announce"
- Use corporate jargon or buzzwords
- Write walls of text
- Use more than 2 emojis
- Self-describe as a "thought leader"
- Write without reading `_insights.md` first
- Skip the review checklist
- Publish directly without user review

---

## Tips for Success

1. **The hook is 80% of the work.** Spend most of your time on the first two lines.
2. **One post, one idea.** If you have two ideas, write two posts.
3. **Specificity beats cleverness.** "Reduced query time from 45s to 2s" beats "Made it way faster."
4. **Read it aloud.** If it sounds like a press release, rewrite it.
5. **When in doubt, shorter.** Cut every sentence that does not earn its place.
6. **Stay close to the user's voice.** Improve, don't rewrite. Don't invent angles they didn't suggest.
