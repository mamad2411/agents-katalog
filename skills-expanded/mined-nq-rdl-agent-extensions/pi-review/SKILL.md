---
name: pi-review
license: Apache-2.0
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
description: Run a read-only pi code review of local git changes with the OpenAI Codex review rubric and return prioritized findings verbatim. Use for /pi:review on a working tree or branch diff; not for focus-text reviews, fixes, or non-OpenAI prompt tuning.
compatibility: Verified pi 1.0.2 (2026-10-04) on the openai-codex provider. Bash 3.2+, jq >=1.6 and Git. Rubric copied from openai/codex at 81de4f2 (2026-07-21). External pi provider credentials required.
user-invocable: true
disable-model-invocation: true
argument-hint: "[--wait|--background] [--base <ref>] [--scope auto|working-tree|branch] [--model <provider/id[:thinking]>]"
allowed-tools: Bash(bash:*), Bash(git:*), AskUserQuestion
---

<!--
SPDX-License-Identifier: Apache-2.0
Workflow derived from codex:review (openai/codex-plugin-cc v1.0.6, db52e28);
assets/review-rubric.md copied from openai/codex. Modified for rdl-agent-extensions.
-->

# Review local changes with pi

Run one native-style review through pi and return its output verbatim. This is
review-only: do not fix issues, apply patches or say you are about to.

Raw arguments: `$ARGUMENTS`

The helper is [pi-review.sh](scripts/pi-review.sh); `S` below is this skill's
`scripts/` directory. It sends the [OpenAI Codex review rubric](assets/review-rubric.md)
as an appended system prompt and the diff as the request, and runs pi with
`--tools read,grep,find,ls`, `--no-session` and `--no-approve`. Diffs over
150 KB are truncated in the request, which names a temporary file holding the
complete diff for pi to read. The rubric is written for OpenAI models; other
providers' prompting is not tuned yet.

## Before running

- The model is `--model`, else `model` in `${XDG_CONFIG_HOME:-$HOME/.config}/pi-dispatch/config.json`.
  If neither exists, stop and ask the user to run `/pi:setup`. Leave `--model`
  unset unless the user names one; pass it as given (`provider/id[:thinking]`).
- Fast mode is not used. Do not load the dispatch `service-tier.mjs` extension.
- Pass `--base` and `--scope` through. Any other text is focus text: still pass
  it unchanged; the helper rejects it. Return that message as-is and do not
  rerun without it.

## Execution mode

- `--wait`: run in the foreground. `--background`: run as a host background
  task. Do not ask in either case.
- Otherwise estimate the size with plain, separate `git` calls (no pipes,
  `;`, `&&` or redirects): `git status --short --untracked-files=all`,
  `git diff --shortstat --cached` and `git diff --shortstat` for a working
  tree, or `git diff --shortstat <base>...HEAD` for a branch. Untracked files
  count as reviewable work.
- Recommend waiting only for a clearly tiny review (about 1–2 files). In every
  other case, including unclear size, recommend background.
- Ask exactly once with two options, the recommended one first and labelled
  `(Recommended)`: `Wait for results` and `Run in background`. In Claude Code
  use `AskUserQuestion`. If the user dismisses or cancels the question, stop:
  do not launch a review or assume an answer. If no question tool exists, ask
  in text and stop.

## Run

Foreground: `bash "$S/pi-review.sh" run $ARGUMENTS`, then return stdout exactly
as-is, with no summary or commentary before or after it.

Background: launch the same command as a host background task and tell the
user: "pi review started in the background. You will be notified when it
finishes." Do not poll it in this turn. When it completes, return its stdout
verbatim.

Exit 1 means pi failed or returned an unexpected shape; the helper prints the
raw output, which you return unchanged. Exit 2 is a usage, configuration or
repository error: report it and point to `/pi:setup` for model or pi problems.
"Nothing to review" is a valid result, not an error.

Claude Code auto mode can deny `pi -p` as **Create Unsafe Agents**. Do not
rename or wrap the command to evade it. Explain the risk and let the user run
the same helper with `!bash ... run ...`. Read-only tools limit edits, not
reads: pi can read any file the process can.
