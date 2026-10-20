# Agent Swarm Web Design

Use Claude's Agent Swarm to build production-quality websites — Claude does the design research and heavy lifting. Workflow by @ai.with.andrew.

## How It Works

Instead of prompting Claude once, you run an **Agent Swarm** — multiple Claude agents collaborating:
1. One agent researches design references (real websites)
2. One agent extracts the design language
3. One agent builds the site using that language

## Step-by-Step

### Step 1 — Feed Claude Design References

Find 2–3 real websites with the aesthetic you want, then tell Claude:

```
I want to build a website with this visual style.
Reference sites:
- [URL 1] — note what you like about it
- [URL 2] — note what you like about it

Extract the design language: color palette, typography, layout patterns, spacing, component styles.
```

### Step 2 — Define Design Tokens

Tell Claude the exact design primitives to use:

```
Build this website using:
- Typography: Inter (geometric sans)
- Color: Purple gradient (#7C3AED → #4F46E5) as primary
- Cards: layered cards-on-cards with subtle shadows
- Buttons: pill shape, gradient fill
- Layout: full-width hero, constrained content (max-width: 1200px)
```

### Step 3 — Launch the Swarm

```
Act as an agent swarm. Assign these roles:
- Agent 1 (Designer): Define the full design system from the references above
- Agent 2 (Builder): Build every section as clean HTML + Tailwind CSS
- Agent 3 (Reviewer): Check each section against the design system, flag anything off

Build the full [page type] page. Start with Agent 1.
```

### Step 4 — Iterate Section by Section

```
Now build the [hero / features / pricing / testimonials / footer] section.
Match the design tokens exactly. Use real placeholder content.
```

## Design Reference Prompt

```
You are a senior web designer. Analyse the visual design of [URL or description].
Extract:
1. Color palette (hex values)
2. Font choices and weights
3. Layout grid and spacing rhythm
4. Component patterns (cards, buttons, nav)
5. Mood in 3 words

Then build a matching design token file as CSS custom properties.
```

## Example Design Languages

| Style | Typography | Primary Color | Layout |
|-------|-----------|---------------|--------|
| SaaS dark | Inter | Purple gradient | Dark bg, glassy cards |
| Agency editorial | Neue Haas Grotesk | Sand/gold | Asymmetric, large type |
| Luxury brand | Cormorant | Black + cream | Wide margins, serif |
| Developer tool | JetBrains Mono | Green/cyan | Terminal-inspired |
