---
name: architecture-first-implementation
description: "Implement a feature, bug fix, or refactor after checking its architectural fit. Use for issues, legacy tickets, or direct coding requests that need decisions about component responsibilities or interfaces. Plan, implement, and verify against focused acceptance cases. Do not use for issue writing, planning-only requests, repository audits, or mechanical edits."
---

# Architecture First Implementation

Before editing code, establish the product benefit, required outcome, and architectural approach. Then implement and verify the change. Match planning and testing effort to the scope and risk.

## Establish the purpose

Read the request, applicable repository instructions, and relevant product context. Read the issue and relevant discussion when an issue is supplied. Inspect the working tree before editing. Preserve unrelated changes.

Identify the product benefit, required outcome, constraints, and acceptance criteria. Separate requirements from suggested implementation details. Distinguish verified facts, assumptions, and unresolved decisions. Do not invent a product strategy when only the immediate benefit is known.

Use the available input:

- For a clear issue, reuse its purpose, architectural reasoning, and acceptance cases. Verify assumptions that affect the implementation against the current code. Do not repeat settled planning without evidence of a problem.
- For a legacy or incomplete issue, establish the missing purpose from the request, relevant discussion, documentation, and code. Separate observed behavior from evidence of intended behavior. Propose missing acceptance cases before coding.
- For a direct request, use the same reasoning without requiring an issue. Keep the working plan in the conversation unless the user or repository requires a document.

Resolve routine implementation choices within the authorized scope. Ask a focused question when missing information prevents a sound decision about required behavior, an interface contract, or scope. Continue independent work while awaiting the answer. Wait for the answer before making a decision that depends on it.

Do not require an issue rewrite, a new design document, or a separate planning approval merely to start implementation. Do not post or edit an issue unless authorized.

## Inspect the affected architecture

Trace the affected behavior through its callers, responsible components, and dependencies. Read enough surrounding code and tests to identify where the change belongs. Inspect data flow, state ownership, lifecycle, error handling, and external contracts only where they affect the decision.

Use established repository patterns when they fit. Do not duplicate behavior that an existing component already provides. If an existing pattern causes the problem, explain the specific conflict and make a scoped correction.

Choose the smallest coherent change that meets the goal. Evaluate simplicity by the resulting design and maintenance effort, not only the number of edited lines. Keep responsibilities clear and avoid unnecessary dependencies between components.

Preserve useful future options through clear boundaries. Do not implement hypothetical features to prepare for them. Add abstractions, configuration, versioning, compatibility layers, or migration tools only for a demonstrated requirement. Preserve required compatibility with external callers and stored data.

Compare alternatives only when a real tradeoff affects correctness, scope, or maintenance. Do not generate several designs for an obvious local change. Stop architectural investigation when the evidence supports a coherent approach and no unresolved decision prevents implementation.

## State the implementation plan before coding

Give a concise plan that connects these points:

1. **Why:** The problem and the product benefit.
2. **What:** The required outcome, responsible components and affected interfaces, and reason for the architectural choice.
3. **How:** The concrete changes and any sequence that matters.
4. **Validation and completion:** Acceptance cases, required checks, exclusions, and sufficient evidence to stop.

For a small change, a few sentences can cover these points. For work across components, explain the relevant interactions and contract changes.

State which changes are outside scope and which checks add no value. Keep these exclusions specific to the task.

If the code conflicts with an issue's proposed method, explain the evidence and adapt the method within the stated requirements. Do not silently weaken requirements or acceptance criteria to fit the code. Seek clarification when resolving the conflict would change the requested outcome or scope.

## Define acceptance cases and validation limits

Reuse supplied cases when they are adequate. Add missing cases only for required outcomes or concrete risks. Each case must state a starting condition, action or trigger, expected result, and verification method. Use a compact list or table when useful.

Prefer observable behavior to internal implementation details. Identify existing tests that already provide sufficient coverage. Add focused regression tests when they protect the changed behavior. Do not require a new automated test for every case or for a reversible, low-impact change that a direct check adequately verifies.

Include relevant failure and recovery behavior when the change affects it. Use concrete evidence to justify cases for persistence, authorization, concurrency, or compatibility. Do not expand testing to every possible combination.

Identify the required repository checks and review gates. Verify commands from the repository rather than inventing them. Apply required documentation checks when documentation changes.

Use the acceptance cases and required checks to determine whether verification is sufficient. Do not substitute an arbitrary time limit, test count, or coverage target. Do not add new test infrastructure when existing tools can verify the outcome.

## Implement the chosen approach

Proceed from the plan into the authorized code changes. Do not stop after producing a plan when the user requested implementation.

Keep each change connected to a required outcome. Update affected callers, tests, and documentation together. Remove obsolete paths when replacement is authorized and compatibility does not require them. Avoid unrelated cleanup and speculative improvements.

Use focused checks during implementation when they help catch a concrete failure. Do not run a full validation cycle after every small edit unless the repository requires it.

Revisit a decision when new evidence invalidates it. Explain the new evidence and revise only the affected part of the plan. Obtain authorization before expanding the requested scope.

Treat incidental findings separately unless they prevent the required outcome.

## Verify and stop

Run the acceptance checks and required repository checks. Inspect the final diff for scope errors, unintended behavior changes, and disagreement with the chosen design. Correct concrete failures and rerun affected checks.

Expand or repeat validation only for a relevant code change, a failure, a mandatory check or review, or an identified unresolved risk. State why the extra check is needed and what result will resolve the concern.

Stop when acceptance cases pass, required checks and review gates are satisfied, and no known defect prevents the intended outcome. Complete any remaining authorized delivery steps, such as creating a pull request.

If required verification cannot run, report the specific blocker and remaining check. Continue useful work that does not depend on the blocked check. Do not claim full completion or substitute unrelated tests for missing evidence. Preserve applicable authorization boundaries for commits, pull requests, merges, and deployment.

Report the resulting behavior, the architectural choice that matters, the verification performed, and any limitation that affects the outcome. Keep the report proportional to the work. Use short, direct sentences and active voice. Use consistent technical terms. Avoid contractions, idioms, promotional language, and "should" for requirements or recommendations.
