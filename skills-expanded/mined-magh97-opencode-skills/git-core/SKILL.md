---
name: git-core
description: "Guía principal de Git (v2.54): init, clone, add, commit, push, pull, fetch, remote, status, log, diff, stash, .gitignore, configuración y aliases. Úsala para cualquier tarea Git o troubleshooting básico."
---

# Git Core Guide

Guía canónica de Git v2.54 (2026). Fundamentos que todo dev debe dominar.

---

## Configuración inicial

```bash
git config --global user.name "Miguel Galvan"
git config --global user.email "miguel.galvan@example.com"

# Editor por defecto
git config --global core.editor "code --wait"  # VS Code

# Autocorrect typos
git config --global help.autocorrect 20  # Ejecuta automáticamente después de 2s

# Push por defecto (solo rama actual)
# (ya es el comportamiento por defecto desde Git 2.0, no hace falta configurarlo)
git config --global push.default simple

# Rebase por defecto al pull (evita merge commits innecesarios)
git config --global pull.rebase true

# Mejor diff
git config --global diff.algorithm histogram
git config --global diff.colorMoved zebra

# Aliases útiles
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate --all -20"
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
```

---

## Ciclo básico

```bash
# Crear repo
git init
git clone https://github.com/mi-org/miapp.git

# Ver estado
git status
git status -s  # Compacto

# Stage + commit
git add src/orders.ts           # Archivo específico
git add -p src/orders.ts        # Stage interactivo (hunks)
git add .                        # Todo (solo en repo conocido)

git commit -m "feat(orders): add create order endpoint"
git commit -m "$(printf 'feat(orders): add create endpoint\n\n- Validate input with Zod\n- Return 201 on success')"

# Push / Pull
git push origin main
git pull --rebase origin main    # Sin merge commits

# Fetch (traer cambios sin merge)
git fetch origin
git diff origin/main             # Ver qué cambió antes de integrar
```

---

## .gitignore

```gitignore
# Dependencias
node_modules/
__pycache__/
.venv/
*.pyc

# Build
dist/
build/
*.tsbuildinfo

# Secrets
.env
.env.local
*.pem
*.key

# IDE
.vscode/settings.json
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Terraform
*.tfstate
*.tfstate.*
.terraform/
```

---

## Log y diff

```bash
# Log formatos útiles
git log --oneline --graph --decorate --all  # Árbol completo
git log -5                                 # Últimos 5 commits
git log --since="2026-06-01" --until="2026-06-23"
git log --author="Miguel"
git log --grep="feat"                       # Commits con "feat" en mensaje
git log -S"functionName"                    # Commits que tocaron "functionName"
git log -- main.py                          # Commits que tocaron main.py

# Diff
git diff                    # Working tree vs staged
git diff --staged           # Staged vs HEAD
git diff main..feature      # Diferencia entre ramas
git diff HEAD~3             # Diff contra 3 commits atrás
git diff --word-diff        # Diff palabra por palabra (no línea)
```

---

## Stash

```bash
git stash                    # Guardar cambios sin commit
git stash -m "WIP: order validation"  # Con mensaje
git stash -u                 # Incluir archivos untracked

git stash list
git stash pop                # Aplicar último stash y eliminarlo
git stash apply stash@{1}    # Aplicar stash específico

git stash drop stash@{0}     # Eliminar stash
git stash clear              # Eliminar todos
```

---

## Ramas

```bash
# Crear y cambiar
git branch feature/order-creation
git checkout feature/order-creation
git checkout -b fix/duplicate-email   # Crear + cambiar (atajo)

# Listar
git branch                   # Locales
git branch -r                # Remotas
git branch -a                # Todas

# Eliminar
git branch -d feature/old    # Delete local (merged)
git branch -D feature/old    # Forzar delete (no merged)
git push origin --delete feature/old  # Delete remota
```

---

## Remotes

```bash
git remote -v                # Listar remotes
git remote add upstream https://github.com/original/miapp.git
git remote rename origin upstream
git remote remove origin

# Sincronizar con fork upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## Hooks compartidos

```bash
# Apuntar a un directorio de scripts versionado (en vez de .git/hooks/, que no se versiona)
git config core.hooksPath .githooks
```

Para reescribir historial (reword, split, squash) usa `git rebase -i` (ver `git-rewriting`).

---

## Reglas de oro

1. **Commits atómicos.** Un cambio lógico = un commit. No mezclar refactor + feature.
2. **Mensajes descriptivos.** `feat(orders): add validation` no `fix stuff`.
3. **Pull con rebase.** `git pull --rebase` evita merge commits basura.
4. **Nunca commitear secrets.** `.env` en `.gitignore`. Usar `.env.example`.
5. **Hacer push frecuente.** No acumular 3 días de trabajo local.
6. **Revisar `git status` y `git diff` antes de commit.**
7. **No commitear archivos generados** (`dist/`, `build/`, `node_modules/`).

---

## Sub-skills del kit

> 📁 Cada sub-skill tiene su propio `SKILL.md` con el detalle; el subagente `.opencode/agent/git.md` decide cuál cargar según la tarea.


| Skill | Cuándo cargarla |
|-------|-----------------|
| `git-branching` | GitFlow, GitHub Flow, Trunk-Based, Conventional Commits |
| `git-rewriting` | Rebase interactivo, squash, fixup, cherry-pick |
| `git-recovery` | Reflog, bisect, revert, reset, restore |
| `git-collaboration` | PRs, code review, merge strategies, conflict resolution |
| `git-advanced` | Hooks, worktrees, submodules, git-lfs, monorepo patterns |

---

## Stack recomendado

| Propósito | Herramienta |
|-----------|-------------|
| GUI | VS Code Git, GitLens, Sublime Merge |
| Hooks | Husky 9 o config-based hooks (Git 2.54) |
| Conventional commits | commitlint + husky |
| Release automático | semantic-release |
| Monorepo | Turborepo + conventional commits |
