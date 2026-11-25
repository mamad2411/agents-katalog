---
name: Soul
description: Inject a distinct personality, tone of voice, and custom behavior guidelines into your AI assistant to make it high-agency, witty, and direct.
tagline: Inject custom personas and tone-of-voice profiles into your AI assistant.
whenToUse: Use this skill to customize your AI assistant's communication guidelines, personality, opinions, and tone of voice for a more human, high-agency, and engaging interaction.
license: MIT
category: skill
tags: ["persona", "assistant-behavior", "tone-of-voice", "customization"]
---

# Soul

Transform your AI assistant from a dry, sycophantic corporate drone into a highly competent, witty, and opinionated development partner.

## Features

- **High-Agency Personality**: Equips your assistant with strong, direct takes rather than dry "it depends" hedging.
- **Fluff Elimination**: Strips out polite boilerplate phrases like "Great question!" or "I'd be happy to help" to deliver answers instantly.
- **Natural Wit & Tone**: Adjusts communication style to support subtle humor, direct warnings about bad ideas, and natural phrasing.
- **Custom Profile Library**: Browse custom persona files under the `ppl/` folder (such as `steipete.md` for Peter Steinberger style).

## Workflows

### 1. View Available Personas
Browse the `ppl/` directory inside this skill to view different personality templates. Each template lists specific behavioral overrides, rules, and example adjustments.

### 2. Apply Custom Soul to Your Workspace
To configure your assistant to use a specific persona (e.g. `steipete.md`):
1. Read the profile contents of the target file under `ppl/`.
2. Append the rules to your global instructions, system prompt, or your local `.clauderc` file.
3. Restart or refresh your assistant session to activate the persona.