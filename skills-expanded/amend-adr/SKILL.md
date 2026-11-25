---
name: amend-adr
description: >-
  Use when changing an accepted ADR in docs/adr/ — amending, superseding a
  clause, renaming inside one — or when reviewing a PR that touches one.
metadata:
  author: Spool maintainers
---

# /amend-adr — changing an accepted ADR

*Moved verbatim from `docs/CONVENTIONS.md` (#470), which keeps the one-line rule
and points here. The rule binds whether or not this skill is loaded.*

**Amending an accepted ADR** (#141): a change that **narrows, extends or
clarifies** a decision is amended in place — a block
`**Amendment (YYYY-MM-DD, #n):**` on the item or section it affects, with the
date added to the file's `Amended:` header. A change that **reverses** a
decision is a new ADR; the reversed one gets `superseded by ADR-XXXX` in its
status and a pointer, nothing else. **A supersession that reverses one clause**
of an otherwise-standing ADR (#234) names the clause and the superseding ADR
in the status rather than flipping it, and may add one annotation beside the
clause that no longer holds — a reader lands on the clause before the header,
and the rest of the ADR is still accepted, which a bare `superseded` status
would deny. Like an amendment, the annotation adds and rewrites nothing.
**Amendments never touch an existing line**: they add, so the unmarked text
still reads as what was accepted and "what did this ADR decide" needs no git
archaeology. New text goes where it
reads best — appended after the original, or beside a bullet it pairs with —
but nothing above it is rewritten or deleted. An amendment block counts as
decision text from the moment it lands, so the same applies to it: a later
amendment that contradicts an earlier one says so and leaves it standing.
A block edited on its own unmerged branch is not that case — it folds into
its origin commit and lands once.

**Three things are not "touching a line"**, and only these:
- **A rename** (operator's call, 2026-09-19, recorded on #141): swapping an
  identifier for the name the code now uses, with nothing else on the line
  changing — so an ADR keeps naming things a reader can grep for. A rename
  that also **splits or merges** what the name referred to is not one: that
  changes the decision and takes a block. Neither is rewording around it.
- **A rewrap**: line breaks moved with the rendered text identical — collapse
  the whitespace and the paragraph is unchanged.
- **Bookkeeping**: the `Amended:` header and any section index, which are
  navigation rather than decision, and are edited freely.

A whole new item or section that an amendment adds carries
`(added YYYY-MM-DD, #n)` in its heading rather than a block. Reviewer bar,
answerable from the diff alone: marker present, issue linked, and every
touched line is one of the three above.

The ADRs already on `main` were brought up to this rule once, on #141: that
sweep rewrote landed markers and added the `Amended:` headers, which the bar
above forbids. It was the cost of having the rule at all — the alternative
was a rule with six files contradicting it. **The bar binds from #141
onward**, so an edit of that shape afterwards is a defect rather than
precedent, and archaeology that lands on the sweep has this sentence for an
answer.

(The two exclusions from the rename clause, the rewrap clause, and the
amendment-block sentence are the fleet's readings of the operator's bar,
settled on #188 — not the operator's own wording.)
