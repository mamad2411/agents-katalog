---
name: draft-creator
description: Create SEO content drafts from topic ideas or requirements. Use when the user wants to write a blog post, article, or guide and needs help with research, outlining, and structure. Triggers on "create a draft", "write a blog post", "help me outline", "content brief", or when the user provides a topic idea they want to develop into full content.
metadata:
  displayName: Draft Creator
  status: live
  phases:
    - name: Gather requirements
    - name: Find information gain
    - name: Select conversion hooks
    - name: Create outline
---

Create a content draft from a topic idea or content requirements.

## 0. Load Project Context

Run /seo-memory. It handles checking for an existing file, creating one if needed, or skipping.

## 1. Gather Requirements (subagent)

Read `references/requirements-gatherer.md` for the full process.

> **Constraint**: Never use WebSearch in this step. Use /serp-gap-analysis Phase 1 only — it has a specialized SERP API.

**Input**: user's topic idea OR content requirements

**Returns**:
- Keyword
- Search intent (must be related to the topic)
- Winnability (for reference)
- Pages to explore (title + snippet from SERP)

### Setup

Create `./blogs/<topic>/` folder for all writing-related files.

## 2. Find Information Gain (subagent)

Run /content-researcher, passing the SERP from Step 1 (keyword + pages list) so it skips its own search steps and goes straight to reading. This produces:
- `./blogs/<topic>/knowledge-base.md` — collected knowledge from SERP pages
- `./blogs/<topic>/under-discussed.md` — questions competitors don't answer well

Information gain = what the reader still cannot do, decide, understand, or trust after reading the top results. The under-discussed questions are your information gain.

## 3. Select Conversion Hooks (subagent)

If seo-memory was loaded, scan it and pick the pieces that naturally fit this article's topic and reader intent:

- **Offerings** — which capabilities/benefits are directly relevant to the reader's problem?
- **Pricing** — is there a free tier or low-commitment entry point worth mentioning?
- **Audience** — which segment matches the target reader? Use their pain points and goals to frame the narrative.
- **Positioning** — any differentiator that answers a question the reader would naturally ask?

Write a short selection (a few bullet points) into `./blogs/<topic>/conversion-hooks.md` — what you picked and where it fits in the article. These are not ads; they should feel like natural examples, proof points, or recommendations within the content.

If seo-memory was not loaded, skip this step.

## 4. Create Outline (subagent)

Use this structure, adapting to content format and word count:

1. **Hook** — grab attention, establish relevance
2. **Problem** — what's at stake, why it matters
3. **Why existing advice is incomplete** — set up your unique angle
4. **Your framework/method** — the core value
5. **Examples/applications** — make it concrete
6. **Mistakes/caveats** — build trust, add depth
7. **Conclusion/next step** — actionable takeaway

### Adapt Based On

- **Word count** — expand or compress sections accordingly
- **Must-have topics** — verify knowledge base has content to cover each
- **Under-discussed questions** — integrate 2-3 as your information gain
- **Conversion hooks** — place them where they serve the reader (e.g., a product capability as a concrete example in the framework section, a free tier mention in the next-step conclusion). Mark these placements in the outline with `[hook: ...]`.

### Output Format

```
## {H2 Title}
{1-2 sentence description of what this section covers}
({word count} words)
```

Repeat for each section. Total word counts should match the target.
