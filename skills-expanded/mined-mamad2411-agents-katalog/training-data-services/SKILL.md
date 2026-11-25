---
name: training-data-services
description: >
  Captura DETERMINISTA de casos (petición, contexto, trayectoria chat/SFT sin chain-of-thought,
  métricas opacas del proyecto, validación) en un case store versionado FUERA de Git y de
  `docs/knowledge/`, y ensamblado de dataset solo con casos Gold aprobados por un humano. Opt-in
  por proyecto con `.claude/knowledge-services/training.json`; sin él, cero impacto. El plugin
  valida FORMA, nunca dominio: no calcula métricas, no marca Gold solo, no entrena ni sirve
  modelos. `scripts/case_schema.py` valida `training.json` y el esquema del caso (vocabularios
  cerrados de `validation.status` y `outcome`, mapeo declarado desde `useful|dead_end|corrected`).
  `dataset-assembler.py` ensambla el dataset; `propose-from-case.py` propone, nunca aprueba.
  Úsala cuando el usuario diga "guarda este intento como caso", "captura casos para entrenar un
  modelo local", "valida el esquema del caso", "prepara un dataset con los casos aprobados",
  "activa training-data-services", o al activar la capacidad `training` desde `/setup`.
---

# training-data-services — casos versionados y dataset Gold, sin saber nada del dominio

Algunos proyectos repiten tareas con una forma objetiva de medir el éxito y quieren conservar cada
intento para entrenar después un modelo local más barato. Esta skill da el **mecanismo genérico**:
esquema del caso, recorder determinista, puerta humana para Gold y ensamblador de dataset. Todo lo
de dominio (métricas, simulación, herramientas) es del proyecto consumidor.

> Regla central: **Gold es siempre una acción humana explícita** y **solo Gold se exporta**. El
> conocimiento aprobado nunca alimenta hacia atrás al case store (anti-leakage).

## Cuándo NO usarla

- Para curar o aprobar conocimiento (`docs/knowledge/candidates/`): `knowledge-curator` (esta skill,
  como mucho, **propone** un caso Gold, `bridge_to_curator`); para publicarlo (Kwipu): `knowledge-services`.
- Para calcular una métrica, simular o evaluar semánticamente un resultado: código del proyecto.
- Para lanzar un fine-tuning, servir un modelo o correr un benchmark: siempre fuera del plugin.
- Sin `training.json` (o con `enabled: false`) no hay nada que hacer: la capacidad está apagada y
  eso es correcto, no un error.

## Piezas

| Fichero | Qué es |
|---|---|
| `scripts/case_schema.py` | Validador stdlib de `training.json` y del caso (exit 0 válido · 1 errores · 2 uso/JSON ilegible). Fuente única de los vocabularios cerrados y del mapeo de `outcome`. |
| `scripts/case-recorder.py` | Recorder (API importable + CLI `record` · `set-status` · `index` · `list`; todos aceptan `--config <training.json>` y `--project-root <dir>`). Graba cada intento como versión inmutable `cases/<family>.<variant>/v<NNN>/`. La redacción la delega en `agent-kits/shared/redact.py` (fuente única); sin él se niega a grabar. Un caso `corrected` exige que la versión que corrige exista y sea `failure` o `corrected`. |
| `scripts/dedup.py` | Near-duplicates deterministas (shingles de palabras + Jaccard, sin embeddings ni red; boilerplate por frecuencia documental con 20 casos o más; índice PPJoin, no todos los pares; muestreo por valor declarado por encima de 10⁷ shingles). `shingles` es copia declarada de `code-health` (`agent-kits/shared/copias.json`). |
| `scripts/dataset-assembler.py` | Ensamblador en dos pasadas en streaming: solo Gold leído de `validation.json` en disco y atado a su contenido (`content_hash`), benchmark por familia COMPLETA declarada con `--benchmark` (sin ella, exit 1), near-duplicates que cruzan excluidos del lado de train, `exports/<export_id>/` con `train.jsonl`/`benchmark.jsonl` (chat, redactados, con procedencia) y `manifest.json` el último; nunca sobrescribe ni borra. Tras cada ensamblado real deja la marca `exports/.ultimo.json` (firma de la entrada); `--estado [--json]`, solo lectura: la frescura sin tope (exit 0/1/2). |
| `scripts/propose-from-case.py` | Puente opt-in (`bridge_to_curator`): un caso Gold → UN candidato en `docs/knowledge/candidates/pending/` con la forma de `curator-gate.py`; nunca aprueba ni sobrescribe. |
| `assets/` | Plantillas del case store: `training.example.json`, ejemplo completo `case-store-example/` (caso con par fallo → corrección) y `README.md` con la estructura y cada fichero de versión (`metadata.json`, `validation.json`, `cases_index.jsonl`…). Ubicación: `docs/knowledge/adr/ADR-019-case-store-fuera-de-docs-knowledge.md`. |
| Capacidad `training` | Entrada de `agent-kits/shared/capabilities.py`: `deshabilitado` sin fichero, `error` con fichero y campo si la config es inválida, `declarado`/`ok` según exista `root`. Sin red. |

## Config opt-in — `.claude/knowledge-services/training.json`

| Clave | Obligatoria | Qué es |
|---|---|---|
| `version` | sí | `1` |
| `enabled` | no (`false`) | Activa la capacidad `training` |
| `root` | si `enabled` | Raíz del case store; la elige el proyecto (relativa a su raíz o absoluta, sin `~`); nunca dentro de `<proyecto>/docs/knowledge/` (resuelto con `realpath`, sin distinguir mayúsculas) |
| `id_prefix` | si `enabled` | Slug (≤ 32) que prefija el `case_id`: `<id_prefix>-<family>.<variant>` (`family`/`variant` ≤ 64); cambiarlo deja fuera los casos del store: usa otro `root` |
| `ids` | no | `family_pattern` / `variant_pattern` (regex, sin puntos por defecto) · `version_width` (dígitos de `v<NNN>`, 3 por defecto) |
| `bridge_to_curator` | no (`false`) | Un caso Gold puede proponerse como candidato a `knowledge-curator` (nunca se aprueba solo) |

Cualquier otra clave se rechaza (salvo `$comment`), para que una errata no pase en silencio.

## Esquema del caso (mapa)

Obligatorios `case_id`, `version`, `family`, `variant`, `request` (literal), `trajectory` (turnos
`system|user|assistant|tool`, **sin chain-of-thought**), `validation` y `outcome`; `metrics` es opaco
y `artifacts` solo referencias `{path, hash, kind}`. `validation.status` ∈ `pending · approved ·
needs_changes · rejected` (`approved` ⇔ `approved_by_human: true`); `outcome` ∈ `success · failure ·
corrected` (`corrected` exige `supersedes_case`). Detalle, límites y mapeo de `outcome` desde fuentes
externas (`graphify`): `references/case-schema.md`.

## Proceso

1. **Activar**: `training.json` con `enabled: true`, `root` e `id_prefix` (`/setup`, capacidad `training`).
2. **Validar** antes de escribir: `scripts/case_schema.py config <training.json>` y
   `case_schema.py case <caso.json> --config <training.json>` (lee `references/case-schema.md`).
3. **Grabar** cada intento: `scripts/case-recorder.py record <caso.json>`; versión nueva e inmutable,
   redactada antes de escribir; nunca sobrescribe ni borra.
4. **Aprobar Gold**, siempre a mano: `set-status <case_id> <versión> approved --approved-by-human`
   (o `record … --approved-by-human`); sin el flag, rechazo.
5. **Consultar**: `list` (lee el índice, una caché), `index check` / `index rebuild`. Exit codes,
   concurrencia, redacción y límites de los pasos 3-5: `references/recorder.md`.
6. **Ensamblar** el dataset: `scripts/dataset-assembler.py --benchmark <family>[,…] [--dry-run]` →
   `exports/<export_id>/` (solo Gold, benchmark por familia completa, near-duplicates, manifiesto con
   hashes). Lee `references/dataset.md` al llegar aquí.
7. **Proponer** (opcional) un caso Gold al Curator: `scripts/propose-from-case.py <case_id>
   <versión> --category <KEY>` → `docs/knowledge/candidates/pending/` (`references/dataset.md`).

## Referencias (bajo demanda)

| Fichero | Léelo al llegar a |
|---|---|
| `references/case-schema.md` | Paso 2: esquema completo del caso, reglas de `family`/`variant`, chain-of-thought, mapeo de `outcome`. |
| `references/recorder.md` | Pasos 3-5: proceso detallado, exit codes (0/1/2/3), semántica de `index check`, redacción, concurrencia y límites declarados. |
| `references/dataset.md` | Pasos 6-7: dedup, partición anti-leakage, formato del export y del manifiesto, puente al Curator. |

## Degradación

- Sin `training.json` o con `enabled: false`: la capacidad no existe para el ciclo (CA-01). Inválido:
  `/doctor` lo informa con fichero y campo; nada se bloquea. Activo: `/doctor` da el recuento por estado
  y la frescura del dataset (firma de la entrada frente a la marca del último ensamblado, que registra
  los Gold omitidos: ⚠️ `con_omisiones` hasta corregir la causa y reensamblar (si era transitoria, basta
  con reensamblar); tope de 2 s, entre ~1 000 y ~2 000 versiones
  en caliente según la carga, en sistemas de ficheros locales; «PARCIAL» si no llega:
  `dataset-assembler.py --estado` la verifica sin tope). Sin `python3`: el resto sigue.

## Scripts y rutas

Rutas relativas dentro de la skill; desde fuera, `find` sobre las seis raíces de la regla 5 de `docs/CONVENTIONS.md`
(`-path '*skills/training-data-services'`). Los tests viven junto a los scripts, solo en el repo; sin dependencias.
