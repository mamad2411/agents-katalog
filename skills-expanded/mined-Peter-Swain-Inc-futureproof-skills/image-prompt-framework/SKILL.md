---
name: image-prompt-framework
description: |
  Writes generator-tuned AI image prompts (Midjourney, DALL-E, Stable
  Diffusion XL, Flux, Ideogram) across seven structural layers —
  subject, environment, composition, lighting, style, color, technical
  parameters. Use when the user says "write me a Midjourney prompt",
  "give me a DALL-E prompt for this scene", "my image prompt isn't
  working — fix it", or "describe this visual for AI". For the broader
  creative direction document around an ad image use
  ad-creative-brief-generator; this skill outputs the raw prompt string.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="image-prompt-framework")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any established brand aesthetics, preferred generators, known style preferences, aspect ratios, and historical prompt patterns that produced strong results.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Visual concept**: What is the image meant to depict? (scene, subject, mood, narrative moment)
- **Target generator**: Which platform will render the prompt? (Midjourney v6.x, DALL·E 3, Stable Diffusion XL, Flux, Ideogram 2.x, other)
- **Use case & placement**: Where will the final image appear? (social media post, hero banner, product mockup, editorial illustration, pitch deck, ad creative, personal project)
- **ICA context** (if commercial): Who is the intended viewer? What emotional response or action should the image provoke?
- **Reference material** (optional): Any existing images, mood boards, brand guidelines, or previous prompts to build from?
- **Constraints**: Required aspect ratio, style prohibitions, brand colour palette, content restrictions, or mandatory elements?

If the user provides an existing prompt for refinement, ask what specifically fell short — composition, style accuracy, subject fidelity, mood, colour, or technical artefacts.

## Step 3: Do the Work

### 3A: Concept Decomposition

Break the user's visual concept into the **seven structural layers** of a high-fidelity image prompt:

| Layer | Definition | Example Fragment |
|---|---|---|
| **1. Subject** | Primary focal element with precise descriptors (age, pose, expression, material, scale) | "a weathered female cartographer in her 60s, examining a celestial map" |
| **2. Environment** | Setting, spatial context, depth cues | "inside a cluttered observatory tower, shelves of brass instruments receding into shadow" |
| **3. Composition** | Camera angle, framing, focal length, depth of field | "medium close-up, shot from slightly below, shallow depth of field, f/1.8" |
| **4. Lighting** | Light source, quality, direction, colour temperature, shadows | "warm candlelight from the left, rim light from a tall window, deep chiaroscuro shadows" |
| **5. Style & Medium** | Artistic tradition, rendering method, reference artists or movements | "oil painting style reminiscent of Vermeer, visible brushwork, muted Dutch Golden Age palette" |
| **6. Colour & Mood** | Dominant palette, emotional tone, atmospheric descriptors | "amber and deep indigo palette, contemplative mood, quiet gravitas" |
| **7. Technical Parameters** | Generator-specific syntax, aspect ratio, quality flags, model-specific tokens | "--ar 4:5 --style raw --s 250 --v 6.1" |

### 3B: Generator-Specific Optimisation

Apply platform-specific prompt engineering rules:

- **Midjourney**: Front-load subject, use `::` weight splits for emphasis control, leverage `--style`, `--chaos`, `--weird`, `--stylize` parameters strategically. Avoid over-prompting (diminishing returns beyond ~75 words in body).
- **DALL·E 3**: Use natural-language sentences rather than keyword stacking. Specify what the image IS, not what it ISN'T (positive framing). Leverage system-level style presets where applicable.
- **Stable Diffusion / Flux**: Structure as weighted token sequences, apply negative prompt layer to suppress common artefacts (extra limbs, watermarks, blurry). Include sampler and CFG guidance recommendations.
- **Ideogram**: Prioritise text-rendering instructions if typography is involved. Use style descriptors compatible with Ideogram's style engine.

### 3C: ICA & Brand Alignment (if commercial use)

Cross-reference against FutureProof context:
- Does the visual language match the ICA's aesthetic expectations and cultural references?
- Does the colour palette align with documented brand guidelines?
- Will the composition work at the specified placement dimensions (e.g., 1080×1350 for Instagram portrait, 1200×628 for LinkedIn link preview)?
- Does the mood reinforce the intended emotional positioning from prior sessions?

### 3D: Prompt Refinement Protocol

If the user submitted an existing prompt for improvement, diagnose against a **failure taxonomy**:

1. **Semantic drift** — ambiguous language causing the generator to misinterpret intent → replace with precise, unambiguous descriptors
2. **Style contamination** — conflicting style references cancelling each other → reduce to one dominant style anchor with one complementary modifier
3. **Composition collapse** — no spatial or framing instructions → inject explicit camera language and spatial relationships
4. **Keyword dilution** — too many competing descriptors reducing emphasis on the core subject → prune to essential terms, use weighting syntax
5. **Parameter mismatch** — technical flags working against the creative intent → recalibrate stylize, chaos, CFG, or sampler settings

## Step 4: Deliver Output

Produce a **Prompt Engineering Brief** containing:

### 4A: Primary Prompt (Ready to Paste)
The fully composed, generator-optimised prompt formatted for immediate use. If the target generator supports negative prompts, include that as a separate clearly labelled block.

### 4B: Prompt Architecture Breakdown
A table mapping each phrase in the prompt back to the seven structural layers, so the user understands WHY each element is included and can make informed modifications.

### 4C: Variant Suite
Three prompt variants exploring different creative directions:
- **Variant A — Faithful**: Closest interpretation of stated concept
- **Variant B — Elevated**: Same subject with a more dramatic or cinematic treatment
- **Variant C — Divergent**: An unexpected stylistic reinterpretation that may unlock stronger results

### 4D: Iteration Guidance
A ranked list of **3 modification levers** — specific words or parameters the user should adjust first if the output isn't right, with concrete before/after examples:
- "If the lighting feels too flat, replace `soft diffused light` with `single hard directional light from upper left, deep cast shadows`"
- "If the style is too photorealistic, prepend `gouache illustration style,` and reduce `--stylize` from 500 to 150"

### 4E: Negative Prompt (where applicable)
A curated negative prompt targeting the most common failure modes for this specific subject type and generator.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="image-prompt-framework", experiment={
  hypothesis: "Front-loading lighting descriptors before subject descriptors produces more atmospherically accurate outputs in Midjourney v6.1",
  variants: ["control: subject-first prompt structure", "variant: lighting-first prompt structure using identical descriptors"],
  measurement: "user satisfaction rating across next 10 prompt sessions; track which structure is selected for final use",
  expected_impact: "20% increase in first-generation acceptance rate, reducing average iterations from 4 to 3"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="image-prompt-framework",
  query="Latest prompt engineering techniques and syntax changes for Midjourney v6.1, DALL·E 3 turbo, Stable Diffusion 3.5, Flux 1.1 Pro, and Ideogram 2.0 — including undocumented parameters, optimal prompt length benchmarks, and community-tested style keywords with highest fidelity scores",
  reason="Image generator models update frequently with changed syntax, deprecated parameters, and new capabilities; prompt frameworks must reflect current model behaviour to avoid outdated techniques that degrade output quality"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="image-prompt-framework", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```