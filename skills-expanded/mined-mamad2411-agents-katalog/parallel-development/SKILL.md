---
name: parallel-development
description: >-
  Set up a git worktree to develop a feature in parallel without touching the
  main working tree. Use at the start of any feature to isolate work in its own
  branch and directory.
---

# parallel-development

Aísla el trabajo de una feature usando un **git worktree** dedicado. Esto permite desarrollar en paralelo sin ensuciar la rama principal ni el working tree actual.

## Cuándo usarlo

- Al iniciar cualquier feature nueva (se invoca desde `/develop-feature`)
- Cuando se quiere trabajar en dos features simultáneamente sin stashes ni cambios de rama

---

## Paso a paso

### 1. Confirmar el nombre de la rama

Derivar un nombre de rama limpio a partir del nombre de la feature:

```bash
# Ejemplo: "autenticación por token" → feature/autenticacion-por-token
BRANCH=feature/<nombre-kebab-case>
```

### 2. Crear la rama y el worktree

```bash
# Desde la raíz del repo
git worktree add ../hermes-<nombre> -b $BRANCH
```

Esto crea:
- Una rama nueva `$BRANCH` basada en el HEAD actual
- Un directorio hermano `../hermes-<nombre>/` con ese checkout

### 3. Trabajar dentro del worktree

Todo el trabajo de la feature ocurre en ese directorio:

```bash
cd ../hermes-<nombre>
# Aquí van: migraciones, modelos, controllers, tests, etc.
```

El directorio principal (`hermes/`) queda limpio y en su rama original.

### 4. Al terminar la feature

Una vez que los tests pasan y el trabajo está listo:

```bash
# Dentro del worktree — pushear la rama
cd ../hermes-<nombre>
git push -u origin $BRANCH
```

### 5. Abrir el PR

Siempre abrir un PR para revisión. **Nunca hacer merge directo a main.**

```bash
gh pr create \
  --title "<título descriptivo de la feature>" \
  --body "$(cat <<'EOF'
## Resumen
- <qué hace este PR>

## Cambios
- <listado de cambios principales>

## Test plan
- [ ] Tests unitarios pasan (`bin/rails test`)
- [ ] Revisión manual del flujo principal
EOF
)"
```

El PR queda abierto para revisión. El worktree se mantiene hasta que el PR sea mergeado.

### 6. Después del merge

Una vez aprobado y mergeado el PR:

```bash
# Volver al repo principal y actualizar
cd ../hermes
git pull

# Limpiar el worktree
git worktree remove ../hermes-<nombre>
```

---

## Reglas

- **Siempre abrir PR** — nunca hacer merge directo a main.
- **No borrar** el worktree hasta que el PR esté mergeado o el usuario lo indique.
- **No usar** `git worktree remove --force` salvo pedido explícito.
- Si el directorio destino ya existe, abortar y avisar al usuario.
- Verificar siempre con `git worktree list` antes de crear uno nuevo con el mismo nombre.

---

## Referencia rápida

```bash
git worktree list                          # ver worktrees activos
git worktree add <path> -b <branch>        # crear
git push -u origin <branch>               # pushear rama
gh pr create --title "..." --body "..."   # abrir PR
git worktree remove <path>                 # limpiar (después del merge)
```
