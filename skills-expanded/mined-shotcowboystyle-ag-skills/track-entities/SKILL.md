---
name: track-entities
description: Use when people, organisations, or accounts recur across the material — maintains a register of entities with their aliases, identifiers, and relationships, and keeps it consistent with the redaction alias mapping. Triggers - "track this person", "who is involved", "update the entity register".
allowed-tools: Bash(grep *), Bash(find *), Bash(mkdir *), Bash(date *), Read, Write
---

# Track Entities

Maintain the register of people, organisations, and accounts that recur across the
matter, with their aliases and how they relate.

## When to use

- The same name appears in several spellings or forms.
- Working out who is who before drafting.
- Keeping redaction aliases consistent with the real entity list.

## Inputs

- An entity name or query. Optional — with no argument, summarise the register.

## Procedure

### 1. Read the register

`entities/register.jsonl`, one entity per line. Create it if the workspace has none.

### 2. Record what distinguishes an entity

For each: canonical name, type, every observed variant spelling, identifiers, the first
and most recent material it appears in, and a one-line description of its role.

Keep the identifiers that actually distinguish people — a company number, a case
reference, a handle. A name alone does not identify anyone, and two people sharing a name
is the normal case, not the edge case.

### 3. Resolve carefully, and record the doubt

Before merging two records into one entity, state what the merge rests on. A shared name
is not enough. A shared identifier usually is. Where it is uncertain, keep them separate
and cross-reference with a note saying they may be the same — an unwound merge is far
more expensive than a missing one.

### 4. Record relationships as observed

Store relationships as directed statements with a source: who, to whom, what
relationship, and where it was observed. Never record a relationship that was inferred
without marking it inferred and giving the reasoning.

### 5. Keep aliases in step

Where the workspace has a redaction alias mapping at `aliases/active_mapping.json`, keep
the entity register and the mapping consistent: an entity's canonical name should map to
one pseudonym, and every spelling variant should map to the same one. A variant that
was missed is a name that survives redaction.

Report any entity present in one file and absent from the other.

### 6. Report

With a query, return the matching entity, its variants, its relationships, and the
material it appears in. With no query, summarise counts by type and name any entity with
unresolved variants or missing identifiers.

## Output

- An updated `entities/register.jsonl`.
- Any inconsistency between the register and the alias mapping.

## Notes

- The register is append-and-amend. Keep superseded records with a note rather than
  deleting them, so a merge can be reviewed later.
- This register is about identification within the matter. It is not a dossier, and it
  records only what the matter's scope covers.
