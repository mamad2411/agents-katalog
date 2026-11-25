---
name: luxel
description: Use the Luxel macOS CLI to record screens, control Replay Buffer, open recordings and settings, convert or export media, transcribe audio and video, manage sandbox folder access, run diagnostics, and cancel jobs. Trigger when the user asks to run, automate, troubleshoot, or explain `luxel` commands or control the Luxel app from Terminal. This is the generic CLI operations skill; use `luxel-evidence` instead only for its external pull-request publication or issue-closure workflow when that skill is available.
---

# Luxel CLI

Use `luxel` as the authenticated command-line client for the Luxel macOS app. The CLI parses and signs requests; the app performs recording, media processing, transcription, and sandboxed file access.

This skill explains the CLI without imposing an evidence, review, or publishing workflow. Route to `luxel-evidence` only when the task is about to attach evidence while opening or updating an external pull request, or resolving or closing a GitHub, Jira, or Linear work item.

## Read the command reference

Before running a Luxel command, read [references/command-reference.md](references/command-reference.md). It contains setup recovery, current commands and options, path-access rules, result handling, and exit semantics.

## Route the request

| Intent | Command |
| --- | --- |
| Install, pair, or verify health | installer, `pair`, `doctor` |
| Start a recording | `record` |
| Stop or toggle recording | `stop`, `toggle` |
| Save recent Replay Buffer history | `clip` |
| Open the latest recording or settings | `latest`, `preferences` |
| Open media in the editor | `editor` |
| Convert media with convenient flags | `convert` |
| Submit a complete export request | `export` |
| Transcribe local media | `transcribe` |
| Check or manage app folder access | `access` |
| Cancel a running command-line job | `cancel` |

## Workflow

### 1. Preflight the installed client

Run read-only discovery first:

```bash
command -v luxel
luxel --version
luxel doctor --json
luxel <command> --help
```

Treat the installed subcommand help and `doctor` result as authoritative because the app and CLI version independently.

If the CLI is missing, give the user the official installer command and wait for authorization or confirmation that installation is complete. If `doctor` reports that pairing is required, guide the user through `luxel pair` and ask them to approve the visible prompt in Luxel themselves. Rerun `doctor` before continuing.

Do not silently install the CLI, pair a client, grant macOS privacy permissions, add folder access, or approve trust prompts.

### 2. Normalize the requested operation

Translate the user's intent into one documented command. Inspect that subcommand's installed help before selecting flags. Do not invent flags or infer unsupported combinations.

For agent-driven calls, prefer `--json` and preserve the complete terminal result. Use `--quiet` only when successful progress is genuinely unwanted; it never suppresses errors. Change `--timeout` only when the default inactivity window is unsuitable.

### 3. Prepare paths and app access

Use absolute, quoted input and output paths. Luxel, not the CLI process, must be authorized for those paths under the Mac App Sandbox.

Before using a path outside Luxel's built-in or configured folders, check it:

```bash
luxel access check /absolute/path --json
```

If access is missing, explain `luxel access add /suggested/folder`. That command opens Luxel's native folder picker; the folder the user selects is authoritative. Do not assume that a shell-visible path is app-accessible.

### 4. Execute and observe

Run the smallest command that satisfies the request. Long-running conversion, export, and transcription calls stream progress and wait for a terminal result. Recording start returns after Luxel accepts or rejects the start; it does not wait for the recording to stop.

Capture returned file paths, recording IDs, job IDs, result text, and structured errors. Do not report success from exit status alone when the JSON terminal event contains an error.

### 5. Verify the requested outcome

Verify what the command was meant to accomplish:

- recording control: confirm the accepted state and stop/finalization result;
- file-producing work: confirm the returned path is the intended output;
- transcription: confirm text or the requested output file was returned;
- access changes: rerun `access check` or `access list`;
- cancellation: confirm the job reached its terminal canceled state; and
- navigation commands: remember that `latest`, `preferences`, and `editor` intentionally open app UI.

Report the exact command category, result, output path or job ID, and any recovery still required.

## Computer Use boundary

Luxel CLI commands remain the primary control surface. Some commands open Luxel UI or require user selection.

- Use Computer Use only when it is enabled in the current harness and UI interaction is necessary.
- If Computer Use is unavailable, do not substitute browser control, AppleScript, accessibility scripting, UI-test runners, or legacy UI-driving tools. Ask the user to perform the visible interaction.
- Pairing approval, folder-picker selection, Screen Recording permission, microphone permission, camera permission, and other trust decisions remain user actions even when Computer Use is enabled.

## Command invariants

- `record` requires exactly one target: display, active window, or last area.
- `toggle` with no target stops an active recording; when starting, target-specific options require a target.
- `--active-window` resolves the frontmost window before the countdown begins.
- `--last-area` reuses Luxel's remembered capture; the CLI cannot define a new screen rectangle.
- `--save-to`, input files, output files, export-request files, and transcription destinations remain subject to Luxel's folder access.
- Do not pass `--overwrite` unless replacing the destination is part of the user's request.
- Do not expose pairing secrets, authentication material, private paths, transcript contents, or media contents in logs unnecessarily.
