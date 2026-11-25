---
name: clarification-intelligente
description: >-
  Système de clarification contextuelle intelligent pour EPCI.
  Use when: /epci-brief needs to generate clarification questions,
  analyzing briefs for domain detection, or finding similar features.
  Not for: direct implementation tasks, code generation, or when brief is already complete.
allowed-tools: [Read]
---

# Clarification Intelligente

## Overview

Ce skill fournit le système de clarification intelligente pour la phase de brief EPCI.
Il transforme les questions génériques en questions contextuelles basées sur:

- L'historique des features (Project Memory F04)
- Les patterns détectés dans le projet
- Le domaine technique identifié
- La persona active (F09, quand disponible)

## Components

### 1. Clarification Analyzer

**Module**: `src/project-memory/clarification_analyzer.py`

Analyse le brief pour extraire:
- **Keywords**: Mots-clés significatifs
- **Domain**: Domaine technique (auth, api, ui, data, etc.)
- **Gaps**: Informations manquantes

```python
from project_memory.clarification_analyzer import analyze_brief

analysis = analyze_brief("Ajouter un système de notifications")
# analysis.keywords = ['notifications', 'système']
# analysis.domain = DomainInfo(name='notification', confidence=0.8)
# analysis.gaps = [GapInfo(category='channels', ...)]
```

### 2. Similarity Matcher

**Module**: `src/project-memory/similarity_matcher.py`

Trouve les features similaires par similarité Jaccard:

```python
from project_memory.similarity_matcher import find_similar_features

matches = find_similar_features(features, keywords, threshold=0.3)
# matches = [SimilarFeature(slug='user-alerts', score=0.75, ...)]
```

### 3. Question Generator

**Module**: `src/project-memory/question_generator.py`

Génère max 3 questions intelligentes:

```python
from project_memory.question_generator import generate_clarification

result = generate_clarification(brief, manager, persona='backend')
# result.questions = [Question(type=REUSE, text="..."), ...]
```

## Question Types

| Type | Déclencheur | Exemple |
|------|-------------|---------|
| **REUSE** | Feature similaire trouvée | "La feature X utilise le pattern Y. Réutiliser ?" |
| **TECHNICAL** | Lacune technique détectée | "Quelle méthode d'authentification ?" |
| **SCOPE** | Périmètre flou | "Quel est le périmètre exact ?" |
| **INTEGRATION** | Composants existants | "Intégration avec Messenger existant ?" |
| **PRIORITY** | Persona-specific | "Quelle garantie de fiabilité requise ?" |

## Rules

1. **Maximum 3 questions** par itération
2. **Maximum 3 itérations** de clarification
3. **Pas de redondance** - ne pas reposer une question déjà répondue
4. **Priorisation** - questions bloquantes d'abord
5. **Suggestions** - proposer des réponses par défaut basées sur l'historique

## Integration with epci-brief

Le système est intégré dans Step 2 de `/epci-brief`:

```markdown
### Step 2: Clarification Loop

If Project Memory available:
1. Analyze brief → extract keywords, detect domain
2. Find similar features → suggest reuse
3. Identify gaps → generate targeted questions
4. Adapt to persona → customize question focus
5. Present max 3 questions with suggestions

If Project Memory unavailable:
→ Graceful degradation to generic questions
```

## Graceful Degradation

Si Project Memory est indisponible ou corrompu:
- Le système retourne des questions génériques
- Aucune erreur n'est propagée
- Le workflow continue normalement

## Future Enhancements (F09)

Quand le système de Personas sera implémenté:
- Questions adaptées au focus de la persona
- Priorisation différente selon le rôle
- Suggestions contextualisées

## Testing

```bash
# Test analyzer
python src/project-memory/clarification_analyzer.py "Add OAuth authentication"

# Test matcher
python src/project-memory/similarity_matcher.py "notification email user"

# Test generator
python src/project-memory/question_generator.py "Ajouter un système de notifications"
```
