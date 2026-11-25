---
name: post-call-followup
description: "Turn a sales call into a follow-up email, clear next steps, and a clean CRM update. Use after a discovery, demo, or any customer call. Triggers on: follow up email, post call, recap email, log this call, update the deal."
---

# Post-Call Follow-Up

## Purpose
Turn a just-finished call into three artifacts: a recap email the buyer actually
wants, clear mutual next steps, and a CRM update that keeps the deal honest.

## Inputs
- What was discussed (transcript, notes, or your recollection)
- Who was on the call and their role
- The deal's current stage and what you're trying to advance

## Method
1. **Extract the spine of the call.** Work this checklist so nothing gets dropped:
   - **Pains named** — the problems the buyer stated, in their words.
   - **Value landed** — which of your points they reacted to (and which fell flat).
   - **Objections raised** — concerns, hesitations, and who raised them.
   - **Commitments** — *both* sides: what you owe, what they owe. (See the rule below.)
   - **Next step** — the single agreed action, with an owner and a date.
   - **People** — anyone new mentioned, their role, and whether they're for/against.
2. **Draft the recap email in the buyer's language** — lead with their stated problem,
   mirror their words, make the next step a single clear ask. Keep it under 150 words.
3. **Write next steps as `owner + action + date`.** No orphaned tasks; if a step has no
   date, it isn't a commitment yet — chase the date.
4. **Produce the CRM update.** Map the call to concrete fields, and flag — don't
   silently overwrite — anything the call *contradicts*:

   | CRM field | Update from the call |
   |---|---|
   | Stage | Advance only if the exit criteria were actually met; otherwise hold + note why. |
   | Next step / next step date | The agreed action + date from step 3. |
   | Close date | Adjust only if the buyer gave a real date signal; flag if it now looks unrealistic. |
   | MEDDPICC slots | Update Champion / Economic buyer / Metrics / Decision process as the call revealed them. |
   | Contacts / roles | Add new stakeholders; update influence/sentiment. |
   | ⚠️ Contradictions | List any field the call disproves (e.g. "stage = Negotiation but no economic buyer engaged") for the rep to resolve. |

**Good vs bad recap:** a good recap reflects *their* problem and one clear next step a
busy buyer can say yes to in five seconds. A bad recap is a feature recap in seller
language with a vague "let me know your thoughts" close.

**Recap email template:**
```
Subject: <their problem> — next steps

Hi <name>,

Thanks for the time today. To recap what I heard: <their stated problem, their words>.

What we agreed:
- <value point that landed>
- Next step: <single clear ask> by <date>

<one-line close>
<signature>
```

**Both-sided commitments rule:** capture what *you* owe and what *they* owe. A recap
with only your commitments is a to-do list, not a mutual plan.

## Tool binding
This skill works from raw notes alone. It gets sharper when connected to your stack —
strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the call directly instead of
asking the user to paste notes:
- `ontology_resolve("deal", id, expand=["meetings","commitments","objections","stakeholders"])`
  — use the real transcript-derived commitments and existing deal context so the recap
  reflects what was *actually said* and the CRM update is evidence-backed.
- `search_transcripts(...)` to quote exact buyer language.
Doris already extracts commitments, objections, and stakeholders per call — prefer
those over re-deriving from raw text.

### With a CRM / CI / email MCP
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) or a transcript file → source
  the call content.
- CRM MCP (Salesforce/HubSpot) → write the stage/field updates back directly.

### With nothing connected
Ask the user to paste notes or the transcript; extract commitments yourself; output the
email, next steps, and a copy-paste CRM update block.

## Works without Doris
Fully functional from pasted notes — Doris only removes the paste step and supplies
evidence-backed commitments.

## Common mistakes
- Recap written in seller language, not the buyer's.
- Next steps with no owner or date.
- CRM update that restates the stage instead of flagging contradictions.
