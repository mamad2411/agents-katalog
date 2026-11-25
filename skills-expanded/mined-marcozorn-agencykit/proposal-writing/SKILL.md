---
name: proposal-writing
version: 1.0.0
description: Generate a client proposal from scope, budget and past project references. Draws from scope/outcome example pairs when provided.
author: MarcoZorn
license: MIT
tags: [agency, proposal, client, sales]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# proposal-writing

## When to use this skill
**EN triggers:** "proposal", "write a proposal", "client proposal", "new pitch", "scope document"
**IT triggers:** "proposta", "scrivi una proposta", "pitch", "documento di scopo"

## Inputs required
Before generating, ask:
1. Client name and industry
2. Service scope (what will be delivered)
3. Budget range (or "unknown")
4. Deadline for the proposal
5. Do you have past proposals or scope/outcome examples to reference? (optional but recommended)

## Output format
Produces two blocks:

**CLIENT-FACING PROPOSAL**
- Executive summary (2-3 sentences, outcome-focused)
- Scope of work (phased, specific)
- Deliverables list
- Timeline
- Investment (pricing table)
- Payment terms (default: 50% upfront, 50% on delivery)
- Revision policy (2 included, extras billed separately)
- Next steps / CTA

**INTERNAL NOTE** (do not send)
- Margin estimate if budget provided
- Assumptions made
- Risks flagged

## Human gate
This output is a draft. Review all pricing, scope, and commitment language before sending to the client. Do not send automatically.

## Brand voice
If a BRAND.md file exists in `.claude/skills/proposal-writing/` or `.claude/brand/`, read it before generating and apply its tone, terminology, and examples throughout the proposal.

## Past proposal reference
If the user provides past proposals or scope/outcome example pairs, extract:
- Tone and structure patterns
- Pricing conventions
- How scope was framed
Apply these patterns to the new proposal without copying verbatim.

## Edge cases
- If budget is unknown: produce the proposal with a [TBD] placeholder and a note to fill before sending
- If scope is vague: ask one clarifying question before proceeding
- If past examples conflict: use the most recent one as primary reference

---

## 🇮🇹 Versione italiana

### Quando usare questa skill
**Frasi trigger:** "proposta", "scrivi una proposta", "pitch cliente", "documento di scopo"

### Input necessari
Prima di generare, chiedi:
1. Nome e settore del cliente
2. Scope del servizio
3. Budget indicativo (o "non definito")
4. Deadline per la proposta
5. Hai proposte precedenti o esempi scope/outcome da usare come riferimento? (opzionale ma consigliato)

### Output
**PROPOSTA PER IL CLIENTE** — sommario esecutivo, scope, deliverable, timeline, investimento, termini di pagamento, politica revisioni, prossimi passi.
**NOTA INTERNA** — stima margine, assunzioni, rischi.

### Nota importante
L'output è una bozza. Verifica sempre prezzi, scope e linguaggio contrattuale prima di inviare.
