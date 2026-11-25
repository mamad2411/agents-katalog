---
name: outreach-writer
description: >
  Write personalized first-contact copy (one email + one LinkedIn message per company) for
  prospect companies, using Syrto company data and a user-provided value proposition. Copy
  only: nothing is sent, scheduled or loaded into a campaign tool. Use whenever the user says
  "scrivi i messaggi per questi prospect", "genera le email di primo contatto", "email a
  freddo", "messaggio LinkedIn per [azienda]", "messaggio personalizzato", "crea messaggi",
  "outreach copy", "write outreach", "cold email", or wants tailored messages for a set of
  prospect companies. Typically runs after prospects-scout / company-analysis have produced
  the company list. Not for replies to an existing thread or emails unrelated to prospecting.
metadata:
  version: "1.0.0"
---

# Outreach Writer

## Suite integration (read first)
Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`). Reuse any upstream `SYRTO-HANDOFF` before calling Syrto; emit one when you feed another skill.

Generate one personalized email and one LinkedIn message per target company, tailored to what that company actually does. Output is copy only: this skill never sends, schedules or drafts the messages in a mail, LinkedIn, CRM or campaign tool, even when one is connected; the user sends them.

## Inputs
1. **Company list** — from an upstream `SYRTO-HANDOFF` (preferred: reuse the anagraphic already gathered), an uploaded file, or the user's message. For each company you need its real activity, size and market — read from the handoff, else the company profile.
2. **Value proposition** — the angle to push. Ask the user if it isn't given (or take what they sell from the commercial context, core §3).
3. **Reference client to cite (optional)** — a satisfied client the message can name as proof. This is a **user input or from the saved portfolio**. Never invent one; if none is provided, write the message without a name-drop. Any result you attribute to it (a percentage, time saved) must come from the user too; the figures in the examples below are placeholders.
4. **Channels** — which companies also get a LinkedIn message (default: both).
5. **Recipients (optional)** - names come only from the user, their CRM or their file; otherwise write to `[Nome]` and let the user fill it in. This skill does not look people up, in Syrto or on the web, and does not buy person contacts (paid): a purchase spends the organization's credits, so it happens only on a separate, explicit request, after naming the person and the credit cost and getting a yes.

## Message format rules
These are the house style: apply them to every message unless the user asks for something different in this conversation.

**Opening greeting (email and LinkedIn).** Start with a time-of-day greeting followed by the first name: use "Buongiorno [Nome]," in the morning and "Buonasera [Nome]," from the afternoon on. The time is when the message will be sent; when you don't know it, use "Buongiorno [Nome],". Write it as plain text — use the neutral placeholder `[Nome]` where the first name goes.

**Email closing.** End with:
```
Un caro saluto,
[Firma]
```

**LinkedIn closing.** End with: `Un caro saluto, [Firma]`

Use neutral placeholders throughout — `[Nome]`, `[Firma]`, `[Azienda]` — never templating syntax.

### Style rules
- **Short and direct.** Email body (between greeting and closing) is 3–5 sentences max, two short paragraphs.
- **Never use em dashes.** Use commas or periods.
- **Never use question marks when proposing a meeting.** "Posso proporti un incontro martedì alle 9." not "Ti va martedì alle 9?"
- **Never use English words** where an Italian equivalent exists (no "nice-to-have", "game-changer", "deep dive", "follow-up").
- **Never use colons to introduce a concept.** Write complete sentences.
- **Always propose a specific day and time.** Rotate days (lunedì–venerdì). Only orario 9 or 14. Never repeat the same day+time for consecutive companies.
- **Cite the reference client naturally** when one is provided, as proof of a result — not as a bare customer list. If none is provided, skip the name-drop.
- **Human tone.** Write like someone who genuinely knows what the company does. No buzzwords, no hype.
- **Company-specific hook.** The first sentence after the greeting must reference something specific about THAT company: what they do, their size, their market — drawn from Syrto anagraphic data.

### Email structure
```
Buongiorno/Buonasera [Nome],

[1-2 sentences: company-specific hook from activity + size]
[1-2 sentences: the value proposition, connected to their reality]
[1 sentence: reference-client proof if available + a specific day and time]

Un caro saluto,
[Firma]
```

### LinkedIn structure
Shorter — body under ~300 characters, same rules compressed.
```
Buongiorno/Buonasera [Nome], [company hook + value prop + reference proof + meeting proposal, 2-3 sentences max]

Un caro saluto, [Firma]
```

## Workflow
1. **Group by company.** All recipients at the same company share one email and one LinkedIn message.
2. **Generate per company.** For each unique company produce the email body and the LinkedIn body, built from its Syrto activity/size + the value proposition.
3. **Rotate meeting slots.** Cycle days lunedì→venerdì, alternate 9 and 14, never the same day+time twice in a row.
4. **Assemble & review.** Present the messages (email + LinkedIn per company) to the user, showing 2-3 examples in chat for feedback on tone before finalizing. Adjust on request.

## Output
Email copy + LinkedIn copy per company, presented for review (and exportable to a file on request). For more than a handful of companies, the full set goes in a file per core §5 (one row per company), with the 2-3 examples in chat. No campaign creation, no external push.

## Examples (de-branded — reference client is a placeholder)

**Consulting firm — VP "gestire più progetti senza aumentare le risorse":**
con circa 120 persone su trasformazione strategica, IT e supply chain, immagino che i team spendano parecchio tempo a costruire analisi di mercato e competitive per le offerte. Noi forniamo quei dati pronti in minuti, scenario competitivo, benchmark, posizionamento. Se ti va di approfondire come [cliente di riferimento] ha ridotto il tempo di questi processi di [risultato], posso proporti un incontro martedì alle 14.

**Corporate finance — VP "trova aziende perfette per i mandati":**
so che lavorate su M&A e raccolta di capitale internazionale. Trovare i target giusti per i mandati, soprattutto nelle nicchie italiane, è spesso il pezzo più lungo del processo. Noi identifichiamo aziende per attività reale, non per codice ATECO, e mappiamo chi è più predisposto a operazioni straordinarie. Se ti va di vedere come [cliente di riferimento] arriva prima sulle opportunità migliori, posso proporti un incontro mercoledì alle 9.
