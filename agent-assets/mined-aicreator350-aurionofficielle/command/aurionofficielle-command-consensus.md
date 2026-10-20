Lancer un vote de consensus entre les agents de la hive.

## Usage
`/hive:consensus [question]`

## Mécanismes disponibles
- **majority** — Vote simple, majorité gagne
- **weighted** — Queen vote compte 3x, workers 1x
- **byzantine** — Supermajorité 2/3 requise (pour sécurité)

## Instructions

1. Présenter la question à tous les agents actifs
2. Chaque agent évalue et vote (pour/contre/abstention)
3. Collecter les votes avec justifications
4. Appliquer le mécanisme de consensus choisi
5. Annoncer le résultat avec breakdown des votes
6. Stocker la décision dans la mémoire collective

## Quand utiliser quel consensus
- Architecture/design → weighted (queen a plus d'experience)
- Sécurité/production → byzantine (décision critique)
- Style/conventions → majority (vote démocratique)
