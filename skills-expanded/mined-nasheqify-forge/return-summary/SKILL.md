---
name: return-summary
description: >
  Format for preparing or adopting a sub-agent or session return. In a final
  reply, use the decisions list when the agent settled a choice left open by
  the request and rules and a wrong choice would cost the user beyond redoing
  the edit.
status: active
relevant_for: ["main-code-agent", "tester", "security", "solution-expert"]
invocation:
  primary: sub-skill
  secondary: [workflow-step]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: return-summary

Format and rules for the return summary. Load this skill before
step 8 (return).

---

## Spec-assumption diff (MUST — before discoveries)

1. Read the spec assumptions (constraints, external
   dependencies, schema, service behaviour).
2. Compare with what was actually found.
3. Every deviation is a discovery — even if worked around in the
   code.

Examples: an env var is ignored, an API signature changed.

`Discoveries: none` only after an explicit diff. Not as a
default.

Before returning, apply the agreement comparison in `framework/work-principle.md`
to the actual commissioned assignment, outputs and evidence. `DONE` means that
assignment is fulfilled; `PARTIAL` means required assignment work remains;
`BLOCKED` means a blocker prevents the required continuation. State unmet assignment
requirements in Changes/Discoveries or accompanying prose, with concrete unchecked
dependencies or limits and the responsible caller. Preserve relevant unresolved
parent obligations when summarizing a nested return: local success does not fulfill
its parent. Completion status does not substitute for tester confirmation.

Each completion claim in a return or final message (tests pass, fixed, complete,
met, pushed, active) carries the evidence its row in
`skills/_protocols/evidence-author-claims.md` §8.5 requires, or states what holds instead.

## Original nested tester reports

Before returning, retain each complete nested tester return once at the existing
work-unit owner (for example, its build or fix evidence directory). Preserve the
original verbatim with its tester attribution and provenance, including the exact
commands, results, failed attempts, qualifications and unverified boundaries; a
synopsis or reproduced verdict does not replace it. Reference an already retained
original rather than making another copy.

In the parent return, include accessible references to those originals and direct
subsequent consumers relying on tester evidence (including Buddy adoption, code
review and close-retro) to open and read the relevant original before using its
claims. Carry that instruction with the references so it reaches readers through
the parent return. A path's existence or a reproduced `SIGNED OFF` is not proof of
the reported outcome: use the original's actual results and qualifications in the
acceptance or downstream conclusion, and state any relevant original that could
not be accessed or read as an evidence limit.

If no durable owner is available, forward the complete attributed original inline
in the parent return and explicitly state its recovery limitations. Keep it before
the final tester verdict line. This preserves evidence through the existing return;
it does not change the commissioned assignment's completion scope or permit a
parent to assign its own tester sign-off.

## Accuracy at handovers

This section applies under both workflow selections to every handover between
actors: a brief, a return, and a report that carries a return to the user. A
summary loses accuracy. What must stay exact travels as a verbatim copy or as a
pointer to its source (`path:line`, a record, a commit): the user's words, the
acceptance, identifiers, figures, findings, and decisions with their reasons.
The summary orients and points there; it does not replace them. Whoever relies
on such content to decide, integrate or report reads it at the source, not in
the summary.

## Decisions I took for you

This section applies under both workflow selections to every return and to
the final message of a turn that changed something or delegated work: a
sub-agent's return summary, a session's return artifact, and Buddy's final
message to the user. Within an approved scope the agent settles much without
asking (the process map, §Authorization); the user reads the final
message, not the records under it, so this list is where they see those
choices and correct the wrong ones. It holds the points settled since your
last final message.

**What goes on it.** A point goes on the list when both hold:
1. **You settled it.** The request, the brief and the rules you followed left
   it open, and you picked one way: a reading of what the request meant; what
   to keep, remove or leave undone, including what you kept on your own
   judgement; a value, default, limit, window or place you chose; a departure
   from the request, brief or plan. Check: name the way you did not take. Not
   yours: what the user's words decided, and what a rule decided through a
   check with a recorded result (command output, a measured value, a named
   file). Where you judged a rule's predicate yourself ("deliberately kept",
   "unrelated to the problem"), the point is yours. So is a ruling on a review
   finding (on an implementer's push-back, or a finding's class at the fix
   loop's cap) that no such check decided; its entry names the ruling's log id and origin
   (`skills/convergence_loop/cause-before-answer.md` §Ruling record), and a derived ruling is never
   reported as approved by the user.
2. **It costs the user if wrong.** Check: write what the user would lose, miss
   or have to do differently in the result, beyond the edit that redoes the
   point. A point whose only cost is that edit (a name, a file layout), or that
   differs only in how you worked (order, tool, search, retries), stays off.

**Form.** One line per entry: what you decided, instead of what; what it costs
if wrong; the undo as an action (a command, an edit, a setting), or "cannot be
undone". Choices of one kind with one cost and one undo are one entry. At most
five entries, highest cost first, so that the list is read; the rest in one
line that names the record holding them. A point another line of the message
already reports with its cost and undo is not repeated.

**It asks nothing.** §Authorization decides which points need the user before
you act; those are questions asked then, not entries afterwards. An item you
kept because you judged a rule's predicate ("deliberately kept") is an entry
under Test 1. An item a rule kept through a check with a recorded result
(`git status` shows changes no remote holds: the last copy of user files) is
no entry: report it as a fact, or ask about it when the order cannot be
completed without it.

**Where it goes.**
- Sub-agent return summary: the `Decisions-For-User:` field, with the entries
  or `none`.
- Session return artifact: a section "Decisions I took for you", with the
  entries or "none".
- Final message to the user: a section "Decisions I took for you", in the
  user's language, after the result; no section when there are no entries.
- Adopting a return: apply both tests to its entries from your side, drop those
  the user's words decided or your integration changed, merge entries of one
  kind, and carry the rest into your own list.

## Signs of context pressure

Adopting a return, compare it with its brief, its report and the changes it names. Signs the actor ran short of context: a brief criterion
not reported on; a step reported done whose output is missing or incomplete at its source; general wording where
sites, commands or results belong. A short return that reports every criterion with evidence shows none. On a sign, do
not adopt that part as done: check it at its source; when the check confirms a gap, cut the actor's next brief to
fewer goals or files to read.

## Format

```
RETURN-SUMMARY:
  Task:    <task ID + title>
  Status:  DONE | PARTIAL | BLOCKED
  Changes:
    - <path>: <what changed, one sentence>
  New-Files:
    - <path>: <purpose, one sentence>
  Deleted-Files:
    - <path>: <reason, one sentence>
  Spec-Assumption-Diff: executed
  Discoveries:
    - <fact that may concern context / decisions / backlog, one sentence>
  Decisions-For-User:
    - <what you decided, instead of what> — if wrong: <cost> — undo: <how>
  Spec-Updates: v<old> → v<new> | none
  SPEC_VERIFICATION: NEEDED | NOT_NEEDED
    Changed: [file list, only on spec changes]
    Reason: ">1 spec" | "DESIGN/ARCHITECTURE" | "interface contract" | "single-spec PATCH"
  INCIDENT: No | Yes (see below)

Tester: SIGNED OFF (N tests, M new) | NOT SIGNED OFF — <reason>
```

## Short return

When the dispatch names a report file (`skills/_protocols/mca-dispatch.md`), write the full return there: the
RETURN-SUMMARY above with its incident block, then, for a fix brief, the `## Findings received` table
(`skills/_protocols/mca-dispatch.md` §A fix brief's findings), then, when a required test still fails, the
`## Still-failing tests` table (§Tests still failing at the return), then the detail a reviewer needs (sites changed, each
command with its exit status and decisive result lines; raw output stays outside,
`skills/_protocols/evidence-author-claims.md` §8.4).
Then reply with these lines, in this order, and nothing else:

```
Status:   DONE | PARTIAL | BLOCKED
Commits:  <short hash + subject>, one per commit | none
Report:   <report file path>
Tests:    <each command → result, L0 included>, one line
Concerns: <each difference from the brief, discovery (§Spec-assumption diff), test written but not run, open risk
          or blocker, one line each> | none
SPEC_VERIFICATION: NEEDED | NOT_NEEDED   (only when spec files changed; the file list stays in the report)
Decisions-For-User: <entries per §Decisions I took for you> | none
INCIDENT: No | Yes — <type>, <action>
Tester: SIGNED OFF (N tests, M new) | NOT SIGNED OFF — <reason>
```

- **Status:** a brief requirement not met gives `PARTIAL`, with the requirement and the reason in Concerns. `DONE`
  means every brief requirement is met; its Concerns hold the rest.
- On `PARTIAL` or `BLOCKED`, Concerns holds the remaining work or the blocker in full, so that Buddy can act without
  opening the report.

## Adoption line

Every return, inline or in a file, and every session report ends with these lines, before the closing line
where it has one:
`Adopt after checking: <the claim to verify at its source, with path or command>`
`Not verified: <what you did not check, or none>` · `Held back: <an open obligation, or none>`
Purpose: the adopter meets what to check in the text that arrives.

## Incident block (MUST always be present — even when no incident)

Buddy can't read along during execution. Incidents
have to be visible structurally in the return.

No incident:

```
INCIDENT: No
```

On an incident:

```
INCIDENT: Yes
Type: [SPEC-STALE / TEST-FAIL / MISSING-FILE / LOGIC-ERROR / ARCH-CONFLICT / SCOPE-CREEP / OTHER]
Scope: trivial / substantial
Description: [1-2 sentences]
Action: [AUTO-FIXED / ESCALATED / STOPPED]
```

## Closing line (hard gate)

The **last line** of the return summary MUST be:
`Tester: SIGNED OFF (N tests, M new)` or
`Tester: NOT SIGNED OFF — <reason>`.

If the line is missing → the task counts as not closed.

Applies on non-code tasks too:
`Tester: NOT SIGNED OFF — no testable code, only <type>`.

## Anti-patterns

- SIGNED OFF only on the tester's confirmation, which the summary reproduces: self-assignment makes the gate
  worthless.
- The summary comes after the retest's result: a premature summary skews the status.

## Source

Superpowers (MIT License, © 2025 Jesse Vincent) and BMAD-METHOD (MIT License, © 2025 BMad Code, LLC); Forge's register
of adopted methods.
