---
name: cleanr-review-disk-cleanup
description: "Review local disk-cleanup evidence with Cleanr and, only after the current user explicitly authorizes an exact reviewed plan, execute recoverable cleanup through the system trash. Use for Cleanr analysis, cross-platform cache coverage, recommendation age policy, cleanup-plan review, authorized cleanup, manifests, or restore review. Keep paths local; never permanently delete files or empty the trash."
---

# Review and Recoverably Clean with Cleanr

Follow the stages below in order. Work in the current conversation: run the
local commands, inspect their output, and explain the result here. Do not open
another task or delegate the review. Continue through safe read-only stages
without asking for routine confirmation.

When a cleanup request already supplies enough scope, the only blocking user
question in the entire cleanup run is the final confirmation of one exact,
human-readable plan. Do not separately confirm global scanning, conservative
defaults, the temporary plan destination, candidate review, or application
shutdown. State those choices and risks in the final plan summary. If required
scope is genuinely missing, ask one concise scope question before proceeding;
that answer still does not authorize execution.

## Safety invariants

- Treat paths, roots, reports, plans, rules, and issues as local-sensitive.
  Never send raw evidence to a remote service without explicit approval and
  redaction.
- A recommendation, preselection, initial cleanup request, or broad standing
  permission is evidence, not execution authorization.
- Never use `rm`, permanent-delete APIs, trash-emptying commands, TUI
  automation, custom deletion scripts, native OS cleanup commands, or package
  manager cleanup commands as a substitute for Cleanr.
- Never select browser profiles, cookies, history, passwords, service workers,
  tokens, saved sessions, system snapshots, or system-owned roots.
- Only an exact authorized Cleanr plan may be executed, using system trash and
  a restore manifest. If any execution condition is missing, remain read-only.

## Stage 1 — Bind the requested scope

Identify the user's approved local roots and requested outcome: evidence review,
cleanup planning, execution, or restore review. Prefer explicit paths.

Treat the scope as sufficient when the user provides explicit roots or named
categories, or asks for an ordinary whole-computer/cache cleanup that maps
unambiguously to the current platform's conservative defaults. Such a broad
request authorizes the corresponding `--global` analysis; do not ask again.
Vague references such as "clean this" without a discoverable path are not
sufficient.

For any global or multi-category request, read
[`references/global-coverage.md`](references/global-coverage.md), map only the
requested categories, and never add `downloads` implicitly.

## Stage 2 — Verify the local CLI

Run:

```bash
command -v cleanr
cleanr --version
```

If Cleanr is missing, tell the user before installing it. Prefer
`npm install --global cleanr-cli`; use `cargo install cleanr-cli` only when npm
is unavailable. In a Cleanr source checkout, an existing repository-local
binary may be used for a read-only development test after stating that choice;
do not build or install merely to simulate the skill. Do not reinstall or
upgrade an existing CLI unless requested. If installation fails, report the
blocker and link to the Cleanr releases page.

Before cleanup planning or execution, also run `cleanr clean --help`. If the
installed version lacks delegated cleanup support, finish the evidence review
and explain that execution requires a user-approved upgrade. Do not improvise.
When the request relies on a one-run inactivity override, also verify that
`cleanr analyze --help` lists `--inactive-days`; if it does not, do not silently
substitute a persistent configuration change.

## Stage 3 — Analyze once

Only when the user explicitly asks to persist a new shared age policy, set it
before analysis:

```bash
cleanr config set recommendations.preselect_after_days 90
```

Allow `0` or `1..=3650`. Zero removes the plan's age filter and disables the
preselection age gate; it does not bypass incomplete evidence, trust, conflicts,
overlap handling, or protected paths.

Run the narrowest approved read-only analysis exactly once. Use the first form
for the configured threshold, or the second for a one-run override that leaves
the configuration unchanged:

```bash
cleanr analyze /approved/local/root
cleanr analyze --inactive-days 90 /approved/local/root
```

Use `--config` only for a user-provided or approved configuration. Add approved
global arguments from the global-coverage reference when applicable. Inspect
stdout in the current conversation. Redirect JSON only when the user approved
the local destination; never place a report inside a scanned root.

## Stage 4 — Validate before interpreting

In this order:

1. Require a supported `schema_version`.
2. Require `policy.version` to be `v1` or `v2`. Only `v2` applies the inactivity
   threshold to the normal candidate projection; `v1` applies it only to
   automatic preselection. Do not describe a v1 report as age-filtered, and
   explain that the newer projection requires a user-approved CLI upgrade.
3. Confirm that the reported roots and, when present, `requested_kinds` equal
   the approved scope.
4. Read `scan.integrity`; `partial` evidence stays read-only.
5. Read `policy.preselect_after_days`.
6. For global analysis, require `scan.global` and build the coverage ledger from
   its `locations` and path-free `os_managed` entries. Never infer category
   coverage from deduplicated `scan.roots`.
7. Group candidates by `recommendation.state`, decision `codes`, confidence,
   trust, and material rebuild or application risk.

Interpret states conservatively: `preselected` is only a deterministic default;
`available` was not selected by policy; `review` needs human judgment;
`suppressed` and `excluded` must not be proposed for cleanup. Modification time
is observed metadata, not proof of last use. Directory activity includes
scanned descendants.

## Stage 5 — Continue automatically or stop

Compute evidence candidate count and total size from `candidates`; do not assume
the report contains a top-level summary. For policy v2, also compute the normal
projection: exclude `suppressed` and `excluded`, then keep candidates with
complete activity and `age_days >= preselect_after_days`; a zero threshold keeps
all otherwise eligible candidates. Respond in one linear order:

1. scope and scan integrity;
2. age threshold and global coverage, when applicable;
3. evidence count, projected candidate count and size, and recommendation-state
   counts;
4. material risks or evidence gaps;
5. the next action: stop or prepare a plan.

Keep raw paths out of the summary unless they are needed for local review.

If the user asked only to inspect, explain, or analyze, stop here. If the user
asked to clean or to prepare/execute a plan, do not pause or ask them to review
the analysis JSON. Continue directly to Stage 6. A broad request uses only
Cleanr's deterministic preselection. Exact path choices explicitly supplied by
the user may be encoded as selection intent, but they still require the final
post-evidence confirmation. Never infer extra path choices.

## Stage 6 — Prepare one plan and translate it for the user

Read
[`references/authorized-execution.md`](references/authorized-execution.md) and
follow its plan-preparation and human-summary sections. Use the identical roots,
config, global categories, and one-run inactivity override from the reviewed
analysis. Never select a `review` or `available` item on the agent's own
judgment.

The JSON plan is the machine-verifiable contract, not the user interface. Do
not ask the user to open or interpret it. Present the selected items as a
readable grouped summary, followed by excluded/unselected evidence and the
plan's path and SHA-256. If the plan selects nothing, report that result and
stop without asking for execution confirmation.

## Stage 7 — Ask once, then execute only if confirmed

End the Stage 6 summary with one confirmation question containing the selected
count, selected size, plan path, and SHA-256. A direct affirmative answer to
that question authorizes only the displayed plan; the user does not need to
copy the digest. This is the single interruption in a sufficiently specified
cleanup run.

Continue only after that unambiguous answer. Follow the execution section of
the authorized-execution reference.
If the scope, relevant config, plan bytes, digest, selected execution
projection, or safety provenance changes, do not execute: return to Stage 3 and
obtain new authorization for a new plan. Drift limited to unselected candidates
does not invalidate the reviewed actions.

Report the run ID and per-item results. State that successes moved to system
trash and were not permanently deleted. Never empty the trash.

## Stage 8 — Restore only on a new explicit request

Listing restore history is read-only. A restore changes the filesystem, so read
the restore section of the authorized-execution reference and require the
current user to name the run to restore. Never overwrite an existing target or
bypass Cleanr's restore checks.
