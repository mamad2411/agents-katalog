---
name: debrief
description: Extrae conclusiones, decisiones y tareas de la sesión actual, propone los formatos y actualiza los archivos locales del proyecto en peter-brain.
---

# 📝 Skill: Debrief (Sesión de Cierre)

Este skill se activa cuando el usuario solicita cerrar la sesión, hacer un resumen, o explícitamente ejecutar un `/debrief`. Su objetivo es asegurar la coherencia de memoria en la arquitectura multi-harness.

## 📌 Reglas de Operación
1.  **Identificar el Foco:** Analiza el historial de chat para entender qué proyecto o área de `peter-brain` fue el centro de la sesión.
2.  **Propuesta de Cambios:** Antes de modificar cualquier archivo en el disco, debes presentarle al usuario una propuesta detallada en el chat con:
    *   **Entrada de Bitácora (`log.md`):** Siguiendo el formato estricto (Foco, Conclusiones, Decisiones, Tareas).
    *   **Decisión Estratégica (`knowledge.md`):** Si se tomaron decisiones de arquitectura o producto en la sesión.
    *   **Nuevas Tareas (`todo.md`):** Si surgieron pendientes (con su emoji de prioridad, tag del proyecto, ID autoincremental y agente).
3.  **Confirmación Humana:** Espera a que el usuario apruebe o ajuste la propuesta.
4.  **Escritura Directa:** Una vez confirmado, actualiza los archivos reales correspondientes en el cerebro principal del usuario (raíz del repo `peter-brain`).
5.  **Commit de Git:** Ejecuta un `git add` + `git commit` automático en la carpeta de `peter-brain` con el formato `[nombre-proyecto] debrief YYYY-MM-DD`.

---

## 📋 Formato de Propuesta a Mostrar

### 1. Entrada propuesta para `log.md`
```markdown
## YYYY-MM-DD
**Foco**: [Tema principal de la sesión]
**Conclusiones**:
- [Punto clave 1]
- [Punto clave 2]
**Decisiones**:
- [Decisión tomada y justificación]
**Tareas generadas**: [ids de las tareas creadas o "—"]
```

### 2. Entrada propuesta para `knowledge.md` (si aplica)
```markdown
- **YYYY-MM-DD**: [Decisión tomada + razonamiento breve]
```

### 3. Tareas propuestas para `todo.md` (si aplica)
*   Formato: `- [ ] Descripción de la tarea [Prioridad emoji] #[tag] 📅 YYYY-MM-DD 🤖 [agente] id:[id-único-autoincremental]`
