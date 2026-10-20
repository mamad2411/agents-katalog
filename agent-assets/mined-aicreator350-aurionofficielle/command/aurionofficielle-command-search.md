Rechercher dans la mémoire persistante des agents.

## Usage
`/memory:search [query]`

## Instructions

1. Chercher dans tous les namespaces de mémoire
2. Supporter la recherche par :
   - Mot-clé exact
   - Préfixe de namespace
   - Recherche sémantique (similarité)
3. Retourner les résultats triés par pertinence
4. Afficher : clé, valeur résumée, score de confiance, date

## Format de sortie
```
🔍 Résultats pour "[query]" — [N] trouvés

| Clé | Résumé | Confiance | Date |
|-----|--------|-----------|------|
| ... | ...    | ...       | ...  |
```
