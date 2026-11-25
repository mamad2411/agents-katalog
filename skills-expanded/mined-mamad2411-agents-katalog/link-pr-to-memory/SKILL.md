---
name: link-pr-to-memory
description: Use when connecting a PR memory to business rules, code patterns, architectural decisions, areas, or other PR memories based on explicit evidence. Also used by other creation skills for post-creation linking.
---

# Link PR to Memory

## Overview

This skill creates graph relationships between PR memory and other memory nodes.

The point is not just storage. The point is navigable engineering context.

## When to Use

- A PR implements a business rule
- A PR introduces or reinforces a code pattern
- A PR affects an architectural decision
- One PR follows up, fixes, or complements another PR
- A creation skill (create-pr-memory, create-business-rule-memory, etc.) needs to create post-creation links

## Preferred Relations

| Relation | Use When |
|----------|----------|
| `IMPLEMENTS` | PR implements a business rule or architectural decision |
| `EVIDENCES` | PR provides evidence for a rule or pattern |
| `MODIFIES` | PR updates or changes an existing memory |
| `RELATED_TO` | General association between PR memories |
| `REFINES` | One PR narrows or improves another |

## Workflow

### Step 1: Identify Source and Target

1. Start from the PR memory (source).
2. Identify the target memory node by searching with `memory.query` or `memory.pr.query`.
3. If the target is not found, inform the user and offer to create it first.

### Step 2: Choose the Narrowest Valid Relation

- Do not default to `RELATED_TO` when a stronger relation exists.
- If the PR clearly implements a rule, use `IMPLEMENTS`.
- If the PR modifies an existing pattern, use `MODIFIES`.

### Step 3: Record Rationale

Provide a short, factual rationale grounded in evidence.

Good: `Introduces middleware and shared API refresh flow used by the auth foundation.`
Bad: `Seems related to auth stuff.`

### Step 4: Create the Link

Call `memory.pr.link_memory` with:
- `pr_memory_id`: the PR memory ID
- `memory_id`: the target memory node ID
- `relation_type`: the chosen relation
- `rationale`: the evidence-based rationale

## Evidence Standard

Link only when at least one of these is true:

- The PR description states it
- Changed files clearly support it
- The diff shows the relation directly
- The linked work item states the intent

Do not create speculative links just because names look similar.

## Common Mistakes

- Creating generic `RELATED_TO` links when a stronger relation exists
- Linking without evidence
- Not checking if the target memory node exists before attempting to link
