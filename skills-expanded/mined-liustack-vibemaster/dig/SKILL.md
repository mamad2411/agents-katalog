---
name: dig
description: Cross-domain root-cause diagnosis for bugs, data mismatches, metric anomalies, and recurring problems, found before touching a fix. Use when the user says 查不出原因 / 有时好有时坏 / 数对不上 / 指标掉了 / 为什么又坏了 / 反复出现 / 改了还是不行 / 一直报错 / dig into this / debug this / why does this keep failing. Do not trigger for concept-explanation whys (why-is-the-sky-blue knowledge questions), first-time errors with obvious messages (the error already states the fix), known-cause fixes (coding's job), or debugging the harness session itself (built-in /debug's job).
---

# dig: cross-domain root-cause digging

Iron rule: **no fix before the root cause is found.** Making the symptom disappear and solving the problem are two different things. This rule applies to every kind of anomaly: code, data, metrics, process.

Repeated failure is the entry signal: a fix that did not fix ("改了还是不行", still failing after changes) means the guessing phase is over. Stop patching from memory and start here. The cause-known boundary runs the other way: when the cause is already understood, skip this skill and take the fix straight through coding's red path. Diagnosis, source fix and regression all complete inside this skill, no forced handoff.

Diagnosis is a thinking activity, and each step is driven by a thinking engine: what an engine gives you isn't terminology, it's **the question that step should ask**.

The deliverable of a non-trivial dig is `.issues/<YYYY-MM-DD-topic>/issue.md`: the symptom and reproduction, the hypothesis list with a verdict on each, the probe log, the root-cause reconciliation, the fix, and the regression line. Create it when the dig starts, append as verdicts land. When the user wants it published, rewrite it from the confirmed understanding into issue or PR text, never by copying the working file. Before writing to disk, make sure the draft directory is ignored: if `git check-ignore .issues` fails, append `.issues/` to `.git/info/exclude` (a local ignore, leaving the shared `.gitignore` untouched) and let the user know. In a non-git environment there's no commit risk, so write directly. This file is three things at once: the vehicle for showing the user the hypothesis list, the counter for the three-strikes stop-loss, and the working memory for picking the investigation back up if the session gets interrupted. Small, obvious problems can skip it, but a dig entered through repeated failure never does: this file is the three-strikes counter, and a problem that already survived two fixes is not small.

## 1. Reproduce and pin down the symptom

Turn the anomaly into something you can observe with certainty: for a code problem, build a minimal, repeatable reproduction. For a data problem, take the raw data and compute it yourself. For a metric problem, pin down the exact definition and time window. If you can't reproduce it, keep gathering observations, don't start fixing. A flaky symptom is a reproduction-rate problem: loop the trigger, parallelise, add stress, narrow the timing window until the rate is high enough to debug against. A 50% flake is debuggable, a 1% one is not, so raise the rate first.

**What counts as "fixing"**: only a change that alters behavior counts. Read-only probes, diagnostic scripts, and pure scaffolding added for testability (exporting a function, wrapping a `main` guard, as long as you verify zero behavior change) don't count, and don't need to clear the hypothesis gate.

## 2. Generate hypotheses: the first-principles engine

Don't ask "what similar bug have I seen before" (pattern matching is fertile ground for anchoring). Ask instead: **"For this symptom to be true, what facts have to hold?"** Break the symptom into a chain of necessary conditions. Every link in that chain is a suspect, and every suspect generates a hypothesis.

- Write each hypothesis in falsifiable form: "If it's this, I'll see X. If it isn't, I'll see Y." If you can't state a falsification condition, it isn't a hypothesis, it's a hunch.
- Run "known information" through the same three-state fact check: what a log said, what the user reported secondhand, what a comment claims: is it a verified fact, or an unverified proposition? Contaminated "knowns" are the deepest trap.
- **The full list has to show up in visible output before you start fixing.** Thinking it through internally doesn't count. List it item by item, show it to the user, and let them challenge your direction (you can keep going without waiting for a reply, but the list itself can't be compressed into one throwaway line).
- Proportionality: when the answer is nearly obvious, the list can shrink to 2-3 items (the leading hypothesis plus the strongest alternative), but step 4's root-cause reconciliation and step 5's item-by-item verification are **never exempted, regardless of scale**.
- One hypothesis class is always on the list: **your understanding of a dependency is stale, or the bug is already known.** What a library actually does is a fact to verify (installed source, docs matched to the installed version, its issue tracker and changelog), not a memory to trust. On a repeated failure this is the first hypothesis to check, because it is the cheapest to settle.
- For a recurring problem, put "how it got fixed last time" on the suspect list too: the root cause is often a loop, where the fix itself is feeding the problem.

## 3. Gather evidence: falsify first, one variable at a time, walk the flow upstream

- **The inversion engine**: for each hypothesis, design the observation that would **falsify it fastest**, rather than one that would support it. Confirming evidence can be collected without limit. One counterexample settles it.
- **Single-variable discipline**: one probe changes exactly one variable. Change two things at once and the symptom shifts, and you've learned nothing. Tag every debug log with one unique prefix, so cleanup at the end is a single grep: untagged logs are the ones that survive into production.
- **External evidence is a probe too, often the cheapest one**: search the exact error message, check the dependency's issues and changelog for the installed version, read the installed source instead of assuming behaviour. Read-only, zero side effects, and a known-bug hit settles a hypothesis instantly. Not searching because "this is a local problem" is a guess about the answer, not a fact about it.
- **The systems engine**: an anomalous value is the output of some production chain: walk upstream along the data flow (output ← computation ← input ← source), placing an observation point at each boundary, until you find the handoff where "correct" turns into "wrong."

## 4. Root-cause reconciliation: the bias firewall stands guard

Confirmation bar: **the evidence has to precisely explain the symptom's magnitude and shape.** If the gap is 75, you need to find the 30 and the 45 that add up to it. Anything that doesn't explain the whole symptom is half a root cause. Go back to step 2 and add hypotheses.

Before declaring a root cause, run the firewall: am I verifying the hypothesis, or defending it (confirmation bias)? Did I pick this hypothesis because of the evidence, or because I saw something similar recently (availability bias)? Have I actually looked for a counterexample?

## 5. Fix, and hold the regression line

- Fix the source, not the point of consumption. When several places need the same kind of protection, fix the data contract or unify the boundary instead.
- Before a code fix, write a failing test that pins down the bug, watch it fail, then watch it turn green once the fix lands. And ask one question before landing it: under what conditions would this fix turn out to be wasted work? If that condition is live, the root cause is not settled yet.
- Verify with an item-by-item reconciliation, not just "the totals match": two sides can each be wrong by an equal and opposite amount and still match.
- **Ask a second-order question**: what shared behavior does this fix change? Who depends on the part being changed? (Blast radius doesn't get a pass just because this is a bug fix.)

## 6. Three strikes, then stop, and the meta root cause

If the same symptom **fails three landed fixes** (probes and redos sent back by single-variable discipline don't count toward this), or every fix spawns a new problem: stop. Don't attempt a fourth. What's wrong is probably not a single line, it's your understanding of the architecture, the data flow, or the problem itself: go back to step 1 and rebuild your understanding, or lay the evidence and the blocker on the table for the user.

Before closing out, ask one more layer of meta root cause: **why was this bug even possible?** Which line of defense was missing (types, contracts, tests, review) that let it slip through: closing that gap is worth more than fixing this one bug.

Then look at what's left. The missing defense the meta root cause named is settled build work: it goes through coding's loop. A remediation the dig revealed to be bigger than the bug (architecture, data model) is an unsettled design question: take the issue.md to shaping. Nothing left: close, don't invent a next step.

## Non-code scenarios

The same loop applies with different words. Reproduce = get the raw data or the complete timeline. Hypotheses fall into four categories (a change in definition, a change in channel, a change in structure, or a genuine change), rule out the statistical-distortion ones first. Probe = a request for evidence that can distinguish between hypotheses. Reconcile = the magnitude adds up. Fix = act on the cause, not on the metric: a metric recovering doesn't mean the problem is solved, so ask first why the metric recovered.

## Red flags: stop the moment these thoughts show up

| Thought | Reality |
|---|---|
| "Let's just try changing this" | A change with no hypothesis behind it is a lottery ticket: even a win doesn't tell you why |
| "Get the numbers to match and it's shippable" | You're fixing the report, not the problem. Faked figures will blow up somewhere else eventually |
| "Add a retry or a fallback and it'll be stable" | Papering over a failure upgrades a random fault into a silent one |
| "I've got the hypothesis list in my head, no need to write it out" | A hypothesis that's never shown escapes every challenge, including your own |
| "Let's try this direction one more time" (the fourth try) | That's three strikes. What's wrong is your understanding, not your technique |
| "That error is too weird, just work around it" | The weirdest error is the one closest to the root cause. Working around it throws away your best lead |
