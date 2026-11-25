---
name: self-healing-fallbacks
description: Use when an AI workflow has to survive a model that fails, stalls, or answers with low confidence instead of shipping a confident wrong answer - when they say "what happens when the model is down", "it gave a fluent wrong answer", "the API timed out and the whole thing broke", "a pilot user hit a dead end and stopped trusting it", "we need a fallback", "it should never guess on a dose/allergen/threshold", or an agent looped and burned tokens at 3am. Produces a fallback map for each critical path (trigger, fallback behaviour, escalation) and the confidence thresholds that fire them. Invoke after eval-and-safety-harness, with design-the-mva.
stage: ship
function: engineering
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# Self-Healing Fallbacks

Your workflow sits behind an API, and that API will sometimes be slow, down, or wrong. The failure that quietly kills pilots is not a crash; it is a confident wrong answer, or a dead end a user hits twice before going back to doing the job by hand. You did not lose them on capability. You lost them on reliability. Self-healing without a hard limit is just an infinite loop in a nicer coat, so the discipline is to retry within bounds, reroute within bounds, then fall to a fixed, boring, non-AI path that cannot guess fluently on a dose, an allergen, or anything irreversible.

## The method

Map each critical path to a pattern, size what to automate, set the threshold that fires the floor. Full framework: [`references/fallback-patterns.md`](references/fallback-patterns.md). Source: Handbook [Chapter 09](../../handbook/09-designing-the-mva.md).

### Step 1: List the critical paths and their reversibility
For each path the workflow depends on, write what it touches and whether a wrong answer can be undone. Reversibility, not value, decides how hard the fallback must be.

| Path touches | Reversibility | Fallback hardness |
|---|---|---|
| A screenshot, a draft, a suggestion | Fully reversible | Retry, then best-effort, log it |
| A stored record, an outbound message | Partly reversible | Retry, reroute, then conservative default |
| A dose, an allergen, a threshold, a trade, a release | Irreversible | No guess ever: deterministic floor + named human |

### Step 2: Choose the pattern per path
Pick from the catalogue by risk and reversibility. The full decision table is in references.

| Pattern | Fires when | Behaviour |
|---|---|---|
| Retry-with-backoff | Transient failure (timeout, 429, overload) | Retry N times, widening gaps, then escalate |
| Confidence-gated fallback | Model confidence below threshold | Stop, drop to the floor, do not answer |
| Deterministic floor | High-risk path, any uncertainty | Fixed rule or conservative default, no model |
| Cached-last-good | Live call fails, a recent answer exists | Serve the last verified answer, flag it stale |
| Circuit breaker | Repeated failures on a dependency | Stop calling it, fail fast to the floor |
| Human escalation | Floor reached on an irreversible path | Hand to a named human with the context |

### Step 3: Set the confidence thresholds
Name the number that fires each gate, and the action below it. Below threshold the system refuses rather than guesses. A model with no floor does not stop on a case it does not understand; it answers anyway, confidently, because that is what it was trained to do.

### Step 4: Bound every loop
Every retry and reroute gets a max-iteration cap, a wall-clock timeout, and a budget ceiling, set tight before you ship. Recovery that never gives up does not heal; it burns tokens in a circle until someone notices the bill.

## Output

- A **fallback map**: for each critical path, the trigger, the fallback behaviour, and the escalation target.
- The **confidence thresholds**: the number that fires each gate and the action below it.
- The **loop bounds**: max iterations, timeout, and budget cap per recovery path.
- Next: wrap this into the `design-the-mva` spec so the fallback ships with the first agent, not after.

## Constraints

- No silent failure. The fallback must make wrong loud: a flag, a log, an escalation. A confident wrong answer that nobody catches is the recall waiting to happen.
- No infinite retry. Self-healing without a cap is a runaway agent in a costume. Bound every loop before it ships.
- Never let the model guess fluently under low confidence on an irreversible path. Keep a human on the loop where the answer touches a person.
- This is not legal or medical advice. Confirm clinical, food-safety, or financial thresholds with a qualified professional.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour.

## Dictionary

[self-healing fallback](../../dictionary/04-agentic-patterns.md#self-healing-fallback) ·
[deterministic fallback](../../dictionary/06-evaluation-and-safety.md#deterministic-fallback) ·
[silent failure](../../dictionary/05-failure-modes.md#silent-failure) ·
[human-on-the-loop](../../dictionary/04-agentic-patterns.md#human-on-the-loop-hotl) ·
[infinite loop](../../dictionary/05-failure-modes.md#infinite-loop-runaway-agent)

## Copy-paste version

> For non-coders: paste into any chatbot or no-code builder (Claude.ai, ChatGPT, Lovable, Bolt, v0).

```
Act as my reliability engineer. My product: [ONE_LINER]. Domain: [DOMAIN]. The job my agent owns:
[AGENT_TASK]. I need it to survive a model that fails, stalls, or is unsure, instead of shipping a
confident wrong answer.
1. List the critical paths and their reversibility. For each, decide fallback hardness: reversible
   (screenshot, draft) = retry then best-effort; partly reversible (a stored record, a sent message)
   = retry, reroute, conservative default; irreversible (a dose, allergen, threshold, trade) = NO
   guess ever, drop to a fixed non-AI answer and a named human.
2. For each path pick a pattern: retry-with-backoff, confidence-gated fallback, deterministic floor,
   cached-last-good, circuit breaker, or human escalation. Give the trigger and the exact behaviour.
3. Set the confidence threshold that fires each gate, and what happens below it (refuse, do not guess).
4. Bound every loop: max retries, a timeout, a budget cap. Tell me self-healing with no cap is just an
   infinite loop.
Make wrong LOUD: every fallback must flag, log, or escalate, never fail silently.
End with the single highest-risk path I must wire a deterministic floor under first.
```
