---
name: recording-studio-api
description: Build Recording Studio APIs by registering capability actions and enabling them on endpoints. Use when exposing JSON APIs for users or AI agents, adding member actions, separating user vs admin named APIs, wiring Accessible, or avoiding duplicate UI/API logic.
---

# Recording Studio API

**Recording Studio API** (`recording_studio_api`) is the mountable engine for authenticated JSON APIs over Recording Studio. Add it after core and Accessible when integrations or AI agents need the same actions as the UI (`recording-studio-getting-started`).

The product idea is simple: **if the gem has UI or API, they share one domain action**. Register it once, enable it where it belongs, authorize with Accessible. Do not invent a JSON surface (or a dashboard) “for completeness.”

In an AI-heavy product world, agents need **broad, structured API access** to act on a user’s behalf. Prefer exposing the real domain actions over the API instead of forcing agents through brittle UI automation or one-off endpoints. Keep sensitive or privileged data on separate **named APIs** (for example a user/workspace API vs an admin/operations API) so agents and clients only receive the surface they are meant to use.

Do not rebuild the same “move folder / publish page / …” logic in a separate API controller. If the UI can do it, expose it as an API capability action and enable it on the relevant resource endpoint.

## Core idea

1. Addon gems own the **capability** (for example `:movable`, `:publishable`).
2. The gem registers an **API capability action** once (`:move`, `:publish`, …) with a handler.
3. The host (or gem) registers the **recordable type API** and lists which `capability_actions` that endpoint may call.
4. When the recordable enables the Recording Studio capability **and** the action is allowlisted, the API exposes it automatically.
5. Handlers authorize through **Recording Studio Accessible** via the request’s `AccessGrant`.

That keeps one action path for UI and API, with predictable access results for any actor.

## AI agents as first-class API actors

Treat AI agents like other actors that need to operate through the API:

- Give them credentials scoped to the right root / access recording.
- Expose the same capability actions the product already supports in the UI.
- Prefer extensive, well-documented endpoints (Scalar/OpenAPI) so agents can discover and call real operations.
- Still authorize every call with Accessible — extensive access does not mean bypassing roles or inventing a parallel ACL.

Design for agents that act **on behalf of** a person or workspace, not as a special snowflake stack. The API client is the credential principal; the Accessible actor on the access recording remains the authorization subject.

## Multiple APIs: user surfaces vs restricted admin surfaces

`RecordingStudioApi` supports **multiple named APIs**, not only the legacy `public` API. Use that to separate:

| Surface | Typical purpose |
| --- | --- |
| User / workspace API (`public` or similar) | Day-to-day content and actions an end user or their AI agent may perform in a root |
| Admin / operations API (`operations`, etc.) | Restricted diagnostics, site-wide credentials, privileged reporting, or other admin-only data |

Each named API can have its own versions, registries, OpenAPI metadata, enablement, logging, rate limits, and clients. An API client is bound to **exactly one** API — a public token does not work on an admin API and vice versa.

```ruby
RecordingStudioApi.configure do |config|
  config.api :operations do |api|
    api.openapi_title = "Operations API"
    api.api_versions = %w[v1]
    api.default_access = :read_only
    api.api_management_authorization_required = true
  end
end

RecordingStudioApi.register_recordable_type_api(
  "AdminRoot",
  api: :operations,
  operations: %i[index show]
)
```

Guidelines:

- Put user-facing resources and actions on the user API.
- Put restricted or site-admin information on a separate admin/operations API.
- Mount admin API screens only under admin roots when the data must stay off the user surface.
- Keep Accessible grants and management roles aligned so AI agents and humans get the same predictable boundaries.

## Prefer enablement over duplicate controllers

Bad:

- UI calls `folder.move!(...)`
- API invents a custom `FoldersController#relocate` with copied rules

Good:

```ruby
# Gem registers the action once
RecordingStudioApi.register_capability_action(
  :move,
  capability: :movable,
  version: "2.0.0",
  http_verb: :post,
  required_role: :edit,
  handler: RecordingStudioMoveable::Api::MoveRecording
)

# Folders endpoint enables that action
RecordingStudioApi.register_recordable_type_api(
  "Folder",
  operations: %i[index show create update destroy],
  capability_actions: %i[move],
  serializer: ->(folder, **) { { name: folder.name } },
  output_keys: %i[name],
  writable_attributes: %i[name]
)
```

If a user can move a folder in the UI because `:movable` is enabled, enable `:move` on the folders API endpoint. Same capability, same authorization story, no second implementation.

`capability_actions` is **default-deny**. An action must be:

1. Registered with `register_capability_action`
2. Backed by an enabled Recording Studio capability on the recordable
3. Listed in that type’s `capability_actions`

Only then is it callable and shown in OpenAPI.

## Access uses Recording Studio Accessible

API auth is credential-based (OAuth2 `client_credentials` or host bearer authenticators), but **authorization is still Accessible**.

Request flow:

1. Authenticate bearer token → API client / credential
2. Resolve `AccessGrant` (`api_client`, `credential`, `access_recording`, `root_recording`, access actor)
3. Dispatch to resource or capability handler
4. Handler calls `context.access_grant.authorize!(recording: ..., role: ...)` or `RecordingStudioAccessible.authorized?`

Do **not** invent custom API permission tables. Use Accessible. If Accessible cannot cover a case, ask how to proceed.

API clients sit under `RecordingStudio::Access` recordings in the tree, so they inherit the same root/hierarchy access model as users and other actors.

## Register resources quickly

Expose a recordable type as a flat JSON resource:

```ruby
RecordingStudioApi.register_recordable_type_api(
  "Page",
  serializer: ->(page, **) { { title: page.title } },
  output_keys: %i[title],
  writable_attributes: %i[title],
  operations: %i[index show create update destroy],
  capability_actions: %i[publish],
  relationships: {
    # named children / custom relationships as needed
  }
)
```

`operations` chooses standard CRUD exposure (`:index`, `:show`, `:create`, `:update`, `:destroy`). Omit only what you intentionally want closed.

Routes follow the recording tree (member actions beside resources):

```text
POST /recording_studio_api/api/v1/folders/:id/actions/move
```

(compat alias without `/actions/` also exists)

## Handler pattern

```ruby
class PublishRecording
  def self.call(context)
    context.access_grant.authorize!(recording: context.recording, role: :edit)

    # Prefer calling the same domain API the UI uses
    context.recording.publish!(actor: context.access_grant.actor)
    context.recording
  end
end
```

Keep business rules in the capability/domain layer. The API handler should authorize, adapt params, and call that layer — not fork behavior.

Member actions default to required role `:edit`. Override per action or via `config.capability_action_roles`.

## UI slice + API slice checklist for gem authors

When adding a capability to a Recording Studio gem:

1. Implement the domain behavior once (UI and services call it).
2. Register `RecordingStudioApi.register_capability_action(...)` for the API slice.
3. Document which recordable types should list it in `capability_actions`.
4. Ensure Accessible roles match the UI (`required_role`, through-actors if needed).
5. Add OpenAPI/input contract metadata so Scalar docs stay accurate.
6. Cover gem suite + dummy app tests, including unauthorized API calls.

## Host setup sketch

```bash
bin/rails generate recording_studio_api:install
bin/rails generate recording_studio_api:migrations
bin/rails db:migrate
```

Then:

1. Enable `:accessible` (and `:api_access_point` where API keys hang) on the right recordables.
2. Register recordable type APIs and capability actions.
3. Mount the engine / Scalar docs as needed.
4. Provision API clients from an Access recording (`ProvisionApiClient` / admin screens).

For Accessible details, follow `recording-studio-access`. For admin API screens, follow `recording-studio-admin`.

## MCP and MCP UI are other gems

This gem is the JSON wrapper. Authorization stays Accessible / `AccessGrant`. It is not a second ACL and not an MCP server.

- **API** may store a widget id (`ui:` on `register_endpoint` / `register_capability_action`). Lookups: `ui_for` / `actions_for_ui`. It does not serve `ui://`.
- **MCP** (`recording_studio_mcp`) is the protocol adapter over this API. When MCP UI is loaded, it serves `ui://` resources.
- **MCP UI** (`recording_studio_mcp_ui`) registers widgets and packages FlatPack HTML.

Need MCP Apps? Add those gems (`recording-studio-gems`). Do not grow `DEFAULT_OPERATIONS` or invent widget serving here.

## Guardrails

- One domain action → UI + API. Do not duplicate business logic in API-only controllers.
- Design APIs so AI agents can act extensively through real capability actions, still gated by Accessible.
- Use multiple named APIs to separate user access from restricted admin/operations information.
- Enable actions explicitly with `capability_actions`; do not assume registration alone exposes them.
- Authorize with Accessible / `AccessGrant`, never a parallel ACL.
- Keep responses flat (`id`, `type`, `root_id`, `parent_id`, serializer keys). No legacy `attributes` / `relationships` wrappers.
- Nested writes use registered relationships; parent changes use the move capability action, not `parent_id` on update.
- If the API gem or Accessible cannot support the scenario, ask how to proceed.
