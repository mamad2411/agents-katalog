---
name: proto-up
description: Upload a self-contained HTML prototype to ProtoPeek (protopeek.dev) and print the private, shareable review link. Re-running on the same file publishes a new version behind the same link. Use when the user wants to share a prototype for review, publish a new version of one, or says "proto-up".
---

Upload an HTML prototype to ProtoPeek and return a shareable link. ProtoPeek
(https://protopeek.dev, source: https://github.com/Brightwing-Systems-LLC/protopeek) hosts
the file behind an unguessable link, gated by an email allowlist, for a flat 30 days.
Invited reviewers pin comments on the page; `/proto-feedback` pulls them back.

Works like a deploy tool: the first run of a file mints a link; later runs publish a new
version behind the SAME link by default (reviewers just refresh — no link churn).

Arguments: the first token is the path to the self-contained `.html` file. Optional flags:

- `--name "..."` — display name (defaults to the file name).
- `--allow <domain-or-email>` — add an allowlist rule (repeatable; comma-separate values).
- `--private` — don't apply your default reviewer domain. Alone: a locked share (nobody
  can view until rules are added). With `--allow`: exactly those rules and nothing else.
- `--new` — force a FRESH link even if this file was shared before.
- `--update <url-or-uuid>` — explicitly target an existing link (overrides the log lookup).

## Step 0 — Config (ask before minting)

```bash
CFG="${XDG_CONFIG_HOME:-$HOME/.config}/protopeek"
[ -n "$PROTOPEEK_TOKEN" ] || . "$CFG/config" 2>/dev/null
```

If there is still no `$PROTOPEEK_TOKEN`, **ask the user before doing anything**: minting a
token is one anonymous API call to protopeek.dev — no account, no signup, no personal data —
and the token will be stored at `~/.config/protopeek/config` (chmod 600). Suggest a default
reviewer domain (from `git config user.email`'s domain, or ask; blank is fine — it's a
local convenience, changeable anytime with `/proto-config set-default`). On a yes:

```bash
mkdir -p "$CFG"
resp=$(curl -s -X POST "https://protopeek.dev/api/tokens" -H "Content-Type: application/json" \
  -d "{\"label\":\"$(hostname)\",\"default_domain\":\"$DOMAIN\"}")
# extract .token from $resp, then:
printf 'PROTOPEEK_BASE_URL=%s\nPROTOPEEK_TOKEN=%s\nPROTOPEEK_DEFAULT_DOMAIN=%s\n' \
  "https://protopeek.dev" "$TOKEN" "$DOMAIN" > "$CFG/config"
chmod 600 "$CFG/config" 2>/dev/null || true
```

Mint only if the config is missing (a second token would orphan the first token's
prototypes). The token is low-value and rotatable — reference it as `$PROTOPEEK_TOKEN`,
never echo it, never commit it.

## Step 1 — Build the allowlist (explicit, no server magic)

The server applies exactly the rules in the request; nothing is added behind your back.
Split `--allow` values into `domains` (no `@`) and `emails` (contains `@`), joined
comma-separated. Unless `--private` was given, include `$PROTOPEEK_DEFAULT_DOMAIN` in
`domains` (your configured default — see `/proto-config`). Tell the user what the
allowlist will be, e.g. "Allowlist: anyone @copient.ai (your default) + jane@partner.com".
If it ends up EMPTY, warn: the link will be locked — nobody can view until rules are added.

## Step 2 — Confirm before the first upload of a file

Before uploading a file for the first time, tell the user in one line where it's going:
the HTML is stored on protopeek.dev, reachable only via the unguessable link by reviewers
whose email matches the allowlist, and expires in 30 days. If the prototype visibly
contains real personal data (real names, emails, customer records), point that out and
offer to swap in placeholders first. On an update, or re-sharing a file the user already
approved, don't re-ask.

## Step 3 — Create or update?

Decide the target before uploading:

- `--update <url-or-uuid>` → extract the trailing UUID and pass `update_of=<uuid>`.
- `--new` → always create a fresh link.
- Neither flag: check `$CFG/prototypes.json` for records under this project directory
  whose `source_path` matches this file (or whose `content_sha256` matches). Exactly one
  match → **update it by default**: announce "publishing v<N+1> behind <url>" and pass
  `update_of=<uuid>`. More than one candidate → list them and ask. None → create a new
  link. (Default-update keeps the reviewers' link and feedback history in one place; a
  fresh link is the deliberate exception, not an accident.)

```bash
curl -s -X POST "$PROTOPEEK_BASE_URL/api/prototypes" \
  -H "Authorization: Bearer $PROTOPEEK_TOKEN" \
  -F "html=@<path>;type=text/html" \
  -F "name=<name>" \
  -F "domains=<domains>" \
  -F "emails=<emails>" \
  -F "update_of=<uuid-if-any>"
```

## Step 4 — Report and record

Parse the JSON response (`uuid`, `url`, `version`, `expires_at`, `rules`) and print
clearly: the **shareable URL**, the version number, the expiry (a flat 30 days from
upload), and **who can view** — the effective allowlist from `rules` (e.g. "anyone
@copient.ai, jane@partner.com"); if `rules` is empty, flag it: **locked — nobody can
view yet**. Then record it in `$CFG/prototypes.json` (atomic write — temp file +
rename): a record keyed by `uuid` with `url`, `name`, `source_path`, `source_basename`,
`project_dir`, `created_at`, `expires_at`, `version`, and the `content_sha256` of the
uploaded file. On an update, refresh the existing record (`version`, `content_sha256`,
`name`) instead of adding one. This lets a later session resolve "yesterday's dashboard"
without a typed UUID.

Remind the user: send the URL to reviewers; `/proto-status <url>` polls cheaply,
`/proto-feedback <url>` pulls and synthesizes. If the response is an error, show the
status and `detail`.
