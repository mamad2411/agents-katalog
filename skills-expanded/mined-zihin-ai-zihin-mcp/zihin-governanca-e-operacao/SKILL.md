---
name: zihin-governanca-e-operacao
description: Use this guide to manage agent budgets, contextual security policies, human approval, operator handoff, consumer restrictions and recovery from operational blocks.
---

# Govern and operate agents

Read the current schema before changing a policy. Use least-privilege API keys and verify
the effective configuration after each change.

Agent budgets are USD spending limits; plan quota is a separate control. Inspect
`get_agent_budget` or `list_agent_budgets`, then use `set_agent_budget` as authorized.
Apply limits to child agents as well when controlling multi-agent costs. In-flight work
can complete after a limit is reached; a higher limit permits subsequent turns.

For CSPs, inspect `zihin://schemas/csp_config` and `get_effective_csps`. Use documented
rule names and scopes. `update_csp` replaces the full rules object. Tool restrictions
require exact names, including external MCP prefixes. Do not rely on unsupported origin
rules as an access-control boundary.

Human approval connects an approval policy to a behavior CSP using `require_approval_for`
and `approval_policy_id`. Inspect `zihin://schemas/approval_policy` for approver formats.
Use the native chat approval flow to decide requests; listing approvals does not approve them.

For operator handoff, set the session to `manual_handoff` or `suspended` before sending
manual messages. Check uncertain delivery outcomes before retrying and preserve the
idempotency key. Cancel an active turn when needed; restore `engaged` to resume automation.

Use `set_engagement_control` to stop one agent serving a consumer, or
`set_consumer_denylist` for an account-wide restriction. Inspect the consumer profile
first. Keep consumer identities distinct: account administrators must not reuse another
person's session. Use dedicated controls rather than storing operational state as memory.
