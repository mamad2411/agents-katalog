---
name: traecn-mcp
description: Operate TraeCN through TraeCN MCP’s local stdio tools. Use to delegate or stop work, choose a workspace/model/mode/conversation, inspect or change Trae settings, manage conversations, or resolve an exceptional question or command approval. The gateway owns task lifecycle and routine UI interactions.
license: MIT-0
metadata:
  author: Luckycat133
  version: "0.7.1"
  openclaw:
    requires:
      bins:
        - node
    primaryEnv: TRAECN_GATEWAY_TOKEN
    envVars:
      - name: TRAECN_GATEWAY_HOST
        required: false
        description: Optional gateway host override; keep loopback unless remote access is secured.
      - name: TRAECN_GATEWAY_PORT
        required: false
        description: Optional gateway port override.
      - name: TRAECN_GATEWAY_TOKEN
        required: false
        description: Optional gateway secret; never print, log, or persist it.
      - name: TRAECN_MCP_CLIENT_ID
        required: false
        description: Stable client identifier for legacy MCP task notifications.
---

# TraeCN MCP

Use the 20 focused tools for user intent. The gateway owns preparation, queues,
waiting, recovery, persistence, notifications, routine non-command questions,
and keep/revert gates. Do not recreate these mechanics with polling, shell,
generic commands, or GUI control.

## Setup when the host is not connected

The local runtime requires macOS, Node.js 22+, and TraeCN. The Skill supplies a
launcher and client configuration; install the matching server separately.

1. Use a source checkout, release server archive, or current scoped package. The launcher checks the repository, `@luckycat133/traecnclaw`, the legacy installed `traecnclaw` package, then `traecn-mcp` on `PATH`. It resolves symlinks to the server's directory and never accepts an environment-selected JavaScript entry point. Historical `traecnclaw@0.3.1` is not a current install target.
2. Run `traecn-mcp doctor` and `traecn-mcp setup-mcp` for an installed server; a checkout uses `npm run doctor` and `npm run --silent setup:mcp`. Alternatively, run `node scripts/setup-mcp.js` from this Skill directory. Setup locates the server and prints an absolute launcher entry. `--output FILE` atomically creates a mode-0600 file and refuses existing files. [Client templates](assets) are manual fallbacks; a printed config does not prove a running gateway or host connection.
3. Start/check the installed gateway with `traecn-mcp quickstart`, or run `npm run start:gateway` in the checkout, then reconnect the MCP client.

## Delegate and read the result

Call `traecn_send_message` with the exact instruction and, when the target is
ambiguous, the intended `conversationId`. Preserve the returned durable task
identity and release the agent turn. A supporting host owns the Tasks
subscription; other hosts use completion notifications or one intentional
later `traecn_get_task` read. Do not send another message to probe progress.
After a disconnect or gateway restart, reconnect and read that same task ID;
do not recreate its conversation or resubmit its instruction.

`traecn_send_message` accepts only `message` and optional `conversationId`.
Prepare a new context with `traecn_create_conversation`, then omit an old ID
when sending into its empty draft. Never pass `newConversation` to this tool.
If the user's instructions explicitly require both a new context and reuse of
an existing ID, resolve that target conflict before submitting.

`traecn_get_task` defaults to `detailLevel: "result"`, which returns the final
answer without the visible execution trace. Use `"trace"` for diagnosis. An
accepted, queued, running, or input-required task is still unfinished; report
the actual terminal status and returned result instead of treating acceptance
as completion. Errors do not establish that the requested effect occurred.

For an existing `awaiting_review` task, use the supporting host's Tasks review
form for that task. Respond to its current `inputRequests` key with
`action:"accept"` and `content:{decision:"approve"}` (or `"continue"`) through
`tasks/update`; optional `notes` are review feedback. The gateway schedules
already-planned follow-ups as linked tasks. Read the original task once for its
returned `metadata.nextTaskId`, then track that child ID; the parent's completion does
not establish that its follow-ups finished. Report a missing link instead of
guessing one. Do not use `traecn_send_message`,
`traecn_answer_question`, or command approval to resolve this review, and do not
infer a new follow-up from notes. A host without Tasks input support cannot
resolve it through these 20 tools: retain the ID and report the need for the
user's existing Web Control Console review action.

Use `traecn_cancel_task` for one known gateway task. Use
`traecn_stop_generation` only for an explicitly requested stop of the visible
Solo generation: first list conversations, pass its active `conversationId`,
set `acknowledgeUntrackedWork:true`, and provide an audit `reason`. The gateway
rejects a stale or different conversation; visible work may belong to the user
or another agent.

## Choose only necessary context

- `traecn_open_workspace`: open the absolute requested folder when it differs. Do not repeat workspace paths in the model message.
- `traecn_list_models` → `traecn_select_model`: discover exact names when model choice matters, then select once.
- `traecn_select_mode`: change to `solo` or `ide` only when required.
- `traecn_list_conversations`: discover the current mode, active conversation, and stable IDs when context is uncertain.
- `traecn_create_conversation` or `traecn_select_conversation`: prepare one genuinely new context or select an existing ID. An empty draft returns `creationDeferred:true` and a null ID until its first message; submit once without a guessed ID. Listed native IDs remain valid when titles or statuses change.

`traecn_delete_conversation` is permanent and requires an inactive target
explicitly named or unambiguously identified for deletion in the user's
authorized request. Read its listed ID and exact title, then pass
`expectedTitle` and `acknowledgePermanentDeletion:true`. The gateway rejects
title mismatches and active targets, records the attempt, and cannot restore a
successful deletion. The existing deletion instruction supplies authorization;
it does not require a second confirmation round trip.

## Inspect or change Trae settings

For settings work, call
`traecn_list_setting_sections`, then `traecn_list_settings` for only the needed
section. Use the returned section, label, and `controlType`; call
`traecn_list_setting_options` before selecting a dropdown value. Apply one
matching tool:

- `traecn_set_setting_toggle` for a boolean switch.
- `traecn_select_setting_option` for a dropdown choice.
- `traecn_set_setting_text` for a text or numeric input.

The gateway serializes visible UI access, confirms the applied value, and
returns to chat. Use that confirmed result; do not navigate back manually or
repeat reads after a successful write.

## Resolve exceptional interactions

The gateway returns every shell command for agent review, including read-only
classifications. Check the exact command, risk reasons, workspace, and the
user-authorized scope; a classification alone is not authorization. Preserve
decisions and authorization already given by the user. Ask only when the
pending choice or command requires information or authority the task lacks.

Resolve an unresolved interaction only on that task's current card. If
conversation context is uncertain, select its recorded, freshly listed
conversation and obtain a fresh task
interaction before deciding. A denied command also acts on the visible card;
do not deny an unrelated task's request.

- `traecn_answer_question`: answer the returned pending question using the user's decision or an offered answer determined by the authorized task.
- `traecn_decide_approval`: approve with the exact `expectedCommand`, `acknowledgeRisk:true`, and a short audit `reason`. The gateway re-reads the visible card and rejects stale or changed commands. Denial needs only `decision: "deny"`.

Modern Tasks elicitation and `tasks/update` retain the same safeguards.

## Safety

- Keep the gateway on `127.0.0.1` unless remote access is deliberately authenticated.
- Never expose `.env`, tokens, authorization headers, or TraeCN profile data.
- Keep the default security audit log enabled; high-impact approvals, stops,
  and deletions are written to date-based JSONL files with sensitive fields
  redacted and a default 30-day retention.
- Use mock mode for development and report it as mock evidence.

Read [references/mcp-surface.md](references/mcp-surface.md) only for exact
inputs, result/error handling, protocol and Tasks compatibility, or notification
reconnection behavior. Its generated contract and examples preserve all 20
capabilities without adding lifecycle tools.
