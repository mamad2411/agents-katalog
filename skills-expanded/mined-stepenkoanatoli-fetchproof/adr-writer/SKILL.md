---
name: adr-writer
description: Records an architecture decision record whenever a design choice set an alternative aside - context, the decision, each rejected alternative with the reason a future reader needs to avoid re-suggesting it, and a dated trigger that would reopen it - and adds it to the ADR index. Use when a choice about behaviour, a format, a rule, a module's responsibility or a deferral had a credible alternative, when the user says "record this decision" or "write an ADR", or when a decision supersedes an older one.
---

# ADR writer

A decision with a rejected alternative is recorded, or the alternative comes back.

## When

Write one when a choice about how the system behaves, what it stores or what it promises
set an alternative aside - including a "not now". Test mechanics, wording, and a bug fix
with one obvious remedy do not need one; the commit report's **why** names any
alternative there.

## Shape

File: the next free number in the project's ADR log (`docs/adr/NNNN-<slug>.md` here),
and one row in its index in the same commit.

```
# ADR-NNNN — <the decision, as a sentence>

- **Date:** YYYY-MM-DD
- **Status:** accepted | superseded by ADR-MMMM
- **Area:** <modules, files, rules it governs>

## Context
<what forced the choice; the evidence rows or the incident>

## Decision
<what is done, precisely enough to check>

## Rejected alternatives
- **<alternative>.** <why not - the reason a future reader needs>

## Trigger to revisit
<the observable event that reopens it, dated if time-bound>
```

## Rules

- Existing ADRs are never edited to change their decision. A decision that is wrong is
  superseded by a new ADR that says so, and the old one's status points at it.
- An external fact in the context cites its evidence row, not memory.
