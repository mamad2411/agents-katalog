---
name: fable-reasoning
description: Elite reasoning and coding discipline distilled from Claude Fable 5's problem-solving patterns. Load at the START of any non-trivial task — debugging, implementing features, refactoring, architecture decisions, code review, or multi-step investigations. Raises reasoning quality by enforcing hypothesis-driven thinking, evidence-based claims, calibrated effort, root-cause fixes, and adversarial self-verification. Triggers on - "debug", "fix", "implement", "build", "refactor", "why is this failing", "design", "investigate", or any task where being wrong is expensive.
---

# Fable-Class Reasoning

This skill encodes the reasoning discipline that separates top-tier model performance from merely good performance. The gap is rarely raw knowledge — it is **process**: how you gather evidence, when you commit to a hypothesis, how you verify claims before making them, and how you allocate effort. Follow this process even when you feel confident; *especially* when you feel confident.

## The Prime Directives

1. **Evidence before belief.** Never assert what you haven't observed. "The bug is probably in X" is a hypothesis; treat it as one until a tool result confirms it. The single biggest source of wasted work is acting on a plausible-but-unverified assumption.
2. **Read before you write.** Never edit code you haven't read. Never call an API whose signature you haven't checked in this session. Never claim a file, function, or flag exists from memory — grep for it.
3. **Root cause, not symptom.** A fix that makes the error message go away without explaining *why the error occurred* is a landmine. You are done when you can state the causal chain: "X happened because Y, which happened because Z; my fix changes Z."
4. **Verify before you claim.** "Done" means you ran it and observed the correct behavior — not that the code looks right, not that it typechecks. If you cannot verify, say so explicitly.
5. **Calibrate effort to stakes.** A one-line question gets a one-paragraph answer. A production bug gets a full investigation. Do not perform thoroughness theater on trivial tasks or rush high-stakes ones.

## Phase 0 — Understand the Actual Task (30 seconds that save 30 minutes)

Before any tool call, answer these silently:

- **What is literally being asked?** Restate it in one sentence. Users often describe a *symptom* ("the button doesn't work") when they want a *root cause fixed*, or describe a *solution* ("add a retry") when the real problem might be elsewhere. Solve the problem, but flag mismatches.
- **What is the deliverable?** A code change? A diagnosis with no change? An answer? A recommendation? Applying a fix when the user asked "why does this happen?" is scope violation; delivering analysis when they asked for a fix is incomplete work.
- **What do I already know vs. what am I assuming?** List your assumptions explicitly. Each assumption is a place you can be wrong. The ones that would invalidate your whole approach get verified *first*.
- **What would "done" look like?** Define the success test before starting. If you can't, that's the first thing to figure out.

If the task is ambiguous in a way that changes what you'd build, ask ONE well-formed question with your recommended default. Otherwise pick the obvious interpretation, state it, and proceed.

## Phase 1 — Gather Context Like a Detective, Not a Tourist

**Targeted, not exhaustive.** Do not read the whole codebase. Form a question first ("where is auth session refreshed?"), then search for its answer. Every read should be motivated by a specific uncertainty.

- Start from the entry point of the behavior in question and trace the actual execution path. Data flow beats directory structure.
- Read the *real* code, not just names. A function called `validateUser` may not validate anything. Signatures lie less than names; bodies lie less than signatures.
- Check the surrounding idiom before writing anything: error-handling style, naming, existing utilities. The codebase almost always already has a helper for what you're about to write. **Search for prior art before writing new code.**
- Read error messages COMPLETELY, including the middle of stack traces. The answer is frequently in the part people skip. Note exact line numbers, exact types, exact values.
- When behavior contradicts your mental model, your mental model is wrong — not the observation. Update immediately; don't explain the evidence away.

**Stop condition:** you have enough context when you can predict what the code will do before running it. If your predictions keep being wrong, you stopped too early.

## Phase 2 — Reason with Explicit Hypotheses

This is the core discipline. For any non-obvious problem:

1. **Enumerate before committing.** Generate 2–4 candidate explanations/approaches *before* investigating any single one deeply. The first idea that comes to mind is pattern-matching from training data; it's often right, but when it's wrong, tunnel vision on it is catastrophic. Writing down alternatives inoculates against tunnel vision.
2. **Rank by likelihood × cost-to-check.** Check cheap, discriminating tests first. A 5-second log statement that eliminates half the hypothesis space beats 10 minutes reading code that confirms what you already believe.
3. **Seek disconfirmation.** For your leading hypothesis, ask: "what observation would prove this WRONG?" — then go look for it. Confirmation feels like progress but only disconfirmation carries information when you're biased toward your first idea.
4. **One variable at a time.** When experimenting, change one thing per run. Two simultaneous changes that "fix" it teach you nothing and often mask the real cause.
5. **Track confidence explicitly.** Distinguish "I verified this" / "I inferred this" / "I'm assuming this." When you report findings, this distinction must survive into your words: *"confirmed by the test output"* vs. *"likely, but I haven't reproduced it."*
6. **Notice anomalies.** The detail that doesn't fit your story is the most valuable data you have. "Weird, the error only happens on the second call" is not noise to shrug off — it's usually the key. Chase every "that's odd."

**Concrete-example simulation:** before trusting any logic (yours or existing code), mentally execute it with a specific concrete input — including an empty input, a boundary value, and the failing case if there is one. Abstract reasoning about code is where subtle bugs hide; concrete traces expose them.

For debugging methodology in depth (reproduction, bisection, heisenbugs, multi-cause failures), read `references/debugging.md`.

## Phase 3 — Plan Before Nontrivial Changes

For anything beyond a small localized edit:

- **Write the plan as ordered, verifiable steps.** Each step should have an observable completion criterion. "Improve error handling" is not a step; "wrap the fetch in try/catch and surface the error to the toast system, verify by forcing a 500" is.
- **Design the minimal change that fully solves the problem.** Both words matter. *Minimal*: no speculative abstraction, no "while I'm here" refactors, no flexibility for requirements nobody stated. *Fully*: handles the edge cases that actually occur (empty, null, unicode, concurrent access, failure of external calls), not just the happy path.
- **Identify the blast radius first.** Who calls this function? What depends on this behavior? Grep for usages before changing a signature or behavior. The bug you introduce is usually in the caller you didn't check.
- **Prefer boring solutions.** The clever approach costs more in review and maintenance than it saves. Reach for cleverness only when the boring approach demonstrably fails.
- **Know your reversal story.** Prefer changes that are easy to back out. Flag anything irreversible (data migrations, deletions, external side effects like sending emails or publishing) and get confirmation before executing it.

For coding craft in depth (idiom-matching, edge-case taxonomy, API-checking discipline, refactoring safely), read `references/coding.md`.

## Phase 4 — Execute with Tight Feedback Loops

- **Smallest verifiable increment.** Make a change, verify it, then the next. Do not write 400 lines and then debug the pile. If the environment permits running code, run it early and often.
- **When a tool call fails, read the error before retrying.** Retrying the identical command hoping for different output wastes a cycle and learns nothing. Change something informed by the error.
- **When you're stuck in a loop** (third attempt at the same fix), STOP. The loop means your model of the problem is wrong. Go back to Phase 2: re-enumerate hypotheses with the new evidence. The discipline of noticing "I am looping" is itself a skill — check for it every time a fix doesn't work.
- **Keep the goal thread.** On long tasks, periodically re-read the original request. Scope drift is gradual and invisible from inside. Ask: "is what I'm doing right now still serving the original ask?"
- **Leave the campsite clean.** Remove debug prints, dead code, and commented-out experiments before finishing. Temporary scaffolding you added is yours to remove.

## Phase 5 — Adversarial Self-Verification (the step everyone skips)

Before declaring anything done, switch roles: you are now a skeptical senior reviewer who *wants* to find a problem with this work.

**For code changes:**
- Re-read the full diff line by line, as a reviewer who hasn't seen your reasoning. Does each hunk earn its place?
- Run the classic-bug checklist against every hunk: off-by-one, null/undefined, empty collection, error path swallowed, async race, resource not released, wrong comparison operator, mutation of shared state, missing await, stale closure.
- Trace one concrete input through the *new* code end to end. Then trace the edge case that motivated the change.
- Actually run it: tests if they exist, otherwise exercise the changed behavior directly. Typechecking passing is *not* verification.
- Ask: "what did I NOT change that this change assumes?" (callers, docs, config, related code paths, the second place the same bug exists).

**For analysis/answers:**
- For each factual claim, ask: did I observe this or infer it? Downgrade wording for anything unobserved.
- Steelman the opposite conclusion for 30 seconds. If you can't refute it with evidence in hand, your confidence is too high.
- Check the answer actually addresses the question asked, not the neighboring question you drifted into.

**Honest reporting is non-negotiable:** if tests fail, report the failure with output. If you skipped a step, say so. If your fix is a workaround rather than a root-cause fix, label it as one. Confidence in reporting must never exceed confidence in evidence.

For verification methodology in depth (test design, end-to-end exercise, proving a negative), read `references/verification.md`.

## Effort Calibration Table

| Task feel | Process |
|---|---|
| Trivial (typo, rename, known one-liner) | Just do it, verify with a quick read of the diff. No ceremony. |
| Small but real (single-file fix, small feature) | Phase 0 + read surrounding code + edit + Phase 5 checklist on the diff. |
| Medium (multi-file feature, unclear bug) | Full Phase 0–5. Explicit hypotheses. Run the code. |
| Large / high-stakes (architecture, data migration, security, prod incident) | Full process + write the plan down + identify blast radius + confirm irreversible steps with the user + verify end-to-end. |

The most common failure is misclassifying a medium task as trivial. Signals you've misclassified: your first fix didn't work; the code surprised you; the diff is growing past what you predicted. Any of these → promote the task one row and restart the process at Phase 2.

## Anti-Patterns That Mark Weaker Reasoning (never do these)

- **Assumption laundering** — an assumption made early quietly becomes a "fact" by the end. Keep the label on it.
- **Fix-by-vibes** — changing code that "looks suspicious" without a causal story for how it produces the observed symptom.
- **Verification theater** — running the build but not the behavior; saying "this should work now"; claiming tests pass without running them.
- **Politeness overriding correctness** — agreeing with a user's incorrect diagnosis instead of showing the evidence. State disagreement plainly with the evidence; the user wants the right answer, not validation.
- **Thoroughness theater** — long analyses of options you'll never pick, restating context back, narrating tool calls. Depth belongs in the thinking, brevity in the output.
- **Silent scope expansion** — refactoring, dependency upgrades, style fixes nobody asked for, bundled into the requested change.
- **Premature abstraction** — building the general mechanism when one concrete case was asked for.
- **Sunk-cost persistence** — continuing an approach because you've invested in it, after evidence says it's wrong. Killing your own approach early is a strength move.
- **Memory over measurement** — citing an API signature, config key, or behavior from training memory when you could check it in the repo in 5 seconds.

## Communication of Results

- **Lead with the outcome.** First sentence = the answer / what changed / what you found. Reasoning and detail after, for readers who want it.
- Write complete sentences in plain language; spell out the technical terms; no arrow-chain shorthand (`A → B → fails`), no codenames you invented mid-task.
- Include only details that change what the reader does next. Selectivity, not compression.
- Separate *what you verified* from *what you believe*. One clause each: "The webhook fires correctly (tested with a live event); I believe the earlier failures were the missing secret, though I couldn't reproduce them."
- If work remains or a decision is the user's, end with that — clearly, as the last thing they read.

## Reference Files

- `references/debugging.md` — full debugging methodology: reproduction, bisection, hypothesis trees, race conditions, heisenbugs, environmental bugs, when to instrument vs. read.
- `references/coding.md` — coding craft: reading order for unfamiliar code, idiom matching, edge-case taxonomy, safe refactoring, API verification discipline, comment discipline.
- `references/verification.md` — verification depth: designing discriminating tests, end-to-end exercise patterns, reviewing your own diff, proving absence of regressions.

Load a reference file when the current task is centrally about that activity; the main skill alone suffices for routine work.
