---
name: onepassword-cli
description: Use the 1Password CLI (`op`) to read secrets, list and inspect vaults/items, inject secrets into env files and commands, and create/edit items on Magnus's accounts (a personal account and a work account). Use when the user mentions 1Password, the `op` command, secret references (`op://...`), needs an API key/token/credential pulled from a vault, wants to feed secrets into `.env` files or commands via `op run`/`op inject`, or asks to find, read, create, or edit a vault item.
user-invokable: true
---

# onepassword-cli

Drive the 1Password CLI (`op`, currently 2.30.0) on this machine. Auth is **desktop-app
integration + Touch ID**, so there is no password or `eval $(op signin)` step. The golden
rule: **resolve secrets into commands/files, never echo them into the terminal.**

## This machine's setup

- **Two accounts** (target with `--account <addr>` or `export OP_ACCOUNT=<addr>`):
  - Personal (**default for personal work**): `my.1password.eu`
  - Work: run `op account list` for the address. It is deliberately not written
    down here: this repo is public, and the employer's tenant plus work email do
    not belong in it. `op account list` is also the only source that stays right.
- **Personal vaults**: `Development`, `Private` (holds most logins + all API credentials),
  `Shared`, `Shared Notes`.
- **Auth quirks** (expected, not bugs):
  - `op whoami` prints `account is not signed in` even when commands work — app
    integration has no classic session token. Don't treat it as an error.
  - Commands trigger a Touch ID prompt that **times out fast** (`authorization
    timeout`). If you see that, just **rerun the same command** and approve promptly.
- `~/.config/op/` is **gitignored** (device ID is sensitive). Never store this skill or
  any resolved secret there, and never commit that directory.

## Quick start

```bash
export OP_ACCOUNT=my.1password.eu        # target the personal account for the session
op vault list                            # Development / Private / Shared / Shared Notes
op item list --vault Private             # titles only (safe)
op read "op://Private/Cargo API Token/token"   # one field; pipe it, don't paste it
```

## Secret references

Format: `op://<vault>/<item>/<field>` or `op://<vault>/<item>/<section>/<field>`.
`<item>` may be a title or its ID; `<field>` is a field label (e.g. `token`, `password`,
`username`, `credential`). Find the exact reference for any item with:

```bash
bash scripts/op-fields.sh "Cargo API Token" Private   # lists labels/types/refs, VALUES MASKED
```

## Core workflows

- **Read one secret into a command** (never assign it to a shell var that gets printed):
  ```bash
  docker login -u "$(op read op://Private/docker/username)" \
               -p "$(op read op://Private/docker/password)"
  ```
- **Fill an env file from a template** — `.env.tpl` holds `KEY=op://...` lines:
  ```bash
  op inject -i .env.tpl -o .env       # resolves refs to real values (gitignore .env!)
  ```
- **Run a command with secrets as env vars** (nothing written to disk):
  ```bash
  op run --env-file=.env.tpl -- ./your-app      # .env.tpl values are op:// refs
  ```
- **Inspect an item's structure** without leaking values: `bash scripts/op-fields.sh "<item>" [vault]`.
- **Open an item in the 1Password desktop app (GUI)** — when the user must view or edit it
  themselves (e.g. paste a secret you must not handle). Uses a macOS deep link, UUIDs only,
  no secret read:
  ```bash
  bash scripts/op-open.sh "github-readme-stats PAT" Development edit   # action: edit | view (default)
  ```
  Raw form: `open "onepassword://view-item/?a=<account_uuid>&v=<vault_uuid>&i=<item_uuid>"`
  (`edit-item` jumps straight into edit mode). Resolve the UUIDs with:
  account → `op account list --format=json` (`.account_uuid`, match by `url`);
  vault + item → `op item get "<title>" --vault <v> --format=json` (`.vault.id`, `.id`).
- **Create / edit items, documents, SSH, multi-account, JSON output**: see [REFERENCE.md](REFERENCE.md).

## Shell plugins (cargo, openai)

`~/.config/op/plugins.sh` aliases `cargo` and `openai` to `op plugin run -- …` so they
authenticate from 1Password (a `gh` plugin exists but is disabled in favour of native
`gh auth`). The source line in `.zshrc` is **commented out** — enable by uncommenting
`source "$HOME/.config/op/plugins.sh"`. Manage with `op plugin list` / `op plugin init <tool>`.

## Safety rules

1. Never print a secret value to stdout for the user to read. Use `op read`/`op inject`/
   `op run` to route it into a command or a gitignored file.
2. When you must show an item, mask values (`scripts/op-fields.sh` does this).
3. Any file produced by `op inject` (e.g. `.env`) contains live secrets — confirm it's
   gitignored before writing it.
4. Use `--account` / `OP_ACCOUNT` explicitly so personal and work secrets don't cross.
