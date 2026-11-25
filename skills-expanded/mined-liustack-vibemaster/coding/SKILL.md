---
name: coding
description: Development discipline from plan to green. New behaviour and known-cause fixes go red-green-refactor with the failing test watched red first, pure refactors go green-to-green with no manufactured red, and how-should-I-write-this questions get verified against current sources before answering. Use when the user says 写个新功能 / 修个 bug / implement this / 重构这段 / TDD / 该不该先写测试 / 这个 API 现在的推荐写法 / 你确定吗 (a correction right after a code change). Do not trigger for unknown-cause anomalies (dig's job), unsettled requirements (shaping's job), pure config or docs edits, or explaining concepts.
---

# coding: plan, then the right loop

The bar for every line of code written here is **current best practice**: what is recommended and adopted today, not just an answer that runs. "It runs" and "this is how you should do it today" are different claims, and only meeting the first is how code ships resting on yesterday's idiom.

Every writing path starts with a plan, sized to stakes. A trivial change plans in one sentence, in your head. A design-level change plans in `.issues/`. When shaping is installed, it is the planner for those: hand the unsettled requirement there, come back with the spec, and skip straight to red. Without it, plan inline. The plan itself may or may not land on disk, the stakes decide. Planning includes verification: version-sensitive practice (API, CLI, config, idioms) gets checked against an authoritative source before use, never written from memory. Official docs and the repo's own conventions outrank blog posts and recall.

## Dispatch

| Request | Path |
|---|---|
| New behaviour, or a bug whose cause is known | Failure list → red → green → refactor |
| Pure refactor | Prove the baseline green → refactor → green again. No manufactured red |
| "How should I write this now" | Verify against current sources → answer |
| Anomaly with unknown cause | Not this skill. `dig` finds the cause first |

## Verification, the judgment not the reflex

The bar applies to every line of code. What varies is where memory can be trusted to meet it: actively verify on version-sensitive ground (a library's API surface, CLI flags, config schemas, anything deprecated-or-not, any question that contains "best practice"), because that is where confident recall goes stale first. Skip verifying stable knowledge (algorithms, settled syntax), facts sitting in the project (read them), and what the user already specified (use it).

Search freely, and often first: it is frequently the fastest move. The source order below is about which answer wins when they conflict, not about earning the right to search. The project itself outranks everything, installed source, lockfile and changelog are the exact version in effect. Then official docs, version-matched to what is installed. Then the open web, read with discipline: recency and version beat search ranking, primary sources beat confident blogs, cross-check before committing, and never phrase the query to confirm what you already believe. When practices conflict, battle-tested survival beats benchmark results beats claims. When there is a lot to verify, send a background subagent rather than skipping.

A verified conclusion that supports the plan lands in the task document with its source attached.

## Red, green, refactor

**Red.** Before implementation code, a failing test exists, and you watch it fail. Paste the red output: it is the auditable evidence, and red is the test for the test itself. A test that never went red might be vacuously true, might test the wrong thing, might never have run.

Test behaviour through the public interface, never internals: a test that breaks on a refactor with no behaviour change was testing the implementation, and it is exactly what makes "tests untouched" in the refactor step possible. Test cases come from a failure list, not from the implementation. With a spec, translate each acceptance criterion into a test. Without one, list 3-5 ways the change would count as broken (the new behaviour works, the old behaviour does not regress), then translate them one at a time: one scenario, one red test, the minimal green, the next scenario. Do not batch a pile of tests up front.

**Green.** The minimal implementation that passes. No drive-by refactors, no drive-by features. Writing against an external API you have not touched this session: confirm the current interface first, not from memory.

**Refactor.** With everything green, improve the structure. Behaviour unchanged, tests untouched. If a test had to change, that was not a refactor. Refactor toward today's idiom, not the one in memory: yesterday's best practice is often today's anti-pattern.

When a test written after the fact passes on its first run, temporarily break the corresponding implementation path, watch the test go red, then restore. A test that cannot be made to fail no matter how you break the implementation is a bad test: delete it and rewrite.

Where subagents exist and a spec exists, hand the acceptance criteria to an independent context that cannot see the implementation, and let it write the tests. The question-writer has nothing to copy from, so its tests encode what the code should do rather than what it did.

## Pure refactor

A behaviour-preserving change has no failing test to write, so do not manufacture one. The discipline is green-to-green: run the suite and see it green before touching anything, refactor, see it green again. A refactor without a green baseline is a rewrite with extra steps.

## Review

After refactor, before done: an adversarial pass over the diff. The reviewer's job is to find what blocks the merge, not to confirm it can.

Where subagents exist, hand the diff to a fresh context that did not write it. Implementer blindness is bias (confirmation, sunk cost, overconfidence), not a capability gap, and a fresh reviewer beats any declared stance. It gets the diff, the intent (spec, commit message), and the three lenses. Without subagents, declare the stance switch and re-read at tool level: pull the diff again, check history, enumerate callers. Never judge from the memory of writing it.

Three lenses. Every deletion: why did the removed thing exist, verified via history and callers, "cleanup" is a claim not evidence. Every new abstraction: born of the problem, or of the implementation path? Every change: who calls it beyond the diff, because the diff shows what changed, never what it affected. And one currency check: nothing new in the diff leans on a deprecated API or a superseded idiom.

With acceptance criteria present, check them item by item, strict on "satisfied" and honest on "unverifiable", and report that separately from lens findings: merged into one ranking, one axis masks the other.

Findings severity-ranked, no nit-padding. Nothing found under all three lenses: say so plainly, citing what was checked.

## Corrections

After a correction (are you sure, that's wrong, 又错了), stop re-answering from memory. The memory that just produced the wrong answer cannot be trusted to produce the right one. But classify before reacting, the signal says something is wrong, not what:

- **Understanding error** (did the wrong thing, misread the ask): reread the requirement and the context. It is the cheapest check, so start here when unsure.
- **Knowledge error** (wrong API, outdated idiom): verify against the source order above.
- **Repeated failure** (the fix did not fix): stop guessing, that is `dig`'s entry signal.

## Exemptions, by risk not by count

Skip the loop only when failure is low-risk and recoverable, and say so out loud. Running once is not the criterion: a data migration runs once and can still destroy data, so it gets the full loop. Config edits skip TDD but not verification, confirm the change took effect. A spike ends one of exactly two ways: promoted to real code with tests, or labelled throwaway and deleted.

## Done

Green is the floor, not the bar. Three claims, checked in order: it runs (every failure scenario has a matching test and all pass, lint clean, no untracked TODOs), it is not outdated (nothing leans on a deprecated API), and it is how you would write it today (idiomatic per current practice). Code most easily ships wrong at the top of that stack: it runs, so it merges, resting on yesterday's idiom. "Ran it by hand once" is a smoke test: it leaves no regression line.

## Silent exit

A request this loop does not fit (a pure config touch, a docs edit, a question already answerable) gets completed directly. Zero ceremony, no mention of this skill. When it cannot be told whether the loop applies, it does not.

## Red flags

| Thought | Reality |
|---|---|
| "Finish writing it, then add tests" | A test written after the fact asks what the code did. A test written before asks what it should do |
| "Too simple to need a test" | Simple code breaks too. If it genuinely is not worth testing, take the exemption and say so out loud |
| "I already checked it by hand" | That is a smoke test. See Done |
| "The user is pushing for progress" | Rushed is exactly when gates drop. Red-to-green is also the fastest proof that it is actually done |
| "I remember how this API works" | Version-sensitive recall is how stale idioms ship. Verify |
