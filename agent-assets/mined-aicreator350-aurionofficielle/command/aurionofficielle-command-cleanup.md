Nettoyer les entrées mémoire obsolètes ou de faible valeur.

## Usage
`/memory:cleanup`

## Instructions

1. Scanner toutes les entrées mémoire
2. Identifier les candidats au nettoyage :
   - Entrées > 30 jours sans consultation
   - Score de confiance < 0.3
   - Entrées dupliquées
   - Entrées sans source valide
3. Demander confirmation avant suppression
4. Supprimer et rapporter le nombre d'entrées nettoyées
5. Consolider les entrées similaires restantes
