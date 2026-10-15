---
name: design-evaluation-scoring
description: This skill should be used when the user asks to evaluate, score, or audit a visual design, wants to compare designs quantitatively, needs an anti-pattern checklist, or wants to understand the 8-dimension design quality framework. Covers the VisAWI-aligned 8-dimension scoring methodology (1-5 per dimension, 40-point maximum), processing fluency theory, the anti-pattern rapid screening checklist, and the complete evaluation workflow.
version: 1.0.0
---

# Visual Quality Is Not Subjective -- It Is Measurable Across 8 Dimensions

Empirical aesthetics research (VisAWI by Moshagen & Thielsch, Lavie & Tractinsky 2004, Seckler et al. 2015) shows that perceived visual quality is not arbitrary opinion -- it decomposes into measurable dimensions. The 8-dimension framework below maps each dimension to research-validated constructs, giving you a repeatable, objective scoring system for any visual artifact.

## The 8 Dimensions

| # | Dimension | Research Alignment | What It Measures |
|---|-----------|-------------------|------------------|
| 1 | **Layout** | Seckler et al. (structural clarity) | Grid adherence, alignment, spatial composition, responsive behavior |
| 2 | **Typography** | Bringhurst, Butterick | Type scale, font pairing, line length, readability, hierarchy |
| 3 | **Color** | Reinecke et al., 60-30-10 rule | Palette harmony, contrast compliance, shade scale, dark mode |
| 4 | **Whitespace** | Pracejus et al. (perceptions of luxury) | Spacing consistency, density ratio, separation techniques |
| 5 | **Hierarchy** | Refactoring UI (emphasis/de-emphasis) | Focal points, 3-tier clarity, scanning patterns, CTA prominence |
| 6 | **Consistency** | VisAWI Craftsmanship subscale | Design tokens, component uniformity, cross-screen coherence |
| 7 | **Craftsmanship** | VisAWI Craftsmanship subscale | Pixel precision, image quality, shadows, micro-interactions, CLS |
| 8 | **Expression** | Lavie & Tractinsky (Expressive aesthetics) | Brand personality, visual motifs, illustration, motion, originality |

## Quick Scoring Rubric

Score each dimension 1-5. Total is out of 40.

| Score | Meaning | Indicators |
|-------|---------|------------|
| **1** | Broken | Fundamental violations; unusable or visually chaotic |
| **2** | Weak | Multiple issues; feels amateur or unfinished |
| **3** | Adequate | Meets basics; no major violations but lacks refinement |
| **4** | Good | Consistent and polished; minor improvements possible |
| **5** | Excellent | Research-aligned best practice; cohesive and intentional |

## Score Interpretation

| Total | Rating | Meaning |
|-------|--------|---------|
| **< 16** | Poor | Significant redesign needed across multiple dimensions |
| **16-23** | Below Average | Several dimensions need improvement; structural issues likely |
| **24-31** | Adequate | Solid foundation; targeted improvements will elevate quality |
| **32-37** | Good | Professional quality; polish and expression can push higher |
| **38-40** | Excellent | Best-in-class visual quality across all dimensions |

## Processing Fluency Theory

Reber et al. (2004) established that **easier to process = more beautiful**. Designs that are visually fluent -- consistent grids, predictable spacing, clear hierarchy -- are perceived as more trustworthy, more professional, and more aesthetically pleasing. This is not taste; it is cognitive science.

**Implication:** Structural factors (layout, typography, whitespace) that increase processing fluency have a larger impact on perceived quality than expressive factors (color, illustration, motion).

## Structural Factors Dominate

Seckler et al. (2015) found that **layout, typography, and whitespace explain more variance in perceived quality than color or expression**. A design with a perfect grid, well-chosen type, and generous whitespace will score well even with a minimal color palette. The reverse is never true -- no amount of color or illustration rescues a broken grid.

**Prioritize dimensions 1-5 before investing in 6-8.**

## The Complete Evaluation Workflow

### Step 1: 50ms First Impression

Look at the design for 50 milliseconds (a glance). Record your gut reaction: professional or amateur? Cluttered or clean? This leverages the Lindgaard et al. (2006) finding that aesthetic judgments form in 50ms and correlate strongly with extended evaluation.

### Step 2: Anti-Pattern Rapid Screening

Run through the 10-item checklist below in under 60 seconds. Each "yes" is a red flag.

| # | Check | Red Flag |
|---|-------|----------|
| 1 | More than 3 font families visible? | Typography violation |
| 2 | Text below 4.5:1 contrast on any background? | Accessibility failure |
| 3 | Elements visibly misaligned to each other? | Grid breakdown |
| 4 | Spacing feels inconsistent (different gaps for same relationships)? | Whitespace violation |
| 5 | No clear focal point -- everything competes equally? | Hierarchy failure |
| 6 | Color-only status indicators without icons or labels? | Accessibility failure |
| 7 | Low-resolution or stretched images? | Craftsmanship failure |
| 8 | Inconsistent border-radius, shadow, or button styles? | Consistency failure |
| 9 | Content touching container edges (no padding)? | Whitespace violation |
| 10 | No visual personality -- could belong to any brand? | Expression gap |

### Step 3: Dimension-by-Dimension Audit

Score each of the 8 dimensions using the rubric. Reference the corresponding principle skill for detailed criteria:

1. **Layout** -- Invoke `visual-design-principles:layout-spatial-structure`
2. **Typography** -- Invoke `visual-design-principles:typography`
3. **Color** -- Invoke `visual-design-principles:color-theory-application`
4. **Whitespace** -- Invoke `visual-design-principles:whitespace-density`
5. **Hierarchy** -- Invoke `visual-design-principles:visual-hierarchy`
6. **Consistency** -- Invoke `visual-design-principles:consistency-design-systems`
7. **Craftsmanship** -- Invoke `visual-design-principles:craftsmanship-polish`
8. **Expression** -- Invoke `visual-design-principles:visual-interest-expression`

### Step 4: Score and Prioritize

Sum the scores. Identify the lowest-scoring dimensions and prioritize improvements there. Structural dimensions (1-5) should be fixed before expressive dimensions (6-8).

## Measurable Proxies

Use these measurable values to ground subjective impressions in data:

| Metric | Target | Tool |
|--------|--------|------|
| Whitespace ratio | 30-50% for standard sites | Browser DevTools element inspection |
| Spacing system compliance | >90% of values on the defined scale | CSS audit / Tailwind config review |
| Contrast ratios | 4.5:1 body, 3:1 large text | WebAIM Contrast Checker, axe-core |
| Grid adherence | >90% of edges aligned to grid lines | Grid overlay in DevTools |
| CLS (Cumulative Layout Shift) | < 0.1 | Lighthouse, Web Vitals |
| Type scale compliance | All sizes from defined modular scale | CSS audit |
| Image resolution | 2x minimum for retina displays | Manual check |

## Cross-Media Notes

The 8-dimension framework applies to any visual medium. Adjust the specific benchmarks per context:

- **Presentations:** Weight Layout (slide grid), Typography (readability at distance), and Whitespace (50-65% ratio) most heavily. Expression matters for audience engagement.
- **CVs/Resumes:** Weight Typography, Whitespace, and Hierarchy most heavily. Consistency is critical for multi-page documents. Expression should be restrained to match professional context.
- **Dashboards:** Weight Layout, Hierarchy, and Consistency most heavily. Whitespace targets are tighter (25-35%). Craftsmanship matters for data credibility.
- **Marketing sites:** All 8 dimensions matter equally. Expression and Craftsmanship differentiate competitors.

## Examples

Working implementations in `examples/`:
- **`examples/evaluation-workflow.md`** -- Step-by-step evaluation of a fictional landing page with the 8-dimension scorecard format

## Review Checklist

When evaluating or scoring a visual design:

- [ ] Performed 50ms first impression assessment and recorded gut reaction
- [ ] Completed anti-pattern rapid screening (10-item checklist, <60 seconds)
- [ ] Scored Layout dimension (1-5) against grid and spacing criteria
- [ ] Scored Typography dimension (1-5) against scale, pairing, and readability criteria
- [ ] Scored Color dimension (1-5) against harmony, contrast, and distribution criteria
- [ ] Scored Whitespace dimension (1-5) against density, consistency, and separation criteria
- [ ] Scored Hierarchy dimension (1-5) against focal point, tiers, and scanning criteria
- [ ] Scored Consistency dimension (1-5) against design token and component uniformity criteria
- [ ] Scored Craftsmanship dimension (1-5) against pixel precision, image quality, and CLS criteria
- [ ] Scored Expression dimension (1-5) against brand personality and originality criteria
- [ ] Calculated total score and interpreted against the rating scale
- [ ] Identified lowest-scoring dimensions and created prioritized improvement plan
- [ ] Verified structural dimensions (1-5) are addressed before expressive dimensions (6-8)
