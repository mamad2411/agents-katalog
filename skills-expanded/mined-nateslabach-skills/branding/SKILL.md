---
name: branding
description: >-
  Builds personal brand assets using Seth Godin's frameworks: signature symbol,
  slogan, surprise (Purple Cow), salient idea, and signature story. Use when
  named (branding), or when the user asks for a brand symbol, slogan, tagline,
  Purple Cow, counterintuitive angle, core idea, brand story, or personal brand
  positioning.
---

# branding

Personal brand workshop. Five Godin-based prompts. Load only what the query needs.

## How to run

1. **Infer the step** from the user's ask (table below).
2. **Read that prompt file** and follow it exactly: ask the intake questions, wait, then execute steps, rules, and output shape.
3. If the ask is ambiguous or spans the whole brand system, ask which step they want (or whether to run more than one). Do not dump all five.
4. If they already answered intake questions earlier in the chat, reuse them. Do not re-ask unless something material is missing.
5. Carry forward prior outputs when chaining (e.g. salient idea → slogan). Do not invent a prior asset they never locked.

## Route map

| User signals | Load |
|---|---|
| symbol, icon, mark, visual identity, mid-scroll, logo-like mark | [prompts/signature-symbol.md](prompts/signature-symbol.md) |
| slogan, tagline, catchphrase, "what people repeat" | [prompts/signature-slogan.md](prompts/signature-slogan.md) |
| surprise, Purple Cow, counterintuitive, contrarian truth, scroll-stop idea | [prompts/signature-surprise.md](prompts/signature-surprise.md) |
| salient idea, core idea, positioning, "what I'm known for", one idea | [prompts/salient-idea.md](prompts/salient-idea.md) |
| brand story, origin story, narrative, about me story, 3-minute story | [prompts/signature-story.md](prompts/signature-story.md) |
| "full brand", "all of it", "Godin system", unclear | Ask which step(s); offer the five names |

## Operating rules

- Wait for intake answers before generating options. No skipping ahead.
- Prefer tables for scoring. Prefer concrete usage examples over abstract advice.
- One winner per step unless the prompt asks for options first.
- Banned fluff in slogans and copy matches each prompt's rules (especially slogan banned words).
- Soften nothing to be polite. Sharp and specific beats broad and safe.

## Sequence (optional)

If the user wants a full pass, run in this order and reuse locked answers:

1. Salient idea
2. Signature surprise
3. Signature slogan
4. Signature symbol
5. Signature story

That order sharpens the idea before packaging it. Only use when they ask for a full system or explicitly say continue to the next step.
