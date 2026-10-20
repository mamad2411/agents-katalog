---
name: create-code-pattern-memory
description: Use when capturing reusable code patterns, design patterns, or implementation conventions. Enforces standardized field collection with modules, examples, preview confirmation, and automatic linking.
---

# Create Code Pattern Memory

## Overview

Code pattern memory captures reusable implementation patterns that should be followed across the codebase.

Core rule: a pattern must have at least one concrete example. Never persist without user confirmation.

## When to Use

- A reusable implementation pattern was identified
- A coding convention or design pattern should be documented
- A PR introduced a pattern that should be replicated elsewhere

## Required Fields (all mandatory before persisting)

| Field | Source | Description |
|-------|--------|-------------|
| `project` | User or context | Project identifier |
| `category` | Always `"CodePattern"` | Memory type |
| `title` | Agent synthesis | Short name for the pattern |
| `summary` | Agent synthesis | One-sentence description |
| `details` | User or agent | Full description of the pattern |
| `modules` | User or inference | System modules where this pattern applies |
| `domain` | User or inference | Conceptual domains |
| `examples` | Code or user | At least one concrete example or code reference (REQUIRED) |
| `event_date` | Context | ISO 8601 datetime when the pattern was identified |

## Standardized Workflow

### Step 1: Identify the Pattern

1. If from a PR, read the code and extract the reusable pattern.
2. Separate the pattern from the specific implementation instance.
3. Write it in a way that can be applied elsewhere.

### Step 2: Collect Data — Ask What You Cannot Infer

The agent must determine:

- **details**: Describe the pattern clearly. What problem does it solve? How should it be applied?
- **examples**: At least one concrete example. Can be a file:line reference, code snippet description, or PR reference. Ask:

```text
Pode me dar pelo menos um exemplo concreto deste padrão no código?
Exemplo: "services/auth_service.py usa esse padrão no método validate_token"
```

- **modules**: Which system modules use or should use this pattern?

```text
Em quais módulos este padrão se aplica?
Exemplos: faturamento, TUSD, contratação, proposta, auth
```

- **domain**: Which conceptual domains?
- **event_date**: When was this pattern identified?

Do NOT proceed until all required fields are populated. The model will reject CodePattern without examples.

### Step 3: Search for Related Nodes

Search the memory graph for:

1. **Existing code patterns**: Check for duplicates or related patterns using `memory.query` with `type=CodePattern`.
2. **Business rules**: The pattern may implement a rule.
3. **Related PRs**: PRs that introduced or use this pattern.

Present findings and ask about linking.

### Step 4: Preview Before Persisting

Show the complete JSON:

```text
Preview da memória que será criada:

{
  "project": "...",
  "category": "CodePattern",
  "title": "...",
  "summary": "...",
  "details": "...",
  "modules": [...],
  "domain": [...],
  "examples": [...],
  "event_date": "..."
}

Confirma a criação? (sim/não)
```

### Step 5: Persist and Link

1. Call `memory.manual.create` with all fields.
2. Create confirmed links.

## Common Mistakes

- Creating a pattern without any concrete example
- Describing a one-off implementation as a reusable pattern
- Not specifying which modules the pattern applies to
- Persisting without preview and confirmation
