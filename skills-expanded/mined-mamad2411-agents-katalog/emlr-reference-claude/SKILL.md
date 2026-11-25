# CLAUDE.md — emlR2

Project-level guidance for Claude Code working on this repository.

## What this project is

An R implementation of the EML (Exp-Minus-Log) Sheffer operator from
**Odrzywołek (2026), arXiv:2603.21852**. The paper proves that a single
binary operator `eml(x, y) = exp(x) − ln(y)` together with the constant `1`
generates all elementary functions. This package operationalises that result
for symbolic manipulation, symbolic regression, and pedagogical exploration
in R.

A v1 prototype already exists in `reference/emlR-v1/` and is **correct but slow
and architecturally limited** — it uses a custom nested-list AST that
duplicates work R's parser and `call` system already do for free. v2 fixes
this by re-grounding the representation in native R AST objects, adding a
peephole simplifier with the paper's identities as rewrite rules, and
compiling to RPN bytecode for batched evaluation.

## Author context

The user is Philipp, a Senior Data Scientist with strong R + Python ML
background. He uses R idiomatically (tidyverse, lavaan, ggplot2, Deriv) and
expects code that respects R conventions: S3 methods over switch/dispatch,
`call`/`name` objects over parallel ASTs, `deparse`/`bquote`/`substitute`
over string manipulation, vectorisation over loops. He has read the paper
and the v1 prototype; he doesn't need either re-explained.

He runs R locally and will execute tests himself. Do not attempt to run R
from this environment if R is unavailable — fall back to careful symbolic
tracing as the v1 prototype did.

## Invariants

These properties must hold throughout. If a change would violate one of
these, stop and surface it as a question rather than break the invariant.

**I1. Mathematical correctness over uniformity.** The paper's beautiful
property is that every node is identical. Practical R code does not need
to preserve this at runtime — it needs to *be able to* preserve it (for
the master formula and the SR search space). The simplifier may break
EML-uniformity to produce a fast execution plan; the canonical tree must
remain available for inspection.

**I2. Three identities are sacred.** These are stated verbatim in the
paper and must round-trip exactly through any simplifier:
- `eml(x, 1)` ↔ `exp(x)`
- `eml(1, 1)` ↔ `e`
- `eml(1, eml(eml(1, x), 1))` ↔ `log(x)` (paper Eq. 5, K=7)

If `simplify(canonical_form_of(log))` does not yield `log(x)` literally,
the simplifier is wrong. This is also the package's primary correctness
check — every catalog identity, when canonicalised then simplified, must
collapse to its native R primitive.

**I3. Complex-domain semantics on the principal branch.** Trig functions,
π, and i all require `log(-1) = iπ`. Any evaluation path must coerce
through `as.complex()` or use a complex-aware code path. R's default
`log(-1)` returns `NaN`; this is wrong for EML. See `eml()` in
`reference/emlR-v1/R/01_core.R`.

**I4. Extended-real semantics matter.** Several constructions use
`log(0) = -Inf` and `exp(-Inf) = 0`, e.g. `−1 = exp(log(0)) − log(exp(1))`.
R complex arithmetic gets this right; do not "fix" the resulting `-Inf`
intermediate values without checking the paper's §4.1.

**I5. The SR master formula must remain complete.** Aggressive
simplification that escapes the EML grammar would produce a faster
evaluator but a *smaller* SR search space than the paper's completeness
proof guarantees. The compile pipeline must therefore have two modes:
"strict" (stays inside EML, used for SR training) and "fast" (uses
native R primitives where pattern-matched, used for inspection and
verification).

**I6. No silent semantic changes.** When refactoring v1 → v2, the test
script in `reference/emlR-v1/tests/test_eml.R` must continue to pass on
the new implementation, modulo the API surface change to native R AST.
Add a compatibility shim if needed.

## What v2 must deliver

In priority order:

1. **Native R AST representation.** EML expressions are R `call` objects
   with the function name `eml`. Free interop with `deparse`, `bquote`,
   `substitute`, `all.vars`, `Deriv::Deriv`, `eval`.
2. **Peephole simplifier** with rewrite rules drawn from the paper's
   identity chain (Fig. 1), implemented as pattern-matching on call
   objects. Two modes: `simplify_eml()` (stays in EML) and
   `simplify_native()` (collapses to base R primitives).
3. **RPN bytecode compiler** producing a flat instruction vector + constants
   table for batched evaluation. The instruction set is documented in
   `SPEC.md` §4. Evaluation is a single tight R loop over instructions
   operating on whole vectors of input.
4. **Symbolic differentiation pipeline.** Take a master formula expression,
   substitute parameter symbols, call `Deriv::Deriv` w.r.t. each parameter,
   evaluate analytic gradient at current parameter values. This replaces
   the v1 SANN fitter with L-BFGS-B and should give ≥100× speedup.
5. **Test suite** covering: every catalog identity round-trips, the SR
   master formula recovers `log(x)` at depth 3, simplifier idempotence,
   bytecode evaluator agrees with `eval()` on randomized trees.

## What v2 must NOT do

- Do not introduce non-base-R dependencies beyond `Deriv` (which is on
  CRAN, lightweight, and already familiar to the user). No tidyverse,
  no Rcpp, no torch — those are appropriate for v3 if we ever need them.
- Do not silently rename functions from v1. If an API change is needed,
  document it in a `NEWS.md` and provide a deprecation shim.
- Do not "improve" the canonical identities by replacing them with K-shorter
  forms invented on the spot. The paper's K-optimal trees came from
  exhaustive search; the v1 constructions are not optimal but are
  *correct* and *traceable*. Keep them. If a shorter form is desired,
  cite the source (paper Table 4 row, or independent derivation with proof).

## Workflow

Phased plan in `IMPLEMENTATION_PLAN.md`. Each phase has explicit
acceptance criteria. **Do not move to the next phase until the current
phase's tests pass.** If a phase's tests reveal a design flaw, stop and
surface it — do not patch around it silently.

When a test fails, the default action is to investigate why, not to weaken
the test. The tests encode invariants; if a test is genuinely wrong, fix
the test in a separate commit with a clear justification.

## Style

R style follows the user's existing codebase conventions:
- Roxygen doc comments on every exported function (`@export`, `@param`,
  `@return`, `@examples` where short).
- S3 dispatch via class attributes, not `switch(type, ...)`.
- snake_case throughout.
- 80-column soft limit, 100 hard.
- No `magrittr` pipes; native `|>` only if it improves clarity.
- Comments explain *why*, not *what*. The code says what.

## Reference materials

- `reference/emlR-v1/` — v1 prototype (correct, slow, custom AST)
- `reference/emlR-v1/README.md` — design notes from v1
- `SPEC.md` — full v2 technical specification
- `IMPLEMENTATION_PLAN.md` — phased plan with acceptance criteria
- `TESTS.md` — test catalog with expected values
- `REFERENCES.md` — paper, related implementations, derivations

The paper itself: https://arxiv.org/abs/2603.21852
