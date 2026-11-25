---
name: ryu-configurator
description: Configure Ryu nodes, models, agents, integrations, privacy, and Gateway policy, including organization/team roles, resource access, app grants, scoped secrets, and budgets. Use to inspect effective settings, apply scoped changes, or diagnose access denials.
---

# Ryu Configurator

Configure the requested Ryu environment through its owning Settings surface or documented API. Resolve effective settings and access, preserve unrelated configuration, and verify the user's intended operation. Skill availability never grants administrator privileges.

## Discover before changing

Identify the target node/profile, local or managed deployment, acting identity, organization/team/resource scope, and desired outcome. Read existing effective settings and supported schemas with the tools actually available. Use MCP discovery, CLI help, current OpenAPI, or Settings rather than guessing endpoint names. Read metadata and redacted values; do not print tokens or dump credential stores.

In a checkout consult the platform consistency standard and the relevant implementation. Otherwise use the installed version's public docs at `https://docs.ryuhq.com/docs`:
- `/start-here/configuration` for storage ownership and precedence.
- `/security/permissions` and `/security/authentication-and-pairing` for roles, resource ACLs, node scope, and credential boundaries.
- `/security/secret-vault` for scoped secret references.
- `/gateway/configuration`, `/gateway/configuration-access`, and `/gateway/reliability` for policy, keys, and budgets.
- `/surfaces/desktop/transparency` for privacy and local support-access preferences.
Read only the domains involved. If an API or setting is unavailable in this version, report that limitation rather than editing an undocumented store.

## Choose the configuration owner

| Concern | Owner and authoring surface |
| --- | --- |
| Node behavior, models, agent bindings, local execution | Core Settings and its supported structured stores; non-secret `node-config.json` where supported |
| Client node targets | `nodes.json` |
| Gateway routing, budgets, firewall, operator policy | Gateway Settings/API for runtime-editable fields; operator `gateway.toml` for service policy |
| Membership, invitations, team and custom-role assignments | Control-plane identity and membership APIs/UI |
| Resource sharing | The owning resource's server-side ACL and tenancy controls |
| Extension requirements and grants | Manifest declarations plus the host's approval/activation state |
| Credentials | Existing sealed secret store or deployment/bootstrap boundary |

Use JSON for Ryu machine-managed contracts, TOML for operator Gateway policy, and YAML only for an external format that requires it. Do not put secrets or bootstrap wiring in `node-config.json` or manifests. Preferences and environment overrides have field-specific precedence: inspect the effective value and reader; do not assume one global precedence rule. Distinguish runtime-editable fields from restart-only fields before applying changes.

## Access-control reasoning

Build a small subject → action → resource → scope matrix. Inspect effective permissions, not just the visible role label. Ryu's built-in roles and applicable custom-role grants combine according to the current shared permission contract; team assignments require matching membership and resource scope. Resource ACLs and node organization/team/personal-owner boundaries still apply. Do not invent a deny override, role inheritance rule, or permission name.

Keep these boundaries separate: control-plane PAT/API/OAuth credentials, node-control bearer or verified managed-node user JWT, inference key, provider key, bootstrap token, and plugin grant. One credential type does not automatically authorize another surface. A manifest grant is not consent, an enabled UI control is not server authorization, and a resource ID supplied by a client does not establish ownership.

For a 401/403, check credential purpose and expiry, node binding, verified identity, membership, effective permission, resource ACL, then capability/grant state. Correct the narrow missing assignment or scope. Do not resolve failures by disabling authentication, removing the firewall, granting wildcard access, switching everything to owner/master credentials, or trusting arbitrary identity headers. Enable trusted-forwarder behavior only for an explicitly intended controlled intermediary that authenticates the forwarded identity.

Skill activation and agent allowlists are separate: an empty skill allowlist means all enabled skills; an explicit list narrows that set and cannot reactivate a disabled skill. Inspect the UI/API representation of “none” before writing it. Instructions and allowed-tool metadata do not bypass runtime tool policy.

## Hooks, extension controls, and capability bindings

Use `/extend/develop/extensions/hooks-lifecycle`, `/extend/develop/extensions/plugin-json-manifest`, `/extend/develop/extensions/capability-broker`, and `/core/swappable-layers` for these changes. Inspect installed/enabled state, approved grants, selected provider and compatibility, runtime availability, per-request flags, and effective settings separately. Installation does not imply enablement, a composer flag is not a grant, and a declared UI control does not prove the handler consumes its value.

For a hook that does not fire, check the enabled manifest, explicit `on`, `match.tools`, target engine/plane, and sandbox logs. `pre_tool_use` can deny; awaited `tool_result` can transform; detached `post_tool_use` only observes. `context` uses `rewrite/messages` on the message-array plane and `replace/text` on ACP. `message_end` acts before persistence; `post_assistant_turn` notes do not rewrite history. Observation phases cannot enforce access. A failed or ungranted hook may become `none`; keep required security restrictions in the authoritative policy owner.

For side-model hooks inspect the `hook:side-model` grant, model preference, and Gateway budget; for storage or notifications check their distinct grants. Inspect continuation limits, dedupe scope, and user opt-in before enabling repeated work. Test the matching event and an unrelated event, then disable and verify that execution stops. Never treat “wired” documentation as live proof across every agent engine.

Resolve swappable capability requirements against available provider versions and the current override/selector contract. Read back `/api/capabilities` and `/api/capabilities/bindings` when supported; preserve unrelated overrides. Provider selection does not approve its permissions. Check dependent apps after rebinding, including unavailable-provider recovery, instead of adding app-specific routes or hardcoded ports.

## Agents, routines, memory, and integrations

Consult `/surfaces/desktop/user-guide/agents` for lifecycle, safety, tools, memory, and triggers. Use `ryu-agent-creator` for new agent design when available. Keep agent groups (coordination records) separate from organization teams (access membership). A group is not a new identity permission scope.

Draft cannot run; Trial is read-only on governed Core paths; Active uses its chosen safety profile. Promotion goes through Trial and a normal-chat test. “Verified plans only” uses Safe Actions and typed plan tools rather than direct execution. Do not assume those protections cover native ACP tools outside the Core bridge. Inspect reachable tool access: current new-agent defaults can include all enabled MCP tools, and empty skills means all enabled skills. Select a narrow subset or the explicit off mode when that is the requested scope.

For routines inspect cron/interval, timezone where supported, instructions, model pin, approval policy, and destination: a new chat per run versus one persistent conversation. Confirm run-now behavior and history before relying on a schedule. Draft/Trial changes pause schedules; deleting a routine preserves existing transcripts. Do not create recurring work without the user's request.

Treat attached Space retrieval, per-agent long-term memory, memory writes, identities, channel credentials, and telemetry as separate grants/consents. Verify retrieval as the intended principal, with an out-of-scope negative case; attaching a Space does not override its ACL. Channel and provider credentials remain in the owning sealed store. Use agent Health and passport/audit views to diagnose configuration and traces; neither proves successful model execution. Check routine and workflow failures in durable run history rather than inferring success from an enabled toggle.

## Apply a scoped change

Explain the effective change and affected subject/resource. Use existing authorization for the requested operation; request missing authority only when necessary. Prepare the concrete diff first for a change requiring approval. Preserve a redacted before-state and a viable recovery path for access changes; avoid removing the last usable administrator or recovery route.

Prefer supported field-level APIs over raw store edits. Preserve unknown/unrelated fields, use supported conflict/version controls, and validate complete config before atomic file replacement when file editing is the documented path. Respect any step-up challenge. Do not retry a non-idempotent mutation after an ambiguous response without reading back the resulting state.

Reference secrets through the documented vault mechanism, such as `secret:NAME`, after verifying its scope and binding. Current vault resolution prefers user, then node, team, and organization; exact MCP bindings take priority within a scope. Confirm this against the installed contract before relying on it. Never copy secret values into chat, screenshots, exported config, child-process environments, or unrelated scopes. Privacy, telemetry, crash reporting, and support-access consent remain separate settings; granting local support access does not prove cloud access is configured.

## Verify effective behavior

Read back through the owning API after applying the change and account for restarts, cache invalidation, and token refresh. Test the intended operation as the intended principal, plus a denied principal or out-of-scope resource for access changes. Use existing test identities or isolated fixtures; do not impersonate a user or create production identities merely for proof. If those identities are unavailable, explicitly bound what was verified.

Check audit/log records with secrets redacted, retained access for unrelated users, and persistence across a supported reload when relevant. For Settings work inspect the actual product flow and save a screenshot or recording without secrets. Report before/after behavior, the affected scope, restart requirements, evidence, and a rollback/recovery action. Keep untested remote configuration or deployment steps distinct from locally verified changes.
