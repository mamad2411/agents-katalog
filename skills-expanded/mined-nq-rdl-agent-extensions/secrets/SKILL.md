---
license: CC-BY-4.0
description: >-
  Manage .env files and development secrets using the Bitwarden personal
  Password Manager CLI (bw). Use when the user asks to store, retrieve, or
  inject secrets / API keys / .env variables from Bitwarden. This skill covers
  the PERSONAL password manager only — NOT Bitwarden Secrets Manager. Trigger
  on: "bitwarden .env", "bw CLI secrets", "load API keys from bitwarden",
  "store credentials in bitwarden", "inject env vars from bitwarden".
compatibility: >-
  Requires the Bitwarden Password Manager CLI (bw), jq, awk, and bash or zsh.
  bw-env.sh was tested on 2026-09-29 against a stub of @bitwarden/cli 2026.9.0
  behaviour, in bash 5 and zsh 5.9 with GNU and BusyBox awk.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Bitwarden Personal PM — .env & Dev Secrets

Use the Bitwarden **personal** Password Manager CLI (`bw`) to keep development
secrets in the vault and load them into a shell on demand, instead of leaving a
plaintext `.env` on disk.

> **This is not Secrets Manager.** `bw` is the personal Password Manager;
> Bitwarden Secrets Manager is a different product with the `bws` CLI. See the
> [Password Manager overview](https://bitwarden.com/help/password-manager-overview/)
> and the [Secrets Manager overview](https://bitwarden.com/help/secrets-manager-overview/).

## Install and authenticate

```bash
npm install -g @bitwarden/cli    # or: brew install bitwarden-cli / snap install bw
bw login                          # interactive, once per machine
export BW_SESSION="$(bw unlock --raw)"
```

For CI and cron, use `bw login --apikey` (`BW_CLIENTID`, `BW_CLIENTSECRET`)
and `bw unlock --passwordenv BW_PASSWORD --raw`, never interactive unlock.

## Use the shell functions in `scripts/bw-env.sh`

[scripts/bw-env.sh](scripts/bw-env.sh) is the one implementation of the
`.env` functions. Tell the user to `source` it from `~/.bashrc` or `~/.zshrc`
(or copy it there). Do not retype the functions from memory: the details below
are what hand-written versions get wrong.

| Function | What it does |
|---|---|
| `bwc <item> [file]` | Create a Secure Note from a `.env` file (default `./.env`) |
| `bwu <item> [file]` | Replace an existing item's notes from a `.env` file |
| `bwe <item>` | Load the note's variables into the current shell |
| `bwunload <item>` | Unset the variables that item exports |
| `bwl [search]` / `bwll [search]` | List item names / names with IDs |
| `bwf <item> <field>` | Print one custom field of a Login item (capture it with `$(...)`) |
| `bwdotenv <item> [file]` | Write a plaintext `.env` for tools that need a file |
| `bwdd <item>` | Move an item to the trash |
| `bwss` | Unlock once per shell; the others call it |

What the script guarantees (covered by `tests/test_bitwarden_bw_env.py` in the
source repository, using a fake `bw`):

- **Storage format.** `bwc`/`bwu` store each line as `export NAME='value'`,
  keeping comments and blank lines. They accept `NAME=value`, `export
  NAME=value`, and single- or double-quoted values, and drop ` # comment` after
  an unquoted value. Values are literal: there is no `$VAR` interpolation.
- **No echo of secrets.** `bw create item` and `bw edit item` print the whole
  item, notes included. The script discards that output and prints only the
  item ID, so the values never reach the terminal or an agent transcript.
- **No arbitrary eval.** `bwe` refuses a note with any line other than a plain
  `export NAME=...`, so a hand-edited note cannot run commands.
- Works in bash and zsh, including under `set -u`.

When you drive `bw` directly instead of through the script, keep the same
rules: pipe `bw create`/`bw edit` output to `jq -r .id`, and never put a secret
on the command line (`--arg secret ghp_...` lands in shell history). Read it
with `read -rs`, then pass it through a pipe as in the Login example in
[references/cli.rst](references/cli.rst): `--arg secret "$secret"` still exposes
the expanded value in process arguments.

## Vault naming

Use predictable names so `bwl <project>` groups them:

```
<project>-<env>          myapp-dev, myapp-staging   (Secure Note, full .env)
<service>-credentials    aws-credentials            (Login, custom fields)
```

## Security rules

1. **`BW_SESSION` decrypts the whole vault.** Keep it in shell memory only:
   never write it to a file, log it, or pass it to `set -x` output.
2. **Use item IDs in lasting scripts** (`bw get notes <uuid>`); names can be
   duplicated, and `bw` errors on ambiguous names.
3. **Run `bw sync`** before reading data that may have changed elsewhere.
4. **Delete `bwdotenv` output after use** and keep `.env` in `.gitignore`.
5. **Mask values in CI logs.** A secret written to `$GITHUB_ENV` is not
   masked automatically; see [references/env-patterns.rst](references/env-patterns.rst).
6. **Secrets Manager is not this.** If a request needs `bws`, machine accounts,
   or projects, say this skill does not cover it.

## Common patterns

- **Several environments:** `bwe myapp-dev`, later `bwunload myapp-dev &&
  bwe myapp-staging`.
- **One token, many variable names:**
  [scripts/load-github.sh](scripts/load-github.sh) loads a token stored as a
  Secure Note by UUID and exports it as `GITHUB_TOKEN`, `GITHUB_OAUTH_TOKEN`,
  and `GIT_TOKEN`. It is written as a zsh autoload function file.
- **Structured credentials:** store AWS or database keys as hidden custom
  fields (type 1) on a Login item and read them with `bwf`:
  `export AWS_ACCESS_KEY_ID="$(bwf aws-credentials AWS_ACCESS_KEY_ID)"`.

## Reference files

| File | Read when |
|------|-----------|
| [references/cli.rst](references/cli.rst) | You need a `bw` command, flag, item type, or environment variable |
| [references/shell-functions.rst](references/shell-functions.rst) | You change `bw-env.sh` or explain why it is built the way it is |
| [references/env-patterns.rst](references/env-patterns.rst) | CI/CD, direnv, Docker Compose files, custom-field items, rotation |
| [assets/bw-env-format.env](assets/bw-env-format.env) | You need an example of the stored note format |
