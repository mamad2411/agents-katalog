---
description: Avvia la pipeline WEFT delegando al master-orchestratore (genera/ottimizza/deploya i siti definiti in siti.json).
argument-hint: [dominio o "all"]
---

Sei il punto di ingresso della pipeline WEFT.

Obiettivo della richiesta: **$ARGUMENTS** (se vuoto, elabora tutti i domini in `siti.json`).

Procedi cosi:

1. Verifica che esista `siti.json`. Se manca, generane uno di default minimale e segnalalo.
2. Inizializza la cartella `runtime/` e il bus eventi `runtime/eventi.jsonl`.
3. **Delega al subagent `master-orchestratore`** tramite il tool Task, passandogli il perimetro
   (dominio singolo o tutti) e il contesto da `runtime/contesto.json`.
4. Il Master eseguira le 8 fasi in sequenza per ogni dominio, coordinando gli orchestratori di
   fase e gli agenti specialisti, ed emettendo eventi di telemetria a ogni passo.
5. Al termine, riassumi: domini completati, eventuali domini bloccati con motivazione, e il path
   della cartella `DOMINI/` con il manifest finale.

Rispetta la Costituzione WEFT descritta in `CLAUDE.md`: lightmode, zero emoji, icone SVG custom,
immagini 2K con skeleton, nessun CSV, output statico per AWS, tracciabilita su `runtime/eventi.jsonl`.
Non fare domande all'utente: opera in autonomia con i default documentati.
