---
name: "plan-vivo"
description: "Mantener el plan vivo de gazetrack (plan.json): al planificar, al escribir prompts para el agente y al cerrar cada prompt. Fases, tiempos y visor del kit plan-vivo."
---

# Plan vivo de gazetrack

gazetrack lleva su plan en `plan.json`, en la raiz del repo (`c:\xampp\htdocs\focus\plan.json`): fases, items (prompts), puertas e imprevistos, con estimados y tiempos reales. Se ve en un visor con fases, linea de tiempo y mapa.

## Donde esta el kit

- El kit vive SOLO en `C:\xampp\htdocs\plan-vivo`. Nunca se copia a este repo; aqui solo esta `plan.json` (y, si hace falta, `asignaciones.json`).
- La fuente de verdad del formato y las reglas es `C:\xampp\htdocs\plan-vivo\AGENTES.md`. Leerlo antes de crear o modificar el plan; esta skill no repite su detalle.
- Zona del proyecto: `America/Guayaquil` (-05:00).

## Comandos (PowerShell, desde la raiz del proyecto)

```
pnpm --dir C:\xampp\htdocs\plan-vivo validar -- --plan c:/xampp/htdocs/focus/plan.json
pnpm --dir C:\xampp\htdocs\plan-vivo visor   -- --plan c:/xampp/htdocs/focus/plan.json
pnpm --dir C:\xampp\htdocs\plan-vivo tiempos -- --plan c:/xampp/htdocs/focus/plan.json
pnpm --dir C:\xampp\htdocs\plan-vivo migrar  -- --plan c:/xampp/htdocs/focus/plan.json
```

- Usar barras normales en la ruta del plan: desde Git Bash los `\` de una ruta de Windows se comen.
- El visor abre en http://localhost:5190 (un solo visor sirve todos los proyectos; si ya esta abierto, el comando le suma este plan y da su direccion). No detenerlo ni levantar otro en otro puerto.
- `tiempos` y `migrar` sin `--aplicar` solo muestran la tabla de diferencias; mostrarla antes de aplicar.

## Al escribir prompts para el agente (orquestador)

- La PRIMERA linea del prompt es el identificador, por ejemplo `F8 · P14: <titulo>`. Nada antes, ni texto pegado. `tiempos` asigna los tramos por ese identificador.
- Lo que aparezca sin planear se agrega como item `unplanned` en la fase donde ocurrio; no se esconde dentro de otro item.

## Al cerrar un prompt (agente)

1. Actualizar a mano el item: `status`, `summary` (una linea), `steps`, `files_changed`, `notes`; y `updated_at` en la raiz. Las fases no llevan `status`.
2. Correr `tiempos` sin `--aplicar`, revisar la tabla y luego `--aplicar`. El `work_log` no se escribe a mano (salvo tramos del orquestador y los `"manual": true`).
3. Correr `validar`.
4. Incluir `plan.json` en el commit del prompt.
5. Cuando se necesite que el usuario haga algo (un comando, una confirmacion, una decision), pedirlo con AskUserQuestion: es la senal de espera que reconoce el script.

## Fallos o mejoras del kit

No se arreglan desde este proyecto ni se copia el kit aqui. Se anotan en `C:\xampp\htdocs\plan-vivo\PENDIENTES.md` (fecha, proyecto de origen, que pasa, como reproducirlo, prioridad), se avisa en una linea y se sigue.

## Nota de historial

El plan se creo el 2026-10-18 reconstruyendo las fases 1, 1B y 2 (2A/2A.1/2B/2B.1/2C) y las mejoras post-fase desde `PROJECT.md` y los timestamps de archivos/commits: las sesiones de Claude Code de julio no se conservaron, asi que esos tramos van marcados `"manual": true` con duracion aproximada. Los prompts nuevos si deben llevar su identificador para que `tiempos` los reconstruya solo.
