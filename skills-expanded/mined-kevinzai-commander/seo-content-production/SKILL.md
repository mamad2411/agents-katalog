---
name: seo-content-production
parent: ccc-marketing
brand: Kevin Z's CC Commander
description: "Bridge between SEO briefs and content production. Transforms seo-content-brief output into production-ready writing guidelines and manages the brief-to-publish pipeline."
version: 1.0.0
dependencies:
  - seo-content-brief
tags:
  - seo
  - content-production
  - editorial
  - pipeline
---

# SEO Content Production

Bridge skill between SEO content briefs and finished content. Takes the output of ccc-seo's `seo-content-brief` skill and transforms it into production-ready writing guidelines, then manages the draft-review-publish pipeline while ensuring SEO requirements survive every editing round.

## When to Use

- You have a completed SEO content brief and need to turn it into a real article
- You need to hand off SEO requirements to a writer (human or AI) without losing fidelity
- You're managing a content pipeline from brief through publication
- You want to verify that edits haven't degraded SEO compliance
- You need to scale content production while maintaining SEO quality

## The Brief-to-Publish Pipeline

```
seo-content-brief (input)
    │
    ▼
[1] Brief Intake & Validation
    │
    ▼
[2] Writing Guidelines Generation
    │
    ▼
[3] Draft Production
    │
    ▼
[4] SEO Compliance Review
    │
    ▼
[5] Editorial Review
    │
    ▼
[6] Final SEO Check
    │
    ▼
[7] Publish-Ready Output
```

## Step 1: Brief Intake & Validation

When you receive an SEO content brief, validate it has the minimum required fields before proceeding.

### Required Fields Checklist

- [ ] **Primary keyword** — the main term this content targets
- [ ] **Secondary keywords** — supporting terms (3-10)
- [ ] **Search intent** — informational, navigational, commercial, transactional
- [ ] **Target word count** — based on SERP analysis
- [ ] **Recommended headings** — H2/H3 structure from competitor analysis
- [ ] **SERP features to target** — featured snippet, PAA, knowledge panel
- [ ] **Competitor URLs** — top 3-5 ranking pages analyzed

### Optional but Valuable

- [ ] Content gap analysis (what competitors miss)
- [ ] Internal linking targets (pages to link to/from)
- [ ] Schema markup recommendations
- [ ] Audience segment and reading level

If any required field is missing, flag it and request completion before proceeding. Producing content from an incomplete brief wastes effort.

## Step 2: Writing Guidelines Generation

Transform the SEO brief into actionable writing instructions that any writer can follow without needing to understand SEO.

### Writing Guidelines Template

```markdown
## Content Writing Guidelines

**Article Title:** [draft title — include primary keyword naturally]
**Target Length:** [X] words (min [X-10%], max [X+20%])
**Reading Level:** [Grade level / audience description]
**Tone:** [from brand voice guide or marketing-context.md]

### Structure

Follow this outline exactly. Each H2 is a required section. H3s are recommended but flexible.

#### H2: [Section Title]
- Cover: [key points to address]
- Include keyword: [specific term to use naturally]
- Length: ~[X] words
- [Special instruction: table, list, example, etc.]

#### H2: [Section Title]
- Cover: [key points]
- Include keyword: [term]
- Length: ~[X] words

[Repeat for all sections]

### Keyword Usage Rules

| Keyword | Min Uses | Where to Place |
|---------|----------|----------------|
| [primary] | [3-5] | Title, H2, intro, conclusion, meta description |
| [secondary 1] | [1-2] | H2 or body text |
| [secondary 2] | [1-2] | H2 or body text |
| [secondary 3] | [1-2] | Body text |

**Important:** Keywords must read naturally. Never force a keyword into a sentence where it sounds awkward. If a keyword doesn't fit naturally, use a close variant.

### Content Requirements

- [ ] Open with a hook that addresses the reader's problem directly (no "In today's world..." openers)
- [ ] Include at least [X] concrete examples or data points
- [ ] Every claim must be supportable (cite source inline or note for editor)
- [ ] Include a clear CTA in the conclusion
- [ ] Write for scanners: use bullet lists, bold key phrases, short paragraphs (3-4 sentences max)

### Featured Snippet Optimization

**Target format:** [paragraph / list / table]
**Target query:** [the question to answer]
**Instruction:** Write a concise [40-60 word paragraph / numbered list / comparison table] that directly answers "[query]" in the [section name] section. Place it immediately after the relevant H2.

### Internal Links

Link to these pages naturally within the content:
- [URL 1] — anchor text suggestion: "[text]"
- [URL 2] — anchor text suggestion: "[text]"
- [URL 3] — anchor text suggestion: "[text]"

### What NOT to Do

- Do not use the primary keyword more than [X] times (keyword stuffing)
- Do not copy structure or phrasing from competitor articles
- Do not use generic stock photo descriptions as alt text
- Do not write an introduction longer than 100 words
- Do not use passive voice for more than 15% of sentences
```

## Step 3: Draft Production

Use the writing guidelines to produce the draft. If using an AI writer, feed the guidelines directly as the prompt context.

### AI Writing Prompt Structure

```
You are a content writer. Follow the attached Writing Guidelines exactly.

Context:
- Brand voice: [paste from marketing-context.md]
- Target audience: [from brief]
- Goal: [from brief]

Writing Guidelines:
[paste generated guidelines from Step 2]

Write the complete article now. Follow the structure, keyword placement, and content requirements precisely.
```

### Quality Checkpoints During Writing

- After intro: Does it hook the reader and contain the primary keyword?
- After each section: Does it follow the outline and hit the keyword targets?
- After conclusion: Is there a clear CTA? Does the article feel complete?

## Step 4: SEO Compliance Review

After the draft is complete, run a systematic SEO compliance check. This catches issues before the editorial review changes things.

### SEO Compliance Checklist

```markdown
## SEO Compliance Review

**Article:** [title]
**Reviewer:** [name/agent]
**Date:** [date]

### Keyword Placement
- [ ] Primary keyword in title: [YES/NO]
- [ ] Primary keyword in first 100 words: [YES/NO]
- [ ] Primary keyword in at least one H2: [YES/NO]
- [ ] Primary keyword in conclusion: [YES/NO]
- [ ] Primary keyword density: [X%] (target: 0.5-1.5%)
- [ ] Secondary keywords present: [list which ones are included]
- [ ] No keyword stuffing detected: [YES/NO]

### Structure
- [ ] Word count: [X] (target: [Y] ±20%)
- [ ] H2 count: [X] (matches brief: [YES/NO])
- [ ] H3 usage for subsections: [YES/NO]
- [ ] No skipped heading levels (H2→H4): [YES/NO]
- [ ] Intro under 100 words: [YES/NO]
- [ ] Paragraphs under 4 sentences: [mostly YES/NO]

### Featured Snippet
- [ ] Target snippet section exists: [YES/NO]
- [ ] Format matches target (paragraph/list/table): [YES/NO]
- [ ] Concise enough for snippet extraction: [YES/NO]

### Links
- [ ] All required internal links present: [YES/NO]
- [ ] Anchor text is natural: [YES/NO]
- [ ] External links to authoritative sources: [count]

### Meta
- [ ] Meta title drafted (50-60 chars): [YES/NO]
- [ ] Meta description drafted (150-160 chars): [YES/NO]
- [ ] Primary keyword in both: [YES/NO]

### Issues Found
| Issue | Severity | Location | Fix |
|-------|----------|----------|-----|
| [description] | HIGH/MED/LOW | [section] | [what to change] |
```

## Step 5: Editorial Review

After SEO compliance passes, the content goes through editorial review for quality, accuracy, and brand voice. The key challenge: editors often break SEO requirements without realizing it.

### Editor Instructions

Provide editors with this notice:

```
IMPORTANT FOR EDITORS:

The following elements are SEO-critical and must be preserved through editing:

1. TITLE — contains target keyword "[keyword]". You may rephrase but the keyword must remain.
2. HEADINGS — H2 structure follows a specific SEO blueprint. You may adjust wording but do not remove, merge, or reorder H2 sections without checking with SEO.
3. KEYWORD USAGE — the following terms appear intentionally:
   - "[primary keyword]" — must appear in intro, at least one H2, and conclusion
   - "[secondary keywords]" — must appear at least once each
4. INTERNAL LINKS — these links are placed intentionally for SEO. Do not remove them. You may adjust surrounding text.
5. FEATURED SNIPPET BLOCK — the [paragraph/list/table] in [section] is formatted specifically for Google's featured snippet. Preserve its format and conciseness.

If you need to make changes to any of these elements, flag them for SEO review rather than editing directly.
```

## Step 6: Final SEO Check

After editorial review, run the SEO compliance checklist again (Step 4). Compare results against the pre-edit check.

### Post-Edit Comparison

```markdown
## Post-Edit SEO Delta

| Element | Pre-Edit | Post-Edit | Status |
|---------|----------|-----------|--------|
| Primary keyword in title | YES | [?] | [OK/BROKEN] |
| Primary keyword density | [X%] | [?] | [OK/BROKEN] |
| H2 count | [X] | [?] | [OK/BROKEN] |
| Internal links present | [X/Y] | [?] | [OK/BROKEN] |
| Featured snippet intact | YES | [?] | [OK/BROKEN] |
| Word count | [X] | [?] | [OK/BROKEN] |
| Meta title/desc | YES | [?] | [OK/BROKEN] |

### Remediation Required
[List any BROKEN items and what needs to be restored]
```

If any SEO requirements were broken during editing, fix them now. Do not publish with degraded SEO compliance.

## Step 7: Publish-Ready Output

The final deliverable includes all assets needed for publication.

### Publish Package

```markdown
## Publish-Ready Package

### Content
- **Title:** [final title]
- **Slug:** [url-slug]
- **Body:** [the article in HTML or Markdown]
- **Meta Title:** [50-60 chars]
- **Meta Description:** [150-160 chars]
- **Featured Image Alt Text:** [descriptive, includes keyword if natural]

### Technical SEO
- **Canonical URL:** [if applicable]
- **Schema Markup:** [from brief recommendations]
- **Open Graph:** title, description, image
- **Twitter Card:** title, description, image

### Internal Linking
- **Links placed in article:** [list with anchor text]
- **Pages that should link TO this article:** [list — update after publishing]

### Post-Publish Checklist
- [ ] Article indexed (submit URL in Search Console)
- [ ] Internal links from other pages added
- [ ] Social promotion scheduled
- [ ] Email newsletter inclusion scheduled
- [ ] Performance tracking set up (rank tracking for target keywords)
```

## Pipeline Management at Scale

When managing multiple articles through this pipeline simultaneously:

### Status Board

```markdown
| Article | Brief | Guidelines | Draft | SEO Check | Edit | Final Check | Published |
|---------|-------|-----------|-------|-----------|------|-------------|-----------|
| [title] | Done  | Done      | In Progress | - | - | - | - |
| [title] | Done  | Done      | Done  | Done | In Progress | - | - |
| [title] | Done  | In Progress | - | - | - | - | - |
```

### Throughput Guidelines

- 1 writer can handle 2-3 articles/week through this full pipeline
- SEO compliance review takes 15-30 minutes per article
- Editorial review takes 30-60 minutes per article
- Budget 2-3 business days from brief to publish-ready for a single article

## Anti-Patterns

- Skipping brief validation and writing from incomplete data
- Generating content without writing guidelines (the brief is NOT the same as writing instructions)
- Letting editorial changes go unchecked for SEO compliance
- Publishing without the final SEO check (editors break SEO more often than you'd expect)
- Keyword stuffing to hit density targets (if it doesn't read naturally, reduce usage)
- Ignoring featured snippet formatting (this is where most organic traffic gains come from)
- Not updating internal links on other pages after publishing (half the SEO value of internal linking)
