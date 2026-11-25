---
name: crear-rutina
description: Convierte una skill o un proceso con reglas fijas en una rutina que corre sola (subir de Nivel 2 a Nivel 3) — verifica que califica, elige dónde corre (nube, compu en la nube o script), escribe RUTINAS/<slug>.md con el contrato, explica cómo programarla y la prueba. Usar con /crear-rutina, "que esto corra solo", "automatizá esto todos los días".
argument-hint: "[el proceso o la skill, ej. \"revisar campañas cada 30 minutos\"]"
---

# /crear-rutina — que corra sin que vos aprietes nada

Una rutina es una skill que se dispara sola: **cada X tiempo o cuando pasa algo**. No todo tiene que terminar en rutina.

## 1 · ¿Califica? Las tres preguntas, en orden

1. ¿Se hace 2-3 veces por semana o más? **No** → no es rutina.
2. ¿Necesitás ver el resultado antes de que salga? **Sí** → se queda en Nivel 2. *(Una rutina puede igual dejar el borrador listo cada mañana: eso sí vale. Lo que no hace es enviarlo.)*
3. ¿Se puede escribir como *"si pasa X, hacé Y"*? **No** → se queda en Nivel 2.

Ejemplos para que la persona lo vea claro:
- ❌ *"Haceme 10 creativos por día y subilos."* Querés verlos antes. Es Nivel 2.
- ✅ *"Si el ROAS de la campaña supera mi vara, subí el presupuesto un 20%."* La regla la escribiste vos; la rutina solo la cumple.
- ✅ *"Todas las mañanas buscá cobros rebotados y disputas abiertas y avisame."* Detecta y avisa. No decide.

**Delegá la ejecución, nunca el criterio.** Si la rutina toca dinero, clientes o publicaciones, por defecto es **solo lectura + aviso + borrador**. Escribir o ejecutar algo final requiere que la persona lo diga explícito, y queda anotado en el prompt.

## 2 · Escribí las reglas

Con la persona, en formato:
- **Disparador:** cada cuánto (o qué evento).
- **Reglas:** `si <condición medible> → <acción>`. Cada condición con su número y su vara.
- **Qué NUNCA hace.**
- **A quién avisa y cómo** (notificación, mail, un archivo que lee el resumen diario).
- **Qué pasa si falla una fuente** (un 401, un timeout): eso **nunca** se reporta como "todo bien".

## 3 · Elegí dónde corre

| Si la rutina… | Corre en… | Por qué |
|---|---|---|
| Es todo API y deja el resultado en el repo | **La nube de tu IA** (en Claude Code: *routines*, se crean con `/schedule` o desde claude.ai/code) | No depende de que nada esté prendido |
| Necesita un navegador logueado o mucho cómputo (render de video) | **Una computadora en la nube** (una Mac o una VM remota con tus accesos) | Tiene el navegador con tus sesiones y potencia |
| Es una cuenta determinista, sin juicio (*"si ROAS > X, subí Y"*), cada pocos minutos | **Un script con cron** (por ejemplo GitHub Actions con secrets) y la IA solo para el resumen diario | Una IA por cada latido cada 15 minutos gasta tokens sin necesidad y se puede quedar sin cupo justo cuando hace falta |
| — | **Nunca tu computadora personal como base** | Se apaga en silencio cuando la cerrás, y no podés trabajar mientras la IA la usa |

## 4 · Escribí el prompt en el repo

`RUTINAS/<slug>.md`, siguiendo el contrato de `RUTINAS/README.md`. Estructura:

```markdown
# <slug> — <qué vigila o hace, en una línea>

Sos una rutina <cadencia> del segundo cerebro de <nombre>. Leé `RUTINAS/README.md` (contrato) antes de arrancar.

## Fuentes
- …

## Reglas
- si … → …

## Nunca
- …

## Qué escribís
`RUTINAS/log/AAAA-MM-DD/<slug>.md`: primera línea `OK` · `HALLAZGOS n` · `ERROR <razón>`. Después los hallazgos (nuevo / cambió / sin cambios en una línea).

## Aviso
Cuándo y cómo avisa. Una línea.
```

Sumala a la tabla de `RUTINAS/README.md` y a la lista de esperadas de `RUTINAS/vigia.md`.

## 5 · Programala (esto lo hace la persona, vos la guiás)

1. El repo tiene que estar en GitHub (privado) y con el prompt ya pusheado.
2. En Claude Code: `/schedule` → *"Creá una rutina <cadencia> que lea RUTINAS/README.md y RUTINAS/<slug>.md y lo ejecute"*. O desde claude.ai/code → Routines.
3. Las keys que necesite van en el **entorno de la rutina**, nunca en el repo. Las pega la persona.
4. Conectores: solo los que la rutina usa. Ni uno más.

## 6 · Probala

- Corréla a mano una vez y leé el log que dejó.
- **Una rutina no está viva hasta que su primer aviso llegó.** Escrita, programada, ejecutada y verificada son cuatro estados distintos. Decí en cuál quedó.
- Entrada arriba en `changelog/AAAA-MM.md`.
