---
name: onboard-project
description: Bootstrap un projet existant ou nouveau avec le stack standard Claude Code (CLAUDE.md projet, .gitignore, .editorconfig, pre-commit, GitFlow, structure). À invoquer sur un nouveau repo ou pour industrialiser un repo existant.
---

# Skill : Onboard Project

Initialise un projet avec toute l'infrastructure de dev standardisée (normes, hooks, GitFlow, config Claude).

## Procédure

### 1. Détecter l'état du projet

```bash
ls -la
git status 2>&1
git branch -a 2>&1
cat README.md 2>/dev/null | head -20
# Détection langages :
ls *.tf 2>/dev/null             # Terraform
ls *.py pyproject.toml 2>/dev/null   # Python
ls package.json 2>/dev/null     # JS/TS
ls composer.json 2>/dev/null    # PHP
ls Dockerfile 2>/dev/null       # Docker
```

### 2. Demander confirmation sur

- Nom du projet (pour le `CLAUDE.md`)
- Description courte
- Stack détectée (proposer + valider)
- Si repo existant : confirmer qu'on peut modifier

### 3. Installer le script bootstrap

Exécuter `~/.claude/bin/claude-init-project.sh` (qui fait toutes les étapes ci-dessous). Voir section manuelle si besoin de customiser.

### 4. Étapes manuelles détaillées

#### a) Git init (si pas déjà un repo)
```bash
git init
git checkout -b main      # default
git commit --allow-empty -m "Initial commit"
git checkout -b develop
```

#### b) Installer `.editorconfig`
```bash
cp ~/.claude/templates/.editorconfig .
```

#### c) Installer `.gitignore` (fusionner avec existant si présent)
```bash
# Si pas de .gitignore :
cp ~/.claude/templates/.gitignore .

# Si existant : ajouter en tête les lignes CLAUDE.md / .claude/
```

#### d) Installer `.pre-commit-config.yaml` (filtré par langages)
```bash
cp ~/.claude/templates/.pre-commit-config.yaml .
# Commenter les sections non pertinentes (ex: PHP si pas de .php)
```

#### e) Installer `.yamllint`
```bash
cp ~/.claude/templates/.yamllint .
```

#### f) Créer `CLAUDE.md` projet
```bash
cp ~/.claude/templates/CLAUDE.md.template CLAUDE.md
# Remplacer {{PROJECT_NAME}} et remplir les sections
```

#### g) Init pre-commit
```bash
pip install --user pre-commit    # si pas déjà installé
pre-commit install
pre-commit install --hook-type commit-msg
# Premier run (peut échouer sur formatage existant → fix automatique)
pre-commit run --all-files || true
```

#### h) Init GitFlow (si git-flow installé)
```bash
if command -v git-flow >/dev/null; then
    git flow init -d
else
    # Manuel : s'assurer que main + develop existent
    git checkout -b develop 2>/dev/null || true
    git checkout develop
fi
```

#### i) Structure docs
```bash
mkdir -p docs/adr docs/runbooks
touch docs/adr/.gitkeep
```

#### j) Premier commit structuré (demander validation)
```bash
git add .
git status      # montrer à l'utilisateur avant commit
# Si OK :
git commit -m "chore: bootstrap project with standard tooling"
```

### 5. Mémoire

Créer dans `~/.claude/projects/<hash>/memory/` :
- `project_overview.md` : objectif, stack, contraintes
- `project_stack.md` : détail techniques (versions, deps critiques)

### 6. Rapport final

```
## Bootstrap terminé — <nom projet>

✅ Fichiers installés : .editorconfig, .gitignore, .pre-commit-config.yaml, CLAUDE.md
✅ Branches : main, develop
✅ Hooks : pre-commit activés
✅ Docs : docs/adr/, docs/runbooks/
✅ Memory seed : project_overview.md, project_stack.md

Prochaines étapes suggérées :
1. Remplir le CLAUDE.md (contexte spécifique du projet)
2. Installer les deps (`npm install`, `composer install`, `pip install -e .[dev]`, etc.)
3. `pre-commit run --all-files` pour valider la base

Commit initial prêt à pousser : `git push -u origin main develop`
(pas fait automatiquement — attente de ton Go)
```

## Règles

- **Jamais** écraser un `CLAUDE.md` / `.pre-commit-config.yaml` existant sans confirmation
- **Vérifier** les outils requis (`pre-commit`, `git-flow`) et signaler les manquants
- **Respecter** les langages détectés (ne pas imposer PHP sur un projet JS)
- **Le premier commit** doit être validé par l'utilisateur avant d'être fait
