---
name: input-clarifier
description: >-
  Conditional input clarification for voice-dictated text. Detects confusion
  artifacts (hesitations, fillers, self-corrections) and proposes reformulation
  only when needed (clarity score < 0.6). Ultra-fast, non-blocking for clear inputs.
  Use when: Any command receives free-form user input (brief, brainstorm, debug, promptor).
  Not for: Structured inputs (flags, file paths, subcommands), iteration responses in brainstorm.
---

# Input Clarifier

## Overview

Module de clarification conditionnelle pour les inputs dictés. Se déclenche uniquement
quand l'input est détecté comme confus, permettant un workflow fluide pour les inputs clairs.

## Configuration

| Element | Value |
|---------|-------|
| **Trigger** | Clarity score < 0.6 |
| **Model** | Haiku (ultra-fast) |
| **Blocking** | Only when triggered |

## Process

### Step 1: Artifact Detection

Scan input for voice artifacts using patterns from `references/artifact-patterns.md`.

**Categories detected:**
- Hesitation markers: `euh`, `hum`, `hein`, `ben`, `bah`
- Filler words: `genre`, `tu vois`, `quoi`, `en fait`, `du coup`, `truc`, `machin`
- Self-corrections: `non`, `pardon`, `enfin`, `plutôt`, `je veux dire`
- Structural issues: incomplete sentences, contradictions, repetitions

### Step 2: Score Calculation

Calculate clarity score (0.0 - 1.0):

| Artifact Type | Penalty |
|---------------|---------|
| Hesitation markers | -0.1 each |
| Filler words | -0.05 each |
| Self-corrections | -0.1 each |
| Incomplete sentence (no verb, trailing...) | -0.15 |
| Contradictions (mais non, enfin si) | -0.15 |
| Repetitions (same phrase 2x) | -0.1 |

```
Base score: 1.0
Final score: max(0.0, base - sum(penalties))
```

### Step 3: Decision

```
IF score >= 0.6:
   → PASS
   → Return original input unchanged
   → Continue workflow immediately

IF score < 0.6:
   → CLARIFY
   → Generate reformulation
   → Show user prompt
```

### Step 4: Reformulation (if triggered)

When score < 0.6, generate clean version:

1. **Remove artifacts** — Strip hesitations, fillers
2. **Complete sentences** — Add implied verbs/subjects
3. **Resolve contradictions** — Keep last stated intent
4. **Preserve meaning** — Don't add assumptions

**Output format:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚠️  INPUT CONFUS DÉTECTÉ (score: 0.4)                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ **Original** :                                                      │
│ "euh le truc là il marche plus, enfin le bouton quoi, non pardon   │
│ le formulaire"                                                      │
│                                                                     │
│ **Reformulation** :                                                 │
│ "Le formulaire ne fonctionne plus"                                  │
│                                                                     │
│ [1] ✅ Utiliser la reformulation                                    │
│ [2] ✏️  Modifier                                                     │
│ [3] ➡️  Garder l'original                                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Step 5: User Choice

| Choice | Action |
|--------|--------|
| [1] Utiliser | Continue with reformulated input |
| [2] Modifier | User provides corrected version |
| [3] Garder | Continue with original (as-is) |

### Step 6: Return

Return structured result:

```json
{
  "cleaned_input": "Le formulaire ne fonctionne plus",
  "original_input": "euh le truc là...",
  "was_clarified": true,
  "score": 0.4,
  "artifacts_found": ["euh", "truc", "quoi", "enfin", "non pardon"]
}
```

---

## Integration

### Invocation Pattern

Commands should invoke this skill at the start of their workflow:

```markdown
### Step 0: Input Clarification (Conditional)

**Skill**: `input-clarifier`

IF user provided free-form text input:
   Invoke input-clarifier
   Use returned `cleaned_input` for subsequent steps

IF --no-clarify flag:
   Skip this step
```

### Exclusions

Do NOT invoke for:
- Inputs that are purely flags (`--force`, `--turbo`)
- File paths (`/path/to/file.md`)
- Subcommands (`status`, `init`, `reset`)
- Iteration responses in `/brainstorm` (only initial input)
- Technical content (stack traces, error codes)

---

## Flags

| Flag | Effect |
|------|--------|
| `--no-clarify` | Skip clarification entirely |
| `--force-clarify` | Force clarification even if score >= 0.6 |

---

## Examples

### Clear Input (no intervention)

```
Input: "Le bouton submit ne déclenche pas la validation du formulaire"

Artifacts: none
Score: 1.0

→ PASS (workflow continues immediately)
```

### Confusing Input (clarification triggered)

```
Input: "euh le truc là il marche plus, enfin le bouton quoi"

Artifacts: euh (-0.1), truc (-0.05), quoi (-0.05), enfin (-0.1)
Score: 0.7

→ PASS (still above threshold)
```

```
Input: "euh ben en fait le machin là, tu vois, il marche plus, enfin non pardon, c'est le bouton, non le formulaire quoi"

Artifacts: euh, ben, en fait, machin, tu vois, quoi, enfin, non pardon, non
Score: 0.25

→ CLARIFY
→ Reformulation: "Le formulaire ne fonctionne plus"
```

### Edge Cases

**Stack trace in input:**
```
Input: "TypeError: undefined is not a function at line 42"

→ Technical content detected
→ PASS (don't try to reformulate error messages)
```

**Mixed technical + confusing:**
```
Input: "euh j'ai une erreur là, TypeError quelque chose"

→ Extract technical part, clarify the rest
→ Reformulation: "J'ai une erreur TypeError"
```

---

## References

- `references/artifact-patterns.md` — Complete pattern list

---

*Input Clarifier v1.0 — EPCI Plugin*
