---
name: luxel-evidence
description: >-
  Create and attach focused WebM evidence with Luxel only at an external publication or closure step:
  opening or updating a pull request for review, or posting final evidence while resolving or closing
  a GitHub, Jira, or Linear work item. Do not invoke implicitly for local implementation, debugging,
  bug fixing, testing, verification, internal handoffs, or work that is merely ready for review. Use
  outside this boundary only when the user explicitly requests Luxel evidence.
---

# Luxel Evidence

Create the smallest convincing recording of changed behavior for an imminent external review or work-item closure. Prove the relevant acceptance criteria, not merely that the application launches. Treat the recording as review evidence and durable documentation, never as a replacement for automated tests.

This workflow requires macOS, a compatible Luxel app, Screen Recording permission, and a runnable build of the changed product. If the `luxel` CLI is absent or unpaired, guide the user through setup before recording.

## Enforce the activation gate

For implicit invocation, proceed only when every condition is true:

1. Implementation and normal verification are complete.
2. The current task authorizes an external update now.
3. That update is one of:
   - opening or updating a pull request for review; or
   - posting final evidence while resolving or closing a GitHub, Jira, or Linear work item.
4. The WebM evidence will be attached as part of that external update now.
5. The changed behavior is materially clearer on video than through tests or text alone.

If any condition is false, stop without reading the playbook, checking Luxel, recording media, or mentioning missing video evidence. Continue the underlying task normally.

Do not implicitly invoke this skill merely because:

- a bug or feature was implemented locally;
- tests passed or work is ready for an internal handoff;
- a task mentions a pull request or external issue without authorizing an update now;
- a GitHub, Jira, or Linear issue supplied context for the implementation;
- the agent is debugging, reproducing, verifying, or demonstrating behavior locally; or
- visual evidence might be useful later.

A direct user request to use `luxel-evidence` may bypass the implicit activation gate. All authorization and safety boundaries still apply.

## Read the playbook

Before invoking Luxel, read [references/capture-playbook.md](references/capture-playbook.md). It contains the Computer Use boundary, setup recovery, target-selection rules, exact CLI recipes, WebM conversion, failure handling, and the attachment contract.

When adopting this skill in another repository, read [references/adoption.md](references/adoption.md) for the discoverable location, recommended `AGENTS.md` trigger, and artifact-policy decisions.

## Workflow

### 1. Define the proof

Inspect the external pull request or work item, task specification, acceptance criteria, diff, and test results. Select one to three observable claims that matter to that external review or closure. Express each as a short scenario:

```text
Given <visible starting state>
When <one deliberate action>
Then <observable result introduced or fixed by this change>
```

Prefer one coherent clip. Split clips only when the claims require materially different applications, capture targets, or setup. For a bug fix, exercise the original failure path and show the corrected result; do not require a separate broken-build recording unless one already exists and adds value.

### 2. Check prerequisites and guide setup

Run:

```bash
command -v luxel
luxel --version
luxel doctor --json
luxel record --help
```

Treat the installed CLI help and `doctor` capabilities as authoritative. Confirm that command-line control is enabled, the app and protocol are compatible, `record`, `stop`, and `convert` are available, and Screen Recording is authorized.

If the CLI is missing, give the user the official installation command and wait for them to complete installation. If it is unpaired, explain that `luxel pair` opens a visible approval prompt in Luxel, ask the user to run and approve it, and then rerun `luxel doctor --json`. Pairing approval is always a user action; do not approve a new trusted client through Computer Use.

Do not silently install the CLI, pair a new client, change macOS permissions, modify Luxel settings, or add folder grants. If another prerequisite is missing, report the exact failed check and guide the user through the corresponding recovery.

### 3. Choose the narrowest useful target

Use this priority order, then deviate when the scenario requires it:

1. `--last-area` for one control, panel, canvas region, or terminal subsection.
2. `--active-window` when the window frame, resizing, or whole-window context matters.
3. `--display main` for cross-window interaction, menu-bar or system UI, drag-and-drop between apps, or other behavior a single window cannot contain.
4. Record a larger target and crop the deliverable only when a precise capture area cannot be staged reliably.

The recording CLI does not accept a new `x,y,width,height` target. To capture a fresh exact screen rectangle, open Luxel's Area picker, draw or resize the region with Computer Use when that capability is enabled, verify the bounds, and then use `--last-area`. If Computer Use is unavailable, ask the user to define the area; do not substitute another UI-driving capability. Never invent a `luxel record --region` or coordinate flag. `luxel convert --crop x,y,width,height` is a post-capture pixel crop, not a screen target.

### 4. Stage and record

Follow the current project's local launch instructions and use a development or test environment. Prepare deterministic fixture data, a stable window size, and a clean desktop. Exclude secrets, personal data, unrelated notifications, and irrelevant application chrome.

When the scenario requires UI interaction, use Computer Use only if it is enabled in the current harness. If it is unavailable, do not use browser control, AppleScript, accessibility scripting, UI-test runners, or legacy UI-driving tools. Ask the user to perform the documented actions while the recording runs, or report that unattended visual evidence cannot be produced.

Start the selected target with structured output and a short countdown when useful:

```bash
luxel record --last-area --countdown 3 --json
luxel record --active-window --countdown 3 --json
luxel record --display main --countdown 3 --json
```

Run only one of these commands. Add a known `--preset`, an FPS override, or `--save-to` only when the scenario requires it and the installed help confirms the option.

Show the initial state briefly, perform the scenario deliberately, and pause on the result long enough to inspect it. Stop immediately after the proof:

```bash
luxel stop --json
```

Use the returned `result.filePath` as the source of truth for the new artifact. Do not guess based on directory order when multiple recordings may exist.

### 5. Convert to WebM and inspect

Keep the source recording, then create a WebM deliverable with `luxel convert`. Use a descriptive `.webm` output path and preserve any trim, resize, crop, mute, or retiming choices needed for review.

Watch the complete WebM artifact. Confirm that it shows the intended build, readable content, the triggering action, and the final state without leaking unrelated information. Re-record weak or ambiguous evidence instead of explaining around it. Preserve enough surrounding context that the video remains credible.

### 6. Attach to the external update

Follow the authorized external destination's existing artifact convention and attach the WebM file to the pull request or closing/resolution update. Prefer a purpose-built connector, API, or CLI that supports binary attachments. If attachment is available only through UI, use Computer Use when enabled; otherwise return the absolute WebM path and an attachment-ready summary without claiming the external publication or closure is complete.

Do not commit large binary media to the repository unless its documented policy calls for that. Do not claim a local file is attached. Verify the final link from the reviewer's perspective.

Use this compact handoff:

```markdown
## Visual evidence

- **Claim:** <acceptance criterion demonstrated>
- **Scenario:** <starting state → action → visible result>
- **Capture:** <selected area, active window, or display; relevant preset/FPS>
- **Artifact:** [<descriptive filename>.webm](<durable reviewer-accessible URL>)
```

Report the source path, any derived artifact path, the capture target, the scenario demonstrated, and where the video was attached. If attachment or recording was blocked, name the failed prerequisite or missing capability precisely.

## Guardrails

- Prefer focused evidence over long tours or full-display recordings.
- Never activate implicitly without an imminent, authorized external publication or closure action.
- Keep setup out of the clip unless setup behavior is itself under review.
- Never record credentials, private communications, customer data, or unrelated windows.
- Do not use a production account or mutate production state merely to stage a demonstration.
- Stop recording promptly if unexpected sensitive content appears; do not attach that artifact.
- Create evidence intentionally from a planned scenario; do not repurpose retrospective or ambient recordings.
- Use Computer Use as the only UI-driving capability, and only when it is enabled in the current harness.
- Default every review deliverable to WebM and verify the destination accepts it before claiming attachment success.
- Use narration, transcription, camera, or audio only when they help prove the changed behavior.
- A polished video does not override failing tests or unresolved acceptance criteria.
