---
name: design-thinking-partner
description: >
  Use AI as a pre-design creative partner before opening Figma/Canva/Photoshop.
  Generates brand names, moodboard concepts, creative direction, typography pairings,
  brand voice guides, and logo concept directions for a design project. Trigger when
  the user wants to think through branding or visual direction faster, not just generate images.
metadata:
  laniameda:
    departments: ['Marketing', 'Design']
    purposes: ['Research', 'Branding', 'Pre-Production']
    tags: ['design', 'branding', 'creative-direction', 'gemini', 'prompting']
    status: active
    depends_on: []
    replaces: []
---

# Design Thinking Partner

## Purpose

Use AI the **right way for design thinking**:
- not only to generate images
- but to act like a **creative partner before execution**

This skill is for the phase **before visual production**:
- naming
- creative direction
- moodboard planning
- typography direction
- brand voice
- logo direction

## When to Use

Trigger this skill when the user wants to:
- brainstorm a new brand/system visually
- define brand direction before designing
- accelerate concept development
- turn a rough brief into clear design inputs
- use Gemini/LLMs as a strategic design copilot

Typical asks:
- “help me think through this brand”
- “give me creative direction prompts”
- “generate design prompts for branding”
- “turn this design idea into a system”
- “help me define the vibe before I design”

## What This Skill Produces

Depending on the request, produce one or more of:
1. **brand name options**
2. **moodboard concept**
3. **creative direction brief**
4. **typography pairing directions**
5. **brand voice guide**
6. **logo concept directions**

## Inputs

Ask for / infer these when needed:
- `industry`
- `audience`
- `tone`
- `brand name` (if it exists)
- `brand type`
- `project goal`
- `visual references` (optional)

If missing, use `[BLANK]` placeholders instead of inventing specifics.

## Output Standard

Default output must be:
1. **fast result first**
2. **structured**
3. **copy-pasteable prompts**
4. **useful before design execution**

Do **not** output generic branding theory.
Do **not** over-explain.
Do **not** drift into long strategy essays unless explicitly asked.

## Core Workflow

### 1. Clarify the design stage
Identify which of these the user actually needs:
- naming
- moodboard
- creative direction
- typography
- brand voice
- logo concepts

### 2. Select the minimum useful modules
Do not dump all modules by default.
Return only what is relevant.

### 3. Generate structured prompt(s)
Use the prompt bank below.
Adapt placeholders to the user’s context.

### 4. Add execution-ready notes
For each prompt, include:
- what it is for
- when to use it
- what to do with the output next

### 5. Convert output into design inputs
Where useful, transform AI output into:
- a concise brief
- moodboard ingredients
- type direction
- logo direction list
- brand voice bullets

## Prompt Bank

### 1) Brand Name Generator
**Use when:** naming a new brand/product/studio

```text
Act as a branding expert. Generate 20 unique brand name ideas for a [industry] company that targets [audience]. The names should feel [tone: modern, premium, playful, futuristic], be easy to pronounce, and suitable for a global brand.
```

**Next step:** shortlist 5 → test tone fit → test domain/username availability.

### 2) Moodboard Concept Generator
**Use when:** defining visual atmosphere before making assets

```text
Act as a creative director. Create a detailed moodboard concept for a brand in the [industry] space targeting [audience]. Include color palette ideas, textures, visual references, lighting style, photography direction, and overall emotional tone.
```

**Next step:** turn output into Pinterest / Are.na / gallery collection inputs.

### 3) Creative Direction Prompt
**Use when:** defining the big visual idea behind a brand/project

```text
Act as a senior creative director. Create a strong creative direction for a brand in the [industry] industry. Include the core visual theme, art direction style, layout inspiration, imagery style, and how the brand should feel visually.
```

**Next step:** convert into design brief / direction board / `Design.md` seed.

### 4) Typography Pairing Ideas
**Use when:** choosing a font direction fast

```text
Act as a typography expert. Suggest 10 strong font pairings for a [brand type] brand. Include one primary headline font and one supporting body font, and explain why the combination works.
```

**Next step:** shortlist 3 pairs → test in hero/header/card UI.

### 5) Brand Voice Writing
**Use when:** aligning messaging with visual identity

```text
Act as a brand strategist. Create a brand voice guide for a [industry] brand targeting [audience]. Include tone of voice, personality traits, communication style, and example brand messaging.
```

**Next step:** use for landing page copy, captions, social content, product UI copy.

### 6) Logo Concept Generator
**Use when:** exploring symbols before sketching

```text
Act as a professional logo designer. Generate 10 logo concept ideas for a brand called [brand name] in the [industry] industry. Describe the symbolism, style, and visual concept behind each idea.
```

**Next step:** choose 2–3 concepts → sketch / vector / generate references.

## Recommended Deliverable Formats

### Format A — Prompt Pack
Use when user wants prompts only.

```markdown
## Prompt Pack

### [Module Name]
**Use for:** ...
**Prompt:**
```text
...
```
**Next:** ...
```

### Format B — Pre-Design Brief
Use when user wants something more operational.

```markdown
## Pre-Design Brief
- Brand / project:
- Audience:
- Tone:
- Core visual direction:
- Moodboard ingredients:
- Typography direction:
- Brand voice summary:
- Logo concept directions:
```

### Format C — Design Thinking Sprint
Use when user wants a full rapid ideation pass.

```markdown
## Design Thinking Sprint
1. naming
2. moodboard
3. creative direction
4. typography
5. voice
6. logo concepts
7. next execution steps
```

## Hard Rules

- Use AI as a **thinking partner**, not just an image generator.
- Stay in the **pre-design / concept / direction** layer unless asked to execute visuals.
- Keep outputs tactical and reusable.
- Prefer prompts + structured outputs over generic explanation.
- If the user gives a concrete brand/project, fill prompts with real context.
- If context is missing, preserve `[BLANK]` placeholders instead of guessing.

## Source

Derived from Instagram carousel by **@gent.huruglica**:
`https://www.instagram.com/p/DVizw0yCOHd/`

Key extracted modules from slides:
- Brand Name Generator
- Moodboard Concept Generator
- Creative Direction Prompts
- Typography Pairing Ideas
- Brand Voice Writing
- Logo Concept Generator
