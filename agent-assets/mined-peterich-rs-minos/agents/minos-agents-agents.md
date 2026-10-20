# Agents feature — capability SSOT

## The one rule

**Harness / runtime capability facts have exactly one source: Rust.**

| Fact | Source |
|------|--------|
| Which runtimes exist | `minos_domain::AgentName` + daemon `list_clis` |
| Display name, model selection, reasoning-effort support | Domain metadata on `AgentName` → fields on `AgentDescriptor` / `CliDto` |
| Per-model effort ladder | Daemon `list_models` → `supported_reasoning_efforts` (honest; empty when unsupported) |

Desktop **projects** these values into UI. It must **not**:

- Hardcode a rival `RUNTIMES` / capability table that invents which agents exist
- Invent a default effort ladder (`["low","medium","high"]`) when the model returns empty efforts
- Use harness id string checks in render to show/hide capability fields (e.g. `if (runtime === "codex") showEffort`)

Presentation-only maps (colors, avatar tone) are fine and may fall back by agent id.

## Projection helpers

`features/agents/lib/agentConfigProjection.ts` is the pure boundary:

- `runtimeOptionsFromClis(clis)` — picker options from store/daemon inventory
- `effortOptionsForModel(model)` — **no fallback ladder**; empty ⇒ hide effort UI
- `shouldShowEffortPicker(model)` / `defaultEffortForModel(model)`

## Bot identity SSOT

- **Hub `agents` is bot identity SSOT** (global bot directory + digital body).
- Desktop Agents page: create/list/update/delete prefer Hub (`createCloudAgent` / `listCloudAgents` / `updateCloudAgent` / `deleteCloudAgent`) when the account is online.
- Daemon `agent_profiles` is an **offline / Host launch cache only** — not multi-device identity. Mirror by name is best-effort; never treat local-only profile rows as collab send targets without conversation membership.
- `ensureHostRuntimeAgent` seeds a host_runtime registry slot only — **never** join a conversation.

## `@agent` / `@profile` routing

- **Membership first**: conversation roster SSOT is **`participatingBots`** (botId + name + runtime) and Hub `…/participants` agents — not the deprecated `participatingAgents` runtime-label array. That array is derived for host-runtime ensure / badges only.
- Picker uses `buildAgentMentionOptions({ …, memberAgents })` with **roster-scoped** profiles only. Empty roster ⇒ no options. Non-member start is rejected by `resolveDispatchTargets` (and Hub plan delivery).
- **Composer / send path**: prefer Hub participants when Account is online (agent_id ∪ display name ∪ runtime as membership tokens). Offline: gate Host profiles by local roster tokens from `membershipTokensOfBots(participatingBots)` (fallback: deprecated `participatingAgents`). Never load the full unjoined profile directory as @ targets.
- Within the roster, prefer CLI inventory for bare runtime mention rows. `KNOWN_AGENTS` in `shared/lib/agent-route.ts` is an **offline parse fallback only** when clis are empty — not the capability catalog, and not a bypass of membership.
- **Bare `@agent`**: only if that runtime token is a **roster member**. Desktop collab send validates via `resolveDispatchTargets` then uplinks to Hub (`client_live`); bot activation is Hub plan_agent_deliveries on the bound Host — not local silent auto-attach of non-members. Session reuse (`@agent#short`) is explicit when the user picks an existing session from the picker.
- **`@ProfileName` / `@p/<id>` / Hub bot display name**: bot must be a roster member; named routes carry `profileId` / agent id. Insert `@Name` when the name is unique among roster bots + runtimes; otherwise `@p/<id>`. Runtime names win over same-named profiles at parse time.
- Do **not** offer unjoined Host profiles or bare non-member runtimes as collab @ targets. Do **not** invent dual-write membership into `participatingAgents` — write bots, derive runtime labels.
- Launch fields are **server-owned**: daemon `resolve_launch_options` loads the profile and applies model / reasoning_effort / instructions. Explicit request fields override profile fields (`explicit > profile > None`). `request.agent` must match `profile.runtime_agent`.
- **MCP** honors membership the same way: clients pass `profile_id` (or MCP `target_profile` name → id); daemon resolves launch options. Clients must not merge model/effort/instructions locally.

## How to add a new runtime

1. **Domain first** — add variant to `AgentName` in `crates/minos-domain/src/agent.rs` with `bin_name`, `display_name`, `supports_model_selection`, `supports_reasoning_effort`, `model_discovery`. Extend unit tests over `AgentName::all()`.
2. **Detect** — `minos-cli-detect` probes via `AgentName::all()`; no extra list needed if `bin_name` is correct.
3. **Model catalog** — `minos-daemon/src/model_catalog.rs`: probe and/or static list. Efforts must be honest (empty arrays when the runtime/model does not support effort). Never invent efforts for unsupported runtimes.
4. **Protocol** — `AgentDescriptor` already carries capability fields filled by `AgentDescriptor::new`. Desktop `CliDto` maps them through.
5. **UI projection** — no new hardcoded runtime list. Optional: add presentation entry in `agentMeta` (label/color only).
6. **Do not** regenerate mobile FRB solely for display polish unless mobile needs the new agent; domain + daemon remain SSOT.

## Non-goals (this surface)

- Mobile client host agent profiles (host profiles live on daemon; mobile does not manage them yet)
- Full Agents page visual redesign
- React Query
