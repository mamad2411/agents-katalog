---
name: empirical-system-invariants
description: "Use when a system must prove, every cycle, that it measures what it claims - auditing a data pipeline for phantom wiring, silent empty getters, or unpopulated fields. Provides per-cycle data contracts, a RED-light rule naming the exact broken link, NULL-not-zero semantics, and a project-agnostic guard script that fails the build."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [empirical, invariants, data-contracts, fail-high, monitoring, verification]
    related_skills: [empirical-project-playbook, systematic-debugging]
---

# Empirical System Invariants

Batería de invariantes que convierte "¿funciona?" en una respuesta mecánica:
por ciclo, cada etapa del pipeline publica un CONTRATO de datos y un guard lo verifica,
fallando ALTO con el eslabón exacto. La confianza la da la batería completa en verde,
no la memoria del operador.

**Origen:** polymarket-trading-bot (2026). Un sistema de prediction-markets acumuló
`edge_neto`/`edge_bruto` siempre NULL (el código nunca se escribió), `edge_elo/form/casino`
estructuralmente NULL, phantom wirings, y flags que el `.env` no tenía. Nada lo detectaba:
las fallas eran "silencios traidores" hasta que una sesión de debug las encontraba por
suerte. Esta skill es la capa operativa que cierra ese vacío.

## Cuándo usar esta skill

- El sistema genera datos que un consumidor (modelo, guard, venta de feed, dashboard) usa
  para decidir, y no hay contrato que atestigüe que cada etapa pobló lo que promete.
- Antes de confiar en cualquier métrica de producto o veredicto de edge sobre datos de un
  pipeline no verificado.
- Antes de vender un feed de datos: un feed que no puede probar que mide lo que dice no
  se vende ni se confía.
- En cada ciclo de producción (systemd/cron) y bajo demanda (CLI).

## Los 5 contratos de datos (por ciclo)

Verificar en CADA ciclo. Si alguno falla: ciclo ROJO con el eslabón exacto.

1. **Ingest/WS:** ¿entregó books, o procesó estalejos? Contar los stales; ROJO si crece.
   Un reconnect hace todo verse sano 1-2 min — medir durante horas, no segundos.
2. **Modelo:** ¿`model_prob` (o el campo que el siguiente paso consume) pobló valores, o
   escribió NULL? ROJO si el campo consumido está NULL en filas post-deploy.
3. **Señal/enriquecimiento:** ¿los campos de edge/fuentes traen datos o phantom NULL?
   `edge_elo/form/casino` NULL es defecto (nunca se escribió), no dato legítimo.
4. **Guard → orden:** ¿la señal que pasó guards es la misma que salió a orden? No wiring
   fantasma (getattr con default que nadie asigna). Verificar `hasattr` / módulo real.
5. **Shadow/ledger:** ¿vio un book medido, no una fila degenerada sin book? El shadow no
   escribe una fila sin book medido.

## Regla de semáforo

- Ciclo ROJO si al menos un check falla, con el eslabón + valor esperado vs real.
- Confianza = batería completa en verde, NO memoria del operador ni "corre sin error".
- **NULL ≠ 0:** un contrato declara si "campo ausente" es defecto (NULL a corregir) o dato
  legítimo (0 medido). Tratar 0 como fallo eterno → fatiga de alertas.

## Falla alto — nunca swallow

- Cada check fallido loguea eslabón + valor esperado vs real.
- Prohibido `|| true`, `continue-on-error`, `except: pass` en un guard de invariante.
- Un getter de DB que traga excepciones devuelve `[]` en silencio: leer con conexión NUEVA,
  no la del pool (el pool ve su propia transacción sin commit y oculta el bug).
- Verificar el intérprete ANTES de interpretar la salida. `pytest | grep passed || fail`
  da lo mismo con tests rojos que con intérprete inexistente.

## Cómo declarar un contrato (pasos)

1. Para CADA etapa, listar etapa fuente → etapa consumidora → campo prometido.
2. Escribir la CONDICIÓN que atestigua que el campo se pobló (no "hay filas" sino valores
   plausibles en filas post-deploy).
3. Escribir la QUERY o LOG de PRODUCCIÓN que lo demuestra ANTES de escribir el código
   (build con query de aceptación pre-escrita).
4. Agregar el "gemelo de frontera": un test que pruebe que el fixture efectivamente roza
   la cota — si no, el check pasa por accidente.
5. Declarar NULL≠0 por campo.

Ver el detalle en `templates/data-contracts.md`.

## Cómo correrla

- **Por ciclo (prod):** systemd timer o cron que corre el guard y persiste el resultado;
  ROJO → fichero de estado + notify. No depender de logs que rotan.
- **Bajo demanda (CLI):** `python scripts/invariant_guard.py --contract <path.json>`.
  Exit 0 = todos verdes; exit 1 = al menos un ROJO con detalle de eslabón.
- Ejemplo en `scripts/invariant_guard.py` (stdlib, agnóstico, paths anclados a `__file__`
  o inyectados por env — nunca al cwd).

## Pre-deploy gate (opcional, recomendado MONITOR primero)

La batería puede ser solo monitoreo en prod, o también bloquear el deploy si un contrato
no se cumple. Recomendado: monitorear en prod durante HORAS antes de convertirlo en gate;
un gate apurado frena deploys legítimos. Un kill switch flag OFF = el nuevo check no rompe
deploys mientras se estabiliza.

## Cómo verificar esta skill (presence ≠ utility)

1. `skill_view(name='empirical-system-invariants')`; linked_files debe mostrar
   `scripts/` y `templates/`.
2. Correr el script sobre un contrato de prueba que declara un campo NULL → debe devolver
   exit 1 con el eslabón identificado (prueba que DETECTA deuda real, no teoría).
3. La plantilla queda rellenable con los nombres reales del proyecto objetivo.

## Deuda que esta skill convierte en ROJO (ejemplos del fuente)

- `edge_neto`/`edge_bruto` en trades siempre NULL → contrato #3 lo marca ROJO.
- `edge_elo/form/casino` en rejected_signals siempre NULL (infra multi-source diseñada pero
  nunca conectada) → contrato #3.
- Shadow escribiendo fila sin book medido → contrato #5 (bug ya corregido; el check evita
  regresión).
- Flags declarados ON que el `.env` no tiene → contrato #4/#2 (doc vs estado real).

## Relación con el playbook

Esta skill es la capa OPERATIVA de `empirical-project-playbook`. El playbook cataloga la
familia de silencios traidores como conocimiento; esta skill entrega la batería que los
detecta por ciclo y el guard que la ejecuta.

## Fuente canónica

Repo-tap `manusabbath-arch/hermes-skills` (skills/empirical-system-invariants). Los perfiles
locales tienen una COPIA instalada que es la que se carga. Al editar, hacerlo en el repo
(no en la copia), commit + push, y re-propagar. Ver README del repo tap.
