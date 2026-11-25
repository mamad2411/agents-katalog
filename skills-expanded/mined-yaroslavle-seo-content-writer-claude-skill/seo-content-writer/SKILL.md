---
name: seo-content-writer
description: >
  Full AI-assisted workflow for long-form SEO content (2,000+ words). Covers JTBD strategy, E-E-A-T quality standards,
  and 5 production phases: research, outline, draft, editing, and SEO/publishing. Built for B2B marketing agency context.
  Use when: user wants to write or optimize an SEO article, mentions "SEO content", "blog post", "GTM article",
  "long-form content", or asks to create content with keyword strategy.
---

*Based on O-CMO Blog Writing & AI Copywriting Framework*

---

## OVERVIEW

This skill guides Claude through a complete AI-assisted workflow for creating long-form SEO content (2,000+ words). It integrates prompt engineering frameworks, E-E-A-T quality standards, JTBD-based content strategy, and the O-CMO brand writing framework.

**Core philosophy:**
- Every article starts with a Job-to-Be-Done (JTBD) — not a keyword
- People-first content that demonstrates first-hand experience and expertise
- Treat AI like a smart intern: smaller content units → more control → better quality
- Build iteratively: concept → outline → section → full article

---

## PHASE 0: STRATEGY FOUNDATION

### 0.1 — Define the JTBD Before Anything Else

Every article — new or optimized — starts with a Job-to-Be-Done statement:

> "When [situation], I want to [motivation], so I can [desired outcome]."

**Legend:**
- **When [situation]** = the context the reader is in → *"When I'm comparing vendors…"*
- **I want to [motivation]** = what they're looking for → *"…I want to understand how each one delivers…"*
- **So I can [desired outcome]** = the real reason behind the search → *"…so I can avoid delays and explain my choice to the team."*

**Examples:**
- When I realize our current marketing automation platform isn't working anymore, I want to understand what's involved in switching tools, so I can avoid data loss, downtime, and adoption issues.
- When we're planning the next lifecycle marketing phase, I want to evaluate whether gamification would improve retention, so I can present a clear case to the growth team.

**Rule:** One JTBD per article. Don't try to serve every ICP in one piece.

---

### 0.2 — E-E-A-T Alignment Check

Before writing, confirm the content plan passes Google's E-E-A-T framework (Experience, Expertise, Authoritativeness, Trustworthiness):

| Dimension | What to include |
|-----------|----------------|
| **Experience** | First-hand observations, real project examples, personal usage insights |
| **Expertise** | Author credentials, technical depth, evidence of knowledge |
| **Authoritativeness** | Bylines, author bios, links to authoritative sources |
| **Trustworthiness** | Fact-checked claims, cited sources, no outdated info (max 5 years old) |

**The three Google questions to ask about every article:**
- **Who** created it? → Is authorship clear? Does it have a byline?
- **How** was it created? → Is the process transparent (including AI use)?
- **Why** was it created? → Is it primarily for readers, not for search rankings?

**Content quality self-check:**
- Does it provide original information, reporting, or analysis?
- Does it go beyond the obvious?
- Would you bookmark, share, or recommend this?
- Does it leave the reader feeling they've learned enough to act?
- Is every major claim supported by a primary source?

---

### 0.3 — Prompt Engineering Setup

Choose the right framework for each task:

| Task | Framework | Purpose |
|------|-----------|---------|
| Research & analysis | **R.I.S.E.N.** | Facts, sources, pain points, narratives |
| Writing content | **C.R.E.A.T.E.** | Tone, audience, structure |
| Setting up any AI task | **C.O.R.E.** | Goal, limits, end use |
| Improving tone & specificity | **C.O.A.S.T.** | Context, audience, style |

**C.O.A.S.T.** — For all prompts
- **C** – Context: what you're doing and for whom
- **O** – Objective: exactly what you want
- **A** – Audience: who will read it
- **S** – Style / Voice: tone, paste voice guardrails
- **T** – Task details: word count, structure, required data

**C.O.R.E.** — AI task setup
- **C** – Context; **O** – Objective; **R** – Requirements; **E** – End use

**C.R.E.A.T.E.** — Content generation
- **C** – Command; **R** – Role (e.g., "expert SaaS copywriter"); **E** – Examples; **A** – Audience; **T** – Tone; **E** – Extras (word count, CTA style)

**R.I.S.E.N.** — Research
- **R** – Relevant data; **I** – Interesting/contrarian viewpoints; **S** – Sources; **E** – Engagement triggers; **N** – Narratives/emerging trends

**Prompt structure rules:**
- Use XML tags or `##` headings to separate sections of long prompts
- Use `[PLACEHOLDER]` in CAPS for reusable variables
- One minimum content unit per prompt — never ask for the full article at once
- Ask for 3 options before committing: concept → approve → expand
- Use "step by step" when AI reasoning is unclear
- One example → AI copies structure. Three+ examples → AI extracts patterns

---

## PHASE 1: RESEARCH & STRATEGY (30 min)

### Step 1.1 — Voice DNA Extraction (one-time setup)

Upload 3–5 of your best articles and prompt:

```
Analyze these writing samples and create my "Voice DNA":
1. Tone descriptors (8–10 specific adjectives)
2. Sentence structure patterns (average length, variety)
3. Vocabulary level and word choices
4. Paragraph rhythm and flow
5. Common transitional phrases
6. How I handle examples and analogies
7. My approach to hooks and conclusions
Output a detailed style guide I can paste into every future prompt.
```

### Step 1.2 — Voice Guardrails Template (save and reuse)

```
VOICE GUARDRAILS

DO:
- [Your tone requirements]
- [Sentence structure preferences]
- [Vocabulary style]

DON'T:
- [Words/phrases to avoid: "just", "delve", "enhance", "game-changing"]
- [Structural patterns to avoid: em-dash overuse, passive voice, generic corporate openers]
- [Formatting to avoid: lists of "Bold term: description" pairs — very AI-looking]

DO NOT START WITH:
- Proverbs, sayings, or "everyone knows that…"
- Generalizations: "every marketer has…", "all founders…"
- Direct questions to the reader: "Have you ever noticed…"
- Quotes from classics or famous people

VOICE EXAMPLES:
Instead of: "[Bad example]"
Write: "[Good example]"
```

**Session warm-up prompt:**
```
Before writing, review my voice guardrails: [paste guardrails]
After writing, self-check:
1. Does this sound like me?
2. Are sentence lengths varied and consistent with my style?
3. Have I avoided my "don't" list?
If not, revise before showing me output.
```

---

### Step 1.3 — Topic Research (5 min) — Perplexity

```
Research [TOPIC] and provide:
1. 5 recent statistics or data points (2024–2025)
2. 3 trending subtopics people are currently discussing
3. 2 contrarian or surprising viewpoints
4. Top pain points your audience faces with this topic
5. 3 credible sources for each point
Format as: Fact | Source | Why it matters
```

**Warning:** Always verify sources manually. AI often references outdated or renamed products.

### Step 1.4 — Competitive Analysis (5 min) — ChatGPT

```
Find 5 popular articles about [TOPIC] published in the last 6 months.
For each article, analyze:
- Main angle/approach taken
- Key points covered
- What's missing or could be improved
- Word count and structure
- Engagement elements (hooks, examples, CTAs)
I want to create something better and more comprehensive.
```

### Step 1.5 — GSC Integration (for optimization tasks)

When optimizing an existing article:
1. Open Google Search Console → Performance → Search results
2. Filter by the live URL
3. Check Search Queries for: what's already ranking, what gets impressions without clicks, what's missing

Use findings to:
- **Prioritize** queries already getting impressions
- **Integrate** them naturally into subheadings and intro text
- **Fill gaps** by adding sections that address uncovered queries
- **Improve relevance** by matching the intent (informational, comparative, how-to)

### Step 1.6 — Audience Research (5 min)

```
I'm writing about [TOPIC] for [TARGET AUDIENCE].
Create a detailed reader profile:
- Current knowledge level about this topic
- Biggest frustrations/pain points
- Questions they ask but can't find answers to
- Preferred language/tone style
- What would make them share this content
```

### Step 1.7 — Angle Selection (5 min)

```
Based on this research: [PASTE ALL RESEARCH]
Generate 10 unique angles for a [WORD COUNT]-word article about [TOPIC]:
1. The contrarian take
2. The data-driven approach
3. The case study method
4. The step-by-step guide
5. The trend analysis
6. The beginner's deep-dive
7. The expert interview
8. The problem-solution format
9. The myth-busting approach
10. The future prediction
For each angle, write a compelling one-sentence hook.
```

### Step 1.8 — Research Master Brief

```
Organize all research into a master brief:
CHOSEN ANGLE: [Selected above]
JTBD: [Your JTBD statement]
KEY STATISTICS: [Top 3–5 data points]
CONTRARIAN ELEMENTS: [Surprising viewpoints]
AUDIENCE PAIN POINTS: [Top 3 problems to address]
COMPETITIVE GAPS: [What others missed]
CREDIBLE SOURCES: [All sources organized by section]
```

---

## PHASE 2: STRATEGIC OUTLINE (30 min)

### Step 2.1 — Master Outline

```
Create a detailed outline for a [WORD COUNT]-word article.
TOPIC: [Topic]
JTBD: [Your JTBD statement]
ANGLE: [Chosen angle]
TARGET AUDIENCE: [Audience]
RESEARCH BRIEF: [Paste master brief]

STRUCTURE:

HOOK (150 words)
- Opening: [specific statistic or unexpected fact]
- Context: why this matters now
- Promise: what readers will gain
- Transition to introduction

INTRODUCTION (300 words)
- Problem statement (audience pain point matching the JTBD)
- Your unique angle
- Article roadmap
- Transition to Section 1

SECTION 1: [Title] (500 words)
- Core argument
- Supporting evidence [which research to use]
- Concrete example or case study (from real experience, anonymized if needed)
- Reader application
- Transition

[Repeat for Sections 2–4]

CONCLUSION (150 words)
- Synthesize key insights (elevate, don't repeat)
- Why this matters for the reader
- One immediate action step
- Forward-looking close

FOR EACH SECTION SPECIFY:
- Exact talking points (3–4 bullets)
- Which research/data to include
- Type of example needed (client case, quote, testimonial, internal framework)
- Suggested subheadings
```

**Word count guidance:** Check Ahrefs for competitor article length — never rely on AI word count estimates.

### Step 2.2 — Outline Optimization

```
Review this outline and optimize:
1. Logical flow — does argument build properly?
2. Word distribution across sections
3. Content variety — no two sections with the same structure
4. Hook delivery — does the opening earn the reader's time?
5. Evidence balance — every claim has support

Provide: 3 specific improvements + rewrite any weak sections.
```

---

## PHASE 3: SECTION-BY-SECTION DRAFT (60 min)

**Golden rule:** One section at a time. The smaller the content unit, the more control you have.

### Step 3.1 — Hook + Introduction (15 min)

```
Write the hook and introduction (~450 words).
OUTLINE: [Paste hook + intro]
JTBD: [Your JTBD statement — the reader should recognize their situation from line one]
RESEARCH TO USE: [Paste relevant data]
VOICE GUARDRAILS: [Paste guardrails]

REQUIREMENTS:
- Start with the compelling statistic/unexpected fact
- Establish why this matters to this specific reader
- Include brief preview of what they'll learn
- Include target keyword in first or second paragraph
- End with smooth transition to Section 1
- Paragraphs max 3–4 sentences
- No proverbs, no "everyone knows", no direct questions to the reader
```

### Step 3.2 — Main Sections (10 min each)

```
Write Section [N]: [TITLE] ([WORD COUNT] words)
OUTLINE: [Paste section details]
RESEARCH TO INCLUDE: [Paste relevant data/examples]
VOICE GUARDRAILS: [Paste]

STRUCTURE:
1. Opening hook connecting to previous section
2. Main argument with supporting evidence
3. Concrete example — prioritize: client case (anonymized), quote from interview, internal framework, credible external data
4. Practical application for readers
5. Smooth transition to next section

FORMATTING:
- Short paragraphs (3–4 sentences max)
- Use bullet points for lists of 3+ items
- Bold key concepts when it adds emphasis — don't overuse
- Use subheadings if section exceeds ~300 words
- Sentence case for H3 subheadings
- [WORD COUNT] words exactly
```

### Step 3.3 — Conclusion (5 min)

```
Write conclusion ([WORD COUNT] words).
KEY INSIGHTS TO SYNTHESIZE: [List]
VOICE GUARDRAILS: [Paste]
CTA DIRECTION: [What do you want readers to do next?]

STRUCTURE:
1. Synthesize (don't repeat — elevate the insight)
2. Reinforce why it matters for this reader
3. One specific immediate action
4. Forward-looking close
```

### Step 3.4 — Section Transitions

```
I need a smooth transition between these sections.
FROM: [Section N title — last sentence]
TO: [Section N+1 title — first idea]
TONE: [your tone]

Provide 3 options:
1. Question transition
2. Summary-to-preview bridge
3. Problem-to-solution transition
```

### Emergency Fixes

**Stuck on a section:**
```
I'm struggling with [SECTION]. Outline says: [paste]
Give me 3 approaches:
1. Story-led: start with a narrative or case study
2. Data-heavy: lead with statistics
3. Step-by-step: break into numbered actions
Write opening paragraph for each so I can choose.
```

**Word count off:**
```
Section is [too long / too short]. Current: [N] words. Target: [N].
[If too long]: Cut to exactly [N] while keeping all key points.
[If too short]: Expand to [N] by adding [examples / data / reader application].
[PASTE SECTION]
```

---

## PHASE 4: EDITING (60 min)

**Priority order:** Repetition → Logic flow → Tone → SEO technical

### Layer 1 — Content & Structure (15 min)

```
Review first draft for structural issues.
ANALYZE:
1. Repetitive content across sections (biggest AI problem — check first)
2. Logical flow — does argument build from general to specific?
3. Content gaps vs the outline
4. Pacing — where does engagement drop?
5. Transitions — are they smooth?
Provide specific fixes for each issue.
[PASTE DRAFT]
```

### Layer 2 — Fact-Checking & Credibility (15 min)

```
Fact-check this article.
FLAG:
1. Statistics (with suggested verification method)
2. Claims that need sourcing
3. Dates and versions
4. Technical terms
5. Attribution issues
For each: flag it + suggest primary source to verify.
[PASTE ARTICLE]
```

**Manual checks required:**
- All sources ≤5 years old
- No competitor blogs, statistics compilations, or unauthored posts as sources
- No renamed/outdated tools cited

### Layer 3 — Readability (15 min)

```
Optimize for readability.
FIX:
1. Long sentences → rewrite as shorter
2. Dense paragraphs → break up (max 3–4 sentences)
3. Weak transitions
4. Missing subheadings in long sections
5. Passive voice
Provide specific edits.
[PASTE ARTICLE]
```

### Layer 4 — Voice Consistency (15 min)

```
Final polish for voice consistency.
VOICE GUARDRAILS: [Paste]

CHECK:
1. Tone consistency across all sections
2. Sentence structure matches style
3. Vocabulary level appropriate throughout
4. Bold/emphasis used sparingly and meaningfully
5. No Corporate Memphis content: no generic stock-image descriptions, no "innovative solutions", no "holistic approach"

ENGAGEMENT:
1. Weak openings in any section
2. Concepts that need an analogy
3. Claims missing examples
[PASTE ARTICLE]
```

### Layer 5 — Humanize (when needed)

```
Make this AI-written section feel more human.
TEXT: [Paste section]
AUDIENCE: [Target audience]
TONE: [Your tone]

1. Identify what feels generic, cliché, or flat
2. For each: explain why + suggest improvement
3. Identify one sentence that needs a metaphor or analogy
4. Output a humanizing checklist (5 items)
5. Suggest 3 voice techniques to apply
```

**Manual catch list:**
- Em-dash overuse → replace with colon, comma, or period
- "Bold term: description" list pattern → rewrite as prose or varied bullets
- Phrases to remove: "just", "delve", "enhance", "leverage", "game-changing", "innovative", "seamless", "holistic"
- Repetition between sections → cut or reframe
- Passive voice → find subject and make it active

---

## PHASE 5: SEO & PUBLISHING

### Headline Generation

Use these formula categories based on content angle (from Chris Garrett's 102 Formulas):

**Get What You Want (value/benefit angle):**
- "How to Get [RESULT] in Half the Time"
- "5 Ways to Boost Your [METRIC] Without Spending More [RESOURCE]"
- "Who Else Wants to [ACHIEVE GOAL]?"

**Problems & Fears (pain-point angle):**
- "Get Rid of Your [PROBLEM] Once and For All"
- "[TOPIC] Do's and Don'ts"
- "What Your [SOURCE] Is Not Telling You About [TOPIC]"

**Fact, Fiction, Secrets (insight/authority angle):**
- "What Everyone Ought to Know about [TOPIC]"
- "The Real Truth About [TOPIC]"
- "21 Secrets the [NICHE] Experts Don't Want You to Know"
- "Little Known Ways to [ACHIEVE GOAL]"

**How-To (step-by-step angle):**
- "How to [ACTION] Like a [ROLE MODEL]"
- "Here Is a Method That Is Helping [AUDIENCE] to [RESULT]"
- "[TOPIC] Like an Expert in 10 Easy Steps"

**Crystal Ball (trends/future angle):**
- "How [TOPIC] Will Impact [INDUSTRY] in [YEAR]"
- "The Modern Rules of [TOPIC]"
- "40 Predictions on the Future of [TOPIC]"

**Title generation prompt:**
```
Generate 20 title options for a blog post about "[TOPIC]" for "[AUDIENCE]".
PRIMARY KEYWORD: [keyword]
CONTENT ANGLE: [how-to / listicle / case study / opinion]

Categories:
- Curiosity-driven (5)
- Benefit-focused (5)
- Problem-solution (5)
- Authority/credibility (5)

Requirements:
- 60–100 characters (for SEO title) or 50–60 for H1
- Include primary keyword naturally
- Title Case (AP style)
- No clickbait
- For each: title + why it works + SEO strength (1–10)
```

**Check with:** capitalizemytitle.com (AP style) + highervisibility.com SERP snippet optimizer

---

### Meta Title & Description

```
Write meta title and meta description.
ARTICLE TITLE: [Your H1]
PRIMARY KEYWORD: [keyword]
ARTICLE SUMMARY: [2 sentences]

REQUIREMENTS:
- Meta title: 60–100 characters, keyword included
- Meta description: up to 160 characters, 1–2 keywords, creates curiosity or urgency

Deliver 3 options per field.
```

---

### Keyword Placement

```
Place these keywords in the article.
PRIMARY: [keyword] → H1, first 100 words after H1, H2 twice max (1–2 total uses)
SECONDARY: [keywords] → body text, subheadings where natural

Rules:
- Show me exact placement with surrounding sentence
- Highlight integrated keywords in [BRACKETS] for review
- List any keywords not integrated + reason why
- No keyword stuffing — max 1–2 primary uses per 500 words
```

---

### CTA Strategy

```
Plan CTAs for this article.
ARTICLE: [Paste]
PRIMARY CTA: [email signup / product page / case study / demo]
FUNNEL STAGE: [awareness / consideration / decision]

Identify:
- 3 high-impact CTA locations (with surrounding text quote)
- Reader mindset at each location
- CTA copy + lead-in sentence for each
- 2–3 micro-CTAs within the content

Rules:
- CTAs must be a bridge between what was said before and the next idea
- They work best after proof points (cases, quotes, data)
- End of article: CTA banner/snippet with 2 short phrases + button text (required)
- Cross-reference related articles with "Read more: [Full Article Title]" anchor links
```

---

### Visuals Brief

```
Plan visuals for this article.
ARTICLE: [Paste]

For each visual, specify:
- Visual type: infographic / chart / table / screenshot / custom illustration
- Placement (after which paragraph/subheading)
- Purpose (what concept it illustrates)
- Description for designer (what it should show)
- Alt text (include keyword where natural)

Rules:
- No generic Corporate Memphis stock images
- Prefer: infographics, charts, data tables, UI screenshots with source link
- Images must add informative value, not decor
- Compress to max 200KB before publishing
```

---

### Convert to Newsletter

```
Convert this blog post into an email newsletter.
BLOG TITLE: [title]
AUDIENCE: [email segment]
PRIMARY CTA: [link + CTA text]
TONE: [conversational / professional]
BLOG CONTENT: [paste or summarize]

Deliver:
- 3 subject line options
- Intro paragraph (hook-driven, 3–4 sentences)
- 2–3 key takeaways
- CTA with button copy
- Optional PS line
```

---

## APPENDIX A: WRITER'S CHECKLIST

Pre-publish verification:

**Content:**
- [ ] JTBD is clear — reader recognizes their situation from line one
- [ ] Every major claim has a primary source (no aggregators, no >5-year-old sources)
- [ ] Article provides unique insight, not just a summary of what others say
- [ ] Examples present: client case / quote / internal framework / verified data
- [ ] No repetition between sections
- [ ] Logical flow: general → specific or problem → solution

**Formatting:**
- [ ] H1 = file name; H1 and H2 in Title Case (AP style); H3 in sentence case
- [ ] No H4 or deeper headings
- [ ] Paragraphs max 3–4 sentences
- [ ] Short paragraphs, bullet points used for lists of 3+ items
- [ ] Bold used for emphasis, not decoration

**SEO:**
- [ ] Target keyword in H1, first 100 words, H2 twice
- [ ] All keywords highlighted and reviewed
- [ ] Meta title: 60–100 characters with keyword
- [ ] Meta description: up to 160 characters with 1–2 keywords
- [ ] Internal links to related articles (anchor text or "Read more: [title]")
- [ ] CTA banner/snippet at end of article

**E-E-A-T signals:**
- [ ] Byline / author attribution visible
- [ ] Sources cited and linked (primary sources only)
- [ ] American English, proofread manually + Grammarly
- [ ] Images have alt-text with keyword, compressed to max 200KB

---

## APPENDIX B: HEADLINE FORMULA REFERENCE

**102 fill-in-the-blank headline templates** (use as a trigger for AI generation):

*Benefits:* "How to Get [RESULT] in Half the Time" | "5 Ways to [DO X] and Profit" | "Who Else Wants to [GOAL]?"

*Problems:* "[TOPIC] Do's and Don'ts" | "Get Rid of [PROBLEM] Once and For All" | "What [SOURCE] Is Not Telling You About [TOPIC]"

*Secrets:* "What Everyone Ought to Know About [TOPIC]" | "The Real Truth About [TOPIC]" | "Little Known Ways to [DO X]"

*How-To:* "How to [ACTION] Like a [EXPERT]" | "[TOPIC] Like an Expert in 10 Easy Steps" | "Here's a Quick Way to [DO X]"

*Trends:* "How [X] Will Impact [INDUSTRY] in [YEAR]" | "The Modern Rules of [TOPIC]"

*Best/Worst:* "5 Reasons [X] Is Better Than [Y]" | "The World's Worst [TOPIC] Advice"

---

## APPENDIX C: TOOLS STACK

| Task | Tool |
|------|------|
| Real-time research | Perplexity Pro |
| Competitive analysis | ChatGPT, Ahrefs |
| Writing & editing | Claude |
| Keyword research | Ahrefs, SEMrush |
| Word count benchmark | Ahrefs Chrome Extension → Content tab |
| Title check | capitalizemytitle.com |
| SERP snippet preview | highervisibility.com |
| Grammar | Grammarly |
| Synonyms | Powerthesaurus.org, OZDIC.com |
| Image compression | imagecompressor.com, tinypng.com |

---

## APPENDIX D: QUICK DIAGNOSTIC

| Problem | Fix |
|---------|-----|
| Repetitive content | Layer 1 edit: check non-repetition first |
| Broken logic | Check: does A lead to B, does B lead to C? |
| Generic AI tone | Layer 5 humanize + voice guardrails |
| Wrong word count | Set exact targets per section in every prompt |
| Keyword stuffing | Add keywords in a separate, dedicated prompt |
| Outdated sources | Manual verification always required |
| Em-dash overuse | Add to guardrails "DON'T" list |
| Missing examples | Prompt: add client case / quote / internal framework |
| Weak hook | Rewrite: start with statistic, unexpected fact, or concrete scenario |
| CTA not converting | Place after proof point (case, quote, data), not randomly |

---

*SEO Content Writer Skill v3.0 — O-CMO project*
*Sources: O-CMO Blog Writing & AI Copywriting Framework · E-E-A-T Guidelines (Google) · Creating Helpful Content (Google Search Central) · 102 Headline Formulas (Chris Garrett)*
