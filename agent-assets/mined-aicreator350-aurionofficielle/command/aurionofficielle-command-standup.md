# Standup Report

Génère un rapport de standup automatique basé sur l'activité récente.

## Instructions

1. **Activité Git**
   - `git log --oneline --since="yesterday"` → commits récents
   - `git diff --stat HEAD~10` → fichiers modifiés récemment
   - Branches actives : `git branch -a --sort=-committerdate | head -5`

2. **État des outils**
   - Vérifie PROGRESS.md pour l'état de chaque outil
   - Note les outils modifiés récemment

3. **Format du rapport**
   ```
   # Standup — [date]

   ## ✅ Fait hier
   - [liste basée sur les commits]

   ## 🔄 En cours
   - [basé sur les branches ouvertes et PROGRESS.md]

   ## ⏳ Prévu aujourd'hui
   - [basé sur les issues assignées et gaps.md]

   ## 🚧 Blockers
   - [le cas échéant]
   ```

4. **Métriques**
   - Commits : X
   - Fichiers modifiés : X
   - Lignes ajoutées/supprimées : +X/-X
