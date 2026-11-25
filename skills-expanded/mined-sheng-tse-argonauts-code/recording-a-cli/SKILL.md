---
name: recording-a-cli
description: How to record or re-record an agent CLI's output for the replay tests, when a CLI's output changed or a new scenario needs a recording, and how to clean a recording before committing it.
---

# Recording a CLI

Adapter tests replay what each CLI printed, so a change in a CLI's output shows up as a failing replay rather than a broken release.

## Where recordings live

- `crates/adapters/<id>/fixtures/` and `crates/conductor/fixtures/<cli>/`: a few files per scenario (its stdout, stderr and, where it has input, stdin), named for what it shows (`plan_usage`, `report_in_execute`).
- `<scenario>.meta.json` beside each: the CLI and its version.

## Re-recording

Follow `live-runs` first: the script makes live calls on your own plan.

```sh
crates/conductor/scripts/rerecord-fixtures.sh --live --scratch <a folder outside this repo> [claude-code] [codex] [antigravity-cli]
```

- It makes three calls per CLI on the cheapest models, and its shims refuse any other call.
- Each adapter's ignored `record` tests build the commands, so a recording shows what the adapter passes today.
- As each file is written, it says whether the recording's shape (its kinds of line and their fields) changed. Keep the recordings whose shape changed and restore the rest with `git checkout`, adding the new version to `also_matches` in each restored `.meta.json` so the adapter counts it as checked. A scenario that resumes another goes with it: keep both or restore both.
- OpenCode isn't in the script yet. Record it by hand the same way, on a local model.

## Before you commit a recording

- **Take out anything about the person whose plan ran it:** account plan and email, user name, home path, machine name, organization or project ids, and any token. `grep` the new files for the user name and the home path. Home paths become `/Users/you`; the testkit test that guards this fails on any other home path, on an email outside the example domains, and on an account plan.
- Run the adapter's tests: `cargo test -p argonauts-adapter-<id>`.
- Say in the pull request which CLI version you recorded and what changed.
