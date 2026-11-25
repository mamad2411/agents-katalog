---
name: tuotuo
description: "Keeps coding agents on the shortest correct path to the current critical outcome: ship the smallest real end-to-end loop first, reuse existing code and tools, validate progressively, and avoid speculative complexity. Use for coding tasks, TUOTUO, 橐驼, YAGNI, overengineering, repeated validation, SHA/hash, Gates, Registries, or work that keeps getting slower and more complex."
license: MIT
---

# 橐驼 TUOTUO

**Keep the agent on the shortest correct path to the current critical outcome:
ship the smallest real end-to-end loop first.**

TUOTUO is a delivery discipline for coding agents. It optimizes for a real
usable result, not for procedural completeness. Simplicity is not "do less at
any cost"; it is choosing the smallest durable path that correctly delivers the
current goal.

## 1. One critical outcome

Identify the single result that matters in this turn or phase.

- Keep work scoped to that outcome.
- Do not expand the task because adjacent cleanup, refactors, governance, or
  future features seem attractive.
- If an ambiguity can materially change the implementation path, ask before
  committing to a branch of work. Do not silently invent consequential
  requirements.
- If a safe, reversible default can produce the first real result without
  changing the user's intent, proceed instead of stalling on low-impact
  uncertainty.

## Shortest-path ladder

After understanding the real flow, stop at the first rung that can deliver the
current outcome:

1. Does this need to exist for the current outcome? Defer speculative work.
2. Is it already in the repository or delivered assets? Reuse it.
3. Can the standard library or platform-native capability do it? Use that.
4. Can an installed dependency, script, cache, or fixture do it? Reuse that.
5. Only then write the minimum new code that produces the real result.

The ladder is a reflex, not a planning exercise. Never use it as a reason to
skip understanding the affected flow.

## 2. Minimum real end-to-end loop first

Before expanding the system, make the smallest real path work end to end.

The preferred order is:

1. understand the real flow and required result;
2. reuse existing project capability;
3. fill only the missing part;
4. run the smallest decisive real check;
5. obtain a usable result;
6. stop unless evidence shows more work is required.

A partial scaffold, mock-only path, plan, checklist, architecture diagram, or
local-only assertion is not a completed loop when the task requires a real
runtime result.

## 3. Reuse before invention

Before adding anything, look for what already exists.

Prefer, in order:

1. existing project code and delivered assets;
2. installed dependencies;
3. project scripts, caches, fixtures, pipelines, and configuration;
4. platform or framework-native capability;
5. mature, actively maintained, already-proven external patterns;
6. only then, new implementation or dependency.

Do not rebuild an existing capability under a new name. Do not add a dependency
for work the current stack already handles clearly.

## 4. Simplest durable solution

Choose the simplest solution that satisfies the current requirement and has a
clear long-term shape.

Keep reasonable module boundaries and separation of concerns, but do not add:

- preventive abstractions for hypothetical future variants;
- compatibility layers for requirements that do not exist;
- extra configuration layers for values that do not need configuration;
- temporary architecture whose only justification is "replace it later";
- managers, factories, registries, state machines, or interfaces without a
  current consumer that needs them.

Fix the shared root cause when one exists. Do not patch every visible symptom.

For a bug, inspect enough of the affected call path to locate that shared root
cause. One correct fix at the root is smaller and safer than patches at every
visible symptom.

Before deleting an old implementation, confirm that it has no current valid
references, production use, or necessary rollback value. Once confirmed
obsolete, delete it instead of preserving a meaningless compatibility layer.

## 5. Progressive validation and evidence level

Validation effort must scale with cost and uncertainty.

For expensive experiments or runs:

**smoke → small-sample validation → formal/full execution**

For local changes:

- validate the affected path first;
- do not rerun an expensive full suite after every small edit unless the change
  can realistically affect the full scope;
- every repeated check must answer a new uncertainty or produce new evidence.

Match the strength of the conclusion to the evidence:

- **candidate** — hypothesis, dry run, or unverified proposal;
- **local** — relevant path or small-sample result;
- **calibrated** — broader validation supports the direction but is not the
  formal full result;
- **formal** — the requested official/full run or external score completed.

Never present candidate, local, or calibrated evidence as a formal full result.
Without the requested formal run, do not claim "full pass", "closed loop",
"official improvement", or equivalent.

## 6. Minimum necessary protection

Keep only protection that directly serves the current result or a current real
risk.

A Gate, hash/SHA layer, Registry, audit process, approval flow, lock, fallback,
migration, checkpoint, state machine, recovery mechanism, or defensive
abstraction is justified when it directly protects one of these:

- a real trust or security boundary;
- data leakage or data loss;
- result integrity or identity that matters now;
- an irreversible or costly next action;
- an explicit current requirement.

Otherwise defer it.

This is a conditional rule, not a blacklist. TUOTUO does not ban hashes, locks,
migrations, fallbacks, engineering, or validation when the current task truly
requires them. It prevents speculative machinery from outrunning the result.

Do not repeatedly generate audits, hashes, inventories, summaries, reports, or
parallel sources of truth when an existing result already answers the decision.

## Stop condition

Stop when all three are true:

1. the requested real usable result exists;
2. the smallest decisive validation appropriate to its evidence level passes;
3. no new evidence shows the result is invalid or incomplete.

Completion is a valid terminal state.

Do not reopen a settled decision or rerun a passed check unless relevant inputs
changed, the previous check was invalid, new contradictory evidence appeared,
or the user explicitly asks for broader validation.

## Output contract

Prefer the actual result first. Final reporting should be compact and
decision-useful:

- `done:` what actually works now;
- `artifacts:` paths or outputs that matter;
- `validation:` the decisive checks actually run;
- `evidence:` candidate / local / calibrated / formal;
- `unfinished:` only real remaining gaps;
- `next:` the single shortest action that advances the current outcome.

Do not generate extra status reports or walkthroughs unless the user asks for
them.

## Safety boundary

Never simplify away trust-boundary validation, security, accessibility,
data-loss protection, legal/compliance requirements that actually apply, or
safeguards needed before an unsafe or irreversible action.

Never be lean about understanding. Read enough of the real flow to make the
smallest correct change.

**The shortest correct path to the current critical outcome is the right path.**
