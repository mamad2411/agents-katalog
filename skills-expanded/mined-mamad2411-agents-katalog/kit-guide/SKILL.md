---
name: kit-guide
description: Complete guide to the Unity 6 2D Mobile Game Agent Kit. Explains
  every skill, agent, command, the pipeline order, and how to get started.
  Use when the user asks for help, /guide, or wants to understand the kit.
---
# Unity 6 2D Mobile Game Agent Kit — User Guide

## What is this kit?
An AI agent kit for **OpenCode** that turns a one-line game idea into development-ready planning documents — GDD, player flow, technical design, UI system, level progression, and monetization design. It also includes Unity-specific knowledge skills for implementation guidance.

## Architecture
```
core/skills/          ← Portable brain (tool-agnostic know-how)
adapters/opencode/    ← Thin wiring for OpenCode
output/<game-slug>/   ← All generated documents land here
```

## Commands (available at the repo root)

| Command | What it does |
|---|---|
| `/interview` | Conversational interview about your game idea — explores genre, mechanics, audience, art, monetization. Can save as `game-intent.json`. Good starting point if you're unsure. |
| `/jumpstart <idea>` | Quick pipeline: idea → GDD + player flow. Use for a fast start. |
| `/blueprint <idea>` | Full pipeline: idea → GDD + flow + TDD + UI system + progression + monetization. Use for complete planning. |
| `/tdd` | Generate a Technical Design Document from the latest GDD in `output/`. |
| `/ui-system` | Generate a UI design system from the latest GDD and TDD. |
| `/progression` | Generate a level progression design from the latest GDD. |
| `/monetization` | Generate a monetization design from the latest GDD. |
| `/commit` | Generate a formatted git commit message from staged changes. Asks which format you want. |
| `/guide` | Shows this guide. |

## Recommended workflow
1. **Start with `/interview`** to flesh out your idea conversationally.
2. **Run `/blueprint`** with your refined idea to generate all planning docs.
3. **Review the docs** in `output/<game-slug>/`.
4. **Create your Unity project** in Unity Hub (2D URP template).
5. **Load Unity skills** as needed by asking Unity-specific questions (e.g., "how do I set up mobile input?").

## Pipeline (how documents flow through the kit)
```
idea
 └─▶ game-intent.json          (inferred by concept-clarifier)
       └─▶ gdd.md               (game design document)
             └─▶ flow.json       (player flow graph)
             │     └─▶ render_flow.py (deterministic, no LLM)
             │            └─▶ player-flow.md
             └─▶ tdd.md          (technical design document)
                   └─▶ ui-system.md   (reads gdd + tdd)
             └─▶ progression.md  (reads gdd)
             └─▶ monetization.md (reads gdd)
```

## Skills included

### Document skills (produce artifacts)
- **game-concept-clarifier** — idea → structured `game-intent.json`
- **game-design-document-authoring** — full GDD with mechanics specs, controls, accessibility
- **game-flow-graph** — schema-validated JSON flow graph + deterministic Python renderer
- **technical-design-document-authoring** — Unity 6 architecture, mobile optimization, build targets
- **game-ui-design-system** — mobile-first UI kit with WCAG contrast ratios
- **level-progression-design** — difficulty curves, unlock gates, level templates
- **monetization-design** — economy model, ad placement, IAP catalog, GDPR
- **validator** — read-only doc reviewer (returns PASS or GAPS)

### Interactive skills
- **game-idea-interviewer** — dynamic conversation about your game idea
- **commit-message-authoring** — generates git commit messages in your chosen format

### Unity knowledge skills (loaded on demand — no artifacts)
- **project-scaffold** — Unity 6 2D URP setup guide (you create the project in Unity Hub)
- **mobile-input-setup** — cross-platform touch + PC keyboard/mouse input
- **scene-state-management** — scene graph, loading screens, state machine
- **sprite-animation-workflow** — sprites, atlases, Animator, 2D Animation rigging
- **save-load-persistence** — JSON serialization, encryption, save slots
- **audio-management** — Audio Mixer, SFX pooling, music crossfade
- **performance-tuning** — draw calls, batching, profiling, memory
- **monetization-integration** — Unity Ads, AdMob, Unity IAP, GDPR
- **build-deployment** — Android + iOS build config, signing, CI/CD

## Quick start example
```
# Start with an interview
/interview

# Or jump straight in with a one-liner
/blueprint a 2D platformer where a cat collects stars and avoids dogs

# After coding, commit your changes
/commit

# When ready to build for mobile, ask:
"How do I configure build settings for Android?"
```
