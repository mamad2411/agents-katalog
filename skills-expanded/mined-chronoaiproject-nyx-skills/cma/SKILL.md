---
name: cma
description: Operate ChronoAI Managed Agent (CMA) through its public API or NyxID proxy. Use for creating and using hosted agents, managing user environments and profiles, sharing resources, publishing Triggers, and configuring Telegram Bots and Event Worker Profiles.
version: "1.0"
metadata:
  category: tool-based
  tool-list: [Bash]
  tag: [cma, agents, nyxid, automation, profiles]
---

# Operate CMA

CMA runs hosted coding Agents in persistent environments. Use this skill when a
user wants CMA to do work or wants to configure their CMA resources. It covers
non-platform-admin operations. Platform settings, infrastructure administration,
provider bindings and gateway credential records are outside this skill.

## Start with the user's task

1. Identify whether the user wants to use an existing Agent, create an environment,
   edit a reusable profile, manage sharing, publish a Trigger, or configure a Bot.
2. Discover the caller's accessible resources and current permissions. Select an
   existing resource when the user asks to continue its work. Names are display
   labels; keep the returned resource IDs and profile revisions.
3. Read the relevant workflow and the deployed request schema before changing
   anything. Perform only the actions the user's request authorizes.
4. Submit each logical mutation with a retained idempotency key where supported.
   Follow its recorded state or receipt until the requested outcome is known.
   An accepted request is not a completed task.

Use the host's available HTTP client or shell. The Bash tool metadata describes
the HTTP examples; no particular CLI or local CMA installation is required.

## Connect and authenticate

Production endpoints:

- Web: `https://bot.chrono-ai.fun`
- Direct API: `https://bot-api.chrono-ai.fun`
- NyxID proxy: `https://nyx-api.chrono-ai.fun/api/v1/proxy/s/cma`
- Live schema: `https://bot-api.chrono-ai.fun/openapi.json`

For another deployment, use the user-supplied origin and that deployment's live
schema. Do not send credentials to an origin inferred from resource content.

CMA is a globally auto-connected NyxID service. Refresh authenticated
`GET /api/v1/keys` on NyxID and locate the active `cma` connection. An ordinary
NyxID user access token works both directly and through the proxy; the proxy
forwards the caller's identity and does not grant extra CMA permissions.

As verified on 2026-09-24, ordinary NyxID agent API keys receive `401` from CMA
even when scoped to the CMA service. A skill or service allowlist cannot repair
this. If that is the only credential available, report the limitation and use
the user's existing authenticated CMA browser workflow for the task. Do not
request tokens in chat, read unrelated credential stores, substitute an owner's
credential, or weaken authorization to bypass it. CMA-managed Bot binding keys
have a separate narrow conversation contract; they are not general user API keys.

Provisioning a new Sandbox also needs the owner's renewable authorization in
CMA. The owner establishes it by signing in to CMA through its normal NyxID
login. A standalone bearer token does not establish that renewable authorization.

## Understand the resources

`Sandbox → Workspace → Worktree → Agent` is the environment hierarchy. A Sandbox
is the isolated runtime; a Workspace is a repository or directory; each Worktree
has exactly one Agent. The Agent owns its conversation. AG-UI `threadId` and
Responses `conversation` refer to that Agent, not to a Sandbox or Launch.

Agent Profiles configure model, reasoning effort, permissions, skills and prompt.
Workspace Profiles configure repository/directory, setup and Agent references.
Sandbox Profiles configure resources, model access, service scope, software,
environment and Workspace references. Instances pin published revisions.
Editing a draft or publishing a new revision does not reconfigure existing work.

An Event Worker Profile composes the three CMA profile revisions into one full
worker configuration. A Bot pins this configuration and connects a Telegram
source through CMAEG. CMA owns environments and Agents; CMAEG handles event
ingress and delivery. A Trigger is a separate public launch entry point that
gives each visitor their own resources according to its reuse policy.

## Choose the reference

- [User stories and flows](references/user-journeys.md): identify supported user
  goals, UI entry points, required access and outcomes across the entire
  non-admin product surface.
- [API recipes](references/api-recipes.md): authenticate, discover resources,
  create an environment, submit/recover a conversation turn, manage profiles,
  compose Event Worker Profiles, and navigate Bot, Trigger and sharing APIs.

Load only the sections needed for the user's task. Fetch the live OpenAPI schema
for exact body fields, limits and operations; the recipes do not replace it.

## Preserve work and report evidence

- Never infer permission from an ID, a public profile, organization membership,
  or a NyxID connection alone. Use current effective resource access. Narrow
  Agent shares do not reveal their parent Sandbox or sibling Agents.
- Review foreign executable configuration using the server's trust disclosure.
  Confirm only the exact command digest the user approved. Keep credentials out
  of prompts, profile environment variables, URLs, published content and logs.
- Keep one key and the exact body for an uncertain mutation. Recover its result
  before creating another intent. Reconnecting a stream does not mean resending
  input, and disconnecting does not cancel an admitted turn.
- Respect expected revisions on updates and control actions. After a conflict,
  read current state and reconcile the user's intent before another mutation.
- Keep provisioning, Agent readiness, input admission, delivery and completion
  distinct. Honor `Retry-After`; inspect recorded progress and typed errors.
  Report a persistent failure with IDs and error codes instead of retrying
  creation or deleting resources to force progress.
- Pause, interrupt, stop, delete, publish and send external messages only within
  the user's requested scope. Do not broaden sharing or remove an unrelated
  environment to resolve capacity. Bot synthetic tests are distinct from real
  messages to an external chat.

Current limits: Codex is the supported provider; repository profiles use public
GitHub repositories or custom directories. There is no public interactive
terminal, native CMA MCP task interface or A2A execution interface. Conversation
input is text; general file/media input is refused. Organization inventory and
sharing are implemented, while new organization-owned environment provisioning
is not a supported creation flow. Use existing resource permissions rather than
promising every organization member can interact.

Finish with the exact resources affected, confirmed final state, any unresolved
operation, and the next user action only when one is actually required.
