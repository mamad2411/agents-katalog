---
name: gate-engineering
description: "Design, implement, review, or repair durable quality gates such as linters, CI checks, tripwires, corpus detectors, contract suites, and snapshot or golden tests. Use when asked to add a check that catches a defect, when a recurring defect needs class-wide prevention, when a gate is being trusted or recalibrated, or when all-green output may be misleading."
metadata:
  version: 0.2.0
---

# Gate Engineering

Build standing quality nets that prove they detect intended defect class.

## Scope

This skill applies to persistent repository gates: lint rules, CI checks, tripwires, contract suites, corpus detectors, and golden tests. Ordinary unit tests written with a feature do not each need full gate ceremony.

## Core rule

A gate never observed failing is unproven. Ship known-bad input, known-good twin, and repeatable way to prove catch.

## Five laws

1. **Prove red, then green.** Seed representative defect and observe non-zero failure. Fix it and observe pass. Preserve both fixtures and expose `--selftest` or equivalent deterministic command.
2. **Fix classes, not instances.** Recurrence turns one reported case into corpus problem. Detect class, scan full owned corpus, fix all findings, then keep detector as gate.
3. **Keep fixtures hermetic.** Commit inputs. Avoid live database, mutable cache, network, current date, or content SHA dependencies unless gate explicitly tests those boundaries.
4. **Assert contract, not incidental snapshot.** Prefer invariant such as presence, range, mapping, ordering, or semantic label. Byte-exact and pixel-exact snapshots need clear reason and controlled update process.
5. **Audit consumers.** Producer validation does not protect cached, read, import, or alternate write paths. Enumerate bypasses and gate contract where consumers can violate it.

## Assertion traps

- Assert presence before uniqueness – zero matches are trivially unique.
- Assert selection is non-empty before `all(...)` or universal validity.
- Ensure failure fixture reaches code path under test rather than being filtered earlier.
- Include near-miss good fixture so detector does not encode broad false positives.
- Test disabled or feature-flagged path by toggling it in controlled run.

## Gate lifecycle

- Recalibrate baseline after legitimate behavior change; do not weaken invariant to make CI green.
- Re-enable disabled gate only after current corpus passes it.
- Refresh tripwire baseline with producer or consumer refresh that changes expected truth.
- Match gate cadence to data cadence.
- Version fixture schema when parser or contract changes.
- Record scoped skip with owner and expiry; never silently disable.

## Implementation workflow

1. Name defect class in one sentence.
2. Locate producer, readers, caches, alternate writers, and current checks.
3. Create minimal bad and good fixtures.
4. Implement detector against contract.
5. Run red fixture and capture expected failure.
6. Run green fixture and capture pass.
7. Run detector across full owned corpus.
8. Fix findings or document scoped exceptions.
9. Wire gate into repository's existing check path.
10. Add selftest and prove selftest itself fails if catch is removed.

## Proof block

Include with change:

```text
Gate: <name and path>
Defect class: <what it catches>
Seeded red: <fixture> -> <failure output>
Green twin: <fixture> -> <pass output>
Selftest: <command>
Corpus result: <scope and finding count>
Consumer audit: <readers, caches, alternate writers>
Exceptions: <none or explicit list>
```

## Review checklist

- [ ] Known-bad fixture committed and observed red.
- [ ] Known-good and near-miss fixtures observed green.
- [ ] Selftest deterministic and hermetic.
- [ ] Assertions describe contract rather than current formatting.
- [ ] Empty-set and filtered-out traps covered.
- [ ] Full owned corpus scanned.
- [ ] Read, cache, and alternate write paths audited.
- [ ] Baseline update explained by changed truth.

## Stop conditions

- Gate has no red proof: treat its green history as no evidence.
- Request is only to disable gate: propose repair, recalibration, or scoped expiring exception.
- Correct assertion requires unstable live state: separate deterministic contract gate from operational monitor.

## Related skills

- `verify-honestly` governs claims about gate coverage.
- `retro-distill` identifies recurring failures worth promoting into gates.
