---
name: breakpoint-display
description: >-
  Système unifié pour l'affichage de breakpoints interactifs avec validation
  utilisateur via AskUserQuestion. Centralise tous les formats de breakpoints
  EPCI pour cohérence, économie tokens (73% réduction), et maintenabilité.
  Use when: Afficher un breakpoint dans une commande (/brief, /epci, /decompose, etc.).
  Not for: Affichage simple sans interaction utilisateur (utiliser print direct).
applicable-to: ["ALL_COMMANDS_WITH_BREAKPOINTS"]
integration: ["AskUserQuestion", "breakpoint-metrics"]
---

# Breakpoint Display — Unified Interactive Breakpoints

## Overview

Skill centralisé pour afficher des breakpoints interactifs avec validation utilisateur native via `AskUserQuestion`. Remplace les choix textuels manuels par une UI native Claude Code.

**Bénéfices :**
- 📉 **73% réduction tokens** : ~300 tokens/breakpoint → ~80 tokens
- 🎨 **UX native** : Boutons cliquables vs input textuel
- 🔄 **Cohérence** : Format unifié pour 9 commandes
- 🛠️ **Maintenabilité** : 1 skill vs 9 implémentations
- ✨ **Évolutivité** : Nouveaux types facilement ajoutés

---

## MANDATORY EXECUTION — Instructions Impératives

**QUAND tu rencontres `@skill:breakpoint-display` dans une commande, tu DOIS exécuter ces 4 étapes :**

### Étape 1 : Parser les paramètres

Extraire : `type`, `title`, `data`, `ask` (optionnel).

### Étape 2 : AFFICHER le breakpoint ASCII

Tu DOIS afficher une boîte ASCII avec bordures `┌───┐` `└───┘` selon le type.

**Templates détaillés :** Voir @references/execution-templates.md

**Structure générale :**
```
┌─────────────────────────────────────────────────────────────────────┐
│ ⏸️  {title}                                                          │
├─────────────────────────────────────────────────────────────────────┤
│ [Contenu selon type - voir templates]                               │
└─────────────────────────────────────────────────────────────────────┘
```

**Types supportés :** validation, analysis, plan-review, decomposition, ems-status, diagnostic, interactive-plan, research-prompt, lightweight, info-only.

### Étape 3 : INVOQUER AskUserQuestion (si `ask` présent)

```typescript
AskUserQuestion({
  questions: [{
    question: ask.question,
    header: ask.header,       // Max 12 caractères
    multiSelect: ask.multiSelect || false,
    options: ask.options      // Array de {label, description}
  }]
})
```

**Types SANS AskUserQuestion :** `info-only`, `ems-status`, `lightweight`.

### Étape 4 : RETOURNER le choix

Retourner le choix utilisateur au workflow appelant.

---

## Supported Breakpoint Types

| Type | Usage | AskUserQuestion | Template |
|------|-------|-----------------|----------|
| **validation** | Choix simple (Valider/Modifier/Annuler) | ✅ Oui | @templates/validation.md |
| **plan-review** | Métriques + validations agents + preview | ✅ Oui | @templates/plan-review.md |
| **analysis** | Questions + suggestions + évaluation | ✅ Oui | @templates/analysis.md |
| **decomposition** | Table specs + menu modifications | ✅ Oui (2-level) | @templates/decomposition.md |
| **diagnostic** | Root cause + solutions ranked | ✅ Oui | @templates/diagnostic.md |
| **interactive-plan** | DAG + reorder + skip options | ✅ Oui | @templates/interactive-plan.md |
| **research-prompt** | Recherche Perplexity (human-in-the-loop) | ✅ Oui | @templates/research-prompt.md |
| **lightweight** | Auto-continue avec timeout 3s | ⚠️ Optionnel | @templates/lightweight.md |
| **info-only** | Display metrics sans interaction | ❌ Non | @templates/info-only.md |
| **ems-status** | EMS 5 axes + progression brainstorm | ❌ Non | @templates/ems-status.md |

## Usage Pattern

```typescript
// Pattern général dans une commande
@skill:breakpoint-display
  type: {TYPE}
  title: "{TITLE}"
  data: {
    // Type-specific data structure
  }
  ask: {
    question: "{QUESTION}"
    header: "{HEADER}"  // Max 12 chars
    multiSelect: {true|false}
    options: [
      {label: "{LABEL}", description: "{DESCRIPTION}"},
      ...
    ]
  }
```

## Examples by Type

### Type: validation

Simple 2-4 choix (Valider/Modifier/Annuler).

```typescript
@skill:breakpoint-display
  type: validation
  title: "VALIDATION DU BRIEF"
  data: {
    original_brief: "{text}",
    reformulated: {true|false},
    reformulated_brief: {
      objectif: "...",
      contexte: "...",
      contraintes: "...",
      success_criteria: "..."
    }
  }
  ask: {
    question: "Le brief vous convient-il ?"
    header: "📝 Validation"
    options: [
      {label: "Valider (Recommended)", description: "Continuer vers exploration"},
      {label: "Modifier", description: "Je reformule moi-même"},
      {label: "Annuler", description: "Arrêter workflow"}
    ]
  }
```

### Type: plan-review

Métriques + validations agents + preview prochaine phase.

```typescript
@skill:breakpoint-display
  type: plan-review
  title: "PHASE 1 — Plan Validé"
  data: {
    metrics: {
      complexity: "STANDARD",
      complexity_score: 6.2,
      files_impacted: 12,
      time_estimate: "2-3h",
      risk_level: "MEDIUM",
      risk_description: "Auth changes require careful testing"
    },
    validations: {
      plan_validator: {
        verdict: "APPROVED",
        completeness: "OK",
        consistency: "OK",
        feasibility: "OK",
        quality: "OK"
      }
    },
    skills_loaded: ["testing-strategy", "php-symfony", "security-patterns"],
    preview_phase_2: {
      tasks: [
        {title: "Create User entity", time: "30min"},
        {title: "Implement auth service", time: "1h"},
        {title: "Add tests", time: "45min"}
      ],
      remaining_tasks: 5
    },
    feature_doc_path: "docs/features/auth-oauth.md"
  }
  ask: {
    question: "Comment souhaitez-vous procéder ?"
    header: "🚀 Phase 2"
    options: [
      {label: "Continuer (Recommended)", description: "Passer à Phase 2 Implémentation"},
      {label: "Modifier plan", description: "Réviser plan avant implémentation"},
      {label: "Voir détails", description: "Afficher Feature Document complet"},
      {label: "Annuler", description: "Abandonner workflow"}
    ]
  }
```

### Type: analysis

Questions clarification + suggestions + évaluation + personas + MCP.

```typescript
@skill:breakpoint-display
  type: analysis
  title: "ANALYSE DU BRIEF"
  data: {
    exploration: {
      stack: "Symfony 6.3 + PostgreSQL",
      files_impacted: 8,
      patterns: ["Repository", "Service", "Controller"],
      risks: ["Migration données", "Breaking changes API"]
    },
    questions: [
      {tag: "🛑", text: "Quel provider OAuth ? (Google/GitHub/Custom)", suggestion: "Google OAuth 2.0"},
      {tag: "⚠️", text: "Migrer users existants ?", suggestion: "Migration progressive avec fallback"},
      {tag: "ℹ️", text: "UI personnalisée ?", suggestion: "Utiliser OAuth redirects standards"}
    ],
    suggestions: {
      architecture: "Utiliser FOSUserBundle + HWIOAuthBundle",
      implementation: "Créer UserProvider custom pour mapping OAuth",
      risks: "Tester rollback en cas d'échec OAuth",
      stack_specific: "Configurer security.yaml avec firewall OAuth"
    },
    personas: {
      active: [
        {name: "backend", score: 0.72, source: "auto"},
        {name: "security", score: 0.65, source: "auto"}
      ],
      suggested: [
        {name: "qa", score: 0.48}
      ]
    },
    mcp_servers: {
      active: [
        {server: "c7", source: "backend"},
        {server: "seq", source: "security"}
      ],
      available: ["magic", "play"]
    },
    evaluation: {
      category: "STANDARD",
      files: 8,
      loc_estimate: 450,
      risk: "MEDIUM",
      flags: ["--think", "--uc", "--persona-backend", "--persona-security", "--c7", "--seq"]
    },
    recommended_command: "/epci --think --uc --c7 --seq"
  }
  ask: {
    question: "Comment souhaitez-vous procéder avec cette analyse ?"
    header: "🚀 Action"
    options: [
      {label: "Répondre questions", description: "Je fournis réponses clarification"},
      {label: "Valider suggestions (Recommended)", description: "J'accepte suggestions IA telles quelles"},
      {label: "Modifier suggestions", description: "Je veux changer certaines suggestions"},
      {label: "Lancer /epci", description: "Tout OK, passer implémentation"}
    ]
  }
```

### Type: decomposition

Table specs + menu modifications multi-niveau.

```typescript
@skill:breakpoint-display
  type: decomposition
  title: "VALIDATION DÉCOUPAGE"
  data: {
    source_file: "prd-migration.md",
    analysis: {
      lines: 450,
      total_effort: 23,
      structure: "5 phases, 12 steps"
    },
    specs: [
      {id: "S01", title: "Auth Base", effort: 3, priority: "-", deps: "-", status: "Pending"},
      {id: "S02", title: "OAuth Integration", effort: 5, priority: "-", deps: "S01", status: "Pending"},
      {id: "S03", title: "User Migration", effort: 2, priority: "-", deps: "S01", status: "Pending"}
    ],
    parallelization: 2,
    optimized_duration: 15,
    sequential_duration: 23,
    alerts: ["S02 effort élevé - considérer split"],
    validator_verdict: "APPROVED with minor suggestions"
  }
  ask: {
    question: "Le découpage vous convient-il ?"
    header: "📋 Découpage"
    options: [
      {label: "Valider (Recommended)", description: "Générer fichiers sous-specs"},
      {label: "Modifier", description: "Ajuster découpage avant génération"},
      {label: "Annuler", description: "Abandonner décomposition"}
    ]
  }
```

**Si choix "Modifier", afficher sous-menu :**

```typescript
@skill:breakpoint-display (second-level)
  type: decomposition-modify
  title: "MODIFICATION DÉCOUPAGE"
  ask: {
    question: "Que souhaitez-vous modifier ?"
    header: "🔧 Modifier"
    multiSelect: true
    options: [
      {label: "Fusionner specs", description: "Ex: Fusionner S04 et S05"},
      {label: "Découper spec", description: "Ex: Découper S07 en 2 parties"},
      {label: "Renommer", description: "Ex: S03 → Modèles Fondamentaux"},
      {label: "Changer dépendances", description: "Ex: S06 ne dépend plus de S03"},
      {label: "Ajuster estimation", description: "Ex: S08 = 3 jours au lieu de 5"}
    ]
  }
```

### Type: ems-status

Status brainstorm avec EMS 5 axes et progression (display-only).

```typescript
@skill:breakpoint-display
  type: ems-status
  title: "BRAINSTORM STATUS"
  data: {
    phase: "DIVERGENT",
    persona: "Architecte",
    iteration: 3,
    ems: {
      score: 65,
      delta: "+12",
      axes: {
        clarity: 80,
        depth: 60,
        coverage: 45,
        decisions: 75,
        actionability: 70
      },
      weak_axes: ["coverage"],
      progression: ["Init(22)", "Iter1(38)", "Iter2(53)", "Current(65)"]
    },
    done: ["Cible identifiée", "Contraintes listées"],
    open: ["Délais à préciser", "Intégrations externes"],
    commands: ["continue", "dive", "back", "save", "energy", "finish"]
  }
  // No 'ask' - display only with command hints
```

## Reusable Components

Le skill utilise des composants réutilisables pour cohérence :

| Component | File | Usage |
|-----------|------|-------|
| **Metrics Block** | @components/metrics-block.md | Complexité, fichiers, temps, risque |
| **Validations Block** | @components/validations-block.md | Verdicts agents (@plan-validator, etc.) |
| **Preview Block** | @components/preview-block.md | Preview tâches prochaine phase |
| **Flags Block** | @components/flags-block.md | Flags actifs avec sources (auto/user) |
| **Suggestions Block** | @components/suggestions-block.md | Suggestions proactives (Discovery Mode) |

## Suggestions Field (v5.3.7)

Champ optionnel `suggestions[]` pour afficher des suggestions proactives dans les breakpoints.
Activé via flag `--suggest` dans `/brainstorm` (Discovery Mode).

### Structure

```yaml
data:
  # ... existing fields ...
  suggestions:
    - pattern: "{pattern_id}"
      text: "{suggestion_text}"
      priority: "P1|P2|P3"
      action: "{command_or_null}"  # Optional
```

### Supported Types

| Type | Suggestions Support | Usage |
|------|---------------------|-------|
| `ems-status` | ✅ Oui | Suggestions EMS-aware en brainstorm |
| `plan-review` | ✅ Oui | Suggestions convergence/transition |
| `analysis` | ✅ Oui | Suggestions architecture/security |
| `validation` | ❌ Non | Simple validation, pas de suggestions |
| `decomposition` | ⚠️ Optionnel | Suggestions scope si LARGE |
| `diagnostic` | ⚠️ Optionnel | Suggestions debugging patterns |
| `lightweight` | ❌ Non | Auto-continue, pas de temps |
| `info-only` | ❌ Non | Display only |

### Display Format

**Quand `suggestions[]` présent et non-vide:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 💡 SUGGESTIONS PROACTIVES                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔴 [P1] Patterns auth détectés — considérez @security-auditor preview       │
│        → security-check                                                     │
│ 🟡 [P2] Coverage à 35% — essayez Six Hats pour perspectives stakeholders   │
│        → technique six-hats                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Priority Icons:**

| Priority | Icon | Color |
|----------|------|-------|
| P1 | 🔴 | Critical |
| P2 | 🟡 | Important |
| P3 | 🟢 | Nice-to-have |

### Example: ems-status with suggestions

```typescript
@skill:breakpoint-display
  type: ems-status
  title: "BRAINSTORM STATUS"
  data:
    phase: "DIVERGENT"
    persona: "Architecte"
    iteration: 3
    ems:
      score: 65
      delta: "+12"
      axes: {clarity: 80, depth: 60, coverage: 35, decisions: 75, actionability: 70}
      weak_axes: ["coverage"]
      progression: ["Init(22)", "Iter1(38)", "Iter2(53)", "Current(65)"]
    done: ["Cible identifiée", "Contraintes listées"]
    open: ["Délais à préciser"]
    commands: ["continue", "dive", "back", "save", "finish"]
    # NEW: Suggestions field
    suggestions:
      - pattern: "coverage-low"
        text: "Coverage à 35% — essayez Six Hats pour perspectives stakeholders"
        priority: P2
        action: "technique six-hats"
      - pattern: "security-early"
        text: "Patterns auth détectés — considérez @security-auditor preview"
        priority: P1
        action: "security-check"
```

### Conditional Display

```
IF suggestions[] is present AND non-empty AND --suggest flag active:
   Display suggestions block BEFORE ask section
   Sort by priority (P1 first, then P2, then P3)
   Max 3 suggestions displayed

ELSE:
   Skip suggestions block (backward compatible)
```

### Integration with proactive-suggestions skill

See @src/skills/core/proactive-suggestions/SKILL.md section "Discovery Mode" for:
- Pattern catalog
- Priority levels
- Learning integration

## AskUserQuestion Integration

### Headers (max 12 characters)

Pattern utilisé dans `/brainstorm` (référence) :

```typescript
"📝 Validation"  // 12 chars
"🚀 Action"      // 8 chars
"🚀 Phase 2"     // 10 chars
"📋 Découpage"   // 12 chars
"🔧 Modifier"    // 10 chars
"💡 Diagnostic"  // 13 chars → "💡 Solution" (11 chars)
"🔄 Transition"  // 12 chars
```

### Options with (Recommended)

```typescript
{
  label: "Valider (Recommended)",
  description: "Continuer vers exploration"
}
```

Convention : Le premier choix est `(Recommended)` si c'est le chemin par défaut.

### MultiSelect Mode

```typescript
multiSelect: true,
options: [
  {label: "Option 1", description: "..."},
  {label: "Option 2", description: "..."}
]
```

Utilisé pour sélections multiples simultanées (ex: techniques brainstorm, modifications décomposition).

## Display Logic

### Step 1: Render Data Section

Utiliser le composant approprié selon le type :

- **validation** : Brief original + reformulé (si applicable)
- **plan-review** : @components/metrics-block + @components/validations-block + @components/preview-block
- **analysis** : Exploration + Questions + Suggestions + Évaluation
- **decomposition** : Table specs + Parallelization + Alerts
- **diagnostic** : Root cause + Solutions ranked
- **interactive-plan** : DAG Mermaid + Specs table
- **lightweight** : Minimal info + "Auto-continue dans 3s..."
- **info-only** : Metrics seulement

### Step 2: Call AskUserQuestion

Si le type a `ask` défini (tous sauf `info-only` et `lightweight`), invoquer `AskUserQuestion` :

```typescript
AskUserQuestion({
  questions: [{
    question: data.ask.question,
    header: data.ask.header,
    multiSelect: data.ask.multiSelect || false,
    options: data.ask.options.map(opt => ({
      label: opt.label,
      description: opt.description
    }))
  }]
})
```

### Step 3: Handle Response

Retourner la réponse au workflow appelant pour traitement.

## Token Savings

| Type | Avant (ASCII box) | Après (skill) | Gain |
|------|-------------------|---------------|------|
| validation | ~250 tokens | ~70 tokens | 72% |
| plan-review | ~350 tokens | ~90 tokens | 74% |
| analysis | ~450 tokens | ~120 tokens | 73% |
| decomposition | ~300 tokens | ~85 tokens | 72% |
| diagnostic | ~280 tokens | ~75 tokens | 73% |
| interactive-plan | ~320 tokens | ~95 tokens | 70% |
| lightweight | ~100 tokens | ~40 tokens | 60% |
| info-only | ~150 tokens | ~60 tokens | 60% |
| ems-status | ~150 tokens | ~65 tokens | 57% |

**Moyenne : 71% réduction tokens**

## Migration Guide

Voir @references/migration-guide.md pour guide détaillé commande par commande.

**Ordre recommandé :**
1. `/brief` (2 breakpoints : validation + analysis)
2. `/epci` (2 breakpoints : plan-review × 2)
3. `/decompose` (1 breakpoint : decomposition)
4. `/commit` (1 breakpoint : validation)
5. `/debug` (1 breakpoint : diagnostic)
6. `/orchestrate` (1 breakpoint : interactive-plan)
7. `/save-plan` (1 breakpoint : validation)
8. `/quick` (1 breakpoint : lightweight)
9. `/ralph-exec` (1 breakpoint : info-only)

## Error Handling

| Erreur | Action |
|--------|--------|
| Type inconnu | Afficher erreur + liste types supportés |
| Données manquantes | Afficher warning + utiliser defaults |
| AskUserQuestion échoue | Fallback vers input textuel legacy |
| Header > 12 chars | Tronquer avec warning |

## Technical Notes

- **Encoding:** UTF-8 pour emojis et caractères spéciaux
- **Line width:** Max 73 chars pour ASCII boxes (compatibilité terminal)
- **Emojis:** Utiliser codes unicode standards
- **Versioning:** v1.0.0 (aligns with EPCI v5.3.8)

## References

- AskUserQuestion Guide: @references/askuserquestion-guide.md
- Migration Guide: @references/migration-guide.md
- Brainstorm Implementation: @src/commands/brainstorm.md (reference model)
- Component Templates: @components/
- Type Templates: @templates/

## Examples in Production

After migration, commands will use:

```bash
# /brief Step 4
@skill:breakpoint-display type:analysis ...

# /epci Phase 1
@skill:breakpoint-display type:plan-review title:"PHASE 1 — Plan Validé" ...

# /decompose
@skill:breakpoint-display type:decomposition ...
```

**See individual command files for full usage examples after migration.**
