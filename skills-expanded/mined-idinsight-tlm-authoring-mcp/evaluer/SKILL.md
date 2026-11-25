---
name: evaluer
description: Évaluer un document ou un brouillon — le câblage, la couverture au regard du guide de la matière, les contradictions entre énoncés, la page composée contre le graphe, les grilles attachées, puis un regard sur le rendu — et remonter ses constats en une seule relecture. À utiliser quand on dit « relire », « vérifier », « est-ce que c'est prêt », « évaluer ce document », « qu'est-ce qui cloche », ou avant toute transmission.
---

# Évaluer

Cinq contrôles, chacun répondant à une question différente, et **une seule relecture** au bout.
Aujourd'hui ils portent sur les documents et le brouillon qui les touche ; évaluer un programme
contre une grille n'est pas encore outillé, et ce n'est pas demandé.

## La séquence

1. **`check_document`** puis **`check_draft`** — le document est-il produisible (couverture, sections, mise en
   forme et réglages, gabarits, grille, routine — chaque manque avec son verbe), puis le câblage. Un document qui ne couvre rien, une section hors de tout
   document, une routine que rien n'utilise, un élément relié à rien. Sans ce contrôle, ces fautes
   se taisent.
2. **`review_draft`** — la couverture. Il renvoie les attentes du guide de la matière et un
   instantané de la structure ; **c'est vous** qui raisonnez l'un contre l'autre. Il ne rend aucun
   verdict. `includeGuide:false` si vous avez déjà lu le guide dans cette session.
3. **`lint_content`** — la cohérence. Il signale les énoncés qui se contredisent : une routine dont
   le total annoncé ne fait pas la somme de ses étapes, une grille pondérée qui n'atteint pas
   100 %, un identifiant cité dans la prose qui ne mène à rien, une mise en forme dont les valeurs
   déclarées démentent sa propre prose. Il lit le sujet actif **et** les deux bibliothèques du
   catalogue. Avec `document` et `nodeId`, il vérifie aussi **une page composée contre le graphe**
   — c'est l'étape 3 de `produire-et-mesurer`. Une alerte délibérée se tait sur le nœud avec
   `metadata.lintIgnore` ; pas de déploiement. Lisez `rulesPending` : tant qu'il n'est pas vide,
   tout n'est pas vérifié.
4. **`evaluate_document`** — les grilles attachées au document. Il remonte les grilles et le
   document. **Triez la grille avant de la confier** : un point que la mesure du rendu, une règle
   de page ou une règle déclarée tranche déjà (pages, marge, police, chevauchements, couleurs,
   codes restés, lettres, durées) se répond depuis cette sortie ; seuls les points de jugement
   vont au sous-agent `relecteur`, dans un dossier écrit en fichier — les points qu'il juge, les
   images de page du rendu (`pagePictures`), le répertoire des phrases-types, la couverture de la
   page de l'élève. Un document peut porter plusieurs grilles, et toutes s'appliquent.
5. **Le rendu** — un regard, une fois, par `relecteur` sur les images de page du rendu final ;
   `mesureur` seulement pour un fichier que le serveur n'a pas rendu ; `terminologue` si le
   document est traduit, avec les termes lus en un appel (`get_terminology`, `queries`). Les
   sous-agents travaillent sur des fichiers, jamais sur le graphe.

## Une seule relecture, pas cinq résultats d'outil

L'expert ne se soucie pas de savoir quel contrôle a produit quel constat. Fondez le tout en un seul
compte rendu, en français, dans son vocabulaire : ce qui ne va pas, où, quoi faire. Une faute de
câblage et un trou de couverture se lisent côte à côte.

Donnez d'abord la forme — combien de constats, de quelle gravité — puis le détail.

## Les constats ne bloquent rien

Aucun de ces contrôles n'empêche une publication, et c'est voulu. Votre rôle est que la personne
qui décide les ait vus, pas de décider pour elle. Si elle transmet ou publie avec des constats
ouverts, c'est son choix : notez-le dans le journal du document, et poursuivez.

## Ne jamais soulever un constat qu'on n'a pas vu

Avant de dire qu'il manque quelque chose, retrouvez-le vous-même dans le rendu et citez la page.
Un constat qu'on ne peut pas montrer est une supposition, et c'est l'expert qui paie pour la
réfuter.
