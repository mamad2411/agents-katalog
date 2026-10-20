---
name: knowledge-modeling
description: Use when building or refining a project's domain model, glossary, or bounded contexts, when validating tool outputs/data against a domain ontology before side effects, or when extracting entities, relations, evidence, and provenance from Markdown/plain text into a typed versioned knowledge graph under `.devin/`.
agent: architect
triggers: [user, model]
---

# Knowledge Modeling

Domain model, ontology validation, and knowledge-graph extraction — the
typed-vocabulary family.

## Domain modeling (active discipline)

Build and sharpen the domain model as you design — challenge terms, invent
edge-case scenarios, write glossary + decisions the moment they crystallise.
(Merely *reading* `.devin/CONTEXT.md` is a habit, not this skill — this is
for *changing* the model.)

Structure: `.devin/CONTEXT.md` (glossary + bounded contexts) + `.devin/adr/`
(decisions). Formats: `reference/CONTEXT-FORMAT.md`,
`reference/ADR-FORMAT.md`.

Cross-skills: `research` for authoritative term definitions; deep-mode for
how code currently uses terms; `ai-coding-dictionary` for AI-coding jargon
alignment.

## Ontology validation (before side effects)

> **Pydantic at the door, ontology at the ledger.**

Schema/type checks (Pydantic or equivalent) validate shape; ontology
validates domain-level reasonableness. Check, before any write/insert/API
call driven by tool output:

1. **Entity type** valid for this domain.
2. **Status** value allowed (`pending`/`in_progress`/`completed`…).
3. **Relationship** type makes sense (`contains`, `depends_on`…).
4. **No duplicates** — entity or relation already exists?
5. **Disjointness** — disjoint entities treated as same?

```python
# Schema validates shape
class Ticket(BaseModel):
    status: Literal["pending", "in_progress", "completed"]

# Ontology validates domain
if ticket.status == "completed" and ticket.depends_on_open():
    raise ValueError("Cannot complete ticket with open dependencies")
```

Helper: `python3 scripts/validate.py` (this skill's `scripts/`). Anti-pattern:
trusting tool output because the schema allows it.

## Knowledge extraction (text → typed graph)

Deterministic, provider-neutral extraction of entities, relations, evidence,
and provenance from Markdown/plain text into versioned JSON + relational
Markdown under `.devin/`. No API key, no LLM — lexical baseline (not vector
search).

- Every extracted fact points back to `source file:line` + quote.
- Incremental: merge new sources without duplicating entities or silently
  overwriting conflicts (conflicts reported, explicit action required).
- Baseline for evaluating Hyper-Extract/embeddings/MCP later.

Helper: `python3 scripts/extract.py`.
