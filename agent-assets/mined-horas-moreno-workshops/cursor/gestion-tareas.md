---
description: 
globs: 
alwaysApply: true
---
description: Siempre usa el script de gestión de tareas para cualquier acción sobre tareas, estado o bloqueos.
globs: ["tasks.md", "status.md"]

---
- No edites manualmente los archivos tasks.md ni status.md.
- Usa siempre el script workshop/cursor_task_manager.sh para agregar, completar o bloquear tareas.
- Mantén el estado del proyecto actualizado tras cada acción.
- Si el usuario solicita una acción sobre tareas, ejecuta el script correspondiente en modo no interactivo.
