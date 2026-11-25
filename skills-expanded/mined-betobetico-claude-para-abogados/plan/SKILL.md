---
name: plan
description: >
  Planificador de estudio a largo plazo para estudiantes de derecho y opositores.
  Genera un calendario con sesiones de estudio, repaso y evaluación basado en la fecha
  del examen, las materias, las horas disponibles y el histórico de sesiones. Se adapta
  dinámicamente según los resultados. Usar cuando el usuario dice "plan de estudio",
  "planifica mi estudio", "calendario de estudio", "cómo organizo el tiempo", o necesita
  estructurar su preparación.
argument-hint: "[fecha de examen, materias, horas disponibles por semana]"
---

# /plan

1. Leer `~/.claude/plugins/config/claude-para-abogados/estudiante-derecho/CLAUDE.md` — perfil del estudiante.
2. Recopilar datos: examen, materias, disponibilidad, nivel actual.
3. Generar el plan de estudio.
4. Si hay histórico de sesiones, adaptar el plan a los resultados.

---

## Propósito

Generar un plan de estudio realista y ejecutable que distribuya las materias, los repasos y las evaluaciones en el tiempo disponible. El plan se adapta a los resultados reales del estudiante — no es estático.

## Datos necesarios

| Dato | Obligatorio | Ejemplo |
|---|---|---|
| Fecha del examen | Sí | 15 de septiembre de 2026 |
| Tipo de examen | Sí | Acceso a la abogacía / oposición de judicatura / examen de Civil II |
| Materias/asignaturas | Sí | Civil, Penal, Administrativo, Laboral, Procesal, Deontología |
| Horas disponibles/semana | Sí | 25 horas/semana |
| Días de estudio/semana | Sí | 5 días (lunes a viernes) |
| Nivel actual por materia | Recomendado | "Civil: bien, Penal: regular, Administrativo: flojo" |
| Sesiones anteriores | Si hay | Resultados de fichas, IRAC, test |

## Principios de planificación

### 1. Distribución del tiempo

| Fase | Proporción | Contenido |
|---|---|---|
| Estudio nuevo | 40% | Temas que no se han visto nunca |
| Repaso | 30% | Temas ya vistos — consolidación |
| Práctica/evaluación | 20% | Test, casos prácticos, fichas, socrático |
| Descanso/buffer | 10% | Imprevistos, descanso activo |

### 2. Regla de repaso espaciado

Cada tema se repasa según este calendario (adaptación del sistema de repetición espaciada):

| Repaso | Cuándo | Tipo |
|---|---|---|
| Repaso 1 | 1 día después de estudiar | Lectura rápida de esquema |
| Repaso 2 | 3 días después | Fichas / autoevaluación |
| Repaso 3 | 1 semana después | Test o caso práctico |
| Repaso 4 | 2 semanas después | Exposición oral o IRAC |
| Repaso 5 | 1 mes después | Simulacro integrado |

### 3. Priorización de materias

| Criterio | Mayor tiempo | Menor tiempo |
|---|---|---|
| Peso en el examen | Materias con más preguntas | Materias con menos peso |
| Nivel del estudiante | Materias débiles (más tiempo) | Materias dominadas (mantenimiento) |
| Dificultad intrínseca | Materias complejas | Materias más asequibles |

### 4. Sesiones tipo

| Tipo de sesión | Duración | Contenido |
|---|---|---|
| Estudio intensivo | 2-3 horas | Tema nuevo: lectura + esquema + fichas |
| Repaso | 1-1,5 horas | Repasar esquema + practicar fichas |
| Evaluación | 1,5-2 horas | Test / caso práctico / IRAC |
| Socrático | 30-45 min | Sesión de preguntas sobre tema reciente |
| Simulacro | 4 horas | Examen completo en condiciones reales |

## Formato de salida

```markdown
## Plan de estudio: [Tipo de examen]

**Fecha del examen:** [fecha]
**Semanas disponibles:** [N]
**Horas/semana:** [N]
**Total de horas disponibles:** [N]

---

### Distribución por materia

| Materia | Peso examen | Nivel actual | Horas asignadas | % del total |
|---|---|---|---|---|
| [materia] | [%] | [nivel] | [horas] | [%] |

### Calendario semanal

#### Semana 1: [fechas]

| Día | Sesión 1 (mañana) | Sesión 2 (tarde) | Tipo |
|---|---|---|---|
| Lunes | [Materia] — Tema [N] | [Repaso] — Fichas [materia] | Estudio + repaso |
| Martes | [Materia] — Tema [N] | [Evaluación] — Test [materia] | Estudio + evaluación |
| ... | | | |

#### Semana 2: [fechas]

[Mismo formato]

[Continuar para todas las semanas]

### Hitos y simulacros

| Semana | Hito | Evaluación |
|---|---|---|
| [semana X] | Completar [materia] — primer pase | Simulacro parcial |
| [semana Y] | Completar todas las materias | Simulacro completo |
| [semana Z] | Repaso final | Simulacro en condiciones reales |
| Última semana | Repaso ligero + descanso | No introducir materia nueva |

### Reglas del plan

1. **No estudiar materia nueva en la última semana.** Solo repaso y descanso.
2. **Un simulacro completo como mínimo 2 semanas antes del examen.**
3. **Si un test sale < 60%, dedicar sesión extra a esa materia la semana siguiente.**
4. **Día de descanso completo cada 7-10 días.**
5. **Si se acumula retraso > 1 semana, replanificar — no intentar recuperar sacrificando descanso.**

---

**Qué hacer a continuación:**
1. **Empezar** — arranco con la primera sesión del plan.
2. **Ajustar** — modifico horas, materias o prioridades.
3. **Registrar sesión** — tras estudiar, registro resultados para adaptar el plan.
4. **Fichas** — `/estudiante-derecho:fichas` para la sesión de hoy.
5. **Otra cosa** — dime qué necesitas.
```

## Adaptación dinámica

Si el estudiante registra resultados de sesiones (tests, fichas, IRAC):

- **Materia con resultados < 50%:** incrementar horas asignadas en un 20%.
- **Materia con resultados > 80%:** reducir horas y pasar a mantenimiento.
- **Tema que se falla repetidamente:** sesión socrática + esquema antes de volver a evaluar.

## Guardarraíles

- **El plan debe ser realista.** Si el estudiante tiene 15 horas/semana y 12 materias, decirlo: "Con este tiempo, no podrás cubrir todas las materias en profundidad. Hay que priorizar."
- **No sacrificar descanso.** Un plan que no incluye descanso es un plan que no se cumple. El rendimiento cae drásticamente sin descanso.
- **No todo es memorización.** Alternar entre estudio, práctica y evaluación. Solo leer no prepara un examen.
- **No acumular deuda de repaso.** Si el estudiante no repasa, el estudio nuevo se pierde. Mejor avanzar más despacio y repasar que cubrir mucho sin consolidar.
- **La última semana es sagrada.** No introducir materia nueva. Solo repaso ligero y descanso. El estudiante que estudia hasta la víspera llega agotado.
- **Adaptar al ritmo real, no al ideal.** Si el plan dice 5 horas/día y el estudiante hace 3, ajustar el plan a 3 — no insistir en un plan que no se cumple.
