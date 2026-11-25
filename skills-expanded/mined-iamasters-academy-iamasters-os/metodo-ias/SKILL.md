---
name: metodo-ias
description: "Método I.A.S. (Intención · Acción · Síntesis) para trabajar con IA agéntica sin AI brain fry. Dos modos: diario (planificación previa con checklist verde/rojo y decisiones congeladas) y semanal (recap macro con inventario, Pareto, boundary erosion, recalibración de techo y delegables). USAR cuando el usuario diga 'método IAS', 'I.A.S.', 'planifica sesión', 'planificación previa', 'checklist intención', 'recap semanal', 'síntesis semanal', 'AI brain fry', 'me estoy quemando con la IA', 'cuello de botella IA agéntica', 'micro-decisiones', 'decisiones congeladas', 'boundary erosion', 'ratchet effect', 'mountain of outputs', o tras un viernes/fin de iteración con sensación de deuda invisible."
version: "0.1.0"
---

# Método I.A.S.

## Qué es

I.A.S. es un método de productividad para operar con IA agéntica sin colapsar. Tres letras, una idea por letra: **Intención** (qué quiero producir y con qué inputs), **Acción** (el agente ejecuta sin abrir microdecisiones nuevas), **Síntesis** (qué cerró y qué sigue abierto).

El método responde a dos problemas operativos concretos en cualquier flujo agéntico:

1. La fase de Acción se contamina con micro-decisiones que vacían el tanque del operador.
2. La salida acumulada de outputs no se procesa y se convierte en deuda invisible.

## Cuándo activarse

- El usuario verbaliza "AI brain fry", "me estoy quemando", "demasiadas micro-decisiones", "el agente no termina en una pasada".
- El usuario va a abrir una sesión larga con un agente y quiere planificar antes de ejecutar.
- Es viernes / fin de iteración y el usuario quiere cerrar la semana con un recap estructurado.
- El usuario nota síntomas de boundary erosion (días sin parada, agentes corriendo de noche) o ratchet effect (cada win sube el listón sin parada negociada).
- El usuario menciona el método I.A.S., I.A.S., Intención Acción Síntesis.

## Cuándo NO activarse

- Tareas atómicas que no necesitan planificación previa (un mensaje, una búsqueda, un retoque).
- El usuario ya está dentro de la fase A con un agente en marcha y no quiere parar para planificar.
- El usuario pide brainstorm puro o ideación divergente: ahí encaja mejor `seis-sombreros` o `strategy-web-research`.
- Auditorías post-mortem profundas de una entrega: usar otra skill de auditoría si existe en el repo.

## Dos modos

La skill tiene dos ciclos independientes pero conectados. El protocolo de cada uno vive en su propio archivo:

### Modo diario — Hipótesis 1 (planificación previa)

- **Disparador:** apertura de sesión con IA agéntica.
- **Protocolo:** `protocolos/h1-planificacion.md`.
- **Salida:** un activo por sesión guardado en `projects/metodo-ias/diarios/YYYY-MM-DD-{slug}.md`.
- **Idea:** la fase I se vuelve checklist verde/rojo; no se ejecuta A hasta que I esté completo. Bloque de decisiones congeladas que el agente no puede re-cuestionar.

### Modo semanal — Hipótesis 2 (recap macro)

- **Disparador:** viernes o fin de iteración.
- **Protocolo:** `protocolos/h2-recap-semanal.md`.
- **Salida:** `projects/metodo-ias/semanales/YYYY-Www.md` con cinco bloques fijos: inventario, Pareto 80/20, boundary erosion, recalibración del techo, delegables.
- **Idea:** una S macro semanal cierra el ciclo; sin ella el método es un embudo abierto.

Si el protocolo correspondiente no existe en el momento de invocar el modo, la skill avisa al usuario y para.

## Comandos disponibles

| Comando | Modo | Stub |
|---------|------|------|
| `/ias-start` | Diario (H1) | `comandos/ias-start.md` |
| `/ias-recap` | Semanal (H2) | `comandos/ias-recap.md` |

Los comandos son la entrada normal a la skill. La skill también responde a triggers en lenguaje natural según el frontmatter.

## Formato de salida esperado

- **Diario (H1):** archivo Markdown en `projects/metodo-ias/diarios/YYYY-MM-DD-{slug}.md` con 8 secciones planas definidas en `protocolos/h1-planificacion.md`: `objetivo`, `inputs`, `restricciones`, `formato`, `criterios de aceptación`, `decisiones congeladas`, `resultado`, `lecciones`. Las 6 primeras se cierran al terminar I; las 2 últimas al cerrar la sesión.
- **Semanal (H2):** archivo Markdown en `projects/metodo-ias/semanales/YYYY-Www.md` con cinco bloques numerados.
- **Resumen en chat:** la skill devuelve siempre un resumen breve en chat además del archivo. Sin emojis. Español.

## Persistencia entre sesiones

- Por defecto se escribe en `projects/metodo-ias/` dentro del repo del OS donde se invoca la skill.
- Si la skill se ejecuta en un cliente (`clients/<nombre>/`), escribir en `clients/<nombre>/projects/metodo-ias/`.
- Si el operador la invoca fuera de un repo OS, fallback a `~/.claude/metodo-ias-outputs/diarios/` y `~/.claude/metodo-ias-outputs/semanales/`.
- No se inventa ninguna API ni servicio externo: todo es archivo local Markdown.

## Dependencia entre modos

H2 lee la última semana de la carpeta `diarios/` para construir el inventario. Si en la semana hay menos de 3 sesiones diarias registradas, el modo semanal sigue corriendo pero avisa al usuario en el bloque de inventario de que el sample es bajo y la S macro será aproximada.

## Skills relacionadas en el OS

- **`decisions-log`** — el modo H1 puede append decisiones congeladas al log de decisiones del operador, no solo al archivo diario.
- **`meta-wrap-up`** — el modo H2 encaja con el ritual de cierre semanal del OS. Si ya existe un wrap-up activo, integrarse en lugar de duplicar.
- **`seis-sombreros`** — si en la fase I aparece una decisión que merece análisis multi-perspectiva, invocar seis-sombreros antes de congelar la decisión.

## Reglas anti-drift

- Comunicación en español. Código en inglés.
- Cero emojis en archivos generados.
- No inventar datos. Si falta un dato del usuario, preguntarlo o marcarlo como `[pendiente]` en el archivo.
- No saltar de I a A si I no está completo (regla H1).
- No abrir decisiones nuevas durante A si están en el bloque de "decisiones congeladas" (regla H1).
- No ejecutar el recap semanal sin haber leído los diarios de la semana en curso (regla H2).
- Sin gold-plating: la skill termina cuando el archivo de salida está escrito y el resumen en chat entregado.
- **Jerga interna invisible al usuario.** Términos como "gate", "dimensión roja", "fase I", "8 secciones", "contrato H1↔H2", paths del repo, no aparecen en lo que el usuario lee en chat. La skill habla como una persona experta. Detalle del tono y ejemplos en `comandos/ias-start.md` y `comandos/ias-recap.md`.
