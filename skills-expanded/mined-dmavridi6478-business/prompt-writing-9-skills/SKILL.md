---
name: prompt-writing-9-skills
description: A 9-step chain of Claude skills that turns a messy idea into a ready-to-use prompt - Prompt Maker (/prompt-master), Grill Me (/grill-me), How To (/how-to), Optimizer for the current Opus model (/opus-polish), Fable Prompter (/fable-polish), Personal Voice (/personal-voice), Anti-AI (/anti-ai), Write a Skill (/write-a-skill) and Hand Off (/handoff). Use when the user has a vague idea and wants a clean task spec, or wants to chain prompt-improvement steps. Source appmillers infographic "9 Claude Skills that write your prompts for you" (Batch 102). The slide shows names and one-line purposes only; the command bodies here are written from those purposes, not copied from the author.
---

# 9 skills that write your prompts

Flow on the slide: messy idea -> 01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08 -> 09 -> "ready-to-use prompt" with a clear goal, full context and your voice. "Use them in order, mix and match, or loop back."

| # | Slide name and command | Purpose on slide | Here |
|---|---|---|---|
| 01 | Prompt Maker `/prompt-master` | Brain dump in, clean task spec out | new command `/prompt-master` |
| 02 | Grill Me `/grill-me` | Asks questions until nothing is vague | new command `/grill-me` |
| 03 | How To `/how-to` | Maps the steps you do not know yet | already installed: `/how-to` |
| 04 | Optimizer 4.8 `/48` | Polishes your prompt for Opus 4.8 | new `/opus-polish` (version-agnostic) |
| 05 | Fable Prompter `/fable` | Same polish, for Fable 5 | new `/fable-polish` |
| 06 | Personal Voice `/personal-voice` | Tunes it to sound like you | new `/personal-voice` (uses `/voice-builder` profile) |
| 07 | Anti-AI `/anti-ai` | Strips the AI tells from the draft | new `/anti-ai` (uses `avoid-ai-writing`, `humanizer`) |
| 08 | Write a Skill `/write-a-skill` | Bottles it as a reusable skill | new `/write-a-skill` (uses `skill-creator`) |
| 09 | Hand Off `/handoff` | Creates a handoff doc to start your next chat | already installed: `/handoff` |

Version note: the slide says "Opus 4.8" and "Fable 5". The models named in this environment are Opus 5.5, Sonnet 5.5 and Fable 5.1, so `/opus-polish` and `/fable-polish` do not hard-code a version; they tell the target model what the prompt needs rather than relying on version-specific quirks. [Guessing] that the author's skills differ in detail from these; the slide does not show their contents.

## Minimal chain
`/prompt-master <idea>` -> answer `/grill-me` -> `/opus-polish` (or `/fable-polish`) -> `/anti-ai` on any text the prompt will produce -> `/write-a-skill` only if you will reuse it 3+ times.
