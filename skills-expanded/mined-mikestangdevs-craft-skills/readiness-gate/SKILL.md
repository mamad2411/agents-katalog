---
name: readiness-gate
description: "Use at every 'are we ready?' moment — before declaring done, shipping, demoing, or answering 'so everything works?'. Replaces 'should work now' with an evidence-backed go/no-go: what was verified and how, what was not, the spec walked line by line, and the residual risk. Certainty is calibrated to what was actually tested."
---

# Readiness Gate

## The failure mode this fixes

"Done. Should work now." — the most expensive sentence in agent-assisted engineering. The user ships, demos, or builds on top of it, and discovers in production what "should" was hiding. When they come back burned, the trust loss costs more than the bug: now every future "done" gets re-verified by hand, and the agent's leverage collapses.

The root defect is uncalibrated confidence. Agents report completion as a mood ("everything looks good!") rather than a claim with evidence. They answer "are you sure?" with escalating enthusiasm instead of escalating proof. And under pressure to be concise, they truncate exactly the part that matters — the caveats, the unverified paths, the one failing edge they decided was probably fine.

A readiness gate makes "done" a structured claim: **verified / not verified / changed / residual risk / go or no-go.** It's allowed to say no-go. It's *required* to say what it doesn't know.

## When to Use This Skill

- Finishing any unit of work, before reporting it complete
- Before a ship, demo, deploy, or handoff — anything with an audience or a blast radius
- The user asks "are we ready?", "are you sure?", "so everything works?"
- Checking deliverables against a spec, checklist, or requirements doc
- You notice the words "should", "probably", or "looks good" forming in a completion report

**Don't use when:** mid-task on intermediate steps (gates are for boundaries, not every commit), or for trivial changes where the full ceremony outweighs the risk — but even a one-line fix gets one honest sentence of what was and wasn't verified.

## Instructions

### 1. Separate what you verified from what you believe

For every claim in the report, ask: did I *watch this work*, or do I *expect it to work*? Verified means executed and observed — a test run, a live request, a rendered page, a queried row. Everything else is belief, and belief gets labeled as such. "The migration ran clean (verified, 4 rows updated); rollback path is implemented but untested (belief)."

### 2. Verify against the contract, not your memory of it

If there's a spec, checklist, requirements doc, or acceptance criteria — re-read it *now* and walk it line by line against what exists. The most common readiness failure is drift: the work satisfies the plan as remembered, not as written. Items get marked ✅ / ❌ / ⚠️ partial, individually. "We're green on the doc" is only sayable after the walk.

### 3. State what was NOT verified — unprompted

Every gate names the paths not taken: the browser not tested in, the scale not load-tested at, the error path never triggered, the config combination assumed. This is the section pressure tells you to cut. Cut anything else instead. An incomplete verification honestly mapped is useful; a complete-sounding one is a trap.

### 4. Calibrate certainty to evidence

Match the strength of the claim to the strength of the proof. "All 47 tests pass and I ran the live flow twice" earns "this works." A type-check and a reread earns "this should work, unverified at runtime." If the user pushes — "are you absolutely sure?" — the answer is to *add evidence*, not adjectives. Confidence that inflates under social pressure is the thing this skill exists to kill.

### 5. End with a go/no-go and the next risk

Close with the verdict: ready / not ready / ready-except. If no-go: what's missing and the shortest path to green. If go: the residual risk you'd watch first. A gate that can't say no-go is a rubber stamp.

## Output format

```
Readiness gate: <unit of work> against <contract/spec if any>
Verified (executed & observed): <list, with how>
Not verified: <list, with why and risk>
Changed: <surface area of the change — what could be affected>
Contract walk: <n>/<n> items green; exceptions: <list>
Verdict: GO / NO-GO / GO-except-<scoped caveat>
First thing to watch: <the residual risk, named>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| "Should work now" | a belief dressed as a verdict. |
| Confidence inflation | answering "are you sure?" with stronger words instead of stronger evidence. |
| The truncated summary | caveats and unverified paths cut for brevity; the report reads complete and isn't. |
| Memory-walking the spec | checking deliverables against your recollection of the requirements. |
| The rubber-stamp gate | a readiness check that has never once concluded no-go. |

## Mental Model

> "Done" is a claim someone else will act on. The gate is where you decide what you're willing to have them bet on your word — and the only honest collateral is evidence you can show.
