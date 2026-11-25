---
name: intent-resolve
description: Resolve merge, rebase, cherry-pick, or revert conflicts by composing both sides against routed product direction, architectural constraints, executable contracts, and accepted exceptions. Writes only when explicitly authorized.
---

# intent-resolve

Compose behavior; never select a side merely because Git labels it `ours` or `theirs`.

## Invocation

```text
/intent-resolve [path] [--other branch] [--auto]
```

Require `git ls-files -u` to be non-empty. Identify the operation before naming sides: rebase
stage roles differ from merge, cherry-pick, and revert.

## Resolve

1. Read base, stage 2, and stage 3 for each conflict.
2. Compile `intent-check` for the conflicted unit and paths. Use matching routes and active
   decisions, not the full state. Read the exact unit exception file only for landing.
3. Read proposal files from each ref only when the conflict actually involves concurrent intent.
4. Inspect merge attributes and generated/binary policy; a policy introduced by the same change
   it exempts is not automatically trusted.
5. Classify:

   - adjacent: preserve both;
   - overlapping-compatible: compose both properties;
   - structural: replay behavior at its new location;
   - contradictory: apply the consequence gate after composition and same-domain resolution.

6. Resolve against routed schemas, types, APIs, and contract tests. Product direction and
   architectural constraints must compose; neither silently erases the other.
7. Run commands defined by the repository and report results at runtime. Confirm no active
   exception is hidden or falsely discharged.

Path overlap alone is never contradictory. Implementation uncertainty invites reversible
experimentation, not a human question. For a consequential non-composable conflict, follow
`../intent-check/references/intent-interview.md`.

Default behavior proposes content and the correct continuation command without writing. With
`--auto`, write and stage only conflicted files when no semantic contradiction remains, every
affected contract passes, and current authorization permits the operation. Never commit, push,
switch unrelated worktrees, or stage unrelated files.

If the resolution creates a durable non-testable decision, use direct capture unless the decision
itself is concurrent. Record accepted temporary underdelivery in the unit exception file; never
create a read receipt or implementation report.
