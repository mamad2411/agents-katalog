---
name: arriere-garde
description: >-
  Porte de sécurité « avant mise en ligne » pour sites et applications vibe-codés (Supabase, Vercel,
  Next/React, API). Utiliser dès qu'un projet touche à des comptes, des paiements, des données
  personnelles, ou avant tout déploiement / après un redesign. Trois étages : pré-vol statique
  gratuit (secrets, RLS, colonnes sensibles, variables d'environnement, en-têtes), revue senior par
  checklist, puis test d'intrusion autorisé (Strix) sur une cible possédée et non productive, sous
  devis et GO humain. Règle fondatrice : jamais « sécurisé » sans preuve, et toujours la liste de ce
  qui n'a pas été testé.
---

# Arrière-Garde — la porte avant la mise en ligne

Avant-Garde cadre *avant* d'écrire du code. Arrière-Garde vérifie *avant* de mettre en ligne.
Ce skill existe parce qu'une IA est très forte pour dire « c'est sécurisé » quand ça ne l'est pas,
et parce que les premiers sites d'un vibe-codeur portent toujours les mêmes cinq fautes. Il sert
autant au débutant qu'à l'assistant qui l'accompagne.

## 0. Règles fondatrices (prévalent sur tout)

1. **Jamais de verdict sans preuve.** « Sécurisé » ne s'écrit qu'après un test qui a *échoué à
   entrer*. Sinon on écrit « non testé » — et on liste ce qui n'a pas été testé.
2. **On ne vérifie que ce qui nous appartient.** Une cible dont l'humain n'atteste pas la propriété
   (ou une autorisation écrite) n'est pas testée. Point. (Tester le site d'un tiers est un délit.)
3. **Jamais sur la production.** L'étage 3 tourne en local ou sur une préproduction jetable, avec
   une base de données de test.
4. **Devis avant dépense, GO humain.** L'étage 3 consomme des tokens et du temps : il passe par
   `scripts/devis-strix.mjs`, qui affiche le devis et s'arrête tant que le jeton humain n'existe pas
   (`.cockpit_go` du plugin ultracode-cockpit, ou `ARRIERE_GARDE_GO=1` posé par l'humain dans son
   terminal). L'assistant ne crée jamais ce jeton.
5. **Un rapport, pas une opinion.** Le livrable est `.arriere-garde/rapport.md` : constats, preuves,
   correctifs, et la colonne « non testé ».
6. **Pédagogie.** Chaque constat s'accompagne d'une phrase qui explique *pourquoi* c'est une faute,
   en français simple. Le débutant doit repartir en comprenant, pas seulement en ayant corrigé.

## 1. Quand la porte sonne

L'assistant déclenche ce skill, sans attendre qu'on le lui demande, quand l'une de ces conditions est
vraie :
- le projet a des **comptes utilisateurs**, un **paiement**, ou stocke des **données personnelles** ;
- le projet utilise **Supabase, Firebase, ou un back-end as a service** ;
- on s'apprête à **déployer** (Vercel, Netlify, VPS) ou on vient de finir un **redesign** ;
- l'humain dit « c'est bon, on peut mettre en ligne ».

Il annonce alors : *« Arrière-Garde : avant la mise en ligne, trois étages. L'étage 1 est gratuit et
prend cinq minutes. »*

## 2. Étage 1 — pré-vol statique (gratuit, 5 minutes)

```bash
node <skill>/scripts/preflight.mjs .            # depuis la racine du projet
```

Il lit le dépôt et rend un rapport sur les cinq fautes du vibe-codeur :

| # | Faute | Ce que le script cherche | Pourquoi c'est grave |
|---|---|---|---|
| 1 | **Secret dans le code ou l'historique git** | motifs de clés (OpenAI, Anthropic, Stripe, Supabase `service_role`, AWS, tokens GitHub), fichiers `.env*` suivis par git, `.env` absent du `.gitignore` | une clé commitée est publique pour toujours, même supprimée ensuite |
| 2 | **Clé serveur exposée côté client** | `service_role`, `SUPABASE_SERVICE`, `STRIPE_SECRET` dans des fichiers servis au navigateur ; variables `NEXT_PUBLIC_*` / `VITE_*` au nom sensible | tout ce qui est `PUBLIC_` est lisible dans le navigateur par n'importe qui |
| 3 | **Tables Supabase sans RLS** | migrations/SQL : `create table` sans `enable row level security` ni `create policy` correspondante | sans RLS, la clé publique du site lit et écrit toute la table |
| 4 | **Colonnes sensibles modifiables par leur propriétaire** | colonnes `is_admin`, `role`, `plan`, `credits`, `balance`, `verified` dans des tables où une policy d'`update` vise l'utilisateur lui-même | la RLS « chacun modifie sa ligne » permet de se nommer admin soi-même |
| 5 | **Configuration de déploiement** | `vercel.json` / `next.config` : en-têtes de sécurité absents (CSP, HSTS, X-Frame-Options), CORS `*`, `NODE_ENV` ou debug en prod | la configuration par défaut n'est pas une configuration sûre |

Sortie : `.arriere-garde/preflight.json` + un résumé lisible. **Tout FAIL de l'étage 1 se corrige avant
l'étage 2** — c'est gratuit, et l'étage 3 le trouverait de toute façon en payant.

Le script est un filet, pas un juge : il ne lit pas la base de données réelle. Pour Supabase, l'humain
vérifie lui-même dans le tableau de bord (Authentication → Policies) que **chaque** table a RLS activée
— le script lui donne la liste des tables trouvées dans les migrations pour cocher.

## 3. Étage 2 — revue senior (checklist, 20-40 minutes, gratuit)

Lire `references/revue-senior.md` et la dérouler avec l'humain, domaine par domaine : identité et
sessions, autorisations (le fameux « peut-on lire l'objet d'un autre en changeant l'identifiant ? »),
validation des entrées, secrets et configuration, dépendances, journalisation et limites de débit,
données personnelles (RGPD : minimisation, durée, droit d'effacement). Chaque ligne se termine par
**OK / À corriger / Non testé**. On n'écrit pas OK sans avoir regardé.

Le test manuel de la vidéo Supabase est dans cette étape : prendre la clé publique du site, appeler
l'API depuis l'extérieur (`curl`, sans session), et **lire ce qui répond**. Si une table répond, la RLS
manque. C'est gratuit, et c'est la preuve la plus parlante pour un débutant.

## 4. Étage 3 — test d'intrusion autorisé (Strix, sous devis)

[Strix](https://github.com/usestrix/strix) (Apache 2.0) lance des agents qui tentent de vraies
exploitations sur la cible et fournissent preuve + correctif. Il tourne sur **ta** clé de modèle.
Prérequis : Docker en marche, `pip install strix-agent` (ou l'installateur du projet, lu avant
d'être exécuté).

Toujours à travers le devis :

```bash
node <skill>/scripts/devis-strix.mjs --target http://localhost:3000 --owner "oui, préprod locale du projet X"
```

Le script : (1) refuse toute cible qui ressemble à une production (domaine public sans
`--env preprod` explicite) ; (2) exige l'attestation de propriété `--owner` ; (3) affiche le devis
(modèle, effort, portée, coût attendu) ; (4) s'arrête sans GO humain ; (5) avec GO, lance
`strix --non-interactive --scan-mode <quick|standard> --target …` avec le cadrage de
`references/cadrage-surface.md`, et journalise. Réglages économes par défaut : modèle peu coûteux via
`LLM_API_BASE` (OpenRouter), `STRIX_REASONING_EFFORT=medium`, `--scope-mode diff` quand on ne
vérifie qu'un changement. Un scan complet coûte des centimes à quelques euros : le devis le dit avant.

## 5. Le rapport (`.arriere-garde/rapport.md`)

1. Verdict en une ligne : **BLOQUÉ** (un FAIL critique ouvert) / **OUVERT** (FAIL mineurs, listés) /
   **PASSÉ** (tous les tests ont échoué à entrer) — et **ce qui n'a pas été testé**.
2. Étage 1 : chaque constat, fichier et ligne, correctif, phrase pédagogique.
3. Étage 2 : la checklist remplie.
4. Étage 3 : les constats de Strix avec leur preuve, les correctifs appliqués, et le **re-test**
   (un correctif non re-testé reste « À corriger »).
5. Journal des exécutions (`.arriere-garde/journal.md`).

## 6. Jamais

- Déclarer « sécurisé » sans test échoué à entrer ; cacher un « non testé ».
- Tester une cible dont la propriété n'est pas attestée ; tester une production.
- Créer soi-même le jeton de GO ; lancer Strix hors de `devis-strix.mjs`.
- Corriger en désactivant le contrôle (supprimer une policy « parce qu'elle bloque ») ; le rapport
  le signale comme régression.
- Commiter un secret « temporairement ». Un secret commité se révoque et se régénère, il ne se
  supprime pas.

## Références
`references/revue-senior.md` (étage 2) · `references/cadrage-surface.md` (questions de cadrage avant
l'étage 3) · `references/supabase-vercel.md` (les pièges spécifiques, avec les correctifs) ·
`references/pedagogie.md` (les phrases d'explication pour débutants).
