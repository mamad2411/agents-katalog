---
name: double-check
description: Rigorously review the work for defects, fix what's safely fixable, verify, and end with a confidence rating out of 10. Hunts careless slips, code-quality issues, logic gaps, intent-vs-execution mismatches, and edge cases. An audit-and-fix pass over existing work, not a fresh build.
---

# double-check

Scrutinize the work for anything wrong — silly slips, bad code, logic gaps, things that don't make sense, edge cases — then **fix what's safely fixable, verify it, and rate your confidence out of 10.** This is an active audit: investigate → plan → fix → verify, not just a list of complaints.

## Scope
Default: the work just done — the current changes (`git diff` if available) and the files touched this session. If the user names a target (file, folder, feature), scope to that. Investigate the **actual** code; never assume it's fine because it "looks" right.

## The five review lenses
1. **Careless errors (correctness slips)** — wrong file paths, incorrect folder/directory references, typos, wrong variable/function names, copy-paste leftovers, off-by-one, mismatched identifiers, stale comments. The small stuff that silently breaks things.
2. **Code quality / maintainability** — hold a clean-code bar: one function = one responsibility (split it if it does two things), intention-revealing names, **no boolean flag arguments** (a function that switches behavior on true/false is two functions in disguise), the simplest thing that works, no dead code, a 1–2 line header on each file. Flag duplication and needless complexity.
3. **Logic gaps (unhandled conditions)** — the divide-by-zero class: missing guards, absent error handling, null/empty/missing inputs, failure paths real users *will* hit. These map to concrete ways the program falls over in real use.
4. **Coherence (intent vs. execution)** — does what was built actually achieve the stated goal? Catch the cases where the implementation does something different from what was intended, or solves the wrong problem. More general than #3 — can be about the idea or the approach, not just the code.
5. **Edge cases & boundaries** — enumerate **all** plausible ones: empty/null, min/max limits, concurrency/races, latency/timeouts, very large input, unicode/encoding, offline/permission failures, unexpected order. Some only surface with real testing or data — predict them anyway.

## Procedure — do the work, don't just report it
1. **Review** — read the real code/files across all five lenses; gather findings.
2. **Plan** — rank findings by severity (breaks things · should fix · minor). Decide which fixes are **safe and easy to apply now** vs. which to only flag (risky, large, or needing real test data).
3. **Fix** — apply the safe, clear fixes. For edge cases: fix the cheap/safe ones; **list** the rest with why they're deferred. Don't make risky or large changes without surfacing them first.
4. **Verify** — actually confirm each fix: run it, run tests, or trace the logic. Make sure nothing regressed. State what you verified and how.
5. **Report** — concise: what was found, what you fixed, what's still open (and why). Point to locations (`file:line`), don't dump full files.

## Always end with the confidence rating (last line, no preamble)
After everything, output exactly this — no lead-in sentence:

**Confidence: N/10** — code works as intended, flaw-free, across edge cases.

If below 10, add one short line naming the single biggest remaining risk. Nothing more.

Rough anchor: **10** = exhaustively verified, nothing left; **7–9** = solid, only minor/unlikely edges unverified; **4–6** = happy path works, real gaps remain; **1–3** = likely broken or unverified.
