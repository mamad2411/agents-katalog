---
name: pipeline-followup
description: Prepare draft follow-up emails for CRM deals that have gone quiet. Use whenever the person wants to chase deals with no reply, re-engage stalled opportunities, or "prepare the follow-ups" for their pipeline — e.g. "controlla la pipeline e preparami i follow-up", "chi non mi ha risposto?", "fammi le bozze per i deal fermi", "follow up on the Rossi deal". Reads the CRM (e.g. Pipedrive) and the deal's Gmail thread, applies the rules in pipeline/rules.md (no-reply threshold, max follow-ups), and writes a Gmail DRAFT in the person's voice. Draft-only: never sends, never moves CRM stages. On-demand, not a schedule.
---

# Pipeline follow-up — bozze per i deal silenziosi

Prepari **bozze** di follow-up per i deal che si sono raffreddati. On-demand: la persona ti chiama quando vuole recuperare i thread fermi. Non sei una routine automatica e **non invii mai nulla**.

## Non-negoziabili (paletti)
- **Draft-only.** Crei una **bozza in Gmail** (mai invio). Il destinatario e l'oggetto sono pronti, ma l'invio lo fa la persona.
- **Non toccare il CRM.** Non spostare stadi, non chiudere deal, non modificare campi. Al massimo, se `rules.md` lo consente, proponi di aggiungere una *nota/attività* — ma solo su conferma esplicita.
- **Rispetta le regole in `pipeline/rules.md`.** Soglia no-reply e numero massimo di follow-up: se un deal ha già ricevuto il massimo, **non** generare un'altra bozza — segnalalo come "da marcare freddo".
- **Mai inventare.** Nessun prezzo, promessa, data o fatto che non sia già nel thread Gmail o nelle note del CRM. Se manca il contesto, dillo e chiedi.
- **Conferma prima dei volumi.** Se i deal candidati sono più di ~5, elencali prima e chiedi su quali preparare le bozze, invece di generarne venti.

## Preflight
1. Leggi `pipeline/rules.md`. Se è un template vuoto ({{placeholder}}), fermati: serve prima la sessione `knowledge-transfer` sul processo di vendita. Non inventare soglie.
2. Leggi `pipeline/followup_templates.md` per la voce e i template per situazione.
3. Verifica i connettori: **CRM** (es. Pipedrive, lettura) e **Gmail** (lettura + creazione bozze). Se manca uno dei due, dillo e fermati sul pezzo che non puoi fare.

## Flusso
1. **Individua i candidati.** Dal deal radar (`pipeline/deal_radar.md`) se è fresco, o interrogando il CRM: deal con silenzio oltre la soglia del loro tipo (vedi `rules.md`). Se la persona ha nominato un deal specifico ("il deal Rossi"), lavora solo su quello.
2. **Per ogni deal candidato, leggi il thread Gmail reale.** Trova l'ultimo scambio con il referente: cosa è stato mandato, cosa è rimasto in sospeso, il tono. La bozza si aggancia a QUESTO, non a un template generico.
3. **Scegli il template giusto** in base alla situazione (primo follow-up / secondo / deal fermo in negoziazione) e adattalo al thread: 3-6 righe, voce della persona, un solo next step chiaro.
4. **Crea la bozza in Gmail** (in risposta al thread, così mantiene oggetto e destinatario). Non inviare.
5. **Riepiloga alla persona:** per ogni deal, 1 riga — "{{deal}}: bozza pronta, angolo = {{...}}". Segnala i deal che hanno superato il max follow-up (→ "da marcare freddo, non ricontatto"). Elenca cosa NON hai potuto fare (contesto mancante, connettore assente).

## Chiusura
Chiudi con `Memory Update` nel formato del Project. Se emergono deal da marcare freddi, thread caldi dimenticati o pattern (es. un tipo di deal che si raffredda sempre), annotali in `decisions/open_questions.md` o nei file pertinenti.
