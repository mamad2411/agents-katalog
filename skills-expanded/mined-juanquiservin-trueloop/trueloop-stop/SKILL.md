---
name: trueloop-stop
description: Detiene un loop TRUELOOP en curso de forma limpia, con checkpoint de git y estado persistido para poder reanudar después. Úsalo cuando el usuario escriba /trueloop-stop, /trueloop-pause, o pida parar, pausar, congelar o apagar el equipo de agentes.
---

# TRUELOOP · Stop

Parar bien importa tanto como arrancar bien. Un loop mal detenido pierde trabajo,
deja el repo a medias y hace imposible retomar.

## Antes de parar

Pregunta una sola cosa si no está claro por el mensaje del usuario:

- **PAUSA** → se retoma después con `/trueloop -Resume`. El estado queda intacto.
- **ALTO DEFINITIVO** → se cierra el proyecto y se produce el reporte final.

Si el usuario dice "párale" sin más, asume **PAUSA**: es reversible, y lo irreversible
nunca es el default.

## Secuencia de apagado

1. **Señal de alto**: crea `.trueloop/STOP` con el motivo y la fecha. Los workers la
   revisan entre tareas y cierran solos al terminar lo que traen en la mano - nunca a
   media herramienta.
2. **Espera al turno en curso.** Matar un agente a media escritura corrompe archivos.
   Si lleva más de 5 minutos, dile al usuario que puede cerrar el panel manualmente.
3. **Checkpoint de git**: commitea lo que haya en la rama del loop con
   `trueloop: checkpoint de pausa <fecha>`. Nunca a `main`, nunca `--force`.
4. **Persiste el estado**: actualiza `STATE.json` con
   `loop_status = PAUSED_USER` (pausa) o `DONE`/`BLOCKED` (alto definitivo),
   y `timestamps.finished_at`.
5. **Actualiza `HANDOFF.md`** para que quien retome - humano o agente fresco - sepa
   exactamente dónde quedó, qué se intentó y qué no vale la pena reintentar.
6. **Registra en `RUN_LOG.md`** el motivo del alto.

## Reporte de cierre

```
╔══ TRUELOOP · DETENIDO ═══════════════════════════════════════╗
 MOTIVO       pausa solicitada por el usuario
 ESTADO       PAUSED_USER · iteración 7 de 12
 AVANCE       19 de 23 criterios pasan
 GASTO        $3.42 de $10.00
 CHECKPOINT   c9d0e1f en trueloop/reservas-barberia
 ÚLTIMO BUENO e5f6a7b
 PENDIENTE    AUTH-04 · validar expires_at en el middleware
 RETOMAR      /trueloop -Resume  (desde este mismo proyecto)
╚══════════════════════════════════════════════════════════════╝
```

## Si era alto definitivo

Encadena con `/trueloop-report` para producir el handoff completo. El usuario tiene que
poder entender su propio sistema después de la automatización - ese es el examen final
de TRUELOOP, no que el código compile.

## Nunca

- Nunca borres `.trueloop/`. Es la memoria del proyecto.
- Nunca hagas `git reset` al parar. Parar no es revertir.
- Nunca dejes el repo sin commitear. Trabajo sin checkpoint es trabajo que se puede perder.
