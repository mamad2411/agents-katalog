---
name: Agent Harness Evaluation
description: >
  Audit an AI agent harness (the execution framework around the model — agent
  loop, tool execution, state management, context management, retry, recovery,
  permissions, observability) for robustness, safety, and recoverability. Also
  designs deterministic reliability test suites for such harnesses. Use this
  whenever someone asks you to review, audit, harden, or write tests for an
  agent framework, agent runtime, agent loop, tool-calling layer, or
  "harness" — and also when they describe symptoms of harness fragility
  without naming it: orphaned tool calls, 400s from the provider on the next
  turn, runs that won't cancel, duplicated side effects after a retry, state
  corruption after a crash, infinite tool loops, or prompt cache that never
  hits. This skill evaluates the framework, NOT whether the model is smart
  enough to solve a task — do not use it for model or prompt quality
  evaluation.
---

# Agent Harness Evaluation

## What this evaluates

The execution framework around the model. Not the model.

The question is not "did the task succeed" but: when something goes wrong,
does it fail **safely**? Is the state afterwards **consistent and
recoverable**? Are side effects **bounded** — never duplicated, never
unauthorized? Can you **reconstruct** what happened, and **replay** it?

A harness that succeeds on the happy path and corrupts state on every third
failure is worse than one that succeeds less often and always fails cleanly.
Grade accordingly.

## Two modes

Decide which applies before doing anything. If ambiguous, ask — they produce
completely different artifacts.

**Mode A — Audit.** The user has a harness codebase and wants to know what's
weak. Output is a findings report with code locations. Minutes, no
infrastructure. **Default — start here** even when the user eventually wants
tests, because the audit tells you which tests are worth writing.

**Mode B — Build tests.** Output is code: scripted model, fake tools, fault
injector, oracles, CI wiring. Part 2 of this document.

Most real requests are A then B. Do not build a generic test suite for
problems the codebase doesn't have.

---

# PART 1 — AUDIT

## Step 1 — Locate landmarks

Find where things live; record file and line. Missing landmarks are a normal
result — they mean the corresponding checks report "not implemented" rather
than "passed".

Landmarks: agent loop · request assembly · system prompt build · tool
registry · tool execution · history append · stream parse · retry ·
truncation · process spawn · http call.

Use symbol-level navigation where available, text search otherwise. A grep
hit is a candidate, not a landmark — read the enclosing function.

## Step 2 — Run the checks

Fourteen checks below. Priority **P1** = fails loudly and often, judgment
nearly mechanical. **P2** = real production risk, more reading. If context is
limited, P1 alone is a useful audit.

Each check lists search terms for TypeScript/JavaScript (TS), Python (PY),
and Go. These locate candidates only.

## Step 3 — Report

Use the template at the end of Part 1. The "Not covered" section is not
optional.

---

## Group 1 — State stays self-consistent

### C1 · Tool-call pairing completeness — P1

**Symptom.** A tool call is emitted but no matching result is recorded on
some exit path. The next request carries an unclosed call and the provider
rejects it (usually 400). Highest-frequency real failure in agent harnesses.

**Check.** Walk every path that can exit tool execution: normal return,
`catch`, timeout, cancellation, early return, permission denial. Each must
write a result. Then check parallel dispatch: if one call fails, are the
others' results still recorded? All-or-nothing combinators reject on first
failure and discard settled results — that breaks this and C8.

**Search.** TS: `Promise.all` · `Promise.allSettled` · catch blocks and early
returns inside the dispatch function · `AbortError`. PY: `asyncio.gather`
(check `return_exceptions`) · `except` in the dispatch coroutine ·
`CancelledError`. Go: `errgroup` · early `return err` before the append ·
`select` on `ctx.Done()`.

Grep misses the early-return case, which is the most common one — enumerate
exits by reading.

**Confirmed when** a reachable exit path writes no result, or parallel
dispatch is all-or-nothing.

**Invariant.** Every tool call has exactly one result.

### C2 · History is append-only — P2

**Symptom.** Messages mutated after being added — a field backfilled, an
assistant message corrected in place. Breaks replay and debugging, and
silently invalidates every cached prefix from the mutation point onward.

**Check.** Assignment into elements of the message collection, or functions
that return a modified copy replacing the original. Legitimate exception: a
declared compaction step replacing a range — that is C13, not this.

**Search.** All: `messages[i].` assignment · `.content =` · `.splice(` /
`.pop()` / in-place list ops outside a compaction path.

**Confirmed when** messages already in history are mutated outside a declared
compaction path.

### C3 · Crash and checkpoint semantics — P2

**Symptom.** The process dies mid-write. On restart the partial state is
indistinguishable from a complete one, so the harness resumes on top of a
half-written checkpoint.

**Check.** For each multi-part write (a start record and an end record, a
header and a body), ask what a reader sees if the process dies between them.
Good designs leave a **detectable incomplete marker**; bad ones leave
something that reads as complete. Also: does resume re-execute anything that
already ran?

**Search.** Writes not routed through write-temp-then-rename · absent
`fsync` · bracketed records with no reader-side detection of a missing end ·
resume paths with no already-ran check.

**Confirmed when** a partial write reads as complete, or resume re-executes a
side-effecting operation.

**Invariant.** Recovered state equals the state normal execution would reach.

---

## Group 2 — Untrusted input is treated as untrusted

### C4 · Model output parsing — P1

**Symptom.** Malformed tool arguments, a truncated stream, or a repeated call
id crashes the loop or produces silent garbage. Malformed model output is
routine, not exceptional.

**Check.** (1) Bare deserialization of model-produced JSON with no error
handling. (2) Stream terminated early — is partial state discarded, or
committed as complete? (3) Duplicate tool-call id in one turn. (4) Delta
accumulation assuming indices are contiguous, zero-based, monotonic.

**Search.** TS: `JSON.parse(` on response-derived values · stream reader
loops · `delta.index`. PY: `json.loads(` on response content · `async for`
over the stream · `choices[0]` unchecked. Go: `json.Unmarshal` with no error
branch · `bufio.Scanner` over the SSE body.

For duplicate ids the *absence* of handling is the finding — check the
accumulation structure, since a map keyed by id silently overwrites.

**Confirmed when** model output is deserialized without error handling, or
partial stream state is committed on early termination.

### C5 · Path and sandbox boundaries — P2

**Symptom.** A model-supplied path escapes the workspace.

**Check.** Path joining with no resolve-and-prefix check afterwards. Prefix
checks performed before symlink resolution. Whether the check runs on the
same string that is later opened.

**Search.** TS: `path.join(` without following `resolve` + `startsWith` ·
`fs.realpath` absent · `lstat` vs `stat`. PY: `os.path.join(` · pathlib `/` ·
`os.path.realpath` absent · `open(` on the unvalidated variable. Go:
`filepath.Join` · `filepath.EvalSymlinks` absent.

High-yield pattern: a validation function returning a boolean, with the
caller then opening the *original* string.

**Confirmed when** a model-supplied path reaches a filesystem call without
resolve-then-prefix validation.

### C6 · Secrets and ambient environment — P2

**Symptom.** The whole process environment is handed to model-generated
commands, so every credential is one `env` away from the transcript.

**Check.** Subprocess launches passing the full environment, explicitly or by
inheritance. Predictable paths handed to untrusted output. Whether tool
output is scanned for secrets before entering history.

**Search.** TS: `spawn(`/`exec(` with no `env` option · `env: process.env` ·
`...process.env`. PY: `subprocess.run(` with no `env=` · `env=os.environ`.
Go: `exec.Command` without setting `cmd.Env`.

**Confirmed when** subprocess launch inherits the full environment for
model-generated commands.

---

## Group 3 — Failure is a first-class outcome

### C7 · Error taxonomy and retryability — P2

**Symptom.** Callers receive a bare error and cannot decide what to do, so
they retry everything or give up on everything.

**Check.** Is there a closed set of error codes a caller can enumerate? Is
each failure classified retryable / not retryable / fatal? Or does a raw
provider exception reach the loop?

**Search.** `throw new Error(` / `raise Exception(` with a string message in
the tool or provider layer · empty catch blocks · catching a base exception
class · error *text* matched by string comparison to decide retryability.

**Confirmed when** failures reach the agent loop without classification.

### C8 · Partial success — P2

**Symptom.** Four of five parallel operations succeeded, but the batch is
reported as one failure and the four results discarded.

**Check.** Any place where multiple independent outcomes collapse into one
status. Question any single-status return type over a batch of independent
work.

**Search.** Same combinators as C1.

**Confirmed when** independent results are discarded because a sibling
failed.

### C9 · Idempotency and side-effect safety — P1

**Symptom.** An operation with an external effect times out *after* the
effect committed. The harness retries. The effect happens twice.

**Check.** What does the retry wrapper enclose? If the retried region
contains a write, a command execution, or an outbound message, retry
duplicates it. Safe designs retry only the transport, carry an idempotency
key, or query-before-retry when the outcome is unknown.

The specific case to look for: **timeout after commit**. Unknown outcome is
not failure and must not be classified as one. If a timeout on a
side-effecting call maps to the same branch as a connection refusal, that is
the defect.

**Search.** `retry` · `backoff` · `for attempt in` · `tenacity` · `p-retry`
to find the region; then writes, `spawn`/`exec`, outbound posts inside it.
Also `idempotency` / `idempotencyKey` — its absence is the finding.

**Confirmed when** a retried region contains a side-effecting operation with
no idempotency key and no query-before-retry.

**Invariant.** Duplicate side effects = 0. Any violation blocks release.

---

## Group 4 — Boundaries can be closed

### C10 · Cancellation propagation — P1

**Symptom.** The user cancels; the subprocess keeps running, the request
keeps waiting, the timer keeps firing. Symptom is "it won't stop".

**Check.** (1) Is the cancellation signal actually passed to outbound
requests, or created and forgotten? (2) After spawning a process, is a kill
registered? Does it kill the **process group** — killing only the direct
child leaves shell-spawned grandchildren behind. (3) Are timers cleared on
error paths, not just success paths? (4) Does stream consumption stop on
cancel, or run to EOF? (5) Does shutdown reach genuine quiescence, or merely
*request* that everything stop and return?

**Search.** TS: `new AbortController` · every `fetch(` — check for `signal:` ·
`spawn(` — check for a kill on abort · `setInterval`/`setTimeout` with no
clear on the error path · `process.kill(pid)` vs `process.kill(-pid)`
(negative = process group). PY: swallowed `CancelledError` · `task.cancel()`
not awaited · `terminate` vs `killpg`. Go: `context.Context` accepted but not
passed down · `SysProcAttr` `Setpgid` absent · goroutines with no done
channel.

Highest-yield grep across all languages: every process spawn, then check
whether a kill exists anywhere in the same scope.

**Confirmed when** a spawn has no kill registration, or a request is issued
without the available cancellation signal.

### C11 · Timeout layering — P2

**Symptom.** Users always see a low-level connection error, never a
meaningful "this tool timed out", so nobody can tell which tool is slow.

**Check.** Count the timeout layers on one tool call and compare the numbers.
The healthy relationship is **tool-level budget < underlying resource
backstop**, so a normal timeout surfaces as a classified tool timeout.

**Search.** All timeout constants and their units; then map which wraps
which. The finding is a *relationship*, so list them together. Watch units —
seconds compared against milliseconds is its own bug.

**Confirmed when** the inner backstop is shorter than the outer tool budget.

### C12 · Loop and budget limits — P1

**Symptom.** The model calls the same tool forever. Cost climbs until someone
notices.

**Check.** Hard ceilings on turns, tool calls, wall-clock runtime, tokens,
and — if delegation is supported — depth and fan-out. Any no-progress
detection (identical call with identical arguments)? When a ceiling is hit,
is the outcome a distinct status, or indistinguishable from completion?

**Search.** `maxTurns` · `max_iterations` · `while True` / `for {}` in the
loop file · depth parameters on delegation. Absence is the finding, so read
the loop's exit conditions rather than searching for a constant that may not
exist.

**Confirmed when** turns / tool calls / runtime lacks a ceiling, or a ceiling
produces a status indistinguishable from success.

---

## Group 5 — Finite resources are accounted for

### C13 · Context management and truncation boundaries — P1

**Symptom.** Long sessions hit the context limit and the harness either dies
or truncates across a tool-call boundary — producing exactly the C1 failure.

**Check.** (1) Is there any context management at all? If not, the ceiling is
a hard wall; report it. (2) Where is the cut chosen? Purely by token or
message count with no pairing validation means the cut can separate a call
from its result. (3) What if content is still too large after compaction — a
second path, or a loop? (4) Are oversized tool outputs spilled to storage and
replaced by a reference, or pushed whole into context?

**Search.** `compact` · `truncate` · `summarize` · `slice(` / `[-n:]` on the
message collection · token counting functions. Then read the cut selection.

**Confirmed when** the cut point is selected without tool-pairing validation,
or there is no path for "still too large after compaction".

**Not-implemented** when no context management exists — note explicitly that
this is a hard ceiling, not a passing grade.

### C14 · Prompt prefix determinism — P1

**Symptom.** The provider's prefix cache never hits. Nothing errors. Nothing
is functionally wrong. Every request is billed at full input price. Because
there is no failure signal, this survives in production for months.

**Check.** On the path that builds everything before the newest user message
— system prompt, tool definitions, prior messages:

1. Non-deterministic values: current time, timestamps, random numbers,
   generated ids, process id, hostname.
2. Tool ordering that depends on iteration over a runtime-populated map or
   set with no explicit sort.
3. Volatile content at the front rather than the back — directory listing,
   "today's date", live status — when it could live in the trailing message.
4. In-place history mutation (C2), which invalidates from that point onward.

**Search.** TS: `Date.now` · `new Date` · `toISOString` · `Math.random` ·
`randomUUID` · `process.pid` · `os.hostname` · `Object.keys(` over a runtime
map · `Set`/`Map` iteration without sort. PY: `datetime.now` · `time.time` ·
`uuid4` · `random` · `os.getpid` · `gethostname`. Go: `time.Now` · `rand.` ·
`uuid.New` · `os.Getpid` · **map range** — unordered by specification, so a
map range on the serialization path is a finding by itself.

**Verify empirically.** Build the request twice from identical conversation
state and compare the serialized prefix byte for byte. Any difference is a
defect. Cheap, and worth adding as a permanent test regardless of what the
search finds.

**Framing.** This is robustness, not optimization. A harness costing several
times what it needs to, with no signal anything is wrong, is failing — just
slowly.

---

## Group 6 — The run is observable

### C15 · Trace completeness and replay — P2

**Symptom.** Something went wrong in production and nobody can reconstruct
what happened, so no fix can be validated.

**Check.** Is there an event record covering turn boundaries, tool calls and
results, request composition, retries, truncation, approvals? Is token usage
recorded, including cache read and write separately? Can a recorded run be
replayed without calling the provider?

Providers report cached input tokens separately; if only a single total is
stored, cache hit rate cannot be computed and C14 has no regression
protection.

**Confirmed when** tool calls and results are not recorded with correlation
between them, or token usage is not recorded at all.

**Why last but not least.** Without it, none of the other fourteen can be
verified after a change. If the user must fix one thing first and has no
traces, this is it.

---

## Evidence rules

A report full of plausible findings with no locations is worse than no
report — verifying it costs more than auditing from scratch, and the reader
stops trusting the tool.

**Every finding carries a file path, a line number, and a verbatim code
excerpt** checkable in under a minute. No location, no finding.

| Verdict | Meaning |
|---|---|
| `confirmed` | Evidence directly supports the claim. |
| `suspected` | A protection is structurally absent but you could not confirm the path is reachable. State exactly what a human should check. |
| `not-implemented` | The subsystem doesn't exist here. Not a pass. |

**Do not upgrade on the way to the summary.** `suspected` in the body stays
`suspected` in the summary. This is the most common way such reports lose
credibility.

**Do not pad.** Zero findings in a group is a fine result. Inventing marginal
findings to make each group non-empty destroys the signal.

**Say what you didn't cover.** Landmarks not found, or code not read, go in
"Not covered". The reader must be able to distinguish "checked, clean" from
"never looked".

## Report template

```markdown
# Harness robustness audit

Target: <path> @ <commit>
Checks run: <n>    Findings: <n> confirmed / <n> suspected

## Summary
One line per check group, with its highest verdict.

## Confirmed
### C<n> · <check name>
**<file>:<line>**
<one sentence: what is wrong>

<verbatim code excerpt>

Consequence: <what breaks, concretely, under what conditions>
Direction: <what a fix looks like — not a patch>

## Suspected
Same shape, plus: "To confirm, check <specific thing>."

## Not covered
Which checks could not be evaluated, and why.

## Cost
Tokens consumed by this audit.
```

Report cost. The reader needs it to decide whether to run this regularly.

---

# PART 2 — BUILDING TESTS

Findings are worth little without regression protection — the same defect
reappears in three months. Build tests for the defects actually found, in the
order the audit ranked them. **Do not stand up the full infrastructure
first**; that ordering has killed more of these efforts than any technical
problem.

## Finding → test

None of these needs a real model or real network.

| Finding | Test | Assertion |
|---|---|---|
| C1 pairing | Tool throws on the Nth call | Every emitted call has exactly one result |
| C1 parallel | One of N parallel tools throws | N results present; N−1 successful |
| C3 recovery | Kill between the two halves of a checkpoint write | Restart detects incomplete state; nothing re-executes |
| C4 parsing | Scripted model emits invalid JSON arguments | Classified error, loop survives |
| C4 stream | Cut the stream mid-frame | Partial state discarded |
| C5 paths | Traversal plus a symlink pointing outside | Rejected before the filesystem call |
| C9 idempotency | Side effect commits, then times out; retry follows | Effect count exactly 1 |
| C10 cancel | Cancel with a subprocess and a request in flight | No surviving processes; no writes after the cancel point |
| C11 timeouts | Tool sleeps past the budget but under the backstop | Error is the tool timeout, not transport |
| C12 loops | Scripted model repeats one call forever | Terminates at the ceiling with a distinct status |
| C13 truncation | Drive past the context limit | No cut separates a call from its result |
| C14 prefix | Build the request twice from identical state | Prefixes byte-identical |

The C14 test costs almost nothing and catches an entire class of silent cost
regressions. Write it even if the audit found nothing.

## The scripted model

**The problem with the obvious design.** A harness sends arbitrary prompts.
You cannot write a stub that responds *sensibly* to arbitrary input — that
would require a model.

The resolution is to stop trying. These tests assert on harness behaviour,
not model reasoning. The stub does not need to be sensible; it needs to be
controllable.

**Design A — turn-indexed script (the workhorse).** Ignore the prompt; return
the Nth entry of a predetermined list on the Nth call. Covers most tests.
Breaks when the harness changes how many requests it makes per logical turn —
so assert on the transcript, not the turn count, and let the script return a
terminal response past its end.

**Design B — rule-matched responses.** A small table of predicates over the
last message, with a default fallback. More robust across many turns, where
turn indices become fragile.

**Design C — record and replay.** Highest fidelity; the only option when the
test needs realistic model output. Three rules decide whether this works or
becomes a permanent source of pain:

- *Normalize the cache key.* Canonicalize the request — strip timestamps,
  sort tool definitions, drop generated ids. Without this the cache misses
  every run and you have built an expensive live test.
- *Never fall back to the live provider on a miss.* Fail with a message
  naming the re-record command. A silent fallback turns a deterministic suite
  into a flaky billable one, and the failure is invisible — the suite still
  passes, just slowly and expensively.
- *Store recordings as raw frames, not parsed objects.*

**The constraint that shapes all three.** The scripted model is where you
inject malformed output — invalid JSON, duplicate call ids, truncated
streams. It therefore **cannot be built on the provider SDK's typed response
objects**, because those make invalid output unrepresentable. It must emit
raw bytes or stream frames at the transport boundary. Design for this from
the start; retrofitting means rewriting.

**Placement.** Substitute at the narrowest seam that still allows
transport-level malformation — usually the HTTP client or provider adapter,
not the "call the model" helper three layers up. Substituting too high skips
the stream parsing code, which is exactly what C4 tests.

## Fake tools

Must be able to: succeed; fail with a classified error; fail with an
unclassified exception; hang past every timeout layer; return output far
larger than the context window; return malformed output; **commit a side
effect and then fail** (the C9 case); and count their own invocations.

That last pair is the point — a fake tool that can only succeed or fail
cleanly cannot test the interesting half of the space. Keep the effect
counter outside the tool instance so it survives whatever the harness does
between retries.

## Fault injection

```yaml
scenario: side-effect-commits-then-times-out
fault:
  target: <tool or seam name>
  phase: after_side_effect     # before_call | during | after_side_effect | on_response
  occurrence: 1
  error: timeout
expect:
  max_side_effect_count: 1
  allowed_status: [SUCCESS, NEEDS_REVIEW]
  forbidden: [DUPLICATE_EFFECT]
```

`phase: after_side_effect` is the valuable one — the only way to test the
unknown-outcome case, which is where duplicate side effects come from.

Injection points worth wiring: provider transport (status codes, stream cut,
malformed body) · tool boundary · filesystem (permission denied, disk full,
file changed between read and write) · subprocess (hang, non-UTF-8 output,
exit code inconsistent with output) · persistence (write fails, crash between
the halves of a bracketed write) · clock (jump forward to trip timeouts
without real waiting).

**Verify zero-injection first.** Run the suite with every injector disabled
and require green. Injectors change timing; without this baseline you cannot
tell a real defect from one the injector caused.

## Oracles

Do not assert on final text alone — it is the least reliable signal the
system produces.

**State oracle.** Assert on the world: files, records, external state. Keep
the interface generic; domain assertions belong in the test case, not the
oracle.

**Trace oracle.** Assert on the execution record: which tools ran, in what
order, how many times, how many retries, where it stopped. Most harness
defects are visible here, because they usually show up as a wrong *sequence*
with a plausible-looking final answer.

**Invariant oracle.** Checked automatically after *every* scenario:

- every tool call has exactly one result;
- side-effect count equals intended effects;
- no unauthorized operation executed;
- no cross-tenant access (if multi-tenant);
- recovered state equals normal-execution state;
- no process, timer, or connection survives shutdown.

This is how one test catches a defect a different test was written for.

---

# PART 3 — CI AND THRESHOLDS

Every metric below has a threshold. A metric without one cannot gate
anything, and an ungated metric becomes a report nobody reads — which is how
most of these efforts die. These defaults are starting points; set them from
your own first week of data, then only tighten.

## Three pipelines

**Pull request** — scripted model, fake tools, injection, oracles. No
network, no real model. Under five minutes. **Gate: 100% pass.** It is
deterministic, so a failure is a defect. If it becomes flaky, fix the flake
as a P1 — a flaky blocking gate gets disabled within two weeks and then you
have nothing.

**Nightly** — real model, production-like scenarios, repeated. Measures what
determinism can't. **Never blocks merges.**

**Release** — chaos and migration: network partition, service restart, store
unavailable, worker crash, corrupted checkpoint, schema migration, concurrent
sessions. **Gate: zero P0 violations.**

## Safety metrics — these gate releases

| Metric | Threshold |
|---|---|
| Duplicate side effects | **0** |
| Unauthorized actions | **0** |
| Cross-tenant access | **0** |
| Approval replay | **0** |
| Orphaned tool calls | **0** |
| State divergence after recovery | **0** |

Zero means zero. These are correctness properties, not quality metrics.

## Reliability

| Metric | Threshold |
|---|---|
| Deterministic suite pass rate | 100% |
| Fault recovery rate (allowed status under injection) | ≥ 95% |
| Success rate (nightly, single run) | ≥ 90%, set from baseline |
| pass^3 (3 of 3 consecutive) | ≥ 80% |
| pass^5 (5 of 5) | ≥ 70% |

`pass^1` is the success rate — don't report it twice. The gap between success
rate and pass^5 is the useful number: it measures how much apparent
reliability is luck. 95% success with 50% pass^5 is far less stable than the
headline suggests.

## Cost

| Metric | Threshold |
|---|---|
| Tokens per scenario | alert on +20% week over week |
| Cache hit rate (cached ÷ total input tokens) | ≥ 60% on multi-turn |
| Retry amplification (attempts ÷ logical operations) | ≤ 1.2 |
| Tool calls per task (median) | alert on +30% |

Cache hit rate is the one people skip. A regression from 80% to 0% roughly
triples the bill with no test failing and no error logged. Track it or C14
comes back.

## Latency and recovery

| Metric | Threshold |
|---|---|
| P95 per scenario | baseline, alert +30% |
| P99 | alert +50% |
| Time to cancel (signal → full quiescence) | **< 2s** |
| Crash recovery rate | 100% |
| Replay success rate | ≥ 95% |

Time to cancel is a robustness metric, not a performance one — it directly
measures C10.

## Flake policy

`pass^5` is noisy by construction. Without a stated policy, the first red
night gets the job marked allow-failure and it becomes decoration.

- Nightly reports trend; it never blocks merges.
- Classify each failure the next morning: harness defect (file it, add a
  deterministic test — this is the goal) · model variance (record, move on) ·
  scenario defect · infrastructure.
- Quarantine is time-boxed, with an owner and a date. Expired quarantine is a
  build failure, or quarantine becomes a graveyard.
- Act when a scenario's pass^5 drops more than 20 points week over week, or
  when any safety metric moves off zero. Safety metrics are never
  quarantined.

## Cost control

Nightly is real model × repetitions × scenarios, and "it costs too much" is
the most common reason these suites get switched off.

Budget the suite first, then fit scenario and repetition counts to it — not
the other way around. Tier the scenarios: a small core set nightly at 5
repetitions, the long tail weekly at 3. Push everything that can be
deterministic into the PR layer; every real-model scenario should have a
reason it can't be scripted, and most can. Report cost in the nightly output
— a suite whose cost is invisible gets cut in the first budget review; one
reporting "caught 3 defects, cost X" survives.

## P0 — blocks release

Any of these, once: a side effect executed more than intended · an operation
outside the granted permission scope · state corruption, or recovery to a
state normal execution would not reach · a run that cannot be terminated ·
data crossing a tenant boundary · an approval bypassed or replayed.

Not scored. Binary.