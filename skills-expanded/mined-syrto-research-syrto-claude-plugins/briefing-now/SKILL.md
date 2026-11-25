---
name: briefing-now
description: >-
  Comando esplicito: genera subito il briefing per i meeting di oggi o di una data indicata,
  oppure per una singola azienda nominata, seguendo la skill `briefing`. Solo su invocazione
  diretta (/briefing-now); le richieste in linguaggio naturale ("briefing di oggi", "prepara
  le call") vanno alla skill `briefing`.
disable-model-invocation: true
argument-hint: "[data opzionale, es. \"domani\" o \"2025-03-15\", o un nome azienda]"
---

# Briefing Now

Genera immediatamente il briefing per i meeting di oggi (o della data indicata), invocando la
skill **briefing**.

## Cosa fare

1. **Determina la data target**:
   - Nessun argomento → **oggi**.
   - `$ARGUMENTS` contiene "domani" / "tomorrow" → domani.
   - `$ARGUMENTS` è una data (YYYY-MM-DD) → quella data.
   - `$ARGUMENTS` è un nome azienda (non una data) → profila solo quella azienda (salta il calendario).

2. **Segui la skill `briefing`** con quella data target, oppure in modalità spot per l'azienda
   indicata. Contesto, metodo, formato, consegna e casi limite sono tutti lì, quindi non
   ripeterli qui.
