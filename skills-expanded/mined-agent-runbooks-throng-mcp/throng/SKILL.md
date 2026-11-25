---
name: throng
description: "Delegating work to another agent harness or model through throng (run_thronglet, send_message, wait_thronglet, list_thronglets, cancel_thronglet, list_harnesses). Use before any throng tool call, when a task should run on another model (codex, opus, gpt, glm, gemini) or get its review or opinion, and when running agents in parallel or in the background."
---

# Working with thronglets

A **thronglet** is a nested session of an agent harness that throng starts for you. It works in a directory you name, and its final message comes back as the result. It sees nothing of your conversation: no files you read, no decisions you made, no user messages. Everything it needs travels in the prompt.

## Choosing the agent

`agent` is one string: `<harness>/<model>[:<effort>]`, e.g. `claude/opus:high`, `codex/gpt-6-sol:xhigh`, `opencode/openrouter/z-ai/glm-5.3-flash`, `gemini/gemini-2.5-pro`, `cursor/gpt-5.4-nano`. The model is a value the harness itself offers: `list_harnesses` returns them with the effort levels (it probes the adapters: seconds, no tokens), and a `model_rejected` message lists them too. A value with bracketed parameters (Cursor's `gpt-5.4-nano[reasoning=medium]`) can be named by the part before the `[` when only one value has it. Effort is `low | medium | high | xhigh | max`; omitted means the harness default.

Pick another harness or model when the task gains from a different model's view (a second review, a design critique) or when the user names one. Same-vendor subagents of your own harness stay the cheaper default for plain parallel work.

## The prompt

Self-contained, written for a reader with no context: the task, the repository and the files by path, the constraints, what the result must contain, and what to leave alone. The final message is the result, so ask for the shape you need ("end with a list of findings: file, line, problem"). A harness that finds an `AGENTS.md` follows it, commits and reviews included: when you want only the work, say where the thronglet's job ends ("leave the changes uncommitted").

`cwd` is the live tree the agent edits: no sandbox, no copy. Thronglets that write in parallel each get their own tree, e.g. a worktree apiece.

## One turn or a conversation

`run_thronglet` creates the session and runs the first turn; `send_message` runs the next one in the same session, with the harness's own memory of the earlier turns. One message is one turn. Use a follow-up instead of a new run whenever the context already lives in the session: "now fix what you found", "the tests fail with this output, continue", a corrected structured result.

Messages to a session whose turn is still running queue up and run in order; the queue lives in the server process and is lost if it dies. `steer: true` interrupts the running turn instead and runs your message next, ahead of the queue: the agent keeps its memory of what it was doing, the in-flight tool call is aborted and a half-applied edit may remain. Steer only when the correction cannot wait for the turn to end, e.g. "stop, do not touch the migrations".

## Foreground or background

A synchronous call returns when the turn ends. Use it for one task whose result you need before doing anything else.

`background: true` returns once the turn is running, and a `send_message` to a busy session returns at once as `queued`; the turn continues inside the server. Use it to run several thronglets at once, or to keep working while one runs. `wait_thronglet` collects the result exactly as the synchronous call would have returned it; when its `timeout_s` elapses first it returns the session's state instead of an error: call it again. The result is stored with the session, so asking twice, or after a server restart, gets the same answer.

The fan-out pattern: start every thronglet with `background: true`, then `wait_thronglet` each in turn. A run past `limits.max_concurrency` (default 10) blocks the call until an earlier turn frees a slot, so fan out wider than that only when you can afford the wait. Follow-ups work the same way: `send_message` with `background: true`, then wait. Failures before the call returns (bad spec, unknown session, a failed handshake) come from the call itself; everything after comes from `wait_thronglet`.

## Housekeeping

`list_thronglets` finds a session whose id you lost and shows what is still running. Check it before you finish: a background thronglet you no longer need keeps running and spending tokens until `cancel_thronglet` stops it. Cancel drops the session's queue too, and a pending `wait_thronglet` returns `cancelled`.

A session run by another throng server (another Claude session, a nested agent) shows the state its record carries; cancel its turn from the session that started it.

## Structured output

Pass `schema` (JSON Schema) when you will parse the result rather than read it. throng appends the schema to the prompt and asks the agent to end with a final message that is only a JSON value matching it, so the prompt need not repeat it. When that message holds no JSON, or JSON the schema rejects, the agent gets up to two corrective prompts. After that the call fails with `structured_missing` or `structured_invalid`, carrying `text` (what it said) and `session_id`, so a `send_message` with the correction is the next step. Keep schemas small and flat: every field is something the agent must fill.

## Permissions

What a thronglet may do on disk comes from the throng config (`~/.config/throng/config.yaml`), not from a tool parameter: a calling model cannot grant itself more. `harness_mode` picks the harness's mode: `auto` (the default) its own auto-approve mode, `ask` its asking mode. `permission_answers` is how throng answers what the harness still asks: `deny` (the default) refuses, `allow` allows once, `elicit` puts the request in front of the human as a dialog in the client and their answer goes to the agent, `auto` does that when the client can and refuses otherwise. `permissions:` (`auto`, `allow_all`, `deny_all`, `elicit`) is the older shorthand for a pair. Dialogs from background turns arrive the same way, so the human may be asked while you do other work; an unanswered dialog times out and counts as refused. `elicit` needs a client with elicitation: a throng server inside a thronglet usually has none, and the call fails with `elicitation_unsupported` before anything starts. When a result reports refused edits or permission errors, that is the config (or the human) at work and a rephrased prompt meets the same refusal: report it to the user, or do that part of the work yourself.

## Reading results

- `stop_reason` `max_tokens` or `max_turn_requests` means the agent was cut off: `send_message` "continue" picks the session up.
- `warnings` are adapter notices, an effort the harness does not offer, time spent queued: worth a line to the user when they change the meaning of the result.
- Failures are tool errors with `code`, `message` and, when the session exists, `session_id` and the partial `text`:

| code | what to do |
|---|---|
| `harness_unavailable`, `model_rejected` | the message says what is missing or lists the valid values; fix the spec, or tell the user what to install, log in to (`; log in: <command>`) or fix in the config |
| `depth_exceeded` | nesting is at `limits.max_depth`; do the work yourself |
| `session_not_found` | the id is wrong, the record expired (14 days) or the harness can't continue it; `list_thronglets` has the live ones, and `accepts_messages: false` marks a session that takes no further message |
| `timeout` | the turn outlived `timeout_s` and was cancelled; the session exists: `send_message` "continue", with a larger `timeout_s` if the work needs it |
| `cancelled` | the turn was cancelled; the message names the source: `cancel_thronglet`, a `steer`, the client, or the agent itself |
| `transport_lost` | the adapter or the server running the turn died; messages queued behind it are lost; with a `session_id`, `send_message` can resume the session; otherwise start again |
| `refusal` | the agent declined the task; tell the user, rephrasing rarely helps |
| `structured_missing`, `structured_invalid` | see Structured output |
