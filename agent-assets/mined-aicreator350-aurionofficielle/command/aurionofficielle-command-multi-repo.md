Coordonner des opérations entre les 11 outils Aurion.

## Usage
`/github:multi-repo [action]`

## Actions
- `sync-deps` — Synchroniser les dépendances entre tous les outils
- `deploy-all` — Déployer tous les outils (`node scripts/deploy-all-tools.cjs`)
- `health-check` — Vérifier le health de tous les outils déployés
- `update-env` — Mettre à jour une env var sur tous les outils

## Instructions

1. Lister les 11 outils dans `tools-deploy/`
2. Exécuter l'action demandée sur chaque outil
3. Collecter les résultats
4. Afficher le rapport avec statut par outil

## Format
```
📦 Multi-Repo: [action]

| Outil | URL | Statut | Détails |
|-------|-----|--------|---------|
| chat  | chat-aurion1.vercel.app | ✅/❌ | ... |
| ide   | ide-aurion1.vercel.app  | ✅/❌ | ... |
| ...   | ... | ... | ... |
```
