---
name: grill-with-docs
description: Alias: a relentless interview to sharpen a plan or design that also writes ADRs and a glossary as decisions are made. Use when the user wants questioning plus durable docs. Not for plain questioning without docs (use grill-me).
disable-model-invocation: true
---
Call the Skill tool twice, for "grilling" and "domain-modeling".

## Purpose
Alias skill. Runs the `grilling` and `domain-modeling` skills together so each decision is also recorded as an ADR or glossary entry.

## When to use
The user wants a plan challenged and the resulting decisions and terms documented.

## When NOT to use
- Questioning without any documentation -> grill-me.
- The repository has no place for docs and the user does not want files created.

## Core workflow
1. Call the Skill tool for "grilling".
2. Call the Skill tool for "domain-modeling".
3. As decisions settle, write ADRs and update the glossary using those skills' conventions.

## Validation
- Each settled decision has a matching ADR or glossary entry; terms in docs match terms used in the conversation.

## Output requirements
Resolved decisions plus new or updated ADR and glossary files (paths listed).

## Example
```text
"Grill my billing design and document it" -> grilling questions -> ADR for "invoice per tenant" -> glossary entry "Tenant".
```

## Related skills
grilling, domain-modeling, grill-me
