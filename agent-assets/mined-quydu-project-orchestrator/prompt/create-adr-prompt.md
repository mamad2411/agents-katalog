---
mode: agent
description: Create a numbered Architecture Decision Record from a decision, its context, options, and consequences.
---

# Create an ADR

Create a new Architecture Decision Record in `docs/adr/`.

1. Read `docs/adr/` and choose the next sequential four-digit number.
2. Read `docs/adr/0000-template.md` and follow its structure exactly.
3. Gather the decision context from the repository before asking the user. Ask only for what the repository cannot answer.
4. Record at least two genuinely considered options with their trade-offs, not a strawman.
5. State consequences honestly, including the negative ones and what becomes harder.
6. Set status to `Proposed` unless the user confirms the decision is already accepted.
7. If this decision replaces an earlier one, set the earlier ADR to `Superseded by NNNN` and link both directions.

Name the file `docs/adr/NNNN-short-kebab-title.md`. Do not modify accepted ADRs other than to mark them superseded.
