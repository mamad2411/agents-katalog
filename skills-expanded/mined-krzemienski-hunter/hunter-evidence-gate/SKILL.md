---
name: hunter-evidence-gate
description: >-
  The enforcement arm of the doctrine: the gate that decides whether any claim
  may leave an agent's hands. Run this whenever you are about to emit a verdict,
  promote a Sign to a Find, accept a subagent's result, or write anything into a
  report that asserts a surface passes, works, is fixed, is clean, or is
  covered. It runs the verification loop (identify claim type, identify required
  evidence, personally open the artifact, match evidence to criterion, emit
  verdict with citation), enforces the claim-type to required-evidence matrix,
  forbids accepting a subagent verdict without opening its artifact, flags
  red-flag phrases that mark ungrounded claims, and downgrades rather than
  assumes when evidence is missing. Load before any promotion, verdict, report
  section, or completion claim.
allowed-tools: Read, Bash, Grep, Glob, View
---

# Hunter Evidence Gate

Assumes `hunter-doctrine` is loaded. The doctrine states the Law; this skill is
the checkpoint that refuses to let a claim past unless the Law is satisfied. It
runs between pipeline stages and before every emission.

## What this gate governs

Any *claim*. A claim is any statement that would change a reader's belief about
the target: a verdict, a Sign→Find promotion, a "this surface is cold", a
coverage fraction, a "the patch fixes it", a completion report. If it asserts
something about the quarry, it passes through this gate first.

The Law, restated as the gate's single question:

> Can I, right now, open the artifact that proves this claim and point to the
> line in it that matches the criterion? If not, the claim does not leave.

## The verification loop

Run this loop for every claim. No step is skippable, and step 3 is the one that
is always tempting to skip.

```
1. IDENTIFY the claim and its type          (what is being asserted, and in which class)
2. IDENTIFY the required evidence           (from the matrix below — the exact artifact)
3. OPEN the artifact yourself               (read/view the bytes; do not trust a summary)
4. MATCH evidence to the criterion          (does the artifact actually show it? at which line/frame?)
5. EMIT the verdict with a citation         (verdict + coverage fraction + artifact id + locus)
```

Step 3 is literal. "Personally examine the artifact" means: read the file, view
the screenshot and describe what is visible, quote the exact stdout line, open
the HTTP exchange. A claim backed by an artifact you have not opened is
ungrounded, regardless of who produced the artifact.

## Claim-type → required-evidence matrix

For each claim type, the artifact you must open in step 3 and the criterion you
match in step 4. Anything less than the required evidence downgrades the claim
(see the downgrade procedure) — it does not get the benefit of the doubt.

| Claim type | Required evidence (must open) | Match criterion |
|---|---|---|
| "Find" (deviation reproduced) | Durable artifact per probe class from doctrine (screenshot / full HTTP exchange / argv+exit+stdio / query+resultset / stack trace) AND a second independent run's artifact | Same deviation visible in ≥2 runs; expectation and its source named |
| "Sign promoted to Find" | All five doctrine promotion boxes, each with its artifact | Every box checkable against an opened artifact; if one is missing it stays a Sign |
| "surface is cold" (probed, clean) | The probe's execution record: what ran, its inputs, its captured output showing no deviation | A probe actually executed against this surface and its oracle returned no deviation — not "I read it and it looks fine" |
| "surface is dark" | The surface-map entry and the reason it was not probed | Surface exists in the map; a stated reason it was skipped |
| "coverage is N/M" | The surface map (denominator M) and the probe log (numerator N) | N = surfaces with an execution record; M = total surfaces in the map; both counted, not estimated |
| "tests pass" | Fresh test-runner output from this session | Exit 0, explicit failure count 0, no silent skips masking failures |
| "build succeeds" | Fresh build output | Exit 0; quote the success line |
| "the patch fixes it" | Replay of the original reproduction against the patched system, ≥2 runs | Original symptom no longer reproduces; anti-mock scan clean (hand to `hunter-anti-mock`) |
| "verdict: PASS / FAIL / ..." | Every claim the verdict aggregates, each already gated | Verdict is from the §6 closed set and matches the aggregate; coverage fraction attached |
| Conformance deviation | The spec line quoted verbatim with file:line, beside the observed behaviour artifact | Observed behaviour contradicts the quoted authority |

If a claim type is not in this table, do not invent evidence for it — map it to
the nearest row or escalate via `hunter-ask`.

## Reviewing subagent evidence

Subagents produce evidence. They do not produce verdicts you may forward.

**The rule: never accept a subagent's verdict without opening its artifact.**
A subagent reporting "10/10 probes passed, surface cold" is providing an
evidence *location*, not a proven claim. You run the verification loop against
its artifacts exactly as if you had produced them:

- Take the artifact id / path the subagent returned.
- Open it (step 3). If the path is missing, unreadable, or empty, the subagent's
  claim is downgraded to `VERIFICATION-PENDING` and returned, not accepted.
- Match its content to the criterion (step 4). A subagent's "PASS" with a
  screenshot that shows an error state is a FAIL, and your reading governs.
- If the subagent asserted a Find, re-check the two independent runs are
  genuinely present and genuinely independent, not the same capture twice.

A subagent's confidence, tone, or self-reported count is not evidence. Only the
artifact is. This is the same loop the doctrine's Sign→Find ladder runs; the
gate just refuses to let delegation launder an ungrounded claim into a grounded
one.

## Red-flag phrases

If a draft claim (yours or a subagent's) contains any of these, stop — it marks
a claim that skipped step 3. Replace the phrase with an opened artifact or
downgrade the claim.

| Phrase | What it usually hides | Do instead |
|---|---|---|
| "should pass", "should work" | no execution happened | run it; cite the output |
| "looks like", "seems to", "appears" | reading substituted for observing | probe it; attach the artifact |
| "probably clean", "likely fine" | a dark surface dressed as cold | mark it dark or probe it |
| "the agent reported success" | subagent verdict accepted unopened | open the subagent's artifact |
| "detected" | passive, unproven | "reproduced" / "observed", with the capture |
| "all good", "no issues" | coverage-free cleanliness | state N/M and the dark count |
| "I assume", "presumably" | fabrication risk | do not assume — downgrade |
| "should be fixed now" | patch not replayed | replay original reproduction ≥2× |

These map directly to the banned/hedging vocabulary in the brand system §4–§5.

## When evidence is missing: downgrade, never assume

The absence of an artifact is never evidence of cleanliness. When step 3 finds
no artifact, or step 4 fails to match:

1. **Do not fabricate** the missing artifact, count, or citation (anti-fabrication law).
2. **Downgrade** along the honest ladder:
   - Missing reproduction/second run → the claim is a **Sign**, not a Find.
   - Probe never executed on the surface → the surface is **dark**, not cold.
   - Evidence collection incomplete mid-run → **`VERIFICATION-PENDING`**
     (allowed mid-run, forbidden in a delivered report).
   - An axis never exercised → **`NOT-COVERED`** with the reason.
3. **Record the gap** with its reason so the report can publish it. An honest
   gap is a usable result; a guessed pass is unrecoverable.

Downgrading is the correct, expected behaviour of a working gate. A gate that
never downgrades anything is not verifying — it is rubber-stamping.

## Coverage-fraction requirement

No verdict leaves this gate without its coverage fraction attached, and the
fraction is a real numerator over a real denominator:

- **Denominator M** = total surfaces in the surface map from `hunter-recon`.
  Never the count of surfaces you happened to try.
- **Numerator N** = surfaces with an execution record you opened.
- Render `N/M` adjacent to the verdict. `PASS` requires `N = M`. Any `N < M`
  downgrades to `PASS (LIMITED COVERAGE)` and requires the dark list.

A verdict without a fraction is incomplete output and does not pass the gate.

## Zero-find review block

If a hunt reaches this gate with zero Finds, the gate does not emit a success
verdict. It requires a `zero_find_review` block, and refuses the emission until
every field is answered from opened artifacts:

```json
{
  "zero_find_review": {
    "preflight_outcome": "ready",
    "preflight_artifact": "preflight.json",
    "probes_executed": 78,
    "probes_with_output": 78,
    "coverage": "78/78",
    "dark_surfaces": 0,
    "oracles_attached": true,
    "oracle_artifact": "method/oracle_registry.json",
    "harness_silent_failure_ruled_out": true,
    "note": "0 finds across 78/78 surfaces; oracles verified attached; flagged for human review"
  }
}
```

Zero finds across low coverage, or with any field unverifiable, is not a clean
result — it is a suspected broken hunt. Render the review prompt, never a
success state (brand §10 zero-find protocol).

## Emission format

Every emitted claim carries its pointer, per the doctrine citation format:

```
<observation> — <confirmation count> · <artifact id> [· <authority for conformance>]
login: POST /session returns 500 on valid credentials — 2/2 · trail/A31
cart total excludes tax — 2/2 · trail/B07 · spec: pricing.md:L142 "totals include tax"
checkout: PASS (LIMITED COVERAGE) — 41/78 surfaces · 37 dark · coverage_map.json
```

## Hand-off

- Promotions cleared here go to `FINDS.json`; unpromoted Signs go to
  `SIGNS.json` with their failure reason for the report's "Signs not promoted"
  section.
- A "the patch fixes it" claim is NOT cleared here alone — hand the diff to
  `hunter-anti-mock` first; a patch that suppresses detection fails the gate
  regardless of a green replay.
- Cleared verdicts and their coverage fractions feed the report builder in the
  fixed order (coverage map before finds).

## Self-check before emitting anything

- [ ] Ran the five-step loop; step 3 opened the actual artifact
- [ ] Claim type mapped to the matrix; required evidence present and matched
- [ ] No subagent verdict forwarded without opening its artifact
- [ ] No red-flag phrase survives in the emitted text
- [ ] Every missing artifact produced a downgrade, not an assumption
- [ ] Verdict from the §6 closed set, adjacent to a real N/M fraction
- [ ] Zero-find results carry a fully answered `zero_find_review` block
