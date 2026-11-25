---
name: design-it-twice
description: Produce and compare divergent designs for a consequential, hard-to-reverse software interface or seam using isolated parallel design subagents. Use from talk-it-through only after constraints and factual unknowns are known, or standalone when first-solution anchoring would be costly.
---

# Design It Twice

Explore genuinely different interfaces before a consequential technical choice is committed. This
is a decision aid, not implementation. Do not edit repository files or select a product preference
on the user's behalf.

This workflow adapts the Design It Twice mechanism documented in Matt Pocock's engineering skills
and applies it without an issue tracker.

## Applicability gate

Run only when all are true:

1. the decision creates or materially changes an important public, module, service, platform, data,
   or provider interface;
2. the decision is hard to reverse after callers or persisted data depend on it;
3. at least two credible designs remain after repository conventions and factual research; and
4. the result could materially change coupling, invariants, error handling, compatibility, testing,
   or task boundaries.

Skip local helpers, routine implementation, small visual choices, speculative extensibility, and
anything existing conventions already settle. Return `not-applicable` with the reason instead of
manufacturing alternatives.

## 1. Frame the decision

State:

- the exact decision to make;
- current behavior and callers;
- constraints and invariants every design must preserve;
- dependencies and trust boundaries;
- ordering, concurrency, persistence, compatibility, and error requirements;
- test and integration seams;
- relevant repository paths or durable source documents; and
- which facts are verified versus still uncertain.

If a factual unknown could invalidate every design, return to research before continuing. Show the
frame to the user, then proceed unless they correct it.

## 2. Generate divergent designs in isolated context

Run three isolated design subagents in parallel using the environment's available mechanism. Give each
the same decision frame and a different binding optimization constraint:

1. **Smallest interface** — minimize entry points and maximize behavior hidden behind the seam.
2. **Maximum flexibility** — support credible variation without speculative generality.
3. **Simplest common caller** — make the dominant use case obvious and difficult to misuse.

Add a fourth ports-and-adapters design only when the seam crosses a platform, process, provider, or
other trust boundary. Do not ask subagents for cosmetic variants of the same interface. Each subagent must
inspect the relevant repository evidence directly and return only its structured proposal.

## 3. Compare without voting

Validate every proposal against the common constraints. Compare them on:

- interface depth and leverage;
- caller simplicity and misuse resistance;
- locality of future change;
- invariants and legal operation ordering;
- failure and error semantics;
- dependency direction and adapter placement;
- persistence, migration, or compatibility cost;
- testability at stable behavioral seams;
- operational and security consequences; and
- reversibility.

Reject a proposal that violates a hard constraint rather than averaging it into a hybrid. A hybrid
is valid only when its combined pieces preserve one coherent set of invariants and are simpler than
the alternatives.

## 4. Recommend, then ask one question

Present each valid design concisely, followed by the comparison and one opinionated recommendation.
Ask the user one question at a time: whether to accept the recommendation or choose a named
alternative. If the user identifies a new constraint, update the frame and rerun only when that
constraint materially invalidates the proposals.

Return a compact decision record to the caller:

```markdown
### <Decision name>
- **Selected design**: <choice, or Unresolved>
- **Interface and invariants**: <decision-rich summary>
- **Why**: <trade-off>
- **Alternatives rejected**: <name and decisive reason>
- **Consequences**: <planning, testing, compatibility, migration, or risk constraints>
- **Evidence**: <paths and research artifacts>
```

`talk-it-through` passes this record to `write-planning-brief`. Do not create tasks or
implementation code.
