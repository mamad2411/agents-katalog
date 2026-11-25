---
name: webgpt
description: Delegate work to signed-in Web ChatGPT when the user requests WebGPT (m/medium, h/high, xh/xhigh or p/pro), or open a user-controlled project terminal chat with webgpt open.
---

# WebGPT

Delegate bounded work to save Codex usage. User instructions about division of work, model,
monitoring, permissions, follow-ups and retention override defaults. Never silently take over
WebGPT's assignment; Codex may perform separately assigned work concurrently.

Keep Codex ↔ WebGPT coordination in English, preserving source quotations and the requested
deliverable language. Reply in the user’s language unless they request another; leave browser UI language unchanged.
**Every conversation must use Chat, never Work**, including setup tests, browser-only work and
`open`. Verify Chat before composing or selecting a connector; return to Chat if a shortcut opens Work.

## Route

- `webgpt open [path]`: follow [open.md](references/open.md); skip delegation below.
- Worker delegation: read [workspace.md](references/workspace.md).
- Explicit browser-only work: use [browser-reply.md](references/browser-reply.md); skip Worker commands.
- Read [setup.md](references/setup.md) only for installation or missing capability, and
  [recovery.md](references/recovery.md) only for actionable exceptions or same-chat follow-ups.
  Client tunnel/connection errors require setup's origin recovery before dispatch.

For Worker tasks, register first and use the returned `connection.name` and `connection.registrationId`.
With `connection.status: ready`, skip configuration/setup reads, directory searches and Plugins
rediscovery. Missing/invalid metadata routes to recovery.md; keep the registered task, do not register again.

## Delegate

Assign one bounded deliverable with its relevant tests per new chat. Investigate only enough to
specify the objective, context, constraints and success criteria; leave routine commands to WebGPT.
Avoid open-ended projects, arbitrary duration limits and separate chats for tiny actions. Assign
file ownership/worktrees for concurrent changes. No duplicate task documents or tracking files.

Prepare one concise English prompt before opening the tab: task, necessary context/constraints and
success criteria. Reference accessible project briefs by path instead of restating them.
For Worker tasks, add the named connector/task token and “Save the final outcome
through the Worker.” Tool schemas supply the completion protocol; do not repeat it. Never send the
controller key or connection URL. Retain task and owned chat/tab identifiers in context.

Use documented browser initialization; reuse known browser identity without scanning all surfaces.
For Worker tasks, select the existing connector in Chat by verified registration ID, or
use a verified Chat launch URL. Mentioning a connector in prose does not select it.
Import helpers once per runtime (again after reset/resume); allow 60 seconds per helper call:

```js
var {dispatch, deleteAndClose} = await import('<skill>/scripts/browser.mjs');
var sent = await dispatch(tab, prompt, 'xh', {
  startup: {connectorName, authorizeConversation: true}
});
```

Modes: `m|medium` = Medium (중간; also Standard/표준), `h|high` = High,
`xh|xhigh` = Extra High (default), `p|pro` = Pro. Pass any of these aliases to `dispatch`.
Omit `startup` for browser-only work. The helper verifies mode, sends once and checks startup.
Choose **Always allow / 항상 허용** for authorized WebGPT permission prompts whenever offered;
this is the helper default. Only an explicit narrower user request uses
`permissionScope:'conversation'`. Preserve unrelated permissions and runtime gates.

On `submitted`, reuse the returned URL and wait. Permission selections or `not_observed` do not
prove terminal readiness; do not poll startup. On `submission_unconfirmed`, inspect the existing
user turn without resending. Resolve other actionable states via recovery.md.
Emit only relevant evidence, not full AX trees/exports or unnecessary screenshots. If helper
imports are unavailable, use documented CUA; do not read helper source during normal operation.

## Wait, review, close

Use `client.mjs finish <ids>` for quiet waiting, verified result text and collection in one call;
do not repeat status/read/collect. Do separately assigned Codex work after verified submission.
Without requested monitoring, inspect progress only for a due backup or explicit help/failure.
On `backupDue`, read recovery.md: one scoped chat check, then `resume <id>`, not another `finish`.
Waiting requires a live parent runtime; it cannot wake exited Codex.

Review once against the outcome and relevant diff/evidence. Hash integrity is not correctness.
Do not reread the returned artifact or rerun reported passing tests on the delivered version
unless evidence is missing/conflicting, failures or integration changes need checks, or the user
requests verification. Distinguish PASS/FAIL/NOT_RUN. A `partial` result
needs continuation; a `cleanupError` needs recovery. Do not duplicate WebGPT's investigation.

After preserving/reviewing results, call `deleteAndClose(tab, cua, browserId, ownedChatUrl)`.
**Permanently delete the exact owned task chat, verify deletion, close its tab and verify absence.**
This cleanup is already authorized: do not ask again due to permanence, generic confirmation
notices or a new CLI session. Honor explicit retention; never delete `open` chats, uncollected work
or unrelated chats. Keep the connector, Worker and tunnel for reuse. Actual tool rejection or a
user-requested cleanup pause routes to recovery.md; tab closure alone never proves deletion.
