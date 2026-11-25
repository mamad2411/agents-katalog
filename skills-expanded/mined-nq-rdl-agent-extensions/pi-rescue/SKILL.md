---
name: pi-rescue
license: Apache-2.0
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
description: Forward an investigation, explicit fix request or follow-up to pi in print mode and return its answer verbatim, with one resumable rescue session per checkout. Use for /pi:rescue; not for reviews of local changes (/pi:review) or multi-issue dispatch (/pi:dispatch).
compatibility: Verified pi 1.0.2 (2026-10-04) on the openai-codex provider. Bash 3.2+, jq >=1.6 and Git. Prompting guidance targets OpenAI GPT-5.6/6.x models only. External pi provider credentials required.
user-invocable: true
argument-hint: "[--background|--wait] [--resume|--fresh] [--write] [--model <provider/id[:thinking]>] [--effort <off|minimal|low|medium|high|xhigh|max>] [what pi should investigate, solve, or continue]"
allowed-tools: Bash(bash:*), AskUserQuestion
---

<!--
SPDX-License-Identifier: Apache-2.0
Workflow derived from codex:rescue (openai/codex-plugin-cc v1.0.6, db52e28),
Apache-2.0. Modified for rdl-agent-extensions.
-->

# Forward a rescue task to pi

You are a thin forwarder. Make one helper call and return pi's stdout verbatim:
no paraphrase, summary or commentary, and no inspecting files, solving the task
yourself or follow-up work. If the user gave no request, ask what pi should do.

Raw user request: `$ARGUMENTS`

The helper is [pi-rescue.sh](scripts/pi-rescue.sh); `S` below is this skill's
`scripts/` directory.

## Flags

- `--background` / `--wait` are host execution flags; default is foreground.
  Never pass them to the helper.
- `--resume` / `--fresh`: the user already chose; do not ask. Strip them;
  `--resume` becomes `--resume-last`.
- Otherwise run `bash "$S/pi-rescue.sh" candidate`. If it reports
  `available: true`, ask exactly once: `Continue current pi session` or
  `Start a new pi session`. Put Continue first with `(Recommended)` for clear
  follow-ups ("continue", "keep going", "apply the top fix", "dig deeper"),
  else New first. In Claude Code use `AskUserQuestion`. Continue adds
  `--resume-last`; New adds nothing. If the user dismisses or cancels the
  question, stop: start nothing and assume no answer. If no question tool
  exists, ask in text and stop.
- If `available: false` and the request only says to continue, there is no
  session to continue: start nothing and ask what pi should do.
- A new session becomes the resumable one only when pi exits 0; a failed
  start keeps the previous session, and the helper says so on stderr.
- If a resume reports that the saved session no longer exists, report that and
  ask whether to start a new session; do not retry with a new one silently.
- `--write` only when the request asks pi to fix, implement or change files.
  Investigation, diagnosis, review and research stay read-only. Continuing a
  session does not authorise edits by itself.
- `--model`: leave unset unless the user names one; the helper falls back to
  the `/pi:setup` default. `--effort` maps to `--thinking` with pi's levels.
  Fast mode is not used.

## Prompt

The task text is the request with every flag removed. When the model provider
is `openai` or `openai-codex`, you may tighten it into one prompt using the
[GPT prompting guide](references/gpt-prompting.rst); this is the only
Claude-side work allowed. For any other provider, forward the text unchanged:
no provider-specific guidance exists yet.

## Run

```bash
bash "$S/pi-rescue.sh" task [--write] [--resume-last] [--model M] [--thinking L] -- "<task text>"
```

Run in the foreground, or as a host background task for `--background` (tell
the user it started and do not poll). Return stdout exactly as-is. If the
helper fails, report its most actionable stderr lines and stop; do not write a
substitute answer. Point to `/pi:setup` for model, authentication or missing
pi errors.

Claude Code auto mode can deny `pi -p` as **Create Unsafe Agents**. Do not
rename or wrap the command to evade it. Explain the risk and let the user run
the same helper with `!bash ...`. Neither read-only tools nor `--write`
sandbox pi: it runs with the process's OS permissions.
