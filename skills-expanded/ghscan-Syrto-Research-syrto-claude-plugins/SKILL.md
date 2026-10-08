---
name: briefing-now
description: >-
  Comando esplicito: genera subito il briefing per i meeting di oggi o di una data indicata,
<!-- only:claude -->
  oppure per una singola azienda nominata, seguendo la skill `briefing`. Solo su invocazione
  diretta (/briefing-now); le richieste in linguaggio naturale ("briefing di oggi", "prepara
  le call") vanno alla skill `briefing`.
disable-model-invocation: true
argument-hint: [data opzionale, es. "domani" o "2025-03-15", o un nome azienda]
<!-- /only -->
<!-- only:openai -->
  oppure per una singola azienda nominata, seguendo la skill `briefing`. Usala solo quando
  l'utente la chiama per nome (briefing-now); le richieste in linguaggio naturale ("briefing
  di oggi", "prepara le call") vanno alla skill `briefing`.
<!-- /only -->
---

# Briefing Now

Genera immediatamente il briefing per i meeting di oggi (o della data indicata), invocando la
skill **briefing**.

## Cosa fare

<!-- only:claude -->
1. **Determina la data target**:
   - Nessun argomento → **oggi**.
   - `$ARGUMENTS` contiene "domani" / "tomorrow" → domani.
   - `$ARGUMENTS` è una data (YYYY-MM-DD) → quella data.
   - `$ARGUMENTS` è un nome azienda (non una data) → profila solo quella azienda (salta il calendario).
<!-- /only -->
<!-- only:openai -->
1. **Determina la data target** dal testo che l'utente ha scritto insieme alla richiesta:
   - Nessuna data né azienda → **oggi**.
   - "domani" / "tomorrow" → domani.
   - Una data (YYYY-MM-DD) → quella data.
   - Un nome azienda (non una data) → profila solo quella azienda (salta il calendario).
<!-- /only -->

2. **Segui la skill `briefing`** con quella data target, oppure in modalità spot per l'azienda
   indicata. Contesto, metodo, formato, consegna e casi limite sono tutti lì, quindi non
   ripeterli qui.
