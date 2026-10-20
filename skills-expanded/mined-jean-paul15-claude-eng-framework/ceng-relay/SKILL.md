---
name: ceng-relay
description: Coordination entre plusieurs sessions Claude Code qui travaillent en parallèle (worktrees), pour signaler un point d'arrêt sans coût de jetons, réveiller la session de coordination, passer une session sur un modèle plus fort (Opus) au bon moment et travailler en équipe autonome sans humain devant l'écran.
---

# Relais entre sessions et équipe autonome

Plusieurs sessions travaillent sur un même dépôt dans des copies de travail (worktrees). Elles ne peuvent pas s'attendre en
lisant tout le temps un fichier (coûteux). Le relais fait l'inverse : **une session signale, la coordination est réveillée**.

## Pour une session de travail (émettre)
Quand tu atteins un point d'arrêt (dossier d'intégration prêt, blocage, décision à prendre), écris d'abord ton dossier d'une page
dans le dépôt, puis **émets un événement** et arrête-toi :
`node .ceng/runtime/cli.js relay emit --kind opus-ready --session <nom> --ref <dossier.md> --note "<une phrase>"`
Types : `opus-ready` (passer sur un modèle plus fort), `opus-done` (verdict rendu), `blocked`, `decision-needed`, `custom`.
Un événement n'est qu'un signal : tout le contexte vit dans le fichier désigné par `--ref`. Ne recopie pas l'historique.

## Pour la session de coordination (écouter, agir)
1. Lancer UNE fois l'écoute en tâche de fond avec l'outil **Monitor** (une ligne JSON par événement, rien tant qu'il ne se passe rien) :
   `node .ceng/runtime/cli.js relay watch --reader coordination --interval 5`
2. À chaque ligne reçue, lire le champ `action` et l'appliquer :
   - `opus-ready` : changer le modèle de la session visée (outil de gestion de sessions `set_session_model`, valeur Opus), puis lui envoyer
     un message court : « Lis <ref> et exécute le point d'arrêt. » Elle garde tout son contexte : ne rien lui re-expliquer.
   - `opus-done` : repasser la session sur Sonnet (`set_session_model`), lire le verdict dans le fichier désigné.
   - `blocked` / `decision-needed` : débloquer ou présenter la décision à l'humain en deux phrases.
3. `node .ceng/runtime/cli.js relay events` liste ce qui n'a pas été traité (au cas où l'écoute s'est arrêtée) ; `relay ack` le marque traité.

## Équipe autonome (`ceng team on`, action humaine)
Quand plusieurs sessions travaillent sans humain devant l'écran, les boîtes de permission bloqueraient tout. Le mode équipe les remplace par
une liste de sécurité fermée, journalisée : lecture, recherche, coordination entre sessions et outils locaux passent ; ce qui agit hors de la
machine (base de production, déploiement, e-mail, paiement, secrets) ou change les permissions est **refusé proprement et consigné** dans
`.ceng/brain/pending-approvals.md` pour l'humain, sans jamais attendre. Ne jamais réessayer ni contourner une action consignée : continuer autrement.
`ceng team status` montre l'état ; `--allow` / `--defer` ajustent la liste pour un outil MCP précis.

## Économie de jetons
Contexte dans des fichiers stables, pas dans la conversation ; un événement = une consigne courte ; une session inactive ne coûte rien ;
le modèle fort n'intervient que sur le point d'arrêt demandé, puis on revient au modèle courant.
