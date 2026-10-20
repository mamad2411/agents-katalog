Créer une release GitHub avec changelog automatique.

## Usage
`/github:release [version]`

## Instructions

1. Déterminer le bump de version (major/minor/patch) :
   - major : breaking changes
   - minor : nouvelles features
   - patch : fixes et améliorations
2. Générer le changelog depuis le dernier tag :
   - Grouper par type (feat, fix, perf, security, docs)
   - Inclure les PRs mergées
3. Mettre à jour package.json avec la nouvelle version
4. Créer le tag Git
5. Préparer la release note GitHub
6. Confirmer avant push

## Format changelog
```markdown
## [X.Y.Z] — YYYY-MM-DD
### ✨ Features
### 🐛 Fixes
### ⚡ Performance
### 🔒 Security
### 📝 Documentation
```
