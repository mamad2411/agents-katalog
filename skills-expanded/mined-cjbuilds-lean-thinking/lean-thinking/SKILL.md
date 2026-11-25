---
name: lean-thinking
description: Plan and execute implementation work with proportionate evidence, the smallest complete change, risk-based verification, and a firm stopping point. Use when building, fixing, changing, or reviewing a system where overplanning, speculative work, rebuilding, or incomplete validation could waste effort or weaken the result.
---

# Lean Thinking

Measure twice, cut once: understand the requested outcome and the actual system well enough to choose one sound path, implement it completely, verify it, then stop.

## Scale the work

Match the process to the task. For a simple, reversible edit with an obvious result, inspect the target, make the change, and check it directly. Do not create ceremony, extensive research, a multi-stage plan, new abstractions, or extra tests merely because this skill is active.

For substantive or risky work, inspect the relevant code, data, tests, configuration, and current behavior before editing. Gather evidence that could change the implementation; stop researching once the requirements and execution path are clear.

Preserve the user's explicit outcome, constraints, compatibility needs, and approval boundaries. If an uncertainty would change the scope, public contract, destructive effect, or required authority, clarify it before committing to that path. Resolve reversible implementation details with judgment and state only assumptions that materially affect the result.

## Make one sufficient plan

Choose one implementation path and define, as briefly as the work allows:

- the observable outcome;
- what is outside scope;
- the smallest files or components that must change; and
- the checks that will prove the result.

The plan is sufficient when it covers the requested behavior, likely failure paths, and material risks. It is excessive when it adds alternate implementations, future-use frameworks, unrelated cleanup, speculative features, or research that cannot change the decision.

## Implement the whole requirement

Reuse the existing flow, helpers, dependencies, and conventions. Change the fewest coherent parts that solve the root problem. Add an abstraction only when the current requirement has a real second use or explicitly calls for one. Remove a superseded path unless compatibility requires it.

Small scope does not excuse missing work. Include error handling, data integrity, security, accessibility, migration behavior, or compatibility when the requested change actually depends on them. If evidence shows the chosen path is wrong, revise the plan instead of stacking workarounds on it.

## Verify by risk, then stop

Run the narrowest check that observes the changed behavior and its relevant failure path. For integrated or consequential changes, also run the existing type, build, integration, or end-to-end checks needed to prove the real flow. Do not substitute a shallow unit check for a user-visible path, and do not add tests that merely restate the implementation.

When the acceptance checks pass, the requested flow works, and the diff contains no unrelated work, stop. Report the outcome, checks performed, and any real limitation. Do not keep polishing, redesigning, or manufacturing extra assurance after the result is established.

## Calibration examples

**Excessive work:** A request adds one optional field to an existing form. The agent introduces a form framework, a generic schema layer, and a new test harness. A sufficient change follows the existing form pattern, updates the actual validation and submission path, and runs the relevant form test.

**Missing work:** A database column becomes required. The agent changes the application type and sees the type checker pass, but ignores existing rows and deployment order. Sufficient work inspects the schema and rollout path, handles existing data as required, and tests the migration or equivalent failure risk.

**Sufficient work:** A CLI needs a `--json` flag. The agent traces argument parsing and output, adds the flag through the existing parser, preserves the default text output, tests both formats and invalid input, updates the usage documentation, and stops when those checks pass.
