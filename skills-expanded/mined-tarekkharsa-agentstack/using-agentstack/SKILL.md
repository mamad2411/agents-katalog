---
name: using-agentstack
description: Operate and troubleshoot AgentStack projects, personal capability libraries, zero-files MCP delivery, toolsets, secrets, trust, policy, machine bootstrap, and legacy MCP cleanup. Use whenever a task changes or diagnoses an AI coding CLI setup managed by AgentStack.
---

# Use AgentStack

## Start with the state

Run `agentstack status` first. Use `agentstack doctor` only when status points to
a problem or deeper verification is needed.

Read these facts separately:

- `locked`: portable content is pinned; this does not mean a connection is live.
- `trusted`: a human approved the current manifest and lock on this machine.
- `default toolset`: what a trusted new agent connection opens automatically.
- `live toolset`: a process-scoped connection that exists right now.
- `delivery`: which capabilities are served live and which are written to files.

## Follow the delivery decision

When status says skills or MCP servers are served live:

- Do not run `use`, `apply`, or `render-locally` to make them appear.
- Do not create `.mcp.json`, `.claude/skills/`, `.agents/skills/`, or similar
  capability folders.
- Use the trusted default toolset. If several toolsets exist without a default,
  ask the user which one should be selected.
- The connection already receives loadable skill names and one-line
  descriptions. Refresh or filter them with `agentstack_list_loadable(query)`.
- Load only a needed full body with `agentstack_load(name, reason)`. The user
  does not need to say the skill name when its description clearly matches.
- Discover proxied runtime tools and their schemas with `tools_search` only
  when the task needs one.

File-only CLIs and capability kinds are rendered automatically. An explicit
`render_locally` override is a compatibility choice, not the normal live path.

## Change the source of truth only

- Change `.agentstack/agentstack.toml`, legacy `agentstack.toml`, or the
  personal library. Never hand-edit generated provider configuration.
- Keep secret values out of manifests and libraries. Declare `${REF}` and tell
  the user to run `agentstack secret set REF` on each machine.
- After changing selected skills or servers, preview with `agentstack lock`.
  Use `agentstack lock --write` only with authorization.
- Never run `agentstack trust` for the user. Show what changed and leave the
  consent action to the human.
- Preview any write. Do not add `--write` unless the user explicitly authorized
  that AgentStack change.
- Respect policy and guard refusals. Explain them; never retry around them.

## Preserve native and app-owned capabilities

- Installing AgentStack is not permission to delete existing CLI configuration.
- `init` imports representable MCP entries and supported settings after review;
  it does not automatically import native skills or delete source entries.
- Leave Computer Use, built-in connectors, plugins, and MCP servers installed
  inside another application's bundle with that owning application. Do not
  adopt them unless the user explicitly requests `--include-tool-managed`.
- When the user wants an existing native skill to become portable, preview
  `agentstack adopt --to-library`; write only with explicit authorization.
- Put reusable user-owned capabilities in the linked central library. Keep
  repository-specific content in the project manifest or `.agentstack/`.

## Work across machines

Treat the three layers differently:

1. Project manifest and lock travel with the repository.
2. Reusable definitions travel through the user's personal library Git remote.
3. Secrets, trust, machine policy, installed CLIs, leases, and audit stay local.

On a new machine, preview with `agentstack up --library <git-url>` and leave the
`--write` application to the human. Afterwards, bare `agentstack up` is the
safe refresh preview. AgentStack is standalone; the same local setup works when
a provider is launched directly or by stock T3 Code or another supervisor.

Read only the reference matching the task:

- [references/recipes.md](references/recipes.md) — mutations, bootstrap, drift,
  secrets, and legacy cleanup.
- [references/library.md](references/library.md) — linked sources, precedence,
  project locks, and cross-machine behavior.
- [references/instructions.md](references/instructions.md) — reusable
  CLI/model-specific instruction variants.
