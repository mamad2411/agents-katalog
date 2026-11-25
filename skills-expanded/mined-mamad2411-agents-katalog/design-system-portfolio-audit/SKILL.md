---
name: design-system-portfolio-audit
description: >-
  Audits an existing React portfolio or web application to extract, formalize, and document design system foundations. Identifies design tokens (colors, typography, spacing, shadows, border-radius, z-index, animations), analyzes component structure and reusability, detects hardcoded styles and visual inconsistencies, and generates a structured audit report, a tokens.json file, and a prioritized implementation roadmap. Use whenever the user asks to audit their existing portfolio or codebase to create a design system, extract tokens, inspect component reusability, or evaluate visual consistency.
---

# Design System Portfolio Audit Skill

Ce skill guide l'agent pour auditer un portfolio ou une application React existante, en extraire les fondations d'un Design System pérenne, et produire un rapport d'audit détaillé accompagné d'un fichier `tokens.json` et d'une feuille de route priorisée.

---

## Ressources Disponibles

- [Modèle de Rapport d'Audit](./resources/audit-report-template.md)
- [Schéma JSON des Tokens (`tokens-schema.json`)](./resources/tokens-schema.json)
- [Modèle de Feuille de Route (`roadmap-template.md`)](./resources/roadmap-template.md)

---

## Workflow d'Audit en 5 Phases

### Phase 1 : Cartographie & Détection de la Stack
1. **Identifier l'architecture CSS** :
   - Inspecter `package.json`, `tailwind.config.js`, `postcss.config.js`, `vite.config.js`.
   - Repérer la méthode de style principale (Tailwind CSS, CSS pur, CSS Modules, Styled Components, etc.).
2. **Localiser les fichiers clés** :
   - Fichiers de styles globaux (`src/index.css`, `src/App.css`, variables CSS).
   - Dossier des composants (`src/components/`, `src/sections/`, `src/pages/`).
   - Fichiers de données ou configuration UI (`src/data/`, locales JSON).

---

### Phase 2 : Extraction & Formalisation des Tokens

Scanne le projet pour répertorier l'ensemble des valeurs de design :

1. **Couleurs** :
   - Examiner `tailwind.config.js` (`theme.colors` ou `theme.extend.colors`).
   - Scanner les variables CSS (`:root { --... }`).
   - Détecter les couleurs en dur (*hardcoded*) dans les fichiers JSX/CSS via recherche de patterns hex (`#...`), rgb/rgba ou classes arbitraires Tailwind (`bg-[#...]`, `text-[#...]`).
2. **Typographie** :
   - Polices déclarées (`fontFamily`), liens Google Fonts / `@font-face`.
   - Échelle de tailles (`fontSize`), graisses (`fontWeight`), hauteurs de ligne (`lineHeight`).
3. **Espacements & Grille** :
   - Unités dominantes (`px`, `rem`, multiples de 4px ou 8px).
   - Constater si les marges/paddings dérivent d'une échelle systématique ou de valeurs ad-hoc.
4. **Élévations & Rayons (Shadows & Border Radius)** :
   - Ombres portées (`box-shadow`, `drop-shadow`).
   - Rayons de courbure (`rounded-*`, `border-radius`).
5. **Breakpoints & Transitions** :
   - Points de rupture responsive (`sm`, `md`, `lg`, `xl`).
   - Durées et courbes d'animation (`duration-*`, `ease-*`, `requestAnimationFrame`).

---

### Phase 3 : Analyse des Composants

Pour chaque composant React identifié dans le projet :
1. **Responsabilité & Scope** : Bouton, Carte, Navbar, Modale, Layout, Section de contenu.
2. **Props & Types** : Liste des propriétés acceptées et typage (explicite ou implicite).
3. **États & Variantes** : Prise en charge des états (`hover`, `active`, `focus-visible`, `disabled`, `loading`).
4. **Niveau de Réutilisabilité (Score 1 à 5)** :
   - `1/5` : Composant monolithique totalement couplé à une page unique.
   - `3/5` : Composant paramétrable mais contenant des valeurs de styles codées en dur.
   - `5/5` : Composant pur, hautement composable et découplé de la donnée métier.
5. **Matrice Récapitulative** :
   Synthétiser dans un tableau markdown :
   `| Composant | Fichier | Rôle | Props | Variants | Réutilisabilité | Dépendances |`

---

### Phase 4 : Détection des Patterns, Incohérences & Dette Visuelle

Évaluer la santé globale du design system :
- **Taux d'incohérence chromatique** : Proportion de couleurs arbitraires non répertoriées dans la palette officielle.
- **Micro-décalages d'espacement** : Ex. composants utilisant tantôt 12px, tantôt 10px ou 14px pour un espacement similaire.
- **Multiplication des polices ou graisses** : Utilisation de graisses redondantes sans justification hiérarchique.
- **Z-Index "Magic Numbers"** : Valeurs arbitraires (`z-50`, `z-[999]`, `z-[9999]`) non centralisées dans un système d'empilement.
- **Doublons de composants** : Deux composants distincts ayant 80% de structure commune qui mériteraient d'être fusionnés avec une prop `variant`.

---

### Phase 5 : Génération des Livrables

L'audit aboutit à 3 livrables concrets :

1. **Rapport d'Audit Complet (`ds-audit-report.md`)** :
   - Rédigé selon le template [resources/audit-report-template.md](./resources/audit-report-template.md).
   - Inclut le score de santé global (% cohérence), l'analyse des composants et la liste des anomalies.
2. **Fichier `tokens.json` Standardisé** :
   - Conforme au schéma [resources/tokens-schema.json](./resources/tokens-schema.json).
   - Prêt à être importé dans Tailwind, Style Dictionary ou un outil d'export Figma.
3. **Feuille de Route Priorisée (`ds-roadmap.md`)** :
   - Basée sur [resources/roadmap-template.md](./resources/roadmap-template.md).
   - Organisée en 4 niveaux de priorité (Tokens de base → Refactoring composants → Showcase vivante → Export Figma).

---

## Conseils Opérationnels pour l'Agent

- **Inspecter avant d'affirmer** : Utiliser les outils de recherche (`grep_search`, `view_file`) pour compter précisément les occurrences réelles plutôt que de formuler des suppositions.
- **Respecter l'existant** : Ne pas chercher à remplacer immédiatement tout le code, mais cartographier fidèlement l'état des lieux pour offrir une transition progressive sans régression.
- **Proposer du code directement exploitable** : Quand une incohérence majeure est relevée, fournir la configuration Tailwind ou le composant refactorisé correspondant.
