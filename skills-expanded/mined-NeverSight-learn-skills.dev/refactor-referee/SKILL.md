---
name: refactor-referee
description: Two-phase refactoring for hunting, investigating, and resolving refactoring leads.
disable-model-invocation: true
---

Refactor in two phases. **hunt** is read-only and optimizes recall: it finds and clusters suspicious places into **leads**, and touches nothing. **fix** optimizes precision: it takes one lead at a time, investigates until the truth and owner are known, runs the referee, then resolves confirmed leads or names their blockers. The discipline in one line — **a hit becomes a lead only if it is worth inspecting; a lead becomes a change only after fix investigates it and the referee judges it; fix deepens a lead but adopts no unrelated ones.** Understanding a problem happens when you prepare to change it — so HUNT proposes, FIX decides.

FIX carries each confirmed lead to an **honest boundary**; unresolved closure is **blocked**, not disguised as a **patch**.

Optimize for the cost of the *next* change. Judge every structure by its **blast radius**: when the assumption it embeds is wrong, how many places must change? Under-structure spreads an assumption across many sites; over-structure adds a mechanism that bounds no assumption. An AI copies both — so the leverage is the **seam** (where an assumption is contained) and the **first instance** of a pattern (the template that gets copied).

## The referee

The gate from investigation to disposition, run in FIX once a lead's ownership is established — one present-tense question, no appeal to the future:

> **What truth does this own, and is that truth stated anywhere else?**
> copied across places → **extract** · re-states a truth another structure already owns → **delete** · owns a truth stated nowhere else behind an honest boundary → **keep**.

Terms, so the verdict is checkable, not a matter of taste:
- **Truth** — a rule governing behaviour, data format, legal state, or external contract.
- **Owner** — the single structure you would edit to change that rule.
- **Seam** — a boundary a consumer uses without knowing the owner's representation.
- **Honest boundary** — the consumer depends only on the promised capability, not on the implementation, hidden state, or representation behind it.

Run the referee one truth at a time, not one structure at a time — a structure may own several (an overloaded value; a funnel holding a real invariant *and* stray branch rules). Separate them before judging: one truth may be kept while another is extracted or deleted. Each verdict names an ownership move, not a literal code edit — `extract` may split a type or relocate a schema owner, not only lift a helper.

A `keep` may not leave a known inconsistency standing behind a comment: if a truth is enforced unevenly across its inlets, that is `extract` — unify every inlet through the one owner — not `keep`.

Not criteria: caller count, implementation count, or "we might need it." A lone structure is condemned only if it re-states a truth or leaks its boundary. Applied to **unused code**: re-states a truth a newer owner holds → delete; owns nothing → delete; owns a distinct truth behind an honest boundary → keep. A `keep` needs *present* dependence — a test or external contract, a reflection/config/codegen/plugin entry, a public API, or an approved migration citing real references. "Might be needed later" is not evidence; if removal is confirmed but cannot yet close safely, mark it **blocked** like any lead (name the trigger — a date counts).

## Scope contract

Establish and record before hunting, so "the whole scope" is verifiable:
- **Target scope** — dirs/packages/files in play; **off-limits** — generated/vendored/excluded code.
- **Constraints** — public API / compatibility to preserve; which behaviour changes are allowed.
- **Validation** — the commands that check this repo, plus any baseline failures already present.
- **Commit policy** — commit only when the user authorizes it.

## Phase 1 — HUNT (read-only)

Optimize recall: surface everything worth a second look; decide nothing final.

1. **Cover every catalog signal** with a fitting method — text search for textual signals; structural enumeration or relationship tracing for fake seams, god-funnels, mixed concepts, and unowned aggregates. Record method and coverage, including zero hits.
2. **Inspect structural pressure points** — chokepoints, co-traveling values, divergent branches, and cross-flow structures. Use metrics to rank, not judge; account for every candidate with a lead, grouped pattern, or local dismissal.
3. **Cluster into leads** — group hits by a shared suspected truth/owner/pattern; dismiss obvious non-candidates with a local, observable reason; uncertain cases become leads. Sketch ownership where it helps reveal a truth owned twice — owners stay tentative.
4. **Record each lead** — the observable reason it deserves inspection, never a verdict.

Lead table:
```
| ID | Location | Signal | Suspicion | Why inspect |
```
- **Signal** — `A1|A2|A3|A4|B1|B2|B3|B4|unused` from the catalog.
- **Suspicion** — what truth may be duplicated, restated, overloaded, or hidden behind a dishonest boundary.
- **Why inspect** — the observable evidence that triggered it (e.g. "same field validation in two flows"); may group many hits.

**Completion:** every catalog signal checked across the declared scope; every pressure-point candidate accounted for by a lead, grouped pattern, or local dismissal; every lead names why it deserves inspection; no verdicts forced; no file modified.

### Smell catalog (discovery signals — the referee judges later)

| # | Signal | The question it raises |
|---|---|---|
| A1 Duplicated truth | same constant/schema/guard in ≥2 places; "keep in sync with…" | Do these sites really state one rule — and where should its sole owner live (helper, schema/codegen, domain object, parse boundary)? |
| A2 Overloaded name/value | one symbol meaning two things; one literal serving two axes; two id-spaces in one map | Does one name or value carry two concepts that must vary independently? |
| A3 Redundant abstraction | strategy/registry/enum/`mode` mirroring a split a type/union already enforces | Does this mechanism own a runtime truth the type doesn't express (discovery, plugin isolation, lifecycle)? |
| A4 Unowned aggregate | values repeatedly travel together through calls, messages, state, or parallel collections without a named owner | Do these values describe one event, state, or protocol record with an invariant of its own, or are they honestly independent? |
| B1 Fake seam | `instanceof`/downcast; a port whose sole impl is also used directly; a "temp/legacy" path beside the real one | Must the consumer know implementation-specific details to do its job? |
| B2 Variance by branch | `if (mode)`/`if (x == null)` scattered; a nullable collaborator null-checked everywhere | Do these branches belong to one change axis a single owner could absorb? |
| B3 God-funnel | one chokepoint coordinates stages or flows that change for different reasons; branches *inside* tell them apart | What are its independent change axes? Does the funnel own one shared invariant and sequence its phases, or merely route unrelated policy? |
| B4 Leaky invariant | a rule/guard/lock enforced at some inlets but not others; a carve-out held by a comment; an exception with no honest boundary | Is one invariant enforced non-uniformly — can every path route through the single seam that owns it, leaving only explicit exceptions, each owned by an honest boundary with a present-tense reason? |

## Phase 2 — FIX

Enter FIX only when the user asked to fix — up front, or after seeing the leads. If they asked only to find or review, stop at HUNT. When the fix was requested up front, present the lead table once, then work through all leads without pausing for approval.

Take one lead at a time; let understanding mature before you touch code.

1. **Investigate** — follow the call chain, tests, state lifecycle, error handling, and compatibility constraints until the truth, its real owner, the boundary, and the true impact surface are known. HUNT's suspicion is a starting point, not a fact.
2. **Verify, judge, disposition** — first test whether the suspicion is real; **reject** false positives with a specific present-tense reason grounded in inspected code, tests, or contracts, or **merge** leads sharing one root cause. For a confirmed problem, establish the truth and owner and run the referee: **extract/delete** changes it, carried to the honest boundary now; **keep** ends the lead unchanged, recording the present dependence or invariant that earns it; or, when safe closure needs a concrete prerequisite the current authorized scope cannot satisfy (an off-limits surface, a missing dependency or approval, a broken baseline), mark it **blocked** — name the blocker, its owner, and the measurable condition that makes it actionable, and never disguise it with a comment, carve-out, or stopgap. Do not pause merely because the necessary surface grew (that is deepening, §3); seek new authorization only when closure crosses a declared constraint.
3. **Deepen to the honest boundary, don't widen to unrelated leads** — the full surface a lead's honest fix requires (every site of a non-uniform invariant, a fourth path routed through the seam, the callers a move forces to change) IS the fix; expanding onto it is deepening. Widening is adopting *unrelated* smells noticed in passing — leave those for a later hunt. Never read "the necessary surface is large" as "out of scope"; stopping at the small surface leaves a **patch**.
4. **Fix the mold, not the brick** — for a class-wide root cause, make the first instance exemplary, then **encode the rule** mechanically where proportionate — a type that makes the wrong state unrepresentable (e.g. branded ids), a lint, a test, a schema, or generation. Use a naming/partition convention only as a documented fallback, with a stated way to catch violations in review. **Eliminate representable invalid states; guard only real external uncertainty** — before adding a flag, wrapper, retry, timeout, or watcher, name the *present* assumption it bounds and the boundary that owns it. Prefer a type, schema, or ownership move that removes the invalid state outright; real external uncertainty (a network, a crash, a race, untrusted input) is a legitimate present assumption to guard, but a mechanism that merely watches a hypothetical, preserves a carve-out, or compensates for a removable ownership leak is itself a **patch**.
5. **Change cleanly** — a structural slice carries a behaviour-preservation claim (ordering, lifecycle, error propagation, and state semantics unchanged); a lead that turns out to be a real behaviour change or bug fix goes in its own slice, stating old vs new behaviour with a test that fails before the change. Align every reference (docs, comments, dead pointers, symbol/table names), not just what compiles. If honest closure would require touching an off-limits surface or breaking a recorded constraint, don't ship a partial fix — either land a *smaller fix that is itself complete* or mark the lead **blocked**; never leave a **patch**. A smaller fix is complete only if it closes a **separable truth** with its own owner and honest boundary — arbitrarily dividing callers or inlets does not make a sub-fix complete (two of four inlets unified still leaks the invariant). Prefer deletion — a fake seam, dead path, or redundant mechanism is negative value.
6. **Re-referee new structures** — inspect only artifacts and edges introduced or made obsolete by this fix. Remove intermediaries that own no present truth; keep those with a contract or invariant behind an honest boundary. If the original truth remains split, deepen the lead; delete mechanisms that bound no assumption.
7. **Validate to impact** — each slice passes checks matched to its blast radius, adds no new failure against the baseline, and stays coherent and revertible; commit only when authorized.

**Completion:** every confirmed lead, after any merge, was judged one truth at a time before change, and is now **resolved** (carried to its honest boundary), **kept** (justified, no change), **blocked** (named gate, undisguised), or **rejected** (specific evidence-backed reason) — none disguised as a fix; every class-wide root cause encoded its rule mechanically or documented why enforcement is disproportionate; structures introduced or exposed by the fix were re-refereed and own a present truth or were removed; validation is clean relative to the recorded baseline (no new or worsened failures); and a concise plain-prose summary accounts for every lead by ID, explaining what changed and why.
