---
name: fabrique-outils
description: "Méthode et socle qualité pour fabriquer dans une collectivité un outil durable avec Claude Cowork : HTML partagé, application web conteneurisée, MSI ou Grist. DÉCLENCHER quand l'outil servira à d'autres que son auteur ou dans la durée, traite des données de personnes, s'installe sur un serveur ou un poste, remplace un outil existant, ou est montré régulièrement aux élus ou à l'extérieur ; aussi pour faire évoluer ou reprendre un tel outil, ou sur transcription d'un besoin. NE PAS DÉCLENCHER pour un fichier HTML jetable, pour soi ou une réunion (calculette, graphique de diaporama, mini-tableau de bord ponctuel, sans donnée de personne). Dans le doute, déclencher et poser la question du curseur. Impose : questions en mots simples, SPEC validée avant de coder, jalons selon la grille de vigilance IA, sécurité et RGPD dès la conception, tutoriel, paquet contrôlé pour la DSI, partage et transmission. Ne couvre pas : assistants documentaires, macros, documents, scripts d'exploitation (fiche dédiée)."
metadata:
  version: "0.1.2"
---

# Fabrique d'outils et d'applications

Cette skill encadre la fabrication des petits outils d'une collectivité : remplacement d'un existant, contournement d'une « douleur » dans un logiciel éditeur, réponse à un besoin nouveau. Elle laisse aux référents et aux agents la liberté de fabriquer leurs outils, et pose des garde-fous pour que chaque outil dure et s'intègre au système d'information. Elle ne remplace pas la méthode de la cellule opérationnelle, agile et ancrée dans les métiers : elle la sécurise et rend chaque outil reprenable.

Ce qui dépend de l'organisation (rôles, serveurs, postes, outils d'exploitation) est dans `references/environnement-collectivite.md`, **à lire avant l'étape 0**. « La cellule » désigne l'équipe qui valide (la cellule opérationnelle, ou son équivalent). Le besoin a été questionné à l'oral avec son émetteur, l'entretien enregistré et transcrit, et la transcription Markdown, anonymisée, est déposée dans le dossier de travail. La sécurité est évaluée avec la grille de vigilance des outils IA, tenue par la cybersécurité.

## Tant que la skill n'est pas adaptée : mode essai

Si `references/environnement-collectivite.md` contient encore des « [À ADAPTER] », ou `references/grille-vigilance.md` des « [À REMPLIR] », la skill s'essaie mais n'est pas encore celle de la collectivité. Dans ce cas :

- Le dire une fois, au début, en une phrase simple : « Cette skill n'a pas encore été adaptée à votre collectivité : je continue avec des valeurs d'exemple, pour un essai. » Ne pas le répéter ensuite.
- Pour l'environnement, prendre les exemples entre parenthèses comme hypothèses et les noter dans la SPEC (« À faire préciser »).
- **N'annoncer aucun niveau vert, orange ou rouge, n'écrire aucun score.** À la place, dans la SPEC et dans `docs/grille-vigilance.md`, lister les sujets de la grille que l'outil touche (liste indicative du modèle), avec la mention « à soumettre à la cybersécurité ».
- La méthode, le socle de sûreté et les douze règles s'appliquent sans changement. La mise en service pour d'autres attend que la grille soit remplie : sans niveau, personne ne peut la valider.

Pour sortir du mode essai : le guide `docs/adapter-a-votre-collectivite.md` du dépôt, une demi-journée avec la DSI.

## Règle d'or : libérer la création, cadrer sans freiner

Avec Claude, fabriquer un outil prend des heures, plus des mois : c'est une chance à saisir, pas un risque à contenir. Cette skill doit **toujours** permettre aux agents de créer. Chaque règle passe donc un test : *ralentit-elle l'agent qui crée ?* Si oui, soit Claude l'applique lui-même sans rien lui demander, soit elle n'est exigée qu'au moment où la cellule installe l'outil pour d'autres, jamais pendant la création. Seul le socle de sûreté (secrets, données de personnes, appels externes, code dangereux) s'applique dès le premier jour, parce qu'il protège l'agent lui-même. Il n'est jamais allégé : ni pour un brouillon, ni pour un outil partagé, ni pour aller plus vite.

## Parler à l'agent (à lire en premier)

L'agent qui fabrique l'outil connaît son métier, pas forcément l'informatique. Lire `references/dialogue-agent.md` avant la première question :

- **Le métier se demande, le technique se décide.** Format, sécurité, hébergement : Claude choisit et explique en une phrase.
- Une question à la fois (trois au maximum), chacune avec sa raison et une proposition par défaut ; « je ne sais pas » est accepté et noté comme hypothèse.
- Aucun sigle sans explication ; un garde-fou n'est jamais un refus sec (on dit comment y arriver) ; les protections sont appliquées sans qu'on les demande puis résumées dans « Ce que j'ai sécurisé pour vous ».
- **Liberté d'abord.** L'agent peut toujours fabriquer et utiliser son outil. Les garde-fous portent sur la sûreté (secrets, données de personnes, appels externes, code dangereux) et sur la préparation de la transmission, jamais sur l'envie de fabriquer. Le contrôle ne le freine pas : il dit à la cellule ce qu'il manque pour installer l'outil un jour.

## Le curseur : à quelle hauteur déclencher la méthode

Le critère n'est pas le format, mais **qui utilise l'outil, combien de temps, avec quelles données**. Une question suffit : « Cet outil servira-t-il à d'autres personnes que vous, ou plusieurs fois dans la durée ? » Détail, cas d'école et règles minimales à ajouter aux instructions générales : `references/curseur-declenchement.md`.

| Niveau | Quand | Méthode |
|---|---|---|
| **0. Jetable** | Fichier pour soi ou une réunion, sans donnée de personne | La skill ne se déclenche pas (règles minimales des instructions générales) |
| **1. Partagé** | HTML utilisé par quelques collègues ou montré régulièrement, sans donnée de personne | Voie courte (`creer_projet.py --niveau partage`) : cinq lignes de SPEC, en-tête de version, chiffres rapprochés, tutoriel court, fiche de partage. Seul le socle de sûreté est exigé ; le reste est recommandé |
| **2. Durable** | Serveur, poste ou Grist partagé ; données de personnes ; connexion à un logiciel ; remplace un outil ; outil essentiel (classe 1) ; installation demandée pour d'autres | Méthode complète ci-dessous |
| **3. Avis d'abord** | Public, externes, grille rouge | Arrêt dès la SPEC : DSI, cybersécurité, DPO |

La durée seule ne fait pas monter au niveau durable : un fichier local sans donnée de personne, utilisé de temps en temps, reste en voie courte même pendant des années (exemple : le bilan réglementaire).

Le curseur monte, il ne descend pas sans l'accord de la cellule : dès qu'un critère supérieur apparaît en cours de route, le dire simplement et proposer de monter d'un cran.

## Partager et transmettre (lutte contre l'égoïsme d'usage)

Un outil fabriqué dans une licence ne doit pas y rester si d'autres peuvent en profiter. Claude repère le potentiel de réutilisation (besoin non propre à une direction, collègues qui font pareil, outil déjà paramétrable, brique réutilisable), puis envoie **une fois** un message amical et amusant et propose : prévenir la cellule opérationnelle (message rédigé par Claude), préparer la fiche pour l'intranet, ou pas maintenant. À la livraison, il propose aussi une transmission : exercice de reprise par le suppléant, courte présentation, « ce que j'ai appris ». Formules, signaux et fiche : `references/partage-et-transmission.md` ; suivi dans `docs/partage.md`.

## Avant de commencer : est-ce le bon outil ?

La skill vise un outil avec une interface et des utilisateurs. Pour le reste, le dire en une phrase et orienter.

| Demande | Que faire |
|---|---|
| Script d'exploitation ou d'administration (PowerShell, bash, Ansible) | `references/scripts-exploitation.md` (simulation, sauvegarde, retour arrière, garde-fou sur la cible) ; règles 1, 7, 8 ; grille si données personnelles ou annuaire |
| Assistant documentaire, chatbot, prompt système | La skill de rédaction de prompts de votre collectivité, si elle existe ; passer la grille (données personnelles et sensibles, envoi à une IA externe, décisions concernant des personnes) |
| Macro Office (VBA, Office Scripts) | Passer la grille ; la cellule tranche entre refonte en format A ou C et maintien |
| Paramétrage d'un progiciel éditeur (gestion du courrier, gestion du patrimoine, outil de tickets…) | Seulement aider à rédiger la SPEC du besoin |
| Document, note, courrier, présentation | Les skills de modèles de votre collectivité, si elles existent |
| Carte | La skill de cartographie de votre collectivité, si elle existe, la fabrique ajoutant SPEC, tutoriel, versions, documentation |
| Service ouvert au public | **S'arrêter dès la SPEC** : `references/ouverture-externe.md`, cas 3 ; pas de construction avant l'avis de la DSI, de la cybersécurité, du DPO et de la direction concernée |

## Cinq principes

1. **Le besoin métier commande.** Résoudre la douleur décrite, pas une version idéale. Ce qui n'est pas demandé va dans « Hors périmètre ».
2. **Le format le plus simple qui tient la charge.** Un fichier HTML autonome bat une appli web, qui bat un MSI.
3. **Reprenable sans Claude.** Un agent de la collectivité doit pouvoir comprendre, reconstruire, mettre à jour et redéployer l'outil avec la seule documentation livrée.
4. **Sûr dès la conception.** Éviter un point bloquant au moment de la SPEC coûte bien moins cher que le corriger dans du code livré.
5. **Une seule vérité, trois usages.** Les règles de gestion de la SPEC (RG-01…) servent à la validation, au code et aux tests ; la documentation en découle ; `build/fabriquer.py` le vérifie.

## La méthode : 4 étapes, 3 validations

### Proportionner avec la grille de vigilance

Évaluer le projet avec la grille au jalon 1 sur la base de la SPEC (niveau provisoire), puis au jalon 3 sur le code réel (niveau définitif).

| Niveau | Démarche |
|---|---|
| Vert (seuil de votre grille, aucun bloquant) | SPEC courte ; jalons 1 et 2 fusionnables ; mise en service validée par la cellule |
| Orange (seuil de votre grille, aucun bloquant) | Les 3 jalons ; plan d'actions daté dans la SPEC ; avis de la cybersécurité, et du DPO si données personnelles, avant la mise en service |
| Rouge (seuil de votre grille, ou un bloquant) | Ne pas coder tel quel : proposer une conception qui lève les points bloquants (presque toujours possible à ce stade), puis réévaluer |

La grille intégrée (`references/grille-vigilance.md`) est un modèle à remplir avec votre cybersécurité ; une fois remplie, en cas d'écart avec sa skill, la sienne prime (`scripts/verifier_grille.py`). Score vert mais données sensibles : le signaler à la cellule. Si l'agent veut aller plus vite (« vas-y »), respecter son choix sauf face à un point bloquant, et noter ce qui n'a pas été validé dans `docs/derogations.md`.

### Étape 0 — Lire le besoin

Lire `references/environnement-collectivite.md` et `references/dialogue-agent.md`, placer le curseur, puis vérifier la demande avec « Avant de commencer ».

1. **Contrôle résiduel de confidentialité.** La transcription doit arriver anonymisée ; le vérifier quand même, résumé automatique de l’outil de transcription compris. Noms d'agents dans un cadre professionnel : le signaler en une ligne, ne jamais les recopier, demander de repasser le fichier dans l'outil d'anonymisation. Données réelles d'usagers (nom associé à une situation, numéro de dossier, adresse, santé) : s'arrêter et demander une version anonymisée. La SPEC désigne les personnes par leur fonction.
2. **Séparer le besoin principal des autres douleurs** : le premier va dans la SPEC, les autres dans « Hors périmètre ».
3. **Extraire :** la douleur en une phrase ; utilisateurs et nombre ; fréquence ; données qui entrent et sortent ; ce que l'outil remplace ; irritants ; critères de réussite ; situation actuelle chiffrée.
4. **Se méfier des noms propres** déformés par la reconnaissance vocale : proposer la correction probable, marquée « à confirmer ».
5. **Repérer l'ouverture à l'extérieur** (communes, partenaires, usagers, diffusion publique) : lire `references/ouverture-externe.md` avant la SPEC.
6. **Repérer les manques** qui changeraient la conception (5 au maximum) : les poser en mots simples, sinon noter une hypothèse.
7. **Réutiliser avant de refaire :** consulter le registre des outils (`references/registre-des-outils.md`) et demander à la cellule si un outil proche existe.
8. **Repérer le potentiel de partage** (voir plus haut) : une phrase au bon moment, sans insister.
9. **Repérer une rustine**, par une question simple : « Cet outil contourne-t-il un logiciel, une trame ou une façon de faire qu'on ne maîtrise pas ? » Si oui, la fiche rustine (`creer_projet.py --rustine`) note le problème de fond, à qui il appartient et quand l'outil pourra disparaître (`references/role-editeur.md`). Cela n'empêche jamais de fabriquer : c'est souvent la meilleure réponse en attendant mieux.
10. **Proposer une classe** (`references/classes-d-outils.md`) : 1 essentiel (chaque jour, ou remplace un logiciel), 2 important, 3 confort. Une question suffit : « Si l'outil s'arrêtait une journée, des collègues seraient-ils bloqués ? » La cellule confirme à la mise en service ; la classe 1 ajoute la page du mode dégradé (`creer_projet.py --classe 1`).

### Étape 1 — SPEC et grille provisoire → ✋ Jalon 1

Créer le projet (`python3 scripts/creer_projet.py <nom> --format A|B|C|D`, avec `--niveau partage` pour un simple HTML partagé), lire `references/modele-spec.md` et rédiger `SPEC.md` : 2 pages au maximum, un résumé de cinq lignes en tête pour l'agent. Les points de la grille sur l’architecture, les données et l’IA se déduisent de la SPEC ; ceux qui portent sur le code y figurent comme engagements de conception. **Dès ce jalon, poser les bases de la transmission** : demander en mots simples si la cellule pourrait un jour installer l'outil pour d'autres (noté dans `docs/partage.md`) et proposer un signalement de trois lignes à la cellule, pour qu'elle dise tout de suite si cela existe déjà (`references/partage-et-transmission.md`). Terminer par une demande d'accord en mots simples : je ne construis rien avant votre accord.

### Étape 2 — Prototype cliquable → ✋ Jalon 2

Livrer une v0.1 qui déroule le parcours principal avec des données fictives, la charte appliquée et le squelette du tutoriel. Demander : « Est-ce bien l'outil attendu ? Qu'est-ce qui manque ou gêne ? » Reporter tout changement dans la SPEC avant de continuer.

### Étape 3 — Construction, contrôle, recette → ✋ Jalon 3

1. Construire selon `references/socle-technique.md`, `references/pratiques-de-code.md` et `references/tutoriel-prise-en-main.md` : cœur métier pur dans `src/coeur/`, un test par règle (fonctions `test_…`), aucune erreur avalée, `docs/decisions.md` tenu au fil de l'eau.
2. Relire à froid (liste de `pratiques-de-code.md`), vérifier le code sur les points de la grille qui portent sur le code et rédiger `docs/grille-vigilance.md` (fichiers et lignes cités).
3. Renseigner `docs/composants.md` : version et **date de fin de support de chaque composant, vérifiée sur le site de l'éditeur**.
4. Lancer `python3 build/fabriquer.py` (avec `--exiger-analyses` pour un outil orange) : il écrit **toujours** `dist/dossier-transmission.md` (résumé d'une page et statut, à envoyer à la cellule quand on veut, même inachevé), **exécute les tests** et refuse de fabriquer le paquet durable si l'un échoue, si le code contient une faute de syntaxe ou un motif dangereux, si une version diffère, si une règle n'a ni test ni mention dans le code, si un secret, un appel externe non déclaré, une dépendance non figée, une faille connue ou un compose non conforme est trouvé, ou si un composant n'a plus de support. Ne jamais contourner : corriger, ou noter l'exception.
5. Compléter `docs/partage.md` (potentiel de réutilisation, cellule informée, transmission) et proposer l'exercice de reprise.
6. **Rôle d'éditeur**, tenu par Claude sans charge pour l'agent (`references/role-editeur.md`) : chaque fichier reçu décrit dans `docs/entrees.md` avec un exemple inventé ; mention « Produit avec … » sur les documents produits (brique traçabilité) ; questions-tests pour toute fonction d'IA ; lien « Signaler un problème » dans le tutoriel. Briques communes : `creer_projet.py --briques`.
7. Livrer selon `references/livraison.md` et `references/paquet-integration.md` ; mise en service : recette par le métier → serveur de test → validation selon le niveau → serveur de production.

### Évolutions et reprises

Une fois l'outil en service, son **entretien** (dépannage, évolution, reprise d'un outil sans dossier, veille sur les composants) relève de la skill `entretien-outils`, qui relit et complète le même dossier. En résumé :

- Toute évolution part de la SPEC : RG ajoutée ou modifiée, puis code, test et CHANGELOG. Évolution mineure : une confirmation suffit.
- **Ajout en cours de route :** noté le jour même dans `docs/perimetre.md` ; s'il n'est pas dans la SPEC, la cellule en est informée à la livraison.
- Outil qui garde des données : **cloner, tester, puis produire** (`references/scripts-exploitation.md`).
- Réévaluer la grille à chaque évolution importante : nouvelle donnée, nouvel accès, nouvelle connexion, ouverture à d'autres services ou à l'extérieur.
- Reprise dans une nouvelle session : lire d'abord `README.md`, `SPEC.md`, `CHANGELOG.md`, `docs/grille-vigilance.md`, `docs/derogations.md` et `docs/perimetre.md`. Le dossier fait foi, pas le souvenir d'une conversation.

## Choisir le format

Partir du plus simple ; ne monter d'un cran que si un critère l'impose ; justifier le choix dans la SPEC (la décision est celle de Claude, pas une question à l'agent).

| Format | Quand | Exemples |
|---|---|---|
| **A. HTML autonome** (défaut) | Un utilisateur à la fois, pas de données partagées entre agents, traitement possible dans le navigateur | Comparateur de classeurs, jeu de formation portable, carte de prévisions |
| **B. Web conteneurisé** | Données partagées, traitement serveur (OCR, Python), accès mobile, usage appelé à grossir | Analyse de devis, renommage de documents par lecture automatique, inventaire de terrain, supervision |
| **C. Bureau (MSI)** | Traitement obligatoirement local sans serveur, ou accès aux fichiers du poste | Pseudonymisation locale de documents, conversion de fichiers d’archives |
| **D. Grist (+ widget)** | Surtout un tableau de suivi partagé : ne pas redévelopper ce que Grist fait | Suivi d'équipements |

Le format A échappe à plusieurs points de la grille (pas de stockage serveur, pas d'exposition réseau, pas de comptes). Le format C coûte le plus en maintenance (installation poste par poste, antivirus, signature) : le justifier. Si deux formats coexistent, écrire un seul cœur métier, sans interface, appelé par les deux.

## Douze règles non négociables

Détail dans `references/socle-technique.md` ; entre parenthèses, les sujets de la grille évités.

1. Aucun secret dans le code ni dans le compose : `.env` sur le serveur, `.env.exemple` factice livré (secrets en dur).
2. Aucune donnée envoyée à une IA externe, Cowork compris : développer sur des données fictives ou anonymisées ; jamais d'appel à l'API Anthropic (IA externe).
3. L'outil aide, l'humain décide : aucun classement, score ou tri de personnes sans avis préalable du DPO ; tout résultat est une proposition à vérifier (décision par l'IA, sans vérification humaine).
4. Interne par défaut : joignable seulement depuis le réseau interne, derrière le frontal HTTPS, jamais en direct ; toute ouverture à l'extérieur est une décision écrite (accès depuis Internet).
5. Comptes nominatifs dès qu'il y a des données partagées ; jamais de compte générique sans exception notée ; mots de passe hachés (authentification, mots de passe et comptes partagés). Mode d'authentification standard : en attente.
6. Journal « qui, quoi, quand » pour toute donnée partagée (traçabilité).
7. Composants figés et vérifiés : versions précises, analyse des vulnérabilités à chaque version (code ni relu ni analysé). Tests exécutés et réussis avant toute livraison.
8. Un référent et un suppléant par fonction, procédure de mise à jour écrite, code déposé chez la DSI à chaque version (une seule personne, documentation et code non remis).
9. **Composants maintenus :** chaque composant est listé avec sa date de fin de support ; un composant sans support n'est pas livré (hors grille).
10. **Tout fichier reçu est suspect :** taille et type contrôlés, XML sans entités externes, exports tableur neutralisés contre les formules, rien d'importé inséré tel quel dans une page.
11. **Appels réseau déclarés :** toute adresse écrite dans le code figure dans `reseau-autorise.txt` avec sa raison, aucune n'est construite à l'exécution ; en format A, chaque page porte la balise de sécurité (CSP) que `fabriquer.py` indique : c'est le navigateur qui bloque le reste (IA externe).
12. **Une exception se note :** `docs/derogations.md` (règle, raison, décideur par fonction, date de revue, avis demandé). Un ajout hors SPEC se note dans `docs/perimetre.md`.

Deux habitudes : travailler sur une **copie** des fichiers fournis, jamais sur l'original ; chaque bouton qui copie ou télécharge **confirme visiblement** ce qui s'est passé.

## Tutoriel de prise en main (obligatoire)

Chaque application embarque une visite guidée qui se lance seule à la première ouverture, éclaire les vrais éléments de l'écran, se relance par un bouton permanent « ? Prise en main » et s'accompagne d'un guide imprimable. Utiliser le module prêt à l'emploi `assets/prise-en-main/` et son test, selon `references/tutoriel-prise-en-main.md`.

## Versions, documentation et paquet d'intégration

- Numéro x.y.z (correction / évolution compatible / changement d'usage ou de données), tenu dans le seul fichier `VERSION`, affiché dans l'application (`APP_VERSION`) et en tête de chaque document.
- `scripts/creer_projet.py` crée le projet avec tous les gabarits ; `build/fabriquer.py` exécute les tests, contrôle le code et le projet, puis fabrique `dist/<nom>_vX.Y.Z.zip`, son empreinte, la fiche DSI et le bilan (réussi, refusé, signalé, non testé). `scripts/autotest_fabrique.py` et `scripts/essai_playbooks.py` vérifient que ces garde-fous refusent bien ce qu'ils doivent refuser.
- Format B : compose durci, vhost, playbooks Semaphore de déploiement et de contrôle (Podman ou Docker), inscription dans la supervision : `references/paquet-integration.md`.

## Articulation avec les autres skills

- `entretien-outils` : tout ce qui suit la mise en service (dépannage, évolution, reprise sans dossier, veille) ; le dossier de l'outil est le contrat entre les deux skills.
- Grille de vigilance de votre cybersécurité : intégrée dans `references/grille-vigilance.md` (modèle à remplir) ; si votre cybersécurité a sa propre skill, elle prime en cas d'écart.
- Skill de charte graphique de votre collectivité, si elle existe : toujours, avant toute interface.
- Skills de cartographie, de modèles de note ou de courrier de votre collectivité, si elles existent : elles fixent la forme ; la fabrique ajoute SPEC, tutoriel, versions et documentation.

## Pour aller plus loin

`references/classes-d-outils.md` (trois classes, ce que coûte une panne, ce que le dossier doit contenir) · `references/role-editeur.md` (rustines, contrat d'entrée, traçabilité, IA dans les outils, briques communes, revue du parc) · `references/registre-des-outils.md` (le registre des outils, registre du parc, et la fiche à coller dans chaque carte) · `references/pratiques-de-code.md` (pratiques des meilleures équipes, relecture à froid, ce que le contrôle refuse) · `references/curseur-declenchement.md` · `references/partage-et-transmission.md` · `references/decisions-a-prendre.md` (ce qui n'est pas encore décidé, avec décideur) · `references/historique.md` (versions et limites connues) · `references/fiche-observation-test.md` (si la cellule teste la skill).
