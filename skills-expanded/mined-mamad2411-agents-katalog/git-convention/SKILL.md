---
name: git-convention
description: Standard de référence pour la gestion de Git. Règles de sécurité, workflows atomiques, conventions de commit et bonnes pratiques de configuration.
---

# Git Convention

Standards de gestion de version pour Agents et Développeurs. Ce skill doit être utilisé pour toute opération Git (commit, push, checkout) ou demande d'aide sur Git.

## Priorités de Référence

| Priority | Category | Impact | Reference File |
|----------|----------|--------|----------------|
| 1 | Sécurité | CRITICAL | [security.md](references/security.md) |
| 2 | Workflow | HIGH | [workflow.md](references/workflow.md) |
| 3 | Recovery | HIGH | [recovery.md](references/recovery.md) |
| 4 | Configuration | MEDIUM | [config.md](references/config.md) |

## Quick Reference

### 1. Sécurité (CRITICAL)
- **Vérifier** `git status` avant `git add`
- **Jamais** de `--force` sur branches protégées (main/master)

### 2. Workflow (HIGH)
- **Atomique** : 1 commit = 1 changement logique
- **Conventional** : `Header` + `Body` + `Footer` (Strict)
- **Branches** : Pas de dev direct sur main

### 3. Recovery (HIGH)
- **Amend** : Pour corrections mineures pré-push
- **Restore** : Pour annuler proprement

### 4. Configuration (MEDIUM)
- **Identité** : Vérifier user.name/email
- **Gitignore** : Ignorer `.env`, `node_modules`
