# WEFT · istruzioni per Claude Code

WEFT e un sistema multi-agente che genera siti statici di qualita editoriale a scala,
ottimizzati SEO/GEO e pronti per il deploy su AWS. Questo file e la memoria di progetto:
Claude Code lo carica automaticamente e lo usa come contratto operativo.

## Punto di ingresso

Quando l'utente chiede di generare, ottimizzare o pubblicare uno o piu siti — oppure lancia
il comando `/weft` — **delega immediatamente al subagent `master-orchestratore`** (cartella
`.claude/agents/00-master/`). Non eseguire tu il lavoro di dettaglio: il Master coordina gli
8 orchestratori di fase, che a loro volta coordinano i 300 agenti specialisti.

Catena di comando:

```
/weft  ->  master-orchestratore  ->  orchestratore-<fase>  ->  agenti specialisti
```

## Le 8 fasi (in ordine, per ogni dominio)

1. **Ricerca** (`orchestratore-ricerca`) — trend, keyword, intenti, manifest pagine (JSON).
2. **Sviluppo** (`orchestratore-sviluppo`) — bozze .md -> HTML semantico essenziale.
3. **Humanizer** (`orchestratore-humanizer`) — tono naturale, loop di approvazione.
4. **Legale** (`orchestratore-legale`) — privacy/cookie/T&C, GDPR + Privacy Act AU, banner TCF.
5. **Design** (`orchestratore-design`) — moodboard, logo e icone SVG custom, design system lightmode, skeleton.
6. **Completatore** (`orchestratore-completatore`) — robots, sitemap, manifest, file di sistema.
7. **SEO tecnico & GEO** (`orchestratore-seo`) — performance, schema, analytics, ottimizzazione per AI.
8. **Debug & Deploy** (`orchestratore-deploy`) — QA, loop-fix, build statico, deploy AWS, cartella DOMINI.

## Costituzione (vincoli inderogabili, validi per ogni agente)

1. **Lightmode** obbligatorio in ogni interfaccia, pagina e asset.
2. **Zero emoji**, ovunque. Icone solo SVG vettoriali custom e non banali.
3. **Palette mai dozzinali**: derivate dalla moodboard del dominio.
4. **Immagini 2K** (>=2560px), sempre diverse e pertinenti, con anti-ripetizione.
5. **Skeleton shimmer** (stile Instagram) per ogni area che carica.
6. **Niente CSV**: i dati di progetto vivono in manifest JSON/YAML.
7. **Output statico** ottimizzato per AWS S3 + CloudFront.
8. **Tracciabilita visiva**: ogni agente emette eventi su `runtime/eventi.jsonl`.
9. **Compliance reale** GDPR/AU; i testi legali sono template tecnici, non consulenza.
10. **E-E-A-T autentica**: nessun contenuto-spazzatura a scala.

## Bus di telemetria (osservabilita)

Ogni agente, a ogni step, scrive una riga JSON su `runtime/eventi.jsonl`:

```json
{"ts":"<iso8601>","agente":"<slug>","fase":"<fase>","stato":"avviato|progresso|completato|errore","percentuale":0,"messaggio":"<breve>","artefatti":["<path>"]}
```

La CLI `weft` legge questo flusso e mostra in tempo reale che qualcosa e cambiato
(barra del run, barra della fase, righe degli agenti che si accendono).

## Dati di progetto (niente CSV)

- `siti.json` — manifest dei domini e tipologie (sostituisce il vecchio `siti.csv`).
- `runtime/contesto.json` — configurazione del run (geo target, budget, modalita dry-run).
- Output dati delle fasi: sempre JSON nelle cartelle del dominio.
- Domini finali: cartella `DOMINI/` con manifest JSON ed export di registrazione (no CSV).

## Modalita autonoma

Gli agenti operano con default sensati e **non fanno domande all'utente**. Se un dato manca,
scelgono il default documentato e lo annotano tra i rischi nell'handoff.

## CLI visiva

- `weft demo` — dashboard animata in dry-run (nessuna chiamata esterna).
- `weft agents` — riepilogo dei 300 agenti.
- `weft doctor` — controllo ambiente.
- `weft snapshot --out frame.svg` — esporta un frame della dashboard (tema chiaro).
