---
name: adr-lifecycle
description: >-
  Fires at the moment a hard-to-reverse choice is settled — during framing, planning, review,
  or reconciling — and on the symptom of the same choice being re-argued across sessions
  ("why did we choose X"), and on explicit asks: "write an ADR", "record this decision",
  "supersede ADR-NNNN", "review this ADR". Author, review, number, index, and
  supersede Architecture Decision Records — the durable record of such a choice and the
  options it rejected. Runs a significance gate before authoring, picks a formality tier,
  requires at least two genuinely considered options and one named negative consequence,
  keeps implementation detail out of the record, and treats an accepted record as immutable —
  supersede, never edit. Neighbour boundary: `../change-writing/SKILL.md` owns commit,
  pull-request, and squash text, including the message that lands an ADR file; this skill
  owns only the decision record itself. An accepted ADR is advisory evidence; it never
  authorizes a push, merge, publication, deployment, or queue mutation.
---

# ADR lifecycle

One ADR records **one decision**: the forces that made it necessary, the options that were
genuinely considered and rejected, the option taken, and the costs accepted with it. It is not a
specification, not a design doc, and not a changelog.

## Authority boundary (advisory evidence, never authorization)

An accepted ADR is durable evidence a conductor may cite when adjudicating a later related
proposal. It is not a gate result and not an authorization. No ADR — accepted, reviewed, or
indexed — authorizes a push, publication, pull-request mutation, merge, deployment, credential
use, or queue mutation; each of those needs explicit operation-specific authorization from a
human. Work an ADR leaves open departs as exactly one typed `SeedProposal` for conductor triage.

An accepted ADR also does not retroactively make existing non-conforming code compliant. That
gap is its own recorded item of work, not an implication of the record.

## Mode selector

One hop each. Read only the file the request lands on.

| Request | Go to |
|---|---|
| A decision was just made; write the record | §Workflow below, then `references/house-template.md` |
| Is this even worth an ADR? | §Step 0 below |
| Which template tier / what goes in each field? | `references/house-template.md` |
| Reviewing someone else's ADR | `references/review-and-antipatterns.md` |
| Supersede, deprecate, or relate two records | `references/lifecycle-states.md` |
| Typed edges, the index, a multi-record initiative | `references/relationships-and-index.md` |
| How does this record sit in the authority model? | `references/adr-as-evidence.md` |
| Write the commit or PR text that lands it | `../change-writing/SKILL.md` |

## Hard rules

1. **Significance first.** Run Step 0 before drafting. A choice that fails it gets a lighter
   record, not an ADR.
2. **At least two genuinely considered options.** A straw option included to be rejected is a
   rejection of the rule, not a satisfaction of it.
3. **The title states the decision, not the question.** Imperative and settled: "mise is the
   single front door", never "Should we use mise?".
4. **One decision per file.** An "and" in the title usually means two ADRs.
5. **At least one named negative consequence.** A record with only upsides was not a decision.
6. **Immutable after accept.** The only edit to an accepted record is its status line. Everything
   else is a supersession.
7. **No append-only update log.** An ADR that grows dated "Update:" sections has become a
   changelog. Supersede instead.
8. **Supersession ordering.** The replacement reaches `accepted` *before* the superseded record's
   status flips. Never leave both records non-authoritative at once.
9. **Decision, not specification.** No full schemas, config blocks, API contracts, or
   implementations in the body. Illustrative fragments only; substance goes to a sibling design
   doc cited by path.
10. **Confirmation names something real.** If the decision is mechanically checkable, name the
    actual command or review step in this repository that checks it — never a hypothetical
    fitness function.
11. **Reversal condition is an observable event.** One thing that would falsify the decision, and
    who would see it. Not a date, not a feeling.
12. **Record and index land together.** The new or edited record and the index entry are one
    change. Message text comes from `../change-writing/SKILL.md`.

## Workflow

**Step 0 — significance gate.** A choice earns an ADR when it is expensive or slow to reverse
*and* at least one of these holds:

- it constrains structure, a cross-cutting concern, or an interface others must build against;
- it accepts a named non-functional cost (performance, security, operability, portability);
- it takes on or refuses an external dependency the team does not control;
- it is first-of-a-kind here, or a repeat of something that previously caused trouble;
- a key stakeholder disagrees, or would if asked;
- it has already been re-argued from scratch more than once because no record exists.

Fails the gate → propose the cheapest record that holds it (a one-sentence rationale line in
the code, a design-doc paragraph, or a tracked item) and stop. Say which, and why an ADR would
be over-ceremony. Refusing to write an ADR is a valid outcome of this skill.

**Step 1 — readiness.** Do not draft until all five exist: the stakeholders are named; the
timing is right (the most responsible moment — late enough to know, early enough to matter); at
least two options are real; the drivers and context are writable without hand-waving; the tier
is chosen. A gap here produces a worse record than waiting.

**Step 2 — locate the directory.** Prefer, in order: an existing `docs/adr/`, `docs/decisions/`,
`doc/architecture/decisions/`. None present → ask. Do not invent a sixth convention. If the
choice of location is itself contested, that is an ADR-0000 meta-record.

**Step 3 — pick the tier.** Weight of the decision sets the ceremony. Selection matrix in
`references/house-template.md`. Match the tier of the records already in the directory unless
this decision is genuinely heavier.

**Step 4 — number it.** Next unused four-digit number, zero-padded, filename
`NNNN-kebab-case-title.md`. Two branches picking the same number is normal; the later-merged
branch renumbers, detected at merge time. Never reuse a number, even for a rejected record.

**Step 5 — elicit.** Seven questions, in this order. Missing answers are gaps to report, not
gaps to fill with plausible prose:

1. What forces this now, and what breaks if nothing is decided?
2. What options were genuinely on the table?
3. What was chosen?
4. Why that one — which driver was decisive?
5. Why not each of the others, specifically?
6. What does this cost us, concretely and in the negative direction?
7. What would make this wrong, and who would notice?

**Step 6 — write.** Use the house template at the chosen tier. Fields and their exact meanings
in `references/house-template.md`.

**Step 7 — relate.** Name the typed edges to existing records, and check them against the
validation rules in `references/relationships-and-index.md`. Depending on a rejected record is
an error; depending on a superseded one is a warning that needs a note.

**Step 8 — evidence pass.** Read `references/adr-as-evidence.md`. Name what this decision
blocks or unblocks in the body itself. Every open action point leaves as one typed
`SeedProposal`; the record does not mutate any queue and does not close anything on its own.

**Step 9 — index.** Rebuild the index rather than hand-appending to it. An ADR missing from the
index is an ADR nobody can find, which is the same as not having written it.

**Step 10 — accept, or leave it proposed.** Acceptance needs evidence, not elapsed time — the
bar and the transition rules are in `references/lifecycle-states.md`. A record with unresolved
review comments stays `proposed` with those comments assigned. Then hand the commit or PR text
to `../change-writing/SKILL.md`; a human authorizes whatever is published.

## What this skill never does

It never runs `git add`, `git commit`, `git push`, `gh pr create`, `gh pr edit`, or
`gh pr merge`; never merges, deploys, or publishes; and never treats its own output as
permission for any of those. It writes and reviews decision records, and nothing else.

## Composition

- `../agentic-sdlc/SKILL.md` — its framing step already reads existing ADRs; its reconcile step
  is where a `proposed` record usually becomes `accepted`.
- `../change-writing/SKILL.md` — all commit, PR, and squash text, including for supersessions.
- `../repo-toolchain-gates/SKILL.md` — what a Confirmation line may legitimately point at.

## References

- `references/house-template.md`: the four tiers, the house template at each, every field's
  exact meaning, and where this house format departs from MADR upstream.
- `references/lifecycle-states.md`: the status vocabulary, the one-way transition rules,
  supersession ordering, and what immutability does and does not forbid.
- `references/review-and-antipatterns.md`: the review protocol, the seven-question review
  checklist, and the named creation and review anti-patterns with their tells.
- `references/relationships-and-index.md`: the five typed edges, their validation rules, index
  rebuilding, and the multi-record initiative pattern.
- `references/adr-as-evidence.md`: how an accepted record sits in the authority model, what
  Confirmation and Reversal Condition must contain, and the explicit non-claims.
