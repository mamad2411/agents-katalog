---
name: econ-debug
description: "Diagnose unexpected estimates, sample changes, or computational results in economics research."
---

# Economist Debugging Workflow

Determine whether a surprising research number is wrong, and correct an evidenced implementation error when repair is authorised. The object under investigation is a research result — an estimate, a realised sample, a diagnostic, a computed model object — not application code. This file is the contract; it adapts the ce-debug diagnosis loop to research anomalies.

## Core principles

- **Investigate before fixing.** Support the diagnosis with a reproducing example and a causal explanation that distinguishes the leading alternatives before changing the live analysis.
- **One change at a time.** Test one hypothesis and change one thing. Changing several things "to see what helps" hides which change mattered and is how a symptom patch masquerades as a cause.
- **Observed beats assumed.** Assumed values lie; a printed count, a `describe`, or a boundary check does not. Ground every hypothesis in something you actually observed.
- **When stuck, diagnose why.** After two or three exhausted hypotheses, stop and read the pattern — different subsystems implicated, contradictory evidence, an environment or vintage mismatch — rather than trying harder along the same line.

## Trigger

Invoke on an anomalous empirical or computational output: a sign flip against theory or a prior run, an observation-count cliff, an implausible magnitude, unexplained pre-trends, a broken identity or accounting residual, a convergence or feasibility failure, a failed object-defining check, or a plain "this number can't be right". If the request is a pure software fault with no estimate, sample, or output at stake, hand it to the Compound Engineering debug skill (`compound-engineering:ce-debug` when available) and stop.

## Diagnosis and repair authority

A surprising sign or magnitude is not itself a bug. Trace the anomaly through the relevant data construction, specification, estimation, or numerical steps. “The coefficient looks right after this edit” is not evidence of a repair. State what the evidence establishes and what remains uncertain; do not demand impossible certainty or conceal an unexplained step.

Use reversible tests on isolated copies to discriminate between hypotheses before changing the live analysis. Label a candidate fix as a hypothesis until the reproduction and affected checks support it.

Present the diagnosis in economic terms before applying a repair: what changed in the research object, why it produced the anomaly, the supporting file or output locations, and the minimal correction and validation.

When the user or authorised parent already requested a fix, apply a supported, reversible implementation correction within that authority without another permission menu. A diagnosis-only request remains diagnosis-only. Ask before changing an intended baseline, estimand, sample rule, benchmark, identification strategy, or other researcher-owned choice, or before an unauthorised costly rerun or destructive overwrite. In a parent run, return an unresolved research choice to the parent rather than deciding it silently.

## Assumption audit

Before forming hypotheses, identify the consequential assumptions behind the surprising output and mark each **verified** (you read the code, checked the state, or ran it) or **assumed**. Most stuck debugging is a correct hypothesis tested against a wrong assumption. Cover the relevant parts of:

- the **sample rule** — which rows the active filter actually keeps, and whether it matches the intended population;
- **merge cardinality** — one-to-one, one-to-many, or many-to-many, and whether a silent many-to-many inflated the panel;
- **weights** — which weight is applied, whether it is the intended one, and whether any step drops or renormalises it;
- **timing** — event, treatment, and reference dates; period alignment; lead/lag construction;
- **estimator settings** — fixed effects, clustering level, absorbed terms, reference category, optimiser tolerances, standardisation;
- **data vintage** — which extract, build, or version produced the inputs, and whether it is the one you think.

Verify cheapest-first: a one-line count or a `describe` before a full rerun.

## Hypotheses

Rank hypotheses by likelihood. Each must carry a concrete testable prediction — something in another slice of the data or code that must also hold if the hypothesis is right. For example: "if the merge duplicated firms, the raw panel row count exceeds the register firm count by roughly the number of duplicated keys"; or "if the sign flip is an omitted reference-category change, dropping the new control returns the old sign". A prediction that fails while the fix appears to work means you found a symptom. When the chain is obvious and gapless (a mis-typed variable, a filter with a flipped inequality), the chain explanation is itself the gate — no prediction ritual.

## Escalation by research subsystem

Localise the anomaly to the subsystem that produced it, then investigate there:

- **data construction** → transformation and sample diagnostics: recompute row counts before and after each merge and filter, missingness and support, key uniqueness, denominator and weight construction.
- **specification or estimation** → the model specification and estimator settings: fixed effects, clustering, absorbed terms, reference categories, standardisation, optimiser tolerances, and whether the realised specification matches the intended one.
- **software convention** → cross-package defaults: a default that differs between Stata, R, Python, or a solver (degrees-of-freedom corrections, small-sample adjustments, base levels, NA handling, integer vs float division). Reach for the `software-equivalence` lens — rebuild the disputed object in a second language and compare — when a convention gap is plausible.
- **genuine economics** → the number may be real and surprising. Do not fix it away: write a surprise memo and return the evidence boundary and next research decision to the user.

If several hypotheses fail, reassess the evidence and identify the next discriminating check. Failure to localise a bug is not evidence that the research design is wrong. Route to `econ-plan` only when the evidence reveals an actual design or definition choice.

## Reproduce minimally

Build a minimal script that reproduces the anomaly on the smallest input that still shows it — one merge, one estimator call, one slice — and keep it. Run it before the fix (it must reproduce) and after (it must be gone for the stated reason). After fixing, refresh every audit the change touches: sample counts, missingness, merge diagnostics, and any object-defining check on the affected output family. A fix that leaves stale audits behind is not closed.

## Questions

Read the relevant request, plan, definitions, and code before asking whether the observed behaviour was intended. Ask only when that cannot be resolved from the evidence and the answer changes the diagnosis or repair authority. Use `request_user_input` when available, otherwise ordinary chat. Explain the economic consequence and your recommendation; do not repeat answered questions or turn routine debugging into an approval interview.

## Exits

- **Fix applied** → verify the changed surface and refreshed audits, then report the diagnosis and evidence. Do not automatically invoke `econ-review`; return to a formal review only when the user explicitly selected it or an already-authorised end-to-end caller includes it.
- **Design problem discovered** → the anomaly is a wrong baseline, estimand, sample definition, or benchmark, not a coding slip. Route back to `econ-plan`; a fix cannot repair a definition.
- **Genuine surprising finding** → the number is real. Route to the surprise-memo path in `econ-work`: write the memo (HTML via `econ-html-memo` when installed, plain standalone HTML under the same content discipline otherwise), state the minimal validation and open explanation, and ask only for the research decision or local check needed to continue.

## Hard stops

- Do not apply an unsupported fix to the live analysis or present a hypothesis as a confirmed diagnosis.
- Do not fix a number without first reproducing it minimally, and do not close without refreshing the sample counts, missingness, and merge diagnostics the change touched.
- Do not "fix away" a result that is actually a genuine, correctly computed finding — write the surprise memo and report it locally instead.
- Do not treat an intended baseline or a deliberate sample restriction as a bug — when in doubt, ask first.
- Do not change more than one thing at a time while hunting the cause; shotgun edits hide which change mattered.
- Do not route a pure software fault with no research object here; it belongs to `compound-engineering:ce-debug`.
