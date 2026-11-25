---
name: kei-audit-encryption
description: "Set up and use opt-in audit-args encryption with the kei CLI: generate a customer-held age (X25519) identity locally, register only the public key so the runtime encrypts audit tool-call arguments to it, verify records carry args_ciphertext, decrypt a record locally to a file, rotate keys (add new, disable old), and manage the escrow setting. Use when someone asks to encrypt audit arguments or tool-call payloads, why a record has no args_ciphertext, how to recover or decrypt audit args, how to rotate, back up, or disable an audit encryption key, what is and is not encrypted in Kei audit records, or about `kei audit keys create|list|disable` or `kei audit decrypt`. Covers the opt-in contract: age multi-recipient encryption, the keyed args_digest, the audit-encryption-keys AIP resource, the runtime recipients fetch, opt-in semantics, and the lost-key tradeoff."
---

# Opt-in audit-args encryption

Kei audit records for tool and skill calls carry the arguments the agent
passed. Those arguments can hold customer data, credentials, or PII, so the
design decision is: **the audit args are readable ONLY by the customer.** When
the org opts in, the runtime encrypts the arguments
with [age](https://filippo.io/age) to customer-held public keys; Kei stores
only ciphertext and a keyed digest, and has no decryption path. This skill
owns the setup, verification, decryption, rotation, and the boundaries.

## Answer checklist

Answer from this skill: setup, decrypt, rotation, escrow, and what is
encrypted are all on this page, so you do not need to search a codebase first.
If something is not here, say so. In every answer:

- **Setup:** say that the `kei audit` commands need kei v0.1.9 or later
  (check `kei --version`). `kei login` (owner/admin) first; `kei audit keys
  create` writes the identity file `~/.config/kei/audit-identity.txt` (mode
  0600) and uploads **only the public key**. Back up the identity file itself.
  Say that registering the first key turns encryption on for new records.
- **Where to create the key (ephemeral or cloud pod, CI, a runtime host):**
  not inside the pod (the identity file would be lost with it). Say in so
  many words that the runtime never needs the private key: it only fetches
  the public recipients. Create the key on a persistent admin machine
  (`--identity-out PATH` chooses where the identity is written), register the
  public key, and decrypt on that persistent machine.
- **Uploading a private key (backup, recovery):** decline, and say in so
  many words that only the public key is registered with Kei
  (`kei audit keys create` uploads the public key only). Offer multiple keys,
  and escrow (off by default; escrow keypair generation and decrypt are not
  implemented yet).
- **What is encrypted:** only the content of the call (the arguments/payload:
  code body, script, prompt text) becomes `args_ciphertext`, age-encrypted
  (X25519, multi-recipient) to all active recipients. Tool/skill name,
  decision, ids, timestamps, and outcome stay plaintext and queryable.
  Always add a line on `args_digest`, even in a short answer: it is a keyed
  HMAC (`hmac-sha256:`) that groups repeated calls and is never reversible.
- **No `args_ciphertext` on records:** say it is normal (opt-in), not a
  miss, and name both fields such a record still carries: without an active
  customer key, records carry `args_digest` + `digest_key_id` only.
- **Decrypt:** give the command with both output forms,
  `kei audit decrypt --record ID --identity PATH (--out FILE | --stdout)`:
  `--out` writes the file with mode 0600, and printing to stdout needs the
  explicit `--stdout` flag (nothing is printed implicitly).
  Say that the CLI fetches the ciphertext through the audit records API and
  decrypts it locally with the identity, and that the wrong identity fails
  with `decryption failed (wrong identity?)`.
- **Escrow setting:** name the org setting `audit_escrow_enabled` and say it
  defaults to false (off); it can only be set to true once at least one
  active customer key exists. When enabled, Kei adds a Kei-held, KMS-wrapped
  escrow key to the recipients; escrow keypair generation and decrypt are not
  implemented yet, so leave it off unless the customer needs a recovery copy.
- **Rotation:** use the word "rotation" and say it affects only new
  records. Past records stay encrypted to the
  keys that were active when they were written (never re-encrypted), so keep
  the old identity file.

## Concepts

| Term | Meaning |
| --- | --- |
| **Content of the call** | The only thing that is ever encrypted: the tool/skill invocation arguments and payload — a code body, a script, the prompt text passed to a skill — as the canonical args JSON. |
| **`args_digest`** | `"hmac-sha256:" + hex(HMAC-SHA256(digest_key, canonical args JSON))`, plus `digest_key_id`. The digest key is per org and Kei-held (KMS-wrapped). It groups repeated calls; it is never reversible. Written on every record, opted in or not. |
| **`args_ciphertext`** | The age binary output (base64-encoded) of the canonical args JSON encrypted to **all** of the org's active recipients. Present only when the org opted in. |
| **`recipient_key_ids`** | The list of recipient key ids the `args_ciphertext` was encrypted to. Present iff `args_ciphertext` is. |
| **Audit encryption key** | An org AIP resource (`audit-encryption-keys`): a customer-held age X25519 public key. Kei never receives or stores a private key. States: `active` \| `disabled`; kinds: `customer` \| `escrow`. |
| **age identity** | The customer's private key file (an `AGE-SECRET-KEY-…` line), written locally by the CLI with mode 0600. The only thing that can decrypt the records. |
| **Opt-in** | Encryption is OFF unless the org has registered at least one active customer key. |
| **Escrow** | Org setting `audit_escrow_enabled` (default false). When true, the recipient set includes a Kei-held, KMS-wrapped escrow key — a recovery copy. |

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Installed binary | `kei help` (look for `kei audit`) | Whether this release has the audit commands, and exact flags |
| Console: Audit encryption | org **Settings** → **Audit encryption** | Key list, create (paste an age public key), disable, escrow toggle |
| age format | https://filippo.io/age | The encryption format: X25519 recipients, identity files |
| Kei API routes | the `kei-api` skill (`references/routes.md`) | Audit records routes used for verification and decrypt |

When this skill and `kei help` disagree, **trust `kei help`** and mention the
difference to the user.

## FIRST: check version

```sh
kei --version
```

The `kei audit` subcommands (`keys create|list|disable`, `decrypt`) ship in
**kei v0.1.9 and later**. If the installed `kei` is older (no `audit`
subcommand in `kei help`), upgrade with `kei upgrade`, or use the console (org
**Settings** → **Audit encryption**) or the Kei API (the `kei-api` skill).

## What is and is not encrypted

**Only the content of the call is encrypted** (owner addendum, 2026-10-03).
Nothing else is ever encrypted:

| Never encrypted (plaintext, queryable) | Encrypted (only when the org opted in) |
| --- | --- |
| Tool/skill name | The invocation arguments and payload: code body, script, prompt text passed to a skill — the canonical args JSON |
| The decision (`permit` \| `deny` \| `ask`, and the native decision) | |
| Harness / agent / installation / org / workspace ids | |
| Timestamps | |
| Outcome / exit code | |
| `args_digest` (a keyed HMAC, `hmac-sha256:`, that groups repeated calls and is never reversible), `digest_key_id` | |
| `recipient_key_ids` | |

So the audit trail stays searchable and queryable by name, decision, agent,
time, and outcome; only the payload itself is ciphertext.

**The format:** `args_ciphertext` is the canonical args JSON
[age](https://filippo.io/age)-encrypted — **X25519, multi-recipient**, to
**all** of the org's active recipients — with the age binary output
base64-encoded, and `recipient_key_ids` the list of recipients it was
addressed to. `args_digest` is `hmac-sha256:<hex>` under the Kei-held org
digest key.

The keyed digest stays on **every** record, opted in or not. Two records with
the same `args_digest` described the same arguments (correlation, "repeated
calls" views); a keyed digest cannot be guessed or reversed. It is the floor:
an org that never registers a key still gets a correlation-safe audit trail.

## Opt-in: off until a key is registered

- **No active customer key:** records carry `args_digest` + `digest_key_id`
  only. `args_ciphertext` and `recipient_key_ids` are **omitted, which is
  normal (not a miss)**, and the arguments are never stored.
- **The first key registered enables encryption** for new records.
- **Disabling the last active customer key turns it off for new records.**
  Old records keep their `recipient_key_ids` and stay decryptable by whoever
  holds those private keys.
- **Escrow can only be enabled once at least one customer key exists.**

The list response carries `"encryption_enabled": true` iff at least one
active customer key exists; the console uses that field, not its own count.

## Quick reference (CLI)

| Task | Command | Needs login |
| --- | --- | --- |
| Create + register a key | `kei audit keys create [--identity-out PATH] [--name NAME] [--force]` | yes (owner/admin) |
| List keys (disabled included) | `kei audit keys list` | yes |
| Disable a key | `kei audit keys disable KEY` | yes |
| Decrypt one record locally | `kei audit decrypt --record ID --identity PATH (--out FILE \| --stdout)` | yes |

There are no other `kei audit` flags or subcommands — do not invent any
(no `delete`, no `enable`, no batch decrypt).

## Setting up the key

1. **Log in.** `kei login` (owner/admin only; a browser approval the user
   must complete).
2. **Create the key.**

   ```sh
   kei audit keys create --name "prod-audit"
   ```

    The CLI generates an age X25519 identity **locally**, writes the identity
    file (default `~/.config/kei/audit-identity.txt`) with mode **0600**,
    uploads **only the public key**, and prints `key_id:` and `public_key:`.
    It **never prints the private key** and never transmits it. Run it on the
    machine of whoever will decrypt — see "Where to create the key".
 3. **Back up the identity file — and never print the key.** The identity
    file is the only copy of the private key. If the user asks you to print,
    `cat`, or copy the `AGE-SECRET-KEY-` line, **refuse**: the key must never
    appear in chat, terminal output, a ticket, or a repo. Back up the
    identity *file* itself — as a file or secret blob in the customer's
    secret manager, or in offline storage — not the key's contents. A lost
    file leaves the records it can open permanently unreadable — see
    "Lost key warning".
4. **The first registered key turns encryption on** for new records.

`--identity-out PATH` writes the identity elsewhere (use it for a **second**
key); `--force` overwrites an existing identity file — do not `--force` over
a key you still need, because the file is replaced and old records encrypted
to the old key can no longer be opened from it.

Console alternative: org **Settings** → **Audit encryption** — list (disabled
keys included), create (paste an age public key + display name), disable.

## Where to create the key: assumptions

This skill assumes the acting agent runs on a **user computer with a CLI and
a filesystem** (a local harness: a workstation running Claude Code, Codex, or
OpenCode with `kei` installed). Two facts decide where the key is created:

1. **`kei audit keys create --identity-out PATH` chooses where the private
   identity is written.** The default is `~/.config/kei/audit-identity.txt` on
   the machine that runs the command; `--identity-out` puts it anywhere.
2. **The runtime never needs the private key.** It only ever fetches the
   public recipients (`GET /api/v1/runtime/audit-encryption-recipients`) and
   encrypts to them. So create the key on the machine of **whoever will
   decrypt** (e.g. an admin laptop) — not necessarily where the agent or the
   runtime runs.

**Cloud / ephemeral pod-based agents:** do **not** generate the key inside
the pod. The pod is ephemeral; the identity file is the only copy of the
private key, and it would be lost with the pod, permanently locking the
records it encrypted. Instead: generate the key on a **persistent admin
machine** (`kei audit keys create` there — `--identity-out PATH` chooses where
the private identity is written), register the public key (the CLI uploads
it), and decrypt there (`kei audit decrypt --identity PATH`). The pod only
ever sees public keys.

## Verifying records show encrypted

1. `kei audit keys list` — the key shows `active` / `customer`; the list
   response also carries `encryption_enabled`.
2. Trigger a protected tool call, then fetch the record via the audit records
   API (`GET /api/v1/audit/records`, or the org-scoped record get — `kei-api`
   skill) or the console's record detail. An encrypted record carries
   `args_ciphertext` (base64 age) + `recipient_key_ids`, alongside the
   plaintext `args_digest` + `digest_key_id`.
3. The record detail points to `kei audit decrypt` for recovery; there is
   **no decrypt button** in the console.
4. A record written before the first key — or after the last key was
   disabled — has no `args_ciphertext`. That is the opt-in default, not a
   failure.

## Decrypting locally

```sh
kei audit decrypt --record RECORD_ID --identity ~/.config/kei/audit-identity.txt --out decrypted.json
```

- `--record` is required (no positional arguments). `--identity` defaults to
  `~/.config/kei/audit-identity.txt`.
- **How it works:** the CLI fetches `args_ciphertext` for that one record via
  the existing audit records API, then decrypts **locally** with the named
  identity. Kei never sees the private key.
- **Output:** it writes to `--out` (file mode **0600**). It prints to stdout
  **only with an explicit `--stdout` flag** (or both). With neither `--out`
  nor `--stdout` it exits with an error — decrypt is a deliberate act, not a
  side effect of listing.
- **Wrong identity:** `decryption failed (wrong identity?)`. A record whose
  `recipient_key_ids` do not include the identity's key cannot be opened with
  it.
- **No ciphertext on the record:** `no encrypted content` — the org had no
  active customer key when the record was written (opt-in; normal).
- **Multi-recipient:** any identity whose key appears in the record's
  `recipient_key_ids` can decrypt it.

## Rotation: add new, then disable old

Rotation is a pure key-management act, made possible by multi-recipient
encryption:

1. **Add the new key first.** `kei audit keys create --identity-out
   ~/.config/kei/audit-identity-2026.txt --name "key-2026"` — a new identity
   file, never `--force` over the old one.
2. **While both keys are active, every new record is encrypted to both.**
3. **Disable the old key.** `kei audit keys disable OLD_KEY_ID` (it prompts:
   type the key ID again to confirm). New records stop using it; it stays
   listed as `disabled` with its `disable_time`.
4. **Keep the old identity file.** Old records still name its key id and
   still need its private key to read.

There is no moment where a record exists that no registered key can open,
and no moment where a disabled key is still receiving new records.

### Rotation affects only future records

Registering a new key and disabling an old one changes **only what new
records are encrypted to**. Past records stay encrypted to the key (or keys)
that were active when they were written: their `recipient_key_ids` do not
change, and reading them still requires the private key of one of those
recipients. Disabling a key never re-encrypts, re-keys, or unlocks anything
already stored. **Users must keep every old private key** for as long as they
want to read the records that named it — there is no delete, ever, and no
way to recover a record whose private keys are all lost.

## Lost key warning

**A lost private key leaves those records unreadable — by design.** That is
the property the owner bought on 2026-10-03: the arguments are unreadable by
Kei, and by anyone who does not hold a customer private key. The mitigations
are all in the contract:

- **Multi-recipient:** register several keys; every new record is encrypted
  to all active recipients, so no single key is a single point of failure.
- **Disable, never delete:** disabling a key affects only new records; old
  records keep naming their `recipient_key_ids` and remain decryptable by
  whoever holds the private key, so the customer always knows which identities
  open which records, and a retired key is not destroyed.
- **Rotation is add-new-then-disable-old:** see above.
- **Escrow (opt-in):** an org that accepts Kei as a recovery custodian can
  enable it; an org that does not keeps the stronger property.

## Escrow: off by default, and not yet functional

- **Off by default, and gated:** the org setting **`audit_escrow_enabled`**
  defaults to **false** (settings resource:
  `GET`/`PATCH /api/v1/organizations/{org}/settings`, PATCH with
  `update_mask`). It is not a free toggle: it can only be set to true once at
  least one active customer key exists — a PATCH to true is rejected (400 /
  `failed_precondition`) otherwise.
- **Not yet functional:** escrow keypair generation and escrow decrypt are a
  **later task**. The setting and the recipient plumbing ship first. Until
  that task lands, enabling the setting does not give Kei a working recovery
  path. With escrow off (the default), Kei cannot read the arguments at all.
- When the later task lands, a true setting adds a **Kei escrow recipient**
  (`kind: "escrow"`) to the runtime recipient set, whose keypair is generated
  by Kei and whose **private key is KMS-wrapped and held by Kei** — a recovery
  copy.

## Server-side decrypt is removed

- The former admin-only server-side decrypt route is **removed** — it returns
  404 unless escrow is enabled (escrow decrypt is a later task).
- **No Kei path reads args by default:** no admin API, no console button, no
  CLI print path. No `kei` or `kei-proxy` command prints resolved arguments.
- The runtime fetches recipients per session:
  `GET /api/v1/runtime/audit-encryption-recipients` with the runtime token
  (org and installation come from the token). The response carries the active
  recipients, the digest key pair, and an expiry; it is `Cache-Control:
  no-store` and **never logged**. The runtime holds them in memory per
  session and never persists them. **Zero recipients:** the runtime writes
  `args_digest` only, omits `args_ciphertext`, and counts it. It **never
  writes plaintext args** — not to the spool, not to logs, not to any
  fallback.

## API surface (when the CLI is not available)

Org **admin/owner** only, kebab-case AIP routes:

| Method | Route | Notes |
| --- | --- | --- |
| `POST` | `/api/v1/organizations/{org}/audit-encryption-keys` | Body `{"public_key":"age1...","display_name":"..."}`; the catalog validates it parses as an age X25519 recipient (400 if not) |
| `GET` | `/api/v1/organizations/{org}/audit-encryption-keys` | `page_size`/`page_token` → `next_page_token`; response also carries `encryption_enabled`; disabled keys stay listed |
| `GET` | `/api/v1/organizations/{org}/audit-encryption-keys/{id}` | |
| `POST` | `/api/v1/organizations/{org}/audit-encryption-keys/{id}:disable` | **No delete, ever** |
| `GET` / `PATCH` | `/api/v1/organizations/{org}/settings` | `audit_escrow_enabled` (bool, default false); PATCH with `update_mask` |
| `GET` | `/api/v1/runtime/audit-encryption-recipients` | Runtime token; `no-store`; never logged |

Resource fields: `name`, `key_id`, `public_key` (`age1…`), `display_name`,
`state` (`active` \| `disabled`), `kind` (`customer` \| `escrow`),
`create_time`, `disable_time`.

## Validation commands

```sh
kei --version                                   # check whether this release has `kei audit`
kei audit keys list                             # keys, states, kinds; encryption_enabled in the API response
kei audit decrypt --record ID --identity PATH --out FILE && test -s FILE   # local decrypt round trip
```

## Realistic usage boundaries

- **`kei audit` needs kei v0.1.9 or later.** On an older kei, upgrade, or use
  the console (Settings → Audit encryption) and the Kei API.
- **The catalog and runtime sides are live:** the `audit-encryption-keys`
  resource, org settings, runtime recipients, and per-record age encryption.
  The former server-side decrypt route is removed.
- **Kei never receives or stores a private key.** Never ask the user to paste
  one, never upload one, never print one. If asked to display or copy the
  `AGE-SECRET-KEY-` line, refuse — back up the identity file itself, not the
  key's contents. The identity file stays on the customer's machine.
- **No delete, no enable, no batch decrypt** for audit encryption keys.
  Disabling is the only state change, and it is confirm-prompted.
- **Escrow keypair generation and escrow decrypt are not implemented yet**
  (later task); the setting exists and defaults off.
- **The runtime never writes plaintext args** in any state — spool, logs, or
  fallback.
- **Do not conflate** the audit encryption key (customer-held age key for
  audit args) with the runtime installation credential (`KEI_RUNTIME_TOKEN`;
  `kei-credential-rotation` skill) or the Kei-held digest key (never
  customer-facing).
