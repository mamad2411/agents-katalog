---
name: lark-approval-status-probe
version: "1.1"
description: Check one Lark approval instance or list approval tasks with the typed lark_approvals_get / lark_approvals_list tools and report the normalized status (approved / rejected / running, is_terminal, pending task and approver). Doubles as the end-to-end test for approval status tracking and as a daily "查审批" helper.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - probe
    - lark-approval
    - status-tracking
    - diagnostics
---

# Lark Approval Status Probe

Use this when someone asks "我的审批怎么样了", gives you an approval `instance_code` to check, wants
their approval todo list, or wants to verify that the typed approval tools work in this environment.

**You (the agent) run the check yourself with the typed tools.** Never invent instance codes,
statuses, task ids, or approvers. A tool error is a finding — quote it verbatim, never fail the run.

## How to run it

1. **Resolve the ask.** From the user's text take either an `instance_code` (the long code returned
   when an approval instance is submitted), or a list intent: 待办/todo, 已办/done, 我发起的/initiated,
   抄送未读/cc_unread, 抄送已读/cc_read. Default to the todo list when nothing is given.

2. **Single instance** — call `lark_approvals_get` `{instance_code, locale:"zh-CN"}` once. Report:
   - normalized `status`: `approved` / `rejected` / `withdrawn` / `terminated` / `running` / `none`
   - `is_terminal` and `should_continue_waiting`
   - the currently pending task and its approver, plus a one-line summary of key form fields
   Optional `user_id_type`: `open_id` / `user_id` / `union_id` if the user cares about id format.

3. **List** — call `lark_approvals_list` with the mapped `topic` (`todo` / `done` / `initiated` /
   `cc_unread` / `cc_read`). Render a compact table: instance_code | approval | status | started.
   Offer: "给我某个 instance_code 可以看明细".

4. **Act (explicit request only).** Only when the user explicitly tells the bot to approve, reject,
   or transfer a specific task AND you have both `instance_code` and `task_id` (from step 2's task
   list), call `lark_approvals_act` `{action, instance_code, task_id}`. Warn first that this is a
   real approval action and a human-approval card may appear before it executes. Never act on your
   own initiative; never guess `task_id`.

5. **Report.** One line per check: what you queried, the normalized status, and the next sensible
   step (e.g. "still running — ask me again later, or let me set a `scheduled_agent_creator`
   reminder"). Check once per request; do not busy-poll inside a chat turn.

## Failure semantics (this is also a test skill)

- `success:false` with a scope/permission error (e.g. `230027 need scope: ...`) → quote verbatim;
  the `need scope` text names the exact grant to add.
- **`99991663 Invalid access token` does NOT mean the token failed.** Lark's gateway answers
  nonexistent routes with this misleading error. Before claiming any credential problem, run the
  control probe `nyxid_proxy` `{slug:"api-lark-bot", method:"GET", path:"/open-apis/im/v1/chats?page_size=1"}`
  — `code:0` there proves credentials are healthy and the failing call hit a broken endpoint.
  Known case: `lark_approvals_list` on platform builds before 2026-06-11 called the phantom
  `approval/v4/tasks` path (fixed to the documented `tasks/query`); `lark_approvals_get`
  (instances/{code}) was always a real endpoint.
- Never recommend rotate/disconnect/re-OAuth from 99991663 alone.
- Tool not found → the runtime predates the typed approval tools; fall back to
  `nyxid_proxy` `{slug:"api-lark-bot", path:"/open-apis/approval/v4/instances/{instance_code}", method:"GET"}`
  and NOTE the fallback in your report — that note is the test signal.

## Guardrails

- Read paths (`lark_approvals_get` / `lark_approvals_list`) are read-only and auto-approved; the
  act path is not — treat it as a real-world side effect.
- Only use real returned data; never fabricate codes, tasks, approvers, or statuses.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
