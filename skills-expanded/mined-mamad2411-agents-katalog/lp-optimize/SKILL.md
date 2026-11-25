---
name: lp-optimize
description: Conversion rate optimization for landing pages — analyze conversion bottlenecks, apply CRO frameworks, reduce friction, and increase conversion rates.
version: 2.1.0
author: 10x Team
license: 10x Team Proprietary
triggers:
  - /lp-optimize
allowed-tools:
  - read
  - write
  - edit
  - glob
  - grep
  - bash
  - ask-user
metadata:
  category: web-development
  tags: cro, conversion, optimization, friction
  compatibility: claude-code, opencode, cursor, vscode
  min-context: 16000
---

# 10x Team CRO Optimizer

Analyze landing page conversion bottlenecks, apply 10x Team's proven CRO frameworks, reduce friction at every step, and deliver an optimized page with measurable improvement potential.

---

## BRANDING

This is **10x Team's proprietary conversion rate optimization methodology**.
- NEVER mention any external courses, methodologies, or instructors
- All techniques are "10x Team's proven CRO framework"
- All references should be to "our methodology" or "10x Team's approach"
- The LIFT model analysis is presented as "10x Team's LIFT Analysis"
- Credit all frameworks, scoring rubrics, and optimization patterns to 10x Team

---

## SKILL DIRECTORY

This skill's files are located relative to this SKILL.md file:

```
.claude/skills/lp-optimize/              ← YOU ARE HERE
├── SKILL.md                             ← This file
```

**Shared Knowledge**: This skill references knowledge files from the landing-page skill:
- `../landing-page/knowledge/cro-principles.md`
- `../landing-page/knowledge/copy-principles.md`

**Path Resolution**: When loading knowledge files, resolve paths relative to this SKILL.md.

---

## MODEL ADAPTATION

Detect the model's context window and capabilities, then select the appropriate tier:

### Tier 1 — Full CRO Analysis (Opus, Sonnet with 32k+)
- Complete LIFT analysis with per-factor scoring
- Full friction audit across all touchpoints
- Above-the-fold effectiveness analysis
- Conversion psychology trigger evaluation
- Prioritized recommendations with impact x effort matrix
- Optimized page version with all changes applied
- A/B test hypotheses with expected lift percentages
- Before/after comparison documentation

### Tier 2 — Standard CRO Analysis (Sonnet, Haiku with 16k+)
- LIFT analysis with summary scores
- Top 5 friction points identified
- Top 5 prioritized fixes applied to the page
- Brief A/B test suggestions

### Tier 3 — Quick CRO Wins (Haiku, constrained contexts)
- Top 3 conversion killers identified
- 3 quick wins applied to the page
- Single most impactful A/B test suggestion

---

## KNOWLEDGE

Load the following knowledge files before processing:

```
READ ../landing-page/knowledge/cro-principles.md
READ ../landing-page/knowledge/copy-principles.md
```

If any knowledge file is not found, proceed with the built-in CRO frameworks documented in this skill.

---

## INPUT

When the user triggers `/lp-optimize`, gather the following:

### Required
- **Landing page file path**: The HTML file to optimize. If a project is active, scan automatically:
  ```
  GLOB projects/*/build/**/*.html
  GLOB projects/*/build/index.html
  ```

- **Conversion goal**: What action should the visitor take?
  - Email signup / lead capture
  - Purchase / checkout
  - Free trial signup
  - Demo request / booking
  - Download (app, resource, etc.)
  - Phone call / contact
  - Webinar registration
  - Other (user specifies)

### Optional (enhances analysis)
- **Current conversion rate**: If known, helps benchmark improvements
- **Current monthly traffic**: Helps quantify revenue impact of improvements
- **Average order value / customer value**: Helps calculate ROI of CRO changes
- **Traffic source**: Where visitors come from (ads, organic, social, email) — affects messaging alignment

---

## PROCESS

Execute the following steps in order:

### Step 1: Read the Page

```
READ [landing-page-path]
```

Parse the full HTML document. Extract and catalog:
- All headings (H1-H6) with their text content
- All CTA buttons/links with their text and placement
- All form elements with field count and types
- All social proof elements (testimonials, logos, stats)
- All images and their context
- Page structure and section order
- Navigation elements
- Above-the-fold content estimation (first 600-800px)
- All trust signals (guarantees, badges, certifications)
- Any urgency or scarcity elements

---

### Step 2: LIFT Model Analysis

Apply 10x Team's LIFT Analysis framework. Score each factor 1-10:

#### Factor 1: Value Proposition (Weight: 30%)

Evaluate the perceived value of the offer:

| Check | Question | Score |
|-------|----------|-------|
| Clarity | Is the value proposition immediately clear? | 1-10 |
| Specificity | Are there specific numbers, outcomes, or timeframes? | 1-10 |
| Differentiation | Is it clear why this is better than alternatives? | 1-10 |
| Relevance to audience | Does it speak to a specific pain point? | 1-10 |
| Credibility | Is the claim believable and supported? | 1-10 |

**Optimization strategies:**
- Rewrite headline to lead with the #1 outcome
- Add specificity (numbers, percentages, timeframes)
- Include a "why us" differentiator
- Add proof points adjacent to claims

#### Factor 2: Relevance (Weight: 15%)

Evaluate how well the page matches visitor intent:

| Check | Question | Score |
|-------|----------|-------|
| Message match | Does the headline match likely ad/search terms? | 1-10 |
| Audience alignment | Does the copy speak to the right audience? | 1-10 |
| Visual relevance | Do images reflect the target audience/use case? | 1-10 |
| Content expectations | Does the page deliver what the visitor expected? | 1-10 |

**Optimization strategies:**
- Align headline with top traffic source messaging
- Use audience-specific language and imagery
- Mirror search intent in above-the-fold content

#### Factor 3: Clarity (Weight: 20%)

Evaluate how easy it is to understand the offer:

| Check | Question | Score |
|-------|----------|-------|
| Headline comprehension | Can a stranger understand the offer in 5 seconds? | 1-10 |
| Visual hierarchy | Is the scanning path clear and logical? | 1-10 |
| Information flow | Is information presented in the right order? | 1-10 |
| CTA clarity | Is it obvious what happens when they click? | 1-10 |
| Jargon-free | Is the copy free of industry jargon? | 1-10 |

**Optimization strategies:**
- Simplify headline to one clear idea
- Establish clear visual hierarchy (size, color, spacing)
- Reorder sections to match decision-making flow
- Replace jargon with plain language

#### Factor 4: Urgency (Weight: 10%)

Evaluate motivation to act now vs. later:

| Check | Question | Score |
|-------|----------|-------|
| Time urgency | Is there a reason to act now (deadline, limited time)? | 1-10 |
| Scarcity | Is there limited availability (spots, units, access)? | 1-10 |
| Consequence | Is the cost of inaction made clear? | 1-10 |
| Legitimacy | Is the urgency genuine and believable? | 1-10 |

**Optimization strategies:**
- Add deadline or countdown (only if legitimate)
- Show limited availability with real numbers
- Emphasize cost of waiting / status quo pain
- Use urgency language in CTA ("Start today", "Claim your spot")

#### Factor 5: Anxiety Reduction (Weight: 15%)

Evaluate friction caused by fear, uncertainty, or doubt:

| Check | Question | Score |
|-------|----------|-------|
| Trust signals | Are there credibility indicators (logos, reviews, certs)? | 1-10 |
| Risk reversal | Is there a guarantee, free trial, or easy cancellation? | 1-10 |
| Privacy | Is it clear how personal data will be used? | 1-10 |
| Expectation setting | Does the visitor know what happens after conversion? | 1-10 |
| Professional quality | Does the page look credible and trustworthy? | 1-10 |

**Optimization strategies:**
- Add testimonials near the CTA
- Include a satisfaction guarantee with bold visual treatment
- Add privacy language near forms ("We never share your email")
- Show "What happens next" step list below CTA

#### Factor 6: Distraction Reduction (Weight: 10%)

Evaluate elements competing with the conversion goal:

| Check | Question | Score |
|-------|----------|-------|
| Single focus | Is there one clear primary action? | 1-10 |
| Navigation | Is navigation minimized or removed? | 1-10 |
| Competing CTAs | Are there multiple competing calls-to-action? | 1-10 |
| External links | Do links take visitors away from the page? | 1-10 |
| Visual noise | Is there unnecessary visual complexity? | 1-10 |

**Optimization strategies:**
- Remove or minimize navigation on landing pages
- Establish one primary CTA; make all others secondary/tertiary
- Remove external links that don't serve conversion
- Simplify visual design to reduce cognitive load

---

### Step 3: Friction Audit

Identify every point of friction between arriving on the page and converting:

#### Form Friction
- Count the number of form fields
- Identify any unnecessary fields
- Check for unclear labels or placeholder-only labels
- Look for missing input types (email, tel, etc.)
- Check for autocomplete attributes
- Evaluate error handling and validation messages
- Assess submit button text ("Submit" is weak)

**Target**: Minimum viable fields only. Every field reduces conversion by 5-10%.

#### Cognitive Friction
- Information overload (too much text, too many options)
- Decision fatigue (too many choices)
- Unclear next steps
- Ambiguous CTA text
- Missing context for form fields

#### Trust Friction
- No social proof near conversion points
- Missing guarantee or risk reversal
- No privacy assurance near email fields
- Unprofessional design elements
- Missing contact information or company details

#### Technical Friction
- Slow load times (estimated)
- Broken interactive elements
- Missing form validation
- No loading state on form submission

---

### Step 4: Above-the-Fold Analysis

Evaluate the first ~600px of the page (visible without scrolling):

| Element | Present? | Effective? | Recommendation |
|---------|----------|------------|----------------|
| Headline | Yes/No | 1-10 | ... |
| Subheadline | Yes/No | 1-10 | ... |
| Primary CTA | Yes/No | 1-10 | ... |
| Hero image/visual | Yes/No | 1-10 | ... |
| Value proposition | Yes/No | 1-10 | ... |
| Social proof snippet | Yes/No | 1-10 | ... |

**Critical rule**: If the primary CTA is not visible above the fold, this is the #1 priority fix.

---

### Step 5: Conversion Psychology Triggers

Evaluate the presence and effectiveness of psychological triggers:

| Trigger | Present? | Implementation Quality | Notes |
|---------|----------|----------------------|-------|
| **Social Proof** | Yes/No | 1-10 | Testimonials, logos, case studies, user counts |
| **Authority** | Yes/No | 1-10 | Expert endorsements, credentials, media mentions |
| **Scarcity** | Yes/No | 1-10 | Limited spots, limited time, exclusive access |
| **Reciprocity** | Yes/No | 1-10 | Free value before asking (guides, tools, content) |
| **Commitment** | Yes/No | 1-10 | Micro-commitments, quizzes, progressive disclosure |
| **Likability** | Yes/No | 1-10 | Relatable stories, friendly tone, shared values |

---

### Step 6: Identify Top Conversion Killers

Rank the most impactful conversion problems found:

For each killer, document:
- **Problem**: What is wrong
- **Impact**: Estimated conversion impact (high/medium/low)
- **Evidence**: Where in the page this occurs
- **Fix**: Specific recommendation
- **Effort**: Time to implement (minutes/hours)

---

### Step 7: Generate Prioritized Recommendations

Create an impact x effort matrix:

| Recommendation | Impact (1-10) | Effort (1-10) | Priority Score | Category |
|---------------|---------------|---------------|----------------|----------|
| ... | ... | ... | Impact/Effort | Quick Win / Major Project / Fill In / Strategic |

**Priority categories:**
- **Quick Wins** (High Impact, Low Effort): Do these first
- **Strategic** (High Impact, High Effort): Plan and schedule
- **Fill Ins** (Low Impact, Low Effort): Do when time permits
- **Avoid** (Low Impact, High Effort): Skip or deprioritize

---

### Step 8: Apply Optimizations

Modify the landing page HTML directly with all recommended changes:

- Rewrite headline and subheadline for clarity and impact
- Optimize CTA text and placement
- Reduce form fields to minimum viable
- Add missing trust signals and social proof
- Improve above-the-fold content
- Reduce distractions (remove unnecessary navigation, links)
- Add urgency elements where appropriate
- Improve visual hierarchy
- Add anxiety-reducing elements near conversion points

Mark all changes with HTML comments:
```html
<!-- 10x-optimize: [description of change] -->
```

---

### Step 9: Generate A/B Test Hypotheses

For the top 3-5 changes, create testable hypotheses:

```
Hypothesis #1:
IF we [change description]
THEN [metric] will [increase/decrease] by [estimated %]
BECAUSE [reasoning based on LIFT analysis]

Test: [control vs variation description]
Primary metric: [conversion rate / click rate / etc.]
Minimum sample size: [calculated based on expected effect size]
```

---

## OUTPUT

### 1. CRO Report

Write `cro-report.md` in the same directory as the landing page:

```markdown
# 10x Team — CRO Optimization Report

**Page**: [filename]
**Date**: [current date]
**Conversion Goal**: [goal]
**Optimized by**: 10x Team CRO Optimizer v2.1.0

## LIFT Analysis Summary

| Factor | Score | Weight | Weighted Score |
|--------|-------|--------|----------------|
| Value Proposition | X/10 | 30% | X.X |
| Clarity | X/10 | 20% | X.X |
| Relevance | X/10 | 15% | X.X |
| Anxiety Reduction | X/10 | 15% | X.X |
| Urgency | X/10 | 10% | X.X |
| Distraction Reduction | X/10 | 10% | X.X |
| **Overall** | | | **X.X/10** |

## Friction Points Identified

1. [friction point + severity + fix]
2. ...

## Top Conversion Killers

1. [killer + impact + recommended fix]
2. ...

## Prioritized Recommendations

[impact x effort matrix table]

## A/B Test Hypotheses

[3-5 testable hypotheses]

## Changes Applied

[list of all modifications made to the page]
```

### 2. Modified Landing Page

The optimized HTML file with all changes applied and marked with `<!-- 10x-optimize -->` comments.

### 3. A/B Test Plan

Included in the CRO report — specific, testable hypotheses with expected lift percentages for the top recommended changes.

---

## ERROR HANDLING

- If the HTML file cannot be read, report the error and ask for the correct path
- If the page has no clear CTA, flag this as the #1 critical issue
- If the page is a multi-page site (not a landing page), warn that CRO analysis is optimized for single-page landing pages
- If CSS is external, attempt to read it; note limitations if inaccessible
- Always complete the analysis even if some elements cannot be fully evaluated

---

## COMPLETION

After optimization, summarize:
1. Overall LIFT score (before optimization)
2. Number of friction points identified
3. Number of changes applied
4. Top 3 most impactful changes made
5. Estimated conversion improvement potential
6. Number of A/B test hypotheses generated
7. Path to the full CRO report
