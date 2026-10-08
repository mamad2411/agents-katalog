---
name: fruxon-use-integrations
displayName: Use Integrations in Fruxon
description: >
  Wire integration tools into an agent: discover what's connected,
  attach the right tool, point it at a credential slot. Load when
  adding tools (Slack, GitHub, Jira, Drive…) to a Fruxon agent.
---

You are now operating as a Fruxon integrations specialist.

## Discovery
- `fruxon describe` — whole CLI tree as JSON (recommended for an
  AI-agent driver — gives commands, flags, types, and examples in
  one call).
- `fruxon integrations list` — the integration **catalog** for your
  workspace (id, displayName, type, tags). Being listed means the
  integration exists, NOT that credentials are configured. Filters
  (from the server's `IntegrationListRequest`):
  `--has-configs` (only *connected* ones — the quick "what can I
  actually use" view), `--has-triggers` (integrations that declare a
  trigger), `--has-channels` (messaging-capable: Slack/Telegram/Twilio/…),
  plus `--query` / `--type` / `--tag` (repeatable).
- `fruxon integrations configs list <integration>` — the **tenant
  configs** configured for that integration: their ids, and whether
  each is published. This is how you get the `tenantConfigId` a slot
  needs. `fruxon integrations configs get <integration> <config>`
  prints one config's full payload (auth shape, `publishedRevisionId`)
  — use it to confirm a config is published before pointing a slot at it.
- `fruxon integrations get <id>` — catalog metadata for one
  integration (description, tags). (It does not report auth status —
  use `configs list` for that.)
- `fruxon tools list <integration>` — tools the integration exposes
  (id, displayName, toolType, actionType — e.g. `READ_ONLY`).
- `fruxon tools get <integration> --tool <tool>` — the tool descriptor: id,
  type, actionType, **and its `parametersMetadata`** (each input's
  name/type/required/description). The LLM fills these at call time,
  so this is where you learn the shape the agent has to produce.

  The tenant list API deliberately omits internal platform tools, so
  `tools list knowledge_base` and `tools list assets` may be empty even
  when the tools are runnable. Their known IDs are
  `create_knowledge_document`, `get_knowledge_document`,
  `publish_knowledge_document`, `search_knowledge_base`, and
  `update_knowledge_document` under `knowledge_base`; and
  `list_asset_documents`, `read_document_chunks`, and `search_assets`
  under `assets`. Pass any one to `tools get ... --tool ... -o json` to
  discover its exact parameter metadata.

  Where the two families meet, mind which id you are holding. A
  `search_assets` hit carries **two**: `document_id` is the index's own
  id for the indexed copy — what `read_document_chunks` takes, alongside
  `asset_id` — while `knowledge_document_id` is the editable document,
  and the only one `get_knowledge_document` and
  `update_knowledge_document` accept. They are never interchangeable,
  and `document_id` is not stable: re-publishing a document whose body
  changed re-indexes it under a new one. `list_asset_documents` and
  `read_document_chunks` report `knowledge_document_id` too, and a hit
  from anything that is not a knowledge base simply has none.
- `fruxon agents schema <agent>` — the typed parameter metadata for
  the *agent that uses these tools*. Pair with
  `fruxon agents validate <agent> -p k=v` to pre-flight a `run`
  payload before submitting.
- `fruxon agents draft validate <agent>` — lint the draft body itself
  before pushing. It catches the integration-wiring mistakes that
  otherwise only fail at run time: a built-in tool placed in
  `definition.tools` instead of `provider.builtInTools`, an integration
  tool whose `integrationConfigId` isn't a declared slot, a tool that
  omits it where no binding can supply one, a slot id that isn't a
  GUID, and a binding key that disagrees with its slot.
- `fruxon assets create --file ./docs.pdf -o id` + `fruxon assets wait
  <id>` — provision a file-backed RAG source before adding it to the
  definition's `assetConfig.assetIds`. Use `fruxon assets list` / `get` for existing
  assets and `operations` to inspect ingestion progress.

## The two tool flavors
Confirm which kind a tool is before placing it in the definition:

**Integration tools** — tied to an external service. Found via
`fruxon tools list <integration>`. Examples: `slack.send_message`,
`github.list_commits`, `jira.create_issue`.

   Where they go: `definition.tools`.
   Required fields:
   - `toolKey.integrationId` = integration id (`"slack"`)
   - `toolKey.id`           = tool id (`"send_message"`)
   Optional:
   - `integrationConfigId`  = the **id of an integration slot** the
                               revision declares (see next section) —
                               a GUID, NOT the tenant config id. Omit
                               it to inherit the agent-wide binding for
                               the integration, which is the usual case;
                               pin it only to single out one slot among
                               several.

**Built-in tools** — provider-native or Fruxon-native. Examples:
`web_search`, `code_interpreter` (provider-specific),
`approval_request` (Fruxon, cross-provider).

   Where they go: `definition.provider.builtInTools`.
   Required fields:
   - `toolKey.integrationId` = `""`  (empty string, important!)
   - `toolKey.id`           = tool name (`"web_search"`)
   - NO `integrationConfigId`

## Declaring integration slots & bindings
A revision never embeds credentials. It declares **slots** that point
at a published tenant integration config, and tools reference a slot
by id. Three pieces, all at the top level of the revision body:

1. **`integrationSlots`** — one entry per credential used:
   ```jsonc
   {
     "id": "<GUID>",                  // YOU mint it; tools reference it
     "integrationId": "slack",        // must match the tenant config's integration
     "displayName": "Slack",
     "tenantConfigId": "<config-GUID>"  // a PUBLISHED tenant config
   }
   ```
2. **Each integration tool** either sets `integrationConfigId` to a
   slot's `id` (reuse the exact GUID) or omits it and inherits the
   binding below. An integration with exactly one slot is auto-bound by
   the server on create, so that case needs neither.
3. **`integrationBindings`** — `{ "<integrationId>": "<slotId>" }`, the
   agent-wide default slot for that integration. The key must equal
   the slot's `integrationId`.

Where the ids come from:
- `tenantConfigId` ← `fruxon integrations configs list <integration>`;
  pick a **published** config (slots reject unpublished ones).
- The slot `id` is a GUID you generate and reuse across the slot,
  every tool's `integrationConfigId`, and the binding value.

At save the server validates each slot's tenant config **exists**,
**matches the slot's `integrationId`**, and **is published** — but it
does NOT check that a tool's `integrationConfigId` actually matches a
slot. A wrong/typo'd config id therefore deploys fine and only fails
at run time. See `fruxon-build-agent` for a complete example body.

## Common pitfalls
- Putting `web_search` in `definition.tools` instead of
  `provider.builtInTools` — resolution fails because there's no
  integration backing `("", "web_search")`.
- `integrationConfigId` not equal to a declared slot `id` — NOT caught
  at create; the tool call fails at **run** with an auth-not-found
  error. Keep the slot GUID identical in the slot, the tool, and the
  binding. (Leaving the field out is not this mistake — that inherits
  the binding. The one omission that breaks is an integration with
  several slots and no binding to choose between them.)
- Slot `id` (or `tenantConfigId`) not a GUID — rejected at create
  (`could not be converted to System.Guid`).
- Slot `integrationId` ≠ the tenant config's integration — rejected at
  create (a `slack` slot can't point at a `github` config).
- Mixing tool key forms — for Slack, `slack.send_message` is the
  PromptTemplate string form; `{integrationId:"slack", id:"send_message"}`
  is the object form. The CLI/JSON uses the object form.
- Using `IntegrationId: null` for built-ins — must be empty string
  `""`, not null.
