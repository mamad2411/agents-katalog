---
name: slopomatic
description: "Runs a structured, deterministic implementation workflow via the installed slopomatic CLI: clarifies intake, gates human release, runs build and verify, records independent review evidence, and delivers a reviewed artifact. Use when the user says /slopomatic, run this plan, execute the task list, ship this in slices, implement with checkpoints, walk the plan end to end, build it with human gates, or do a governed multi-step implementation. Do not use for ad-hoc edits or planning-only work."
disable-model-invocation: true
---

# Slopomatic

Deterministic and structured approach to slop cannoning.

```text
plan → /slopomatic → clarify → human releases → machine runs
```

## Require the binary

```bash
command -v slopomatic
slopomatic version
```

If missing, stop and ask the user to install the CLI through their approved host
package or release workflow. Do not download or run installers from this skill.
Do not invent a second runtime.

## Bootstrap the run

```bash
slopomatic status --json --fields state,run_id,next_action,allowed_commands,required_evidence,intake_revision,required_reviewers,completed_reviewers,delivery_mode,blocker,decision_question
```

If status reports `UNINITIALIZED`, obey its `slopomatic init` next action.
If it reports multiple open runs, show their IDs and ask which one to resume.
Do not replace a blocked run. If status shows `RUN_DONE` and the user requested
new work, create a new run; otherwise report the completed run.

Turn the agreed plan into intake immediately after init. Keep units concrete,
bounded, and dependency-ordered; use stdin so the workflow does not leave
evidence scratch files in the repository:

```bash
slopomatic intake --input - --dry-run --json <<'JSON'
{
  "run": "run-id-from-status",
  "delivery_mode": "pr-hold",
  "review_consent": "autoreview",
  "series_bound": 1,
  "units": [
    {"id": "u1", "title": "Implement and verify the agreed change", "blockers": []}
  ]
}
JSON
```

Inspect the dry-run projection. If it matches the agreed intake, repeat the
same command without `--dry-run`. Do this for every mutation: validate first,
then apply. A dry run never advances canonical state.
`verify --cmd --dry-run` cannot predict an exit code; when it returns
`outcome_undetermined: true`, validate the command and current state instead of
expecting a post-verification transition.

Show the human a compact intake summary: units, delivery mode, review consent,
and exact `intake_revision`. Wait for explicit release approval, then run the
exact `slopomatic release --revision N` command printed by `next_action`.

## Status leash

1. Run the field-masked `slopomatic status --json` command above and obey its
   next step. See
   [status.md](references/status.md) for the full status field contract.
2. Validate every mutation with `--dry-run --json`; apply only when the
   projection matches intent. Successful `--json` output is the resulting
   status document.
3. Advance only through named CLI commands with the evidence status requires.
   Re-read status after errors or whenever output was not JSON.
4. Treat placeholders in `next_action` as fields to fill, not literal text.
   Never materialize intake, review, delivery, or other evidence payloads in
   the repository; send them through stdin.
5. Before guessing a payload field or enum, run
   `slopomatic schema --command <name>`. See
   [protocol.md](references/protocol.md) for raw input and error handling.

## Machine loop

After the human releases: build → verify → review → deliver, always driven by
status.

```bash
# after verify succeeds and status asks for review
slopomatic review --input - --dry-run --json <<'JSON'
{"run":"run-id-from-status","reviewer":"autoreview","verdict":"clean","artifact_ref":"autoreview://local"}
JSON
```

Deliver only after every required reviewer is present in `completed_reviewers`.
Use stdin evidence and match the intake delivery mode:

```bash
slopomatic deliver --input - --dry-run --json <<'JSON'
{"run":"run-id-from-status","delivery_mode":"pr-hold","pr_url":"https://github.com/example/repo/pull/1"}
JSON
```

After each projection is accepted, repeat without `--dry-run`.

## Talk to the human

Collaborator voice: short prose + optional tables. Lead with what changed or
what you need — never a wall of CLI JSON. Plain words over machine dumps.

## Three human moments

1. **Release** — confirm table (what/how/review), wait, then
   `slopomatic release --revision` using `intake_revision` from status JSON.
2. **Review consent** — once at intake: `autoreview` CLI, Cursor `/review-bugbot`,
   both, or human. Store via intake `review_consent`. Do not auto-fire reviewers.
3. **Decide** — `slopomatic ask --question …`, then
   `slopomatic decide --answer …`.

## Error recovery

Failed verification records `BLOCKED` and exits 6. Show the compact failure,
re-read status, surface `blocker` verbatim, and ask how to recover. After the
human confirms the recovery, record it with `slopomatic retry --reason "…"`;
never retry silently. For a known external blocker before verification, use
`slopomatic block --reason "…"` and follow the same recovery rule.

With `--json`, failures return `error.kind`, `error.message`, and
`error.exit_code`. Malformed input exits 2; illegal transitions or unmet guards
exit 3. Fix the input or re-read status instead of bypassing the gate. Empty
next action means the run is done or needs human inspection.

## Post-review flow

- `clean` records that reviewer. Consent `both` requires distinct clean
  `autoreview` and `bugbot` evidence before delivery.
- `findings` moves directly to `REWORK`; summarize findings, then obey the next
  build command.
- `ambiguous` moves to `NEEDS_DECISION`; ask the human and record the answer.

## Mindful spend

Strong model for BUILD; cheaper review (Bugbot / lighter autoreview). Never
default "most expensive everywhere."

## Companion tools

Installed `autoreview` binary preferred; Cursor `/review-bugbot` is a cheap
local option with consent.

## Done

Stop when `RUN_DONE`, blocked pending human recovery, or waiting at release or
decision. SQLite holds the canonical event log.
