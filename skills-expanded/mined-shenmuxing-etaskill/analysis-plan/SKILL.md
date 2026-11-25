---
name: analysis-plan
description: Turn a theory-first research idea into a proof-oriented research plan. Use after idea-creator-analysis, or when the user asks for theorem targets, assumptions, proof obligations, impossibility routes, analysis validation, or a non-experimental plan.
---

# Analysis Plan

Convert a selected idea into a compact, auditable theory plan. This is the analysis-side counterpart to `experiment-plan`: the deliverable is a proof and validation roadmap, not a GPU run matrix.

## Output

Write:

```text
idea-analysis-stage/ANALYSIS_PLAN_<YYYYMMDD_HHMMSS>.md
idea-analysis-stage/ANALYSIS_PLAN.md
```

When called from `idea-discovery-analysis`, fold the summary into that workflow's canonical report and keep the plan file as the detailed artifact.

## Workflow

1. **Freeze the research object.** State whether the work targets a theorem, counterexample, lower bound, convergence/sample-complexity result, unification, or diagnostic principle.
2. **State the minimal formal setup.** Define objects, assumptions, algorithm class, and comparison baseline. Mark missing definitions as gaps instead of filling them silently.
3. **Draft the claim stack.** Separate core claim, supporting lemmas, optional extensions, and nonclaims.
4. **Run formal sanity checks.** Check boundary cases, constrained domains, and nonstandard equalities. A plan that fails here should be reframed as a counterexample, diagnostic theorem, or weaker inequality before continuing.
5. **Build proof obligations.** For each lemma, list the input facts, desired conclusion, likely proof lever, and failure mode.
6. **Add disproof paths.** Explain what counterexample or obstruction would invalidate the idea and whether that failure would still be publishable.
7. **Run independent stress review.** Prefer `deepseek-agent` for adversarial proof-route critique when available. Ask it to find circular reasoning, hidden assumptions, and known prior work.
8. **Define acceptance gates.** The plan passes only if the core claim is precise, the novelty delta is defensible, the proof obligations are locally checkable, boundary regimes are coherent, and the strongest failure mode is understood.

## Plan Template

```markdown
# Analysis Plan

## Research Object
<theorem / counterexample / lower bound / unification / diagnostic>

## Minimal Setup
- Objects:
- Assumptions:
- Compared methods or quantities:
- Nonclaims:

## Core Claim
<one precise statement shape>

## Formal Sanity Checks
- Boundary regimes:
- Constrained-domain issues:
- Nonstandard equalities:
- Known-framework overlap:

## Proof Obligations
| Obligation | Desired conclusion | Inputs | Proof lever | Failure mode |
| --- | --- | --- | --- | --- |

## Disproof and Negative-Result Value
<smallest counterexample family and why it matters>

## Novelty Delta
<closest work and exact difference, with verification status>

## Independent Review
<DeepSeek critique path, verdict, and unresolved objections>

## Acceptance Gates
- [ ] Core claim is formally stated.
- [ ] Assumptions are explicit and not stronger than the contribution needs.
- [ ] Boundary cases are meaningful or split into separate claims.
- [ ] Nonstandard equalities are proved facts or explicitly marked as lemma candidates.
- [ ] At least one proof route is non-circular.
- [ ] Closest prior work is checked or marked `[UNVERIFIED]`.
- [ ] Failure mode is publishable or bounded.
```
