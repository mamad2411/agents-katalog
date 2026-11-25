---
name: verify-harness-capability
description: Drive an agent tool beside a deliberately broken control to establish whether it enforces, follows or ignores a capability. Use before claiming or changing a capability-matrix cell, and when a generated surface seems accepted but does nothing.
metadata:
  internal: true
---

<!-- cockpit:verified version=0.0.0 -->

# Verify a harness capability

**This skill is for developing cockpit; cockpit does not ship it to consumers.**

A capability-matrix cell is one of four states, and only driving the tool tells them apart:

- **enforced**: the tool refused the forbidden operation, and you hold its refusal.
- **instructed**: the guidance reached the agent and nothing would stop it acting otherwise. This is
  a legitimate state; hiding it inside "supported" is the defect this skill exists to prevent.
- **generated**: cockpit writes the files, but no run has shown the tool loads them.
- **unavailable**: the tool offers no mechanism, so cockpit emits nothing for the cell. A line that
  reads as a control and enforces nothing is worse than its absence, because the next reader
  budgets for a control that is not there.

Reading the tool's docs or symbols, or watching it accept a config file, establishes none of them:
several cells across three harnesses accepted the configuration, reported no error, and bound
nothing.

## The method

1. **Write the real file and a deliberately broken twin in the same directory.** Silence about
   your file means nothing unless the broken one is named in the same run. Done when both files
   exist and the twin differs from the real one only in what should make the tool reject it.
2. **Drive the tool for real**, headless, through the capability itself rather than by asking the
   tool to describe itself: self-report is the least reliable signal there is. Done when the run
   names the broken twin, by an error, a warning or a skip it reports. If it never does, the tool
   did not scan the directory, and the run measures nothing; change the setup and rerun.
3. **Attempt the thing the capability forbids.** A read-only restriction is proved by trying to
   write and being refused, and a guard by the protected operation failing while an unprotected one
   in the same run succeeds. Done when you hold the refusal, or the operation's success.
4. **Record what you saw.** Note the tool's exact version (`<tool> --version`), the date, the
   invocation, and the observed result for both files. A measurement of one version is a claim
   about that version only. Done when someone else could rerun it from your notes.

## Then

1. Update the cell in `packages/cockpit/src/surfaces/harness-registry.ts` with its state, the date,
   the version and a provenance line saying what the run showed, then run `npm run references`,
   which renders `docs/capability-matrix.md` from it. Done when the regenerated page shows the new
   measurement.
2. If the run contradicts a cell that was claimed without a measurement, add the fixture or test
   that would have caught it, and correct every doc and shipped skill that repeats the old claim.
   Done when that test fails on the old claim.
