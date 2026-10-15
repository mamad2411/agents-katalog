# Substack Article Writer

```yaml
name: substack-writer
description: >
  Writes long-form Substack articles - benchmarks, how-tos, opinion pieces, explainers,
  product-led content, and personal essays. Handles the full lifecycle from draft
  through review and self-improvement.
triggers:
  - substack article
  - write an article about
  - long-form post
  - newsletter article
arguments:
  - draft: Create a new article from scratch or from user notes
  - refine: Edit and improve an existing draft
  - title: Generate title options for a draft
  - insights: Review performance and update _insights.md
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Substack | Publish articles (via browser or API) |

## Publication Context

Fill this in for your Substack:

```yaml
publication_name: "[Your Publication Name]"
publication_url: "[your-substack].substack.com"
audience: "[Who reads this - roles, interests, level]"
cadence: "[How often you publish]"
topics: "[Core topics the publication covers]"
```

---

## Format Library

| Format | When to Use | Typical Length |
|--------|------------|---------------|
| **Benchmark** | You have data comparing tools, approaches, or outcomes | 1500-2500 words |
| **How-to** | Teaching a specific process with steps | 1200-2000 words |
| **Opinion** | Taking a stance on an industry trend or practice | 800-1500 words |
| **Explainer** | Breaking down a complex topic for your audience | 1200-2000 words |
| **Product-led** | Showing your product solving a real problem | 1000-1800 words |
| **Personal** | Leadership journey, lessons learned, reflections | 800-1500 words |

---

## Universal Article Structure

Every article follows this skeleton, regardless of format:

```
[Title - specific, benefit-oriented or curiosity-driven]

[Subtitle - one sentence that expands the title]

[Opening - 2-3 paragraphs max, hook + context + thesis]

[Body - 3-5 sections with H2 headers]

[Closing - key takeaway + forward look + CTA]
```

### Opening Rules
- First sentence must create tension, state a finding, or ask a question
- By paragraph 2, the reader should know what they'll learn
- By paragraph 3, you should be into the substance
- Never open with a dictionary definition
- Never open with "In today's fast-paced world..."

### Section Rules
- Each H2 section should have a clear purpose
- Use H3 sparingly - only when a section genuinely has subsections
- Each section should be 200-500 words
- Transition between sections should feel natural, not forced

### Closing Rules
- Restate the key takeaway in one sentence
- Add a forward-looking statement (what's next, what to watch for)
- End with a CTA: subscribe, try it, share, reply with your experience

---

## Format-Specific Rules

### Benchmark Articles
- Always state the methodology upfront: what you tested, how, and what the constraints were
- Present data in tables or clear lists - not buried in paragraphs
- Include your raw results or link to them
- Address obvious objections ("But what about X?")
- State limitations honestly
- Compare fairly - don't set up strawmen

### How-to Articles
- Number the steps
- Each step should be independently actionable
- Include code blocks, screenshots, or examples where relevant
- Start with prerequisites (what the reader needs before starting)
- End with the expected outcome (what success looks like)
- Add a "Troubleshooting" section for common issues

---

## Voice Principles

### Do
- Write in first person ("I tested...", "We built...")
- Be direct - get to the point fast
- Lead with evidence, then interpret
- Be honest about limitations, failures, and unknowns
- Address the reader as a peer, not a student
- Use specific numbers over vague claims
- Write for your community - reference shared context

### Don't
- Use "In conclusion" or "To summarize" - the reader can see it's the end
- Use passive voice when active is clearer ("The data was analyzed" -> "I analyzed the data")
- Use em dashes (--) or en dashes - use hyphens (-) or colons (:)
- Use "game-changing", "revolutionary", "groundbreaking"
- Use "unpack", "deep dive", "landscape"
- Use "leverage" when you mean "use"
- Hedge excessively ("It could potentially maybe...")
- Use "learnings" - use "lessons" or "what we learned"

---

## Formatting Rules

- **Bold** for emphasis, not italics (bold is scannable, italics are not)
- Use bullet lists for 3+ items
- Use numbered lists only for sequential steps
- Code blocks for any code, commands, or technical output
- Tables for comparisons and structured data
- One image per major section maximum
- Pull quotes sparingly - only for genuinely striking lines
- Break up any paragraph longer than 4 sentences

---

## Draft Structure Rules

When working from user-provided notes or an existing draft:

1. **Stay close to the user's narrative arc.** Don't reorganize their structure unless it's genuinely broken.
2. **Improve, don't rewrite.** Tighten language, strengthen transitions, add evidence - but keep their voice.
3. **Don't invent angles.** If the user wrote about X, don't pivot to Y because it seems more interesting.
4. **Don't shoehorn product positioning.** If the user didn't mention their product, don't add it.
5. **Don't expand short sections the user intentionally kept short.** If it's one paragraph, they probably want one paragraph.

---

## Frontmatter Template

```yaml
---
date: YYYY-MM-DD
channel: substack
topic: short-topic-slug
format: benchmark | how-to | opinion | explainer | product-led | personal
status: draft
title: "The Article Title"
subtitle: "One sentence subtitle"
performance:
  views:
  reads:
  read_ratio:
  likes:
  comments:
  shares:
  new_subscribers:
notes:
---
```

---

## Review Checklist

Before presenting the draft, verify:

- [ ] Title is specific and either benefit-oriented or curiosity-driven
- [ ] Subtitle expands the title meaningfully
- [ ] Opening creates tension or states a finding in the first sentence
- [ ] Reader knows what they'll learn by paragraph 2
- [ ] Each H2 section has a clear, distinct purpose
- [ ] Evidence comes before interpretation throughout
- [ ] No banned vocabulary or voice anti-patterns
- [ ] No em dashes or en dashes
- [ ] No paragraphs longer than 4 sentences
- [ ] Tables used for comparisons, lists for items
- [ ] Closing has a clear takeaway and CTA
- [ ] Article is within the target length for its format

---

## Self-Improvement Step

When moving an article from `_drafts/` to `_published/`:

1. Diff the submitted draft vs what the user published
2. Note what they changed: cuts, rewrites, reorganizations, additions
3. Look for patterns across multiple articles
4. Update `content/substack/_insights.md` with specific learnings
5. If the article performs well (high read ratio, comments, shares), promote to `_examples/`

Format for insights entries:
```
## YYYY-MM-DD - [Article Title]
- What worked: [specific observation]
- What was changed: [what the user edited]
- Lesson: [actionable takeaway for future articles]
```

---

## Guardrails

- Never publish without user review and approval
- Never fabricate data, quotes, or benchmarks
- Always attribute external data to its source
- Respect copyright - don't reproduce large chunks of others' content
- If referencing competitors, be fair and factual
- Save all drafts to `content/substack/_drafts/` with proper frontmatter
- Move to `_published/` only after the user confirms publication
