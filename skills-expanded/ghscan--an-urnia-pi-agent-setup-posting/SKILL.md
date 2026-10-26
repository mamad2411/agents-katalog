---
name: posting
description: Terminal API client (Postman/Insomnia alternative) with file-based collections (*.posting.yaml). Use when creating, editing, or reviewing Posting collections, request YAML files, .env files, importing from OpenAPI/Postman/curl, or writing pre-request/post-response Python scripts. pi maintains the files, the human drives the interactive TUI.
disable-model-invocation: true
---

# Posting × pi

[Posting](https://github.com/darrenburns/posting) (`posting.sh`) is a terminal TUI HTTP client.
Its collaboration model with pi is **file-based, not API-based**: pi creates and maintains
collection files, the human explores them interactively in the TUI.
There is **no headless runner** — pi cannot ask Posting to execute requests in CI.
For automated checks use `curl`/`httpx`/`php artisan test` instead.

Official docs: https://posting.sh/guide/ — verify against docs before inventing anything.
Last verified: posting 2.10.0, docs `main`, Sep 2026.

## Install

```bash
# recommended (uv manages Python itself)
uv tool install --python 3.13 posting
# or reuse an existing interpreter:
uv tool install --python /path/to/python posting
# alternative
pipx install posting
```

Do NOT `pip install` it. If `posting` is not on PATH after install,
add the uv tools shims dir (`uv tool update-shell` prints it).

## CLI (verified, `posting --help`)

```bash
posting --collection path/to/collection [--env dev.env [--env shared.env]]
posting import path/to/openapi.yaml [-o out-dir]            # OpenAPI 3.x, experimental
posting import --type postman collection.json [-o out-dir]  # Postman, experimental
posting locate collection   # default collection dir ("global" scratch area)
posting locate config       # config.yaml location
```

- `--collection`: any directory; all `*.posting.yaml` found **recursively**. No metadata files.
- `--env`: repeatable, later files override earlier ones. With no `--env`,
  a `posting.env` in cwd is autoloaded if present.
- If no `--collection`, requests land in the **default collection** — fine for
  throwaway probes, wrong place for project work.

## Collection layout (agent conventions)

```text
<collection>/
  shared.env            # variables common to all envs
  dev.env / prod.env    # env-specific overrides (BASE_URL, keys, POSTING_* config)
  <area>/               # sub-collection = plain subdirectory, mirrors URL structure
    list-things.posting.yaml
  scripts/              # pre/post-request python, committed with the collection
```

Rules for pi:

1. One request per file, filename mirrors request `name` (kebab-case).
2. Mirror URL structure in subdirectories (same convention `posting import` generates).
3. **Secrets and host-specific values go in `.env`, never in YAML.** Reference via `$VAR`/`${VAR}`.
4. Commit the collection dir (minus real secrets). `.env` files with real keys stay local;
   commit `*.env.example` instead.
5. After writing YAML, validate it parses (`python -c "import yaml,..."`) and matches
   [the request schema](references/request-format.md). Never invent keys.

## Variables & environments

- Syntax `$VAR` / `${VAR}` in URL, description, headers, query, path-param values,
  body content, form data, proxy URL (substituted via `string.Template` before send).
- Path params use `:name` placeholders in the URL; literal colons escape as `::`
  (`::id` renders `:id`, not a placeholder).
- Host OS env vars are **ignored** unless config `use_host_environment: true`
  (or `POSTING_USE_HOST_ENVIRONMENT=true`).
- Config precedence (high→low): `config.yaml` > `POSTING_*` env vars > `.env` files.
  Nested config via `__`: `POSTING_HEADING__VISIBLE=false`.
- Since all config keys are settable as env vars, per-env config (theme, SSL bundle,
  `use_host_environment`) can live in `dev.env`/`prod.env`, e.g.
  `POSTING_THEME=solarized-light` in `prod.env` as a "you are in prod" reminder.

## Import flows (pi's main leverage)

- **OpenAPI 3.x → collection**: `posting import api.yaml -o <collection>/`. No `-o`
  means the default collection — always pass `-o`.
- **Postman → collection**: `posting import --type postman c.json -o <collection>/`;
  Postman variables land in a `.env` inside the collection — review and split into
  `shared`/`dev`/`prod` afterwards.
- **curl → request**: paste the curl command into Posting's URL bar (experimental,
  interactive). Reverse direction is `export: copy as curl` from the command palette.
- **Framework routes → collection**: no built-in importer — generate YAML (or an
  OpenAPI spec, then import) from `route:list` output. This is the highest-value pi task.

## Scripting (Scripts tab, paths relative to collection root)

Three lifecycle hooks; one Python function each (extra args optional):

```python
def setup(posting): ...                          # before request is built
def on_request(request, posting): ...            # after build, before send
def on_response(response, posting): ...          # after response received
```

- Attach as `path/to/script.py` (looks for `setup`/`on_request`/`on_response`) or
  `path/to/script.py:function_name`. Scripts auto-reload on edit.
- `Posting` API: `set_variable` / `get_variable` / `clear_variable` /
  `clear_all_variables` / `notify(...)`. Variables are **session-scoped**.
- Available imports: stdlib + Posting's env (`httpx`, `pydantic`, `yaml`, ...).
  Extra deps (uv installs): `uv tool install posting --with <lib>`.
- Typical uses: fetch token in `setup` → `set_variable("auth_token", ...)` then use
  `$auth_token`; `on_request` to `request.headers.append(Header(...))` or set
  `request.auth = Auth.bearer_token_auth("...")`; `on_response` to capture tokens.
- Scripts run in Posting's process — no monkey-patching stdlib, no destructive globals.

## TUI survival guide (for instructing the human)

`Ctrl+J` send · `Ctrl+L` URL bar · `Ctrl+O` jump mode · `Ctrl+T` method ·
`Ctrl+N` new · `Ctrl+S` save · `D`/`Shift+D` duplicate · `Backspace` delete ·
`Ctrl+P` palette (`export: copy as curl`, `export: copy as YAML`) ·
`Ctrl+E` edit script in `$EDITOR` (file must already exist) · `F1` shortcuts.
