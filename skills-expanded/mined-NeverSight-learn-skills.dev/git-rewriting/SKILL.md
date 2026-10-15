---
name: git-rewriting
description: "Reescritura de historial en Git. Cubre rebase interactivo (pick, squash, fixup, reword, drop), autosquash, cherry-pick, amend, y cuándo reescribir vs cuándo mantener el historial original. Actívala al limpiar commits antes de PR, reorganizar trabajo, o aplicar commits específicos entre ramas."
disable-model-invocation: true
---

# Git History Rewriting

Guía de reescritura de historial con rebase interactivo y cherry-pick.

---

## Regla de oro

> **Nunca reescribir commits que ya fueron pusheados a una rama compartida.**

Reescribir es seguro en:
- ✅ Ramas locales (antes de push)
- ✅ Ramas de feature personales (si nadie más trabaja en ella)

Peligroso en:
- ❌ `main`/`develop` (ramas compartidas)
- ❌ Commits que otros ya tienen en su repositorio

---

## Rebase interactivo

```bash
# Editar últimos 5 commits
git rebase -i HEAD~5

# Editor se abre con:
pick a1b2c3d feat(orders): add create endpoint
pick e4f5g6h fix: typo in validation
pick i7j8k9l feat(orders): add list endpoint
pick m0n1o2p WIP: tests
pick q3r4s5t feat(orders): add cancel endpoint
```

### Comandos del rebase interactivo

| Comando | Efecto |
|---------|--------|
| `pick` | Usar commit tal cual |
| `reword` | Editar mensaje del commit |
| `squash` | Fusionar con commit anterior (conserva ambos mensajes) |
| `fixup` | Fusionar con commit anterior (descarta mensaje) |
| `drop` | Eliminar commit |
| `edit` | Pausar para modificar el commit |
| `break` | Pausar el rebase (abrir shell) |

### Ejemplo: limpiar antes de PR

```bash
# Commits originales:
# 1. feat: add create endpoint
# 2. fix typo
# 3. feat: add list endpoint
# 4. WIP tests
# 5. feat: add cancel endpoint

# Después de rebase:
pick a1b2c3d feat(orders): add CRUD endpoints  # 1+2+3+5 squash
pick m0n1o2p test(orders): add integration tests  # 4 reword
```

```bash
git rebase -i HEAD~5
# Cambiar a:
# pick a1b2c3d feat(orders): add create endpoint
# fixup e4f5g6h fix: typo           # Se fusiona con el anterior
# squash i7j8k9l feat(orders): add list endpoint  # Se fusiona, editar mensaje
# reword m0n1o2p WIP: tests         # Cambiar mensaje
# squash q3r4s5t feat: add cancel    # Se fusiona
# Luego editar mensaje combinado
```

---

## Autosquash

```bash
# Hacer commit con fixup/squash automático

# Commit original
git commit -m "feat(orders): add create endpoint"

# Commit de fix con mensaje especial
git commit -m "fixup! feat(orders): add create endpoint"

# Rebase con autosquash
git rebase -i --autosquash HEAD~3
# El fixup se coloca automáticamente debajo del commit correcto
```

---

## Amend (modificar último commit)

```bash
# Modificar mensaje del último commit
git commit --amend -m "feat(orders): add create endpoint with validation"

# Agregar archivos olvidados al último commit
git add forgotten-file.ts
git commit --amend --no-edit  # No cambia el mensaje

# ⚠️ Solo si el commit NO fue pusheado
```

---

## Cherry-pick

```bash
# Aplicar un commit específico a la rama actual
git cherry-pick a1b2c3d

# Cherry-pick rango de commits
git cherry-pick a1b2c3d..e4f5g6h  # De a1 (exclusive) a e4 (inclusive)

# Cherry-pick sin hacer commit (para editar antes)
git cherry-pick -n a1b2c3d

# Resolver conflicto en cherry-pick
git cherry-pick a1b2c3d
# ... resolver conflicto ...
git add .
git cherry-pick --continue
git cherry-pick --abort  # Cancelar
```

### Cuándo usar cherry-pick vs merge

| Cherry-pick | Merge/Rebase |
|-------------|--------------|
| ✅ Hotfix debe ir a main y a release | ✅ Integrar feature completa |
| ✅ Un commit específico de otra rama | ❌ Copiar commits sueltos entre ramas |
| ❌ Sincronizar ramas completas | ✅ Sincronizar ramas |

---

## Git 2.54 — `git history` (experimental)

```bash
# Reword commit antiguo sin rebase completo del rango
git history reword a1b2c3d

# Dividir un commit grande en varios
git history split e4f5g6h
# Git pausa y permite crear múltiples commits desde los cambios de e4f5g6h
```

⚠️ Experimental en 2.54. Puede cambiar. Alternativa estable: `git rebase -i`.

---

## Checklist rewriting

- [ ] Solo reescribir ramas locales o personales
- [ ] Squash de WIP/typos antes de PR
- [ ] Autosquash para fixups automáticos
- [ ] Amend solo para commits no pusheados
- [ ] Cherry-pick solo para commits aislados (hotfixes)
- [ ] `git push --force-with-lease` (no `--force`) si reescribiste rama remota
- [ ] Comunicar al equipo si force-pusheaste una rama compartida
