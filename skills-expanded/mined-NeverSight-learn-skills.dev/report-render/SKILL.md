---
name: report-render
description: "Met en forme un contenu déjà présent dans la conversation (un plan, une explication de changements, ou n'importe quel contenu) en un rapport HTML autonome écrit sur disque et ouvrable au navigateur. Utiliser quand l'utilisateur demande « un rapport HTML », ou après planify / explain-your-changes pour rendre le plan ou les changements. Invocable via /report-render."
argument-hint: "[sujet / quoi mettre en forme]"
allowed-tools: Read, Write, Glob
---

# Rendu d'un rapport HTML

Tu mets en forme, tu ne décides rien. Tu prends un contenu **déjà présent dans la conversation** et tu le coules
dans un rapport HTML autonome. Tu ne reposes aucune question, ne prends aucune décision, et n'inventes aucun
contenu absent de ce qu'on te donne. Même esprit que `planify-write-plan`, mais la sortie est du HTML.

## Entrée

Le contenu à rendre vient de la conversation. Trois cas typiques, tous traités par le **même gabarit** :

- un **plan** produit par `planify` (tâches, contraintes d'acceptation) ;
- une **explication de changements** produite par `explain-your-changes` (diffs + explications fichier par fichier) ;
- un **contenu quelconque** fourni directement par l'utilisateur (analyse, audit, note…).

Si le contenu à mettre en forme est ambigu, prendre le contenu pertinent le plus récent de la conversation.

## Sortie

Un fichier unique : `.reports/<slug>.report.html`.

1. `<slug>` = slug court en kebab-case (2 à 5 mots signifiants) dérivé du sujet. Si on rend un plan `planify`,
   **réutiliser le `<prefix>`** du plan (ex. `report-render` → `.reports/report-render.report.html`).
2. Créer le dossier `.reports/` s'il n'existe pas.
3. Écrire le HTML en suivant **[`references/html-report.md`](references/html-report.md)** : scaffold à copier,
   design system (palette, typo, layout, thème clair/sombre) et catalogue des blocs réutilisables.
4. Chaque `<section>` porte une ancre `data-annote` (ID de tâche `T3` pour un plan, sinon un slug du titre) et la
   **couche d'annotation** est collée avant `</body>` : elle est présente sur **chaque** rapport.

## Règles

- **Contenu réel uniquement** : jamais de texte de remplissage (« lorem »), jamais de section vide inventée.
- Reprendre les **titres, l'ordre et les mots** du contenu source. Tu mets en forme, tu ne réécris pas le fond.
- Le rapport est **autonome** : un seul fichier `.html`, aucune ressource locale annexe.

## Retours

Le rapport embarque une **couche d'annotation** : le lecteur sélectionne un passage, y attache un commentaire, puis
clique sur « Copier les retours » pour récupérer un bloc Markdown. Ce bloc se **colle dans `planify`**, qui localise
chaque passage cité et applique les retours. Détail du format et du composant : `references/html-report.md`.

## Fin

Signaler le chemin écrit sous une forme cliquable (`.reports/<slug>.report.html`) et inviter l'utilisateur à
l'ouvrir dans son navigateur. Préciser qu'il peut **annoter le rapport** (sélection de texte) et **coller ses
retours dans `planify`**.
