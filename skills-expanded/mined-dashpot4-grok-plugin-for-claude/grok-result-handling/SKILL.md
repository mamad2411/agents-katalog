---
name: grok-result-handling
description: Internal guidance for presenting Grok helper output back to the user
user-invocable: false
---

# Grok Result Handling

When a slash command or subagent returns Grok companion output:

- Present the stdout verbatim unless the command instructions say otherwise.
- Do not paraphrase, summarize, or add commentary before or after Grok output for delegate and review commands.
- If the output includes a Grok session ID, preserve it so the user can run `grok resume <session-id>` directly.
- A normal (foreground) delegate or review returns Grok's answer in-band — present it directly. Do not send the user to `/grok:status` or `/grok:result` for it.
- Only for an explicit `--background` run (a detached companion job) tell the user to retrieve the result with `/grok:status <id>` and `/grok:result <id>`.
- If a foreground delegate was interrupted (for example a very long run hit the Bash ~10-minute limit), its job may be left showing `running` with no stored result. Tell the user to re-run the task with `--background`, which survives long runs, rather than waiting on the stuck job.
- If setup reports Grok is missing or unauthenticated, direct the user to `/grok:setup` or `!grok login`.