# Context Token Optimizer

Optimisation de l'utilisation des tokens de contexte pour Claude Code.

## Instructions

1. **Audit du contexte actuel**
   - CLAUDE.md : nombre de lignes, tokens estimés
   - AGENTS.md : nombre de lignes, tokens estimés
   - .claude/skills/ : nombre de skills, taille totale
   - .claude/commands/ : nombre de commandes, taille totale
   - .claude/settings.json : configuration

2. **Analyse de redondance**
   - Informations dupliquées entre CLAUDE.md et AGENTS.md
   - Skills qui se chevauchent
   - Commandes avec du contenu identique
   - Sections de documentation jamais référencées

3. **Classement par utilité**
   | Fichier | Taille | Fréquence d'usage | Garder/Compresser/Supprimer |
   |---------|--------|-------------------|---------------------------|
   |         |        |                   |                           |

4. **Optimisations**
   - Compresser les sections peu utilisées
   - Déplacer le contenu de référence vers des fichiers séparés
   - Utiliser des liens vers la doc plutôt que tout inclure
   - Réduire les exemples verbeux en one-liners
   - Supprimer les TODO/WIP obsolètes

5. **Résultat**
   - Tokens avant : ~N
   - Tokens après : ~N
   - Réduction : X%
   - Informations perdues : aucune (juste réorganisée)
