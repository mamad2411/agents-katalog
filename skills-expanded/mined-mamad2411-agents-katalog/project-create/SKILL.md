---
name: project-create
description: Crear un proyecto nuevo fusionando una plantilla del equipo según el stack tecnológico (Angular, React, Symfony, etc.). Usar siempre que el usuario pida crear un proyecto nuevo, inicializar desde plantilla, o use `/project-create`. Si el stack no está claro, preguntar antes de cualquier acción.
---

# Skill: Crear proyecto desde proyecto base

Fusiona la plantilla del equipo al repo del usuario según el stack elegido.
**No modifica repositorios remotos de plantilla.**

## Flujo obligatorio

### 1 · Confirmar stack

Si el usuario no indicó un `stack_id` explícito → **listar stacks disponibles y preguntar; parar aquí.**

Stacks disponibles:

| `stack_id` | Referencia |
|------------|-----------|
| `angular`  | `references/angular.md` |

Si el usuario pide un stack distinto a los stacks disponibles → indicar que aún no está disponible; no continuar con merge.

### 2 · Leer referencia

Leer **completo** `references/<stack_id>.md` antes de cualquier comando git.

- Si el archivo no existe → avisar al usuario; **no improvisar URL, rama ni sustituciones; parar.**

### 3 · Preparar repo

Verificar `.git` en la raíz de trabajo. Si no existe → `git init` o clonar según indique el usuario.

### 4 · Ejecutar pasos git

Seguir **exactamente** los pasos git de `references/<stack_id>.md` (remote, fetch, merge…).

- Si el nombre de remote ya existe con otra URL → acordar con el usuario antes de continuar.
- Si el merge produce conflictos → listar paths en conflicto, orientar resolución manual, **parar hasta que el usuario los resuelva.**

### 5 · Post-merge

Ejecutar el resto de pasos de la referencia en el orden del documento (personalización de nombres/IDs/envs, `npm install`, etc.).

### 6 · Cerrar

Confirmar al usuario que el proyecto fue creado exitosamente.

---

## Restricciones

- **Nunca** iniciar `git merge` sin `stack_id` confirmado.
- **Nunca** asumir Angular u otro stack por defecto.
- **Nunca** obtener URL de plantilla desde memoria; solo desde `references/<stack_id>.md`.
- **Nunca** modificar repositorios remotos de plantilla.

---

## Ejemplos

| Input | Acción |
|-------|--------|
| «Quiero un proyecto Angular nuevo» | `stack_id = angular` → leer `references/angular.md` → ejecutar flujo |
| `/project-create` sin stack | Listar stacks disponibles → preguntar → parar |
| Stack sin `references/<stack>.md` | Avisar; no ejecutar merge |