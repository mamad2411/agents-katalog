---
name: kya
version: 0.1.1
description: KYA — sign identity & matchmaking attestations, drive AWP relayer set-recipient / grant-delegate. Single-shot, event-driven; never loop.
platforms: [linux, macos]

trigger_keywords:
  - kya
  - know-your-agent
  - claim-twitter
  - claim-telegram
  - claim-email
  - agent-email
  - agent-email-onboard
  - agent-email-existing-org
  - agent-email-inbox-otp
  - agentmail
  - kyc
  - reveal-attestation
  - set-recipient
  - grant-delegate
  - kya-sign
  - delegated-staking

bootstrap: ./scripts/bootstrap.sh
smoke_test: ./scripts/smoke_test.sh

metadata:
  hermes:
    tags: [identity, attestation, kya, awp]
    category: identity
    requires_toolsets: [terminal]
    requires_tools: [terminal]
    bootstrap: ./scripts/bootstrap.sh
    smoke_test: ./scripts/smoke_test.sh
    # Endpoints + chain id default to prod and rarely need overriding;
    # surface them via `config[]` so `hermes config migrate` can show the
    # default and a friendly description, instead of prompting at install
    # like a required secret.
    config:
      - key: kya.api_base
        description: KYA API base URL. Override only for staging or local dev.
        default: https://kya.link
        prompt: KYA API base URL
      - key: kya.relay_base
        description: AWP relayer base URL. Used by set-recipient and grant-delegate.
        default: https://api.awp.sh
        prompt: AWP relayer base URL
      - key: kya.base_rpc_url
        description: Base mainnet RPC URL. Used to read AWPRegistry.isRegistered / nonces.
        default: https://mainnet.base.org
        prompt: Base mainnet RPC URL
      - key: kya.chain_id
        description: EIP-712 chain id. 8453 = Base mainnet.
        default: "8453"
        prompt: Chain ID
    # Only the wallet session token has secret semantics + no default —
    # keep it as a real env var so Hermes prompts (with TTY) or points
    # the user at `~/.hermes/.env` (no TTY).
    required_environment_variables:
      - name: AWP_WALLET_TOKEN
        prompt: awp-wallet session token
        help: Only legacy awp-wallet (<v0.17) needs this. Newer versions auto-unlock; leave blank.
        required_for: legacy awp-wallet (<v0.17) only — leave blank for newer wallets

  openclaw:
    bootstrap: ./scripts/bootstrap.sh
    smoke_test: ./scripts/smoke_test.sh
    os: [linux, darwin]
    requires:
      bins:
        - kya-agent
      anyBins:
        - awp-wallet
      env:
        - KYA_API_BASE
    # `envVars[]` mirrors `requires.env` for ClawHub's declaration-vs-code
    # scanner — every variable kya-agent reads is listed here so the
    # scanner doesn't flag drift. None of these are KYA-issued secrets;
    # all have prod defaults except AWP_WALLET_TOKEN (legacy-only).
    envVars:
      - name: KYA_API_BASE
        required: false
        description: KYA API base URL (default https://kya.link)
      - name: AWP_RELAY_BASE
        required: false
        description: AWP relayer base URL (default https://api.awp.sh)
      - name: BASE_RPC_URL
        required: false
        description: Base RPC URL (default https://mainnet.base.org)
      - name: KYA_CHAIN_ID
        required: false
        description: Chain id (default 8453 = Base mainnet)
      - name: AWP_WALLET_TOKEN
        required: false
        description: awp-wallet session token; only legacy awp-wallet (<v0.17) needs this
      - name: AGENTMAIL_API_KEY
        required: false
        description: Optional advanced AgentMail inbox key; used only when agent-email-inbox-otp is run with --auto-read
      - name: AGENTMAIL_INBOX_ID
        required: false
        description: Optional AgentMail inbox_id for --auto-read
      - name: AGENTMAIL_API_BASE
        required: false
        description: AgentMail API base URL (default https://api.agentmail.to)
      - name: KYA_AGENTMAIL_KEY_DIR
        required: false
        description: Local directory where agent-email-onboard saves AgentMail key JSON files
    emoji: "🪪"
    homepage: https://github.com/awp-worknet/kya-skill
    # `kind: download` is the OpenClaw-supported install kind; it pulls
    # the prebuilt kya-agent binary from the GitHub Release matching
    # this skill version. Falls back to `bootstrap.sh` for environments
    # where the macOS Skills installer doesn't run (it itself just
    # wraps `install.sh` which is the same artifact).
    install:
      - kind: download
        url: https://github.com/awp-worknet/kya-skill/releases/latest/download/install.sh
        bins: [kya-agent]
        label: Install kya-agent prebuilt binary
---

# KYA — Know Your Agent

You are an AI agent driving KYA on behalf of an agent owner. Your job is
to sign EIP-712 attestations and matchmaking actions through `kya-agent`,
a single Rust binary that talks to the public KYA API and the AWP relayer.

## Rules — read these first

1. **ALL operations go through `kya-agent`.** Never re-implement the flow
   in bash, python, curl, or any other tool. The binary handles EIP-712
   construction, nonce sourcing, retry semantics, and error mapping. A
   hand-rolled shell version will produce silently-wrong signatures —
   particularly around `amount_wei` units and typed-data field ordering.
2. **Never modify files on disk.** Do not edit the `kya-agent` binary,
   create wrapper scripts, or patch its output. If a command fails, read
   `error.code` and follow the recovery table below.
3. **Never expose secrets.** Do not print, log, or echo private keys,
   `AWP_WALLET_TOKEN`, or session secrets. Signing is delegated to
   `awp-wallet` — keys never enter `kya-agent`'s memory.
4. **Follow `_internal.next_command` exactly.** Every JSON result includes
   `_internal.next_action` and (when applicable) `_internal.next_command`.
   Run the suggested command verbatim. Do not paraphrase, reorder flags,
   or insert your own.
5. **One signing flow per invocation.** `kya-agent` is event-driven, not
   a daemon. Do not loop. Do not poll outside the binary's own polling.
6. **Never broadcast a transaction yourself.** `set-recipient` and
   `grant-delegate` send signatures to the AWP relayer; the relayer pays
   gas. The agent EOA needs zero ETH for any flow this skill handles.
7. **When in doubt, run `kya-agent preflight`.** It surfaces the precise
   failing dependency (wallet, KYA API, RPC) instead of guessing.
8. **Magic links → `kya-agent open <url>`.** When KYA web hands the user a
   `kya-sign://...` URL, do not translate query params into flags
   manually. The binary parses and dispatches; that's its only job.
9. **AWP registration is mandatory.** KYA is a subnet of AWP. If
   `kya-agent preflight` returns `AWP_NOT_REGISTERED`, do **not** attempt
   any KYA flow — hand off to [awp-skill](https://github.com/awp-core/awp-skill)
   for free gasless onboarding (one `setRecipient(self)` via relay) and
   only resume KYA after preflight returns `ready`.

## Running on Hermes via messaging surfaces (Telegram / Discord / Slack)

### Installing the skill from inside a Hermes session

Hermes-from-messaging runs the skill loop **inside** a long-running
Hermes daemon — the `hermes` CLI is **not on PATH** of the agent's
sandbox. Use the in-loop tool instead:

```
skill_manage create   # register the cloned kya-skill repo
skill_view kya        # verify it's loaded
```

`hermes skills install <repo>` is the **operator-side** install — it
works only from the host shell where the Hermes daemon was launched.
Inside the agent loop, always go through `skill_manage`.

### Running on the install.sh side

The `kya-agent` binary itself is downloaded by `install.sh` from
GitHub Releases. On minimal sandboxes (Hermes containers often lack
`curl` and `wget`), `install.sh` falls back to `python3` then `node`,
all of which follow HTTPS 302 redirects properly. If you find
yourself improvising another download path, that's a bug — open an
issue and use the existing fallback chain instead.

### What changes from the canonical journey

Hermes users frequently reach this skill from a messaging gateway with
**no TTY and no clickable links**. Adapt the canonical journey:

- The handoff URL produced by `claim-twitter` / `claim-telegram` /
  `claim-email` / `kyc` must be **emitted as plain text** for the owner
  to copy into their browser. Do not attempt to "open" the URL — the
  agent has no display.
- Any [STOP] that says "tell the owner X" is a chat message you send
  back over the messaging surface, then you stop and wait for the
  owner's next message before resuming.
- Secrets (`AWP_WALLET_TOKEN`) are not collected over messaging — they
  must already be in `~/.hermes/.env` or the user's local
  `awp-wallet`. If they're missing, surface the SKILL.md error-table
  text verbatim instead of asking the user to type the secret.

**This skill is event-driven; never schedule it via `hermes cron`.**
Each KYA flow is a one-shot human-in-the-loop interaction, not a
recurring task. If a user tries to wire `kya-agent claim-twitter` or
`kya-agent set-recipient` to cron, refuse and explain — SKILL.md Rule
#5 is the authoritative line ("One signing flow per invocation. KYA is
event-driven, not a daemon. Do not loop.").

## Running on OpenClaw

OpenClaw users typically reach this skill from the desktop app's
chat — TTY available, browser openable. The canonical journey works
without adaptation; just a couple of OpenClaw-specific notes:

- **Never wire kya-agent to OpenClaw cron.** OpenClaw has built-in
  scheduled invocations, but every KYA flow is one-shot,
  human-in-the-loop. Restating SKILL.md Rule #5 because the runtime
  won't stop a user from doing this themselves.
- Secrets are injected via the OpenClaw Skills config
  (`skills.entries.kya.env`) — don't ask the user to type
  `AWP_WALLET_TOKEN` in chat. If it's missing, surface the
  preflight error and tell them to set it in OpenClaw's Skills
  preferences.
- `kya-agent open <kya-sign://...>` works the same; OpenClaw can
  open the resolved URL with the OS default browser if available.

## How agents discover this skill

KYA is registered on the AWP network as worknet **`845300000012`**.
AWP-aware agents typically arrive here through the standard discovery
path — they ask the AWP API for the worknet's `skillsURI`:

```sh
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"worknets.getSkills","params":{"worknetId":"845300000012"},"id":1}' \
  https://api.awp.sh/v2
# → { "result": { "skillsURI": "https://github.com/awp-worknet/kya-skill" } }
```

That URI always points at this repository's `main` branch, which is
where install.sh, SKILL.md, and the kya-agent binary releases live.
Agents reaching KYA from another worknet's skill (e.g. predict bouncing
the user here for delegated staking) follow the same path: read
`worknets.getSkills(845300000012)` → install kya-skill → run
`kya-agent preflight`.

## Prerequisites — AWP first

KYA is a subnet of the AWP network. Every flow assumes the agent EOA is
already registered on AWPRegistry. Two paths land here:

- ✅ **Came from awp-skill / awp.pro** (most users). Registration is
  done; `preflight` passes silently.
- ❌ **KYA-first**. `preflight` returns `AWP_NOT_REGISTERED` with
  `_internal.handoff.skill = "awp"`. Install awp-skill, run its
  onboarding (free, gasless), then re-run preflight.

`kya-agent` does **not** implement AWP onboarding itself — that lives
in awp-skill. Single source of truth, no duplication.

## Canonical journey — "I want delegated staking"

This is the dominant reason owners arrive at KYA: another worknet's
skill (predict, community, …) checked their stake, found it
insufficient, and bounced them here for KYA's delegated-staking service.
KYA stakes on their behalf if they pass at least one verification.

**Walk owners through these steps in order. Stop at every [STOP].**

### Step 0 — preflight

```sh
kya-agent preflight
```

- `_internal.next_action = "ready"` → continue to Step 1.
- `_internal.next_action = "register_on_awp"` → **[STOP]**: bounce to
  awp-skill onboarding (see Prerequisites). Resume only when preflight
  returns ready.
- Any other failure → surface `error.code` per the recovery table.

### Step 1 — query existing attestations

```sh
kya-agent attestations
```

Branches on `_internal.next_action`:

- **`ready_for_delegated_staking`** (active `twitter_claim`) → **skip to
  Step 3.** Don't ask the owner to verify again — they already did.
- **`choose_verification`** (no active attestation) → continue to Step 2.

### Step 2 — owner picks a verification path

The `attestations` response carries `_internal.options` — for delegated
staking this is currently X/Twitter only. **[STOP]** — present it to the
owner before continuing.

```
You don't have active X verification yet. Complete:
  A) Twitter (X) — public tweet

Telegram, Email, and KYC attestations may exist for other KYA surfaces,
but they do not unlock delegated staking.
```

Run the matching command (the binary's `command` field). For Twitter the
binary returns a `handoff_url`:

```sh
kya-agent claim-twitter
# stdout JSON contains EXACTLY:
#   handoff_url:           "https://kya.link/verify/social/claim#agent=…&sig=…"
#   instructions_for_agent: "Relay handoff_url verbatim … do NOT ask owner to publish/paste"
#   _internal.next_action:  "browser_handoff_then_verify"
#   _internal.next_command: "kya-agent attestations"
#
# Note: the JSON deliberately does NOT include claim_text, claim_nonce,
# or expires_at — those are KYA web's concern. If you find yourself
# wanting to show claim_text to the owner, you've misread the contract:
# KYA web shows it inside the browser flow once they open handoff_url.
```

**[STOP]** — give the **handoff_url** verbatim to the owner:

> Open this link in your browser: `<handoff_url>`. KYA web walks you
> through publishing the tweet/post and writes the attestation itself.
> You do NOT need to paste any URL back to me. When KYA web confirms
> done, tell me and I'll verify.

After the owner says done, run `kya-agent attestations`. If the new
attestation isn't active, **[STOP]** and ask the owner to re-check the
browser flow before retrying.

**DO NOT** ask the owner to "paste the tweet URL" / "send me the
published link" / "give me the X URL". The web-driven flow makes
that step unnecessary — KYA web handles the URL collection.
The signatures are baked into the handoff URL fragment; KYA web
posts the claim itself. If you find yourself drafting "send me the
tweet link", you've drifted from this skill — re-read the
**handoff_url** field of the JSON and present THAT instead.

**DO NOT** invent your own variant of the claim text. Copy
`claim_text` verbatim from the binary's stdout if the owner asks
what to publish; the text is signed and KYA web will reject any
deviation.

For Email and KYC, the same `next_command: kya-agent attestations`
pattern applies after the in-app verification completes.

### Step 3 — execute delegated staking

**[STOP]** — confirm both the target WorkNet and the amount. The WorkNet
must be explicit. If the owner came from KYA web, use the `worknet_id`
embedded in the `kya-sign://set-recipient?...` magic link. If you do not
have a WorkNet id, **stop and ask the owner to choose one in KYA web**;
do not default to KYA's own WorkNet.

```
About to request delegated staking:
  agent      0xabc...
  worknet    <worknet_id>   ← explicit target WorkNet selected by the owner
  amount     <N> AWP        ← owner picks; per-agent cap is 10 000 AWP
  requester  0xowner...     ← optional owner wallet for the reward share

This will:
  1. Sign AWPRegistry.SetRecipient → relay broadcasts (gasless, no ETH).
  2. Sign KYA Action(delegated_staking_request) → KYA stakes from its pool.

Proceed?
```

After confirmation:

```sh
kya-agent set-recipient --worknet <worknet_id> --amount <N> --requester <owner_wallet>
```

For this full delegated-staking path, `kya-agent` intentionally fetches
the KYA deposit address without `worknet_id`. The `--amount` value is
carried with `--worknet` only in Stage 2 (`delegated_staking_request`).
If the owner wallet is known, pass it as `--requester`; the binary sends
it to KYA as `requester_address` so KYA can route the owner reward share
without falling back to the agent EOA.
The legacy deposit-address `worknet_id` path means "enter awaiting_match"
and can trigger the fixed admission-threshold allocation instead of the
owner's requested amount, so the binary deliberately omits worknet from
the Stage 1 deposit-address lookup when `--amount` is present.

The binary re-checks X/Twitter verification (defense-in-depth — the
server gates on this too) and, if green, runs both stages and polls for
terminal status.

### Step 4 — terminal status

| `_internal.next_action` | Action |
|---|---|
| `ready` | Stage 1 + stage 2 both landed cleanly. Report `tx_hash` and `staking_request.request.matched_allocation_id` to the owner. Done. |
| `staking_pending` | Stage 1 confirmed; KYA's pool stake didn't land before the timeout. **[STOP]**: tell owner the stake will land later automatically (server-side issue, not theirs to fix), and that re-running `kya-agent set-recipient` would post a duplicate. Re-check later with the suggested next_command (`kya-agent staking-status --request-id <id>`). |
| terminal `failed` with `failed_reason: per_agent_cap_exceeded` | **[STOP]**: this agent already has ≥10 000 AWP delegated-staked. Cannot stack more. |
| `no_capacity` | **[STOP]**: tell owner no provider has free capacity right now. Surface verbatim — do not retry in a tight loop. |
| terminal `failed` (other) | **[STOP]**: surface `failed_reason` verbatim. |

For repeat / additive delegated staking (same agent, more AWP) or new
agents: same journey. Step 1 will skip to Step 3 if verification is
already active. The 10 000 AWP per-agent cap is enforced server-side.

## Quick start

```sh
# Install kya-agent (pre-built binary, no Rust toolchain required)
curl -fsSL https://raw.githubusercontent.com/awp-worknet/kya-skill/main/install.sh | sh

# Sanity check
kya-agent preflight
```

`preflight` prints `_internal.next_action: ready` when everything is in
place. Otherwise it returns an `error.code` listed below.

## Magic links (canonical entry from KYA web)

KYA web encodes any user intent as a `kya-sign://...` URL. Always feed
the URL to `kya-agent open` — let the binary dispatch:

```sh
kya-agent open "kya-sign://reveal?api=https://kya.link&type=email_claim"
```

| URL form | Resolves to |
|---|---|
| `kya-sign://twitter-claim?api=<base>` | `claim-twitter` (handoff URL) |
| `kya-sign://telegram-claim?api=<base>` | `claim-telegram` (handoff URL) |
| `kya-sign://email-claim?api=<base>` | `claim-email` (prompts for email + code) |
| `kya-sign://email-claim?api=<base>&email=<addr>` | `claim-email --email <addr>` |
| `kya-sign://agent-email-onboard?api=<base>` | `agent-email-onboard` (prompts for human-email + username + OTP). Writes `agent_email_claim` with `proof_strength=signup_only`. |
| `kya-sign://agent-email-onboard?api=<base>&human_email=<addr>&username=<name>` | TTY: `agent-email-onboard --human-email <addr> --username <name>`. Non-TTY: `agent-email-onboard --human-email <addr> --username <name> --prepare-only`, then run the returned `_internal.next_command` with the OTP. |
| `kya-sign://agent-email-existing-org?api=<base>` | Advanced recovery only: `agent-email-existing-org` prompts for an existing AgentMail org API key + username + inbox OTP. Use only when the user must create a new inbox under an existing org. |
| `kya-sign://agent-email-existing-org?api=<base>&username=<name>` | Advanced recovery only: `agent-email-existing-org --username <name>`; pass `--agentmail-api-key` or set `AGENTMAIL_API_KEY`. Non-TTY can use `--prepare-only`, then run the returned `_internal.next_command` with the OTP. |
| `kya-sign://agent-email-inbox-otp?api=<base>` | `agent-email-inbox-otp` (prompts for inbox + OTP). Upserts `agent_email_claim` to `proof_strength=inbox_control`. Do not ask the user for an AgentMail API key. |
| `kya-sign://agent-email-inbox-otp?api=<base>&inbox=<addr>@agentmail.to` | `agent-email-inbox-otp --inbox-email <addr>` (`inbox_email` is also accepted). Non-TTY returns `_internal.next_command`; run that exact command with the OTP. If entering the code manually, include `--code <OTP>` on the confirm run so it confirms the existing challenge instead of preparing a new OTP. |
| `kya-sign://kyc?api=<base>&owner=0x...` | `kyc --owner 0x...` |
| `kya-sign://reveal?api=<base>` | `reveal` (all types) |
| `kya-sign://reveal?api=<base>&type=<t>` | `reveal --type <t>` |
| `kya-sign://set-recipient?api=<base>` | `set-recipient` (stage 1 only — point recipient at KYA deposit) |
| `kya-sign://set-recipient?api=<base>&worknet_id=<id>&amount=<awp>&requester=0x...` | `set-recipient --worknet <id> --amount <awp> --requester 0x...` (full delegated-staking; `requester_address` and `owner` aliases are also accepted) |
| `kya-sign://set-recipient?api=<base>&worknet=<id>&amount=<awp>` | same as above; legacy alias for `worknet_id` |
| `kya-sign://grant-delegate` | `grant-delegate` |
| `kya-sign://sign?clip=1` | `sign --from-clipboard` |

Use `kya-agent open --dry-run <url>` if the user wants to see the
dispatched command before it runs.

## Subcommand reference

| Subcommand | Purpose |
|---|---|
| `preflight` | Self-check (awp-wallet, KYA reachable, RPC reachable, AWP registration). Run first. |
| `bootstrap` | First-run alias of `preflight` plus an onboarding hint. |
| `smoke-test` | Non-destructive probe — never signs, never POSTs. CI-safe. |
| `open <url>` | Parse `kya-sign://...` and dispatch. Use `--dry-run` to preview. |
| `attestations` | List active attestations + delegated-staking eligibility. Step 1 of the canonical journey. |
| `claim-twitter` | Sign locally, emit a `kya.link/verify/social/claim#…` handoff URL. **Web-driven only** — owner opens the URL, KYA web takes care of the tweet + claim POST. Agent must NOT ask the owner to paste the tweet URL back. |
| `claim-telegram` | Same shape as `claim-twitter`, public-channel only. |
| `claim-email` | Bind an email. Two signs sandwich a 6-digit code. TTY prompts; piped requires `--email --code`. |
| `agent-email-onboard` | Create a new `*@agentmail.to` inbox through KYA's AgentMail proxy. Two signs sandwich the AgentMail OTP. TTY prompts; piped can either pass `--human-email --username --code` or use `--prepare-only` followed by `--state <file> --code <OTP>`. After confirm, the AgentMail inbox key is saved locally and the output strongly warns the owner to keep that file for future `inbox_control` upgrades. |
| `agent-email-existing-org` | Advanced recovery path. Uses an org API key once to create a new inbox + inbox-scoped key, sends a KYA OTP to the new inbox, then confirms `proof_strength=inbox_control`. Do not use it for the normal web `agent-email-inbox-otp` magic link. |
| `agent-email-inbox-otp` | Prove control of an existing `*@agentmail.to` inbox. Two signs sandwich a KYA OTP. Default TTY flow: KYA sends the OTP, the user reads the AgentMail inbox, and pastes it at the prompt. Non-TTY flow: first run `--prepare-only` or the magic link command, then run the returned `--state <file> --code <OTP>` command. Supplying `--code` confirms an existing challenge without preparing a new OTP. Optional local-only auto-read requires `--auto-read` plus saved credentials; never ask the user for an API key just to finish the web flow. |
| `kyc` | Sign `KycInit`, create a Didit session, return verification URL, optionally poll until terminal. |
| `reveal` | Off-chain. Sign `Action(attestation_reveal)`, get unredacted metadata. `--type email_claim/kyc/twitter_claim/telegram_claim/staking`. |
| `set-recipient` | Stage 1: gasless `AWPRegistry.setRecipient` via relayer. Stage 2 (with `--amount`): KYA `delegated_staking_request`. Pre-checks X/Twitter attestation. |
| `staking-status` | Re-check a delegated-staking request's status (use after `set-recipient` returns `staking_pending`). |
| `grant-delegate` | Provider side: authorize `KyaAllocatorProxy` to allocate on your behalf, gasless via relayer. |
| `sign` | Generic EIP-712 signer for ad-hoc KYA / AWPRegistry payloads. `--from-file` / `--from-clipboard` / stdin. |
| `sign-action` | Single-shot KYA `Action` / `KycInit` signer for the wizard manual-paste UX. |

Every subcommand emits a single-line JSON result on stdout (with
`_internal.next_action` and optional `_internal.next_command`) and
streams progress on stderr as NDJSON `step` / `info` lines.

## Error codes → recovery actions

| `error.code` | Action |
|---|---|
| `AWP_NOT_REGISTERED` | Agent EOA isn't on AWPRegistry yet. KYA is a subnet of AWP — registration is mandatory. Hand off to [awp-skill](https://github.com/awp-core/awp-skill) onboarding (free, gasless). After it lands, re-run `kya-agent preflight`. |
| `WALLET_NOT_CONFIGURED` | `awp-wallet receive` to check; `awp-wallet init` only if no wallet exists. **Never re-init an existing wallet.** |
| `WALLET_LOCKED` | Re-run; the binary auto-unlocks. If it still fails: `awp-wallet unlock --scope transfer --duration 3600` and retry. |
| `AGENT_MISMATCH` | `awp-wallet wallets`, find the right profile, `export AWP_AGENT_ID=<id>` (or pass `--agent-id`), retry. |
| `TIMESTAMP_OUT_OF_RANGE` / `INVALID_SIGNATURE` | Local clock drift. `sudo sntp -sS time.apple.com` (macOS) / `w32tm /resync` (Windows) / `chronyc makestep` (Linux). Retry. |
| `EMAIL_INVALID` | Ask the user for a syntactically valid email and re-run. |
| `EMAIL_CODE_INVALID` | For human email, re-read the inbox and re-run `kya-agent claim-email --email <addr> --code <CODE>`. For `agent-email-inbox-otp`, do not start a fresh prepare unless you need a new OTP; use the returned `--state <file> --code <OTP>` command with the latest code from the same prepared run. |
| `EMAIL_MAX_ATTEMPTS` | 5 wrong codes — restart with a fresh `kya-agent claim-email`. |
| `EMAIL_RESEND_COOLDOWN` | Wait ~60 s and retry. |
| `AGENT_EMAIL_FEATURE_OFF` | Agent-email is disabled on this deployment. Surface verbatim; do not retry. |
| `AGENTMAIL_ORGANIZATION_EXISTS` | The human email already has an AgentMail organization. First ask whether the target `*@agentmail.to` inbox already exists; if yes, run `agent-email-inbox-otp --inbox-email <addr>` and ask the user to paste the OTP from that inbox. Use `agent-email-existing-org --username <name> --agentmail-api-key <key>` only if they explicitly need to create a new inbox under the existing organization and have the org key. |
| `AGENTMAIL_API_KEY_INVALID` | Only applies to the advanced `agent-email-existing-org` recovery path. Ask for a valid AgentMail organization API key from the AgentMail console, or fall back to `agent-email-inbox-otp` if the inbox already exists. |
| `AGENTMAIL_SIGNUP_DEDUP` | That human email recently created or attempted an AgentMail inbox for another agent. Use `agent-email-inbox-otp` if the inbox already exists. |
| `AGENTMAIL_SIGNUP_INVALID_USERNAME` | Pick a 3-32 char lowercase `[a-z0-9-]` username that does not start or end with `-`. |
| `AGENTMAIL_PROVIDER_UNAVAILABLE` | AgentMail provider is unavailable. Surface verbatim and retry later. |
| `NOT_VERIFIED` | `set-recipient --amount` requires X/Twitter verification first. Run `kya-agent claim-twitter`. |
| `PER_AGENT_CAP_EXCEEDED` | Agent already has ≥10 000 AWP delegated-staked. Cannot stack more. |
| `NO_CAPACITY` | No provider capacity right now. Surface verbatim — do not retry in a tight loop. |
| `STAKING_REQUEST_FAILED` | Read `failed_reason` and surface it verbatim. Do not retry blindly. |
| `RELAY_TX_REVERTED` | Check `tx_hash` on basescan. Usually stale nonce — just re-run; the binary re-reads `AWPRegistry.nonces(agent)`. |
| `KYA_UNREACHABLE` | `curl $KYA_API_BASE/api/healthz` to sanity-check. |
| `RPC_UNREACHABLE` | Set `BASE_RPC_URL` to a working endpoint and retry. |
| `INPUT_REQUIRED` | Non-TTY invocation missing a required flag. Re-run with the flag the message asks for (e.g. `--email`, `--code`). |
| `MAGIC_LINK_INVALID` | Check the link is `kya-sign://...` and a known flow. |

For any error not in this table, surface `error.message` verbatim to the
user. Do not retry the same call in a tight loop hoping for a different
outcome.

## Pitfalls

- **Clock skew is the #1 cause of `INVALID_SIGNATURE`.** KYA accepts ±60 s
  future / 300 s past. If the user's clock is off, every sign attempt
  will fail until they resync — re-trying without a resync is futile.
- **`set-recipient --amount` requires X/Twitter verification first.** The
  binary pre-checks the agent has an active `twitter_claim` attestation
  before signing stage 1, so the user sees a clean "go run claim-twitter"
  instead of burning a setRecipient tx that the server would then reject.
- **`reveal` is off-chain.** It signs an `Action(attestation_reveal)` to
  authenticate the owner, but KYA writes nothing — only consumes the
  nonce and returns one unredacted response. Re-run for a fresh view.
- **Per-agent cap is 10 000 AWP across delegated stakers.** Re-running
  `set-recipient --amount` won't bypass it; the cap is enforced server-side
  at match time.
- **Do not lose the AgentMail inbox key.** `agent-email-onboard` creates a
  local key file after confirm (override directory with
  `KYA_AGENTMAIL_KEY_DIR`). Do not print, paste, or commit the key. Without
  that key, the agent cannot automatically read future OTPs sent to its
  `*@agentmail.to` inbox. Manual OTP entry still works.
- **AgentMail auto-read is opt-in and local-only.** By default,
  `agent-email-inbox-otp` asks the user to open the AgentMail inbox and paste
  the 6-digit code. With `--auto-read`, it calls
  AgentMail's HTTP API directly (`/v0/inboxes/{inbox_id}/messages`) using
  the saved key file, `--key-file`, or `AGENTMAIL_API_KEY` plus optional
  `AGENTMAIL_INBOX_ID`. Do not ask the user for an API key unless they
  explicitly requested auto-read or advanced existing-org recovery.
- **`set-recipient --amount` requires `--worknet`.** The binary omits
  worknet only from the Stage 1 deposit-address lookup; it still sends the
  explicit WorkNet id in Stage 2 (`delegated_staking_request`). If the
  magic link lacks `worknet_id`, stop and ask the owner to choose the
  target WorkNet in KYA web.
- **Pass `--requester` when the owner wallet is known.** KYA accepts this
  as `requester_address` on the delegated-staking request and uses it for
  owner reward routing. Omitting it keeps legacy behavior and lets KYA
  fall back to its server-side owner/agent resolution chain.
- **Telegram claim is public-channel only** (`t.me/<channel>/<msg_id>`).
  KYA fetches the public web preview; private DMs and unlisted groups
  cannot be verified.

## Security

- `kya-agent` never reads or writes a private key. Signing is delegated
  to `awp-wallet sign-typed-data`.
- Two domain shapes are signed — both pinned in `src/eip712.rs`:
  - `domain.name = "KYA"`, `primaryType ∈ {Action, KycInit}` — off-chain.
  - `domain.name = "AWPRegistry"`, `primaryType ∈ {SetRecipient, GrantDelegate}` —
    POSTed to AWP relayer; relayer broadcasts on Base.
- The binary never broadcasts a transaction itself. Network egress is
  limited to the configured KYA, relay, and RPC endpoints.
- Source: https://github.com/awp-worknet/kya-skill — MIT, public.
  Releases are built from a tagged commit via GitHub Actions; the
  SHA256 of each binary is published in the release notes.
