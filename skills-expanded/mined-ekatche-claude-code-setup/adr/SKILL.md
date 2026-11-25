---
name: adr
description: Use when making, changing, or deprecating an architectural, data-model, protocol, topology, or domain-rule decision — records immutable Architecture Decision Records (lightweight MADR format) in docs/adrs/ with numbered files, status lifecycle, actionable code invariants, and an index README. Portable across Claude Code and Antigravity (agy).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
---

# ADR — Architecture Decision Records

Capture every structuring decision in `docs/adrs/` using a lightweight, immutable MADR format so future developers and agents understand **what** was decided, **why**, and **which invariants the code must enforce**.

## When to Use

Trigger this skill whenever a task involves:
- System topology, service boundaries, or storage choices (queues, caches, databases).
- Cross-system identity, routing keys, or ownership matrices.
- API, webhook, or message-schema contracts and retry/idempotency guarantees.
- Domain rules with non-obvious invariants (read-only guards, normalization, fallback rules).
- Replacing, deprecating, or amending a previously accepted architectural decision.

Do **not** use for routine bug fixes or refactors that leave existing architectural decisions unchanged.

## Golden Rules (Immutability Law)

1. **One decision = one numbered file**:
   `docs/adrs/NNNN-titre-en-kebab-case.md` (4-digit zero-padded sequence: `0001`, `0002`, ..., short indicative title).
2. **Append-only (never rewrite history)**:
   An accepted ADR is never silently edited to change its decision. When a decision changes:
   - Create a new ADR (`ADR-MMMM`) whose metadata states `Remplace / remplacé par : Remplace ADR-NNNN`.
   - Update the superseded ADR's status to `Remplacée par ADR-MMMM` (or `Acceptée, point X remplacé/précisé par ADR-MMMM` for a partial amendment).
   - Update the index table in `docs/adrs/README.md`.
3. **Facts, not opinions, in `## Contexte`**:
   Document the concrete constraint, measured limit, or observed incident that forces the decision.
4. **Executable invariants in `### Règles qui en découlent pour le code`**:
   This subsection is mandatory. List strict, verifiable rules that code and tests must respect (what is forbidden, what is required, where guards live).
5. **Traceability in `## Références`**:
   Point to exact source files, test files enforcing the rule, scripts, and related ADRs.
6. **Maintain the index (`docs/adrs/README.md`)**:
   Keep the index table (`| N° | Titre | Statut | Date |`) synchronized, track unresolved external questions in `## Questions ouvertes` (referencing their ADR), and preserve the creation checklist.

## Workflow

1. **Inspect existing ADRs**:
   - Read `docs/adrs/README.md` (or initialize `docs/adrs/` from `references/README_TEMPLATE.md` and `references/template.md` if absent).
   - Check whether an existing ADR already covers or conflicts with the topic.
2. **Determine the next number**:
   - Take the highest `NNNN` in `docs/adrs/` + 1 (zero-padded to 4 digits).
3. **Draft the ADR**:
   - Copy the structure from `references/template.md`.
   - Keep `## Décision` in the present tense, crisp and unambiguous.
   - Populate `### Règles qui en découlent pour le code` with concrete invariants and `## Alternatives écartées` with why each alternative was rejected.
4. **Update cross-references**:
   - Add the new row to `docs/adrs/README.md`.
   - If superseding or amending an older ADR, update its `- **Statut**` and `- **Remplace / remplacé par**` lines and its row in `docs/adrs/README.md`.
   - If the decision leaves an external question open, add it under `## Questions ouvertes` in `docs/adrs/README.md` with its ADR reference.

## References

- `references/template.md` — Lightweight MADR template for individual ADR files.
- `references/README_TEMPLATE.md` — Template for initializing `docs/adrs/README.md`.

