---
name: content-create
description: "This skill should be invoked when the user wants to write or draft new marketing content assets including social posts, ads, emails, email sequences, newsletters, blog posts, case studies, video scripts, carousels, threads, cold emails, or launch announcements. Triggers include 'write me a post', 'I need content for...', 'draft content', 'I need to announce something', 'I don't know what to say', or 'what should I write about' -- even if they just name a platform like 'LinkedIn', 'Twitter', 'Instagram', or 'TikTok' or a format like 'carousel' or 'reel.' For craft-quality headlines, hooks, CTAs, or full-page section-by-section copy, defer to copywriting. Not for editing or fixing existing text (use humanize), auditing a live landing page (use lp-optimization), diagnosing why existing content underperforms (use seo or attribution), or technical documentation (use technical-writer)."
argument-hint: "[angle or topic]"
license: MIT
metadata:
  author: hungv47
  version: "3.0.0"
---

# Content Creation

*Communicate Track — Step 3 of 4. Turns IMC angles into production-ready content assets with A/B variants.*

**Core Question:** "Would the target persona actually stop scrolling for this?"

## Philosophy

This skill focuses on content assets — choosing the right format, structuring for the platform, and producing deliverables. For copy craft (variation workflows, evaluation rubrics, annotation), use `copywriting`.

## Inputs Required
- Angle + channel from `.agents/mkt/imc-plan.md` (or user-provided)

## Output
- `.agents/mkt/content/[slug].md`

## Quality Gate
Before delivering, verify:
- [ ] Hook communicable concisely — ≤8 words is a strong target; if longer, every extra word must earn its place by adding specificity or surprise
- [ ] Key lines pass `copywriting` skill's quality gate (3Q test, rubric ≥3.5, swap test, variations, annotations)
- [ ] CTA follows formula: [action verb] + [what they get] (not "Learn More" or "Click Here")
- [ ] A/B variant changes exactly ONE element — and hypothesis states the learning if B wins

## Chain Position
Previous: `imc-plan` | Next: `attribution`
**Re-run triggers:** When IMC plan angles are updated, when targeting a new platform, or when A/B test results suggest a new direction.

### Skill Deference
- **Need craft-quality headlines, hooks, or page copy?** → Run `copywriting` for variation workflow, 3Q test, and evaluation rubric.
- **Page already exists and problem is conversion?** → Run `lp-optimization` first — it diagnoses conversion blockers before rewriting.
- **Content reads as AI-generated?** → Run `humanize` after this skill — it strips AI patterns and compresses.
- **Angle already defined in IMC plan?** → Use it directly — don't re-derive. This skill refines hooks within an angle, not replaces the angle.
- **Optimizing for search/AI citations?** → Coordinate with `seo` for keyword targeting, schema markup, and content structure.

---

## Before Starting

### Step 0: Product Context
Check for `.agents/product-context.md`. If available, read for product details and accuracy.
If `.agents/mkt/imc-plan.md` or `.agents/product-context.md` `date` fields are older than 30 days, recommend re-running upstream skills before proceeding — stale data produces misaligned content.

### Required Artifacts
| Artifact | Source | If Missing |
|----------|--------|------------|
| `imc-plan.md` | imc-plan | **INTERVIEW.** Gather: angle, channel, placement, awareness stage. |

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `icp-research.md` | icp-research | VoC language for copy |
| `product-context.md` | icp-research | Product details for accuracy |

Read `.agents/mkt/imc-plan.md` if it exists — pull angle, hook type, awareness stage, channel. If it doesn't exist, interview for:
1. Target angle for this content piece
2. Channel and placement
3. Audience awareness stage

Use WebSearch to verify current platform specs before writing — specs change frequently and outdated dimensions waste production time: `"[platform] [format] specs [year]"` (e.g., "LinkedIn carousel specs 2026"). See [references/platform-specs.md](references/platform-specs.md) for baseline reference.

---

## Step 1: Write the Hook

The hook stops the scroll. Write the exact text.

| Hook Type | Pattern | Example |
|-----------|---------|---------|
| Question | "Have you ever [relatable]?" | "Have you ever spent more time reporting than doing?" |
| Bold claim | "[Controversial statement]" | "Your meetings problem isn't meetings." |
| How-to | "How to [outcome] without [sacrifice]" | "How to ship 2x faster without hiring" |
| Story | "I [action] and [surprise]" | "I cut meetings 80%. Output doubled." |
| Data | "[Surprising stat]" | "31 hours/month in unproductive meetings" |
| Contrarian | "Stop [common advice]" | "Stop tracking velocity." |

Apply `copywriting`'s Variation Workflow and Three-Question Test to the hook. Write 3-5 variations, score with the evaluation rubric, and annotate the winner.

---

## Step 2: Write the Body

Write the ACTUAL copy — not an outline, not a description.

**Video:** Timestamped script with text-on-screen, voiceover, and visual direction.
**Static post:** Complete caption, every word.
**Carousel:** Every slide, cover to CTA.
**Thread:** Every post, numbered.
**Full-page copy** (landing pages, homepages): Run `copywriting` for section-by-section organization with alternatives and annotations.
**Email** (drip campaigns, onboarding sequences, lifecycle emails): Subject line (≤50 chars, A/B variants) + preview text (≤90 chars) + body (one CTA per email, PAS or story framework) + CTA button text + P.S. line (optional — high-read section). For sequences, include send timing and trigger conditions between emails.

---

## Step 3: Write the CTA

| Stage | Pattern | Example |
|-------|---------|---------|
| Unaware | Discover | "See why this matters →" |
| Problem Aware | Explore | "Discover the fix →" |
| Solution Aware | Compare | "See how we're different →" |
| Product Aware | Try | "Start free trial →" |
| Most Aware | Act | "Start now — first month free →" |

Starting vocabulary, not a prescription. Match CTA energy to audience readiness, not just the awareness stage label. A Most Aware audience may respond better to a softer CTA if trust is already established.

Include: exact CTA text, destination, tracking parameters.

---

## Step 4: A/B Variant

Create variant B that changes exactly ONE element:

| What to Test | When | What You Learn if B Wins |
|-------------|------|------------------------|
| Hook | Default — always test the hook first | Audience responds more to [B's approach] than [A's] |
| CTA | Hook is strong, conversion is weak | [B's framing] reduces friction better |
| Format | Engagement is low despite good hook | Audience prefers [B's format] on this platform |
| Angle framing | Testing different emotional entry points | [B's emotion] resonates more than [A's] |

---

## Step 5: VoC Validation Check

Before finalizing, verify the content echoes actual audience language:
- [ ] Hook uses words/phrases from VoC quotes in ICP research (not marketing-speak)
- [ ] Pain expressions match how the audience actually describes the problem
- [ ] Emotional triggers are grounded in ICP emotional drivers (not assumed)

If `.agents/mkt/icp-research.md` exists, pull 2-3 VoC quotes and check: does this content sound like something the persona would share, or something a marketer would write? The gap between these two is where content underperforms.

---

## Step 6: Asset Checklist

What the production team needs. Be specific about dimensions, formats, and brand assets. For copy polish, apply `copywriting`'s Seven Sweeps or `humanize` for AI pattern removal.

---

## Artifact Template

```markdown
---
skill: content-create
version: 1
date: [today's date]
status: draft
---

# Content: [Title]

**Date:** [today]
**Skill:** content-create
**Angle:** [from IMC plan]
**Channel:** [platform + placement]
**Stage:** [awareness level]

## Hook

[Exact hook text]

**3Q Test:** Visual: [Y/N] | Falsifiable: [Y/N] | Uniquely ours: [Y/N]
**Annotations:** [Rule that drove hook choice, cut alternative, rubric score — see copywriting skill]

## Body

[Complete copy — every word, slide, or timestamp]

## CTA

- **Text:** [exact CTA copy]
- **Destination:** [URL or action]
- **Tracking:** [UTM parameters]

## A/B Variant

| Element | A (Main) | B (Variant) |
|---------|----------|-------------|
| [Hook/CTA/Format] | [Original] | [One change] |

**Test hypothesis:** If B wins, it means [specific learning about the audience].

## Asset Checklist

- [ ] [Asset with specs]
- [ ] [Asset with specs]
- [ ] [Brand assets needed]

> On re-run: rename existing artifact to `[slug].v[N].md` and create new with incremented version.
```

---

## Worked Example

```markdown
# Content: Status Update Waste — LinkedIn Carousel

**Date:** 2026-03-13
**Skill:** content-create
**Angle:** "Engineering teams lose 12 hrs/week to status updates nobody reads"
**Channel:** LinkedIn carousel, @brand
**Stage:** Problem Aware

## Hook

"Your team loses 12 hours a week to status updates nobody reads."

**3Q Test:** Visual: Y (12 hours, status updates) | Falsifiable: Y (12 is a specific, checkable number) | Uniquely ours: Y (cites our research data)

## Body

- Slide 1: "Your team loses 12 hours a week to status updates nobody reads."
- Slide 2: "Here's where those hours go:" [pie chart visual]
- Slide 3: "4 hrs — writing updates for managers who skim them"
- Slide 4: "3 hrs — standups where 8 people wait to give 30-second updates"
- Slide 5: "3 hrs — switching between tools to piece together who's doing what"
- Slide 6: "2 hrs — 'quick syncs' that could have been a dashboard"
- Slide 7: "The fix isn't better updates. It's fewer updates with better visibility."
- Slide 8: CTA slide

## CTA

- **Text:** "See how teams ship without status theater →"
- **Destination:** /product/visibility
- **Tracking:** utm_source=linkedin&utm_medium=organic&utm_campaign=status-waste&utm_content=carousel-v1

## A/B Variant

| Element | A (Main) | B (Variant) |
|---------|----------|-------------|
| Hook | "Your team loses 12 hrs/week..." (Data) | "I stopped doing standups. Here's what happened." (Story) |

**Test hypothesis:** If B wins, our audience responds more to personal narrative than statistics on LinkedIn.

## Asset Checklist

- [ ] 8 slides, 1080×1350px (LinkedIn carousel format)
- [ ] Slide 2: pie chart showing hour breakdown
- [ ] Brand fonts + colors applied to all slides
- [ ] Logo on slides 1 and 8
```

---

## Anti-Patterns

**Burying the lead** — Starting with context or background instead of the hook. The first line must stop the scroll — everything before the hook is wasted because nobody reads past a weak opening.

**Platform-generic content** — Writing the same way for LinkedIn, Twitter, and Instagram. Each platform has native patterns (carousel slides vs. threads vs. reels) — content that ignores format conventions underperforms regardless of message quality.

**Weak CTAs** — "Learn More" and "Click Here" tell the reader nothing about what they get. Every CTA must follow [action verb] + [what they get] — specificity increases click-through.

**A/B testing multiple variables** — Changing the hook, CTA, and format simultaneously makes results uninterpretable. Change exactly ONE element per variant — the learning is more valuable than the lift.

**Writing outlines instead of copy** — Delivering "Slide 3: Talk about the pain point" instead of the actual words. Content creation means writing every word, slide, and timestamp — outlines are not deliverables.

---

## References

- [references/examples.md](references/examples.md) — Complete worked examples with full copy
- [references/platform-specs.md](references/platform-specs.md) — Platform dimensions, limits, native patterns
- [references/repurposing-cascade.md](references/repurposing-cascade.md) — Hero → derivative content workflow across channels
