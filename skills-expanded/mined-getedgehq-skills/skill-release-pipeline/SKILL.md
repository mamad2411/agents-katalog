---
name: skill-release-pipeline
description: Take an Agent Skill from a concrete user problem through package creation, behavioral evaluation, evidence binding, and publication. Use when asked to build and publish a new skill, turn a skill idea into an evaluated release, or run the full Edge skill release workflow.
---

# Skill Release Pipeline

Ship a reproducible package and an honest result, not a folder plus a marketing claim.

## Release contract

1. Name one real job and the observable behavior the skill should improve.
2. Check the target repository for an incumbent with the same trigger. Evaluate against that incumbent when one exists, not an empty baseline.
3. Build the smallest package that can change the target behavior. Keep deterministic operations in `scripts/` and conditional detail in `references/`.
4. Run static gates before spending model calls: strict front matter, package tests, secret scan, license and provenance checks, and exact file hashes.
5. Create representative tasks from real work. Separate authoring cases from held-out cases. Make the verifier fail a known-bad output and pass both short and thorough known-good outputs.
6. Use the repository's `skill-eval-loop` for blind paired runs. Require at least three valid pairs for an adoption decision. Use more tasks when the public claim depends on a confidence interval.
7. Confirm that the treatment actually loaded the candidate. A run where it did not load is invocation evidence, not quality evidence.
8. Publish the package identity, task definitions, outputs, verifier results, grader verdicts, failures, and limitations. Raw private inputs remain local unless the user explicitly approves disclosure.
9. Publish the observed status even when it is negative or inconclusive. Never convert a smoke test, launch review, or attractive example into an efficacy claim.
10. Merge only after CI passes, an independent review finds no blocking issue, and the public record identifies the exact shipped package hash.

## Result states

- `supported`: the predefined statistical gate passes and no safety or package gate fails.
- `inconclusive`: the run completed but the predefined evidence bar was not reached.
- `negative`: the baseline performed materially better or the candidate introduced a blocking regression.
- `not_run`: no controlled comparison exists.
- `invalid`: parity, loading, blinding, or verifier integrity failed.

After every package or evidence change, run `scripts/refresh_derivation.py <skill-directory>`, then run `scripts/release_check.py <skill-directory>`. The first command binds the release record to the exact bytes on disk. The second fails closed on inventory drift, hash drift, malformed metadata, invalid result states, and common secret patterns. Neither replaces behavioral evaluation or human review.

Publishing to GitHub, GetEdge, a package registry, or social media is an external action. Use authorization from the current request only for the destinations it actually covers.
