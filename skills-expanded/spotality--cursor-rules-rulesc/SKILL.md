---
description: 
globs: 
alwaysApply: false
---
```markdown name=.cursorrules
# Cursor Rules - Spotify Music Personality Analyzer

## 📋 Règles Fondamentales

### 1. Lecture Obligatoire des Fichiers de Contexte
- **TOUJOURS** lire `objectif.md` avant de commencer une nouvelle fonctionnalité
- **TOUJOURS** consulter `avancement.md` pour comprendre l'état actuel du projet
- **METTRE À JOUR** `avancement.md` après chaque tâche complétée

### 2. Analyse du Code Existant
- **AVANT** d'écrire du code, explorer la structure existante du projet
- **IDENTIFIER** les patterns et conventions déjà établis
- **RÉUTILISER** les composants, services et utilitaires existants
- **NE PAS** dupliquer du code existant sans raison valable

### 3. Cohérence Architecturale
- **RESPECTER** l'architecture Clean Architecture + BLoC définie
- **SUIVRE** la structure de dossiers établie
- **MAINTENIR** la séparation des responsabilités (data/domain/presentation)
- **UTILISER** les mêmes patterns de nommage dans tout le projet

### 4. 🧩 STRUCTURATION DES VUES ET COMPOSANTS (NOUVEAU)
- **LIMITE DE TAILLE** : Aucun fichier de page ne doit dépasser 300 lignes
- **DÉCOUPAGE OBLIGATOIRE** : Si une page dépasse 300 lignes, découper en widgets séparés
- **EXPLORATION PRÉALABLE** : Avant de créer un nouveau composant, vérifier l'existant dans :
  - `/shared/widgets/` pour les composants réutilisables
  - `/features/[feature]/presentation/widgets/` pour les composants spécifiques
- **RÉUTILISATION MAXIMALE** : Identifier et réutiliser les patterns UI existants
- **COMPOSANTS ATOMIQUES** : Créer des widgets spécialisés (ex: `StatusCard`, `SectionHeader`, `ApiTestButton`)
- **NAMING COHÉRENT** : Nommer les composants selon leur fonction (`build[SectionName]Section()` → `[SectionName]Section()`)
- **SÉPARATION PAR RESPONSABILITÉ** :
  - **Pages** : Coordination et navigation uniquement
  - **Sections** : Groupes logiques d'UI (ex: `RecentlyPlayedSection`)
  - **Items** : Composants atomiques (ex: `TrackListItem`, `ArtistListItem`)
- **DOCUMENTATION OBLIGATOIRE** : Commenter le rôle de chaque composant extrait

#### Règles de Refactorisation :
1. **IDENTIFIER** les sections répétitives (Container + padding + decoration)
2. **EXTRAIRE** en widgets séparés avec paramètres configurables
3. **CENTRALISER** les styles communs (couleurs, bordures, padding)
4. **TESTER** chaque composant extrait individuellement
5. **VALIDER** que la fonctionnalité reste identique après refactorisation

#### Structure Recommandée pour les Pages Complexes :
```
lib/features/[feature]/presentation/
├── pages/
│   └── [feature]_page.dart (max 300 lignes)
├── widgets/
│   ├── sections/
│   │   ├── welcome_section.dart
│   │   ├── status_section.dart
│   │   └── recently_played_section.dart
│   └── items/
│       ├── status_card.dart
│       └── api_test_button.dart
```

### 5. 🚶‍♂️ DÉVELOPPEMENT PAR PETITES ÉTAPES (CRUCIAL)
- **JAMAIS** implémenter une fonctionnalité complète d'un coup
- **DIVISER** chaque tâche en micro-étapes de 10-20 lignes de code maximum
- **TESTER** chaque micro-étape avant de passer à la suivante
- **VALIDER** avec l'utilisateur (Kevinmrgt) avant de continuer vers l'étape suivante
- **PROPOSER** toujours la prochaine micro-étape plutôt que de continuer automatiquement

## 🏗️ Structure et Organisation

### Conventions de Nommage
```
- Fichiers: snake_case (ex: spotify_service.dart)
- Classes: PascalCase (ex: SpotifyRepository)
- Variables/Méthodes: camelCase (ex: getUserTopTracks)
- Constantes: SCREAMING_SNAKE_CASE (ex: API_BASE_URL)
- Dossiers: snake_case (ex: spotify_data)
```

### Hiérarchie des Dossiers
```
lib/
├── core/ (utilitaires globaux, constants, erreurs)
├── features/ (fonctionnalités par domaine métier)
│   └── [feature_name]/
│       ├── data/ (models, datasources, repositories impl)
│       ├── domain/ (entities, repositories abstract, usecases)
│       └── presentation/ (bloc, pages, widgets)
└── shared/ (widgets réutilisables, thème, localisation)
```

## 🔄 Méthodologie par Micro-Étapes

### Principe de Base
**RÈGLE D'OR** : Une seule micro-tâche à la fois, validation utilisateur obligatoire avant de continuer.

### Exemples de Micro-Étapes Acceptables :
✅ **BIEN** : "Créer uniquement la classe SpotifyTrack entity"
✅ **BIEN** : "Ajouter seulement la méthode de connexion OAuth"
✅ **BIEN** : "Créer le widget de base pour afficher un track"
❌ **MAL** : "Implémenter tout le système d'authentification Spotify"
❌ **MAL** : "Créer la page complète d'analyse de personnalité"

### Format de Livraison Obligatoire
Après chaque micro-étape :
```markdown
## ✅ Micro-étape Complétée : [Description courte]

**Fichiers modifiés/créés :**
- `chemin/vers/fichier.dart`

**Ce qui a été fait :**
- Action précise réalisée

**Tests possibles :**
- Comment tester cette micro-étape

**Prochaine micro-étape proposée :**
- Prochaine action spécifique à faire

**Question pour Kevinmrgt :**
Dois-je continuer avec la prochaine micro-étape ou veux-tu vérifier/modifier quelque chose ?
```

## 📝 Règles de Développement

### Avant Chaque Micro-Étape
1. **LIRE** `objectif.md` pour comprendre le contexte
2. **CONSULTER** `avancement.md` pour voir l'état actuel
3. **VÉRIFIER** la documentation Spotify officielle si fonctionnalité API concernée
4. **EXPLORER** le code existant dans le domaine concerné
5. **IDENTIFIER** les composants réutilisables
6. **PROPOSER** une micro-étape spécifique de maximum 20 lignes

### Pendant le Développement
- **SE LIMITER** strictement à la micro-étape définie
- **RÉUTILISER** les widgets existants dans `/shared/widgets/`
- **ÉTENDRE** les classes abstraites plutôt que de créer des doublons
- **SUIVRE** les patterns BLoC établis (events, states, blocs)
- **UTILISER** les services de base existants (DioClient, etc.)
- **RESPECTER** les conventions de nommage du projet

### Gestion des Erreurs
- **UTILISER** les classes d'erreur définies dans `/core/errors/`
- **SUIVRE** le pattern Either<Failure, Success> pour les repositories
- **CRÉER** des messages d'erreur cohérents et localisés

### Tests
- **CRÉER** des tests unitaires pour chaque nouveau usecase
- **MOCKER** les dépendances externes (API, base de données)
- **TESTER** les widgets avec des données de test cohérentes

## 🔄 Mise à Jour de l'Avancement

### Format Requis pour avancement.md
```markdown
## [2025-06-10 15:43:46] - [Micro-étape/Tâche]
- **Status**: ✅ TERMINÉ / 🔄 EN COURS / ⏳ TODO / ❌ BLOQUÉ
- **Fichiers modifiés**: liste des fichiers
- **Micro-fonctionnalité**: description précise
- **Tests ajoutés**: oui/non
- **Notes**: remarques importantes
- **Prochaine micro-étape**: action spécifique suivante
- **Validation Kevinmrgt**: ⏳ EN ATTENTE / ✅ APPROUVÉ
```

### Quand Mettre à Jour
- **APRÈS CHAQUE** micro-étape complétée
- **AVANT** de proposer la suivante
- Avec horodatage précis (format: 2025-06-10 15:43:46)

## 🎯 Spécificités du Projet

### API Spotify
- **RÉUTILISER** les modèles existants dans `/features/spotify_data/data/models/`
- **ÉTENDRE** le SpotifyService existant plutôt que créer de nouveaux services
- **GÉRER** les rate limits de l'API Spotify
- **CACHER** les réponses API avec Hive quand approprié

### 🚨 URI DE REDIRECTION SPOTIFY - RÈGLE ABSOLUE
- **JAMAIS** changer l'URI de redirection : `http://127.0.0.1:8000/callback`
- **TOUJOURS** utiliser `SpotifyConstants.redirectUri` dans le code
- **INTERDICTION FORMELLE** de modifier cette URI sous quelque prétexte que ce soit
- Cette URI est définie selon la documentation officielle Spotify et ne doit JAMAIS être changée

### Analyse de Personnalité
- **CENTRALISER** les algorithmes dans `/features/personality_analysis/domain/`
- **SÉPARER** les calculs des traits de personnalité en usecases distincts
- **DOCUMENTER** les formules utilisées dans les commentaires

### Interface Utilisateur
- **RÉUTILISER** les composants du design system dans `/shared/widgets/`
- **MAINTENIR** la cohérence visuelle avec le thème Spotify
- **OPTIMISER** les performances (lazy loading, pagination)
- **GÉRER** les états de chargement avec les widgets existants

## ⚠️ Interdictions Strictes

### Ne JAMAIS faire :
- ❌ Implémenter plusieurs fonctionnalités à la fois
- ❌ Continuer sans validation de Kevinmrgt
- ❌ Dupliquer du code sans vérifier l'existant
- ❌ Créer de nouveaux patterns sans raison architecturale
- ❌ Ignorer les conventions de nommage établies
- ❌ Oublier de mettre à jour `avancement.md`
- ❌ Créer des widgets dans `/features/` s'ils peuvent être génériques
- ❌ Hardcoder des valeurs qui devraient être dans `/core/constants/`
- ❌ **INTERDICTION ABSOLUE : Changer l'URI `http://127.0.0.1:8000/callback`**
- ❌ **Implémenter une fonctionnalité Spotify API sans consulter la documentation officielle**

### 🛑 STOP Obligatoire Après Chaque Micro-Étape
**TOUJOURS** s'arrêter et demander validation avant de continuer.

## 🎯 Template de Communication

À chaque fin de micro-étape, utiliser ce template :

```
## ✅ Micro-étape terminée

**Fait :** [description précise]
**Fichier(s) :** [liste]
**Temps estimé :** [X minutes]

**Prochaine micro-étape proposée :** [action spécifique]

Kevinmrgt, peux-tu valider avant que je continue ?
```

## 📚 Ressources de Référence

### Fichiers Clés à Consulter Régulièrement
- `objectif.md` - Vision globale du projet
- `avancement.md` - État actuel et prochaines étapes
- `lib/core/constants/` - Constantes du projet
- `lib/shared/` - Composants réutilisables
- `pubspec.yaml` - Dépendances disponibles

### 📖 Documentation Spotify Officielle - LECTURE OBLIGATOIRE
- **TOUJOURS** consulter la documentation officielle Spotify : https://developer.spotify.com/documentation
- **RÉFÉRENCER** les endpoints exacts de l'API Web Spotify avant implémentation
- **VÉRIFIER** les scopes requis pour chaque fonctionnalité dans la documentation
- **RESPECTER** les limites de taux (rate limits) documentées
- **SUIVRE** les conventions de nommage des paramètres selon la doc officielle
- **CONSULTER** les tutoriels d'autorisation pour OAuth 2.0 et PKCE
- **UTILISER** les exemples de réponses JSON pour modéliser les entités
- **RESPECTER** les codes d'erreur HTTP documentés
- **VÉRIFIER** les dépendances entre endpoints (ex: authorization avant API calls)

#### Sections Clés de la Documentation à Consulter Systématiquement :
- **Getting Started** - Configuration d'app et credentials
- **Authorization** - OAuth 2.0, scopes, tokens
- **API Reference** - Endpoints détaillés par catégorie :
  - Users (profil, top items)
  - Tracks (audio features, audio analysis, recommendations)
  - Artists (info, albums, related artists)
  - Playlists (création, modification, items)
  - Player (contrôle playback, queue, devices)
  - Search (recherche multi-type)
- **Rate Limits** - Quotas et gestion des limitations
- **Error Handling** - Codes d'erreur et gestion appropriée

#### Avant d'Implémenter une Nouvelle Fonctionnalité Spotify :
1. **LIRE** la section correspondante dans la doc officielle
2. **IDENTIFIER** les scopes OAuth requis
3. **NOTER** les paramètres obligatoires vs optionnels
4. **COMPRENDRE** le format de réponse attendu
5. **VÉRIFIER** les limitations de taux pour cet endpoint
6. **CONSULTER** les exemples d'usage fournis

### Architecture de Référence
- Clean Architecture principles
- BLoC pattern avec flutter_bloc
- Dependency Injection avec get_it
- Repository pattern pour l'accès aux données

## 🔍 Checklist Avant Chaque Micro-Commit

- [ ] Code exploré et compris la structure existante
- [ ] Pas de duplication de code
- [ ] Conventions de nommage respectées
- [ ] Architecture Clean respectée
- [ ] Micro-étape limitée à 20 lignes maximum
- [ ] `avancement.md` mis à jour avec horodatage
- [ ] Prochaine micro-étape proposée
- [ ] Validation Kevinmrgt demandée

---
**Rappel CRUCIAL** : Ce projet privilégie la progression par micro-étapes validées plutôt que le développement en bloc. Kevinmrgt doit valider chaque étape avant de continuer.
```