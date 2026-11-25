---
name: adr-capture
description: 'Catch an architectural or technical decision as it is being made and draft an Architecture Decision Record (ADR) in the team''s format, leaving explicit TODOs for fields the conversation did not cover. Never writes or commits without explicit confirmation. Use this when the user asks to "draft an ADR", "record this decision", "capture this as an ADR", AND proactively offer it when the conversation shows a commitment pattern — "we''ll go with X over Y because Z", "let''s standardize on...", "decided to...", "we''re choosing..." — paired with a rationale. Do NOT use for: exploratory discussion with no commitment ("we might try", "could consider", "what if we"), non-architectural decisions (scheduling, naming, trivial style), or generating product/requirements specs. When unsure whether a real decision was actually made, ask one question rather than draft.'
version: 0.3.0
---

# adr-capture

Decisions get lost because writing them down is friction. This skill catches the
decision while it's warm and produces an ~80%-complete draft for review. It
never auto-commits, and it biases toward false negatives — better to miss a
decision and be asked than to spam the ADR log with drafts of things that were
only floated.

## Detecting a decision

A real decision has two parts: a **commitment** signal and a **rationale**.

- Commitment: "going with", "we'll use", "decided", "chose X over Y", "let's
  standardize on".
- Rationale: at least one because/why, even if implicit.

Exploratory phrasing — "might", "could", "what if", "worth considering" — is NOT
a decision. If you see commitment without a clear rationale, or you're unsure,
ask one question to confirm before drafting. Do not draft on ambiguity.

## Drafting workflow

1. **Config.** Read optional `.claude/adr/config.yaml` for `adr_dir` (default
   `docs/adr/`), the id format, and the list of `mandatory_sections` — see
   `references/config.example.yaml` for the schema. Otherwise use the defaults
   baked into `references/adr-template.md`.

2. **Next id.** Scan `adr_dir` for the highest existing ADR number and
   increment. Slugify the decision title for the filename, e.g.
   `0042-vector-store.md`.

3. **Fill from the conversation.** Map what was said onto the template: context
   and forces, the decision, alternatives considered and why each was rejected,
   consequences (both + and −).

4. **Mark the gaps.** For every mandatory section the conversation did not
   cover, insert a literal `<TODO: ...>` with a hint of what's needed. Never
   invent regulatory, security, data-classification, or rollback content — those
   must come from a human.

5. **Review, then write.** Show the full draft in chat first. Write the file
   only after explicit confirmation, with `Status: Proposed`. Never commit, and
   never set any status past Proposed on the user's behalf — that is a human
   approval step.

See `references/adr-template.md` for the section structure. The team declares
its mandatory sections in `.claude/adr/config.yaml`; with no config the
default is `Rollback plan` alone. Do not add heavier headings (regulatory
impact, data classification, security review) unless the team declared them —
an ADR full of TODOs nobody will fill teaches the team to ignore the section.
