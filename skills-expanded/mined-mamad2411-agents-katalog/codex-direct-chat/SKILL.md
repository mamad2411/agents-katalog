---
name: codex-direct-chat
description: Use FAST for direct G → X communication with an exact existing repository-bound Codex worker via connected message_send and message_read. Use for an approved Issue/PR delta, status, question, or read-only advisory to a Factory/Manager-owned X. No routine mission IDs, result files, or replacement workers; preserve execution authority and fresh-reply checks.
---

# FAST — Direct G → X (1:1)

Treat this as a **conversation workflow**, never an independent source of execution authority. Follow the owning repository's current Issue/PR, governing rules and approval before any mutations.

1. Identify the *existing* repository and named Codex thread/workspace through the connected app. Reuse known exact bindings. If uncertain, use read-only `workspace_list`; do not assume same workspace ID across Factory, DEV and Home means the same X. Verify the exact thread when the connector requires it.
2. Send one small `message_send` to the verified workspace; ordinary messages need **no mission ID, new session, idle check or extra result file**. A busy X may reply later or defer. Include the relevant Issue/PR and one question or already-approved task delta; for advice, state **READ-ONLY QUESTION; NO WRITES**.
3. Use that app's `message_read` to inspect the worker response. A successful send means **queue admission**, not acceptance/execution. A read may return a *stale reply*; claim a fresh answer only if its content is demonstrably correlated with this request. Keep a cursor if supported.
4. If still queued or uncertain, report `QUEUED; FRESH_REPLY_UNVERIFIED`; never infer completion, force-clear a queue, create a replacement X or blindly resend. Return a succinct outcome and one next action.

## Controlled workers may be consulted

G may directly **ask a verified worker** a non-mutating question even when Factory/Manager controls its execution. The controller retains all goal dispatch, priority, write ownership and acceptance. Do not use a side conversation to order implementation, cloud work, merge or a competing task. Put material findings in the owning Issue/PR and notify the designated controller if they change execution decisions.

For actual controller-owned delegation, invoke the complementary `codex-controller` skill. For direct single-repo implementation, use the owning Issue/SPEC and current worker state; talking to X alone confers no authorization.

References when needed:
- [AO: ordinary G-X conversation](https://github.com/amitkarpe/agent-ops/blob/main/G_START_X.md)
- [AO: Home-specific binding](https://github.com/amitkarpe/agent-ops/blob/main/HOME_MCP.md)
- [Agent OS collaboration and authority](https://github.com/amitkarpe/agent-os/blob/main/kb/playbooks/integrations/chatgpt-codex-collaboration-protocol.md)
