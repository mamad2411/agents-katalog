---
name: engagement-analyze
description: Audita la coherencia de extremo a extremo del engagement (constitución ↔ scope ↔ blackboard ↔ findings ↔ informe) y detecta incongruencias antes de cerrar — targets fuera de scope, findings sin evidencia o sin fuente, autorización caducada, referencias rotas. Úsala antes de generar el informe.
---

# Análisis de coherencia del engagement (`/analyze` adaptado)

Antes del cierre, comprueba que todo el engagement es **coherente** con `CONSTITUTION.md`. Es el
cortafuegos contra incongruencias que arruinarían el informe (un hallazgo fuera de scope, un
"explotado" sin evidencia, una autorización vencida).

## Cómo usarla
Ejecuta el verificador determinista y resuelve lo que marque:
```bash
python tools/analyze_engagement.py
# o con rutas explícitas:
python tools/analyze_engagement.py --scope contracts/scope.json --engagement contracts/engagement.json
```
Sale con código `!=0` si hay **fallos** (no solo avisos). Lee la salida y, por cada fallo, corrige
el artefacto correspondiente (no el verificador).

## Qué comprueba (contra la constitución)
- **§1 Alcance:** ningún `target` del blackboard cae fuera de `scope.json`; el campo `in_scope` del
  target coincide con la realidad.
- **§3 Evidencia:** todo finding `confirmed`/`exploited` tiene `evidence` y respaldo de fuente
  (`source_refs`/`cve`) — *"sin fuente no se explota"*.
- **Integridad:** `target_id` de cada finding existe en `targets[]`; `cvss` en rango; severidad válida.
- **Autorización:** `scope.authorization.valid_until` no está caducada.
- **Informe:** si existe `report/INFORME-*.md`, contrasta con los findings reportables.

## Cuándo
- Al terminar la explotación, **antes** de delegar en `reporting`.
- Tras cualquier edición manual de `scope.json` o `engagement.json`.
- Como puerta de calidad en el dry-run (`dryrun/run_dryrun.py` ya lo invoca al final).

> Esta skill **no** ejecuta nada ofensivo: solo lee artefactos. La barrera de alcance en tiempo de
> ejecución la sigue aplicando `scope_guard.py`; esto es la auditoría estática que la complementa.
