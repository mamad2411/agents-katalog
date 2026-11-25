---
name: trueloop-say
description: Envía feedback humano en vivo a un loop TRUELOOP en curso sin interrumpirlo. Úsalo cuando el usuario escriba /trueloop-say, o cuando quiera corregir el rumbo, agregar un requisito, cambiar una prioridad o decirle algo al equipo de agentes mientras trabaja.
argument-hint: <lo que le quieres decir al equipo>
---

# TRUELOOP · Say

El humano manda. Este comando mete su voz al loop **sin romper nada**.

## Cómo funciona

El orquestador lee `.trueloop/FEEDBACK.md` **entre iteraciones**, nunca a media
herramienta. Así el feedback llega rápido pero jamás corrompe un turno en curso.
Después lo archiva en `.trueloop/archive/` para que quede el rastro.

## Qué haces

1. Verifica que exista `.trueloop/STATE.json`. Si no hay loop corriendo, dilo y
   ofrece arrancar uno.
2. **Anexa** (nunca sobreescribas) a `.trueloop/FEEDBACK.md`:

```markdown
## 2026-08-08 14:32
<el mensaje del usuario, tal cual>
```

3. Si el mensaje es ambiguo sobre a quién va dirigido, agrega una línea de contexto
   tuya para que el orquestador lo enrute bien. Ejemplo: *"(dirigido al Planner: es un
   cambio de requisito, no un bug)"*.
4. Confirma en una línea: qué se envió y cuándo lo va a leer el loop.

## Clasifica antes de escribir

Ayuda al orquestador diciéndole de qué tipo es:

| Tipo | Señal | Efecto |
|---|---|---|
| **CORRECCIÓN DE RUMBO** | "no, mejor así" | El Planner actualiza SPEC |
| **REQUISITO NUEVO** | "también necesito X" | Nueva tarea + nuevo criterio de aceptación |
| **PRIORIDAD** | "primero esto" | Se reordena TASKS.md |
| **RESPUESTA A BLOQUEO** | contesta una pregunta de ISSUES.md | Desbloquea y el loop sigue |
| **ALTO** | "párale" | Sugiere `/trueloop-stop`, que hace checkpoint antes de parar |

## Si el loop está en BLOCKED

Ese es el caso ideal para este comando: el loop está detenido esperando exactamente
esta decisión. Escribe el feedback **y** dile al usuario que el loop reanudará solo
en cuanto lo lea.

## Si el loop está en PAUSED_USAGE

El feedback se guarda igual y se lee al reanudar. Dile al usuario a qué hora será eso,
para que no se quede esperando una respuesta que no va a llegar antes.
