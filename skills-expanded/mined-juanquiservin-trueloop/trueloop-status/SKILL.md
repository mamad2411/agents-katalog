---
name: trueloop-status
description: Muestra el tablero de un loop TRUELOOP en curso - fase, iteración, estado de cada agente, veredicto de QA, blockers, checkpoints de git y gasto. Úsalo cuando el usuario escriba /trueloop-status o pregunte cómo va el loop, qué están haciendo los agentes, en qué va el proyecto o cuánto lleva gastado.
---

# TRUELOOP · Status

Lee el estado desde disco. **No inventes nada y no adivines**: si un archivo no está,
dilo. El punto de este comando es que el humano confíe en lo que ve.

## Qué leer

1. `.trueloop/STATE.json` - la fuente de verdad
2. `.trueloop/USAGE_STATE.json` - si hay pausa por límite de uso
3. `.trueloop/QA.md` - los últimos hallazgos
4. `.trueloop/ISSUES.md` - problemas abiertos
5. `git log --oneline -5` en la rama del loop

Si no existe `.trueloop/STATE.json`, dilo claro: no hay ningún loop en este proyecto,
y ofrece arrancar uno con `/trueloop`.

## Formato de salida

```
╔══ TRUELOOP · <nombre> ═══════════════════════════════════════╗
 ESTADO      LOOPING            ITERACIÓN  7 / 12
 FASE        VERIFYING          QA         FAIL
 GASTO       $3.42 / $10.00     TIEMPO     2h 14m

 AGENTES
   planner   WAITING    -                    SPEC v3 · 23 criterios
   builder   WORKING    T-014                3 archivos, tests locales OK
   qa        TESTING    verify:T-014         FAIL AUTH-04

 CRITERIOS   19 / 23 pasan
 BLOCKERS    ISS-003 (ALTA) bypass de auth con token vencido
 GIT         trueloop/reservas · último bueno e5f6a7b · HEAD c9d0e1f
 SIGUIENTE   Builder corrige expires_at en el middleware
╚══════════════════════════════════════════════════════════════╝
```

## Reglas de lectura

- Si `loop_status = PAUSED_USAGE`, muestra la hora de reanudación **y** el
  `parse_method`. Si dice `default`, avisa explícitamente: *"la hora de reset no se
  pudo leer; es una espera calculada, no leída."* Fingir precisión que no existe es
  peor que decir que no se sabe.
- Si `loop_status = STALLED`, no lo maquilles. Di qué se repitió y propón las tres
  salidas: descomponer la tarea · spawnear un especialista · pedir decisión al humano.
- Si `loop_status = BLOCKED`, lo primero de la respuesta es **qué necesita del humano**.
- Si el gasto va arriba del 80% del presupuesto, márcalo.
- Si `unchanged_rounds > 0`, avísalo antes de que dispare el stall.

## Después del tablero

Una sola línea con lo más útil que puede hacer ahora, no una lista de opciones.
Si todo va bien: dilo y ya. No inventes trabajo para el humano.
