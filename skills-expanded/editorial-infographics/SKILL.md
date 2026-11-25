---
name: editorial-infographics
description: Create original, evidence-led editorial infographics and social graphics that avoid generic AI aesthetics. Use for infographics, news cards, data stories, Pinterest pins, social carousels, visual explainers, diagrams, or when a graphic must explain, prove, compare, map, or humanize an idea.
---

# Editorial Infographics

Create visuals that communicate before they decorate. The output should feel art-directed, not generated from a generic social template.

## Non-negotiable outcome

Every visual must perform one primary job:

1. **Explain** a process or mechanism.
2. **Prove** a claim with a real number, quote, screenshot, or source.
3. **Compare** two states with an honest common scale.
4. **Map** relationships, hierarchy, overlap, or flow.
5. **Humanize** an abstract idea with a relevant person, object, or situation.

If the visual only restates the post title, stop and redesign it.

## Workflow

### 1. Build an evidence pack

Collect the source text and any real data, screenshots, quotes, product UI, photos, dates, or documents that support it. Mark each claim as `verified`, `inference`, or `unknown`.

Never invent statistics, interfaces, quotes, sources, or product behavior. Capture real UI instead of generating fake UI.

### 2. Write the one-sentence takeaway

Complete this sentence:

> After seeing this image for five seconds, the viewer should understand that …

One image gets one takeaway. Split a dense idea into a carousel or series.

### 3. Classify the information topology

Choose structure before style:

- progression or convergence → `convergence`
- why / how / what or nested scope → `concentric`
- levels, maturity, risk, or containment → `layers`
- shared causes, systems, or intersections → `overlap`
- before/after → `binary-comparison`
- a measured trend → `annotated-chart`
- product proof → `real-screenshot`

Read [layout families](references/layout-families.md) before selecting a composition.

### 4. Art-direct the visual

Use [the design language](references/design-language.md). Start from a quiet editorial canvas, one dominant diagram, one accent color, and a deliberate asymmetry. Typography and geometry should carry the design.

Do not imitate a reference literally. Extract its hierarchy, rhythm, spatial metaphor, density, and contrast, then create a new composition.

### 5. Choose a production method

Prefer the method with the highest truth and control:

1. Real screenshot or photo with restrained annotation.
2. Deterministic vector, HTML/CSS, chart, or diagram for exact data and text.
3. AI-generated illustration only when a metaphor genuinely adds meaning.
4. Hybrid: generated background or object plus deterministic type and labels.

Do not ask an image model to invent dense body copy or precise charts. Render text and data deterministically.

### 6. Adapt to the platform

Create a native composition for each aspect ratio. Never stretch one master file. Read [platform formats](references/platforms.md).

If the asset ships with social copy, run the [publishing transport gate](references/publishing-gate.md). Paragraph spacing must survive the scheduler: visible `\\n`, raw HTML, collapsed paragraphs, or duplicated queue items are release blockers.

### 7. Run the anti-slop gate

Score the piece with [quality gate](references/quality-gate.md). A visual cannot ship if:

- the visual job is unclear;
- its main claim lacks evidence or is framed as fact without support;
- it repeats the same layout as another item in the batch;
- the title is the only useful information;
- it contains fake UI, fake data, illegible text, or decorative complexity;
- it resembles a generic AI template more than a specific editorial decision.
- the scheduled copy contains literal escape sequences, unexpected HTML, or broken paragraph spacing.

### 8. Preserve a receipt

Save the brief, sources, final copy, dimensions, production method, file hash, and QA score. When publishing a batch, record which layout family each asset used.

## Batch diversity rule

For any batch of four or more visuals:

- use at least three layout families;
- no more than two assets may share the same dominant composition;
- alternate density and scale;
- include at least one evidence-led visual;
- include at least one visual with no card grid;
- inspect the batch as thumbnails before publishing.

## Required output

Deliver:

1. Evidence pack and source status.
2. One-sentence takeaway.
3. Chosen visual job and layout family.
4. Platform dimensions.
5. Final overlay copy.
6. Production method and reproducible prompt or spec.
7. Final asset path.
8. QA score and any limitations.

Use [the visual brief template](templates/visual-brief.md) as the working record.
