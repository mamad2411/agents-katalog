---
name: build-discipline
description: >-
  A language- and domain-agnostic engineering discipline for building non-trivial
  software that actually survives real use — services, parsers, CLIs, data
  pipelines, simulators, interactive tools, agents, compilers, anything with
  state, logic, or behavior beyond a toy. Use this skill WHENEVER a task involves
  writing or reviewing real code, especially "build me X", "implement Y", "why is
  this flaky/collapsing/wrong", or "make this robust" — even when the user doesn't
  ask for rigor by name. It exists to supply the discipline a senior engineer
  applies by reflex and a model skips by default: separate state cleanly, measure
  the constants you'd otherwise guess, verify with invariants instead of hope, and
  assemble in gated stages. Apply it before writing code, not after the bug.
---

# Build Discipline

A distilled engineering discipline for building software that keeps working after
the demo. It is deliberately concrete: generic advice ("test your code", "watch
performance") is worthless — the value is in *which* specific things break, *why*,
and the exact habit that prevents each. Every rule here was paid for by a real
failure.

**The one idea to keep:**

> Software survives real use not because of a clever algorithm, but because its
> state is cleanly separated, every constant that gates behavior was *measured*
> rather than guessed, correctness is checked by *invariants you can actually
> run*, and the system is assembled in isolated stages you gate one at a time.
> Correct behavior is discovered through instrumentation, not asserted by hope.

The most expensive bug in most builds is the same one every time: a magic number
chosen by intuition instead of measurement. Internalize P3 and you have already
avoided the failure that causes silent collapse, dead output, and days of
vibes-based tuning.

---

## The nine principles

### P1 — Separate three kinds of state; never persist what you can derive
Almost every non-trivial program has exactly three kinds of state, and conflating
them is the root of a whole family of bugs:

- **Source of truth** — inputs, user decisions, config, the seed. Persisted.
- **Derived** — anything computable from the truth (indexes, caches, layouts,
  aggregates, similarity scores, resolved graphs). *Recomputed, never saved.*
- **Ephemeral** — session-only (cursor, hover, in-flight buffers, UI state). Dies
  with the process.

Rule: **never persist what you can derive** (it goes stale and breeds migration
hell); **never derive what encodes intent** (recomputing "the user dismissed
this" destroys the decision). Route all derivation through one recompute path:
mutation → recompute → present. One arrow, no partial-update bugs.

### P2 — Keep a pure core, seed the randomness, make it reproducible
Keep the logic that *decides things* free of I/O — no network, disk, DOM, clock,
or global mutable state reached from inside it. Inject those at the edges. Replace
ambient randomness with an explicitly **seeded PRNG**. This is not purity for its
own sake: a pure, seeded core runs thousands of times in milliseconds, headless,
and reproduces exactly — which is the precondition for every other discipline
here. The moment behavior is non-reproducible, you can no longer answer "did my
change help?", because every run now differs for two reasons at once.

### P3 — Calibrate every gating constant from printed data, never from intuition
**This is the principle that pays for the whole file.** Any constant that *gates
behavior* — a threshold, timeout, retry count, batch size, cache TTL, pool size,
backoff factor, similarity floor, rate — must be chosen by writing a tiny probe
that prints its real distribution on realistic input, then reading the number off
the printout. Not guessed.

Two real collapses, same root:
- A similarity threshold guessed at `0.28` when real values ran `0.05–0.30`
  produced an application that silently did *nothing* — zero output, and no error
  to point at.
- A resource drained `27×` faster than it refilled collapsed a system whose
  *global averages looked perfectly healthy* — the exhaustion was local and
  hidden.

Ten minutes of measurement replaces days of guessing. Always print human-readable
context beside the number (the actual records beside the scores, the actual keys
beside the counts) — the number alone can't tell you whether it's *right*.

### P4 — Prefer composable, data-driven rules over special-cases and global reads
If you catch yourself writing `if (globalTotal > N)` or special-casing one
situation, stop: you are hand-authoring a macro behavior that should fall out of
the design, and it will be brittle. Prefer many small local rules expressed as
**data** (tables, parameter vectors, weighted signal lists) over sprawling
type-specific `if/else` code. Data is editable, testable, and can't hide special
cases in a branch you forgot. When several weak signals exist, stack them with an
explicit priority and merge — each layer stays debuggable alone.

### P5 — Assert invariants, not outputs; build the harness before the UI
You often can't assert an exact output (it's input-, seed-, or corpus-dependent).
You *can* assert the properties that must hold for **any** correct run, and you
should build the thing that checks them *before* building the interface:
- Nothing is `NaN`/null-where-forbidden; every quantity stays within its bound.
- Bookkeeping is consistent (a fresh scan equals the maintained count).
- Reversible operations round-trip exactly: `save → load → continue` is identical
  (two classic bugs live here — restore the RNG/cursor state *last*, and don't
  round-trip through a lossy format if you need bit-identity).
- Intent is honored: a deleted/dismissed thing never silently reappears.
- **Turn the fuzzy goal into a number.** "Does it cluster / converge / stay
  stable?" → a metric that's ~baseline for a degenerate run and clearly higher
  when the property holds. Now "it works" is a regression test, not a vibe.

Ship the harness *inside* the artifact when you can (a self-test mode that runs
assertions and emits a machine-greppable PASS/FAIL verdict). It converts "I
believe it works" into something checkable — exactly the step that gets skipped.

### P6 — Isolate → stabilize → compose → tune → verify, and gate every step
Build in this order, each stage with an explicit **exit criterion**, and refuse
to proceed past a failed gate:
1. State + core loop written; nothing invalid after N iterations.
2. **Isolate one part** and make it correct alone. Calibration and boundary bugs
   surface cleanly here, un-buried by everything else.
3. **Add the next part; test the pair.** Coupling bugs surface here (see P8).
4. **Compose the whole; tune for the *character* you want,** not merely "runs" —
   and tune on a table (a parameter sweep printing outcomes per cell), not by
   eyeballing.
5. Only now build the interface and controls.
6. Adversarial pass: edge inputs, extreme parameters, round-trips, long runs.

Most failures are diagnosed 10× faster in an isolated subsystem than in the whole
assembly. Skipping "isolate" is the most common self-inflicted wound.

### P7 — Every automated judgment carries its reason; destruction needs a guard
If the system decides something *for* the user — a match, a suggestion, an
auto-fix, a merge — the function that computes it must return the **evidence with
it** (`{result, why}`), never the bare result. A decision with no reason reads as
random; the same decision labeled with its cause reads as intelligent, and is
debuggable. If you can't produce a one-line justification, don't ship the
judgment. Enforce the asymmetry: freely create *reversible* structure, but any
*destructive or irreversible* action (delete, overwrite, apply-in-place) requires
an explicit confirmation.

### P8 — Coupled constants can be jointly impossible; check interacting ranges
Two individually reasonable numbers can be *jointly* contradictory. A real one: a
contact radius of `18` nested inside a separation radius of `23` made an
interaction *geometrically impossible* — agents were pushed apart before they
could ever meet — though each number looked fine alone. Whenever two constants
interact (a timeout vs. a retry budget, a buffer vs. a chunk size, a floor vs. a
cap, a lower threshold vs. an upper one), write down the relationship they must
satisfy and assert it. Isolating subsystems (P6) is how you expose these.

### P9 — Design the degenerate case; make even the worst state coherent
The boundaries are where things break or look dead, and where users decide the
thing is alive or broken:
- **Empty / n=0,1,2 / cold start:** every function must degrade gracefully, not
  divide by zero or render a blank void. A crafted starter state that makes the
  interesting behavior *demonstrably fire* beats any amount of documentation.
- **Collapsed / degenerate steady state:** choose a design whose worst case is
  still coherent (a running-but-reduced system beats a frozen or corrupt one).
  This is the difference between something that feels alive after twenty minutes
  and something that settles into a dead equilibrium.

---

## Applying this inside a coding session

This discipline is most valuable injected into an AI-assisted build loop, where
the default failure mode is confidently producing a plausible-looking artifact
that breaks on contact with reality. To counter that:

- **Draw the P1 state table and name the P3 gating constants before writing code.**
  This alone removes most downstream pain.
- **Give one job per turn.** "Build the pure core and pass its invariants," then
  separately "probe the constants and report the distribution," then "add the
  interface." Long "build and tune and verify it all" prompts are where quality
  drifts.
- **Make measurement non-optional.** Demand the probe's printed output in the
  reply before any threshold is chosen. A model (or a person) will confidently
  hardcode `> 0.5` unless forced to look at the data.
- **Demand evidence-carrying returns (P7).** Contracting every decision as
  `{result, why}` forces better logic, because vague logic can't produce a
  concrete reason.
- **Gate on invariants, not vibes.** Refuse to advance a stage until its exit
  criterion prints green. The single biggest quality lever is not continuing past
  a failed gate.

The throughline: a modest model executing a strong, explicit structure beats a
strong model improvising. This file *is* that structure — the principles say
*why*, the build order says *in what order*, and the invariants say *when you're
actually done*. The hard part was never the code. It was knowing what to check,
and in what order.

---

*Distilled from real builds — the failure modes named above (a threshold that
silenced an app, a drain/refill mismatch that hid behind healthy averages, a pair
of radii that made an interaction impossible) all actually happened and were
actually fixed. The specifics are the point; keep them.*
