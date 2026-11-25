---
name: ai-app-stack-2026
description: Reference map of the AI app categories from "Which AI apps do I actually need in 2026?" (@jeanbbttyct) - ten categories (text to speech, writing, marketing, image generators, coding, presentations, video generators, productivity, research, design) with the example tools and what each does, plus which categories this repo already covers with skills, commands or connectors. Use when choosing AI tools for a task, auditing an AI tool stack for overlap, or answering "which tool for X". Tool lists are the creator's picks, not rankings. Source @jeanbbttyct (Batch 101).
---

# AI apps by category (2026 shortlist)

The creator's answer to "which AI apps do I actually need": one or two per job, not everything. These are examples named on the slides, with their one-line descriptions.

| # | Category | Tools shown | What they do |
|---|---|---|---|
| 1 | Text to speech | Speechify, NaturalReader, Animaker, ElevenLabs | natural voices from text; read documents aloud; voiceovers for video |
| 2 | Writing | Claude, Grammarly, DeepL, Gemini | draft and edit; grammar and tone; translation |
| 3 | Marketing | Buffer, Pixelcut, Gemini, Captions | schedule posts; product images; marketing copy; captioned social video |
| 4 | Image generators | Pixelcut, Picsart, Fotor, Dreamina | product photos; AI editing; graphics; images from text |
| 5 | Coding | Base44, DeepSeek, Cursor, ChatGPT | apps from descriptions; code help and debugging; AI code editor |
| 6 | AI presentation | Canva, Gemini, Gamma, Claude | slide layouts; outlines; full decks from a prompt; structuring content |
| 7 | Video generators | Dreamina | video from text; animate images; apply motion from a reference clip; edit videos |
| 8 | Productivity | Otter, Fireflies, Krisp, Shortwave | transcribe meetings; summarise notes; remove call noise; AI email |
| 9 | Research | ChatGPT, Gemini, ChatPDF, Perplexity | answers; gather sources; PDF summaries; sourced answers |
| 10 | Design | Photoroom, SVGTrace, Canva, Adobe Firefly | background removal; raster to vector; templates; generated images |

## What this repo already covers

| Need | Here |
|---|---|
| Writing and editing | Claude itself, `humanizer`, `/plain-human`, `avoid-ai-writing` |
| Presentations | `pptx`, `frontend-slides`, `premium-html-presentation`; Canva and Gamma connectors are connected |
| Research | `research-skeptic`, `deep-research`, the Consensus connector and the Exa MCP server registered in `.mcp.json` |
| Design | `design-templates`, `theme-factory`; Canva, Figma and Adobe connectors |
| Meetings | Fireflies connector (connected); `meeting-notes-processor` |
| Scheduling posts | Typefully and AgentOpus connectors; OS agents only draft |
| Voice and video | `video`, `hyperframes`, `remotion-video-creation`, `kesha-voice-kit`; Higgsfield connector |

Not covered: Speechify, NaturalReader, Buffer, Pixelcut, Picsart, Fotor, Otter, Krisp, Shortwave, ChatPDF (no connector here).

## How to use it

When asked for a tool, name one or two per category and say whether a connector or skill here already does the job before suggesting a new subscription. Prices and features change; check the vendor page.
