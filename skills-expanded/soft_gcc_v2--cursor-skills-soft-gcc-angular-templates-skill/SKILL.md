---
name: soft-gcc-angular-templates
description: >-
  Builds Soft GCC Angular pages from the design-system kit (Tailwind + Angular Material,
  gcc-* templates). Use when creating, migrating, or refactoring Angular screens, layouts,
  lists, forms, fiches employé, paramètres, wizards, dashboards, or any Soft GCC frontend
  UI so styles stay consistent.
---

# Soft GCC — templates Angular

Source de vérité : `design-system/` (galerie sur `npm start` dans ce dossier).
Les maquettes vivent dans `design-system/src/app/layouts/` et `design-system/src/app/ui/`.

## Règle

Toute nouvelle page Angular = **1 layout + 1 page template + des composants `gcc-*`**.

Ne pas inventer un 4ᵉ layout, un header ad-hoc, ni des couleurs de badge.
Ne pas réintroduire PrimeNG, Bootstrap, MUI React, ni du CSS one-shot par écran.

Stack : **Angular + Tailwind CSS + Angular Material**. Typo : **Inter**.

## Workflow

1. Identifier l’écran Soft GCC (liste, fiche, formulaire, dashboard, auth, portail…).
2. Choisir le layout et la page dans [reference.md](reference.md).
3. **Lire** les fichiers `gcc-*` correspondants dans `design-system/src/app/` et les **réutiliser** (copier dans l’app Angular cible si pas encore extraits, ne pas recoder le visuel).
4. Composer uniquement avec les sélecteurs `gcc-*` + widgets Material listés ci-dessous.
5. Vérifier la checklist avant de terminer.

## Choix rapide

| Besoin | Layout | Page |
|---|---|---|
| Après login (menu RH) | `gcc-app-shell` | voir ci-dessous |
| Login / register / 403 | `gcc-auth-shell` | — |
| Questionnaire salarié, attestation publique | `gcc-portal-shell` | Wizard ou confirmation |
| KPI + graphiques | AppShell | Dashboard |
| Tableau (compétences, carrières, retraites, souhaits, évaluations, employés) | AppShell | **ListPage** (défaut, ~80 %) |
| Créer / éditer une entité | AppShell | FormPage |
| Fiche employé, détail dossier | AppShell | DetailPage |
| Paramétrage référentiels | AppShell | SettingsPage |
| Notation, entretien, création de plan | AppShell ou PortalShell | WizardPage |
| Organigramme, matrice, bulletin | AppShell | CanvasPage |

## Composition obligatoire

**ListPage** : `gcc-page-header` → `gcc-filter-bar` → `mat-table` + `mat-paginator` → `gcc-empty-state` si vide. Filtres **jamais** dans le header.

**FormPage** : `gcc-page-header` → une carte blanche → champs `gcc-input` / `gcc-select` → Annuler (stroked) + Enregistrer (flat primary).

**DetailPage** : `gcc-page-header` → `gcc-identity-card` → `mat-tab-group` → `gcc-skill-gap` dans l’onglet compétences.

**Dashboard** : `gcc-page-header` → grille `gcc-kpi-card` → cartes graphiques. Pas de tableau métier.

**PageHeader** : titre centré sur l’icône **s’il n’y a pas** de sous-titre ; `items-start` s’il y en a un. Icônes = ligatures Material (`work`, `star`, `person`…), pas PrimeIcons.

**Select** : toujours `gcc-select`, jamais `<select>` natif.

**Maîtrise / statut** : uniquement `gcc-skill-badge` et `gcc-status-tag`.

## Interdits

- Couleurs hors tokens (`#0F172A`, `#F8FAFC`, `#FFFFFF`, `#6366F1`, `#7C3AED`, badges sémantiques).
- `h1` / breadcrumb / bouton primaire hors `gcc-page-header`.
- Alerte Bootstrap / toast custom pour liste vide → `gcc-empty-state`.
- Recoder un badge « Expert » en Tailwind au lieu de `gcc-skill-badge`.

## Checklist

- [ ] Un seul layout parmi les 3
- [ ] Une page template parmi les 7
- [ ] Header = `gcc-page-header`
- [ ] Select = `gcc-select`
- [ ] Niveaux / écarts = badges existants
- [ ] Police Inter (pas Roboto Material brut)
- [ ] Visuel aligné sur la galerie `design-system`

Détail des sélecteurs, fichiers et tokens : [reference.md](reference.md).
