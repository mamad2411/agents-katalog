---
name: redhat-setup
license: CC-BY-4.0
description: >-
  Check whether this machine can fetch Red Hat documentation and Customer Portal
  content, and when the personal Red Hat offline token is missing, guide the user
  through generating it, storing it (sops + age recommended, Bitwarden, OS keychain, or a 0600 file),
  loading it, and verifying it – without the secret ever entering the chat. Use
  when a Red Hat fetch reports "no offline token", "subscriber_only",
  "invalid_grant", or when onboarding a teammate to the redhat plugin.
argument-hint: '[--check-only]'
user-invocable: true
compatibility: >-
  Red Hat SSO offline tokens from access.redhat.com/management/api (30-day idle
  expiry) as of 2026-08; Bitwarden CLI 2026.8.0 (source-verified sync/list/get/create/edit contract);
  macOS security(1) keychain; libsecret secret-tool on Linux; jq >= 1.6 (`--rawfile`);
  sops 3.13.3 (installed help + dummy stdin round-trip verified; >= 3.10 for age plugins/stdin);
  age 1.3.2; bash 3.2+ for rh-*.sh helpers; bash or zsh for the paste prompts.
allowed-tools: Bash, AskUserQuestion
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Red Hat docs – setup

Each teammate uses their **own** Red Hat account. The plugin never asks for the token
in conversation: every step below either prompts the user in their own terminal or reads
the secret from a store. **Never ask the user to paste the token here, and never run a
command that would print it.**

Before changing or relying on Bitwarden CLI behavior, verify the installed version against
the [official CLI documentation](https://bitwarden.com/help/cli/) and the
[pinned lookup implementation](https://github.com/bitwarden/clients/blob/cli-v2026.8.0/apps/cli/src/commands/get.command.ts).
The offline tests use shims; they do not replace verification against the installed CLI.

Before relying on sops flags, verify `sops --version`, `sops --help`, and
`sops encrypt --help` against the [canonical docs](https://getsops.io/docs/usage/common-operations/).
Verified on **sops 3.13.3**: omit the positional filename to read stdin, supply
`--filename-override` (required for stdin), and explicitly set input/output types.
Do not use `-` as a filename or `--in-place` for stdin. The
[3.10.0 changelog](https://github.com/getsops/sops/releases/tag/v3.10.0) introduced
stdin encryption/decryption and age plugin support. Its
[pinned implementation](https://github.com/getsops/sops/blob/v3.10.0/age/keysource.go)
accepts `AGE-PLUGIN-` identities for decryption: this covers the age plugin protocol
used by TPM and YubiKey plugins, with the plugin executable on `PATH`.
Hardware TPM/YubiKey decryption was **not live-tested**; protocol/source verification
is not evidence that a particular device, PIN, or user-presence policy works.

## 1. Check

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/fetch-docs/scripts"
bash "$S/rh-preflight.sh" --json
```

Report OS, fetcher, `bw`, `sops`, `age`, `age-plugin-tpm`, `tpm` (`present`,
`accessible`, or `none`) with any `tpm_hint`, and `credential`
(`env`, `keychain`, `sops`, `file`, `bitwarden`, or `none`).
If `fetcher` is `none`, stop: curl must be installed first
(`brew install curl` / `dnf install curl` / `apt install curl`). If `jq` is `no`, same.
If `bw` is `no`, say so beside the optional Bitwarden option; it is not required.
If `sops` or `age` is `no` (or sops < 3.10), offer the user-terminal helper:

```bash
bash "$S/rh-install-sops-age.sh"        # preview; no downloads or changes
bash "$S/rh-install-sops-age.sh" --yes  # only after user approves the plan
```

It selects brew/dnf/apt-get for **age only** (EL9 needs EPEL already enabled).
It downloads the pinned sops 3.13.3 **raw binary**, not an rpm/deb: upstream's
checksums do not cover packages. It requires one exact checksum entry and installs
to `~/.local/bin/sops` only after verification. Unsupported OS/arch fails closed.
Ensure that directory is on the user's and agent's PATH; restart after launch-PATH
changes. Checksums over HTTPS are integrity checks, not independent publisher
signature verification; cosign bundle verification is not implemented.
For dnf errors, inspect repository/GPG diagnostics; unrelated broken repos can
block any install. The helper prints a `--disablerepo=<broken-repo>` retry hint;
it never enables repos or disables GPG verification automatically.
Report `age-plugin-tpm` if present. On Linux with `/dev/tpmrm0` readable **and writable**, prefer
TPM-backed storage; if missing, offer
`go install github.com/foxboron/age-plugin-tpm/cmd/age-plugin-tpm@latest` or its
[upstream binaries](https://github.com/Foxboron/age-plugin-tpm/releases).
Check the installed plugin's help against its
[usage docs](https://github.com/Foxboron/age-plugin-tpm#usage) before generating an identity.

If `credential` is not `none`, verify and finish:

```bash
bash "$S/rh-token.sh" --check      # → source=<src> access_token=ok expires_in=900s
```

Exit `4` means Red Hat SSO rejected the token (`invalid_grant`, typically 30 days unused):
continue at step 2 to regenerate.

Exit `3` here also covers sops decryption failure or an empty/missing
`RH_OFFLINE_TOKEN` key: check identity discovery and plugin availability, then
re-store at step 3. Never diagnose by decrypting into a tool call's output.
Other empty sources include a `redhat-credentials` item
with no token in Notes – `export RH_OFFLINE_TOKEN=…`, `RH_OFFLINE_TOKEN=…`, or a bare JWT –
and no nonempty custom field `RH_OFFLINE_TOKEN` (text or hidden), or a token file whose
first line is blank – only line 1 is read. The Bitwarden hint names the item
(`RH_BW_ITEM` overrides the default) and the places checked, never values. Skip step 2
if the user still has their token and re-store it at step 3 with the same source.

With `--check-only`, stop after this step whatever `credential` says.

## 2. Generate (user does this in a browser)

Tell the user, verbatim:

1. Open <https://access.redhat.com/management/api> and log in with **your** Red Hat account.
2. Click **Generate Token**. Copy it now – it is shown once and is not stored by Red Hat.
3. It stays valid as long as it is used at least once every **30 days**; after that,
   regenerate here and re-store it.

## 3. Store – ask once, then give the matching commands

Use `AskUserQuestion` exactly once, options in this order:

- **sops + age (Recommended)** – encrypted at rest, read per call; prefer a TPM-backed identity.
- **Bitwarden personal vault** – optional master copy; syncs across machines.
- **OS keychain** – macOS Keychain or Linux Secret Service; no vault needed.
- **0600 file** – `${XDG_CONFIG_HOME:-$HOME/.config}/redhat/offline-token` (or `$RH_OFFLINE_TOKEN_FILE`);
  least preferred (plaintext at rest).

The user runs the store command **in their own terminal** (not via `!`, whose output
lands in the transcript). Give only the chosen block. Expand `$S` to the installed scripts directory for
commands given to the user (`CLAUDE_PLUGIN_ROOT` is not set in their terminal).

**sops + age** (no `bw` needed):

Use an existing identity if one exists; **never overwrite it**. sops discovers
`$XDG_CONFIG_HOME/sops/age/keys.txt` (default `~/.config/sops/age/keys.txt`) on Linux;
on macOS it also honours `XDG_CONFIG_HOME`, otherwise defaults to
`~/Library/Application Support/sops/age/keys.txt`.
A custom identity path needs `SOPS_AGE_KEY_FILE` in the agent's launch environment;
prefer the default path to avoid that restart requirement. See
[identity discovery](https://getsops.io/docs/usage/identities/age/).

In the user's terminal:

```bash
bash "$S/rh-store-sops.sh"
```

Without a recipient, the store helper calls `rh-age-identity.sh`: reuse the existing
identity or create it at the discovered path (including `SOPS_AGE_KEY_FILE`).
New identities use umask 077 and mode 0600, and are published without overwriting
even a concurrently created key. Symlink identities are refused. With an installed
`age-plugin-tpm` and readable/writable `/dev/tpmrm0`, new keys use TPM generation
(no PIN); otherwise they use `age-keygen`. Existing keys are never migrated.
Generation/derivation errors stop before the token prompt. Multiple-key files need
an explicit public recipient argument; the helper refuses ambiguous output.
For identity creation alone, `bash "$S/rh-age-identity.sh"` prints **only** the public
recipient. No `r` variable has to survive between pasted blocks.

The helper uses a hidden `IFS= read -rs t` prompt, a **builtin printf** pipe to
`sops encrypt --age ... --input-type dotenv --output-type yaml --filename-override ...`,
then a 0600 ciphertext temporary file + rename. No token in argv, history, transcript,
or plaintext staging file. It disables tracing, rejects empty pastes, and leaves an
existing file unchanged on failure. The destination is
`${RH_OFFLINE_TOKEN_SOPS_FILE:-${XDG_CONFIG_HOME:-$HOME/.config}/redhat/offline-token.sops.yaml}`.
It passes `--age` explicitly; no `.sops.yaml` change is needed.

Optional Bitwarden seeding (only if it is already the user's master copy): unlock/sync
in **this terminal**, then use the same helper:

```bash
s="$(bw unlock --raw)"; [ -n "$s" ] && export BW_SESSION="$s"; unset s
if [ -n "${BW_SESSION:-}" ] && bw sync >/dev/null; then
  bash "$S/rh-store-sops.sh" --from-bitwarden
fi
```

This captures the single item's Notes/custom field through the credential resolver
(same accepted layouts and Notes precedence below), never prints it, and feeds it to
sops on stdin. Failed/ambiguous lookup or an empty token does not replace the file.
No `eval` or intermediate plaintext file is used for seeding.

**Bitwarden** (the `bitwarden:secrets` pattern – Secure Note named `redhat-credentials`):

The scripts accept these layouts on that item (a Login item also works):

- Notes: `export RH_OFFLINE_TOKEN=…` or `RH_OFFLINE_TOKEN=…`.
- Notes: a bare JWT on its own line (three base64url segments).
- Custom field named exactly `RH_OFFLINE_TOKEN`, type **Text** or **Hidden**, holding the token.

Notes win when both Notes and the custom field contain a token. The field is read only
when Notes yield no token; an empty field still exits `3`. Keep exactly one matching
item; both Notes and field lookups use the same Bitwarden single-item lookup rules.
The block below stores the Notes layout.

```bash
s="$(bw unlock --raw)"; [ -n "$s" ] && export BW_SESSION="$s"; unset s
if [ -z "${BW_SESSION:-}" ] || ! bw sync >/dev/null; then echo "unlock or sync failed – fix that, then re-run" >&2; else
  # get notes and list --search use the same basic search, including names and note contents
  if ! items="$(bw list items --search redhat-credentials 2>/dev/null)"; then
    echo "vault lookup failed – fix that, then re-run" >&2
  elif ! hits="$(printf '%s' "$items" | jq -ecs '
    if length != 1 or (.[0] | type) != "array" then error("expected one item array")
    else .[0] | map(
      if (.id | type) != "string" or .id == "" or (.name | type) != "string"
      then error("invalid item") else {id, name} end) end' 2>/dev/null)"; then
    echo "vault lookup returned invalid data – fix that, then re-run" >&2
  elif ! count="$(printf '%s' "$hits" | jq -er 'length')" \
    || ! id="$(printf '%s' "$hits" | jq -r '.[] | select(.name == "redhat-credentials") | .id')" \
    || ! names="$(printf '%s' "$hits" | jq -r '[.[].name] | join(", ")')"; then
    echo "vault lookup filter failed – fix that, then re-run" >&2
  elif [ "$count" -gt 1 ]; then
    echo "more than one note matches 'redhat-credentials' ($names) – keep exactly one, named redhat-credentials, then re-run" >&2
  elif [ -n "$names" ] && [ -z "$id" ]; then
    echo "a note named '$names' would shadow 'redhat-credentials' – rename it to redhat-credentials (or delete it), then re-run" >&2
  else
    printf 'Paste offline token: '; IFS= read -rs t; echo
    if [ -n "$t" ] && [ -n "$id" ]; then
      bw get item "$id" | jq --rawfile notes <(printf 'export RH_OFFLINE_TOKEN=%s\n' "$t") '.notes = $notes' \
        | bw encode | bw edit item "$id" >/dev/null && echo updated
    elif [ -n "$t" ]; then
      bw get template item \
        | jq --rawfile notes <(printf 'export RH_OFFLINE_TOKEN=%s\n' "$t") --arg name redhat-credentials \
             '.type = 2 | .secureNote.type = 0 | .notes = $notes | .name = $name' \
        | bw encode | bw create item >/dev/null && echo stored
    fi
  fi
fi; unset t id hits names items count
```

Works in bash and zsh (the macOS default). The template goes to `jq` on stdin and the
note text through a process substitution, so the token is never an argument of any
process. An unavailable session, failed sync, failed lookup, or invalid lookup JSON stops
the block before it asks for the token or writes to the vault. Re-running
(a regenerated token) **edits the existing note in place**. The block refuses when the vault
returns more than one search result, or a result not named exactly `redhat-credentials`.
Bitwarden 2026.8.0 searches names, notes, and other indexed fields, so even a differently
named item mentioning `redhat-credentials` can make the lookup ambiguous. Remove the
matching text from unrelated items or rename the intended note, then retry. If the block
is unfamiliar, the equivalent is: create (or update) a Secure Note called `redhat-credentials` whose content is
one line, `export RH_OFFLINE_TOKEN=<token>`.

**macOS keychain** (prompts for the secret, keeps it out of shell history):

```bash
security add-generic-password -a "$USER" -s RH_OFFLINE_TOKEN -U -w
```

**Linux Secret Service** (prompts for the secret, keeps it out of shell history):

```bash
secret-tool store --label='Red Hat offline token' service redhat key RH_OFFLINE_TOKEN
```

**0600 file** (bash or zsh – `read -p` is deliberately avoided: zsh reads it as a coprocess
and would silently store an empty file):

```bash
d="${XDG_CONFIG_HOME:-$HOME/.config}/redhat" && mkdir -p "$d" && (umask 077; printf 'Paste offline token: '; IFS= read -rs t; echo; [ -n "$t" ] && printf '%s\n' "$t" > "$d/offline-token" && chmod 600 "$d/offline-token" && echo "stored in $d/offline-token")
```

The path honours `XDG_CONFIG_HOME` because the scripts resolve the same
`${XDG_CONFIG_HOME:-$HOME/.config}/redhat/offline-token` (or `RH_OFFLINE_TOKEN_FILE`).

## 4. Load

- **Bitwarden**: before launching `claude`, in the shell: `export BW_SESSION="$(bw unlock --raw)"`.
  Leave `BW_SESSION` exported and the scripts read Notes or the custom field on demand.
  For the `export RH_OFFLINE_TOKEN=…` Notes layout only, you can instead use
  `eval "$(bw get notes redhat-credentials)"` (or `bwe redhat-credentials` from
  `bitwarden:secrets`). Tool calls inherit that environment; this load step does not
  read custom fields or bare JWT Notes.
- **sops / keychain / file**: nothing to load – the scripts resolve them directly.
- Resolution order is `env → keychain → sops → file → bitwarden`; restrict with
  `RH_CRED_SOURCES=env,sops` if needed (membership filter, not a custom ordering).

| Source | Restart the agent after storing? |
|---|---|
| `env` | Yes: export before launching; another pane cannot update a running process. |
| `bitwarden` | Yes if `BW_SESSION` was not exported before launch; vault edits alone need none. |
| `sops` | No with the default identity/path and plugins already on PATH; read each call. |
| `keychain` | No; Secret Service must be reachable on Linux. |
| `file` | No; read each call. |

Changing launch-time path overrides, `RH_CRED_SOURCES`, `SOPS_AGE_KEY_FILE`, or `PATH`
also needs a restart. Creating the default sops file/identity does not.

## 5. Verify

```bash
bash "$S/rh-token.sh" --check
```

`--check` always performs a fresh exchange (it never reports a cached access token), so
it verifies the token that was just stored. Success prints the source and `expires_in`
only. Then hand back to `/redhat:fetch-docs`. If it prints `invalid_grant`, the pasted
token is wrong or expired – regenerate (step 2) and re-store.

If it exits `3`, first confirm storage completed: Bitwarden must report `stored` or
`updated`, the sops helper or file block must report `stored in ...`, and the keychain command must
finish successfully. An empty paste, cancelled prompt, or failed write means step 3
must be retried; do not diagnose a session problem until storage succeeds.

Then read the message. "No Red Hat offline token found" means no usable credential
was found; after successful storage, check visibility to this session: for Bitwarden,
`BW_SESSION` (or the `bwe`-loaded `RH_OFFLINE_TOKEN`)
must be in the environment `claude` was launched from – finish step 4 in that shell and
restart `claude`, or have the user run the same `rh-token.sh --check` in the terminal where
the vault is unlocked (give the expanded `$S` path; `CLAUDE_PLUGIN_ROOT` is not set there; it
prints only the source and `expires_in`); for sops, check the encrypted path and age
identity discovery (without printing plaintext); for a file, `HOME`/`XDG_CONFIG_HOME` must match the
path step 3 printed; for the Linux keychain, the Secret Service must be reachable from this
session. "returned an empty token" means the store was found but holds no usable token –
for Bitwarden, check the named item's Notes layouts and `RH_OFFLINE_TOKEN` custom field
(text or hidden) listed in the message; re-store at step 3. Notes take precedence, so
update or remove a stale Notes token when switching to a custom field.

## Threat model

| Setup | Encrypted at rest | Works per call (no restart) | Protects against same-user processes |
|---|---|---|---|
| `file` (0600) | ❌ | ✅ | ❌ |
| `sops` + plain age key (`~/.config/sops/age/keys.txt`) | ✅ (file alone is useless) | ✅ | ❌ (key is next to it) |
| `sops` + `age-plugin-tpm` | ✅; key cannot be taken off the machine | ✅ (without PIN) | ❌ (can still call `sops -d`) |
| `sops` + `age-plugin-yubikey` | ✅ | ⚠️ needs touch/PIN | Partly (device policy dependent) |
| `bitwarden` / `env` | ✅ in vault; env itself is not encrypted storage | ❌ must be set before launch | ❌ once loaded |

A plain age key gives little extra same-machine protection over a 0600 file. It
protects against the encrypted file leaking **alone** (backups, dotfiles, sync).
TPM backing additionally prevents moving the key to another machine; retain a
recovery plan (e.g. regenerate the Red Hat token) before TPM reset/host loss.
No source is a general defense against same-user processes. The transcript guarantee
is unchanged: the model never handles the token in chat, and the guard denies direct
sops decryption (including `exec-env`/`exec-file`) of this token file. The lexical hook is not an OS security boundary.
