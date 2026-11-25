---
name: ho-review
description: Use when a change has been implemented and someone has to decide whether it is done, whether the reviewer is a different agent with fresh context or the same agent that wrote the code.
---

# Review

Decide whether the change meets its acceptance criteria, from the artifacts
themselves. You are not fixing anything in this phase.

## What you read

`change.yaml`, `01-design.md`, `02-implementation.md`, the actual files the
change touched, and the output of the verification commands run now, by you.

The implementation report tells you where to look and what the implementer
believes. It is a map, not evidence. Every result you record comes from a file
you opened or a command you ran in this session.

## More than one round

`02-implementation.md` carries the current round first and earlier rounds below
under `## Round N (superseded)`. Read the current round for what to check, and
the earlier ones for what was already accepted or left unverified.

If an earlier round is missing — replaced rather than kept — say so. You are
reviewing round N without the record of round N-1, and that limits what you can
conclude about deviations carried forward.

If `01-design.md` has an `Amendments` section, check that each amendment
matches what the user actually said and does not quietly widen scope.

## One result per criterion

Every acceptance criterion in the design gets exactly one of:

| Result | Means |
|---|---|
| `pass` | You checked it and it holds |
| `fail` | You checked it and it does not hold |
| `unverified` | You could not check it, and you say why |

There is no fourth value. Not `partial`, not `mostly`, not `n/a`. A criterion
the implementer did not attempt is `fail`, not `unverified` — `unverified` is
about your ability to check, not about their decision to skip.

If the design offered the user alternatives and their answer picked one, the
criteria belonging to the options they did not pick are not criteria of this
change. They should have been removed from the design when the amendment
landed; if they are still there, say so under `Artifact integrity` and score
only the ones in force.

`unverified` is a legitimate outcome when the check needs a fixture, production
data, or an external system you do not have. It is not an automatic failure.
Whether the change can still be `complete` with an `unverified` item is settled
by the design's own definition of done, not by you.

Give each row its evidence: the command and its real output, or the file and
what you read there. If a criterion would return the same result under an
implementation you know to be wrong, say so in the evidence — it passed without
discriminating anything, and reporting it as a clean pass overstates what you
learned.

## The artifacts themselves

The criteria are about the code. Check the artifacts too, and report what you
find in `Artifact integrity`.

One thing there blocks: **damage to the words the design records as the
user's.** That row is the only evidence the decision was theirs rather than an
agent's, and a reader cannot tell a corrupted quote from a rewritten one. If it
is garbled, truncated, or paraphrased, say so and return `rework` — even when
every acceptance criterion passes and the meaning still looks intact.

You usually cannot verify a quote against the original message; it is not in
the artifacts. Check what you can: that it is well-formed text, that it answers
a question the design actually asked, and that it does not license more than
the amendment claims.

Everything else you notice about the artifacts — a stale cross-reference, a
section that contradicts another, a claim in the report that turned out wrong —
goes in the same section as a finding, and does not block on its own.

## `fail` has to be actionable

A `fail` names the criterion, the observed result, and what would have to
change. "This looks wrong" is not a finding. Separate blocking fixes from
suggestions you are not gating on — a reader must be able to tell which list
they have to act on.

## Say whose review this is

Set `review_kind` in both `change.yaml` and the report:

- `self` — you also designed or implemented this change
- `independent` — you did not, and you came to it with fresh context

A self-review is worth doing and is not worth pretending about. Label it and
let the reader weigh it. If the design marked this change high-risk and the
project's config asks for an independent reviewer, say plainly that this one is
not independent rather than quietly proceeding.

## Configuration

`.ho/config.yaml` governs one thing here. When
`review.independent_reviewer_for_high_risk` is true and the design marks the
change high-risk, a self-review does not satisfy the project. Say that plainly
in the report and leave the change for an independent reviewer, rather than
recording `complete` on your own authority.

## The artifact

Write `03-review.md` with these sections, in this order:

1. **Review kind** — `self` or `independent`
2. **Acceptance item results** — one row per criterion, with its single result
3. **Evidence** — per criterion, from files you read or commands you ran
4. **Deviation decisions** — for each deviation the implementer recorded,
   whether you accept it
5. **Artifact integrity** — the state of the artifacts themselves, and whether
   the recorded user words are intact
6. **Blocking fixes** — what must change before this is done
7. **Non-blocking suggestions** — what you would change but are not gating on
8. **Final status**

Then set `status`: `rework` if anything blocking remains, `complete` if the
change meets the design's definition of done. On `rework`, the next
implementation round increments `round`.

Do not write `complete` and a blocking fix in the same report.

## Ending the phase

Lead with the outcome, not with the verification detail.

`complete` means nothing is handed on — say so plainly instead of offering a
next step that does not exist. `rework` means another implementation round, so
end with a fenced block the user can copy: change id, directory, the blocking
fixes, and what to read first.
