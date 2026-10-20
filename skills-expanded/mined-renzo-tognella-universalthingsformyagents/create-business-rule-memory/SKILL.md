---
name: create-business-rule-memory
description: Use when capturing durable business rules from product, domain, workflow, or policy changes. Enforces standardized field collection with modules, preview confirmation, and automatic linking to PRs and existing rules.
---

# Create Business Rule Memory

## Overview

Business rule memory captures domain truth that should outlive a single PR.

A PR may introduce the rule, but the rule itself is a separate memory node.

Core rule: separate the rule from its implementation. Never persist without user confirmation.

## When to Use

- A product or domain rule was clarified
- A workflow constraint became explicit
- Authorization or data ownership semantics changed
- A PR implemented or refined a rule that should be reusable memory

## Required Fields (all mandatory before persisting)

| Field | Source | Description |
|-------|--------|-------------|
| `project` | User or context | Project identifier |
| `category` | Always `"BusinessRule"` | Memory type |
| `title` | Agent synthesis | Short, stable name for the rule |
| `summary` | Agent synthesis | One-sentence description |
| `details` | User or agent | The rule itself in stable, implementation-free language |
| `modules` | User or inference | System modules affected (e.g., faturamento, TUSD, contratação) |
| `domain` | User or inference | Conceptual domains (e.g., energia, billing, compliance) |
| `event_date` | Context | ISO 8601 datetime when the rule was identified |

## Standardized Workflow

### Step 1: Identify the Rule

1. If the trigger is a PR, read the PR and extract the underlying domain rule.
2. If the trigger is a conversation, isolate the stable business truth from implementation details.
3. Separate the rule statement from how it was implemented.

### Step 2: Collect Data — Ask What You Cannot Infer

The agent must determine:

- **details**: Write the rule in stable language. Example: "Todos os usuários autenticados podem visualizar qualquer proposta." NOT "PR #9 mudou a policy para que users vejam propostas."
- **modules**: Which system modules does this rule affect? Ask the user if not obvious:

```text
Esta regra de negócio afeta quais módulos do sistema?
Exemplos: faturamento, TUSD, contratação, proposta, relatórios, auth
```

- **domain**: Which conceptual domains? Ask if not obvious:

```text
Em qual domínio conceitual esta regra se encaixa?
Exemplos: energia, billing, compliance, regulatório, comercial
```

- **event_date**: When was this rule identified? Use today's date if from current conversation.

Do NOT proceed until all required fields are populated.

### Step 3: Search for Related Nodes

Before persisting, search the memory graph for:

1. **Existing business rules in the same domain/modules**: Use `memory.query` with `type=BusinessRule` and keywords from the rule. Check for duplicates or conflicting rules.
2. **Related PRs**: Search PR memories that touch the same modules or areas.

Present findings:

```text
Busquei no grafo e encontrei:

Regras de negócio existentes no mesmo domínio:
- [memory_id] "Regra Y" — possível relação: REFINES / CONFLICTS_WITH / RELATED_TO

PRs que tocam os mesmos módulos:
- [repo]#[number] — implementa ou evidencia esta regra

Deseja criar links? Se sim, quais e com qual tipo de relação?
```

If a duplicate is found, warn the user and suggest updating the existing rule instead of creating a new one.

### Step 4: Preview Before Persisting

Show the complete JSON:

```text
Preview da memória que será criada:

{
  "project": "...",
  "category": "BusinessRule",
  "title": "...",
  "summary": "...",
  "details": "...",
  "modules": [...],
  "domain": [...],
  "event_date": "..."
}

Confirma a criação? (sim/não)
```

### Step 5: Persist and Link

1. Call `memory.manual.create` with all fields.
2. If the user confirmed links in Step 3, call `memory.link` or `memory.pr.link_memory` for each confirmed relationship.

## Rule Writing Guidance

Prefer stable, implementation-free language:

Good: `Todos os usuários autenticados podem visualizar qualquer proposta.`
Bad: `PR #9 changed the policy so users now see proposals.`

The PR belongs in a relation, not in the rule statement itself.

## Common Mistakes

- Encoding temporary implementation detail as business rule
- Writing a rule without specifying affected modules
- Not searching for duplicate or conflicting existing rules
- Persisting without preview and confirmation
- Duplicating the PR summary instead of isolating the domain truth
- Leaving `modules` empty
