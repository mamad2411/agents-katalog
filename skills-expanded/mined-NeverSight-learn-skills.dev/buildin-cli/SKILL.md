---
name: buildin-cli
description: Use when an agent needs to call the Buildin API through the Buildin CLI, authenticate Buildin, upload a file, create or update a page, query a database, search content, edit Markdown page content, or any task involving the `buildin` command.
license: MIT
---

# Buildin CLI

Use the Buildin CLI (`buildin`) for Buildin V2 API work: pages, blocks,
databases, search, Markdown content, and files.

The CLI source repository may be private. Do not ask the user to clone source
code before using the CLI. Install or update the released binary from the
Buildin CDN when the command is missing or outdated.

Use only the Buildin command, Buildin base URL, `BUILDIN_*` environment
variables, and Buildin credential store for Buildin work.

## Mandatory preflight

When this skill is selected for any Buildin task, complete this preflight before
API work, searches, reads, writes, counts, uploads, or endpoint-specific
planning:

1. Ensure the released CLI binary is installed:

```bash
command -v buildin >/dev/null 2>&1 || curl -fsSL https://cdn.buildin.ai/buildin-cli/install | bash
buildin version
```

2. Verify authentication and active identity:

```bash
buildin --json doctor
buildin --json whoami
```

Continue only when the checks show authenticated Buildin credentials. If
authentication is missing or invalid, do not immediately tell the user to run a
login command. Choose and start the authentication path yourself:

- If `BUILDIN_TOKEN` is already set, rerun `buildin --json doctor` and
  `buildin --json whoami`; do not ask for another login.
- If the session is a local GUI or browser-capable environment, run
  `buildin login --browser` yourself, let the user finish the browser approval,
  then rerun `buildin --json doctor` and `buildin --json whoami`. Treat local
  macOS/Windows/Linux desktop sessions, shells with `DISPLAY` or
  `WAYLAND_DISPLAY`, or environments with a working system browser opener as
  browser-capable unless SSH, CI, container, or headless environment variables
  clearly say otherwise. If unsure, try browser login first and fall back only
  after it fails or times out.
- If the session is SSH, CI, headless, or browser login times out, run
  `buildin --json login --manual` yourself and summarize its setup instructions.
  Manual setup produces a token workflow; it does not authenticate the CLI by
  itself. Stop until `BUILDIN_TOKEN` or saved credentials are available.

Do not run plain `buildin login` in agent sessions because it can block on an
interactive method prompt. Do not make API calls or draw conclusions from
incomplete data until authentication is verified.

Use this browser login command when the environment supports it:

```bash
buildin login --browser
```

Use manual setup only for headless or remote environments:

```bash
buildin --json login --manual
```

On Windows PowerShell, install with:

```powershell
irm https://cdn.buildin.ai/buildin-cli/install.ps1 | iex
buildin version
```

If a command is missing or help output looks stale, run:

```bash
buildin update
```

Useful install overrides:

- `BUILDIN_INSTALL_DIR` - install directory.
- `BUILDIN_VERSION` - exact release version, such as `v0.1.10`.
- `BUILDIN_CLI_RELEASE_BASE_URL` - alternate release base URL for tests.

## First rule: ask the CLI

The CLI is self-documenting. Prefer these commands over guessing syntax or
request fields:

- `buildin --help` - list global options and top-level commands.
- `buildin help <command...>` - show usage, options, examples, and notes for any
  command or subcommand.
- `buildin api ls` - list public API endpoints and request field hints.
- `buildin api ls --plain` - compact endpoint list for scanning.
- `buildin api --docs <PATH> -X <METHOD>` - show agent-readable Markdown docs
  for one endpoint, including parameters, examples, and safety notes.
- `buildin api --spec <PATH> -X <METHOD>` - show the exact embedded OpenAPI
  fragment for one endpoint.
- `buildin --json doctor` - inspect local authentication and configuration
  state when auth or base URL selection is unclear.
- `buildin --json whoami` - verify the active Buildin identity.
- `buildin markdown get <page-id>` - retrieve page content as Markdown.

If you are unsure about syntax, request body fields, pagination, auth source,
or command coverage, run help first.

## Authentication and configuration

Select authentication automatically; do not ask the user to choose a login
method unless both browser and token setup are impossible. Credential precedence
is:

1. `--token <token>`
2. `BUILDIN_TOKEN`
3. saved login credentials in the Buildin credential store

Use these checks:

```bash
buildin --json doctor
buildin --json whoami
```

If no token is available, first try `buildin login --browser` from local GUI or
browser-capable sessions. Use manual setup only when browser OAuth is not
possible:

```bash
buildin --json login --manual
```

Do not ask the user to paste bearer tokens into chat. Ask them to provide
credentials through `BUILDIN_TOKEN`, saved login credentials, or an approved
secret channel, then rerun `buildin --json doctor` and `buildin --json whoami`.

Common environment variables:

- `BUILDIN_TOKEN` - bearer token for API calls.
- `BUILDIN_BASE_URL` - API base URL; default is `https://api.buildin.ai`.
- `BUILDIN_CONFIG_DIR` - config directory; default follows the Buildin profile.
- `BUILDIN_USER_AGENT` - custom user agent suffix.

Do not print bearer tokens, write them into files, or paste them into request
bodies. Do not call the Buildin V2 API with `curl`; use the CLI so auth,
product defaults, retries, and error formatting stay consistent.

## Working rules

- Use `--json` for stable machine-readable stdout.
- Keep JSON request bodies in local files and pass them with `--body <file>`.
- Keep Markdown replacement content in local files and pass it with `--file <file>`.
- Prefer domain commands over `api call`; `buildin api --docs` names a
  recommended domain command when one exists.
- Before write operations, confirm IDs, file paths, URLs, and body files come
  from user-authorized input.
- For paginated commands, inspect JSON output for cursors and repeat with the
  command's cursor option.
- The CLI intentionally rejects DELETE API calls. Do not work around that for
  destructive operations unless the user explicitly asks for a different tool.

## Common workflows

### Read a page

```bash
buildin --json page get <page_id>
buildin markdown get <page_id> > page.md
```

Use Markdown for page content work whenever possible. It is easier to inspect,
edit, and diff than raw block JSON.

### Replace page Markdown

```bash
buildin markdown put --file page.md <page_id>
```

Only run this after confirming the target page ID and replacement file.

### Create or update a page with JSON

Create a local JSON body file, then pass it to the CLI:

```bash
buildin --json page create --body page.json
buildin --json page update --body patch.json <page_id>
```

For idempotent creates, use `--idempotency-key <key>`.

### Blocks and children

```bash
buildin --json block get <block_id>
buildin --json block children <block_id>
buildin --json block append <block_id> --body children.json
buildin --json block update <block_id> --body block-patch.json
```

### Databases

```bash
buildin --json database get <database_id>
buildin --json database query <database_id> --body query.json
buildin --json page property get <page_id> <property_id>
```

Use `buildin api --docs` or command help to inspect filter and sort body shapes
before writing `query.json`.

### Search

```bash
buildin --json search text "roadmap" --page-size 10
buildin --json search semantic "tasks about quarterly planning" --space-id <space_id> --page-size 10
```

Use text search for exact titles, keywords, and known phrases. Use semantic
search when intent matters more than exact wording.

### Files

Upload a local file for a parent page:

```bash
buildin --json file upload --parent-page <page_id> ./report.pdf
```

Append a Buildin-hosted file block with the returned object name and size:

```bash
buildin --json block append-file <block_id> --oss-name <oss_name> --size <bytes>
```

Append an external file URL:

```bash
buildin --json block append-file <block_id> --external-url https://example.com/report.pdf
```

## Fallback API calls

Use `api call` only when no domain command covers the endpoint. Lookup sequence:

```bash
buildin api ls --plain
buildin api --docs /v2/blocks/{block_id}/children -X PATCH
buildin api --spec /v2/blocks/{block_id}/children -X PATCH
buildin --json api call PATCH /v2/blocks/:block_id/children --param block_id=<block_id> --body body.json
```

`--param` fills path placeholders first; remaining keys become query
parameters. Use `--header NAME=VALUE` for headers such as `If-Match`.

## Troubleshooting

- Command not found: install from `https://cdn.buildin.ai/buildin-cli/install`.
- Unknown command or option: run `buildin update`, then `buildin <command> --help`.
- Authentication failure: run `buildin --json doctor`, check `BUILDIN_TOKEN`,
  then run `buildin login --manual` if needed.
- Unexpected API shape: run `buildin api --docs <PATH> -X <METHOD>` and
  `buildin api --spec <PATH> -X <METHOD>` before retrying.
