Afficher le statut complet de la hive active.

## Usage
`/hive:status`

## Instructions

1. Afficher l'état de la queen (type, tâche principale, progression)
2. Lister tous les workers actifs avec :
   - Type et rôle assigné
   - Statut (idle, working, done, failed)
   - Score de qualité (truth-score)
3. Montrer le consensus en cours (votes, résultat)
4. Afficher la mémoire collective (entrées récentes)
5. Calculer la progression globale

## Format
```
👑 Hive Status
Queen: [type] — [tâche]
Consensus: [type] — [résultat ou en cours]

| Worker | Type | Tâche | Statut | Score |
|--------|------|-------|--------|-------|
| ...    | ...  | ...   | ...    | ...   |

📊 Progression: X% — [X/Y tâches terminées]
🧠 Mémoire: [N] entrées — dernière: [résumé]
```
