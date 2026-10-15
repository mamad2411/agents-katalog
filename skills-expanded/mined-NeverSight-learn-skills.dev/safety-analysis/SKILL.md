---
name: safety-analysis
description: >-
  Analyze and test software safety for the ISO/IEC 25010:2023 Safety characteristic
  (operational constraint, risk identification, fail safe, hazard warning, safe
  integration) — new in the 2023 edition. Use when: "safety," "安全性," "fail-safe,"
  "safe state," "guardrails," "kill switch," "hazard analysis," "FMEA," "what happens
  if this destructive action fires by mistake," or building systems that can harm
  people/property/environment or perform irreversible actions. Produces a hazard
  analysis + safety test plan (design mode) and fail-safe / guardrail tests
  (implementation mode). For regulated safety-critical domains, defers to functional
  safety standards. Not for: recovery/availability after infrastructure faults (DB/node
  down) — use reliability-testing; or security-from-attackers — use security-testing.
  Related: reliability-testing, security-testing.
license: MIT
metadata:
  version: "1.0"
  iso25010: [safety]
  mode: [design, implementation]
---

# Safety Analysis

Verify the system stays within safe operating limits, fails into a safe state, and
warns before harm — the ISO 25010:2023 characteristic added because reliability and
security don't cover "what if correct-but-harmful behavior occurs."

## Objective

Coverage of the five ISO 25010:2023 Safety sub-characteristics — **operational
constraint**, **risk identification**, **fail safe**, **hazard warning**, **safe
integration** — scaled to the product's actual hazard potential. The failure mode this
prevents: a system that reliably and securely does something harmful (mass-deletes
data, over-charges, actuates a device past a safe limit) because no one defined the
safe envelope.

## ⚠️ Disclaimer — read before anything else

**LLM-generated hazard analysis, FMEA, and safety tests are a first-draft aid only.
They are NOT a substitute for a certified functional-safety process or a qualified
safety engineer, and must never be treated as safety assurance on their own.** In any
regulated or safety-critical context (medical, automotive, industrial control,
avionics, energy), every safety artifact and test result this skill produces MUST be
reviewed, corrected, and signed off by a **qualified functional-safety engineer** under
the governing standard (IEC 61508 / ISO 26262 / IEC 62304 / DO-178C) before it is
relied upon. When hazard potential is unclear or the domain may be regulated, **escalate
to a human safety owner — do not ship on the strength of this skill's output.** This is
the one skill in this library whose over-trusted output can lead to real-world harm.

## Applicability — read first

Safety in ISO 25010 is a **product-quality attribute** (how safely the product
behaves), distinct from process/certification **functional-safety standards**.

- **Regulated safety-critical domains** (medical, automotive, industrial control,
  avionics, energy — anything that can expose life/property/environment to
  unacceptable risk): this skill does **not** replace the governing standard. Defer to
  **IEC 61508** (general), **ISO 26262** (automotive), **IEC 62304** (medical device
  software), or **DO-178C** (avionics). Use ISO 25010 Safety as a quality-model overlay
  on top of that regulated process.
- **Typical web/SaaS** (no physical actuation): apply the subcharacteristics in their
  **soft form** — operational constraint = rate limits/guardrails/circuit breakers;
  fail safe = safe defaults, graceful degradation, kill switches, feature-flag
  rollback; hazard warning = alerting + confirm-before-destructive-action. Full
  risk-identification/safe-integration rigor is usually not warranted; say so rather
  than manufacturing ceremony. (This tiering is engineering judgment; ISO does not
  classify subcharacteristics by domain.)

If the product has no meaningful hazard, record that conclusion and stop — don't
generate safety theater.

## Context Discovery

- **Hazard potential**: what real-world harm can this system cause — physical,
  financial, data-loss, privacy, irreversible actions? This sizes the whole effort.
- **Irreversible/destructive actions**: enumerate them (bulk delete, payments,
  deployments, device commands) — each needs a guardrail and a confirmation/undo story.
- **Regulatory context**: any domain safety standard in force? If yes, that governs.
- **Existing safeguards**: rate limits, circuit breakers, feature flags, confirmations,
  monitoring already present.

## Instructions

1. **Hazard analysis / FMEA** (risk identification): enumerate failure modes and their
   effects; rank by severity × likelihood × detectability. Each unacceptable risk
   yields a safety requirement to test.

2. **Operational-constraint tests**: drive inputs beyond the safe envelope and confirm
   the system clamps, rejects, or refuses to proceed (rate limits hold, quotas enforce,
   out-of-range commands are denied) rather than acting on them.

3. **Fail-safe tests**: inject faults and verify the system autonomously enters/reverts
   to a defined safe state (safe default, graceful degradation, halt) rather than an
   undefined or harmful one. A kill switch / feature flag must actually revert behavior.

4. **Hazard-warning tests**: confirm warnings/confirmations fire before irreversible
   actions, in time, with correct severity, and reach the operator (destructive
   operations require explicit confirmation; alerts trigger on threshold breach).

5. **Safe-integration tests**: verify safety properties still hold across component/
   version boundaries after integration — an upgraded dependency must not silently
   remove a guardrail.

6. **Trace each test to a hazard**: every safety test cites the hazard (FMEA row) it
   mitigates, for auditability.

## Output Format

### design mode

```
# Safety Analysis: {system}
## ⚠️ Disclaimer & sign-off (MANDATORY, place at top)
   - "Draft safety analysis generated with AI assistance — NOT certified safety
      assurance. Requires review and sign-off by a qualified functional-safety
      engineer under {governing standard} before use."
   - Sign-off: [ ] Functional-safety owner: __________  Date: ______  Standard: ______
## Applicability decision (hazard potential; regulated standard in force?)
## Hazard Analysis / FMEA
   | Hazard ID | Failure mode | Effect | Sev | Likelihood | Detect | Mitigation | Test |
## Safety requirements by sub-characteristic
   (operational constraint / fail safe / hazard warning / safe integration)
## Destructive-action guardrail inventory (action → guardrail → confirm/undo)
```

### implementation mode

Guardrail / fail-safe tests assert the *safe* outcome. Example — a destructive bulk
op must refuse beyond a safe limit and require confirmation:

```ts
test('bulk delete refuses beyond safe limit', async () => {
  const res = await api.post('/admin/bulk-delete', { ids: makeIds(10_001) });
  expect(res.status).toBe(422);                 // operational constraint: clamp
  expect(res.body.error).toBe('EXCEEDS_SAFE_LIMIT');
});

test('destructive action requires explicit confirmation token', async () => {
  const res = await api.post('/admin/wipe', { confirm: false });
  expect(res.status).toBe(400);                 // hazard warning / fail safe
});
```

For fault-driven fail-safe behavior, coordinate with `reliability-testing` fault
injection and assert the resulting state is the defined *safe* one.

## Anti-Patterns

- **Safety theater** — generating FMEA ceremony for a product with no real hazard.
  **Guard:** make the applicability decision first; low-hazard products get guardrails,
  not a 40-page analysis.
- **Reinventing regulated standards** — hand-rolling safety tests for a medical/
  automotive component. **Guard:** in regulated domains defer to IEC 62304 / ISO 26262 /
  IEC 61508 / DO-178C; ISO 25010 is an overlay, not a substitute.
- **Happy-path safety** — testing that the guardrail allows valid input, never that it
  blocks the dangerous one. **Guard:** every guardrail has a test that drives it past
  the limit and asserts refusal + safe state.
- **Confirmation as UI-only** — a client-side "Are you sure?" the API doesn't enforce.
  **Guard:** the safe check lives server-side; test the API directly, bypassing the UI.
- **Conflating safety with security/reliability** — safety is harm from the system's
  own behavior, not attackers or faults alone. **Guard:** keep the hazard (harm to
  people/property/data) as the unit of analysis.

## Related Skills

- `reliability-testing` — fault injection drives the failures that fail-safe tests
  assert a safe state for; safety adds "is that state *safe*," not just "recovered."
- `security-testing` — protection from malicious actors; safety is harm from the
  system's own operation.

## References

- ISO/IEC 25010:2023 — Safety (operational constraint, risk identification, fail safe, hazard warning, safe integration)
- Functional-safety standards (regulated domains): IEC 61508, ISO 26262 (automotive), IEC 62304 (medical), DO-178C (avionics)
- Techniques: FMEA / hazard analysis, fail-safe state testing, operational-limit testing
