---
name: create-architectural-decision-memory
description: Use when capturing architectural decisions — technology choices, system design trade-offs, or structural changes. Enforces standardized field collection with modules, alternatives considered, preview confirmation, and automatic linking.
---

# Create Architectural Decision Memory

## Overview

Architectural decision memory captures significant design choices and the rationale behind them.

Core rule: a decision must document what was considered and rejected, not just what was chosen. Never persist without user confirmation.

## When to Use

- A significant architectural or technology choice was made
- A system design trade-off was resolved
- A structural change was introduced with long-term implications
- A decision needs to be documented so future developers understand why

## Required Fields (all mandatory before persisting)

| Field | Source | Description |
|-------|--------|-------------|
| `project` | User or context | Project identifier |
| `category` | Always `"ArchitecturalDecision"` | Memory type |
| `title` | Agent synthesis | Short name for the decision |
| `summary` | Agent synthesis | One-sentence description of what was decided |
| `details` | User or agent | The decision itself and the rationale |
| `modules` | User or inference | System modules affected by this decision |
| `domain` | User or inference | Conceptual domains |
| `alternatives_considered` | User or agent | At least one alternative that was considered and rejected (REQUIRED) |
| `event_date` | Context | ISO 8601 datetime when the decision was made |

## Standardized Workflow

### Step 1: Identify the Decision

1. If from a PR or discussion, extract the core architectural choice.
2. Identify what was decided, why, and what constraints drove the decision.
3. Separate the decision from its implementation.

### Step 2: Collect Data — Ask What You Cannot Infer

The agent must determine:

- **details**: What was decided and why? Include constraints, trade-offs, and expected impact.
- **alternatives_considered**: What other approaches were evaluated? Why were they rejected? Ask:

```text
Quais alternativas foram consideradas e descartadas para esta decisão?
Para cada uma, explique brevemente por que foi descartada.
Exemplo: "Usar Redis como cache — descartado por adicionar complexidade operacional sem ganho significativo neste estágio"
```

- **modules**: Which system modules are affected?

```text
Quais módulos do sistema são afetados por esta decisão?
Exemplos: faturamento, TUSD, contratação, proposta, auth, infra
```

- **domain**: Which conceptual domains?
- **event_date**: When was this decision made?

Do NOT proceed until all required fields are populated. The model will reject ArchitecturalDecision without alternatives_considered.

### Step 3: Search for Related Nodes

Search the memory graph for:

1. **Existing architectural decisions**: Check for superseded or conflicting decisions using `memory.query` with `type=ArchitecturalDecision`.
2. **Business rules**: The decision may be driven by a rule.
3. **Related PRs**: PRs that implement this decision.

Present findings. If a conflicting decision exists, highlight it explicitly:

```text
⚠ Encontrei uma decisão arquitetural existente que pode conflitar:
- [memory_id] "Decisão Y" — motivo do conflito

Deseja marcar a decisão anterior como DEPRECATED, ou criar um link CONFLICTS_WITH?
```

### Step 4: Preview Before Persisting

Show the complete JSON:

```text
Preview da memória que será criada:

{
  "project": "...",
  "category": "ArchitecturalDecision",
  "title": "...",
  "summary": "...",
  "details": "...",
  "modules": [...],
  "domain": [...],
  "alternatives_considered": [...],
  "event_date": "..."
}

Confirma a criação? (sim/não)
```

### Step 5: Persist and Link

1. Call `memory.manual.create` with all fields.
2. Create confirmed links.
3. If superseding an old decision, call `memory.deprecate` on the old one and `memory.link` with `EVOLVES_FROM`.

## Common Mistakes

- Recording a decision without documenting alternatives
- Not specifying which modules are affected
- Failing to check for conflicting existing decisions
- Persisting without preview and confirmation
- Writing implementation details instead of the decision rationale
