---
name: matriz
description: Ordena los pendientes anotados en el cerebro en una matriz costo × impacto y elige las 3 tareas del día o distribuye la semana. Usar con /matriz, "ordená mi semana", "qué hago hoy". No ejecuta los pendientes.
argument-hint: "[\"hoy\" para solo las 3 de hoy, o \"semana\"]"
---

# /matriz — la semana en cuatro cuadrantes

## 1 · Relevar (solo lo anotado)

Barré, y si tu herramienta tiene subagentes, en paralelo:
- `changelog/` del mes + los últimos 7 días del anterior: todo lo marcado como pendiente, falta, sin dueño, decisión sin tomar.
- `WIKI/`: buscá `pendiente|falta|sin dueño|bloqueado|decidir`.
- `OUTPUTS/` de los últimos 7 días: preguntas sin contestar, plazos hacia adelante.
- `RUTINAS/log/` de la semana: hallazgos que siguen abiertos.
- Si la persona pasó una lista propia en el mensaje, entra entera.

Cada ítem: tarea en ≤15 palabras · quién (solo la persona / la IA / un tercero) · desde cuándo · fuente.

## 2 · Clasificar

- **Impacto alto** solo si mueve lo que `WIKI/negocio.md` dice que es el objetivo, o evita que un problema se repita. Lo demás es bajo.
- **Costo = minutos de la persona.**
- Si lo puede hacer la IA sin su cara, su voz, su decisión ni sus credenciales → casillero **"va al cerebro"**, no entra a la matriz.
- Deduplicá: el mismo ítem aparece con tres redacciones.
- Lo que una decisión posterior ya mató → se tacha.

| | Costo bajo | Costo alto |
|---|---|---|
| **Impacto alto** | **Q1 · hacelo ya** | **Q2 · bloque profundo** |
| **Impacto bajo** | **Q3 · en tanda** | **Q4 · se tacha o se delega** |

## 3 · Entregar

`OUTPUTS/AAAA-MM-DD-matriz-semana.md`, en este orden:
1. Q1 (tarea · minutos · desde · qué desbloquea)
2. Q2 (tarea · día propuesto)
3. Q3 en una línea
4. Q4 con veredicto
5. Va al cerebro: una línea, pide un solo OK
6. **Lo que más viene postergando:** las 5 más viejas que son solo suyas, con días
7. La semana: **3 tareas por día = 1 de Q2 + 2 de Q1**, respetando su agenda (`WIKI/yo.md`)
8. **Decisiones en bloque**: numeradas, opciones A/B/C con **(reco)**. Nunca abiertas.

En el chat: 3-4 líneas (las 3 de hoy, la más postergada, link al output). Con `hoy`: solo las 3 de hoy, sin output nuevo.

## Reglas

- Lo que no está anotado en el cerebro no está en la matriz. No inventes.
- Minutos estimados se dicen estimados.
- Un ítem que pasa dos semanas en Q1 no era de bajo costo: se reclasifica o se delega, y se dice.
- Si la persona corrige una clasificación, gana ella y el porqué se anota.
