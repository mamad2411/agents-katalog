---
name: agent-tool-call-loop-diagnosis-and-circuit-breaking
description: >
  Guides diagnosing an active or recurring runaway agent tool-call loop and
  stopping it safely with a bounded retry policy and a hard ceiling —
  distinct from raising the iteration limit. Use when a user asks to
  "figure out why the agent is stuck calling the same tool," "safely kill
  a runaway agent session," "the agent keeps retrying the same failing
  action," "someone just raised the retry limit and it's still looping,"
  or needs to design a circuit breaker so a stalled agent fails closed
  instead of burning cost/quota indefinitely.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# Agent Tool Call Loop Diagnosis and Circuit Breaking

## Purpose

A runaway tool-call loop — an agent calling the same tool repeatedly, or
oscillating between two or three calls, without making progress — is one of
the most common and most expensive agent failure modes in production: it
burns tokens and API quota, can hammer a downstream system, and often goes
unnoticed until a bill or a rate-limit alert fires. Preventing loops at
design time (a hard iteration cap, stall detection in the dispatcher) is
covered in [agent-architecture-design](../agent-architecture-design/SKILL.md)
and [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md); this
skill is the *operational* companion — what to do when a loop is actually
happening or has already happened: how to confirm it's really a loop and
not a legitimate long-running task, how to stop an in-flight session
safely, how to root-cause the trigger, and how to design a **bounded retry
with a hard ceiling** rather than the reflexive, unsafe fix of just raising
the existing limit. Raising a limit without addressing the cause doesn't
stop the loop — it makes the loop more expensive before it stops.

## When to use

- A cost or latency alert traces back to one agent session or one workflow
  making an unusually high number of tool calls (see
  [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md)
  for the broader spike-triage process this often feeds into).
- An agent session is actively stuck and needs to be stopped safely without
  corrupting in-flight state.
- The transcript shows the same (or near-identical) tool call repeated
  many times with no new information between calls.
- Someone proposes "just raise `MAX_ITERATIONS`" or "just increase the
  retry count" as the fix, and you need to evaluate whether that's masking
  the real problem.
- Designing or auditing a circuit-breaker/retry policy for a tool-calling
  agent before it's given broader autonomy or higher-volume traffic.

## Prerequisites & environment

- Per-session logs of every tool call (name, arguments, result, timestamp)
  so a loop can be identified from history, not just suspected from a
  vague "this looks slow" report.
- A way to cancel or interrupt an in-flight agent session (a kill switch at
  the orchestration layer, not just "stop sending it new input") — see
  step 3 for why cancellation timing matters.
- The tool risk classification already established in
  [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md)
  (read-only / reversible / irreversible), since safe cancellation and
  circuit-breaker design depend on knowing which in-flight call, if any,
  has a side effect that can't simply be abandoned mid-call.
- Access to the dispatcher/loop code so a circuit breaker can actually be
  implemented, not just recommended.

## Step-by-step guidance

1. **Confirm it's actually a loop before treating it as one.** Pull the
   session's tool-call history and check for genuine repetition, not just
   "many calls" — a legitimately long task (paginating through a large
   result set, retrying a transient network blip a bounded number of
   times) can also produce a high call count. The distinguishing signal is
   whether each call carries *new information* toward the goal:

   ```python
   def is_loop(call_history, window=5):
       recent = call_history[-window:]
       signatures = [(c.tool_name, json.dumps(c.arguments, sort_keys=True)) for c in recent]
       return len(recent) == window and len(set(signatures)) <= 2  # near-total repetition
   ```

2. **Classify the loop type** — the fix differs by type:
   - **Exact-repeat stall**: identical (tool, arguments) called repeatedly
     with no change — almost never intentional progress.
   - **Oscillation**: alternating between two or three calls (e.g.
     `search(x)` → `search(y)` → `search(x)` → ...) — usually the model
     re-trying variations without converging, often because neither result
     satisfies an implicit precondition the prompt never stated.
   - **Error-retry storm**: the same call fails (error/timeout) and the
     agent retries it verbatim rather than adapting — this is a dispatcher
     problem (the error wasn't surfaced usefully) as much as a model one.
   - **Cost-without-progress**: calls are all distinct but the session's
     state (as tracked by the agent's own plan/goal) never advances —
     harder to detect mechanically; usually surfaces via a session
     duration/cost outlier rather than a repeated-signature check.

3. **Stop the in-flight session at a safe boundary, not mid-call.** Before
   force-killing a session, check whether any tool currently executing (or
   just completed but not yet acknowledged) is a reversible-write or
   irreversible-write action per its risk classification — killing a
   process mid-write can leave a partial state (a half-applied update, a
   sent-but-unlogged message) that's harder to clean up than the loop
   itself. Prefer a cooperative cancellation (set a flag the loop checks
   between tool calls) over a hard process kill wherever the runtime
   supports it; reserve a hard kill for cases where the loop is read-only
   or already confirmed stalled with no side effects in flight.

4. **Distinguish "still worth retrying" from "already proven futile" before
   designing the breaker.** A transient error (network timeout, momentary
   429) is reasonably retried a small, bounded number of times with
   backoff. An error that is deterministic given the current arguments (a
   404 on an ID that doesn't exist, a validation error on malformed input)
   will not succeed on retry with the same arguments — retrying it anyway
   is pure waste and the fix belongs in surfacing that distinction to the
   model, not retrying harder.

5. **Implement a bounded retry with an explicit hard ceiling, not just a
   backoff schedule.** Backoff alone (exponential delay between attempts)
   without a hard cap on total attempts still allows an unbounded total
   cost if nothing ever forces a stop; a hard ceiling is the actual safety
   property.

   ```python
   class CircuitBreaker:
       def __init__(self, max_attempts_per_signature=3, max_total_calls=25,
                    cooldown_seconds=30):
           self.max_attempts_per_signature = max_attempts_per_signature
           self.max_total_calls = max_total_calls          # hard ceiling, session-wide
           self.cooldown_seconds = cooldown_seconds
           self._attempts = collections.Counter()
           self._total_calls = 0
           self._tripped_signatures = set()

       def before_call(self, tool_name, arguments):
           signature = (tool_name, json.dumps(arguments, sort_keys=True))
           if signature in self._tripped_signatures:
               raise CircuitOpen(f"{tool_name} already failed {self.max_attempts_per_signature}x with these arguments")
           if self._total_calls >= self.max_total_calls:
               raise CircuitOpen("session tool-call ceiling reached — hard stop, not a retryable condition")
           self._total_calls += 1
           return signature

       def after_call(self, signature, result):
           if result.is_error:
               self._attempts[signature] += 1
               if self._attempts[signature] >= self.max_attempts_per_signature:
                   self._tripped_signatures.add(signature)  # this exact call is now permanently blocked this session
   ```

   The critical property: `max_total_calls` is a **hard ceiling** the
   session cannot exceed under any circumstance, independent of and in
   addition to per-signature retry limits — it's the backstop that catches
   oscillation and cost-without-progress loops that per-signature counting
   alone would miss.

   > **Warning:** Raising `max_attempts_per_signature` or
   > `max_total_calls` in response to a loop incident, without fixing the
   > underlying trigger (step 6) and without keeping *some* hard ceiling
   > in place, is not a fix — it is choosing to pay more before the same
   > failure stops. Every ceiling raise should come with a stated reason
   > tied to a legitimate use case (e.g. "this workflow genuinely needs up
   > to 40 calls for large result sets"), not "the loop kept hitting the
   > old limit."

6. **Root-cause the underlying trigger** once the loop is contained. Common
   triggers: a tool schema that doesn't tell the model a precondition
   (e.g. "call `stop_instance` before `resize_instance`"), a tool that
   returns an ambiguous or malformed error the model can't act on, or the
   model misreading a tool result as incomplete when it was actually
   final. This overlaps with
   [agent-bad-response-triage-and-root-cause-classification](../agent-bad-response-triage-and-root-cause-classification/SKILL.md)
   when the loop also produced a bad final answer rather than just wasted
   cost.

7. **Add the trapped case to the eval suite** (see
   [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md))
   so a fix to the tool schema, error message, or prompt can be validated
   against the exact scenario that caused the loop, not just spot-checked.

8. **Add session-level alerting on tool-call count and distinct-signature
   ratio**, not just on total cost or latency — a loop is visible in call
   count and repetition well before it shows up as a cost anomaly large
   enough to alert on its own (see
   [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md)).

9. **Verify the fix by replaying the original trigger** against the
   patched tool/prompt with the circuit breaker still active — the breaker
   should not trip on the fixed path, and should still trip if the same
   bug is reintroduced later.

## Best practices

- Treat the circuit breaker's hard ceiling as safety-critical
  configuration, reviewed with the same scrutiny as the agent's main loop
  iteration cap in
  [agent-architecture-design](../agent-architecture-design/SKILL.md) — the
  two caps overlap in purpose but operate at different layers (overall
  loop vs. per-tool-signature).
- Set a `max_total_calls` ceiling generously above legitimate peak usage,
  but always set one.
- Log every circuit-breaker trip with full context (signatures attempted,
  arguments, errors received) — a trip is a debugging gift, not just a
  safety event to acknowledge and dismiss.
- Prefer fixing the tool/schema/prompt trigger over tuning breaker
  thresholds; a well-tuned breaker limits damage, it doesn't prevent the
  next loop from a different trigger.
- Make the breaker's "circuit open" state produce a clear, structured
  failure the agent's final-answer logic can report as `failed`, not a
  silent truncation that looks like a normal stop.
- Keep the breaker's per-signature and session-wide ceilings both active
  at once — session-wide alone misses cheap, low-cost oscillation loops
  that never trip a cost alert; per-signature alone misses oscillation
  across 3+ varying calls.
- Periodically review which ceilings have been raised and why; a ceiling
  raised during an incident and never revisited is effectively a silently
  weakened safety control.

## Common pitfalls

- **Symptom:** An on-call engineer raises `MAX_ITERATIONS` from 12 to 100
  during an incident to "unblock" a stuck workflow, the workflow completes
  once, and the same loop recurs at higher cost the following week.
  **Fix:** Treat a raised ceiling as a temporary, tracked exception with an
  explicit expiry and a linked root-cause ticket, not a permanent
  configuration change — the underlying trigger (step 6) still needs
  fixing regardless of the ceiling's value.

- **Symptom:** A hard `kill` of a stuck agent session leaves a database
  record half-updated or a message partially sent, because the kill
  happened mid-tool-execution rather than between calls.
  **Fix:** Use cooperative cancellation that only stops the loop at a safe
  boundary (between tool calls), and check the risk classification of any
  in-flight call before a hard kill; reserve hard kills for sessions
  confirmed to have no reversible/irreversible action in flight.

- **Symptom:** The circuit breaker's exact-signature matching never trips
  because the model varies one argument slightly on every call (a
  timestamp, a retry counter, a slightly reworded query string), so the
  session keeps looping under a "different" signature each time.
  **Fix:** Add a session-wide hard ceiling (`max_total_calls`) that trips
  independent of signature matching, and consider a looser signature
  (ignore volatile fields like timestamps when hashing arguments) for the
  per-signature check specifically for oscillation detection.

- **Symptom:** A tool call fails with a generic "error" the dispatcher
  passes back to the model verbatim, the model retries the identical call
  believing a retry might succeed, and this repeats until the ceiling
  trips.
  **Fix:** This is a dispatcher problem, not a model problem — return a
  structured, specific error (see
  [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md)) that
  distinguishes "transient, retry may help" from "deterministic failure,
  retrying with the same arguments cannot succeed," so the model (and the
  breaker's own logic) can react appropriately.

- **Symptom:** Cost/latency monitoring only alerts on aggregate spend, so a
  loop that runs cheap, fast tool calls thousands of times goes unnoticed
  until a downstream rate limit or quota is exhausted.
  **Fix:** Alert on tool-call count and distinct-signature ratio per
  session directly, not only on aggregate dollar cost — a loop is visible
  in call volume long before it's visible in a cost dashboard.

## Worked example

**Scenario:** A cloud-ops agent given `list_instances`, `stop_instance`,
and `resize_instance` tools is asked to "resize the `checkout-api` fleet to
a larger machine type." Tool-call logs show 40+ calls to `resize_instance`
with the same `instance_id`, each failing with a bare `"error": "invalid
state"`.

Diagnosis:

1. Loop check confirms exact-repeat stall: the last 10 calls are
   identical `(resize_instance, {"instance_id": "i-0abc...", "new_machine_type": "large"})`.
2. This is an **error-retry storm**: the tool is failing deterministically
   (the instance is still running — `resize_instance` requires a stopped
   instance per its schema description — see
   [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md)), and
   the dispatcher's `"invalid state"` message gives the model no
   actionable detail to self-correct.
3. Immediate containment: the session's circuit breaker (per-signature
   `max_attempts=3`) should have tripped at attempt 3, but the breaker
   wasn't wired into this dispatcher yet — the session is killed at the
   next safe boundary (no `resize_instance` call was actually in flight
   mid-execution, all had already returned an error, so a hard stop is
   safe here).
4. Root cause: the dispatcher's error handler collapses all
   `resize_instance` failures into a generic `"invalid state"` string
   instead of the specific precondition failure.
5. Fix: the dispatcher is changed to return
   `{"error": "resize_instance requires the instance to be stopped first; call stop_instance(instance_id) then retry"}`,
   and the circuit breaker from step 5 of the guidance above is added to
   the dispatcher with `max_attempts_per_signature=3` and
   `max_total_calls=25` for this agent's sessions.
6. Verification: replaying the original request against the patched
   dispatcher shows the model now calls `stop_instance` after the first
   `resize_instance` failure and completes successfully in 3 tool calls;
   a new eval case captures this exact sequence
   (`resize before stop → expect stop_instance next`) per
   [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md).
7. Alerting: a new per-session alert on `tool_call_count > 15` for this
   agent type is added, so a future recurrence pages before running to the
   ceiling silently.

## Cross-references

- [agent-tool-use-patterns](../agent-tool-use-patterns/SKILL.md) — the design-time stall detection and tool-risk classification this skill's operational diagnosis builds on.
- [agent-architecture-design](../agent-architecture-design/SKILL.md) — the overall loop's hard iteration cap and timeout, which operate alongside (not instead of) the per-tool circuit breaker here.
- [agent-cost-and-latency-spike-investigation](../agent-cost-and-latency-spike-investigation/SKILL.md) — loops are one of the most common root causes of a single-workflow cost/latency spike.
- [agent-bad-response-triage-and-root-cause-classification](../agent-bad-response-triage-and-root-cause-classification/SKILL.md) — when a loop also produces a bad final answer, not just wasted cost.
- [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md) — turning a confirmed loop trigger into a permanent regression case.
