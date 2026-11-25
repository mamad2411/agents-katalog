---
name: acceso
description: >
  Preparación del examen de acceso a la abogacía (examen oficial para colegiarse como
  abogado/a en España). Formato: test de 100 preguntas + caso práctico. Materias:
  civil, penal, administrativo, laboral, mercantil, procesal, deontología. Se adapta
  a las áreas débiles del estudiante. Usar cuando el usuario dice "acceso a la abogacía",
  "examen de acceso", "preparo el acceso", "test de acceso", o está preparando el
  examen de habilitación profesional.
argument-hint: "[materia específica o 'simulacro completo'] [área débil si la conoce]"
---

# /acceso

1. Leer `~/.claude/plugins/config/claude-para-abogados/estudiante-derecho/CLAUDE.md` — perfil del estudiante.
2. Determinar la materia o modalidad de práctica.
3. Generar el ejercicio adaptado.

---

## Propósito

Preparar al estudiante para el examen de acceso a la abogacía con práctica realista: preguntas tipo test y casos prácticos en el formato oficial. Se adapta a las áreas débiles del estudiante para maximizar la eficiencia del estudio.

## Estructura del examen de acceso

| Parte | Formato | Contenido | Duración |
|---|---|---|---|
| Test | 100 preguntas (4 opciones, 1 correcta) | Todas las materias | 4 horas |
| Caso práctico | Supuesto con preguntas tipo test y desarrollo | 1 área del derecho | Incluido en las 4 horas |

### Baremo

- Respuesta correcta: +1 punto.
- Respuesta incorrecta: -0,33 puntos.
- En blanco: 0 puntos.
- Aprobado: 50% de la puntuación máxima (habitualmente) [verificar baremo vigente].

## Distribución por materias (orientativa)

| Materia | N.o aprox. de preguntas | Peso |
|---|---|---|
| Civil y mercantil | ~25-30 | Alto |
| Penal | ~15-20 | Medio-alto |
| Administrativo | ~15-20 | Medio-alto |
| Laboral y Seguridad Social | ~10-15 | Medio |
| Procesal (civil y penal) | ~10-15 | Medio |
| Deontología y ejercicio profesional | ~5-10 | Bajo-medio |
| Caso práctico | ~10-15 preguntas sobre el caso | Alto |

## Modalidades de práctica

### 1. Test por materia

- El estudiante elige una materia.
- Se generan 10-25 preguntas tipo test de esa materia.
- Nivel examen de acceso (no nivel oposición — es más asequible).
- Tras responder: explicación detallada de cada opción.

### 2. Simulacro completo

- 50-100 preguntas de todas las materias (proporcional al examen real).
- Caso práctico incluido.
- Cronometrado si el estudiante quiere.
- Resultado con análisis por materia.

### 3. Refuerzo de áreas débiles

- Si el perfil del estudiante indica áreas débiles, generar preguntas concentradas en esas áreas.
- Dificultad progresiva: empezar con preguntas más asequibles, subir gradualmente.

### 4. Caso práctico

- Supuesto de hechos realista (extensión similar al examen).
- Preguntas tipo test sobre el caso + preguntas de desarrollo corto.
- Materia: civil, penal, administrativo o laboral (según convocatoria).

## Formato de salida (ejemplo: test por materia)

```markdown
## Examen de acceso — Test: [Materia]

**N.o de preguntas:** [N]
**Tiempo sugerido:** [minutos]
**Baremo:** correcta +1 / incorrecta -0,33 / blanco 0

---

**1.** [Enunciado]

a) [Opción A]
b) [Opción B]
c) [Opción C]
d) [Opción D]

[Repetir]

---

## Soluciones y explicaciones

**1.** Correcta: [letra]
[Explicación de por qué es correcta y por qué las demás no]

[Repetir]

### Resultado

| Materia | Correctas | Incorrectas | Blanco | Puntos |
|---|---|---|---|---|
| [materia] | [N] | [N] | [N] | [puntuación] |

### Análisis

**Fortalezas:** [temas donde acierta]
**Debilidades:** [temas donde falla]
**Recomendación:** [qué repasar]

---

**Qué hacer a continuación:**
1. **Repasar errores** — profundizo en las preguntas falladas con explicaciones.
2. **Refuerzo** — test centrado en tus áreas débiles.
3. **Caso práctico** — practico el caso práctico de [materia].
4. **Simulacro completo** — test de todas las materias.
5. **Otra cosa** — dime qué necesitas.
```

## Guardarraíles

- **Nivel de acceso, no de oposición.** El examen de acceso es más asequible que una oposición. No generar preguntas de nivel oposición.
- **Baremo realista.** Aplicar la penalización de -0,33 — el estudiante debe aprender a gestionar las respuestas en blanco.
- **No inventar artículos.** Mejor "el CC regula esto en el Título de obligaciones" que inventar un número de artículo que no existe.
- **Adaptar a las áreas débiles.** Si el perfil del estudiante indica que suspende laboral, concentrar esfuerzo ahí.
- **Deontología no es relleno.** Muchos estudiantes la ignoran y pierden puntos fáciles. Incluir siempre preguntas de deontología.
- **El caso práctico es decisivo.** Muchos aprueban o suspenden por el caso. Dedicar práctica específica.
- **Verificar el formato vigente.** El formato del examen puede cambiar entre convocatorias. Advertir al estudiante que confirme el formato de su convocatoria.
