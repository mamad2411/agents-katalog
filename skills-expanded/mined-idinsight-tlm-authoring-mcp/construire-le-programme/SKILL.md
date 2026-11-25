---
name: construire-le-programme
description: Construire ou faire évoluer un programme avec le serveur — les standards et leur hiérarchie, les composantes d'apprentissage, le cours, ses leçons et leur alignement, les regroupements — à la main, depuis une recherche, ou depuis un document (une planification existante, une leçon, le programme d'un autre pays). À utiliser quand on dit « ajouter un objectif », « créer un cours », « regrouper les leçons », « aligner cette leçon », « partir de ce PDF », « importer ce programme », « nouveau cours », « partir de zéro ».
---

# Construire le programme

Le graphe a deux couches. La **colonne vertébrale des standards** dit ce que l'autorité demande :
des objectifs en hiérarchie, et sous chacun les composantes d'apprentissage qui le soutiennent. La
**couche de contenu** dit comment on l'enseigne : un cours, ses regroupements, ses leçons, et dans
chaque leçon ses activités et ses matériels. Une leçon **s'aligne** sur le standard qu'elle
enseigne ; c'est ce lien qui relie les deux couches.

Ce que chaque sorte d'élément accepte n'est pas écrit ici : `get_capabilities section:'editable'`
le liste sous `batch.kindProperties`, et les conventions de la matière — le nom d'un regroupement,
la catégorie d'un objectif, ce qu'une leçon doit porter — sont dans `get_graph_guide`. Une
convention recopiée ici serait fausse la prochaine fois que le guide change.

## Avant d'écrire

1. **`get_graph_guide`** — les conventions. Si la matière est vraiment nouvelle et n'a pas de
   guide, dites-le : commencer un programme sans guide, c'est laisser le prochain auteur inventer
   les siennes.
2. **`namespace_stats`** puis **`find_node`** et **`walk_graph`** en `detail:'skeleton'** — ce qui
   existe déjà. « À partir de rien » est presque toujours « à partir de moins que prévu », et une
   seconde colonne de standards est pire qu'aucune.

## Les briques, dans l'ordre qui garde le graphe lisible

Chaque brique s'accroche à la précédente ; une brique posée hors d'ordre est un élément qu'aucune
lecture ne trouve.

1. **Les standards** — `add_nodes` avec `kind:'StandardsFrameworkItem'`, chacun sous son parent
   (le serveur pose le lien de hiérarchie). Ils viennent de l'autorité, pas de vous ; s'ils sont
   déjà importés, on les lit, on ne les recrée pas. Un standard n'a pas de numéro d'ordre : sa
   place est celle de la traversée.
2. **Les composantes d'apprentissage** — `kind:'LearningComponent'`, chacune sous le standard
   qu'elle soutient ; le serveur pose le lien de soutien, qui n'est pas un lien de hiérarchie.
3. **Le cours** — `kind:'Course'`, sans parent. Tout le contenu s'y accroche.
4. **Les regroupements** — `kind:'LessonGrouping'` sous le cours ; leur nom de type vient du guide.
5. **Les leçons** — `kind:'Lesson'` sous leur regroupement, avec `alignTo` le standard qu'elles
   enseignent (résolu par son nom). Une leçon sans alignement est un contenu que rien ne rattache
   au programme.
6. **Les activités et matériels** — sous la leçon. Ce sont eux qui portent les mots d'une page ;
   une section de document ne fait que les placer (voir `composer-un-document`).
7. **La routine** — `list_catalog` avec `kind:'routine'`, `get_catalog_entry` pour lire, puis
   `use_routine`. Préférez toujours une routine existante à adapter : personne n'écrit une
   structure de séquence à partir d'une page blanche. La copie est indépendante de la bibliothèque.

## Faire évoluer ce qui existe

- **Modifier** — `edit_nodes` : le titre, le corps, le contenu, la position, ou toute autre
  propriété par son sac `properties`. Une modification n'est jamais une suppression suivie d'une
  recréation : cela change l'identifiant et casse en silence tout ce qui y renvoyait.
- **Déplacer** — `move_node`, sur un seul axe de rattachement à la fois ; le second, s'il existe,
  reste en place.
- **Relier après coup** — `create_edges` pour un alignement ou un soutien ajouté à un élément déjà
  créé.
- **Supprimer** — en dernier recours ; c'est un brouillon, `undo_last` reprend la dernière écriture.

## Trois façons d'obtenir la proposition

La procédure d'écriture est la même pour les trois et vit dans `session-autorat`, « Proposer, puis
écrire ». Ici, seulement ce qui change selon la source.

- **À la main** — l'expert dicte ; reformulez en liste d'éléments (sorte, nom, parent, alignement)
  et montrez-la avant de résoudre quoi que ce soit.
- **Depuis une recherche** — dans le graphe, `find_node` puis `walk_graph` depuis l'id trouvé :
  ce qui existe borne ce qui reste à créer. Une recherche hors du graphe, quand le client en dispose,
  donne une proposition comme une autre, avec sa source citée.
- **Depuis un document** — une planification, une leçon rédigée, le programme d'un autre pays :
  le sous-agent `lecteur` lit le fichier et renvoie une proposition de **programme** (sa forme est
  dans son contrat) — chaque élément avec sa sorte, son nom, son parent et son alignement **par
  leur nom**. Le fil principal résout les noms et écrit ; le sous-agent ne touche jamais au graphe.

**Le point de couture.** Importer d'un coup le programme entier d'un autre pays n'est pas un outil
du serveur : la correspondance entre sa forme et la forme canonique du graphe se décide avec un
développeur, et un script de conversion existe côté serveur pour ce cas. Par le plugin, on construit
par lots, un niveau à la fois — c'est plus lent et c'est voulu.

## Vérifier au fur et à mesure

`check_draft` après chaque niveau posé — un élément relié à rien, une leçon sans regroupement — et
`find_node` sur ce que vous venez de créer, pour voir son chemin. Attraper une faute de câblage à
six éléments coûte moins qu'à soixante.

## Des lots cohérents

`add_nodes` et `create_edges` prennent plusieurs éléments en un appel atomique : servez-vous-en.
Mais un élément créé dans un lot ne peut pas être le parent d'un autre élément du même lot —
construisez **un niveau à la fois** : les regroupements, confirmez, puis leurs enfants. Chaque appel
confirmé doit laisser le graphe dans un état que quelqu'un d'autre pourrait reprendre.
