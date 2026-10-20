---
name: rails-routes
description: "Generate and maintain Rails routes reference file. Use when routes-reference.txt is missing or outdated."
allowed-tools: Bash(bundle exec rails routes:*), Bash(echo:*), Bash(chmod:*), Bash(grep:*)
---

# Rails Routes

**Contexte :** Générer et maintenir `data/routes-reference.txt` pour que les autres skills puissent connaître les routes disponibles sans deviner.

## Workflow

### 1. Seed initial

Vérifier si `data/routes-reference.txt` existe :
```bash
grep -q routes data/routes-reference.txt
```
Si absent ou vide → générer :
```bash
bundle exec rails routes > data/routes-reference.txt
```

### 2. Git hook post-commit

Vérifier si le hook contient déjà la commande :
```bash
grep -q "rails routes" .git/hooks/post-commit
```
Si absent → installer :
```bash
echo 'bundle exec rails routes > data/routes-reference.txt' >> .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```
