---
name: content-tools
description: Use this skill when researching a content topic, gathering supporting facts/data, auditing existing content, building a blog content brief, or generating headlines/value-props/feature-to-benefit/FAQ/social-proof copy for a blog post, landing page, or email — the reusable knowledge layer behind /content-creation and /marketing email + social-post operations, providing content research workflows (topic research, data/fact gathering, existing-content audit, blog content brief template) and AI text-generation prompt templates for headline generation, value propositions, feature-to-benefit translation, FAQ generation, and social proof.
disable-model-invocation: true
---

# Content Tools — Research + AI-Text Patterns

Reusable knowledge skill for content workflows. Topic research methodology, fact-gathering procedures, content brief template, and AI text-generation prompt templates. Used by `/content-creation` and `/marketing` operations that produce blog posts, page content, landing pages, or email copy.

Image-generation workflows live in the companion file `image-and-integration-workflows.md` in the legacy `/content-creation/` directory; load that file when generating visuals.

## Content Research Workflows

Systematic research phase before content creation. Applies to blog posts, articles, landing pages, and other public-facing content.

### Topic Research

**Goal**: Understand the topic landscape before writing.

**Steps**:

1. **Web search** — find 3-5 top-ranking articles for the target keyword. For each, note:
   - Angle and depth (surface-level vs deep-dive)
   - Content gaps (what they miss, what they get wrong)
   - Word count and structure
   - Publication date (freshness)
2. **Competitive content audit** — search competitor blogs for the same topic. Identify:
   - What angle competitors take
   - What unique data or perspective you can add
   - Content format differences (listicle vs guide vs case study)
3. **Keyword research** — identify search intent and related terms:
   - Primary keyword (main topic)
   - Secondary keywords (2-3 related terms for H2 headings)
   - Search intent: informational ("how to"), commercial ("best tools for"), transactional ("buy/sign up")
   - Long-tail variations for FAQ or subsections

### Data and Fact Gathering

**Goal**: Collect citable data points to strengthen the content.

**Steps**:

1. **Find statistics** — search for recent studies, surveys, benchmarks:
   - Prefer primary sources (original study) over secondary (blog citing a study)
   - Note publication date — discard data older than 2-3 years unless it's a foundational study
   - Save exact citation: author, organization, year, URL
2. **Fact-check** — verify every claim before including it:
   - Cross-reference with at least 2 independent sources
   - Check if the stat is used in correct context (not cherry-picked)
   - If a stat seems too good to be true — verify the methodology
3. **Expert quotes** — find relevant quotes from industry experts:
   - Conference talks, podcasts, published interviews
   - Always attribute with name, title, context

### Existing Content Audit

**Goal**: Identify cross-linking opportunities within the project's blog.

**Steps**:

1. **Scan blog directory** — list all existing posts with titles and topics
2. **Map relevance** — for each existing post, rate cross-link potential (high / medium / none)
3. **Plan bidirectional links**:
   - From new post → existing posts (minimum 3 internal links)
   - From existing posts → new post (update old posts to link to the new one)
4. **Identify content gaps** — topics the new post references that don't exist yet (future post ideas)

### Blog Content Brief Template

Use this brief specifically for blog posts (the general Content Brief Template applies to landing pages — see `page-content-patterns.md` in `/content-creation`):

```markdown
# Blog Content Brief: [Working Title]

## Research Summary
- **Top competing articles**: [3-5 URLs with one-line summaries]
- **Content gap identified**: [what competitors miss]
- **Unique angle**: [what makes this post different]

## Audience
- **Who**: [target reader persona]
- **Knowledge level**: [beginner / intermediate / expert]
- **Search intent**: [informational / commercial / transactional]

## Keywords
- **Primary**: [keyword] — [monthly search volume if known]
- **Secondary**: [keyword 2], [keyword 3]
- **Long-tail**: [question-based keyword for FAQ]

## Outline
1. [H2 section] — [what this covers, estimated word count]
2. [H2 section] — [what this covers, estimated word count]
3. [H2 section] — [what this covers, estimated word count]
...

## Data Points
- [Stat 1] — [source, year, URL]
- [Stat 2] — [source, year, URL]

## Cross-Links
- **Outbound to existing posts**: [post 1], [post 2], [post 3]
- **Inbound from existing posts**: [post A → update to link here]

## Visual Needs
- **Cover image**: [description, style, mood]
- **Inline visuals**: [diagrams, screenshots, illustrations]

## Target
- **Word count**: [range]
- **Reading time**: [X min]
```

## AI Text Generation Workflows

### Headline Generation

**Goal**: Generate multiple headline variants for A/B testing.

**Prompt template**:

```
You are a conversion copywriter. Write 10 headline variants for [page type].

Product: [product name and one-sentence description]
Target audience: [who they are, what they care about]
Primary benefit: [the #1 outcome for the user]
Tone: [professional/friendly/bold/playful]
Constraints: Max 10 words. No jargon. Specific > clever.

Format: Number each variant. After all 10, mark top 3 with rationale.
```

**Quality filter**: Discard headlines that are vague, use clichés ("revolutionize", "game-changer"), or don't communicate a specific benefit.

### Value Proposition Writing

**Prompt template**:

```
Write a value proposition for [product] following this structure:

1. Headline: What is the end benefit? (max 10 words)
2. Sub-headline: Who is it for and what does it do? (1-2 sentences)
3. Bullet points: 3 key benefits (outcome-focused, not feature-focused)
4. CTA: Action-oriented button text (3-5 words)

Context:
- Product: [description]
- Target user: [ICP description]
- Key differentiator: [what makes this unique]
- Competitor alternatives: [what users do today without this product]

Tone: [brand voice description]
```

### Feature-to-Benefit Translation

**Prompt template**:

```
Convert these product features into user benefits.

For each feature:
1. State the benefit (what the user gets)
2. Add emotional hook (why they should care)
3. Write a one-liner combining both

Features:
- [Feature 1]
- [Feature 2]
- [Feature 3]

Audience: [who they are]
Format: Table with columns: Feature | Benefit | Emotional Hook | One-liner
```

### FAQ Generation

**Prompt template**:

```
Generate FAQ entries for [product/feature page].

Context:
- Product: [description]
- Page purpose: [what the page covers]
- Target audience: [who visits this page]
- Common objections: [list known objections]

For each FAQ:
- Question: Written from the user's perspective (natural language)
- Answer: 2-3 sentences. Direct answer first, then context. No marketing fluff
- Generate 8-10 questions covering: pricing, features, security, onboarding, support, comparison, limitations

Format as structured FAQ suitable for JSON-LD schema markup.
```

### Social Proof Copy

**Prompt template**:

```
Write social proof copy based on these customer results:

Customer: [name, title, company]
Results: [specific metrics or outcomes]
Quote context: [what problem they had, what they tried before]

Generate:
1. Short testimonial quote (2-3 sentences, first person)
2. Case study headline
3. Metric callout (e.g., "80% faster deployments")
4. Social proof one-liner for near-CTA placement

Tone: Authentic, specific, not salesy. Include real numbers where available.
```

## When each pattern applies

| Pattern | Used by |
|---|---|
| Topic Research | `/content-creation` Step 2 (Research and Brief), `/marketing trend-research` |
| Data and Fact Gathering | `/content-creation` Step 2, `/marketing trend-research` |
| Existing Content Audit | `/content-creation` Step 2 (cross-link planning) |
| Blog Content Brief Template | `/content-creation blog-post` Step 2 deliverable |
| Headline Generation | `/content-creation` Step 3 (drafts), `/marketing social-post` |
| Value Proposition Writing | `/content-creation page` + `landing`, `/marketing-init` Step 3 (messaging) |
| Feature-to-Benefit Translation | `/content-creation page`, `/marketing-init` Step 3 |
| FAQ Generation | `/content-creation` Step 4 (GEO/AEO), `/marketing` content pages |
| Social Proof Copy | `/content-creation page` + `landing` |

## Integration

- **Used by**: `/content-creation` (blog + page workflows), `/marketing` (email, social-post, content-repurpose operations)
- **Companion knowledge**: `@geo-writer` (structure pass after drafting), `@humanizer` (voice cleanup pass)
- **Image workflows**: see `plugin/skills/content-creation/image-and-integration-workflows.md` (image-generation tools and external service integration live alongside /content-creation; not in this knowledge skill)
