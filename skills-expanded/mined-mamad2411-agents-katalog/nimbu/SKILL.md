---
name: nimbu
description: >
  Nimbu CMS CLI — manage channels, pages, products, orders, customers, themes,
  translations, menus, blogs, notifications, redirects, uploads, webhooks,
  cloud code, and local dev server for Nimbu sites. Use when building,
  querying, migrating, or deploying Nimbu CMS content and themes.
---

# Nimbu CLI

The `nimbu` binary is a Go CLI for the [Nimbu](https://nimbu.io) CMS API.

## Documentation

- **Full docs**: https://docs.nimbu.io/
- **Liquid & themes**: https://docs.nimbu.io/themes/introduction/overview.html
- **Cloud code**: https://docs.nimbu.io/cloud-code/overview.html

Refer to these for Liquid template syntax, theme structure, and cloud code APIs. This skill covers the CLI tool; the docs cover the platform concepts.

## Prerequisites

Install via Homebrew (`brew install nimbu/tap/nimbu`), Go (`go install github.com/nimbu/cli/cmd/nimbu-cli@latest`), or download from [GitHub Releases](https://github.com/nimbu/cli/releases).

Authenticate before use:

```bash
nimbu auth login          # Interactive browser OAuth — stores token in OS keychain
nimbu auth status         # Verify current credentials
nimbu auth scopes         # List granted scopes
```

Or set `NIMBU_TOKEN` env var to skip the keychain.

## Site Resolution

Commands that require a site resolve it in this order:

1. `--site` flag
2. `NIMBU_SITE` env var
3. `default_site` in `~/.config/nimbu/config.json`
4. `site` field in `nimbu.yml` (project directory)

If none is found, the command fails with a clear error.

## Output Modes

| Flag | Format | Use case |
|------|--------|----------|
| *(default)* | Human-readable table | Interactive use |
| `--json` | JSON | **Always use for agents** — structured, parseable |
| `--plain` | TSV | Piping to `cut`, `awk`, etc. |

Env overrides: `NIMBU_JSON=1`, `NIMBU_PLAIN=1`.

**Agent rule: always pass `--json` to get structured output.**

## Global Flags

| Flag | Purpose |
|------|---------|
| `--site <id>` | Site ID or subdomain |
| `--locale <code>` | Filter by locale |
| `--fields <list>` | Comma-separated fields to return |
| `--sort <field>` | Sort, e.g. `created_at:desc` |
| `--filters key=val` | Filter criteria (repeatable) |
| `--include <rels>` | Include related resources |
| `--force` | Skip confirmations for destructive ops |
| `--readonly` | Disable all write operations |
| `--no-input` | Never prompt; fail instead (CI mode) |
| `--no-progress` | Disable live progress UI |
| `--verbose` | Verbose logging |
| `--debug` | HTTP request/response traces |

## Safety

Use these to constrain agent access:

- `NIMBU_READONLY=1` — blocks all create/update/delete/copy/push operations
- `NIMBU_ENABLE_COMMANDS=channels,pages` — allowlist of permitted command groups
- `NIMBU_NO_INPUT=1` — never prompt; fail instead (CI/agent mode)
- `--dry-run` — available on copy and sync commands; shows what would happen without writing
- `--force` — required for delete commands; without it, deletes fail

## Inline Payload Syntax

Most `create` and `update` commands accept inline assignments:

| Syntax | Meaning |
|--------|---------|
| `key=value` | String value |
| `key:=json` | Typed JSON (number, bool, object, array, null) |
| `key=@file.txt` | Raw file content as string |
| `key:=@file.json` | Parse JSON from file |

Dot paths for nesting: `seo.title="My Page"`.

`--file` and inline assignments are **mutually exclusive**.

```bash
# Inline
nimbu products update sku-123 name="Wine Box" price:=29.9 seo.title="Gift box"

# File payload
nimbu pages update about --file payload.json
```

## Command Map

### Content

| Command | Subcommands | Notes |
|---------|-------------|-------|
| `channels` | list, get, info, diff, copy, fields | Schema introspection via `info` |
| `channels entries` | list, get, create, update, delete, count, copy | Entry CRUD within a channel |
| `pages` | list, get, create, update, delete, count, copy | Fullpath as identifier |
| `menus` | list, get, create, update, delete, count, copy | Nested tree structure |
| `blogs` | list, get, create, update, delete, count, copy | Has `posts` subcommand |
| `blogs posts` | list, get, create, update, delete, count | Blog post CRUD |
| `translations` | list, get, create, update, delete, count, copy | Locale shorthand support |
| `notifications` | list, get, create, update, delete, count, copy, pull, push | Template sync |
| `mails` | pull, push | Alias for `notifications` sync commands |

### Commerce

| Command | Subcommands | Notes |
|---------|-------------|-------|
| `products` | list, get, create, update, delete, count, copy | Product catalog |
| `collections` | list, get, create, update, delete, count, copy | Product collections |
| `coupons` | list, get, create, update, delete, count, copy | Discount coupons |
| `orders` | list, get, update, count | **No create/delete** — orders are read-only except status |
| `customers` | list, get, create, update, delete, count, copy | Customer records |

### Infrastructure

| Command | Subcommands | Notes |
|---------|-------------|-------|
| `themes` | list, get, cdn-root, pull, push, sync, diff, copy | Theme development |
| `themes layouts` | list, get, create, delete | Layout CRUD |
| `themes templates` | list, get, create, delete | Template CRUD |
| `themes snippets` | list, get, create, delete | Snippet CRUD |
| `themes assets` | list, get, create, delete | Asset CRUD |
| `themes files` | list, get, create, delete | Generic file CRUD |
| `apps` | list, get, config, push | Cloud code management |
| `uploads` | list, get, create, delete, count | File uploads |
| `webhooks` | list, get, create, update, delete, count | Webhook management |
| `redirects` | list, get, create, update, delete, copy | URL redirects |
| `roles` | list, get, create, update, delete, count, copy | Permission roles |
| `accounts` | list, count | Account listing |

### Operations

| Command | Subcommands | Notes |
|---------|-------------|-------|
| `sites` | list, get, current, count, settings, copy | Site management + full-site copy |
| `auth` | login, logout, status, scopes, token, keyring | Credential management |
| `server` | *(run directly)* | Local simulator proxy + child dev server |
| `init` | *(run directly)* | Bootstrap theme project with TUI |
| `config` | list, get, set, unset, banner, path | CLI configuration |
| `functions` | run | Execute cloud functions |
| `jobs` | run | Execute cloud jobs |
| `api` | get, post, put, patch, delete | Raw API access |
| `completion` | bash, zsh, fish | Shell completions |

## Schema Discovery for Theme Development

When working on Nimbu themes or templates, use these commands to understand channel data structures:

```bash
# List all custom fields with types, flags, references, and select options
nimbu channels fields blog --json

# Get full channel schema including ACL, ordering, and dependency graph
nimbu channels get blog --json

# Generate a TypeScript interface from channel schema (works cross-site)
nimbu channels info blog --typescript
nimbu channels info staging/blog --typescript
```

**`channels fields --json`** returns an array of field definitions:
- `name` — field key used in templates and entry data
- `type` — field type (e.g., `string`, `text`, `file`, `date`, `belongs_to`, `select`, `boolean`, `integer`, `float`, `geo`)
- `label` — human-readable label
- `required`, `unique`, `localized`, `encrypted` — field flags
- `reference` — target channel slug for relationship fields (`belongs_to`, `has_many`)
- `select_options` — available options for `select` type fields
- `hint` — field description/help text

**Agent tip**: Always run `nimbu channels fields <channel> --json` before working with channel data in templates. This gives you the exact field names and types to use.

## Rich Resource Contracts

Three resource types have special contracts beyond standard CRUD:

### Pages

- **Identifier**: fullpath (e.g., `about/team`), not UUID
- `pages get <fullpath> --json` returns full page document with nested `items`
- `pages get --download-assets DIR --json` downloads file editables, rewrites to `attachment_path`
- `pages update <fullpath> --file page.json` uses replace-safe patch semantics
- `pages update` inline: only `title`, `template`, `published`, `locale` — deep edits need `--file`

### Menus

- **Identifier**: slug/handle
- `menus get <slug> --json` returns full nested tree
- `menus update` uses replace-safe patch for nested updates
- `menus update` inline: only `name`, `handle` — deep edits need `--file`

### Channels

- `channels get <slug> --json` returns schema, customizations, ACL fields
- `channels info <slug>` outputs TypeScript-friendly schema definition
- `channels diff --from <site> --to <site>` compares channel configs

## Gotchas

1. **Parent field on pages**: Set `parent` to the **fullpath string** (e.g., `"archive"`), NOT an object ID. The API resolves parents by path. `parent_path` is ignored on write.

2. **Inline update limits**: `pages update` and `menus update` inline assignments only accept shallow fields. For nested/deep edits, use `--file` with a full JSON payload.

3. **`--file` vs inline**: Mutually exclusive. The CLI errors if both are provided.

4. **Delete requires `--force`**: All delete commands fail without `--force`.

5. **Orders are read-only**: No `create` or `delete` — only `list`, `get`, `update` (status), `count`.

6. **Translations locale shorthand**: Bare locale keys like `nl=text` are rewritten to `values.nl=text`. Reserved keys (`key`, `value`, `values`, `locale`, `url`) are not rewritten.

7. **Theme sync excludes `code/` and `content/`**: These directories are intentionally not managed by `themes push/sync`.

8. **Copy commands use `--from`/`--to` refs**: Format is `site` for site-level ops, `site/channel` for channel-level ops.

## Common Workflows

### List and filter channel entries

```bash
nimbu channels entries list blog --site my-site --json --sort created_at:desc
```

See [references/channels-and-entries.md](references/channels-and-entries.md) for copy, diff, and schema workflows.

### Update a page with nested content

```bash
# Export, edit locally, re-upload
nimbu pages get about/team --download-assets tmp/assets --json > page.json
# ... edit page.json ...
nimbu pages update about/team --file page.json
```

See [references/pages-menus-content.md](references/pages-menus-content.md) for pages, menus, blogs, translations, and notification sync.

### Push theme changes after build

```bash
nimbu themes push --build --all
```

See [references/themes-and-local-dev.md](references/themes-and-local-dev.md) for push/pull/sync/diff, local dev server, and cloud code.

### Copy a site between environments

```bash
nimbu sites copy --from staging-site --to production-site --dry-run --json
```

See [references/site-migration.md](references/site-migration.md) for full-site and per-resource copy workflows.

### Set up local development

```bash
nimbu init                # Bootstrap nimbu.yml + theme structure
nimbu server              # Start proxy + child dev server
```

See [references/themes-and-local-dev.md](references/themes-and-local-dev.md) for dev server configuration.

## Error Handling

In `--json` mode, errors emit a structured envelope to stderr:

```json
{
  "status": "error",
  "error": {
    "code": "resource.not_found",
    "message": "page not found: about/missing",
    "hint": "",
    "exit_code": 5,
    "http_status": 404,
    "retryable": false
  }
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Usage / invalid arguments |
| 3 | Authentication failure |
| 4 | Authorization / scope failure |
| 5 | Resource not found |
| 6 | Validation error |
| 7 | Rate limit exceeded (retryable) |
| 8 | Network error (retryable) |

### Canonical Error Codes

`auth.not_logged_in`, `auth.unauthorized`, `auth.forbidden`, `auth.scope_missing`,
`resource.not_found`, `resource.conflict`, `request.invalid`, `request.validation`,
`rate_limit.exceeded`, `network.timeout`, `network.failure`, `server.error`.

Check `retryable: true` before retrying failed requests.

## Pagination

List commands support:

| Flag | Purpose |
|------|---------|
| `--all` | Fetch all pages automatically |
| `--page N` | Specific page number |
| `--per-page N` | Items per page |

Default behavior returns the first page. Use `--all --json` for complete datasets.

## Reference Files

| File | Covers |
|------|--------|
| [channels-and-entries.md](references/channels-and-entries.md) | Channel CRUD, entry CRUD, schema, info, copy, diff |
| [pages-menus-content.md](references/pages-menus-content.md) | Pages, menus, blogs, translations, notifications |
| [products-orders-customers.md](references/products-orders-customers.md) | Products, orders, customers, collections, coupons |
| [themes-and-local-dev.md](references/themes-and-local-dev.md) | Theme sync, local dev server, cloud code apps |
| [site-migration.md](references/site-migration.md) | Full-site copy, per-resource copy, cross-API migration |
