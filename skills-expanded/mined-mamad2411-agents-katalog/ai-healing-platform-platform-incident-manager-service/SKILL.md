# REGLAS DE DESARROLLO POR SPRINTS (CIERRE AUTÓNOMO)

1. **CONTEXTO INICIAL:** Antes de cualquier acción, lee obligatoriamente `sprints/sprint-review.md`. Es tu única fuente de verdad para el alcance actual.

2. **CICLO DE TRABAJO (TDD-Iterativo):**
   a. Implementar funcionalidad mínima requerida.
   b. Ejecutar suite de tests del módulo.
   c. En caso de fallo: Analizar logs -> Corregir -> Re-testear hasta éxito.
   d. En caso de éxito: Marcar objetivo con `[x]` en el archivo actual.

3. **PROCEDIMIENTO DE CIERRE DE SPRINT (Crítico):**
   Al completar el 100% de los objetivos:
   a. **Propuesta:** Generar sección "Sugerencias para el próximo Sprint" basada en la deuda técnica o mejoras detectadas del proyecto actual.
   b. **Persistencia:** Renombrar el archivo actual a: `sprints/sprint-YYYY-MM-DD-titulo-del-sprint.md`.
   c. **Sucesión:** Crear un nuevo archivo `sprints/sprint-review.md` vacío con la estructura estándar, volcando los objetivos sugeridos y aprobados.

4. **RESTRICCIONES:**
   - NO asumas requerimientos fuera de `sprint-review.md`.
   - NO propongas sprints fuera del proyecto actual.
   - NO consideres un sprint terminado sin que los tests pasen en verde.
   - Si un error persiste tras 3 intentos, detente y pide feedback humano antes de seguir.