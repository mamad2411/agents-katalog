---
name: architecture-decision-records
description: Writes architecture decision records that capture the context, the options weighed, the decision and its consequences in a short, numbered file.
---

# Architecture decision records

One decision per record. Write it so a stranger can follow the reasoning in two minutes.

## Steps

1. Look for an existing folder (`docs/adr`, `docs/decisions`, `adr/`) and follow its numbering and template. If none exists, create `docs/adr/` and start at `0001`.
2. Name the file `NNNN-short-title-in-kebab-case.md`. Never renumber or delete earlier records.
3. Write these sections:
   - **Title**: a decision as a phrase, such as "Use PostgreSQL for order storage".
   - **Status**: Proposed, Accepted, Deprecated, or Superseded by ADR-NNNN.
   - **Context**: the forces at play: requirements, constraints, team skills, deadlines, scale numbers. Facts only.
   - **Options considered**: two to four, each with its strongest argument and its main drawback. Include "do nothing" when it is real.
   - **Decision**: one clear sentence in active voice ("We will..."), then the reason it won.
   - **Consequences**: what gets easier, what gets harder, what risks remain, and what would make us revisit.
4. Check each claim against the code or docs. Link tickets, benchmarks and the relevant files.
5. Keep it to one page. Cut history that does not change the decision.
6. If the new record replaces an older one, update only the old record's status line to point to it.

## Rules

- Never record a decision the user has not made. Ask when the choice is still open and mark it Proposed.
- Do not hide the downsides of the chosen option.

## Report

The new file path, its status, and any older records it supersedes.
