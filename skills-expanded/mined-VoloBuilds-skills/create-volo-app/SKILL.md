---
name: create-volo-app
description: Scaffolds a new Volo full-stack app using create-volo-app and volo-config.json. Use when the user invokes create-volo-app, asks to scaffold a volo app, or wants a new project created with create-volo-app.
---

# Create Volo App

Scaffold a Volo app with [create-volo-app](https://github.com/VoloBuilds/create-volo-app) using a crafted `volo-config.json` and non-interactive CLI invocation.

**CLI details are not duplicated here.** Before crafting config, run:

```bash
npx create-volo-app --help-config
```

Use the schema URL, field notes, and examples from that output. On errors, trust CLI output over this skill.

## Classify intent

**Scaffold-only** — user gives project/setup details only (name, path, services, template). Stop after scaffolding.

**Scaffold + build** — user describes what the app should do (product features, use case, e.g. "collaborative markdown database"). Scaffold first, then hand off to the `auto-build` skill.

## Gather inputs

Extract from the user's message when present:

- `projectName` (required in config) — directory name; default to a kebab-case slug derived from the app description if omitted
- Target path — default: `./<projectName>` in the current workspace; may also be passed as the CLI positional argument
- Template override — only if the user specifies one (`options.template` in config)
- Service preferences — auth, database provider, deploy, create vs existing resources

If the user did **not** specify which services to connect, ask **once**:

> How would you like services set up?
>
> 1. **Basic local setup** — embedded Postgres, Firebase emulator, no deploy
> 2. **Full setup (auto-decide)** — production auth + database + Cloudflare deploy; CLI creates new resources with smart defaults
> 3. **Full setup (manual)** — you choose each service (provider, create vs existing, credentials/IDs)

Map choices to config:


| Choice      | Config                                                                                        |
| ----------- | --------------------------------------------------------------------------------------------- |
| Basic local | Omit `auth`, `database`, and `deploy`                                                         |
| Full auto   | Include `auth`, `database`, `deploy` with `action: "create"` and defaults below               |
| Full manual | Ask per-service questions in chat, then encode answers in config (do not run interactive CLI) |


### Full auto defaults

Use `--help-config` for field semantics. Starting shape:

```json
{
  "auth": { "action": "create", "allowAnonymous": false, "setupGoogleSignIn": true },
  "database": { "provider": "neon", "action": "create", "projectName": "<service-slug>-db" },
  "deploy": { "provider": "cloudflare", "workerName": "<service-slug>-api" }
}
```

Derive `<service-slug>` from the target directory basename (see `--help-config`). Prefer including `database.projectName` for Neon in config mode.

### Full manual

Ask per production service (auth, database, deploy). Mirror `--init-config` wizard questions from the CLI docs. Encode answers in config; do not run the interactive CLI.

For production config mode, confirm auth prerequisites via `--help-config` / CLI errors — config mode does not open browser auth prompts.

## Craft volo-config.json

Write `./volo-config.json` in the workspace cwd. Set `$schema` from `--help-config`. Include only sections needed for the chosen setup mode.

Set `options.overwrite: true` only when the user explicitly wants to replace an existing directory.

**Do not commit this file** — it may hold secrets.

## Run the CLI

```bash
npx create-volo-app <projectName-or-path> --config ./volo-config.json
```

On success, delete `./volo-config.json` from the workspace cwd.

Do **not** start `pnpm run dev` unless the user asks.

## After scaffolding

**Scaffold-only:** summarize what was created, the project path, and next steps (`cd <path>`, `pnpm run dev`). For local-only scaffolds, mention connect scripts from the scaffolded project's `package.json`.

**Scaffold + build:** read and follow the `auto-build` skill (`volo-skills:auto-build`), passing:

- Absolute path to the new project directory
- The user's feature/product description verbatim
- Any constraints they mentioned

## Errors

Use CLI error messages as source of truth. Common cases: directory exists (`options.overwrite`), config validation, missing auth in config mode, missing CLIs or credentials for production services. Escalate to the user when blocked.