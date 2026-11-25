---
name: produire-et-mesurer
description: Produire un document et vérifier qu'il tient — rendre, compter les pages, resserrer, et ne jamais trancher sur une estimation. À utiliser quand on demande de générer, produire, prévisualiser ou mesurer un document, ou quand on dit « produire le document », « est-ce que ça tient », « combien de pages », « ça déborde ».
---

# Produce, then measure

The rule this whole skill exists to enforce: **render it and count.** Not estimate, not reason about
whether it will fit — produce the artifact and measure the artifact.

## La séquence, dans cet ordre

Pour une **leçon entière** — tous les documents qui la couvrent, toutes leurs langues, et
seulement ce qui est périmé — voir `produire-une-lecon`, qui applique cette séquence page par page.

Elle est écrite ici pour n'être **reprise, jamais réinventée**. Une session qui la redéduit de la
prose choisit à chaque fois autrement où alléger la page — avant le premier rendu ou après — et le
nombre de tentatives change avec elle. Chaque étape nomme l'outil et **d'où vient sa règle** ; aucune
règle n'est recopiée ici, parce qu'une copie vieillit sans que rien ne le signale.

1. **Lire les entrées** — `walk_document_section`, la première section d'un document en entier,
   chaque suivante avec `include:[]` (les images attachées sont celles de la leçon, les mêmes pour
   chaque section : `pictures` se lit une fois, puis se laisse). Les règles sont la pile de mises en
   forme que la lecture renvoie, et rien d'autre. Notez au passage les valeurs du `render` que la
   mesure demandera.
2. **Composer l'arbre de blocs** — `compose_section` d'abord : ce que les gabarits de la mise en forme
   couvrent est rempli depuis le graphe, identique à chaque appel, et les guides que le gabarit
   lui confie sont compilés par le serveur (lisez `compiled` : lignes imprimées, lignes restées
   dans le guide, ce qui n'a pas été résolu), le tout **gardé côté serveur sous `treeRef`** ; vous
   composez seulement ce qu'il renvoie dans `unfilled`, dans la forme que
   `get_capabilities section:'document'` décrit, et vous l'insérez par `patch` sur ce `treeRef`
   — jamais en recopiant l'arbre, jamais en recomposant une section compilée.
3. **Vérifier la page contre le graphe, AVANT tout rendu** — `lint_content` avec `treeRef` (ou
   `document`) et `nodeId` (voir « Vérifier la page avant de rendre »). C'est le seul allègement
   légitime avant le premier rendu : ce que la vérification signale, pas ce que vous estimez. Un
   refus de vérifier est un arrêt, pas un feu vert. La réponse porte `checked.treeRef` : c'est lui
   qu'on rend.
4. **Rendre et compter** — `render_document` avec `treeRef` et `measure:true`, et LIRE sa
   `measurement` contre le budget de la mise en forme : c'est la mesure, il n'y en a pas d'autre
   pour un fichier rendu ici.
5. **Si ça déborde ou se chevauche** — corriger par `patch` sur le `treeRef` du dernier rendu (un
   `clear` inséré, une ligne remplacée), jamais en renvoyant l'arbre entier ; en cas de débordement,
   rendre une fois sans aucune image et compter, puis resserrer dans l'ordre fixe de « When a sheet
   overflows », et **après chaque changement, refaire les étapes 3 et 4**. Un resserrage peut
   casser ce que la vérification garantissait.
6. **Un regard, une fois** — `relecteur` sur le rendu final, contre la grille que
   `evaluate_document` remonte pour ce document ; `terminologue` si le document est traduit.
7. **Déposer** — `create_upload_url` puis `log_generation` pour un livrable, `create_preview_upload_url`
   seul pour un aperçu. Les deux voies ne se mélangent jamais. Plusieurs fichiers se signent en UN
   appel (`relPaths`, une confirmation pour tous) — pour les liens de téléchargement et les dépôts
   d'images aussi ; un appel par fichier, c'est dix-sept allers-retours par leçon.

Ce qui varie d'une matière à l'autre — la mise en forme, la grille, la routine — est lu aux étapes
1, 3 et 6. La séquence, elle, ne varie pas.

## Get the generation inputs

- **`walk_document_section`** for one slot of a document. This is the unit a sheet is produced from,
  and it is the one to prefer. It hands you the section's own text, the curriculum it covers, the
  routine that applies, and every formatter on its path.
- **Read the shared parts once.** The formatters, the document's assembly guide and the routine are
  identical for every section of a document, and together they are about fifteen times the section's
  own text. Read the **first** section of a document in full (follow `nextCursor` until the formatter
  stack is complete); read **every later** section with `include:[]`, adding `'curriculum'` only when
  it covers something you have not read yet. A ten-section lesson read the default way is roughly
  400k tokens of input; read this way it is roughly 40k, with nothing lost — and the formatter rules
  you read first are still in memory when you compose the tenth section.
- **`walk_graph`** when what the section covers is a grouping rather than a single lesson: the
  section names the curriculum it covers, not everything underneath it. Read that subtree with ONE
  walk from its id — `session-autorat` carries the depth discipline — never by descending into it
  call by call.
- **`walk_document`** for a whole document's `sections` spine — but a large document will not fit
  in one response: it sheds the formatters too, tells you so, and points you back at the per-section
  read. Believe it; do not retry, and do not count on it for the formatters.
- **`preview_generation`** when the material should reflect an unpublished draft. Preview the
  **smallest piece you changed** — after editing one section, preview that section, not its document.

Everything about how the sheet must look comes from the **formatters** in that payload, and
everything about what it must contain from the section's own assembly guidance and the routine.
Read them. Do not lay out a document from memory or from another subject's habits.

## Rendre avec `render_document`

Vous composez la page — quel bandeau, dans quel ordre, où elle tourne — et vous l'envoyez comme
**arbre de blocs**. Le serveur la met en page. La géométrie ne vous appartient pas : un bloc nomme
un `style`, une image nomme un `role`, et c'est le formatter qui dit à quoi cela ressemble. L'arbre
ne porte donc **aucune couleur, aucun corps, aucun centimètre** — si vous cherchez où mettre une
couleur, c'est que vous vous trompez de moitié.

Sa forme est dans `get_capabilities section:'document'`. Lisez-la avant de composer : une clé
inventée est REFUSÉE, et rien n'est rendu tant que l'arbre n'est pas valide.

Deux options qui comptent :

- **`translateInto`** — le serveur dérive la langue cible de celle que porte l'arbre, adossé au
  glossaire de l'espace de travail, et sort un fichier par langue. **Quelle langue produire est
  déclaré par la mise en forme du document** (`language.variants`) : lisez-la, ne la devinez pas et
  ne l'écrivez jamais en dur — un autre document en livre une autre. Un arbre qui porte déjà la
  langue cible est laissé tel quel : on ne retraduit jamais ce qu'un auteur a écrit à la main.
- **`measure:true`** — il met la page en page et **compte les pages**. Le compte se fait sur le
  RENDU, jamais sur la lecture du guide : une estimation a déjà donné 2,5 pages pour un document
  qui en faisait onze. Là où le déploiement n'a pas de moteur de mise en page, il répond
  `available:false` — il ne devine pas. La mesure situe aussi les **images** : `freeBelowCm` est le
  blanc sous la dernière marque de la page, image ou mot ; `reserveKept` dit si la réserve de pied
  (`budget.reserveBottomCm`) tient sur la dernière page ; et `overlaps` nomme une bande dessinée
  sur la bande précédente, ou sur des mots — le défaut qu'un compte de pages ne montre jamais.
  Un fichier avec un `overlaps` non vide n'est pas fini, quel que soit son compte de pages.

**Les images se nomment, elles ne se recopient pas.** Une entrée `media` est `{name, nodeId}` (une
image attachée au programme — `walk_document_section` les liste sous `pictures`), ou
`{name, relPath}` (un fichier déjà déposé dans le seau), ou `{name, data}` en base64 pour une image
légère. Préférez `nodeId` : le graphe sait alors quelle image la page porte, et `lint_content` la
compare à ce qui est attaché.

## Composer par le calcul, pas par le rendu

**Avant de composer, lisez `page_geometry`** sur la section (ou le document) : la page et sa boîte
utile, le pas de ligne et le nombre de lignes par page, les styles de bloc et leur budget de
caractères, les plafonds d'image, et — pour les images que vous annoncez placer
(`pictures: [{role, aspectRatio, float}]`) — la taille imprimée de chacune, la largeur qui reste
pour le texte à côté d'une image flottante, et **`linesBeside`** : le nombre de lignes de corps
qu'elle occupe en hauteur. Ce sont les mêmes nombres que le rendu utilise, calculés par la même
fonction ; ils ne peuvent pas contredire le fichier. Le premier rendu est alors un calcul, pas un
essai — là où trois rendus mesurés par fiche étaient la norme.

**Une bande flottante ancrée à un bloc plus court qu'elle** laisse la bande suivante s'ancrer à
côté et se dessiner par-dessus. Deux remèdes, au choix : faire courir le bloc d'ancrage sur au moins
`linesBeside` lignes, ou placer un bloc **`{kind:"clear"}`** après lui — la fin de l'habillage :
ce qui suit part sous l'image flottante la plus basse, quelle que soit sa hauteur. Le `clear` ne
prend aucun nombre ; n'essayez pas de le remplacer par un `spacer` tâtonné.

L'arbre complet à copier est `example` dans `get_capabilities section:'document'`.

## Vérifier la page avant de rendre

`lint_content` prend l'arbre de blocs (`document`) et le nœud qu'il couvre (`nodeId`), et applique
les règles de page sur la géométrie que le serveur résout lui-même pour ce nœud. Elles attrapent
ce qui **se rend sans erreur et faux** : une page comparée au texte du graphe qu'elle couvre, une
image comparée à ce qui est attaché, un bloc comparé aux plafonds de la mise en forme. Une seconde,
déterministe, et une seule fois par changement — là où un rendu coûte un aller-retour.

- Lisez `rulesPending` : c'est la liste des règles qui n'ont PAS tourné. Tant qu'elle n'est pas
  vide, la page n'est pas vérifiée, quoi que dise le reste.
- Un REFUS (pas de géométrie sur la pile, un arbre invalide, un nœud inconnu) est un arrêt. Sans
  limites à lire, chaque règle rend un résultat vide, identique octet pour octet à une page propre —
  c'est pourquoi le serveur refuse plutôt que de se taire. Ne contournez pas un refus en rendant.
- Ce qu'une règle nomme se corrige dans l'arbre, ou dans le graphe si c'est le graphe qui a tort ;
  une alerte délibérée se tait sur le nœud avec `metadata.lintIgnore` — jamais en retirant l'appel.
- Les constats `declared:<id>` viennent des règles que la mise en forme du document déclare
  elle-même (`properties.lintRules` sur le formatter — PT-07 sans exemple, une ligne [FR] qui ne
  s'imprime pas, une RÉPONSE qui déborde…). Un défaut de guide qui revient d'une fiche à l'autre
  est une règle à ajouter là, par `edit_nodes`, pas une décision à reprendre à la main.

## Mesurer, c'est lire la mesure du serveur

**UN FICHIER RENDU PAR LE SERVEUR EST DÉJÀ MESURÉ.** `render_document` avec `measure:true` rend
sur chaque fichier la mesure prise sur le rendu, images comprises : pages, `freeBelowCm` par page,
`reserveKept`, `overlaps`, `gaps`, `fonts` et `fontAsDeclared`. Le fil principal la LIT ; il ne
rend pas un PDF lui-même, ne regarde pas une page pour compter, et ne commissionne pas une seconde
mesure du même fichier — la dernière fois, deux mesures de la même page se contredisaient et il a
fallu une troisième pour trancher. Un `measurement.available:false` dit pourquoi (moteur absent,
budget dépassé) : on relance, on ne mesure pas ailleurs.

**`mesureur` ne sert que pour un fichier que le serveur n'a pas rendu** — déposé, corrigé par un
expert, produit hors du serveur. Les seuils ne s'écrivent pas dans l'agent : ils se lisent dans
le `render` du formatter — `budget.maxPages`, `budget.reserveBottomCm`, `budget.linesPerPage`,
`page.marginsCm`, `type` — et se passent dans l'appel.

L'appel type :

    Mesure ces fichiers : <chemins>.
    Budget lu dans la mise en forme (render.budget) : maxPages=…, type.family=…,
    reserveBottomCm=…, linesPerPage=…, maxCharsPerLine=…, maxCharsBesideImage=…
    Page attendue : <format, marges, police, interligne>.
    Rends le tableau et la liste des dépassements. Aucune image.

## La police déclarée doit être présente, sinon le compte est faux

Tout le budget est exprimé dans la police que la mise en forme déclare — `type.family`,
`type.sizePt`, `type.leadingPt`, et le nombre de lignes et de caractères qui en découlent.
Si cette police est absente du poste qui rend, LibreOffice lui en substitue une autre **en
silence** ; elle n'a pas la même largeur, et le compte de pages part à la hausse. Un document
qui tenait se mesure alors une page trop long — et on le resserre pour rien. C'est le même
piège que « mesurer le rendu, pas le guide » : le nombre a l'air d'une mesure, mais il décrit
un document que personne ne recevra.

Donc `type.family` fait partie des seuils qu'on lit dans le `render`. Le serveur le vérifie
lui-même sur le PDF produit (`fontAsDeclared`, `fonts`) ; pour un fichier qu'il n'a pas rendu,
`mesureur` le vérifie **sur le PDF produit** —
les polices réellement intégrées au fichier, pas ce que le système croit qu'il utiliserait,
car les deux divergent — et refuse de rendre un chiffre si la police déclarée n'y est pas.
Ne pas pouvoir vérifier est aussi un refus : si l'outil qui lit les polices du PDF manque sur
le poste, on le dit et on l'installe avant de mesurer, on ne devine pas. Un compte pris sans
la bonne police n'est pas un résultat.

## When a sheet overflows

**Render it again with no images at all, and count.** The cause is usually text, and stripping the
images tells you that in one measurement instead of an afternoon of guesses.

Read the file's `overlaps` first: a band over the band before it is fixed with a `clear`, not by
tightening anything.

Then tighten in this order — smallest change that could work, remeasured each time:

1. text (the usual culprit),
2. spacing and layout knobs the formatter allows,
3. images,
4. content — and only with the expert's agreement, because dropping content is a pedagogical
   decision and not yours.

After **every** change, run `lint_content` on the new tree and measure again — steps 3 and 4 of the
sequence. Tightening a line can drop the words a page rule requires word for word.

**Never arbitrate on an estimate.** If you cannot measure it, say that you cannot measure it and ask
for the render, rather than reporting a judgement as a result.

## Check the artifact, not the specification

The two most expensive rendering bugs in this project were both invisible to any check of the spec —
a page size that silently defaulted to the wrong standard, and a spacing setting that cropped
full-width images to a few millimetres. Both were found by looking at a rendered page.

Regarder la page reste donc nécessaire — mais c'est un **jugement, pas une mesure** : la lisibilité
d'un bandeau, une image flottante qui rogne un titre. Cela revient à **`relecteur`**, une seule fois,
sur le rendu final. Le fil principal n'ouvre pas les images d'une page pour compter : compter, c'est
`mesureur`, et lui ne remonte que des nombres.

**Les images des pages viennent du serveur.** `render_document` avec `measure:true` et
`pagePictures:true` rend, à côté de chaque fichier, un PNG de chaque page (`pagePictures[]`, même
durée de vie que le fichier). C'est cela qu'on regarde, et c'est cela qu'on donne au `relecteur`.
On n'installe pas la police ni LibreOffice sur le poste pour convertir et voir : la dernière fois,
quatre minutes d'une production de trente-six y sont passées, après que le serveur avait déjà
rendu tous les nombres.

Rends compte de ce que tu as mesuré, et de comment tu l'as mesuré.

## Preview output is segregated — keep it that way

A preview `.docx` goes through **`create_preview_upload_url`** only. Never `create_upload_url`, and
never `log_generation`: those write to the canonical bucket and the generation history, and a
preview recorded there becomes indistinguishable from a real deliverable.
