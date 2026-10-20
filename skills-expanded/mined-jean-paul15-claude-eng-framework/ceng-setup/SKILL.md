---
name: ceng-setup
description: Installer, initialiser, mettre à jour, diagnostiquer ou désinstaller claude-eng-framework (ceng) dans un projet, sur n'importe quelle machine. À utiliser quand l'utilisateur demande d'« installer le framework », « installer ceng », « initialiser claude-eng-framework », de le mettre à jour, ou quand un projet cloné contient déjà un dossier .ceng/ sur une nouvelle machine.
---

# Installer et initialiser claude-eng-framework

Dépôt : https://github.com/Jean-Paul15/claude-eng-framework (Apache-2.0). Prérequis : Node ≥ 22, git, Claude Code.
Tu ne peux pas répondre aux questions interactives de `ceng init` (pas de terminal interactif) : **c'est toi qui
poses les questions à l'humain, puis tu passes ses réponses en options.**

## 1. Disposer de la CLI
- `ceng --version` répond → utiliser `ceng`.
- Sinon, sans installation globale : préfixer chaque commande par `npx -y github:Jean-Paul15/claude-eng-framework`
  (ex. `npx -y github:Jean-Paul15/claude-eng-framework init …`).
- Installation globale (si l'humain le souhaite) : `npm install -g github:Jean-Paul15/claude-eng-framework`.

## 2. Nouveau projet (pas de dossier `.ceng/`)
1. Aperçu sans écriture : `ceng init --dry-run` → lis le type de projet, la stack, le risque et les domaines détectés.
2. Pose les questions avec **l'outil de questions de Claude Code** (`AskUserQuestion` : options cliquables, option
   recommandée en premier avec « (Recommandé) », l'humain peut toujours répondre librement). Un appel = 4 questions
   maximum : un premier appel pour risque, autonomie, budget et parallélisme ; un second pour graphify ; l'objectif
   en texte libre. Sans cet outil (environnement qui ne l'offre pas), poser les mêmes questions en un seul message.
   Valeurs recommandées = celles détectées :
   - risque : `low` · `medium` · `high` · `critical` (argent, santé, infra de production) ;
   - autonomie : `supervised` · `balanced` (défaut) · `high` — les actions irréversibles restent toujours soumises à l'humain ;
   - budget de tokens : `economy` · `balanced` (défaut) · `quality` ;
   - parallélisme : `off` · `subagents` (défaut) · `teams` (Agent Teams, expérimental, plus coûteux) ;
   - stade : `production` (défaut : garde-fous complets) · `prototype` (aucun utilisateur réel, une erreur ne coûte rien :
     migrations, déploiements, suppressions, push et fichiers de garde-fous sans validation, instantané avant
     suppression ; secrets, suppression hors du dépôt, push forcé sur une branche protégée d'un dépôt partagé,
     publication et infrastructure restent soumis à l'humain). Ne propose `prototype` que si l'humain dit que le
     projet n'a pas de vrais utilisateurs ; ne le choisis jamais à sa place ;
   - objectif du projet en une phrase ;
   - installer graphify (graphe de code automatique, sans coût IA) ? oui par défaut.
3. Lance : `ceng init --yes --risk <…> --autonomy <…> --budget <…> --parallelism <…> --goal "<…>" --install-graphify`
   (ou `--code-graph off` si l'humain refuse graphify ; `--stage prototype` s'il a choisi le stade prototype).
4. Bascule automatique (validations par l'invite, expiration → travail sans humain) : propose via l'invite de
   régler `"askUserQuestionTimeout": "10m"` dans ses paramètres **utilisateur** (`~/.claude/settings.json`, ou
   `/config` → « Question auto-continue timeout ») — c'est ce qui permet à une invite sans réponse d'expirer. Ne
   modifie ce fichier qu'avec son accord.
5. Montre à l'humain les **recommandations** affichées (elles expliquent les écarts entre ses choix et la réalité du projet).
6. `ceng doctor` : tout doit être ✔ (sauf éventuellement `claude`/`graphify` selon la machine — à signaler).
7. Projet vide : après la mise en place de la stack, `ceng upgrade` relance la découverte (skills, agents et commandes adaptés).

## 3. Projet déjà initialisé, nouvelle machine ou clone
Rien à installer pour travailler : la CLI et les hooks sont copiés dans le dépôt (`.ceng/runtime/`).
- Diagnostic : `node .ceng/runtime/cli.js doctor`.
- Graphe de code absent sur cette machine : `node .ceng/runtime/cli.js graph install` (installe le paquet Python
  `graphifyy`, avec l'accord de l'humain) puis `node .ceng/runtime/cli.js graph build`.
- Premier lancement de Claude Code dans le dossier : accepter le dialogue de confiance (sinon les règles
  `permissions.allow` du projet sont ignorées).

## 4. Travailler
- `/ceng-orchestrate` dans Claude Code (ou `ceng run` dans un terminal) : la skill `ceng-orchestrate` prend le relais.
- Le travail ordinaire avec Claude reste possible à tout moment : le framework n'est qu'un ensemble de fichiers du projet.

## 5. Stade, commandes de gates, mise à jour
- Stade d'un projet existant : `ceng config stage` (lecture) ; `ceng config stage prototype|production` (écriture : validation
  humaine — c'est un changement du niveau des garde-fous). Le passage en production redemande donc l'humain.
- Commandes de gates déduites de la vraie pile (app Flutter dans `app/`, fonctions Deno…) : `ceng config detect`, puis
  `ceng config detect --apply` (écrit `.ceng/config.json` : validation humaine).
- Mise à jour du projet vers la dernière version : `npx -y github:Jean-Paul15/claude-eng-framework upgrade`
  (ou `ceng upgrade` après mise à jour de l'installation globale). Les fichiers modifiés localement sont préservés.
- Désinstallation : `ceng uninstall --yes` (garde le Project Brain) ; `--purge` supprime aussi `.ceng/` — action
  destructive : confirmation explicite de l'humain d'abord.

Documentation complète : `docs/` du dépôt (installation, configuration, orchestration, sécurité, dépannage).
