# Red-Proof Skill

> Task-scoped skill for Goal 3b triad verification: adversarial sabotage proofs
> that fail closed and restore cleanly.

## When to mount

Mount this skill when running QA Red-Proof Sabotage for any wave
(see `docs/prompts/verify-stage.md` section 1c).

## Protocol

1. Record the green baseline: `bun test` and `bun run check` both exit 0.
2. Sabotage exactly one byte of the wave's core invariant:
   - Wave 1: prepend a role name at byte 0 of the frozen prefix.
   - Wave 2: add a 4th tool to the `tools/list` response.
   - Wave 3: flip one byte inside a locked skill directory.
3. Confirm the matching test file FAILS with exit code >= 1.
4. Restore cleanly (`git checkout -- <file>`) and confirm green again.
5. Append the full transcript to `docs/evidence/wave-<N>/red-proofs.log`.

## Invariants

- Exactly one sabotage at a time; never commit sabotaged state.
- Evidence first: no `VERDICT: PASS` without a red-proofs log entry.
- Fail closed: any ambiguous result blocks the merge.
