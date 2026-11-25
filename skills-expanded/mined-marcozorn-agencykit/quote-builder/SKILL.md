---
name: quote-builder
version: 1.0.0
description: Build a line-item client quote with payment terms and a revision policy, run an internal margin check, and warn when gross margin drops below 40 percent before you send it.
author: MarcoZorn
license: MIT
tags: [agency, workflow, operations, sales, pricing]
compatible: claude-code, codex-cli, cursor, gemini-cli, openclaw
---

# Quote Builder

## When to use this skill

**English:** "quote", "estimate", "how much", "pricing", "proposal", "put together a price".

**Italiano:** "preventivo", "stima", "quanto costa", "offerta", "listino".

## What this skill does

Builds two versions of a quote from the same numbers: a clean client-facing quote with line items, payment terms and a revision policy, and an internal version that runs a margin check and warns you before you underprice the job. It stops the classic agency mistake — sending a number that looks fine to the client and quietly loses you money.

## Inputs required

1. **Scope** — the deliverables and quantities (e.g. 12 reels/month, 1 shooting day, 3 revisions).
2. **Your prices** — unit price per line, or ask the skill to propose a structure you then adjust.
3. **Internal cost estimate** — your real cost to deliver (crew, hours, tools, ad spend passthrough). Needed for the margin check. If withheld, the skill produces the client quote but marks the margin `UNKNOWN` and warns you.
4. **Payment terms** — default 50% upfront, 50% on delivery.
5. **Revision policy** — default 2 included, extra billed at an hourly rate you provide.
6. **Currency** and whether prices are net of tax/VAT.

## Output format

1. **CLIENT QUOTE** — clean, itemised, sendable. No internal costs, no margins.
2. **INTERNAL VERSION** — same lines plus cost, gross margin % per line and overall, and a warning if margin < 40%.

---

## Human gate

This output is a draft. Review all pricing, margins, and payment terms before sending to the client. The internal margin check surfaces the judgment call — a person signs off.

## Brand voice

If a `BRAND.md` file exists in this skill's folder (`.claude/skills/quote-builder/BRAND.md`) or in `.claude/brand/BRAND.md` (global fallback), read it before generating output and apply its tone, terminology, and examples to all text you produce. A skill-local `BRAND.md` overrides the global one; if neither exists, use a clean, professional default voice.

## Instructions

### 1. Build the line items

One row per deliverable: description, quantity, unit price, line total. Group logically (production, management, media, extras). Keep descriptions in the client's language — outcomes and deliverables, not internal task names. Sum to a clear subtotal, then apply tax/VAT if in scope, then the total.

### 2. State payment terms

Default: 50% on signature, 50% on delivery. For retainers: monthly in advance. Always put concrete triggers, not vibes — "50% due to start production, invoiced on signature, net 15."

### 3. State the revision policy

Default: 2 rounds of revisions included per deliverable. Extra revisions billed at [rate]/hour, estimated and approved before work starts. This line is what makes the `client-approval` skill's revision counter enforceable later — keep the numbers consistent between the two.

### 4. Run the margin check (internal only)

For each line and overall: `gross margin % = (price − cost) / price`.

- **≥ 50%:** healthy, no flag.
- **40–49%:** acceptable, note it.
- **< 40%:** **WARN.** Show the shortfall and suggest the price that would hit 40% and 50%, so the user can decide with numbers in front of them. Do not silently pass a thin quote.
- **Cost unknown:** mark margin `UNKNOWN` and warn that the quote is going out blind.

Never show cost or margin on the client version. A margin figure leaking into a client PDF is a real, career-flavoured mistake — keep the two blocks visually distinct and label the internal one clearly.

### Output template

```
CLIENT QUOTE — [Client] · [Date] · [Currency]

| Item | Qty | Unit price | Total |
|------|-----|------------|-------|
| ...  | ... | ...        | ...   |

Subtotal: [x]
VAT/Tax ([rate]): [x]
Total: [x]

Payment terms: [50% on signature, 50% on delivery — net 15]
Revisions: 2 rounds included per deliverable. Additional revisions billed
at [rate]/hour, estimated and approved in advance.
Validity: this quote is valid for 30 days.

---
INTERNAL VERSION  (do not send)

| Item | Price | Cost | Gross margin |
|------|-------|------|--------------|
| ...  | ...   | ...  | ...%         |

Overall: price [x] · cost [x] · gross margin [x]%
[If < 40%: ⚠ MARGIN BELOW 40%. To reach 40% price at [x]; to reach 50% price at [x].]
[If unknown: ⚠ COST UNKNOWN — margin not verified. Confirm before sending.]
```

### Edge cases

- **Client asks for a single "all-in" number:** still build the line items internally so you can defend the price if challenged, then present the total with a one-line scope summary.
- **Ad spend or third-party passthrough:** list it as a separate, clearly-labelled passthrough line at cost, excluded from your margin calculation, so it never inflates or deflates your real margin.
- **Discount requested:** apply it as a visible line, then re-run the margin check on the discounted price — a discount is exactly when margin quietly dies.
- **Retainer:** quote the monthly figure and the minimum term, and compute margin on the monthly basis.

---

## 🇮🇹 Versione italiana

### Quando usare questa skill

Quando devi fare un preventivo: "preventivo", "stima", "quanto costa", "offerta". Costruisce due versioni: una pulita per il cliente e una interna con il controllo margine.

### Cosa fa

Da gli stessi numeri crea due preventivi: uno client-facing con voci, termini di pagamento e policy revisioni, e uno interno che controlla il margine e ti avvisa prima che tu sottoprezzi il lavoro. Blocca l'errore classico: mandare un numero che sembra ok al cliente e ti fa perdere soldi in silenzio.

### Cosa ti serve

1. **Scope** — deliverable e quantità (es. 12 reel/mese, 1 giorno di shooting, 3 revisioni).
2. **I tuoi prezzi** — prezzo unitario per riga, o chiedi alla skill di proporre una struttura.
3. **Stima costo interno** — il costo reale per consegnare (crew, ore, tool, ad spend). Serve per il margine. Se non lo dai, il preventivo cliente esce ma il margine è `SCONOSCIUTO` con avviso.
4. **Termini di pagamento** — default 50% all'inizio, 50% alla consegna.
5. **Policy revisioni** — default 2 incluse, extra a tariffa oraria che fornisci.
6. **Valuta** e se i prezzi sono al netto di IVA.

### Voce del brand

Se esiste un file `BRAND.md` nella cartella di questa skill (`.claude/skills/quote-builder/BRAND.md`) o in `.claude/brand/BRAND.md` (fallback globale), leggilo prima di generare l'output e applica tono, terminologia ed esempi a tutto il testo che produci. Il `BRAND.md` locale ha la precedenza su quello globale.

### Istruzioni

1. **Costruisci le voci.** Una riga per deliverable: descrizione, quantità, prezzo unitario, totale riga. Raggruppa (produzione, gestione, media, extra). Descrizioni nella lingua del cliente. Subtotale, IVA se prevista, totale.
2. **Termini di pagamento.** Default: 50% alla firma, 50% alla consegna. Retainer: mensile anticipato. Trigger concreti, non vibes.
3. **Policy revisioni.** Default: 2 round inclusi per deliverable. Extra a [tariffa]/ora, stimati e approvati prima di iniziare. Tieni i numeri coerenti con la skill `client-approval`.
4. **Controllo margine (solo interno).** Per riga e totale: `margine % = (prezzo − costo) / prezzo`.
   - **≥ 50%:** sano.
   - **40–49%:** accettabile, segnala.
   - **< 40%:** **AVVISO.** Mostra lo scarto e suggerisci il prezzo per arrivare a 40% e 50%.
   - **Costo sconosciuto:** margine `SCONOSCIUTO` e avviso.
   Mai mostrare costo o margine nella versione cliente.

### Template di output

```
PREVENTIVO CLIENTE — [Cliente] · [Data] · [Valuta]

| Voce | Q.tà | Prezzo unit. | Totale |
|------|------|--------------|--------|

Subtotale: [x]
IVA ([%]): [x]
Totale: [x]

Termini di pagamento: [50% alla firma, 50% alla consegna]
Revisioni: 2 round inclusi per deliverable. Revisioni aggiuntive a [tariffa]/ora,
stimate e approvate in anticipo.
Validità: preventivo valido 30 giorni.

---
VERSIONE INTERNA  (non inviare)

| Voce | Prezzo | Costo | Margine lordo |
|------|--------|-------|---------------|

Totale: prezzo [x] · costo [x] · margine [x]%
[Se < 40%: ⚠ MARGINE SOTTO 40%. Per 40% prezza a [x]; per 50% prezza a [x].]
[Se sconosciuto: ⚠ COSTO SCONOSCIUTO — margine non verificato.]
```

### Casi limite

- **Cliente vuole un unico numero "tutto incluso":** costruisci comunque le voci internamente, poi presenta il totale con un riassunto scope in una riga.
- **Ad spend o passthrough di terzi:** riga separata, etichettata, a costo, esclusa dal calcolo margine.
- **Sconto richiesto:** applicalo come riga visibile, poi ri-calcola il margine sul prezzo scontato.
- **Retainer:** quota il mensile e il termine minimo, margine su base mensile.
