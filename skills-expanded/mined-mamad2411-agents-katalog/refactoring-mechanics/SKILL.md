---
name: refactoring-mechanics
version: 1.0.0
description: Safe, behavior-preserving transformation technique — characterization tests as a safety net, finding seams, small verified steps, and a catalog of standard low-risk transformations. Use whenever software-engineer restructures existing code without intending to change its behavior. Do NOT use for deciding what to modernize and in what order (that is `legacy-modernization`) or for tracking and prioritizing debt (that is `technical-debt-management`) — this is the moment-to-moment mechanics once the decision to change is made.
---

# Refactoring Mechanics

## The definition that matters
Refactoring is a behavior-preserving transformation. If the observable behavior changes, it isn't a refactor — it's a feature change or a bug fix wearing a refactor's name, and it needs the scrutiny that comes with actually changing behavior (requirement tracing, test design for the new behavior), not the lighter scrutiny appropriate to "this should do exactly what it did before, just structured differently."

## Prerequisite: a safety net
Never refactor code with no tests and no way to add them safely first. Before restructuring:
- If tests exist and cover the behavior, they're the safety net — run them before, after every step, and at the end.
- If they don't, write **characterization tests** first: tests that pin down what the code *currently* does, not what it *should* do. These aren't a design statement — they're a tripwire that fires if the refactor accidentally changes behavior. Write them, confirm they pass against the current code, then refactor.
- If characterization tests can't be added safely (the code has hidden side effects, external dependencies, or nondeterminism that make it hard to pin down), that's a stop condition, not a reason to refactor blind — say so explicitly rather than proceeding without a net.

## Finding seams
A seam is a place you can alter behavior without editing the code at that exact spot — usually by substituting a dependency, injecting a different implementation, or intercepting a boundary. Seams are how you get legacy code that resists testing under a characterization test without a large rewrite: find the narrowest seam that lets you observe or control the behavior in question, rather than restructuring broadly just to make the code "more testable" first.

## Small steps, verified continuously
- Each individual transformation should be small enough that if something breaks, it's obvious which step broke it.
- Run the safety net after every step, not just at the end. Batching several transformations before verifying turns "which of these five changes broke it" into its own debugging problem — see `debugging-methodology` for how expensive that search gets, and note that batching refactoring steps is exactly how you lose the ability to bisect over them.
- Commit (or otherwise checkpoint) after each verified-green step where practical — it turns "revert to the last known-good state" into a cheap, mechanical action instead of a manual reconstruction.

## A short catalog of standard safe transformations
Extract function/method; inline function/variable; rename (symbol, file, module); move function/class to a different scope or module; extract interface/protocol from a concrete implementation; introduce a parameter object to replace a long parameter list; replace a conditional with polymorphism or a lookup table; consolidate duplicate conditional fragments; replace a magic value with a named constant.

Each of these has a mechanical, low-risk way to perform it — the risk in refactoring almost always comes from combining several of these at once or skipping the safety-net check between them, not from any one transformation itself.

## When not to refactor right now
- No safety net exists and one can't be added safely in the time available — flag it and defer, don't proceed blind.
- The business urgency genuinely doesn't allow verifying each step — that's a signal to do a smaller, more targeted change instead of a broad restructuring, not a reason to skip the discipline on the restructuring you do attempt.
- The "refactor" is actually motivated by a behavior change in disguise — split it into the actual behavior change (with its own requirement tracing and test design) and any genuine structural cleanup, rather than blending them into one diff where a test failure could mean either "the refactor broke something" or "the intended behavior change has a bug," with no way to tell which from the failure alone.
