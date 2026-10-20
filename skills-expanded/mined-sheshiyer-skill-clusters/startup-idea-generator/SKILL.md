---
name: startup-idea-generator
description: "Generate startup ideas grounded in audience pain points, market gaps, and compelling business narratives. USE WHEN a task matches the Craft workspace workflow for startup-idea-generator."
cluster: growth-content
version: 1.0.0
origin: "craft-agent workspace"
---

# Startup Idea Generator

Use this skill when a user wants startup concepts in a category, for an audience, or around specific problems.

## Trigger Conditions
- User asks for startup ideas
- User wants business ideas for a niche
- User wants investor-ready concept framing

## Required Inputs
1. Category/industry
2. Target audience
3. Constraints (budget, tech capability, geography)
4. Desired model (B2B/B2C/marketplace/etc.)

## Workflow
1. **Pain-point scan**: identify unresolved audience needs.
2. **Idea generation**: produce multiple distinct startup concepts.
3. **Validation lens**: evaluate demand, feasibility, differentiation, monetization.
4. **Narrative shaping**: craft concise investor-facing concept pitch.
5. **Next steps**: propose validation experiments.

## Output Format
- 5 startup ideas with names and one-line thesis
- For each: problem, solution, target customer, business model, moat
- Quick validation plan for top 2 ideas

## Guardrails
- Ensure ideas are meaningfully different from each other.
- Avoid purely hype-driven concepts.
- State uncertainty and assumptions explicitly.
