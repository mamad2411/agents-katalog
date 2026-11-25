---
name: client-approval
version: 1.0.0
description: Draft a clean client approval request, set a 48h SLA with a 72h escalation, and track revision rounds so the third billable revision never slips through unbilled.
author: MarcoZorn
license: MIT
tags: [agency, workflow, operations, client]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# Client Approval

## When to use this skill

**English:** "approval", "get client feedback", "send for review", "revision request", "waiting on client", "chase the client".

**Italiano:** "approvazione", "revisione", "feedback cliente", "in attesa cliente", "manda in approvazione".

## What this skill does

Produces everything you need to move a deliverable through client sign-off without it disappearing into a WhatsApp thread: a clean client-facing approval message, an internal note that sets an SLA and an escalation trigger, and a PM-tool status line. It also counts revision rounds and warns you the moment a revision crosses from "included" into "billable extra" — the money most agencies quietly give away.

## Inputs required

1. **Deliverable** — what is being approved (reel, carousel, draft, design, cut).
2. **Client name** and the contact who signs off.
3. **Which revision round is this** — first send, revision 1, revision 2, revision 3+? If you do not say, the skill infers it from the conversation history and states its assumption.
4. **Included revisions in the contract** — default is 2 if you do not specify.
5. **Deadline you need it back by** — used to set the SLA.

## Output format

Three blocks:

1. **CLIENT MESSAGE** — polished, warm, professional. Ready to send as-is.
2. **INTERNAL NOTE** — SLA, escalation trigger, revision count and billing flag. Never send this to the client.
3. **PM STATUS** — a one-line status update for Asana / ClickUp / Notion.

---

## Human gate

This output is a draft. Review SLA, revision count, and all commitment language before sending to the client. The skill surfaces the judgment call — a person signs off.

## Brand voice

If a `BRAND.md` file exists in this skill's folder (`.claude/skills/client-approval/BRAND.md`) or in `.claude/brand/BRAND.md` (global fallback), read it before generating output and apply its tone, terminology, and examples to all text you produce. A skill-local `BRAND.md` overrides the global one; if neither exists, use a clean, professional default voice.

## Instructions

### 1. Establish the revision count

This is the core of the skill. Track how many revision rounds have happened in this conversation and reason about where you are:

- **First send (round 0):** normal. No revisions consumed.
- **Revision 1:** normal. 1 of the included revisions used.
- **Revision 2:** normal, but note in the internal block that this is the last included round. The client-facing message stays neutral.
- **Revision 3 and beyond:** this falls outside the included revisions. The internal note flags it as billable and the client message gains one calm sentence naming the extra fee. Never spring the fee — always phrase it as a heads-up before work starts.

If the round is ambiguous, state your assumption in the internal note ("Assuming this is revision 2 based on two prior rounds in this thread — correct me if wrong").

### 2. Set the SLA

- **SLA: 48h** for the client to respond, counted from send. Put the concrete date/time in the message.
- **Escalation trigger: 72h.** If no response by then, the internal note tells you what to do: a friendly nudge to the primary contact, then a call, then loop in whoever owns the relationship.
- Adjust if the user's stated deadline is tighter — the SLA can never exceed the deadline.

### 3. Write the client message

Professional, warm, specific. It must contain: what you are sending, what you need (approve as-is / approve with notes / request changes), and a clear deadline with a date. No hedging, no "let me know", no apology for existing. One link or attachment reference.

### 4. Write the internal note

Plain facts for the team: revision round, revisions remaining, SLA date, escalation date and action, billing flag if applicable, and the dollar/euro amount if a fee applies (ask for the rate if you do not have it).

### 5. Write the PM status

One line: `[Deliverable] — sent for approval, SLA [date], rev [n]/[included]`.

### Output template

```
CLIENT MESSAGE
Hi [contact],

[Deliverable] is ready for your review — [one-line context].

Could you reply by [day, date, time] with one of:
• Approved as-is
• Approved with minor notes
• Changes needed (please list them in one message)

[If revision 3+: This round falls outside the 2 revisions included in our
agreement, so an additional fee of [amount] applies. Just flagging before we
start so there are no surprises.]

[Link / attachment]

Thanks,
[Your name]

---
INTERNAL NOTE  (do not send)
Revision round: [n]  ·  Included: [x]  ·  Remaining: [x-n]
SLA: reply due [date, time] (48h from send)
Escalation: if no reply by [date, time] (72h) → nudge contact, then call, then loop in [owner]
Billing: [None / EXTRA REVISION — [amount] applies, confirm on approval]

---
PM STATUS
[Deliverable] — sent for approval · SLA [date] · rev [n]/[included]
```

### Edge cases

- **Client already approved, just formalising:** skip the SLA/escalation, produce a short confirmation message and a PM status of `Approved`.
- **Silent past the SLA:** produce the escalation nudge message instead of a fresh approval request, and flag in the internal note how many hours overdue.
- **Revision with no clear contract count:** default included = 2, state it, and recommend confirming the real number.
- **Fee applies but no rate known:** ask for the extra-revision rate before finalising the client message; do not put a placeholder number in front of a client.

---

## 🇮🇹 Versione italiana

### Quando usare questa skill

Quando devi mandare qualcosa in approvazione o gestire una revisione: "approvazione", "revisione", "feedback cliente", "in attesa cliente". Produce il messaggio per il cliente, la nota interna con SLA ed escalation, e lo stato per il PM.

### Cosa fa

Ti dà tutto per portare un deliverable all'ok del cliente senza che sparisca in una chat WhatsApp: messaggio pulito per il cliente, nota interna con SLA e trigger di escalation, riga di stato per il PM. E conta i round di revisione, avvisandoti nel momento in cui una revisione passa da "inclusa" a "extra fatturabile" — i soldi che quasi tutte le agenzie regalano.

### Cosa ti serve

1. **Deliverable** — cosa va approvato (reel, carosello, bozza, design, cut).
2. **Nome cliente** e chi approva.
3. **Quale round di revisione** — primo invio, revisione 1, 2, 3+? Se non lo dici, la skill lo deduce dalla conversazione e dichiara l'assunzione.
4. **Revisioni incluse nel contratto** — default 2.
5. **Entro quando ti serve** — per impostare la SLA.

### Voce del brand

Se esiste un file `BRAND.md` nella cartella di questa skill (`.claude/skills/client-approval/BRAND.md`) o in `.claude/brand/BRAND.md` (fallback globale), leggilo prima di generare l'output e applica tono, terminologia ed esempi a tutto il testo che produci. Il `BRAND.md` locale ha la precedenza su quello globale.

### Istruzioni

1. **Stabilisci il conteggio revisioni.** È il cuore della skill.
   - **Primo invio:** normale.
   - **Revisione 1:** normale, 1 inclusa usata.
   - **Revisione 2:** normale, ma nella nota interna segnala che è l'ultimo round incluso. Il messaggio al cliente resta neutro.
   - **Revisione 3 e oltre:** fuori dalle incluse. La nota interna la marca come fatturabile e il messaggio al cliente aggiunge una frase calma con la cifra extra. Mai far cadere la fee di sorpresa: sempre un preavviso prima di iniziare.
2. **Imposta la SLA.** 48h per la risposta dall'invio, con data e ora concrete. Escalation a 72h: sollecito gentile, poi chiamata, poi coinvolgi chi gestisce la relazione. La SLA non può mai superare la deadline.
3. **Scrivi il messaggio al cliente.** Professionale, caldo, specifico: cosa mandi, cosa serve (approva / approva con note / chiedi modifiche), scadenza con data. Niente "fammi sapere", niente scuse.
4. **Scrivi la nota interna.** Round, revisioni rimaste, data SLA, data ed azione di escalation, flag di fatturazione con importo se applicabile.
5. **Scrivi lo stato PM.** Una riga: `[Deliverable] — inviato in approvazione, SLA [data], rev [n]/[incluse]`.

### Template di output

```
MESSAGGIO CLIENTE
Ciao [contatto],

[Deliverable] è pronto per la tua revisione — [contesto in una riga].

Puoi rispondere entro [giorno, data, ora] con una di queste:
• Approvato così com'è
• Approvato con piccole note
• Servono modifiche (elencale in un unico messaggio)

[Se revisione 3+: Questo giro è fuori dalle 2 revisioni incluse nel nostro
accordo, quindi si applica un costo aggiuntivo di [importo]. Te lo segnalo
prima di partire così non ci sono sorprese.]

[Link / allegato]

Grazie,
[Nome]

---
NOTA INTERNA  (non inviare)
Round revisione: [n]  ·  Incluse: [x]  ·  Rimaste: [x-n]
SLA: risposta attesa entro [data, ora] (48h dall'invio)
Escalation: se nessuna risposta entro [data, ora] (72h) → sollecito, poi chiamata, poi [owner]
Fatturazione: [Nessuna / REVISIONE EXTRA — si applica [importo], conferma all'approvazione]

---
STATO PM
[Deliverable] — inviato in approvazione · SLA [data] · rev [n]/[incluse]
```

### Casi limite

- **Cliente ha già approvato, solo da formalizzare:** salta SLA/escalation, breve messaggio di conferma, stato PM `Approvato`.
- **Silenzio oltre la SLA:** genera il sollecito di escalation invece di una nuova richiesta, e segnala nelle note di quante ore è in ritardo.
- **Fee applicabile ma tariffa sconosciuta:** chiedi la tariffa extra prima di finalizzare; mai un numero placeholder davanti a un cliente.
