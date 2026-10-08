---
name: content-share-protocol
description: >-
  Protocollo 5 fasi per pubblicare artefatti HTML su soli-frames.
  Pre-flight+EgressCheck → Build Payload → Validate → Gate Umano → Dispatch+Log.
  Gated su content_share.enabled (R.CS2 default off). PATTERN §32.
pattern_version: "2.33"
---

# content-share-protocol

Skill di dispatch per il Content Share Consumer Layer (EP-048). Consente di
pubblicare artefatti HTML (report, guide, output di agenti) su soli-frames
tramite GitHub repository_dispatch. Attivabile solo con
`content_share.enabled: true` in `factory.config.yaml` (R.CS2).

Il protocollo si articola in 5 fasi sequenziali: Fase 0 (Pre-flight + Egress
Check), Fase 1 (Build Payload), Fase 2 (Validate), Fase 3 (Gate Umano),
Fase 4 (Dispatch + Log). Il gate umano in Fase 3 e' obbligatorio prima di
qualsiasi dispatch (R.CS3 — azione outward non reversibile).

---

## Invarianti locali

- **R.CS1**: slug format `{source_repo_slug}-{content_slug}`, regex
  `^[a-z][a-z0-9-]{1,78}[a-z0-9]$` (max 80 chars) — STOP in Fase 0 se non
  conforme dopo composizione
- **R.CS2**: `content_share.enabled: false` default — a flag spento: nessuna
  variabile letta, nessuna chiamata API, identico a v2.32
- **R.CS3**: gate umano obbligatorio pre-dispatch (PATTERN §7 r.15 — azione
  outward non reversibile) — STOP senza conferma esplicita
- **R.CS4**: egress classification check bloccante in Fase 0 — EGRESS_BLOCK
  su analytics_report con dati sensibili; label classificazione iniettata nel
  gate R.CS3

---

## Fase 0 — Pre-flight + Egress Check (R.CS4)

1. Legge `factory.config.yaml` blocco `content_share:`
2. SE `enabled: false` → STOP con messaggio:
   > "content_share non abilitato. Imposta `content_share.enabled: true` in
   > factory.config.yaml e compila source_repo_slug, source_repo. Vedi
   > wiki/runbooks/content-share-setup.md"
3. Verifica `$SOLI_FRAMES_PAT` presente (fail-loud):
   > "SOLI_FRAMES_PAT non configurato. Crea un PAT fine-grained con scope
   > Contents:write su soli92/soli-frames e aggiungilo come secret. Vedi
   > wiki/runbooks/content-share-setup.md"
4. Verifica `$SOLI_FRAMES_DISPATCH_SECRET` presente (fail-loud):
   > "SOLI_FRAMES_DISPATCH_SECRET non configurato."
5. Verifica `source_repo_slug` non vuoto (fail-loud):
   > "source_repo_slug vuoto in factory.config.yaml. Inserire il nome slug del
   > repo (es. 'soli-prof')."
6. Verifica `source_repo` non vuoto e formato org/repo (fail-loud):
   > "source_repo vuoto o formato non valido in factory.config.yaml. Usare
   > formato 'org/repo' (es. 'soli92/soli-prof')."
7. **R.CS4 — Classificazione egress**:
   - Categoria `analytics_report` + presenza di dati per-attore o rate card →
     EGRESS_BLOCK:
     > "Artefatto classificato come analytics_report con potenziale dati
     > sensibili. Verifica che il report non contenga actor_id, rate_card o
     > dati GDPR prima di procedere. Usa --dry-run per ispezionare il payload."
   - Categoria non in `artifact_categories` abilitati → EGRESS_WARN
   - Altrimenti → EGRESS_PASS
8. Misura dimensione HTML decoded:
   - > 100 KB → STOP:
     > "HTML decoded supera il limite hard di 100 KB (misurato: X KB). Ridurre
     > il contenuto o attendere US-024 merged su soli-frames."
   - > 80 KB → EGRESS_WARN:
     > "HTML decoded supera la soglia di warning 80 KB (X KB). Considerare
     > ottimizzazione del contenuto."

**Output Fase 0**: `EGRESS_PASS | EGRESS_WARN | EGRESS_BLOCK` (stampato
esplicitamente prima di procedere alla Fase 1).

---

## Fase 1 — Build Payload

1. **Compose slug**:
   - Se `--slug` fornito: usa il valore come `content_slug`
   - Altrimenti: `content_slug` = basename del file HTML senza estensione
     (kebab-case, es. `report-sprint-42` da `report-sprint-42.html`)
   - Slug completo: `{source_repo_slug}-{content_slug}`
2. **Valida slug regex R.CS1**: `^[a-z][a-z0-9-]{1,78}[a-z0-9]$` — STOP se
   non conforme
3. **Estrae title**:
   - Se `--title` fornito: usa il valore
   - Altrimenti: estrae da tag `<title>` dell'HTML (grep/sed); fallback a slug
     se assente
4. **Encode HTML in base64**:
   ```bash
   base64 -i <path> | tr -d '\n'
   ```
5. **Costruisce payload JSON annidato** (FORMA OBBLIGATORIA — payload piatto
   causa 422):
   ```json
   {
     "event_type": "content-ingest",
     "client_payload": {
       "dispatch_secret": "$SOLI_FRAMES_DISPATCH_SECRET",
       "slug": "<slug-completo>",
       "title": "<title>",
       "html_b64": "<base64>",
       "publish": false,
       "source_repo": "<source_repo>"
     }
   }
   ```
   Nota: `publish: false` sempre (`publish_default: draft`, R.CS3 sicurezza).
   Override esplicito solo con `--publish=true` consapevole.

---

## Fase 2 — Validate

1. Doppia verifica slug regex R.CS1 (post-composizione):
   `^[a-z][a-z0-9-]{1,78}[a-z0-9]$` — STOP se non conforme
2. Verifica `source_repo` formato `org/repo`:
   regex `^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$` — STOP se non conforme
3. Verifica dimensione JSON payload complessivo < 10 MB (limite API GitHub) —
   STOP se superata

---

## Fase 3 — Gate Umano (R.CS3)

Mostra riepilogo obbligatorio:

```
╔══════════════════════════════════════════════════════╗
║  CONTENT SHARE — Riepilogo dispatch                 ║
╠══════════════════════════════════════════════════════╣
║  Slug:       <slug-completo>                        ║
║  Title:      <title>                                ║
║  Size:       X KB (HTML decoded)                    ║
║  Target:     https://soli-frames.vercel.app/viewer/ ║
║  Publish:    draft (non visibile finché non merged) ║
║  Categoria:  <EGRESS_PASS|EGRESS_WARN> <categoria>  ║
║  Actions:    https://github.com/soli92/soli-frames/actions
╚══════════════════════════════════════════════════════╝
Procedere con il dispatch? [y/N]
```

- **`--dry-run`**: mostra riepilogo + payload completo → STOP senza dispatch.
  Stampa: "DRY RUN completato. Nessun dispatch eseguito."
- Risposta != "y" (case-insensitive): STOP. "Dispatch annullato."

---

## Fase 4 — Dispatch + Log

1. **Dispatch via gh CLI**:
   ```bash
   gh api repos/soli92/soli-frames/dispatches \
     --method POST \
     -H "Authorization: Bearer $SOLI_FRAMES_PAT" \
     --input - <<< "$PAYLOAD_JSON"
   ```
2. **Response mapping**:

   | HTTP | Azione |
   |---|---|
   | `204` | "Dispatch inviato. Il contenuto sarà disponibile dopo il merge della PR su soli-frames (pending). Non è ancora pubblicato." |
   | `401` | STOP: "Unauthorized. Verificare SOLI_FRAMES_PAT (scaduto o revocato?)." |
   | `404` | STOP: "Repo soli92/soli-frames non trovato. Verificare target_repo in config." |
   | `422` | STOP: "Payload non valido (422). Verificare il formato del payload. Causa frequente: payload piatto senza event_type/client_payload wrapper." |
   | `5xx` | Retry max 2 volte con backoff 1500ms, poi STOP: "Errore server GitHub (5xx). Riprovare tra qualche minuto." |

3. **Stampa link GitHub Actions**:
   `https://github.com/soli92/soli-frames/actions`
4. **Log entry in wiki/log.md** (append-only):
   ```
   [YYYY-MM-DD HH:MM] content-share dispatch — slug: <slug> — status: dispatched (pending merge) — files touched: 0
   ```

---

## Errori comuni

| Condizione | Causa probabile | Azione |
|---|---|---|
| `content_share.enabled: false` | Flag opt-in disattivato | Attivare in `factory.config.yaml`, compilare `source_repo_slug` e `source_repo` |
| `SOLI_FRAMES_PAT` assente | Secret non configurato | Creare PAT fine-grained con scope `Contents:write` su `soli92/soli-frames` |
| `SOLI_FRAMES_DISPATCH_SECRET` assente | Secret non configurato | Verificare il valore nel repo soli-frames e configurare in locale |
| Slug non conforme R.CS1 | Caratteri non validi o lunghezza errata | Usare solo `[a-z0-9-]`, iniziare con lettera, max 80 chars totali |
| 422 da GitHub API | Payload piatto (senza wrapper event_type/client_payload) | Verificare struttura JSON in Fase 1 — mai usare payload piatto |
| HTML > 100 KB | Artefatto troppo grande | Ridurre il contenuto (rimuovere script inline, immagini base64 embedded) |
| EGRESS_BLOCK | analytics_report con dati sensibili | Sanitizzare il report prima del dispatch o usare `--dry-run` per ispezionare |

---

## Riferimenti

- Contratto API: `wiki/sources/soli-frames-integration.md` + `wiki/entities/soli-frames.md`
- Setup credenziali: `wiki/runbooks/content-share-setup.md`
- Pattern architetturale: `wiki/concepts/content-share-hub-pattern.md`
- Comando invocante: `.cursor/commands/share.md`
- Configurazione: `factory.config.yaml` blocco `content_share:`
- PATTERN §32 — Content Share Consumer Layer
