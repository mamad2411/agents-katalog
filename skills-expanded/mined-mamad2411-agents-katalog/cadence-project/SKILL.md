---
name: cadence-project
description: >
  Guide de développement de « Cadence », une application web de gestion de projets agiles
  (sprints, tableau Kanban) intégrant la planification de la capacité de l'équipe à partir
  de ses disponibilités (congés, jours travaillés). Projet de stage réalisé chez Devox (Témara).
  Stack : React (web), Node.js + Express + MongoDB/Mongoose (API). Utilise impérativement ce
  skill dès qu'on travaille sur Cadence : créer ou modifier le back-end ou le front, ajouter
  un endpoint, un modèle Mongoose, un composant React, implémenter le calcul de capacité d'un
  sprint, appliquer les conventions ou les tokens de design. Déclenche-le aussi quand l'utilisateur
  mentionne simplement Cadence, les sprints, le tableau Kanban, la barre de capacité, les congés /
  disponibilités, ou demande de continuer à construire l'application, même sans dire « skill ».
---

# Cadence — guide de projet

## Vue d'ensemble

Cadence est un outil interne pour une société de développement (Devox). Il sert deux besoins
réunis en un seul produit :

1. **Gestion de projets agiles** : projets, sprints, tâches, tableau Kanban (À faire, En cours, En revue, Terminé).
2. **Disponibilité de l'équipe** : congés et absences, jours travaillés, calendrier d'équipe.

**Ce qui rend Cadence unique** : la planification d'un sprint tient compte de la **capacité
réellement disponible**. Les congés validés des membres réduisent la capacité du sprint, qui est
ensuite comparée à la charge des tâches planifiées, avec une **alerte de surcharge**. C'est la
fonctionnalité centrale : ne jamais l'affaiblir ou la traiter comme secondaire.

Il n'y a **aucune logique d'argent** dans Cadence (pas de salaire, pas de facturation). Si une
demande introduit une notion financière, la signaler comme hors périmètre.

## Stack technique

- **Front web** : React + Vite, React Router, une librairie de glisser-déposer (dnd-kit ou
  @hello-pangea/dnd), Recharts pour les graphiques, axios pour l'API.
- **Back-end** : Node.js + Express, API REST.
- **Base de données** : MongoDB avec Mongoose.
- **Auth** : JWT + bcrypt.
- **Temps réel (optionnel)** : Socket.io pour la synchronisation du tableau Kanban.
- **Mobile (optionnel, plus tard)** : React Native + Expo, consommant la même API.
- **Hébergement gratuit** : Vercel (front), Render (back), MongoDB Atlas (base).

Garde une **unité cohérente** entre l'estimation des tâches (`estimate`) et la capacité
(`dailyCapacityHours`) : utiliser les **heures** pour le MVP.

## Structure du dépôt

Back-end :
```
backend/
├── config/        # connexion MongoDB, variables d'env
├── models/        # un fichier par modèle Mongoose (voir references/data-model.md)
├── controllers/   # logique des routes
├── routes/        # définition des routes Express
├── middlewares/   # auth JWT, contrôle de rôle, gestion d'erreurs, validation
├── services/      # logique métier (calcul de capacité)
├── seed/          # données de test
└── server.js
```

Front web :
```
frontend/
├── src/
│   ├── api/         # client axios, intercepteur JWT
│   ├── components/  # composants réutilisables (TaskCard, StatusBadge, Avatar, CapacityBar…)
│   ├── pages/       # écrans (Board, Backlog, Calendar, Leaves, Dashboard, Login)
│   ├── hooks/
│   ├── theme/       # tokens de design (voir references/design.md)
│   └── App.jsx
└── index.html
```

## Conventions de code

- API REST : noms de ressources au pluriel (`/projects`, `/sprints`, `/tasks`, `/leaves`).
- Toute route protégée passe par un middleware `auth` (vérifie le JWT) puis, si besoin, `requireRole('manager','admin')`.
- Valider et assainir les entrées (express-validator ou équivalent) ; ne jamais faire confiance au corps de la requête.
- Centraliser la gestion des erreurs dans un middleware unique renvoyant `{ message }` et un code HTTP cohérent.
- Ne jamais renvoyer `passwordHash` (le champ est `select: false`).
- Côté React, garder les composants réutilisables sans logique d'API ; centraliser les appels dans `src/api/`.
- Respecter les tokens de design de `references/design.md` (accent cobalt, neutres froids, Inter). Pas de dégradé violet, pas de glassmorphism, pas d'ombre exagérée.

## Rôles et permissions

- **developer** : voit et met à jour ses tâches assignées ou celles de ses projets ; déclare ses congés.
- **manager** : gère projets, sprints et backlog ; planifie selon la capacité ; valide les congés ; consulte le tableau de bord.
- **admin** : gère les comptes, les paramètres de capacité (jours travaillés, capacité quotidienne) et le calendrier.

## Cycle de vie d'un sprint

`planned → active → completed`. Un seul sprint **actif** par projet à la fois. Seuls manager/admin
démarrent ou clôturent un sprint. Une tâche dont `sprint` vaut `null` est dans le **backlog**.

## Pour aller plus loin (fichiers de référence)

Lire le fichier pertinent selon la tâche :

- **Modèle de données** (collections, champs, choix d'imbrication, index) → `references/data-model.md`
- **API et logique de capacité** (endpoints, algorithme de capacité détaillé, règles métier) → `references/api.md`
- **Design du front** (palette, typographie, composants, statuts) → `references/design.md`

## Comment ajouter une fonctionnalité (workflow)

1. Identifier la ou les collections concernées (`references/data-model.md`).
2. Côté back-end : modèle (si besoin) → controller → route → middleware d'autorisation → validation.
3. Mettre à jour le `seed/` si la fonctionnalité a besoin de données de test.
4. Côté front : appel API dans `src/api/`, puis composant/écran en respectant les tokens de design.
5. Vérifier les permissions par rôle et le cas du backlog vs sprint.

## Définition de « terminé »

Une fonctionnalité est terminée quand : les routes sont protégées par rôle, les entrées sont
validées, le cas d'erreur renvoie un message clair, le front consomme l'API réelle (pas de données
en dur), et le comportement respecte les règles métier (notamment le calcul de capacité et le cycle
de vie du sprint).
