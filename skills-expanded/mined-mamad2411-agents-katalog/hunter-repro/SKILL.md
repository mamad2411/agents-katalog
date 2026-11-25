---
name: hunter-repro
description: >-
  The promotion engine that turns a Sign into a Find. Load whenever a lead has
  been observed once and you are about to promote it, confirm it, reproduce it,
  minimise it, or write a Trail. Specifies the reproduction protocol (isolate
  preconditions, minimise the trigger, execute twice independently, fingerprint
  the environment), the flake taxonomy with a distinguishing test per class, the
  2-of-2 and 3-run tiebreak rule, minimisation before promotion, and the exact
  Trail artifact schema. Use before emitting any Find, and whenever two runs
  disagree, output is intermittent, or you must decide Sign versus Find.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Hunter Repro — the promotion engine

Assumes `hunter-doctrine` is loaded. A Sign is a lead. A Find is a claim Hunter
stakes its reputation on. This skill is the only sanctioned path between them.

Promotion is not "run it again and it still broke." Promotion is: isolate the
preconditions, shrink the trigger to the smallest failing case, execute that
minimal case twice independently, prove the result is not a flake, and write a
Trail another operator can replay without you. If any step cannot be completed,
the lead stays a Sign and is published as one.

## Inputs

A Sign record from a probe skill (`hunter-web-probe`, `hunter-api-probe`,
`hunter-cli-probe`, `hunter-visual`). Minimum fields you require to start:

- `sign_id` — stable id, e.g. `sign/0f2c`
- `surface` — the addressable unit (route, endpoint, command, control)
- `observed` — what happened, as observed, not inferred
- `raw_steps` — the sequence that produced it, however long or noisy
- `authority` — source of the expectation: `implicit` (universal correctness),
  `spec:<file>:<line>` (declared intent), or `baseline:<id>` (observed intent)

If `authority` is absent you cannot state an expectation, and without a stated
expectation you cannot promote. Resolve authority first or escalate via
`hunter-ask`.

## Outputs

Exactly one of:

- A **Trail** (schema below) written to `trail/<id>/` plus a Find record — when
  all promotion gates pass.
- An **updated Sign** with `promotion_failed` and the specific gate that failed —
  when any gate is unmet. This is published; it is evidence the ladder works.

## The reproduction protocol

Run these steps in order. Do not reorder. Each step has a fail-closed exit.

### 1. Isolate preconditions

List every state the `raw_steps` depend on, then test each by removing it and
re-running. Precondition classes to probe explicitly:

- Auth/session state (logged-in user, role, token)
- Seed/fixture data (a specific row, count, or record must exist)
- Prior actions in the same session (order dependence)
- Clock/date, timezone, locale
- Feature flags, config values, environment variables
- Concurrent load or a second actor

For each precondition, record `required` or `irrelevant` with the run that
proved it. A precondition you assumed but never tested is a fabrication — do not
list it as required unless removal changed the outcome.

### 2. Minimise the trigger

An unminimised repro is much harder to fix, because the fixer cannot tell which
of twelve steps matters. **Minimise before promoting.** Use delta debugging:

1. Split `raw_steps` in half. Run the first half against the isolated
   preconditions. If the deviation still reproduces, discard the second half.
2. Repeat on the surviving half until removing any single step makes the
   deviation disappear.
3. For inputs (payloads, argv, form values), shrink each field toward its
   simplest value that still triggers the deviation: shorten strings, zero
   numbers, drop optional keys.

Stop when the case is **1-minimal**: every remaining step and field is load-
bearing, proven by the fact that removing it kills the repro. Record the
minimisation as a shrink log (`raw_steps` count → `min_steps` count) so the
fixer sees the reduction.

Never minimise past the point of reproduction. If shrinking makes it flaky, you
have crossed into a timing or ordering dependence — go to the flake taxonomy.

### 3. Execute twice, independently

Run the 1-minimal case twice with **independent setup**: fresh process, fresh
browser context or HTTP client, fresh temp dir, re-seeded fixtures. Two runs
sharing a warm cache or a dirty database is one run, not two.

Independence checklist per run:

- New process / new context (not a re-request on a live session)
- State reset to the recorded precondition set between runs
- Same environment fingerprint (§ below) — differences are variables, not noise

### 4. Apply the tiebreak rule

- **2 of 2 agree** → the deviation is confirmed. Proceed to write the Trail.
- **1 of 2 disagree** → you have not found nothing; you have found non-
  determinism. Run a **third** time. Do not average, do not pick the run that
  supports your hypothesis.
  - **3rd matches the deviation (2/3)** → promote as a Find with class
    `intermittent`, `observed_rate: "2/3"`. Intermittency is itself a deviation.
  - **3rd matches clean (1/3)** → run the flake taxonomy to attribute the one
    failing run. If it attributes to a real cause (state leakage, resource,
    network), promote with that class and rate. If it attributes to genuine
    non-determinism you cannot control, promote as `intermittent` with the
    observed rate and the taxonomy result recorded. It never silently becomes a
    Sign again — intermittency is a Find, stated as a rate.

Never report a raw fraction without its denominator. `2/3`, never "usually".

## Flake taxonomy

When runs disagree, attribute the disagreement before promoting. Each class has
a distinguishing test — run it, record the result.

| Class | Symptom | Distinguishing test |
|---|---|---|
| Timing | Fails when the system is fast/slow; passes when latency shifts | Replace every wait with a state assertion; if it stabilises, it was a fixed-sleep race, not the target |
| Ordering | Fails only after a specific prior step or test | Run the minimal case in isolation with a fresh process; if it passes alone but fails in sequence, it is ordering |
| State leakage | Fails on second run, passes on first (or vice versa) | Reset all state between runs (db, cache, tmp, session); if the disagreement vanishes, it was leakage |
| Network | Fails intermittently with connection/timeout errors | Re-run with the network path held constant (same host, retry disabled); attribute to the dependency if only network-path runs fail |
| Resource | Fails under memory/fd/disk/CPU pressure | Re-run in isolation with resources free; if it passes, capture the pressure condition as the precondition |
| Genuine non-determinism | Fails at a stable rate with all above controlled | After the four controls above hold constant and it still varies, it is genuine — promote as `intermittent` with the rate |

Attribution matters because the fix differs per class: a timing flake is fixed
by asserting on state, a leakage flake by isolating state, a genuine flake by
finding the unseeded randomness. Record `flake_class` on the Trail even when the
result is confirmed 2/2 (value `none`), so the fixer knows you checked.

## Environment fingerprint

Two runs are only comparable if their environments match. Capture and store the
fingerprint with every Trail:

- OS + arch (`uname -sm`)
- Runtime versions of every language/tool in the path (node, python, the binary
  under test — exact versions)
- Relevant env vars (redact secret values; record the key and that it was set)
- Container image or host identity
- Seed(s) used for any randomised input
- Wall-clock start (ISO-8601 with timezone) and duration per run

A Trail without a fingerprint is not replayable and is therefore a Sign.

## Trail artifact schema

Write to `trail/<id>/trail.json`. Artifacts referenced by relative path within
the same directory. This is the durable, addressable record — not prose.

```json
{
  "trail_id": "trail/A31",
  "sign_id": "sign/0f2c",
  "surface": "POST /session",
  "hunt_mode": "defect",
  "authority": {
    "kind": "implicit",
    "source": null,
    "quote": null
  },
  "observed": "returns 500 on valid credentials",
  "expected": "returns 200 with a session token",
  "min_steps": [
    "POST /session with body {\"email\":\"a@b.co\",\"password\":\"x\"}"
  ],
  "shrink_log": { "raw_step_count": 7, "min_step_count": 1 },
  "inputs": { "body": "@artifacts/request.json" },
  "preconditions": [
    { "state": "user a@b.co exists, verified", "verdict": "required",
      "proven_by": "run-1" },
    { "state": "cart contains 1 item", "verdict": "irrelevant",
      "proven_by": "run-0" }
  ],
  "env_fingerprint": {
    "os_arch": "Linux aarch64",
    "runtimes": { "node": "20.11.1", "postgres": "16.2" },
    "env_keys_set": ["DATABASE_URL", "SESSION_SECRET"],
    "container": "hunter-range:2026-08-07",
    "seeds": { "faker": 4242 }
  },
  "confirmations": [
    { "run": "run-1", "at": "2026-08-07T14:02:11Z", "outcome": "deviation",
      "artifact": "artifacts/run-1-response.json" },
    { "run": "run-2", "at": "2026-08-07T14:02:19Z", "outcome": "deviation",
      "artifact": "artifacts/run-2-response.json" }
  ],
  "observed_rate": "2/2",
  "flake_class": "none",
  "artifacts": [
    "artifacts/request.json",
    "artifacts/run-1-response.json",
    "artifacts/run-2-response.json",
    "artifacts/stderr.log"
  ],
  "severity": "CRITICAL",
  "created_at": "2026-08-07T14:02:25Z"
}
```

Field rules:

- `confirmations` must contain **≥2 entries with `outcome: "deviation"`** (or
  the 3-run pattern for `intermittent`). Fewer is a Sign.
- `expected` must be non-null and traceable to `authority`. For `conformance`,
  `authority.quote` is the spec text quoted verbatim with `source` as
  `file:line`.
- Every path in `artifacts` must exist on disk. A referenced-but-absent artifact
  is a fabrication and fails promotion.
- `severity` uses the probe skill's scale; do not invent a scale here.

## Promotion gate — check before writing a Find

- [ ] Preconditions isolated; each `required`/`irrelevant` proven by a run
- [ ] Trigger minimised to 1-minimal; shrink log recorded
- [ ] Executed twice with independent setup; fingerprint identical
- [ ] Tiebreak satisfied (2/2, or 3-run resolution with a stated rate)
- [ ] Flake class attributed (`none` counts, and means you checked)
- [ ] ≥2 durable artifacts on disk, each referenced by relative path
- [ ] `expected` stated and traced to a named `authority`
- [ ] `env_fingerprint` complete

Any unchecked box: emit an updated Sign with `promotion_failed: "<gate>"`. Do
not write a Find.

## Handoff

- A completed Trail is consumed by the report layer (brand-system §12 §3 Finds)
  and by `hunter replay <find-id>`, which re-executes `min_steps` against the
  recorded fingerprint. If replay does not reproduce, the Find is defective —
  return it here for re-work, never soften it into a Sign silently.
- Unpromoted Signs flow to the report's "Signs not promoted" section (§12 §4)
  with their `promotion_failed` reason.

## Never

- **NEVER** promote from a single execution. One-shot observations are Signs.
- **NEVER** average disagreeing runs or select the convenient one.
- **NEVER** reference an artifact you did not capture, or a precondition you did
  not test by removal.
- **NEVER** promote an unminimised repro when minimisation was possible; state
  the reason if a case is genuinely irreducible.
