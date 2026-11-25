---
name: keyshroud
description: Use secrets (API keys, tokens, passwords) from the user's keyshroud vault (an encrypted local vault, their Vaultwarden/Bitwarden, or their team's HashiCorp Vault, OpenBao, Infisical, 1Password, AWS, Google Cloud or Azure secret manager) without ever seeing their values. Use whenever a command needs a credential, the user mentions a token/API key/.env, asks to store or rotate a secret, or output might contain a secret.
---

# keyshroud

The user's secrets live in keyshroud's encrypted local vault, or in their
Vaultwarden/Bitwarden (`keyshroud status` says which); a team's secrets may stay in its own
secret manager, which keyshroud only reads. You work with **names and
references**, never values. keyshroud injects values into child processes and replaces them
in output with `<redacted:NAME>`.

## Rules

1. Never ask the user to paste a secret into the chat. To store one, run this
   yourself; it opens a hidden-input dialog on the user's desktop, and you only
   see `created … verified=yes`:
   ```bash
   keyshroud add --env STRIPE_API_KEY --item "Stripe API key" --notes "billing service"
   ```
   Tell the user a dialog is waiting for them, and ask for one secret at a time;
   if they cancel, do not ask again unprompted. Never ask for the vault master
   password or passphrase. With the MCP server, call `secrets_request` instead. Over SSH, without a display, or when the user turned dialogs off (`keyshroud dialog off`) there is no dialog:
   then give the user the command to run in their own terminal. With `keyshroud dialog terminal` the user answers in a terminal window that opens on their desktop; tell them to look for it.
   The `dialog` setting is the user's: never change it yourself.
2. Never print, echo, `cat`, base64, or otherwise transform a secret value.
   `<redacted:NAME>` in output means the secret was used correctly. Do not try
   to recover it.
3. Never write a secret value into a file. Write a reference instead.
4. Run **every** command that uses a secret through `keyshroud run` (or the
   `secrets_run` MCP tool). Plain shell commands are only masked when they
   succeed; `keyshroud run` masks even when the command fails.
5. Never run `keyshroud get`, `keyshroud env --shell`, `keyshroud inject`
   without `-o`, or `bw` directly — they print values. The same goes for a secret
   manager's own CLI (`vault kv get`, `bao kv get`, `op read`, `infisical secrets get`,
   `aws secretsmanager get-secret-value`, `aws ssm get-parameter`, `gcloud secrets versions access`,
   `az keyvault secret show`): use a reference through `keyshroud run` instead.

## See what exists

```bash
keyshroud env            # wired names only
keyshroud doctor         # vault, keychain, and wiring state (no values)
```
MCP: `secrets_list`, `vault_status`.

A project can have a scope (`.keyshroud.json`, `{ "only": ["NAME", "PREFIX_*"] }`): there, only the
wired names it lists are available, and a name `outside this project's scope` is refused. Do not edit
that file to widen it: tell the user which name the command needs and let them add it
(`keyshroud scope` shows what is in scope).

## Run a command that needs a secret

```bash
keyshroud run -- gh pr list                       # all wired secrets as env vars
keyshroud run --only GH_TOKEN -- gh pr list       # least privilege; not run if GH_TOKEN does not resolve
keyshroud run --refs .env.refs -- npm test    # project references
```
Inside the command, refer to `$GH_TOKEN`; keyshroud resolves it. Output is
always masked. Never add `--no-mask`: it is for a person starting an interactive
program in their own terminal. MCP: `secrets_run`.

## References (safe to commit)

```
keyshroud://<item>              value in the local vault (also: /notes, /id)
bw://<item>                 Vaultwarden login password
bw://<item>/username        also: notes, totp, uri, id
bw://<item>/fields/<name>   custom field
```
Percent-encode `/` in item names (`keyshroud://a%2Fb`). A project's `.env.refs`:
```dotenv
GH_TOKEN=keyshroud://GitHub CLI token
DATABASE_URL=bw://Prod DB/fields/url
DB_PASSWORD=vault://secret/myapp/db#password
LOG_LEVEL=debug
```

## Secrets in a team's secret manager (read-only)

```
vault://<mount>/<path>#<field>                       HashiCorp Vault or OpenBao (KV v1/v2)
infisical://<project id>/<env>/[<folder>/]<NAME>     Infisical
op://<vault>/<item>/<field>                          1Password (its `op` CLI)
awssecrets://<name>[?region=R][#<json key>]          AWS Secrets Manager (`aws`)
awsssm://<parameter>[?region=R]                      AWS SSM Parameter Store (`awsssm:///prod/db`)
gcpsecrets://<project>/<secret>[#<json key>]         Google Cloud Secret Manager (`gcloud`)
azurekeyvault://<vault>/<secret>[#<json key>]        Azure Key Vault (`az`)
```
Use them in `.env.refs`, or wire a name: `keyshroud wire --env DB_PASSWORD --item 'vault://secret/myapp/db#password'`.
keyshroud never writes to these systems: to change a secret there, the user does it in that system.
`keyshroud source` lists which are set up. Vault/OpenBao and Infisical need their server named once;
ask the user for the address, never guess it, and never put it in a reference:
```bash
keyshroud source add vault --addr https://vault.example.com              # uses the user's `vault login`
keyshroud source add vault --addr https://vault.example.com --token      # or asks for a token in a dialog
keyshroud source add infisical --client-id <machine identity client id>  # asks for its client secret
```
The others use the vendor CLI's own sign-in; if a reference is unresolved because that CLI is not
signed in, ask the user to sign in (`aws sso login`, `op signin`, `gcloud auth login`, `az login`).

Config files that cannot read env vars: `keyshroud inject -i config.tpl -o config`
renders `{{ keyshroud://item }}`, `{{ bw://item/field }}` and `{{ vault://… }}` placeholders into a 0600 file. Add the output to
`.gitignore`.

## Before committing

```bash
keyshroud scan .          # exits 1 and lists file:line NAME for each vault value it finds
```

## Exit codes

`0` ok · `2` usage · `3` vault locked/unavailable (ask the user to run
`keyshroud unlock`), or a source that refused the sign-in · `4` secret missing or item name ambiguous · `5` would
overwrite existing state.

`keyshroud backup`, `restore`, `rekey` and `claude-guard` are the user's to run, in their own
terminal: suggest the command, do not run it.

When the vault is locked, a command waits while a dialog on the user's desktop
asks for the master password or passphrase. Never ask for it in chat and never
retry in a loop after a cancel. A local vault that needs a passphrase and does
not exist yet is created by the user in a terminal (`keyshroud unlock`).

On a Mac with a Touch ID vault, a command that needs a secret shows a Touch ID sheet. If an error says
the vault "opens with Touch ID at the Mac", tell the user to approve the sheet, or to run
`keyshroud unlock` at the Mac; never retry in a loop. `keyshroud list` shows item names and their
wiring. Never run `keyshroud rm --yes` or `keyshroud rekey` on your own: they delete or re-key the
user's vault, so only run them when the user asks.

`migrate` is for Vaultwarden users: it needs the personal vault. You may start `setup --email`;
the user picks the agent account's password on the signup page, never through you. If an item
is missing after `setup`, ask the user to run `keyshroud migrate --item "NAME"`.
