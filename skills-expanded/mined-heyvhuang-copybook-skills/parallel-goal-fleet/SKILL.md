---
name: parallel-goal-fleet
description: "Use Herdr when the user requests execution by one or more Claude/Codex workers, or coordination across workers. Discussion of agents alone does not trigger this skill."
---

Use Herdr to run real Claude/Codex workers on local or remote machines and finish the user's task. Optimize for useful work and short coordination.

## Execute

1. State a brief split, then start independent work together. Use only workers that help; choose concurrency from the task and actual machine load.
2. Give each worker its objective, target machine/session, working path on that machine, deliverable, what counts as done and how to verify it, and necessary context. Keep dependencies in a short note when needed.
3. Follow the user's model choice, or the assignment of a coordinator running this fleet. Otherwise start OpenAI/Codex workers on **GPT-6.1-Sol** (`gpt-6.1-sol`) and Claude workers on **Opus 5.5** (`claude-opus-5-5`), the defaults as of 16 Nov 2026; if the account doesn't offer one, use the closest model it does and say so. Roles and model mixes remain flexible. Pass effort explicitly by role: `medium` for implementation (`low` only for mechanical edits), `high` for planning and direction. For review of frozen work and security, run Claude workers on Opus 5.5 at `high`; for debugging, run Opus 5.5 at `high` and move a stalled diagnosis to Opus 5.5 at `xhigh` or to a Codex worker at `xhigh`. Fable is left out by default to save quota; use it when the user names it for that task. Codex workers keep `xhigh` for review of frozen work, debugging and security. Honor any model or effort the user requests. Use the exact model ID in launch commands; consult the local model catalog if a requested name is ambiguous rather than inventing an alias.
4. Reuse ready workers for follow-up with the selected model. If switching models requires restarting a worker, resume its saved conversation and preserve its working files. Give simultaneous Git writers separate worktrees; readers can use the relevant checkout. One coordinator integrates the results.
5. Read the results, check the actual deliverables, and run relevant validation after integration. Add independent review when it materially helps or the user asks for it.
6. Release resources created for this task when they are no longer needed. Preserve user work and undelivered artifacts.

## Quick second opinion

When asked to get another model's quick opinion on a draft, plan, or conversation, use a lightweight review rather than the full implementation workflow.

- On the first turn, send one compact context packet: the user's current goal and latest corrections, relevant facts and constraints, decisions already settled, the complete artifact being reviewed, and the question for the reviewer. Preserve decisive source excerpts, uncertainty, and disagreement; an omitted fact in a summary is not evidence that the source lacks it. Do not steer the reviewer toward your own verdict. Avoid dumping raw tool logs or the whole conversation.
- For revisions on the same topic, continue the same model conversation. Send only the changed text (or the current full artifact when a diff would be ambiguous), new user feedback, and the next question. Keep settled constraints unless the user changes them; do not repeat the research or restart the reviewer by default. A new topic or a requested blind independent review should use a fresh conversation.
- Reuse a ready, task-compatible worker. Otherwise run a CLI turn in a Herdr pane in a task-owned directory; no Git worktree is needed for a supplied-text review. Persist the model conversation by default for ongoing discussion. Track topic, host, working directory, Herdr session/pane, model/effort, model conversation ID, and latest result in a small task-local note. A Herdr session or pane ID alone does not preserve model context.
- Follow the requested model and effort. Switch to an authorized fallback only after a clear limit or availability failure; a slow response alone is not a quota failure. Resume the conversation on the fallback when supported; otherwise transfer a compact handoff and explicitly report that it is a new model conversation.
- For a self-contained text review, disable tools and unrelated MCP/skill loading, provide the context directly, and collect structured output in a task-owned file. See [Herdr commands](references/herdr.md#quick-text-review) for initial and resumed CLI turns. Keep ordinary authentication; do not disable it just to reduce startup overhead. Use non-persistent mode only for an explicitly disposable review.
- Ask for the few issues that materially change the result, what should stay, and the smallest useful correction. Allow “no material issue.” Review the conversation's reasoning as well as the artifact when requested. Do not require fresh research, implementation, or another review round unless missing evidence makes the answer unreliable.
- While the worker runs, do useful local work. Read the returned answer, distinguish it from your own judgment, and deliver the accepted changes. Do not resend an already-running request or treat a prompt echo as an answer. Report measured turnaround when testing speed, without promising that later runs will match it.
- Keep the conversation record and task files while the discussion is active; do not clean them up after every answer. An idle CLI process need not stay alive to resume persisted history. On a missing or expired conversation, say so and rebuild from the saved context and decisions rather than pretending history was inherited. Clean up task-owned runtime resources when the topic ends or the user asks.

## Browser routing

Choose the browser by the actual execution environment, honoring an explicit user browser choice first. In Codex App, default to the built-in in-app browser for browser work, including authenticated flows, login checks, multi-step interaction, and console/network evidence; use your browser automation tool if the built-in browser is unavailable or lacks a required capability. Claude Code, Codex CLI and other Herdr CLI workers use the browser automation tool installed on their machine (for example Playwright), even when launched by Codex App; they do not inherit its browser tools. Public static search/fetch may use the available search/fetch tools. Verify the selected browser's login state and required capabilities; never assume shared login or report unmeasured evidence as passed. Reuse one browser owner per goal and close only task-owned browser resources.

## Keep it light

- Proceed on existing user authorization. Do not add approval rounds for routine choices or repeat permissions already granted.
- Keep only useful coordination state: task, host/session, worker ID, model and effort, working path, and result. Keep it in a task-local note file and update it as workers finish, so it survives context compaction. IDs and agent names are scoped to one server; selecting a machine in the UI does not retarget CLI commands. Record IDs of resources you create so cleanup is precise.
- Use short descriptive worker names. Report the split at the start and meaningful changes during long work. End under three headings, Waiting on you first: Waiting on you (anything that needs the user), What changed (result and validation), What I found; drop a heading with nothing under it.
- Startup arguments express the selected configuration. Inspect model/UI/process details when startup fails, an actual mismatch appears, or the user requests verification.
- No fixed worker quotas, resource-reserve formulas, mandatory model pairing, UI/version evidence gates, nonce rituals, full receipts, or automatic review/acceptance ceremonies.
- Read only the reference needed for the next operation. Use known working commands; consult `--help` when syntax is uncertain or a command fails.

## References

- [Herdr commands](references/herdr.md): session, worker, dispatch, results, and follow-up.
- [Multiple machines](references/machines.md): Herdr 0.9+ saved SSH machines, explicit host/session routing, and remote result handoff. Read when using remote workers or managing machine connections.
- [Cleanup](references/cleanup.md): worktrees, child processes, or shared browser resources that need explicit handling.
