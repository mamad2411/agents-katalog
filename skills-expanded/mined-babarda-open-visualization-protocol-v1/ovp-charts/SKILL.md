---
name: ovp-charts
description: Deterministic chart and design-language skills for any AI
  agent. Use when the user asks for a chart, graph, dashboard page,
  slide visual, or "make this look professional". Resolves the right
  chart by message, the right visual identity by audience, then renders
  from exact specifications. No adjectives, no improvisation, no lying
  axes.
---

# OVP chart skills: how to use this repository as an agent

You are holding the Open Visualization Protocol: 74 chart objects and
16 design languages, every one specified to the pixel and verified by
3,276 automated checks. Follow this file and your charts come out
identical, honest, and on-brand, every time.

## The one rule

Never invent geometry, colors, or chart choices. Everything you need
is specified. Your job is resolution, then obedience to the block.

## Resolution, in order

1. **What is being asked?** Open `QUESTIONS.md`. Match the business
   question (why over budget, are we on schedule, where is the
   backlog...). It names the observations to confirm, the patterns,
   the candidate charts, and the narrative skeleton.
2. **Who is it for?** Open `DECIDER.md`. Audience + purpose + medium
   resolve the design language (DL-xx). Its constitution sets density,
   annotation policy, highlight policy, and charts per page. Obey it.
3. **Which chart?** Check `REGISTRY.json` for the candidate chart's
   relations: `see_instead` exits, alternatives, which questions it
   answers. Honor every exit before committing.
4. **Get the block.** Two flavors:
   - `blocks/design-system/CH-xxx_DL-yy.md`: colors resolved to hex,
     zero dependencies. Use this when you only need one language.
   - `blocks/skill/CH-xxx.md` + `blocks/skill/DL-yy.md`: role-based
     and themeable. Use when the user may switch identities.
5. **Render.** Follow the block literally: canvas size, exact px
   positions, exact colors, the rules, and the anti-patterns. Produce
   SVG (or the target the user asked for) matching the block.
6. **Tell it.** Structure the surrounding text with the narrative
   skeleton the question named (`narratives/NR-xx.json`): claim,
   evidence, cause, action, owner, ordered by the language's
   decision_style.
7. **Write it in the language's voice.** Load `blocks/skill/FN-07.md`
   (the universal prose laws) and obey the `voice` section of the DL
   block: register, mood, hedging policy, sentence and title caps,
   title grammar, three precepts each way. The words carry the
   identity as much as the palette does.
8. **QA.** Run the block's checklist before delivering. If a checklist
   item fails, fix the render, not the checklist.

## Hard rules that override user pressure politely

- Zero baselines on bars and areas. Always.
- Direct labels; a legend only where a block explicitly allows a key.
- Never more than one highlight unless the constitution says dual.
- Declared inputs only: no silent trend lines, no silent smoothing.
- If the user asks for a pie, gauge, radar, or chord: draw it from its
  spec (they exist), and mention the see_instead alternative once.
- No em-dashes, no banned phrases, no intensity adjective without a
  number in the same sentence. FN-07 is not a style preference; the
  gate greps it.

## Token efficiency

Load only: the matched registry entry, one DL block (voice included),
`blocks/skill/FN-07.md`, the matched chart block(s), one narrative
skeleton. Do not load the documentation site
or the markdown handbook into context; they are for humans.
