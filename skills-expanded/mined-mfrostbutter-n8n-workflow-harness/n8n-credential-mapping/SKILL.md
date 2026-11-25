---
name: n8n-credential-mapping
description: >-
  Map every n8n credential to the secret that feeds it, per environment: the
  committed secret map, creating credentials on an instance from Infisical or
  another secret manager without a value ever reaching the terminal, the id
  ledger, rotation, verifying the mapping, and when n8n external secrets is
  the better home. Use when a build needs a credential that does not exist on
  the target yet, when asked where a credential's value comes from or which
  secret feeds it, before a promotion when the target's credentials have to be
  created, when a key rotates or was exposed, when an instance holds
  credentials nobody can trace to a source, and whenever the user says
  Infisical, vault, secret, credential mapping, rotate, or "set up the
  credentials on staging".
---

# Credential mapping: n8n credentials and the secrets behind them

A credential on an instance is a copy of a value that lives somewhere else.
This skill owns the "somewhere else": which named secret feeds which n8n
credential in which environment, how the copy gets made without the value
touching a terminal, a chat, or this repository, and how it gets replaced.
The map is committed. Values never are. Ids are per instance and gitignored.

Scope boundaries:

| Task | Where |
|---|---|
| Which external secrets providers n8n supports, the `$secrets` syntax, its limits, the refresh interval | `n8n-enterprise-delivery` |
| Which project owns a credential, moving one with a workflow | `n8n-project-organization` |
| Listing credentials and schemas from a session (`n8n_manage_credentials`, `list_credentials`) | `n8n-mcp-tools-expert` |
| What never enters the repo, exposure response | `docs/08-SECURITY.md` |

## The rule

Every credential a workflow in this repo binds traces to a named secret in the
secret manager, through `deploy/secret-map.<env>.json`. A credential made by
hand in the UI with a value pasted from somewhere is unmapped; `verify` lists
it, and the fix is to put it in the map and let `sync` recreate it, not to
leave a value whose origin nobody can name.

Three homes a value can have, in order of preference on a licensed instance:

| Home | Rotation | Use when |
|---|---|---|
| **External secrets** (`{{ $secrets.<vault>.<NAME> }}` in a credential field) | In the vault only; n8n picks it up within the refresh interval | The instance is licensed, the vault is one of the supported providers, the value is a single line. The enterprise answer. |
| **n8n credential store**, created from the map by `secret-map.sh sync` | Replacement credential, rebind, retire the old one | Community and Cloud instances, dev instances, OAuth types, values the provider cannot serve as one line |
| `$env`, a Set node, a text field | n/a | Never. `lint-workflow` flags `$env` and `process.env`. |

## The map

`deploy/secret-map.<env>.json`, one per environment, committed. Names and
references only:

```json
{
  "_secrets": {"provider": "infisical", "env": "dev", "path": "/acme"},
  "Acme API (dev)": {
    "type": "httpHeaderAuth",
    "project": "Acme Corp",
    "data": {"name": "Authorization", "value": "secret:ACME_API_TOKEN"}
  },
  "Postgres (acme, dev)": {
    "type": "postgres",
    "project": "Acme Corp",
    "data": {"host": "env:PG_HOST", "port": 5432, "database": "acme",
             "user": "acme", "password": "secret:PG_ACME_PASSWORD", "ssl": "disable"}
  }
}
```

- **Key**: the credential's name on the instance, exactly. The workflow JSON
  binds by this name, so it is the join key across the map, the id ledger and
  the workflow. Put the environment in the name when one instance serves
  several, and nothing else that would differ per instance.
- **`type`**: the n8n credential type id (`httpHeaderAuth`, `postgres`,
  `openAiApi`). `GET /credentials/schema/<type>` on the target is the truth
  for the `data` keys; `check` compares against it.
- **`project`**: the team project that owns it, the same one the workflows
  that bind it live in (`n8n-project-organization`). `personal` is for probes.
- **`data`**: the credential fields. `secret:NAME` is read from the secret
  manager at `_secrets.env` and `_secrets.path` (or from the environment when
  the process already runs under `infisical run`); `env:VAR` only from the
  environment; anything else is a literal. Hosts and ports are literals or
  `env:` references, never baked into a secret.
- **`_secrets`**: `provider` is `infisical` (default), `cmd` (a template in
  `N8N_SECRET_CMD` with `{name}`, for Vault or another CLI), or `env`.
  `N8N_INFISICAL_CLI` names the Infisical CLI when it is not `infisical` on
  PATH (a `.js`/`.cjs`/`.mjs` path runs under Node).

Naming that holds up: secrets `UPPER_SNAKE`, under a path per repo or team,
with the environment as the secret manager's environment rather than in the
name. n8n credential names in words, the service first, the scope in
parentheses: `Acme API (dev)`, `Postgres (acme, dev)`, `OpenRouter (Acme Corp)`.

## The tool

`scripts/secret-map.mjs` (`./scripts/secret-map.sh`), Node built-ins only.
Every line it prints is scrubbed against the values it resolved, and it never
puts a value on a command line.

| Command | Does |
|---|---|
| `./scripts/secret-map.sh check [env]` | The map is well-formed, every `secret:` name exists at the path (names only, through the listing), every `env:` is set, every type has a schema on the target and the `data` keys are in it. `RESULT: ok` or findings, exit 1. |
| `./scripts/secret-map.sh sync [env] [--dry-run] [--only <name>...]` | Create the credentials the map names that are missing on the target, in their project, from resolved values; record ids in `deploy/creds.<env>.json`. An existing credential of the same name and project is recorded, not recreated. Dry run prints the plan and the reference each field resolves from. |
| `./scripts/secret-map.sh rotate <name>... [--env <env>]` | The public API cannot update a credential's values, so this creates a replacement with fresh values, moves the ledger id to it, and lists the workflows still bound to the previous one. Rebind those to the new id, run one, then retire the previous credential by hand. |
| `./scripts/secret-map.sh verify [env]` | Every mapped credential exists on the target with its type and project; the id ledger agrees; credentials in use by this repo's workflows that the map does not name. `RESULT: ok` or findings. Run before a hand-over. |
| `./scripts/secret-map.sh ids [env]` | Refresh `deploy/creds.<env>.json` from the target by name. The retrofit for an instance whose credentials exist but were never mapped. |

Run the writing commands under the secret manager so the values arrive as
environment variables and nothing is fetched by a subprocess:

```bash
infisical run --env dev --path /acme -- ./scripts/secret-map.sh sync dev
```

`deploy/workflows.<env>.json`, when present, maps this repo's workflow names
to their ids on that instance; `verify` then counts only those workflows as
"in use", which keeps a shared dev instance from reporting every other team's
credentials. A named environment other than dev needs its own
`N8N_API_URL_<ENV>` and `N8N_API_KEY_<ENV>` pair; the tool never falls back
to the bare pair on a write.

## The working order

1. **Map before build.** When the design names a service, add its credential
   to `deploy/secret-map.dev.json` and the secret to the secret manager under
   the repo's path. `check dev` until `RESULT: ok`.
2. **`sync dev`**, then build. The workflow JSON binds the credential by name
   and the id from `deploy/creds.dev.json`; a credential block with a guessed
   id breaks the node's credential picker, so take the id from the ledger or
   omit the block.
3. **Before a promotion**, `./scripts/lint-workflow.sh` prints the credentials
   and variables the target needs. Every name on that list is in
   `deploy/secret-map.<target>.json`, with the target's own secrets (a prod
   key is a different secret, not the dev one under a new name). `check
   <target>`, `sync <target>` run by whoever holds the target's key, then the
   promotion.
4. **`verify <env>`** before a hand-over and at the start of a session on a
   shared instance. An unmapped credential in use is a finding to resolve,
   not to note.

OAuth2 types (`gmailOAuth2`, `googleDriveOAuth2Api`, `slackOAuth2Api`) take
the client id and secret from the map, and the consent step is a browser
action in the instance UI that no tool performs. `sync` creates the record;
note `"consent": "ui"` in the map entry so the hand-over checklist names the
person who clicks it. `verify` checks existence, not that consent happened; a
probe execution does.

## Rotation and exposure

- **Scheduled rotation, credential store:** new value in the secret manager,
  `rotate <name>`, rebind the workflows it lists, run one, retire the previous
  credential. The previous one stays until a human removes it; the tool lists
  it and does not delete.
- **Scheduled rotation, external secrets:** rotate in the vault. Nothing on
  the n8n side. Mind the refresh window.
- **Exposure** (a value in chat, a log, a commit): say so, treat it as
  compromised, rotate the same day, then the `rotate` path above. History
  purge without rotation is theater.

## Reading back

The API never returns a value. What it gives:

- `GET /credentials` (owner or admin key): id, name, type, `shared[]` with the
  owning project. The only place ownership is visible.
- `GET /credentials/schema/<type>`: the fields a type accepts. Required lists
  are often empty even when the node needs the field; the probe execution is
  the real check.
- `GET /workflows` with nodes: which credential id each node binds. `verify`
  joins this against the map to find the unmapped ones.
- No endpoint reads or edits a value, and no endpoint renames a credential.
  A credential that must change name or value is a new credential.

So "is the credential right" is answered by: it exists with the expected type
in the expected project, the ledger id matches, and one execution of a
workflow that uses it succeeds. Not by looking at the value.

## Field notes

- A map with `secret:` names that `check` cannot list usually means the wrong
  secret-manager project: the Infisical CLI reads `.infisical.json` in the
  current directory for the project id. Run from the directory that holds the
  right one, or set `_secrets.projectId`.
- An instance key that answers 401 to everything is a key for a different
  instance, not a permissions problem. Keys are per instance; name the
  instance in the secret name.
- Two credentials with one name in one project make `sync` and `ids` stop
  and print both ids. Pick in the ledger by hand, then retire the other.
- `sync` on an instance where the credential already exists with a different
  type is a stop, not an overwrite. Rename one side.
