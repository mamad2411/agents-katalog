---
name: pico-schedule
description: Pico reminders, scheduled tasks, and schedule scripts.
---

# Pico schedules

Use the `schedule_*` tools for schedule metadata. Author `script.js`, `prompt.md`, and any supporting files with ordinary filesystem tools.

## Choose what runs

- Use a prompt alone when every run needs the agent.
- Use a script alone for a fixed reminder or deterministic result.
- Use a script with a prompt when a cheap check can decide whether the agent has work to do.

For one-time triggers, `at` is Unix epoch milliseconds. Cron uses five fields and an explicit IANA time zone or `UTC`. Use the user's intended zone. Ask only if it is unknown. Pico must be running, and checks roughly every 30 seconds rather than at an exact instant.

## Choose the target

Schedules stay owned and managed by the workspace that created them. Supply one `target` object:

| Target | Execution destination |
| --- | --- |
| `{ kind: "chat", chatId }` | The selected existing chat. |
| `{ kind: "workspace", workspaceId }` | The selected workspace. |
| `{ kind: "external-chat", platform: "discord", externalId }` | An existing open Pico-bound Discord thread. |
| `{ kind: "external-workspace", platform: "discord", externalId }` | A Discord text channel. |

Use Pico UUIDv7 IDs for `chatId` and `workspaceId`. Use a Discord thread ID for `external-chat` or a channel ID for `external-workspace`. Creation and retargeting resolve these selectors to canonical Pico IDs. An omitted update target keeps the current destination. The agent uses the destination chat's workspace and working directory, not the owner's context.

Workspace targets reserve a per-run chat ID but only materialize a local chat/session/worktree when the run publishes text, starts the agent, or reports a failure. Script skips leave run history only. Native web, desktop, and mobile destinations stay local. Discord workspace targets create a public thread named after the schedule only when the run publishes text, starts the agent, or reports a failure.

Discord text channels must belong to an allowed guild. Unregistered channels use Discord's configured default working directory; existing channel configuration is preserved. Existing-chat selectors reuse a live, open Pico-bound thread in its expected channel. Unknown, archived, mismatched, unsupported, or unavailable destinations fail without adoption or fallback. Pico IDs and external IDs follow the same delivery rules.

Results go only to the explicit destination, never to a saved caller reply. Discord sends are acknowledged; creation, binding, and send failures appear in run history. After binding, a later failure preserves the chat and thread. If binding fails, Pico attempts to remove only the new unbound thread.

Claimed runs retain their frozen destination even after a target update. Restart interrupts unfinished runs rather than resuming delivery.

## Create a schedule

Write the source files in a directory, then pass its absolute path as `sourceDirectory` to `schedule_create`. Supply `name`, `enabled`, `target`, and `trigger`, plus `scriptTimeoutMs` if needed.

At least one root entrypoint, `script.js` or `prompt.md`, must exist. Every entrypoint present must contain valid UTF-8 text with at least one non-whitespace character. Helpers, binary assets, nested directories, and empty directories are allowed. Symlinks and special files are rejected anywhere in the tree.

Do not author root `meta.json`, including case variants such as `Meta.json`. Pico owns that metadata file. Nested `meta.json` files and source assets named `definition.json` are allowed.

Creation copies the complete supported source tree into Pico's managed directory. Later edits to the original directory do not affect that owned copy. Put every helper and asset the script needs inside the source directory. Pico does not crawl imports or copy dependencies from outside it.

Creation and run capture copy files sequentially into private staging before publishing the complete snapshot. Helpers and assets do not accumulate in a whole-tree memory buffer. Entrypoints still require memory for text validation, and the agent receives the complete prompt.

Interrupting creation or run capture during copying waits for the active file copy to settle before removing staging. Pico does not start another copy, but one large file can still delay shutdown.

## Edit or pause a schedule

Read the schedule with `schedule_get`. The result contains the current `sourceDirectory`, not source text. Edit files in that directory with ordinary filesystem tools. Future immutable run snapshots include the edited entrypoints, helpers, assets, and directories. Existing snapshots do not change.

Invalid schedules also report `sourceDirectory` when their directory is known, so you can repair missing entrypoints, blank prompts, or unsupported files in place. A conflicted schedule has `sourceDirectory: null` because it exists in both state directories.

Use `schedule_update` for metadata. Supply only the fields you want to change: `name`, `enabled`, `target`, `trigger`, or `scriptTimeoutMs`. Omitted fields keep their values, including a custom timeout. Set `scriptTimeoutMs` to `null` to remove the override and use the default timeout. Metadata updates preserve all source bytes.

You can repair an invalid cron expression and resume in one update by supplying both `trigger` and `enabled: true`. Pico validates the resulting metadata and still rejects enabling a schedule with invalid source files.

Set `enabled` to `false` to pause or `true` to resume. This moves the directory between `disabled/<id>` and `enabled/<id>`. Call `schedule_get` again after a state change before editing files, rather than reusing the old path.

Changing `name`, `target`, `trigger`, or `scriptTimeoutMs` creates a new metadata revision. Changing only `enabled` preserves the revision.

Pico reads v1 metadata as a reply-free v2 model while preserving the canonical target, owner, and revision. Routine reads leave `meta.json` untouched. The next metadata revision persists v2 without the legacy `replyTarget`. Source files and immutable run history remain unchanged and readable.

## Trigger a schedule now

Call `schedule_trigger` with `{ id }` to run an enabled schedule immediately through the same execution path as a timed trigger. Paused, invalid, and already-running schedules return errors. The tool returns `scheduleId` and `runId` after accepting the run, not after completing it. Results and raw failure diagnostics go to the schedule's configured destination.

A manual trigger consumes a once schedule, including when execution skips or fails. The schedule is disabled after completion. Cron schedules keep their original timing. Call `schedule_get` after a once run finishes before editing its managed files, because disabling moves the source directory.

## Write script.js

Write a Bun JavaScript program. Pico sets `process.cwd()` to the per-run snapshot directory containing `script.js`. Relative data paths and root script imports resolve inside that snapshot, not the chat's working directory or the editable `sourceDirectory`. Relative writes stay in that run's snapshot and do not carry over to future runs. Use an explicit absolute path to access files outside the snapshot.

Pico stores run metadata outside the script directory. On startup, older run snapshots migrate to that layout without rewriting definition or lifecycle bytes. Migration can resume after interruption. Already-corrupt history remains an error rather than being reconstructed from the current schedule.

When needed, read run context with `JSON.parse(await Bun.stdin.text())`. It contains:

- `scheduleId`, `runId`, and `claimedAt`.
- `source`, where `source.kind` is either `"scheduled"` (with `source.scheduledFor`) or `"manual"`.
- `target.kind`, which is `"existing-chat"` or `"workspace-chat"`, plus `target.workspaceId`.

Timestamps are Unix epoch milliseconds. The environment contains `PICO_SCHEDULE_ID`, `PICO_RUN_ID`, and `PICO_WORKSPACE_ID`. Pico forwards only `HOME`, `PATH`, `TMPDIR`, `TEMP`, `TMP`, `LANG`, and `LC_ALL` from its own environment when present.

Write one JSON object to stdout and exit successfully. Send logs to stderr with `console.error`. Only `agent` and optional non-empty `content` are accepted.

| Output | Result |
| --- | --- |
| `{"agent":false}` | Skip without publishing. |
| `{"agent":false,"content":"Time for a break."}` | Publish text directly. Ignore any prompt. |
| `{"agent":true}` | Send `prompt.md` to the agent. Requires a prompt. |
| `{"agent":true,"content":"Review these changes."}` | Send content to the agent, followed by two newlines and `prompt.md` if present. |

Pico captures the prompt from the completed snapshot before starting the script. A script that edits its snapshot's `prompt.md` does not change that run's agent input.

The default script timeout is 60 seconds. `scriptTimeoutMs` controls only the script, not the agent. A nonzero exit, timeout, invalid decision, or stdout larger than 256 KiB fails the run. Failure notifications are posted to the resolved destination when possible and include raw captured stderr/stdout with truncation metadata; notification delivery state is recorded in run history.

### Review only when the working tree has changes

Save this script as `script.js`. Save the absolute path of the repository to review in `repository.txt` beside it. In `prompt.md`, write `Review the working-tree status above and inspect relevant diffs. Summarize risks without modifying files.` The script checks the current state on each run, not changes since the previous run.

```js
const repository = (await Bun.file("./repository.txt").text()).trim();
const result = Bun.spawnSync(["git", "status", "--short"], {
	cwd: repository,
	stdout: "pipe",
	stderr: "pipe",
});
if (result.exitCode !== 0) {
	console.error(new TextDecoder().decode(result.stderr));
	process.exit(1);
}
const status = new TextDecoder().decode(result.stdout).trim();
console.log(JSON.stringify(status === ""
	? { agent: false }
	: { agent: true, content: `Repository: ${repository}\nWorking-tree status:\n${status}` }));
```

Run a new script in a temporary directory with representative inputs before enabling its schedule. Check stdout and exit status. A script can affect real files and external services, so use disposable inputs rather than the user's live data.
