---
name: routine
description: "Plan and run the pre-merge review passes, route every finding, and produce exact-head PR evidence without merging."
---

# Routine

This skill owns sequencing, scope and routing. Read the host instruction file, the project config
(`.agents/trust-before-scale.json`, else `.claude/trust-before-scale.json`) and `routine.extension` if
set (project passes, rules and gate commands; report it if configured but missing). Keep the shared
evidence requirements and invent no domain policy. In a blind review with config hidden, use the routine
inputs the prompt supplies and report missing ones. Host invocations live in `routine.passes` and
`docs/harnesses.md`.

## Scope before implementation

Run `node scripts/tbs/routine.mjs plan --base <base> --json --host <host>` with the project's real base
ref and your host (`claude`, `codex`, `cursor-agent` or `gemini`), so the plan lists only your commands. An older
vendored `routine.mjs` rejects `--host`: rerun without it.
`routine.rows[].paths` are JavaScript path regexes; a diff spanning rows needs their union, and every
matched row and reason is named. Unclassified paths block planning until the config is repaired. The plan
covers committed, staged, unstaged and untracked paths and both sides of moves. It is advisory scope, not
proof a review ran. Use the emitted level and fixed pass order.

For a new surface, perform planned user-role and design reviews **before building and again after**.
If implementation already exists and the pre-build pass was missed, name that gap and do the
review now; never fabricate earlier evidence. Added UI files are a conservative signal; configure
project-specific patterns for new routes or surfaces added inside existing files. Replan whenever
the diff changes. Prose no gate reads requires no passes; consumed prose still runs configured
gates; tooling needs correctness and red proof for new checks; backend needs access and state
review; visible surfaces need role and journey review; shared code needs consumer verification.

## Run in order

Prefer the host's own skill or capability specified in `routine.passes.<step>`; use the kit pass
when absent. Commands are templates/briefs: substitute range/base/level as data using host-safe
argument handling, never evaluate raw configuration as a shell script. Record the actual command
or task brief and its result. Confirm availability and **model identity**, not only CLI name.

1. **simplify** settles the shape first with an explicit `<base>...HEAD` range and a no-behaviour-change
   brief. Wait for its writer to finish, then inspect its diff only for behaviour change; revert
   semantic changes. The correctness read must see this settled shape, even after an earlier review.
2. **correctness** reads that shape at medium for tests/tooling, high for behaviour, xhigh when
   security is in scope. Never max/ultra unless the owner asks. When a different-model cross-review
   will run later, skip same-model correctness provisionally and name that cross-review as the
   correctness read. That promise is not evidence that it happened.
3. **deep-review** checks `routine.ruleSources`, including ADRs, enforcers and do-not-change-back decisions.
4. **security** checks the entire reachable surface and who can now reach its data, not only the diff.
5. **user-roles** checks each `routine.personas` role and its tasks, including cross-role handoffs.
6. **edge-cases** checks what else can happen against `routine.coreFlows` when configured.
7. **design-audit** checks `routine.designSystem`, the UX/motion checklist and persona critics.
   With no design system configured, record “not run: no routine.designSystem configured”; do not
   claim design conformance. The rest of the visible-surface review still runs.
8. **cross-review** uses a model different from the author's. If unavailable, record why and run
   correctness one level higher. If it exits without a review, is out of quota, or its log contains
   no actual review, do the same before merge. Cap at xhigh unless the owner requests more; at that
   ceiling use a fresh independent reviewer and report identity. A successful exit alone proves nothing.
9. **verify-walk** observes the changed journeys on a browser/simulator after the shape settles.

If **any** required review yields no review, run a stronger replacement for the **same scope and
subject** before readiness; a higher-level correctness read cannot replace a missing security,
role or rules review. Record the missing pass and replacement. If no capable replacement exists,
report blocked. Do not turn “not run” into PASS. Passes excluded by rows get their exclusion reason.

Run configured gates after the last edit, without checkout edits or competing builds/walks during
the run. Gate logs start `HEAD=<full sha>` and end with the configured exit marker, written from
the real command exit status. Record counts and failures honestly. New checks need known-bad red
proof before green counts. A new head or changed base requires fresh affected reviews and gates.
Uncommitted work cannot be attested by a head SHA: finalize through the project's authorized git
workflow first, or leave evidence explicitly pending. This skill never commits merely to scan.

## Route every finding

Check cited lines and reachability yourself; report the citation sample size and mismatches.
Read existing decisions and issues before acting. A settled policy is not a new defect; explain
its disposition with the cited decision. Every remaining finding receives one route:

- **Fix now** when in scope; introduced/worsened unauthorized access, data loss, broken journeys,
  core-flow errors or binding design/rule violations block readiness. Reproduce guard failures red,
  fix them, and have the originating pass re-check the blocking fix on its new full SHA.
- **File an issue** for pre-existing defects or missing capabilities outside this slice, with
  severity and evidence before readiness. Link an existing issue when it already covers the finding.
  Never silently expand the slice. Record a proposed issue as pending when posting is unauthorized.
- **Ask the owner** when policy is missing, regulated, or conflicts with a settled decision. First
  search configured decisions and try answering from code. Batch remaining questions with evidence,
  risk and a recommended pick. Pending owner answers remain pending; elapsed time is not approval.

Guidance can be dismissed with a checked reason; record that disposition rather than inventing a
bug or silently dropping it. If a finding is fixed, retain the finding, fix and re-check evidence.
When routing each finding, run `node scripts/tbs/learn.mjs add --class <mistake-kind> --where <file-or-area> --source review-finding --evidence "<sha, PR and finding; disposition>"`. Record the fix, issue or owner decision in evidence.

## One PR evidence block

Before writing the evidence block, run `node scripts/tbs/learn.mjs sync` and review the added lessons
for inclusion in the normal commit. If this changes the diff, refresh affected reviews and gates.

Prepare this block and post it only when the session authorizes PR updates; otherwise return it
for the owner to post. Use the heading below and verify it matches `selfMerge.requiredComments`.
Every required comment still applies. Never merge, deploy or interpret a ship request as permission
to bypass the project's merge workflow.

```text
## Routine evidence
HEAD=<full 40-character sha>
Base/range: <resolved base, range; clean checkout or pending>
Matched rows: <every row, matching paths and reasons>
Before build: <user-roles/design results or explicit missed pre-build gap>
Author / reviewers: <actual model identities and independence>
Pass | Command or task brief | Result / findings / exclusion or replacement | Reviewed SHA
simplify | ... | ... | ...
correctness | ... | ... | ...
deep-review | ... | ... | ...
security | ... | ... | ...
user-roles | ... | ... | ...
edge-cases | ... | ... | ...
design-audit | ... | ... | ...
cross-review | ... | ... | ...
verify-walk | ... | WALKED journeys; INFERRED reason + walk-owed issue | ...
Findings: <each fix, issue link, reasoned dismissal or pending owner question>
Citation sample: <checked / total, mismatches and reachability checks>
Blocking fixes: <originating pass re-check on full SHA, or blocked with reason>
Gates: <actual commands, log paths, exit codes, counts, full SHA after last edit>
Readiness: <ready / blocked / pending; gaps and next action>
```

No gate exists: say “not measured — no gate configured” and link its tracking issue or mark the
issue pending. A gate exists: record its output or why it has not run, never “not measured”.
