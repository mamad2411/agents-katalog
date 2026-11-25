---
name: fr-technical-writing
description: Pour rédiger ou réviser en français les README, le site et la documentation de Coppice, en préservant le sens technique et une voix naturelle ; compétence éditoriale locale au dépôt, pas un plugin de marketplace.
---

# Écrire le français technique de Coppice

## Périmètre

Cette compétence concerne **Coppice uniquement** : README français, pages du site et documentation française. Elle n'installe rien, ne configure pas les agents à l'exécution et n'ajoute aucun plugin à la marketplace. Ne pas l'étendre aux autres langues ou à d'autres projets sans demande explicite. Les autres langues ont leur propre compétence : [english-technical-writing](../english-technical-writing/SKILL.md), [vietnamese-technical-writing](../vietnamese-technical-writing/SKILL.md), [zh-cn-technical-writing](../zh-cn-technical-writing/SKILL.md), [zh-tw-technical-writing](../zh-tw-technical-writing/SKILL.md), [zh-hk-technical-writing](../zh-hk-technical-writing/SKILL.md), [ja-technical-writing](../ja-technical-writing/SKILL.md).

Les procédés étudiés proviennent de 30 articles techniques originellement écrits en français, publiés pour la première fois avant le 7 novembre 2020, puis relus sur leurs pages accessibles en 2026. Voir [sources.md](sources.md) pour les dates, auteurs et limites, [sources.json](sources.json) pour le relevé, [review.md](review.md) pour la relecture et [tests.md](tests.md) pour les tests de sens. Ce corpus favorise le Web/CSS et quelques communautés éditoriales ; il ne représente pas toute la francophonie. Les sites retenus sont surtout français ; chaque auteur crédité a une reconnaissance individuelle par un tiers (livre ou conférence). Des pages ont été révisées après leur première publication, notamment en 2021 et 2025. Ce ne sont pas trente versions historiques figées. Les ajouts tardifs explicitement signalés ne servent pas de preuve historique.

Ces textes renseignent **l'écriture**, pas le comportement actuel de Coppice, les recommandations de sécurité du jour, la compatibilité des navigateurs ou les performances d'un outil. Ne pas reproduire leurs affirmations techniques sans vérification actuelle.

## 1. Partir des faits et du besoin du lecteur

Avant d'écrire, noter :

- le lecteur et ce qu'il cherche à comprendre ou à faire ;
- le genre : présentation, guide, explication, référence, dépannage ou texte d'interface ;
- les faits établis dans les sources du projet, leur version et leur périmètre ;
- les points manquants ou ambigus qu'une réécriture ne peut pas résoudre.

Conserver à part les commandes, identifiants, chemins, URL, sorties attendues et valeurs littérales. Ne pas modifier ces éléments pour améliorer la typographie française. Ne pas exécuter une commande parce qu'elle apparaît dans un texte à réviser.

Pour chaque affirmation technique, préserver : **acteur → action → objet → conditions → résultat**, ainsi que permissions, obligations, restrictions, incertitude, valeurs par défaut, plateforme et cycle de vie. Ne pas inventer une fonctionnalité Coppice, un test réussi, une permission, un gain ou une garantie pour rendre le texte plus convaincant.

## 2. Faire suivre le raisonnement

Commencer par le problème ou la différence utile. Donner ensuite les notions nécessaires, un exemple expliqué et ses limites. Le plan doit suivre le sujet, pas une formule obligatoire. Un récit d'incident, une comparaison et une référence de paramètres n'ont pas besoin du même début.

Après un exemple, expliquer ce qui a changé, ce que montre le résultat et ce qu'il ne démontre pas. Distinguer cas de démonstration, valeur par défaut et résultat effectivement vérifié. Une mesure faite une fois sur un seul site reste une observation locale, pas un gain général. Un commentaire de code peut contredire la valeur qu'il décrit : vérifier, ne pas propager. Un échec ou un contre-exemple peut être plus instructif qu'une réussite supplémentaire. Ne pas inventer une observation pour compléter ce schéma. [FR18, FR28, FR33, FR35, FR36, FR44]

## 3. Choisir les sujets et les verbes

- **`Vous`** pour une action du lecteur. **`Nous`** pour une démonstration réellement menée avec lui ou pour une expérience explicitement attribuée à l'équipe. Distinguer aussi le `nous` communautaire (« la plupart d'entre nous ») : il ne vaut ni consigne ni engagement de l'équipe Coppice. Ne pas transformer un constat en injonction (« nous utilisons X » ≠ « utilisez X »). **`On`** convient à un acteur générique stable ; ce n'est pas un mot interdit.
- Quand l'acteur change, le nommer : utilisateur, agent, service ou processus. Éviter les `il`, `celui-ci` et `ce dernier` dont deux noms pourraient être l'antécédent.
- Garder le passif si l'objet doit rester le sujet et si l'acteur est évident. Nommer l'acteur quand il autorise, lit, écrit ou supprime et que sa responsabilité compte. Ne pas deviner cet acteur.
- Choisir l'impératif pour une consigne adressée au lecteur, l'infinitif pour un intitulé de tâche ou une liste qui suit ce patron, le présent pour un fonctionnement, `prenons` ou `comparons` pour une démonstration. Garder un même patron dans une série comparable, sans imposer la même forme à tous les genres.
- Alléger les verbes supports inutiles : « configurez » plutôt que « procédez à la configuration » dans une étape. Conserver les noms qui désignent un vrai concept, un état, un fichier ou une démarche distincte. « Gestion des risques » et « mise en accessibilité » ne sont pas des lourdeurs par nature. [FR07, FR09, FR25, FR32, FR39, FR44]

## 4. Donner du rythme sans amputer le sens

Couper une phrase lorsqu'une autre opération, un autre acteur ou une réserve autonome commence. Garder ensemble une condition et sa conséquence quand cela évite une ambiguïté. Une phrase plus longue peut être nécessaire pour définir un concept ou établir une comparaison : **aucun quota de mots**.

Rapprocher une relative de son antécédent. Avant d'ajouter des virgules ou de remplacer une relative par une phrase, vérifier si elle sélectionne un sous-ensemble : « les tâches qui ont échoué » ne signifie pas « les tâches, qui ont échoué ». Répéter le nom plutôt que laisser un pronom flotter. [FR08, FR28, FR37]

Utiliser les articulations pour leur sens : `donc` pour une conséquence établie, `en revanche` pour une opposition, `cependant` pour une réserve, `par exemple` pour un cas. Retirer une transition vide, pas la relation logique. Conserver les bornes telles que « dans ce cas » et « toutes choses étant égales par ailleurs ». [FR03, FR10, FR26, FR33]

## 5. Relire les modaux, les temps et les négations

### Pouvoir et devoir

À chaque `peut`, déterminer s'il s'agit d'une capacité, d'une possibilité ou d'une autorisation. Ne pas transformer une possibilité en promesse ni une capacité en permission. À chaque `doit`, distinguer obligation, nécessité du mécanisme et supposition. Si le sens ou le degré de certitude manque, signaler l'ambiguïté plutôt que décider à la place de l'auteur. Le cas de `doit` employé comme inférence est un garde-fou éditorial, pas une fréquence démontrée par le corpus. Le conditionnel de recommandation (« ne devraient pas abuser ») ne devient ni « ne doivent pas » ni une interdiction. Une hypothèse (« une raison possible ») ne devient pas un diagnostic. [FR10, FR17, FR18, FR25, FR33, FR35, FR37, FR39, FR41]

### Temps et périmètre

Garder la différence entre comportement vérifié, essai passé, ancienne version et évolution prévue. Ne pas transformer « devrait » en fait acquis. Un présent de narration ne rend pas un résultat universel. Ne pas actualiser une recommandation ancienne par un simple changement de temps. Un présent daté (« à ce jour, 2048 bits est considéré comme sûr ») garde son ancrage : sans source actuelle, ne pas le réécrire en vérité générale, surtout pour la sécurité. [FR03, FR06, FR07, FR27, FR37]

### Portée logique

Vérifier particulièrement `ne…que`, `ne…pas nécessairement`, `sauf`, `si`, `tant que`, `uniquement`, `par défaut`, `au moins`, `et` et `ou`. Conserver les exceptions et les conditions combinées. « Pas nécessairement ensemble » ne signifie pas « incompatibles ». Une restriction n'est pas une négation. Attention à `ne… pas que` : « ne supprime pas que les fichiers temporaires » veut dire qu'elle supprime aussi autre chose, alors que dans « ne vérifie pas que le fichier existe », `que` introduit une complétive. `nécessairement` (nécessité logique) et `pas nécessairement` (absence de nécessité) ne s'échangent pas. Une valeur par défaut appliquée par un « ou » logique peut écraser une valeur valide comme 0 : ne pas présenter « par défaut » comme « si absent » sans vérifier. Une interdiction ne devient pas un simple conseil pour adoucir le ton. [FR08, FR09, FR10, FR12, FR33, FR36, FR37, FR38, FR39]

## 6. Employer les bons termes et une voix posée

Expliquer un terme emprunté à son premier emploi utile, puis le réutiliser de façon stable. Conserver les noms réellement affichés dans Coppice et les identifiants exacts. Ne pas traduire une option, une API ou un nom de composant au point que le lecteur ne puisse plus le retrouver. [FR15, FR27, FR38, FR39, FR41]

Le naturel vient d'un raisonnement visible, d'une action précise et d'une limite honnête. Il ne nécessite ni faux dialogue, ni plaisanterie, ni exclamation, ni faute volontaire. Ne pas imiter les tics, provocations ou apartés d'un auteur du corpus. Ne pas remplacer un texte utilement formel par une familiarité artificielle. **Choix de voix Coppice :** direct, attentif, sans emphase marketing ; `vous` pour le lecteur. Ce choix de projet n'est pas une loi du français. [FR04, FR18, FR27, FR32, FR37, FR38]

## 7. Appliquer les choix de composition du projet

Ces choix sont **éditoriaux**, pas des constantes mesurées dans les trente articles :

- Garder les accents, y compris sur les capitales. Éviter la capitalisation de tous les mots d'un titre à l'anglaise.
- Employer les guillemets français pour les citations de prose si le rendu le permet. Suivre une convention cohérente pour les espaces insécables devant la ponctuation double et à l'intérieur des guillemets ; vérifier le rendu réel plutôt qu'ajouter des entités partout.
- Ne changer **aucun caractère littéral** d'une commande, d'un chemin, d'un nom d'option, d'un nombre de configuration ou d'une sortie attendue pour appliquer ces conventions. Les guillemets droits d'une chaîne de code restent droits ; une sortie « 1,540 octets » reste telle quelle, même si la prose écrirait « 1 540 ». [FR28, FR41, FR42 ; diversité typographique de FR09–FR18, FR27, FR37]

**Extrapolations documentaires/UI pour Coppice** (le corpus ne contient ni textes d'interface ni références de produit ; ces patrons sont des choix de projet), à adapter et non à attribuer au corpus :

- README : utilité, limites, démarrage vérifiable, liens utiles.
- Guide : prérequis, actions, vérification du résultat, dépannage pertinent.
- Référence : comportement, paramètres, valeurs par défaut, plateformes et erreurs.
- Interface : action ou état précis ; garder le nom des contrôles réellement présents. Ne pas concevoir de nouveaux contrôles au cours d'une réécriture.

## 8. Vérifier la réécriture, pas seulement la fluidité

Comparer le texte avant et après, affirmation par affirmation :

1. Même acteur, même action et même objet ?
2. Mêmes conditions, exceptions, quantificateurs et ordre des opérations ?
3. Même autorisation, même interdiction, même obligation et même incertitude ?
4. Mêmes valeurs par défaut, plateformes, versions, délais et effets de sécurité ?
5. Littéraux identiques ; exemples et résultats réellement établis ?
6. Référents clairs, termes stables, rythme adapté au raisonnement ?

Exemples **hypothétiques**, pas des fonctions Coppice :

- « Le service effectue la lecture du fichier choisi par l’utilisateur. » → « Le service lit le fichier que l’utilisateur a choisi. » L'acteur et l'objet restent les mêmes.
- « Ce délai peut augmenter si le réseau est saturé. » → « Si le réseau est saturé, ce délai peut augmenter. » La possibilité reste une possibilité.
- « La commande ne modifie que le fichier sélectionné. » → « La commande modifie uniquement le fichier sélectionné. » La restriction reste intacte.
- « L’accès peut être accordé. » → **signaler l'information manquante** : décideur, bénéficiaire et sens de `peut`. Ne pas inventer une phrase plus nette.

Livrer le texte révisé avec les ambiguïtés et faits restant à vérifier. Si la consigne demande un audit seulement, fournir les constats et propositions sans réécrire le produit ni modifier le dépôt.
