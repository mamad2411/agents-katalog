---
name: knowledge-services
description: >
  Publica `docs/knowledge/approved/` a backends externos (Kwipu, futuros como Graphiti) por
  config de proyecto (`taxonomy.json`), sin acoplar el plugin a ninguno — `knowledge-sync.py
  --backend <id> [--dry-run|--check|--rebuild]` carga un adaptador por `type` (6 funciones:
  `health/plan/apply/verify/rebuild/revoke`), aplica `routing` ANTES de construir entradas
  (fail-closed) y usa `outbox.py` para staging/dead-letter — un fallo de `apply()` nunca borra la
  publicación anterior. Adaptador Kwipu (`markdown-export`): un Markdown por entrada con el
  frontmatter del Knowledge Gate (`project`/`scope`/`category`/`source`/`confidence`/
  `knowledge_id`/`version`/`hash`) + `manifest.json`; `verify` NOMBRA el reindexado sin
  ejecutarlo. Úsala cuando el usuario diga "sincroniza el conocimiento con Kwipu", "publica
  docs/knowledge en el grafo", "exporta approved a Kwipu", "por qué Kwipu no ve esta entrada",
  "añade un backend de knowledge-services", o al activar la capacidad `kwipu` desde `/setup`.
---

# knowledge-services — de `approved/` a un backend externo, sin acoplar el plugin a ninguno

`docs/knowledge/approved/` es el origen canónico (Git, revisado, curado por `knowledge-curator`).
Esta skill lo **proyecta** hacia fuera: hoy Kwipu (grafo local), mañana cualquier otro backend que
declare su propio `type` — el núcleo (`knowledge-sync.py`) no cambia al añadir uno.

## Cuándo NO usarla

- Para curar o aprobar conocimiento: eso es `knowledge-curator` (`curator-gate.py`) sobre
  `docs/knowledge/candidates/`. Esta skill solo lee `approved/`, nunca escribe ahí.
- Para consultar el grafo ya publicado (queries, respuestas): eso es del stack de Kwipu/Graphiti,
  fuera del plugin.
- Para reindexar Kwipu de verdad (`build_view`, reiniciar contenedores): esta skill **nombra** el
  remedio (`verify`), nunca lo ejecuta — es responsabilidad del stack externo (CA-16).
- Sin `taxonomy.json` con `backends.<id>.enabled: true`, no hay nada que sincronizar: `/doctor`
  reporta la capacidad como desactivada, y eso es correcto, no un error.

## Piezas

| Fichero | Qué es |
|---|---|
| `scripts/knowledge-sync.py` | Único punto de entrada; nunca menciona un backend concreto. |
| `scripts/kwipu-project-add.py` | Alta del proyecto en `<stack>/kwipu/config/projects.yaml` (`/setup` 5-sexies, C-07): **solo añade** un bloque marcado, con vista previa + `sha256`, confirmación (`--apply --esperado`) y copia `.bak-<AAAAMMDDTHHMMSSZ>`. Exit 0 ok/no-op · 1 E/S o fichero cambiado · 2 uso · 3 forma no reconocida (imprime el bloque) · 4 conflicto. Contrato en `references/kwipu-adapter.md`. |
| `backends/__init__.py` | Carga y valida el adaptador por `type` (`backends/README.md`: contrato completo de las 6 funciones). |
| `backends/markdown_export.py` | Adaptador Kwipu (`type: "markdown-export"`): CA-17/CA-16, ver `references/kwipu-adapter.md`. |
| `backends/graphiti.py` + `backends/graphiti_providers.py` | Adaptador Graphiti (`type: "graphiti"`, ADR-018): cliente MCP, `mode: shadow`/`read`, `rebuild`/`revoke` — ver `backends/README.md`. |
| `agent-kits/shared/knowledge-schema.py` | Taxonomía del proyecto (`taxonomy.json`), fail-closed; `--setup-id-prefix` propone/valida/guarda el `id_prefix` y avisa al renombrar con conocimiento ya exportado (CA-14/CA-15). Aviso de grupo ajeno de Graphiti: `knowledge-sync.py --avisos-grupo [--consultar-servidor]`. |
| `agent-kits/shared/knowledge-index.py` | Índice de `approved/`. |
| `agent-kits/shared/outbox.py` | Staging/dead-letter reutilizado (CA-15), nunca reimplementado aquí. |
| `agent-kits/shared/capabilities.py` | Registro de capacidades opcionales (`/setup`, `/doctor`, T-09). |

## Uso

Plugin instalable (regla 5 de `docs/CONVENTIONS.md`): localiza el script en runtime con el
patrón de seis raíces, nunca una ruta relativa fija.

```bash
KSSKILL="$(find "$PWD/.claude" "$PWD/.codex" "$PWD/.opencode" "$HOME/.claude" "$HOME/.codex" "$HOME/.config/opencode" -type f -path '*skills/knowledge-services/scripts/knowledge-sync.py' 2>/dev/null | head -1)"
python3 "$KSSKILL" --backend kwipu --root . --check
python3 "$KSSKILL" --backend kwipu --root . --dry-run
python3 "$KSSKILL" --backend kwipu --root .
python3 "$KSSKILL" --backend kwipu --root . --rebuild
python3 "$KSSKILL" --backend kwipu --root . --outbox-status
```

- `--check`: `health()` + `verify()`, no toca la publicación ni la outbox. `exit 0` solo si
  `estado == "sano"` y `verify().ok`. `verify()` tiene TRES veredictos (`estado`: `ok` ·
  `incompleto` · `desfase`): `incompleto` (la ventana de lectura no alcanzó el grafo) NO es `ok`,
  se imprime con su `no_verificado` y su `aviso`, y sale ≠ 0.
- `--dry-run`: calcula `plan()` y lo imprime; nunca llama a `apply()` ni drena la outbox.
- (ninguno): primero DRENA la outbox propia — reintenta cualquier envelope PENDIENTE de este
  mismo backend cuyo backoff ya venció (`_drenar_outbox_propia`, aplica sus `ops` de forma
  idempotente; si vuelve a fallar, incrementa `intentos` de verdad y escala a `dead-letter` al
  llegar a `MAX_INTENTOS`) — y LUEGO hace `plan()` + `apply()` reales del sync fresco, con
  staging/dead-letter de `outbox.py`. Un envelope de OTRO backend que bloquee el reclamo se cede
  con `outbox.ceder_paso()` sin tocar su presupuesto de reintentos. Un fallo de `apply()` en el
  sync fresco reencola con backoff (nunca dead-letter directo por un solo fallo); la publicación
  anterior queda intacta.
- `--rebuild`: `rebuild(entries, cfg)` sobre TODAS las entradas ya enrutadas para ese backend
  (equivale a `plan(entries, cfg, force=True)` + `apply`, fuerza `upsert` en todo).
- `--outbox-status`: imprime `outbox.estado()` de la cola de este backend y sale — no publica ni
  drena nada. Es el diagnóstico de referencia cuando una corrida sospecha que hay envelopes
  atascados.

Añadir un backend nuevo: un fichero `backends/<type>.py` con las 6 funciones — ver
`backends/README.md` para el contrato exacto y `references/kwipu-adapter.md` para el ejemplo real
(Kwipu) con sus derivaciones documentadas (frontmatter CA-17, mapeo de salud, algoritmo de
`verify`).

## Guardrails

- **Fail-closed por routing**: una categoría sin `routing` declarado, o `routing.<id>: false`,
  jamás llega al adaptador — ni siquiera para "solo probar".
- **Nunca se borra la publicación anterior en error**: `apply()` publica fichero a fichero con un
  diario (`manifest.pending.json` → publica → `manifest.json`, ver `references/kwipu-adapter.md`);
  nunca borra ni mueve ficheros ajenos a los que el propio manifiesto controla. Un fallo va primero
  a reencolado con backoff (`outbox.py`) y solo escala a `dead-letter` al agotar los reintentos —
  no se reintenta dentro de la misma corrida, sí en la siguiente (drenaje antes del sync fresco).
- **`verify` nombra, no ejecuta** (CA-16): el reindexado real es del stack, nunca de este plugin.
- **Una sola excepción a «no toca el stack»** (enmienda de ADR-018 / PAT-001, diseño O1): `kwipu-project-add.py` puede AÑADIR un bloque a `projects.yaml`, nunca modificar ni borrar; `build_view` y el reinicio de contenedores solo se imprimen.
- **Sin dependencias externas**: todo el código de esta skill es stdlib puro.

## Qué NO hace

- No decide taxonomía ni categorías (eso es `taxonomy.json`, por proyecto).
- No aprueba ni rechaza conocimiento (eso es `knowledge-curator`).
- No registra el backend en Kwipu/Graphiti por su cuenta (nada de "auto-discovery" de red); el alta en `projects.yaml` la lanza `/setup` con confirmación del usuario y solo añade.
