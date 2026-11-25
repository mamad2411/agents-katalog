---
name: scientific-debugging
description: Hypothesis-driven debugging method — reproduce, isolate, bisect, prove the cause before fixing. Apply whenever observed behavior differs from expected behavior. Independent of project, language, and domain.
---

# Scientific debugging

A bug is a gap between what you observe and what you expected. Debugging it means explaining that gap with a **proven** cause — not making it disappear. A symptom that vanishes without explanation is not a fixed bug, it's a hidden bug.

## 1. Before searching: pin down the facts

**Write the gap in one factual sentence.** "When I do X, I observe Y; I expected Z." If you can't fill in all three slots, you don't have a bug yet — you have an impression. Go get the three first.

**Reproduce before explaining.** Until you have triggered the bug yourself, you're working on a story, not a fact. A bug you can't reproduce can't be fixed — it gets trapped (logs, instrumentation) until it becomes reproducible.

**Shrink the reproduction to the minimum.** Remove everything that can be removed while the bug persists: data, steps, options, dependencies. Every element removed without making the bug disappear is exonerated; every element whose removal makes the bug disappear is a suspect. The minimal reproduction IS already half the diagnosis.

**Read the error message literally.** Word for word, including the file name, the line number, the error code, and the *first* error in the stack — not the last one, which is often just a consequence. The classic trap: reading what you expect the error to say instead of what it says. If a term in the message is unknown to you, look it up before forming any hypothesis.

**Establish "since when".** Did it ever work? If so, what changed between when it worked and now — code, dependency, environment, data, configuration? A regression is searched for in the *delta*, not in the whole system.

## 2. Searching: hypotheses and bisection

**Form hypotheses BEFORE touching the code.** Two or three plausible causes, each written with its testable prediction: "if it's A, then by doing T I should observe O". A hypothesis without a prediction is not a hypothesis, it's an intuition — unusable.

**Test the cheapest hypothesis first**, not the most seductive one. A hypothesis eliminated in 30 seconds beats a brilliant hypothesis that needs an hour of setup.

**Change ONE variable at a time.** If you change two things and the behavior changes, you don't know which one acted — you burned a trial and polluted your reasoning. Return to the reference state between trials.

**Bisect the space of causes.** Every test should cut the remaining space in half, whatever the dimension: in time (which version introduced the bug), in code (does the bug survive if I short-circuit this half of the path), in data (does the bug persist with half the input). Ten bisections cover a thousand suspects; ten random checks cover ten.

**Look at the actual state, not the assumed state.** Print the effective values at the point of interest: what goes in, what comes out, what is configured, which version is actually running. Half of all "incomprehensible" bugs are a gap between the system you think you're observing and the one that's running: wrong environment, non-invalidated cache, old deployed version, unsaved file. Check THAT point first when nothing makes sense.

**When nothing makes sense, question your certainties, in order.** List what you hold as given ("this function is called", "this file is the one being loaded", "this value is what I think it is") and verify them one by one, from the most fundamental to the finest. The bug always lives in a box labeled "obvious, no need to check".

**Keep a log of your search.** For any investigation beyond a few trials, keep a written trace: hypothesis → test → result → verdict. Without a trace, you will re-test the same hypothesis twice and call it perseverance.

## 3. Fixing: the cause, not the symptom

**Demand a complete explanation before fixing.** You must be able to tell the causal chain end to end: "X triggers Y, which produces Z, which yields the observed symptom". If a link stays fuzzy ("and there, for some reason…"), you're not done searching.

**A fix that works without you knowing why is a failure.** If the symptom disappears after a change you can't tie to your causal chain, don't stop: either your theory is wrong, or the bug is masked and will come back. Remove the fix, verify the bug returns, put it back, verify it leaves — if that back-and-forth isn't clean, you fixed nothing.

**Fix at the level of the contract, not the symptom.** Forbidden, except with explicit and documented justification:
- the magic value that compensates for a wrong calculation elsewhere;
- the special case added to silence the failing example;
- the retry / sleep that "stabilizes" a concurrency problem you don't understand;
- the try/catch that swallows the error instead of preventing it.

Each of these gestures turns a loud bug into a silent one — an aggravation, not a fix.

**Hunt the bug's siblings.** Does the cause you found exist elsewhere? The same pattern copied, the same API misused, the same false assumption on another path. A found bug is a free detector: run the code through the same filter before closing.

**Add the test that would have caught the bug.** The test must fail on the code from before and pass on the code from after — verify both. A test written after the fact that never failed proves nothing.

## 4. Knowing when to stop

**Give each lead a budget.** If a hypothesis withstands several tests without being confirmed or eliminated, it is badly posed: reformulate it or change leads. Grinding on a single lead is the most common failure mode — it looks like work.

**Escalation is a deliverable.** If the investigation runs dry, deliver a structured report: exact symptom, minimal reproduction, hypotheses tested with their verdicts, what remains open and what information is missing. That report has value; "I didn't find it" has none. Whoever picks up after you must be able to start from your eliminations, not redo your search.

**Never "fix" by accumulation.** If you catch yourself stacking changes "to see what happens", stop everything, return to the clean reference state, and start over at section 1. A system riddled with exploratory modifications is harder to debug than the original one — you are manufacturing a second bug.
