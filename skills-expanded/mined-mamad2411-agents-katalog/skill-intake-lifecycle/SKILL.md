---
name: skill-intake-lifecycle
description: Govern third-party skills installed with npx skills from intake through evidence-based review, promotion, retention, or removal. Use for a skill install, skill review, promote skill, remove skill, skill-lock audit, skill journal update, context bloat cleanup, localPatch handling, or any lifecycle decision about third-party skills in ~/.agents.
---

# Skill Intake Lifecycle

Treat `~/.agents` as the intake tier and authored package repositories as the promoted tier.
Installation is provisional: every third-party skill needs a rationale, a review date, and an
eventual evidence-backed verdict.

## Preserve the two sources of truth

`~/.agents/.skill-lock.json` is owned by `npx skills`. Read it for mechanical installation facts,
but never edit, reformat, patch, or replace it. Only the CLI may write it.

`~/.agents/skill-journal.jsonl` is the append-only governance sidecar. Record rationale, review
dates, suite membership, and lifecycle events there. Do not copy lock-owned fields such as
`installedAt`, `updatedAt`, `skillFolderHash`, or `localPatch` into journal events.

**MANDATORY:** Before reading or writing journal state, read
[references/journal-protocol.md](references/journal-protocol.md) completely. It defines the v1
schema, append rules, and canonical queries. Do not invent fields or rewrite earlier lines.

## Intake a third-party skill

1. Establish why the local skill corpus does not already satisfy the need.
2. Install through `npx skills add`; do not copy bytes manually into the managed skill tree.
3. Re-read the lock and confirm the installed skill name and source.
4. Choose a stable suite tag. Use the source's product or collection identity when several skills
   ship together; use the skill name only for a true single-skill source.
5. Append one `intake` event immediately after installation succeeds.
6. Set `review_by` to an ISO date no more than 90 days after intake. Shorten the interval when the
   skill is experimental, high-context, redundant, or locally patched.

Write a rationale that names the intended recurring job, not a generic phrase such as “useful
skill.” One intake line per installed skill is enough; changed intent belongs in a later review
event, not a replacement intake.

If installation succeeds but the journal append fails, stop and repair the journal before using
the skill. An unjournaled install is incomplete intake.

## Find work due for review

Review a skill when its latest `review_by` or `next_review_by` date is today or earlier. Also review
immediately when:

- the lock reports `localPatch`;
- a source adds a large suite or materially changes its contents;
- the installed set creates obvious duplicate-domain or context bloat;
- a reinstall or update could overwrite local behavior.

Group installed skills by source and suite before gathering evidence. A multi-skill source is one
review unit even when only a few members were invoked.

## Gather evidence

Use the active harness's session transcript-mining or session-forensics protocol to count actual
skill invocations since intake or the last review. Record the time window, count, and durable
evidence locator. Mentions in prompts, availability in a skill list, or reading the description do
not count as an invocation.

For a promotion candidate, run the `skill-judge` protocol against the installed content and cite
the full score and report. The normal promotion quality bar is at least `99/120` (grade B), with no
unresolved specification, safety, provenance, or reference-closure defect. A dedicated promotion
proposal may set a stricter domain-specific bar; it may not silently lower this one.

Inspect the current lock at review time. A `localPatch` is an automatic `promote` trigger because
reinstalling can erase the only copy of the changed behavior. Preserve and assess the patched
content, not merely the upstream version.

## Choose the verdict

Apply the first matching rule:

| Signal | Default verdict |
| --- | --- |
| `localPatch` exists | `promote` |
| Review date reached with zero invocations | `remove` |
| Used, but below the promotion bar | `retain`; set `next_review_by` within 90 days |
| Used and quality meets the promotion bar | `promote` through a dedicated proposal |
| Fewer than 20% of a suite's members were used | Suite removal; keep only evidence-backed exceptions |

An exception to a default must be explicit in the `evidence` string. Convenience, possible future
use, install recency after the review date, and “might be useful” are not evidence.

## Review suites as suites

Calculate the used-member ratio across the whole suite. When it is below 20%, choose a suite-level
removal default and name every retained or promoted exception. Record one `review` event per member
using the same suite tag and shared evidence string:

- unused remainder: `verdict: "remove"`;
- used but not promotable exceptions: `verdict: "retain"` plus `next_review_by`;
- locally patched or high-quality used exceptions: `verdict: "promote"`.

Do not turn a suite review into unrelated per-skill narratives. Shared evidence makes the default
and its exceptions mechanically recognizable.

## Execute promotion

Promotion is an existing proposal lane, not a copy command:

1. Append the `review` event with `verdict: "promote"` and its evidence.
2. Open a dedicated proposal for the destination authored package.
3. Carry source repository, immutable revision, and license provenance in the promoted skill's
   accepted frontmatter or package provenance record.
4. Preserve any `localPatch` behavior and explain its divergence from upstream.
5. Run the destination package's quality, boundary, and reference-closure gates.
6. Append the `promote` event naming the destination package and proposal.
7. Land the authored revision and re-pin every required consumer.
8. Only after consumer loading succeeds, remove the third-party install through
   `npx skills remove` and append the `remove` event.

If re-pin or isolated loading fails, keep the intake install in place and leave the promotion
proposal active. Never reverse-copy consumer bytes into the authored repository.

## Execute retention

Append a `review` event with `verdict: "retain"`, concrete usage evidence, and
`next_review_by` no more than 90 days out. Retention is temporary evidence-based custody, not
permanent exemption from review. Repeated retention without stronger evidence should shorten the
next interval or become removal.

## Execute removal

Removal is destructive and requires the active user's authorization unless an already-approved
change names the exact skill or suite. Then:

1. Append a `review` event with `verdict: "remove"` and its evidence.
2. Run `npx skills remove <name>` for the correct scope and agent targets.
3. Confirm the skill disappeared from the lock and managed install surface.
4. Append the `remove` event with the exact CLI invocation in `via`.

If the CLI removal fails, do not append the `remove` event and do not delete the managed directory
by hand. Report the remaining installed state.

## Never do these

- Never write `.skill-lock.json` with an editor, `jq`, a script, or a merge repair; the CLI will
  overwrite unowned fields and may invalidate its hashes.
- Never rewrite, sort, compact, or deduplicate journal history; changed decisions are new events.
- Never duplicate lock timestamps, hashes, or patch objects in the journal; join them at read time.
- Never promote a skill on invocation count alone; quality and provenance are separate gates.
- Never retain an unused suite member merely because neighboring members were useful.
- Never remove a promoted intake copy before the authored revision is pinned and loaded.
- Never claim a suite verdict without recording per-member events and named exceptions.

## Completion evidence

Report the lock state observed, journal lines appended, transcript evidence window, quality report
when promotion applies, suite default and exceptions, CLI result, next review date, and any
proposal or consumer re-pin still outstanding. A verdict is not complete while its required
journal or CLI event is missing.
