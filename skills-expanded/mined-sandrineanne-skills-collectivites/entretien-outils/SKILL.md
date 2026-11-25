---
name: entretien-outils
description: "Entretien des outils maison d'une collectivité, déjà en service, fabriqués avec Claude ou non : dépannage, évolution, reprise d'un outil sans documentation, veille sur les composants. DÉCLENCHER quand un outil existant ne marche plus ou mal (erreur, page blanche, chiffres faux, ne démarre plus, lenteur, après une mise à jour), quand on veut le faire évoluer, quand il faut reprendre un outil dont l'auteur est parti ou qui n'a pas de dossier, quand une faille ou une fin de support touche ses composants, ou pour une revue régulière des outils. NE PAS DÉCLENCHER pour créer un nouvel outil (skill fabrique-outils), pour un progiciel d'éditeur (progiciel de gestion du courrier, progiciel de gestion du patrimoine, outil de tickets… : support de l'éditeur) ni pour un fichier jetable. Impose : remettre en marche avant de comprendre, ne jamais travailler sur l'original, un défaut corrigé = un test ajouté, le dossier de l'outil fait foi, Claude prépare et un humain habilité exécute en production."
metadata:
  version: "0.1.2"
---

# Entretien des outils maison

Cette skill prend le relais de `fabrique-outils` une fois l'outil en service : elle le dépanne, le fait évoluer, le reprend quand personne ne sait plus comment il marche, et surveille ce sur quoi il repose. Les deux skills partagent un contrat : **le dossier de l'outil** (README, SPEC, CHANGELOG, `docs/`, `build/fabriquer.py`). La fabrique le crée ; l'entretien le relit, le corrige et le complète à chaque passage. Un outil sans dossier en reçoit un (parcours 2).

## Parler à la personne (à lire en premier)

La personne en face est souvent inquiète (« ça ne marche plus ») et n'est pas forcément celle qui a fabriqué l'outil : référent, suppléant, utilisateur, cellule ou DSI. Lire `references/dialogue-entretien.md` avant la première question :

- Commencer par rassurer et annoncer la méthode : « On va d'abord remettre l'outil en marche, ensuite comprendre ce qui s'est passé. »
- Une seule question à la fois, en mots simples, chacune avec sa raison ; « je ne sais pas » est une bonne réponse.
- Dire ce que l'on fait, au fur et à mesure ; jamais de jargon sans explication ; jamais de reproche (on cherche ce qui a permis le problème, pas un coupable).
- Détails techniques à la demande pour la DSI ou la cellule.

## Cinq règles

1. **Remettre en marche avant de comprendre.** Quand quelqu'un est bloqué, on revient d'abord à la dernière version qui marchait (retour arrière, restauration), puis on cherche la cause.
2. **Ne jamais travailler sur l'original, ne jamais corriger la production sans trace.** Copie de travail, sauvegarde avant toute action, chaque geste noté. Aucune donnée réelle dans la conversation (règle 2 de la fabrique) : on reproduit avec des exemples inventés ou anonymisés.
3. **Un défaut corrigé = un test ajouté.** Le test qui reproduit le défaut s'écrit avant la correction ; il reste dans `tests/` pour que le défaut ne revienne jamais.
4. **Le dossier fait foi, et il s'améliore à chaque passage.** Version, CHANGELOG, journal des incidents, composants : on laisse le dossier plus juste qu'on ne l'a trouvé.
5. **Claude prépare, un humain habilité exécute en production.** Claude écrit les commandes, les correctifs, les playbooks et les messages ; le geste sur un serveur ou une diffusion aux utilisateurs est fait par la personne qui en a le droit (`references/roles-et-decisions.md`).

## Avant tout : la classe de l'outil

Lire la ligne « Classe » du README (ou la fiche du registre) : **1 essentiel** (chaque jour, ou remplace un logiciel : remise en marche le jour même, mode dégradé donné tout de suite aux agents), **2 important** (dans la semaine), **3 confort** (prochaine évolution). Sans classe, en proposer une et la faire confirmer par la cellule (`remettre_a_niveau.py --classe N`). Rôles, délais et décisions en attente : `references/roles-et-decisions.md`.

## Le tri : quel parcours ?

| Ce que dit la personne | Parcours | Référence |
|---|---|---|
| « Ça ne marche plus », erreur, page blanche, chiffres faux, très lent, ne démarre plus | 1. Dépannage | `references/depannage.md` |
| « Personne ne sait comment il marche », « l'auteur est parti », outil sans README ni SPEC | 2. Reprise d'un outil sans dossier | `references/reprise-sans-dossier.md` |
| « Il faudrait ajouter… », « la règle a changé », « d'autres services veulent l'utiliser » | 3. Évolution | `references/evolution.md` |
| Faille annoncée, fin de support d'un composant, revue trimestrielle | 4. Veille | `references/veille.md` |

Un dépannage peut révéler une reprise (pas de dossier) ou une évolution (le besoin a changé) : finir d'abord la remise en marche, puis enchaîner. Pour un progiciel d'éditeur, orienter vers son support ; pour un fichier jetable, simplement le corriger.

**Gravité** (dépannage) : **bloquant** — des agents ne peuvent plus travailler, ou des données sont en jeu : remettre en marche tout de suite, prévenir la cellule ; **gênant** — un contournement existe : corriger dans la journée ou la semaine ; **mineur** — gêne d'affichage : corriger à la prochaine évolution.

**Données de personnes exposées, perdues ou modifiées : prévenir le DPO sans attendre** (une violation de données personnelles doit, sauf risque improbable, être notifiée à la CNIL dans les 72 heures après en avoir eu connaissance) ; soupçon d'attaque : prévenir la cybersécurité. Claude aide à écrire un message factuel, sans données de personnes.

## Parcours 1 — Dépannage

1. **Trier** : trois questions (qui est bloqué, depuis quand, qu'est-ce qui a changé juste avant) et la question des données de personnes.
2. **Stabiliser** : retour à la dernière version qui marchait (format B : image `avant-maj` ou sauvegarde ; format A : fichier de la version précédente ; format C : MSI précédent ; Grist : sauvegarde ou historique du document).
3. **Diagnostiquer** : version en service, CHANGELOG, message d'erreur exact, journaux, `playbook_check.yaml` ; tableau des symptômes par format dans `references/depannage.md`.
4. **Corriger** : test qui reproduit le défaut → correction minimale → tous les tests → `scripts/nouvelle_version.py <dossier> correction "…"` → `build/fabriquer.py` → serveur de test → production.
5. **Clore** : une ligne dans `docs/incidents.md`, un message simple aux utilisateurs, un retour d'expérience de cinq lignes pour un incident bloquant.

## Parcours 2 — Reprise d'un outil sans dossier

Ne rien réécrire : d'abord mettre à l'abri, puis documenter, puis améliorer.

1. **Mettre à l'abri** : copie de travail, sauvegarde des données ; un secret trouvé dans le code est renouvelé.
2. **Relever l'existant** : `scripts/releve_outil.py <copie>` (fichiers, format probable, dépendances, bibliothèques embarquées, appels externes, secrets masqués, données de personnes possibles).
3. **Écrire des tests de caractérisation** : ce que l'outil fait aujourd'hui, sur des exemples inventés, même si ce comportement est discutable.
4. **Reconstruire le dossier** : `scripts/remettre_a_niveau.py <copie> --copie --format …` ajoute ce qui manque **sans jamais écraser** ; Claude remplit README, SPEC reconstituée (règles déduites du code, à confirmer par le métier), composants avec leurs dates de fin de support (vérifiées en ligne).
5. **Contrôler en brouillon et prioriser** : `build/fabriquer.py --brouillon`, puis l'ordre de `references/reprise-sans-dossier.md` ; ce qui ne se corrige pas tout de suite devient une exception datée.
6. **Transmettre** : dossier de transmission à la cellule, outil ajouté à l'inventaire.

## Parcours 3 — Évolution

Demande en mots simples → impact (règles, données, accès, composants, curseur de la fabrique) → nature de la version (correction, évolution compatible, changement d'usage) et validation qui va avec → SPEC d'abord → test d'abord → code → `scripts/nouvelle_version.py` → `build/fabriquer.py` → test puis production → CHANGELOG en langage métier et encadré « Nouveautés » du tutoriel → information de la cellule. Détail : `references/evolution.md`.

## Parcours 4 — Veille

`scripts/veille_outils.py <dossier des outils>` lit le dossier de chaque outil et classe ce qui est à traiter maintenant (support terminé, incident ouvert, contrôle en échec), à planifier (fin de support dans moins de 6 mois, restauration jamais essayée ou ancienne, exception à revoir) ou en ordre ; `--chercher php` retrouve en une commande les outils touchés par une faille. Revue trimestrielle, éventuellement en tâche programmée ; chaque année, **revue du parc** : garder, mutualiser, retirer ou remonter au processus, rustines réexaminées, questions-tests d'IA rejouées (`references/veille.md`).

## Scripts (bibliothèque standard Python, testés par `scripts/autotest_entretien.py`)

| Script | Rôle |
|---|---|
| `nouvelle_version.py` | Passe à la version suivante partout à la fois (VERSION, README, documents, APP_VERSION, compose, CHANGELOG) ; `--simulation` montre sans écrire |
| `releve_outil.py` | Relevé d'un outil existant, sans le modifier |
| `remettre_a_niveau.py` | Ajoute le dossier manquant à une copie d'outil, sans rien écraser (gabarits de la fabrique) |
| `veille_outils.py` | Revue de tous les outils d'un dossier ; code de sortie 1 s'il y a quelque chose à traiter maintenant |

Les contrôles eux-mêmes restent ceux de la fabrique : `build/fabriquer.py`, présent dans le dossier de chaque outil.

## Articulation

- `fabrique-outils` : socle technique, grille de vigilance, gabarits, `fabriquer.py`, curseur de déclenchement ; à relire quand une évolution fait monter le niveau d'un outil, ou pour une refonte complète.
- Registre des outils de la collectivité : le registre du parc. Après chaque version, incident clos ou revue, recoller la fiche `dist/fiche-registre.txt` dans la carte de l'outil ; pour un outil sans dossier, utiliser la fiche type (`registre-des-outils.md` de la fabrique).
- Skill de charte graphique de votre collectivité, si elle existe : pour toute modification d'interface.
- Skill de modèle de note, si elle existe : note d'incident ou d'arbitrage à la hiérarchie.

## Pour aller plus loin

`references/roles-et-decisions.md` (qui fait quoi en production, décisions en attente) · `references/historique.md` (versions et limites connues).
