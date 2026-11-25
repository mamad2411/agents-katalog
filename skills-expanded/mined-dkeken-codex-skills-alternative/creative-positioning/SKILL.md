---
name: creative-positioning
description: Connect business positioning to a concrete visual language. Maps strategic positioning (category, differentiator, who-it's-for, who-it's-against) onto visual decisions — palette, type, imagery, tone — so the look reinforces the strategy. Use when the user says "positioning into visuals", "what should the brand look like given our strategy", "align visuals with positioning", or is moving from strategy to brand expression. Part of the Creative Production set.
---

# Creative — Positioning Explorer

Ensure the visual language is a deliberate expression of business positioning, not arbitrary taste. Every color, type, and imagery choice should be defensible by a strategic reason. This bridges the gap between "what we are in the market" and "what we look like".

## When to use
- Moving from strategy/positioning work into brand expression.
- The visuals feel disconnected from how the company wants to be seen.
- You need to justify aesthetic choices to founders/stakeholders with reasons, not opinions.
- Before `creative-moodboard`/`creative-explore` to seed them with strategic constraints.

## When NOT to use
- Positioning is undefined — that's a strategy problem, not a visual one; surface it first.
- You just need options to look at fast → `creative-explore`.
- Merchandising a specific offer → `creative-offer`.

## Inputs (ask only what's missing)
- **Category** + how they want to be seen within it.
- **Core differentiator** — the one thing that's true of them and not competitors.
- **Who it's FOR** and **who it's AGAINST** (the foil — the incumbent/alternative they beat).
- **Price/quality tier**.

## Workflow
1. **Write the positioning statement**: "For {audience}, {brand} is the {category} that {differentiator}, unlike {foil}."
2. **Derive visual implications** from each part. Premium-vs-cheap → restraint, whitespace, craft cues. Approachable-vs-intimidating → warmth, rounded forms, human imagery. Each rule traces to a positioning reason.
3. **Produce a visual language spec**: palette logic, type logic, imagery rules, tone, and explicit **do-nots** (what would accidentally signal the foil's positioning).
4. **Generate 2-3 proof images** with your image tool showing the positioning made visible. Save to `./creative/positioning/<NN>.png`.
5. **Pass the spec forward** as hard constraints to `creative-moodboard`/`creative-explore`.

## Worked example
A project-management tool positioned against "bloated enterprise suites".
```
positioning: "For small teams, Tako is the project tool that stays out of your
way, unlike heavyweight enterprise suites."

visual implications:
- palette: 1 accent + lots of neutral (because "stays out of the way" → restraint;
  a rainbow UI would signal the bloated foil)
- type: one humanist sans, generous spacing (calm, not dense dashboards)
- imagery: real small-team moments, not stock boardrooms (audience = small teams)
- tone: plain, confident, short
- DO NOT: dense feature-grid heroes, navy "enterprise" gradients, jargon — all read as the foil
proof: [./creative/positioning/01-restraint.png][./creative/positioning/02-team.png]
```

## Quality bar
- A one-sentence positioning statement exists and the user agrees with it.
- Every visual rule has a "because {positioning reason}" — no orphan aesthetic choices.
- The do-not list explicitly names what would signal the wrong position.
- Proof images visibly embody the position (a viewer could infer the strategy from them).

## Common pitfalls
- **Taste-for-taste's-sake** — a rule with no positioning reason doesn't belong here.
- **Inventing the strategy** — extract it from the user; if it's missing, say so and stop.
- **Ignoring the foil** — positioning is relational; the do-nots come from what the foil looks like.
- **Vague implications** — "modern and clean" isn't a rule; "single accent, 60% whitespace" is.

## Handoff
Visual language spec → `creative-moodboard` (expand to territories) or `creative-explore` (concrete directions within the spec). The spec is a constraint, not a suggestion, for everything downstream.

## Tooling
Proof images need a text-to-image tool. Without one, deliver the positioning statement + visual language spec + do-nots; that alone is a usable strategic artifact.
