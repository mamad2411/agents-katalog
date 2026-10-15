---
name: fcode-cli
description: Use the Factorial Code CLI (fcode) for local development and cloud sync — the pull → add → dependencies:install → run → push flow, when to run each command, --force safety, worked examples, and the workspace config files (process metadata.json with webhook/form/appRole/visibility, team.json, variables.meta.json). Use when running fcode CLI commands, testing a Factorial Code process locally, deploying/syncing Factorial Code (fcode) resources to the cloud, or activating a process's webhook, form, or visibility settings.
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code — CLI

The `fcode` CLI develops and tests processes locally and syncs them with
Factorial Code Cloud. For the platform model see `fcode-core-concepts`.

## Command flow

When making and testing changes:

1. **`fcode pull`** *(optional, first)* — if the cloud may have changed, sync
   down so you work with the latest version.
2. Edit local files (processes, modules, variables, dependencies).
3. **`fcode add`** — **only when you created NEW resources** (new process,
   module, dependency, or variable). Skip for edits to existing code.
4. **`fcode dependencies:install`** — if you changed
   `dependencies/package.json` or `dependencies/requirements.txt`.
5. **`fcode run <process-slug>`** — execute the process locally to test.
6. **`fcode push`** — deploy to cloud when ready.

## Gotchas

- **Never run `fcode run` before `fcode add`** when the process (or other
  resource) was *just created* — you'll hit "Local process not found".
- **`fcode add` is only for NEW resources.** For edits to existing process/module
  code or variables, go straight to `fcode push`.
- **`--force` (on `push`/`pull`) overwrites the other side.** Both commands fail
  when local and cloud diverge; only use `--force` with explicit user
  confirmation.

## Commands

### `fcode add`

Registers **new** local resources with the CLI so they can be run or deployed.
Run after creating a new process/module/dependency/variable, before `run`/`push`.
Not needed after only editing existing resources.

### `fcode dependencies:install`

Installs dependencies into the local workspace. Run after changing
`dependencies/package.json` or `dependencies/requirements.txt`.

### `fcode run <process-slug> --parameters <filepath | json>`

Executes a process locally for development/testing. Uses `variables.env` /
`variables.local.env` and the given parameters (or the process's
`parameters.json` by default). Shows logs, results, and errors.

```sh
fcode run my-process --parameters '{"key": "value"}'
fcode run my-process --parameters ./params.json
fcode run my-process                                  # default parameters.json
```

Prerequisite: run `fcode add` first if the resource was just created.

### `fcode pull`

Downloads the latest processes, modules, variables, and dependencies from the
cloud, overwriting local files to match. Run before starting work if others may
have changed cloud resources, or to discard local changes. `--force` only with
user confirmation.

### `fcode push`

Uploads local changes to the cloud. Run after local changes (run `fcode add`
first only if you created new resources); recommended to `fcode run` first.
`--force` only with user confirmation.

## Process metadata — `metadata.json`

Each process folder holds `processes/<slug>/metadata.json` — the source of
truth for the process's name, description, tags, triggers, and settings. It
round-trips with `push`/`pull`: edit the file and `fcode push` to change these
settings in the cloud, no dashboard needed. Changes show as 🔺 modified in
`fcode status`.

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Display name (defaults to the slug) |
| `description` | string, optional | Process description |
| `tags` | string[] | Tags (defaults to `[]`) |
| `webhook` | object, optional | Webhook trigger: `enabled` (boolean) turns the process's webhook endpoint on; optional `username`/`password` add HTTP basic auth to it |
| `form` | object, optional | Form settings: `enabled` (boolean) is the Forms flag (see `fcode-forms`); optional `appRole` marks the process's role in a marketplace app: `INSTALL`, `SETTINGS`, or `USER_FACING_FORM` |
| `visibility` | object, optional | `isPublic` (boolean) — makes the process form publicly accessible (no Factorial login) |

```json
{
  "name": "Order sync",
  "description": "Syncs Shopify orders into Factorial",
  "tags": ["integration", "shopify"],
  "webhook": {
    "enabled": true,
    "username": "$WEBHOOK_USER",
    "password": "$WEBHOOK_PASSWORD"
  },
  "form": { "enabled": false }
}
```

```json
{
  "name": "Connect your account",
  "tags": ["setup"],
  "form": { "enabled": true, "appRole": "INSTALL" }
}
```

Notes:

- **Webhook basic-auth credentials: use `$VARIABLE` placeholders** (resolved
  from team variables), never literal secrets — placeholders round-trip on
  `pull`, literals would live in the repo.
- Omit `form.appRole` unless the process belongs to a marketplace app; the
  cloud default `NONE` is omitted on `pull`.
- If `metadata.json` is missing, `fcode add` scaffolds
  `{ "name": "<slug>", "tags": [] }`; invalid JSON falls back to those
  defaults with a warning.

## Team settings — `team.json`

A singleton file at the workspace root holding team-level settings. Synced by
`fcode team:pull` / `team:push` / `team:status`, and included in plain
`fcode push` / `pull` (pushed last, so a referenced error-handler process
exists first).

| Field | Type | Meaning |
|---|---|---|
| `parentTeamSlugs` | string[] | Teams this workspace inherits resources from |
| `zoneId` | string, optional | Team timezone (e.g. for schedules) |
| `errorHandlerConfig` | object, optional | `{ "processSlug": "<slug>", "tag": null }` — process invoked when an execution errors |

```json
{
  "parentTeamSlugs": ["base-app"],
  "zoneId": "Europe/Madrid",
  "errorHandlerConfig": { "processSlug": "error-handler", "tag": null }
}
```

The error handler is referenced by **slug** (not id) so `team.json` is
portable across teams; the CLI resolves it to the cloud id on push.

## Variable sensitivity — `variables.meta.json`

A workspace-root file mapping each variable to its sensitivity flag:

```json
{
  "ACME_API_KEY": { "isSensitive": true },
  "ACME_BASE_URL": { "isSensitive": false }
}
```

- Create a sensitive variable with `fcode variables:add --sensitive` (then set
  its value and push); the flag lands here.
- **Sensitive values never leave the cloud**: `pull` writes the placeholder
  `********` into `variables.env`. Don't replace the placeholder there — put
  the real value in `variables.local.env` for local runs.
- **`isSensitive` is immutable** once pushed. Editing it in
  `variables.meta.json` is rejected on push (🚫 in `fcode status`) — revert to
  match remote.

### Getting secret values for local runs

When a local run (`fcode run`, a discovery script) needs a real secret value
that isn't in `variables.local.env` yet, ask the user to provide it. If they
prefer not to share the value with the agent, ask them to add the
`KEY=value` line to `variables.local.env` themselves — local runs pick it up
without the value ever appearing in the conversation.

- **`variables.local.env` values are never pushed.** Remind the user to also
  create those secret variables manually in the remote demo environment —
  `fcode push` won't carry the values.
- **`FACTORIAL_TOKEN`**: needed **locally only** — the remote environment
  populates it automatically, so don't create it there. To obtain it, the user
  completes the OAuth flow in the Factorial Code app details page, then copies
  the generated token with the copy dropdown option in the OAuth Dev app, and
  puts it in `variables.local.env` (or shares it, per their preference).
- Once obtained, never echo secret values back in output or logs.

## Examples

**Development cycle (new process):**

```sh
fcode add
fcode dependencies:install            # if dependencies changed
fcode run shopify-order-sync --parameters '{"dateFrom":"2024-01-01","dateTo":"2024-01-31"}'
fcode push                            # no need to re-run `add` if nothing new was created
```

**Deploy an existing, tested process:**

```sh
fcode push                            # `add` not needed — process already registered
```
