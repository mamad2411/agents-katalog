---
name: composer-un-document
description: Créer ou faire évoluer un document — livre de l'élève, cahier d'exercices, guide de l'enseignant — ce qu'il couvre dans le programme, sa mise en forme, ses grilles d'évaluation, ses sections, ses images, et le journal de ses décisions ; à la main, depuis une recherche, ou depuis un document existant. À utiliser quand on dit « créer un guide », « un cahier d'exercices », « ajouter une section », « changer la mise en forme », « attacher une grille », « noter pourquoi », « ce document couvre ».
---

# Composer un document

Un document, c'est trois choses reliées : **ce qu'il couvre** dans le programme, **comment il se
présente** (sa mise en forme), et **comment il se juge** (ses grilles). Ses sections sont ses pages,
et chaque section dit ce qu'elle couvre et comment elle assemble sa page.

La règle qui tient tout : **le programme porte les mots, une section porte la page.** Le texte
d'une question vit sur l'activité, dans le programme ; la section dit seulement comment cette
activité se place. Une nouvelle question, c'est donc une activité dans le programme
(`construire-le-programme`) ET une section ici, jamais un texte recopié dans un guide de page.

## L'ordre

1. **Le document** — `create_document`, avec son nom et ce qu'il couvre **par le nom**. L'outil
   crée le document et son lien de couverture ensemble. Jamais `add_nodes` puis `create_edges` :
   un document sans lien de couverture est une écriture valide et un document qui génère du vide.
2. **La mise en forme** — `use_formatter` depuis le catalogue, `duplicate_entry` pour en adapter
   une, `add_to_catalog` pour en offrir une nouvelle à d'autres. Une mise en forme a deux moitiés :
   la prose que le modèle lit, et le sac `render` — la géométrie déclarée que le serveur applique.
   **Sans sac `render`, rien ne se produit ni ne se vérifie** : `produire-et-mesurer` refuse. Lisez
   la mise en forme choisie avant de l'attacher, et dites-le si elle n'en a pas.
3. **Les grilles** — `use_rubric` ; ce sont elles qu'`evaluate_document` remontera. Un document
   peut en porter plusieurs et toutes s'appliquent.
4. **Les sections** — `add_section` par emplacement, chacune nommant ce qu'elle couvre. Elles
   s'emboîtent : une partie tient des chapitres qui tiennent des pages. Une page de garde ou une
   table des matières est une section **sans couverture**, exprès. La consigne d'assemblage d'une
   page se pose sur la section, par `edit_nodes` et son sac `properties`.
5. **Les images** — voir `illustrations` : une image s'attache à la leçon ou à l'activité qu'elle
   illustre, et la section la place.
6. **`check_document`** — dès que le document existe, et à nouveau avant de produire : un seul
   compte rendu dit s'il couvre quelque chose, s'il a des sections, une mise en forme avec ses
   réglages, des gabarits de page, une grille, une routine — et pour chaque manque, le verbe qui le
   comble. Il ne bloque rien. Puis `check_draft` pour le câblage du brouillon.

## Faire évoluer un document

- Une section : `edit_nodes` (titre, position, consigne d'assemblage), `move_node`, `add_section`.
- La mise en forme attachée est une **copie** : la modifier par `edit_nodes` ne change que ce
  document. La corriger pour tout le monde, c'est l'écrire dans le catalogue avec `catalog:` — et
  une écriture au catalogue **s'applique et se publie d'un coup**, sans brouillon ni retour arrière.
- Ce qu'une page doit dire se corrige dans le programme, pas dans la section.

## Le journal

Le document et chacune de ses sections gardent un **journal** : la trace datée de leurs décisions —
pourquoi une règle est ainsi, ce qui a été mesuré, ce qui attend l'avis d'un expert. Il ne fait
jamais partie d'une lecture de génération ; on le lit sur l'élément, avec `walk_graph`, quand
quelqu'un demande **pourquoi**.

Toute écriture qui touche un document ou une section pour une raison qui n'est pas évidente en
laisse une entrée : la date, la décision, qui l'a prise, ce qui reste ouvert.

On l'écrit avec **`append_journal`** : le document ou la section par son nom, le texte, un titre
court. Le serveur date et signe l'entrée, l'ajoute après ce que le journal contient **à l'instant
de l'écriture**, et refuse une confirmation dont la base a bougé. Jamais par `edit_nodes` sur le
champ : cela réécrit le journal entier depuis votre copie, et deux sessions sur le même document
s'écrasent l'une l'autre sans erreur.

## Trois façons d'obtenir la proposition

La procédure d'écriture est celle de `session-autorat`, « Proposer, puis écrire ». Ici, ce qui
change selon la source.

- **À la main** — l'expert décrit le document ; reformulez en structure (parties, sections, ce que
  chacune couvre par son nom) et montrez-la avant d'écrire.
- **Depuis une recherche** — un document existant sert de modèle : `find_node` sur son nom,
  `walk_graph` en `detail:'skeleton'` pour lire sa structure, puis la même structure par
  `create_document` et `add_section` sur la nouvelle couverture. On ne duplique jamais les nœuds
  d'un document ; on refait la structure.
- **Depuis un document** — une maquette, un ancien guide, un cahier d'un autre pays : le sous-agent
  `lecteur` renvoie une proposition de **document** (sa forme est dans son contrat) — les parties,
  les sections, ce que chacune couvre **par le nom**, et la consigne de page que le fichier suggère.
  Depuis des leçons existantes, il n'y a rien à lire : les sections les couvrent par leur nom.

## Vérifier

`check_draft` pour le câblage, puis la compétence `evaluer` avant de transmettre. Un document se
produit avec `produire-et-mesurer`, jamais depuis ici.
