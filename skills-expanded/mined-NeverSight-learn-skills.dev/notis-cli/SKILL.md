---
name: notis-cli
description: Use when agents should work through the Notis CLI, especially to develop Notis apps locally or to access Notis, Composio, or MCP tools they do not currently have loaded directly.
feature_flag: cli_access
mcp_resource: true
mcp_tool_patterns: []
---

# Notis CLI Skill

Use this skill when the user wants work done through the Notis CLI.

This skill covers two main CLI workflows:

1. Developing Notis apps locally.
2. Accessing Notis, Composio, and MCP tools through the CLI.

## When to use this skill

Activate this skill when:

- the user wants to init, develop, build, verify, link, pull, or deploy a Notis app through the CLI
- the current agent does not have the tool it needs in its direct tool list
- the user wants direct MCP access through Notis
- the user wants to use an integration-backed capability through Notis rather than a first-class local tool
- the task mentions the `notis` CLI directly

Use the registry-resolved published npm package everywhere:

- `npx --package @notis_ai/cli@latest -- notis ...`

Always use this NPX command form so the agent runs the current published CLI. In hosted shells, the CLI is pre-authenticated through `NOTIS_JWT`. On a local machine the CLI holds its own OAuth grant: `notis login` authorizes one in the browser, and signing in to the Notis desktop app authorizes one automatically for that account. Either way the grant belongs to the CLI, which refreshes it without the desktop app running.

`@latest` is correct for every account, including beta ones. Each deployment reports which published build belongs to it, `notis login` pins that on the profile, and a later run that finds itself on the wrong build hands the invocation to the right one before doing anything. Never substitute a channel by hand: pinning `@beta` on a production profile is how a machine ends up running a build its API does not expect. `notis doctor` reports the active channel, and `NOTIS_CLI_AUTO_CHANNEL=0` turns the hand-off off for a run.

The CLI bundles this `notis-cli` base skill and refreshes its canonical copy under `~/.notis/skills/base/` on every launch. It is independent of account-skill sync, feature flags, target selection, and cloud deletion.

## Profiles: accounts and endpoints

A profile is one account paired with one API endpoint. Profiles live side by side; switching between them never signs any of them out.

- `npx --package @notis_ai/cli@latest -- notis profile list` — every profile on this machine, with its endpoint, user, and whether it is signed in. The active one is marked.
- `npx --package @notis_ai/cli@latest -- notis profile use <name>` — change which account subsequent commands run as.
- `npx --package @notis_ai/cli@latest -- notis --profile <name> <command>` — run a single command as another account without changing the active one.
- `npx --package @notis_ai/cli@latest -- notis login --profile <name>` — add an account. The existing profiles keep their credentials.
- `npx --package @notis_ai/cli@latest -- notis logout` — sign out of the active profile only; pass `--all-profiles` to clear every one.

Read the profile before acting on the user's data. `notis whoami` reports the account and endpoint a command will hit; if that is not the account the user meant, switch profiles rather than proceeding.

### Working against a local `./dev.sh` backend

`./dev.sh` exposes its test account as a lease-backed profile (`dev-<workspace>-<hash>`) pointing at the local backend, and prints the name on startup. Its credential stays in that worktree and it is the automatic default there, so `notis ...` targets the local API and test user with no extra flags. It is not a stored account profile and cannot be selected outside the worktree.

Two rules follow from the dev credential being scoped to that local backend:

- A `dev-*` profile only exists while its `./dev.sh` lease is running. If it is stopped, the CLI fails with `dev_runtime_unavailable` instead of sending the test user's token to the live API.
- To reach a real account from inside a worktree — including when the local backend is wedged — name a real profile explicitly: `notis --profile <name> ...`. That is the supported escape hatch.

## Critical rule for missing tools

If the tool you need is not already available in your current tool surface, do not stop and do not assume the task is blocked.

Use the Notis CLI as the fallback access layer.

This is especially important when:

- you need direct MCP tools
- you need a Composio-backed integration tool
- you need a Notis tool that is not exposed as a first-class command in your current environment
- you need to discover the canonical tool name before execution

Treat the Notis CLI the same way you would treat a Composio-style tool router flow: discover what is available first, then execute the right tool through the CLI.

## Section 1: Developing Notis Apps

Use this section when the goal is to create or update a Notis app from a local workspace.

Notis apps are Vite + React projects using `@notis/sdk`. The workflow is init or pull, dev, build, verify, create/link, deploy, then an explicitly confirmed Store submission when requested.

Important: `deploy` only updates the installed app artifact for the current user or team. Store submission is a separate, user-gated step. After the user explicitly confirms that the current App Details page and Store listing are ready, `apps publish --confirm-ready` submits the matching deployed version through the backend review flow.

### App development workflow

1. Scaffold a new app (every published Store app is a scaffold; `notis apps scaffolds list [--search <term>]` lists them from the public registry, and `--from <slug>` downloads that app's source):
   - `npx --package @notis_ai/cli@latest -- notis apps init ["My App"] [--from <slug>]`
2. Or pull an existing app's source to edit it locally (the project is linked automatically):
   - `npx --package @notis_ai/cli@latest -- notis apps pull <app-id>`
   - then run `npm install`, `npx --package @notis_ai/cli@latest -- notis apps dev`, edit, build, and deploy
3. Develop locally with live reload:
   - `npx --package @notis_ai/cli@latest -- notis apps dev`
4. Build the production artifact:
   - `npx --package @notis_ai/cli@latest -- notis apps build`
5. Verify the built artifact headlessly:
   - `npx --package @notis_ai/cli@latest -- notis apps verify`
6. For a brand-new app already run with `apps dev`, deploy to promote that development app in place:
   - `npx --package @notis_ai/cli@latest -- notis apps deploy`
7. Or link the project to an existing remote app (skip if you used `pull`):
   - `npx --package @notis_ai/cli@latest -- notis apps link`
8. Deploy the artifact to Notis:
   - `npx --package @notis_ai/cli@latest -- notis apps deploy`
9. Check project health:
   - `npx --package @notis_ai/cli@latest -- notis apps doctor`
10. Only after the user explicitly approves the current Store preview, submit the deployed version:
   - `npx --package @notis_ai/cli@latest -- notis apps publish --confirm-ready`

### App development rules

- Always `build` before `deploy`; run `verify` before deploy when validating an app change.
- Prefer `npx --package @notis_ai/cli@latest -- notis apps deploy` for the first deploy of a project already run with `apps dev`; it promotes the development app in place.
- Link before `deploy`, or pass `--app-id <id>` when intentionally deploying without writing local link state.
- Use `npx --package @notis_ai/cli@latest -- notis apps doctor` to diagnose configuration or dependency issues.
- Use `npx --package @notis_ai/cli@latest -- notis apps list` to discover existing app IDs before linking.
- Never treat deploy approval as Store approval. Set visibility to Team or Public first, then run `apps publish --confirm-ready` only after the user explicitly confirms the current App Details page and Store listing.
- `apps publish --confirm-ready` submits the deployed snapshot through the same backend review flow as App Details. It must reject missing confirmation, incomplete listing media, a local/deployed version mismatch, private visibility, or an existing pending review.

### App development command reference

- `npx --package @notis_ai/cli@latest -- notis apps list` -- list accessible apps
- `npx --package @notis_ai/cli@latest -- notis apps init` -- scaffold a new Vite + React + `@notis/sdk` project
- `npx --package @notis_ai/cli@latest -- notis apps pull <app-id> [dir] [--force] [--source-version <n>]` -- download the persisted source snapshot for an installed app and link the local directory to that app/version; legacy apps must be redeployed once with the current CLI before they can be pulled
- `npx --package @notis_ai/cli@latest -- notis apps dev` -- discover local apps, register desktop-local dev sessions, and load them as DEV-badged Workspace rows in the Electron Portal
- `npx --package @notis_ai/cli@latest -- notis apps build` -- compile the production artifact
- `npx --package @notis_ai/cli@latest -- notis apps verify` -- headless render-smoke packaged routes before deploy
- `npx --package @notis_ai/cli@latest -- notis apps create` -- create a fresh remote app and optionally link the local project
- `npx --package @notis_ai/cli@latest -- notis apps link` -- associate the project with a remote app
- `npx --package @notis_ai/cli@latest -- notis apps deploy` -- upload the artifact and editable source snapshot to the linked installed app in Notis
- `npx --package @notis_ai/cli@latest -- notis apps deploy --direct` -- deploy directly to Supabase storage, bypassing the backend server (auto-fallback when server is down)
- `npx --package @notis_ai/cli@latest -- notis apps publish --confirm-ready` -- submit the matching deployed version for Team or Public Store review after explicit user confirmation
- `npx --package @notis_ai/cli@latest -- notis apps doctor` -- run project diagnostics

App Details remains the visual review surface and offers the same Publish/Update action. The CLI command is for agents completing an already approved submission; it does not weaken the separate confirmation gate.

If the task is specifically about app structure, runtime behavior, or database/view packaging, pair this skill with the `notis-apps` skill. Use `notis-cli` for the command workflow and `notis-apps` for the product/runtime contract.

## IMPORTANT: When NOT to use tool access for app development

When building or deploying a Notis app, do NOT use `npx --package @notis_ai/cli@latest -- notis tools exec` for any of these operations:

- Creating databases -- declare them in `notis.config.ts` instead
- Loading or saving app files -- use `npx --package @notis_ai/cli@latest -- notis apps build` and `npx --package @notis_ai/cli@latest -- notis apps deploy`
- Linting app files -- use `npx --package @notis_ai/cli@latest -- notis apps build` which validates automatically
- Managing app routes -- write standard Vite + React pages in `app/`, not raw JS files

The only `npx --package @notis_ai/cli@latest -- notis tools exec` calls that are valid during app development are for testing the app's runtime behavior after deployment (e.g., querying a database to verify data was created).

## Section 2: Accessing Tools Through the Notis CLI

Use this section when the current agent does not already have the right tool and needs to reach tools through Notis.

This is the main escape hatch for:

- direct MCP access
- Composio-backed integrations
- native Notis tools that are available through the generic CLI tool bridge
- any task where you need to discover the canonical tool name and schema before execution

### Tool access workflow

1. List available toolkit namespaces:
   - `npx --package @notis_ai/cli@latest -- notis tools toolkits --timeout-ms 90000`
2. Search for the capability you need using natural language:
   - `npx --package @notis_ai/cli@latest -- notis tools search "<query>" --timeout-ms 90000`
   - optionally add known field hints with `--known-fields "<key:value>"`
3. If needed, inspect the exact tool and parameter schema:
   - `npx --package @notis_ai/cli@latest -- notis tools describe <tool-name> --timeout-ms 90000`
   - `npx --package @notis_ai/cli@latest -- notis tools exec <tool-name> --get-schema --timeout-ms 90000`
4. Validate arguments before execution when the tool is mutating or the schema is non-trivial:
   - `npx --package @notis_ai/cli@latest -- notis tools exec <tool-name> --dry-run --arguments '<json>'`
5. Execute the tool:
   - `npx --package @notis_ai/cli@latest -- notis tools exec <tool-name> --arguments '<json>'`
6. If multiple independent calls are needed, use:
   - `npx --package @notis_ai/cli@latest -- notis tools exec-parallel '<json-array>'`
7. If the toolkit is not connected yet, start its connection flow:
   - `npx --package @notis_ai/cli@latest -- notis tools link <toolkit>`
   - For a revoked or invalid credential-based connection, reconnect with credential JSON on stdin: `npx --package @notis_ai/cli@latest -- notis tools link <toolkit> --reconnect --credentials -`

### Discovery latency and caching

The discovery bridge may query several connected MCP servers on a cold run and
can legitimately take longer than the CLI's general 30-second timeout. Always
use `--timeout-ms 90000` for `tools toolkits`, `tools search`, `tools describe`,
and schema-only discovery calls. If a discovery call returns `network_timeout`,
retry that same command once with `--timeout-ms 90000`; do not start a new
query, invent a tool name, or loop on the default 30-second command.

Discovery is idempotent but should be bounded: run the toolkit listing once per
task, run one natural-language search per distinct capability, and cache the
returned canonical tool names and schemas for the rest of the current turn.
After a successful search/schema response, call the returned canonical tool
directly (with a dry-run before mutations) instead of repeating the same
discovery request before every connected-service action.

### Tool access rules

- Never guess tool names. Discover them with `npx --package @notis_ai/cli@latest -- notis tools search` first.
- Prefer first-class CLI commands when they exist, but use `npx --package @notis_ai/cli@latest -- notis tools ...` whenever the capability is not covered by a dedicated command.
- When you know the tool name but not the argument shape, use `npx --package @notis_ai/cli@latest -- notis tools describe` or `--get-schema` before execution.
- Use `--dry-run` before mutating calls when you want schema validation without execution.
- If a toolkit is missing, use `npx --package @notis_ai/cli@latest -- notis tools link <toolkit>` to start the connection flow.
- Use `--reconnect` to replace an existing connection. If multiple accounts exist, select one with `--connection-id <id>`.
- For API keys, basic auth, or other credential JSON, prefer `--credentials -` and pipe or redirect stdin. Avoid inline secrets because they can enter shell history and process listings.

### Toolkit mental model

Typical toolkit namespaces include:

- `notis` for native Notis tools
- `composio-*` for Composio-backed integrations
- `mcp-*` for MCP-backed tools

The pattern is:

1. discover toolkits
2. search tools
3. inspect schema if needed
4. execute the canonical tool

### Tool access examples

Find a tool:

```bash
npx --package @notis_ai/cli@latest -- notis tools toolkits
npx --package @notis_ai/cli@latest -- notis tools search "list today's calendar events"
```

Inspect a tool before execution:

```bash
npx --package @notis_ai/cli@latest -- notis tools describe composio-googlecalendar-list_events
npx --package @notis_ai/cli@latest -- notis tools exec composio-googlecalendar-list_events --get-schema
```

Dry-run a tool call:

```bash
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_GET_DATABASE --dry-run --arguments '{"database_slug":"tasks"}'
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_QUERY --dry-run --arguments '{"database_id":"tasks-db-id","query":{"page_size":10}}'
```

Execute a tool call:

```bash
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_GET_DATABASE --arguments '{"database_slug":"tasks"}'
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_QUERY --arguments '{"database_id":"tasks-db-id","query":{"page_size":10}}'
```

Connect a missing toolkit:

```bash
npx --package @notis_ai/cli@latest -- notis tools link github
```

Reconnect a credential-based toolkit without putting the secret in shell history:

```bash
npx --package @notis_ai/cli@latest -- notis tools link dataforseo --reconnect --credentials - < credentials.json
```

## Native database access

Native Notis databases are accessed through the generic tool workflow, not a first-class database command group. Use these canonical tool names:

- `LOCAL_NOTIS_DATABASE_LIST_DATABASES` -- list databases accessible to the current profile
- `LOCAL_NOTIS_DATABASE_GET_DATABASE` -- inspect read-only metadata and schema detail
- `LOCAL_NOTIS_DATABASE_QUERY` -- query documents from a database
- `LOCAL_NOTIS_DATABASE_UPSERT_DATABASE` -- create or update a database schema. Every database belongs to a Notis app: creation requires the owning app's slug or id in the `app` argument (create the app first with `LOCAL_NOTIS_CREATE_APP` if needed)

Example workflow before building an app:

```bash
npx --package @notis_ai/cli@latest -- notis tools search "list Notis databases"
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_LIST_DATABASES --arguments '{}'
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_GET_DATABASE --get-schema
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_GET_DATABASE --arguments '{"database_slug":"social_media_calendar"}'
npx --package @notis_ai/cli@latest -- notis tools exec LOCAL_NOTIS_DATABASE_QUERY --arguments '{"database_id":"social-media-calendar-db-id","query":{"page_size":1}}'
```

When `LOCAL_NOTIS_DATABASE_LIST_DATABASES` or `LOCAL_NOTIS_DATABASE_GET_DATABASE` returns a database ID, prefer `database_id` for `LOCAL_NOTIS_DATABASE_QUERY`; `database_slug` remains supported as a fallback.

## Supporting commands

- `npx --package @notis_ai/cli@latest -- notis whoami` — confirm which account and endpoint a command will target
- `npx --package @notis_ai/cli@latest -- notis doctor` — verify CLI config, auth, routing, and API reachability before relying on the CLI
- `npx --package @notis_ai/cli@latest -- notis describe <command...>` — get the exact command contract for first-class CLI commands

## Summary

Use `notis-cli` for two things:

1. local app development through `npx --package @notis_ai/cli@latest -- notis apps ...`
2. tool discovery and execution through `npx --package @notis_ai/cli@latest -- notis tools ...`

Most importantly: if you do not currently have the tool you need, especially for direct MCP or integration work, use the Notis CLI instead of treating the task as blocked.

## Troubleshooting

### CLI returns `auth_expired` or `auth_missing`

The profile's browser authorization has lapsed or was never granted. Run
`notis login` (add `--profile <name>` when the failing profile is not the
active one) and have the user approve the browser prompt. In JSON/agent mode
the first hint is the exact command to run. Do not copy refresh tokens into
commands or try to mint a credential yourself.

If the profile is a `dev-*` one, the fix is to restart `./dev.sh` in the
workspace it belongs to, or to switch to a real account profile.

### Deploy fails with "network_error" or "fetch failed"

The CLI defaults to the live Notis API (`https://api.notis.ai`, or
`https://api-beta.notis.ai` when the signed-in user is on beta). Solutions:

1. Run `npx --package @notis_ai/cli@latest -- notis doctor` and confirm `api_base` is a live Notis host
2. Use `--direct` for app deploys when you only need Supabase storage upload: `npx --package @notis_ai/cli@latest -- notis apps deploy --direct`
3. If auth looks stale, run `npx --package @notis_ai/cli@latest -- notis login` and retry

Localhost backends are a Notis-developer test lane only. Do not retarget the CLI at loopback from this skill — that path is owned by `./dev.sh`, which exposes its own lease-backed `dev-*` profile.

### `npx --package @notis_ai/cli@latest -- notis doctor` shows health/tool_roundtrip errors

The CLI health check pings the configured live API. App development commands that are `backend_call: local` (`init`, `build`, `verify`, `link`, `doctor`) work offline. `dev`, `pull`, `create`, `list`, and normal `deploy` need the live API; `deploy --direct` can bypass it when Supabase credentials are available.

### Stale bundle in the portal after deploy

The portal caches app bundles by version. If you re-deploy to the same version, the portal may serve the cached old bundle. Solutions:

1. Hard refresh the portal page (Cmd+Shift+R)
2. Open browser DevTools > Application > Storage > Clear site data
3. The bundle cache key includes version number -- incrementing the version forces a fresh load
