---
name: git-collaboration
description: "Colaboración en Git. Cubre Pull Requests efectivos, code review, merge strategies (squash, rebase, merge commit), resolución de conflictos, CODEOWNERS, branch protection rules, y etiqueta de equipo. Actívala al definir el proceso de PR, mejorar code reviews, o resolver conflictos complejos."
disable-model-invocation: true
---

# Git Collaboration & Code Review

Guía de colaboración con Git y GitHub. PRs, code review, merge strategies.

---

## Pull Request efectivo

### Template (.github/PULL_REQUEST_TEMPLATE.md)

```markdown
## What

[Descripción breve de los cambios]

## Why

[Contexto del problema y por qué esta solución]

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing steps:

## Checklist

- [ ] Conventional commits used
- [ ] Lint passes
- [ ] Type check passes
- [ ] Tests pass locally
- [ ] No secrets committed
- [ ] Breaking changes documented
```

### Buen PR

```
Título: feat(orders): add order cancellation endpoint with email notification

Commits:
  feat(orders): add cancel endpoint
  feat(orders): add cancellation email notification
  test(orders): add cancellation integration tests

Descripción:
  Closes #1234

  - Validates order is in cancellable status
  - Sends email notification on cancellation
  - Refunds payment if already charged

  Breaking: none
```

### Mal PR

```
Título: fix

Commits:
  WIP
  fix typo
  feat(orders): add stuff
  asdf
  fix

Descripción: (vacía)
```

---

## Code Review

### Para el reviewer

```markdown
# ✅ Buen review
"Nice approach. What happens if the order is already shipped? Could we add a guard for that?"

# ❌ Mal review
"This is wrong." (sin explicar por qué)
"Rewrite this." (sin sugerir alternativa)
```

### Review checklist

- [ ] ¿Resuelve el problema descrito?
- [ ] ¿Hay tests que cubran el cambio?
- [ ] ¿Hay edge cases no considerados?
- [ ] ¿Sigue las convenciones del proyecto?
- [ ] ¿Hay código duplicado con otro lado?
- [ ] ¿Los nombres son claros y descriptivos?
- [ ] ¿Hay código comentado o debug logs?
- [ ] ¿Los mensajes de commit son descriptivos?
- [ ] ¿Se actualizó la documentación si es necesario?

---

## Merge Strategies

| Estrategia | Resultado | Cuándo |
|------------|-----------|--------|
| **Squash and merge** | Todos los commits → 1 commit en main | ✅ Default para features. Historia limpia. |
| **Rebase and merge** | Commits se aplican secuencialmente sin merge commit | Cuando quieres preservar commits individuales bien escritos |
| **Merge commit** | Crea `Merge pull request #X` | Releases, merges entre ramas long-lived |

```bash
# Squash merge (recomendado)
# PR → "Squash and merge"
# Resultado: 1 commit limpio en main

# Rebase merge
# PR → "Rebase and merge"
# Resultado: commits reescritos secuencialmente

# Evitar merge commits en feature → main
# (genera ruido: "Merge pull request #123 from feature/orders")
```

---

## Branch Protection Rules (GitHub)

```
Settings → Branches → Add branch protection rule

Branch name pattern: main

✅ Require a pull request before merging
  ✅ Require approvals: 1
  ✅ Dismiss stale reviews when new commits are pushed

✅ Require status checks to pass before merging
  ✅ lint
  ✅ typecheck
  ✅ test (coverage)
  ✅ build

✅ Require conversation resolution before merging
✅ Require branches to be up to date before merging
❌ Do not allow bypassing the above settings
```

---

## CODEOWNERS

```bash
# .github/CODEOWNERS
# Cada archivo/directorio tiene dueños que deben aprobar PRs

# Dueños globales
* @team-leads

# Backend
src/api/** @backend-team
src/infrastructure/** @backend-team

# Frontend
src/app/** @frontend-team
src/components/** @frontend-team

# Database migrations
migrations/** @backend-team @dba-team

# CI/CD
.github/** @platform-team
Dockerfile @platform-team
```

---

## Resolución de conflictos

```bash
# Al hacer rebase o merge:
git rebase main
# CONFLICT in src/orders.ts

# 1. Ver archivos con conflicto
git status

# 2. Editar archivo (marcadores <<<<<<, ======, >>>>>>)
#   o usar VS Code: "Accept Current | Accept Incoming | Accept Both"

# 3. Marcar como resuelto
git add src/orders.ts

# 4. Continuar
git rebase --continue
# o cancelar todo:
git rebase --abort
```

### Estrategia para conflictos complejos

```bash
# Ver solo archivos con conflicto
git diff --name-only --diff-filter=U

# Ver ambos lados del conflicto
git show :2:src/orders.ts  # Nuestra versión (main)
git show :3:src/orders.ts  # Su versión (feature)

# Usar una versión completa
git checkout --ours src/config.ts   # Nuestra versión
git checkout --theirs src/config.ts # Su versión
```

---

## Etiqueta de equipo

- ✅ **PRs pequeños.** <400 líneas cambiadas. Se revisan en <30 min.
- ✅ **Un PR = una responsabilidad.** No mezclar refactor + feature + bug fix.
- ✅ **Responder reviews en <24h.** No bloquear al compañero.
- ✅ **No hacer push directo a main.** Siempre vía PR.
- ✅ **No mergear tu propio PR sin review.** Otra persona debe aprobar.
- ✅ **Mantener PR actualizado.** Rebase sobre main frecuentemente.
- ✅ **Si el PR es grande, avisar.** Mejor: partirlo en PRs más pequeños.

---

## Checklist colaboración

- [ ] PR template con checklist
- [ ] Conventional commits en mensajes de PR y commits
- [ ] Squash merge para features → main
- [ ] Branch protection: requiere PR + CI + approve
- [ ] CODEOWNERS configurado para módulos críticos
- [ ] PRs revisados en <24h
- [ ] Conflictos resueltos con rebase, no merge de main en feature
- [ ] No mergear propio PR sin review
- [ ] PRs pequeños (<400 líneas), un propósito por PR
