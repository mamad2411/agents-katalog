---
description: Feature-specific entry point for new feature definition. Composition over grill — internally invokes /appmaker:grill (or grill-brownfield) for relentless questioning, then structures output to appmaker/features/<NNN-slug>/interview-result.md. Use when user wants to start defining a new feature.
disable-model-invocation: true
---

Feature-specific wrapper around `/appmaker:grill`. Adds structured output, feature folder allocation, readiness gate. NOT a replacement for grill — composition over it.

## When to invoke

- Manual: `/appmaker:interview "<feature description>"` or `/appmaker:interview` then describe
- Auto: by `start` skill on intent classified as `feature`
- AFK-safe: NO — interactive grilling requires human responses; allocates feature folder (side effect)
- Required state: `appmaker/` directory present (run `/appmaker:init` first if missing)
- Required input: feature description

## Process

### 0. Pre-flight: read memory wiki (MANDATORY)

Before generating feature questions, read prior domain understanding + shipped-feature index. This prevents asking about already-decided domain semantics or proposing features that duplicate an existing one.

```bash
# Pre-flight wiki cat — respects wiki_preflight_mode config flag (v0.2.12)
WIKI_MODE=$(grep '^wiki_preflight_mode:' appmaker/config.yaml 2>/dev/null | awk '{print $2}')
WIKI_MODE="${WIKI_MODE:-auto}"
if [ "$WIKI_MODE" != "never" ]; then
  for page in domain-model feature-index; do
    f="appmaker/memory/wiki/${page}.md"
    # Skip missing or header-only files (≤5 lines = seed stub, not real content yet) — saves tokens on fresh projects
    if [ -f "$f" ] && [ "$(wc -l < "$f")" -gt 5 ]; then
      echo "─── $f ───" && cat "$f"
    fi
  done
fi
```

Cite as `per wiki/feature-index.md: feature 003 already shipped this — clarify what's different?` when relevant. If `feature-index.md` lists a near-duplicate, surface it via AskUserQuestion before generating interview-result.md.

### 1. Confirm feature intent

If user invoked directly without intent, ask via AskUserQuestion: "What feature do you want to define?" If user says "just exploring, not sure if feature" → redirect to `/appmaker:grill` (no artifact).

### 2. Allocate feature folder

1. List `appmaker/features/` to find highest existing number (e.g., `001-...`, `002-...`).
2. Allocate next number (e.g., `003`).
3. Generate slug from feature description (kebab-case, ~3-5 words, e.g., "add-dark-mode").
4. Create folder: `appmaker/features/003-add-dark-mode/`.
5. Note path to user.

### 3. Detect greenfield vs brownfield

- Brownfield triggers: existing `appmaker/glossary.md` has terms, existing `appmaker/features/` has prior features, existing codebase substantial (>10 source files).
- Greenfield: new project, mostly empty.

### 4. Invoke grill (with brownfield variant if applicable)

- Greenfield: invoke `/appmaker:grill`.
- Brownfield: invoke `/appmaker:grill-brownfield` (reads existing docs/code/glossary first).

Pass context: feature description + folder path.

### 5. After grill closes — structure output

When grill detects closure, interview takes back control. Structures conversation into `interview-result.md`:

```markdown
---
feature: add-dark-mode
folder: 003-add-dark-mode
created: 2026-05-11
last_updated_by: interview
readiness: ready  # ready | needs_more_input | reject | ready_with_override
---

# Interview Result: Add Dark Mode

## Problem
[1-2 paragraphs]

## Scope
- **Goals:**
- **Non-goals:**
- **Constraints:**

## Product
- **Primary workflows:**
- **Success criteria:** (verifiable: auto-check OR human-review-with-criteria)
- **Edge cases:**

## Technical
- **Preferred stack:**
- **Integrations:**
- **Data sensitivity:**
- **Deployment target:**

## Risks
- **Ambiguous areas:**
- **Assumptions:**
- **Questions remaining:**

## Readiness
**Status:** ready | needs_more_input | reject | ready_with_override

If `ready_with_override`: include reason.
```

### 6. Output summary + suggest next

```
✓ Interview complete: appmaker/features/003-add-dark-mode/interview-result.md
✓ Glossary: +5 terms (theme, dark-mode-toggle, color-palette, ...)
✓ Readiness: ready

Suggested next:
  /appmaker:prd — synthesize PRD from this interview
Or:
  /appmaker:clarify — extra questions on ambiguous areas first
```

## Difference from `/appmaker:grill`

| | grill | interview |
|---|---|---|
| Purpose | Sharpen any idea | Define feature |
| Output | Conversation only | `interview-result.md` artifact |
| Folder allocation | No | Yes (`features/<NNN-slug>/`) |
| Composes | Standalone | Wraps grill |

## Guardrails

- **Don't replicate grill logic.** Compose, don't replicate. Call `/appmaker:grill` (or `/appmaker:grill-brownfield`).
- **Don't write artifact mid-grilling.** Wait for grill to detect closure first.
- **Allocate folder early (step 2).** User sees path immediately.
- **Readiness mandatory.** Every interview-result.md has explicit readiness state.
- **`ready_with_override` requires reason.**
- **Glossary updates handled by grill.** Don't double-update.
- **Don't allocate folder if user not committed to feature.** If "just exploring" → redirect to grill.
- **Don't auto-invoke `/appmaker:prd` next.** User confirms next step.
