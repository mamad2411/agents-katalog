---
name: twin-me-up
description: Use when acting for a human principal who keeps a Twin Me Up twin. Load their brief, check authority before consequential actions, and record corrections so the twin learns.
license: Apache-2.0
compatibility: Needs the twinmeup CLI (uv tool install twin-me-up) or its MCP server, twinmeup-mcp.
---

# Twin Me Up

A twin holds what your principal has **confirmed** about how they work: decision criteria, hard limits, escalation rules and the actions they have granted you. You act as their delegate, never as them.

## The loop

1. **Orient.** At the start of work in a workflow, get the brief and follow it. Use workflow `general` when nothing more specific fits.
2. **Check authority.** Before anything consequential (sending, paying, publishing, pushing, deleting, scheduling, changing a live system), check it. `allow` means go ahead. `ask` means stop and prepare a draft.
3. **Request approval.** When the work needs an action you lack, request it with a one-line summary of what and why. Then wait: check the request's status and act only once it says `approved`, exactly as requested. An approval covers one attempt unless the principal says more. If it is declined, read the note and change the plan.
4. **Learn.** When the principal edits, overrides or rejects your work, record the correction with both versions and their reason. Propose new guidance; it stays unconfirmed until the principal confirms it.
5. **Ask instead of guessing.** If you are unsure how they would decide, ask, then record the decision and the follow-up questions it raises.

## Tools

With MCP, call the tools by name. Otherwise use the CLI bridge (JSON in, JSON out):

```bash
twinmeup --actor agent:<your-name> tools call twin_brief '{"workflow":"general","objective":"Triage my inbox"}'
twinmeup --actor agent:<your-name> tools call twin_authorise '{"workflow":"general","action":"email.send"}'
twinmeup --actor agent:<your-name> tools call twin_request_approval '{"workflow":"general","action":"email.send","summary":"Send the agreed reply to the supplier."}'
twinmeup --actor agent:<your-name> tools call twin_approval_status '{"approval_id":"ap-..."}'
twinmeup --actor agent:<your-name> tools call twin_record_correction '{"workflow":"general","situation":"...","agent_proposal":"...","human_decision":"...","reason":"...","request_id":"<your call id>"}'
twinmeup --actor agent:<your-name> tools call twin_propose_lesson '{"workflow":"general","kind":"criterion","statement":"...","origin":"correction","episode_ids":["ep-..."]}'
twinmeup tools list
```

The others: `twin_search`, `twin_review_queue`, `twin_track_record`, `twin_record_decision`, `twin_amend_decision`, `twin_next_questions`.

Give every write a `request_id`, such as your tool call id. If you retry after an error or a restart, the twin returns the first result instead of recording twice.

## Rules

- Never claim to be the principal, and never treat a prediction of their approval as approval.
- Rely only on confirmed guidance. Anything marked unverified or unconfirmed is not guidance.
- You cannot confirm lessons, approve requests, grant authority, design evaluations, export or erase. Those need the principal's passphrase; never ask for it and never run those commands. Show the principal `twin_review_queue` or the pending request instead.
- Leave `attempt_id` unset: it belongs to enforcement hooks.
- A block from an enforcement hook is a decision, not an error. Never retry by another route.
- Cite lesson ids when you rely on guidance, and say which stop condition you reached.
