---
name: climate-generator
description: >
  Generate Go CLIs from OpenAPI 3.x specs with climate, inspect generated CLIs,
  and emit Markdown skill prompts so those CLIs can be attached to agent workflows.
license: Apache-2.0
compatibility: Requires Go 1.21+ and climate CLI (brew install disk0Dancer/tap/climate)
metadata:
  author: disk0Dancer
  version: "1.0"
---

# Skill: climate-generator

You have access to `climate`, a CLI that generates production-ready Go command-line
clients from OpenAPI specifications and can emit Markdown prompts for agent skills.

## When to use this skill

- The user has an OpenAPI 3.x URL or file and wants a CLI quickly.
- The user wants a human-usable API client rather than writing SDK glue code.
- The user wants to turn a generated CLI into a reusable agent skill.
- The user wants to compose multiple microservice specs into one facade CLI.
- The user wants a local OpenAPI simulator (mock server) for testing.
- The user wants the generated CLI to receive or emit webhook callbacks itself.
- The user wants shell completion for climate itself.
- The user wants to list, remove, or upgrade a previously generated CLI.
- The user wants to uninstall climate itself and clean up local climate-managed artifacts.

## Core workflow

1. Generate a CLI from the provided spec.
2. If user provides multiple specs, use `climate compose` instead of `climate generate`.
3. Capture the resulting `cli_name`, `binary_path`, and `source_dir`.
4. If the user wants agent integration, run `climate skill generate <cli-name>`.
5. If the user needs sandbox/simulator behavior, run `climate mock <openapi_spec>`.
6. If the user wants shell completion for climate itself, run `climate completion install --shell <shell>`.
7. If the user wants the CLI managed on GitHub, run `climate publish <cli-name>`.
8. Follow the generated instructions from that Markdown prompt.

## Commands

### Generate a CLI

```bash
climate generate [--name <cli-name>] [--out-dir <dir>] [--no-build] [--force] <openapi_spec>
```

- `<openapi_spec>` can be a local path or an HTTP(S) URL.
- `--no-build` generates source only.
- `--force` overwrites an existing output directory.

Success output is JSON:

```json
{
  "cli_name": "<name>",
  "binary_path": "<absolute path to compiled binary>",
  "source_dir": "<absolute path to generated source>",
  "version": "<API version>",
  "openapi_hash": "<sha256 of the spec>"
}
```

Generated CLIs also include config plus spec-aware event commands:

```bash
<cli-name> events list
<cli-name> config list
<cli-name> config set <key> <value>
<cli-name> config get <key>
<cli-name> config unset <key>
<cli-name> config profiles list
<cli-name> config profiles create <name>
<cli-name> config profiles use <name>
<cli-name> config set --secret events.signing_secret <value>
<cli-name> auth login [--scheme <name>]
<cli-name> auth status
<cli-name> auth logout [--scheme <name>]
<cli-name> events listen [event-name] [--host 127.0.0.1] [--port 8081] [--path /] [--tunnel none|auto|cloudflared] [--signature-mode none|hmac]
<cli-name> events emit <event-name> --target-url <url> [--data-json <json>] [--data-file <path>] [--signature-mode none|hmac]
```

Secrets from `config set --secret` and `auth login` are encrypted at rest
(gopass when its store is initialized, otherwise an age-encrypted local file).
Override with `<CLINAME>_SECRETS_BACKEND=gopass|file|plaintext`; move existing
secrets with the hidden `<cli-name> config secrets migrate --to <backend>`.

### List generated CLIs

```bash
climate list
```

### Compose multiple OpenAPI specs into one CLI

```bash
climate compose [--name <cli-name>] [--out-dir <dir>] [--no-build] [--force] [--title <title>] [--api-version <version>] [--description <text>] <spec1>:<prefix1> [<spec2>:<prefix2> ...]
```

Each positional argument is `<spec>:<prefix>` where `<spec>` can be a local
path or URL and `<prefix>` starts with `/`.

### Start local mock server

```bash
climate mock [--port <port>] [--latency <ms>] [--emit-url <url> --event-path <path> [--event-method <method>]] <openapi_spec>
```

### Generate or install shell completions

```bash
climate completion bash|zsh|fish|powershell
climate completion install [--shell bash|zsh|fish|powershell]
climate completion uninstall [--shell bash|zsh|fish|powershell]
```

### Remove a generated CLI

```bash
climate remove [--purge-sources] [--yes] <cli-name>
```

### Upgrade a generated CLI

```bash
climate upgrade [--openapi <spec>] <cli-name>
```

### Uninstall climate itself

```bash
climate uninstall [--full] [--yes]
```

### Generate a skill prompt for a CLI

```bash
climate skill generate [--mode=full|compact] [--out <file>] <cli-name>
```

### Publish a generated CLI to GitHub

```bash
climate publish [--owner <owner>] [--repo <repo>] [--visibility public|private] [--github-token <token>] <cli-name>
```

This command creates or reuses a GitHub repository through the GitHub API,
writes lifecycle files including CI, CI auto-fix, and release workflows,
initializes git, and pushes the generated source tree.

### Print the built-in climate skill

```bash
climate skill generator
```

## Typical examples

Generate a CLI:

```bash
climate generate --name petstore https://petstore3.swagger.io/api/v3/openapi.json
```

Compose two service specs into one facade CLI:

```bash
climate compose orders.yaml:/api/orders users.yaml:/api/users --name gateway
```

Run a local mock server:

```bash
climate mock --port 9090 --latency 150 https://petstore3.swagger.io/api/v3/openapi.json
```

Generate a compact skill prompt for that CLI:

```bash
climate skill generate petstore --mode=compact
```

Publish it to GitHub:

```bash
climate publish petstore --owner disk0Dancer
```

## Notes

- Most climate management output is JSON on success.
- `climate skill generate`, `climate skill generator`, and `climate completion <shell>` print text to stdout.
- `climate mock` in server mode and `climate mock --emit-url ...` intentionally print plain-text runtime output.
- Errors are emitted as structured JSON on stderr.
- Generated CLIs follow the shape `<cli-name> <tag> <operation> [flags] --output=json|table|raw`.
- Homebrew install is available via `brew tap disk0Dancer/tap && brew install climate`.
- GitHub publish auth is read from `--github-token`, `GITHUB_TOKEN`, or `GH_TOKEN`.
- `climate remove` and `climate uninstall` prompt unless `--yes` is passed.
