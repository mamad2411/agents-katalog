---
name: moss-wallet-cli
description: Use the MegaETH Wallet CLI to connect a MegaETH passkey wallet, create/manage scoped delegated session keys, inspect permissions, and use those keys for read-only calls, transfers, and relay-backed execution on MegaETH.
---

# MegaETH Wallet CLI

Use this skill when an agent needs to operate a local MegaETH wallet through
`mega moss` commands.

## Mental Model

MegaETH Wallet CLI is not a root wallet or passkey manager. It is a local tool
for creating, managing, and using scoped delegated session keys for a MegaETH
wallet account.

- The wallet account is an EVM address on MegaETH controlled by the user's
  passkey wallet at `account.megaeth.com`.
- Commands default to mainnet. Add `--network testnet` when the user explicitly
  asks for testnet; local profiles are separate per network.
- `mega moss login` connects this CLI install to that wallet account and
  stores an account profile locally. It does not create a delegated session key.
- `mega moss create-key` generates a delegated key locally and asks the
  passkey wallet to approve a scoped session key for the same wallet account.
- Session keys can spend only within their approved expiry, token spend limits,
  fee allowance, and contract call scopes.
- The CLI signs with the delegated session key and submits writes through the
  MegaETH/Porto relay. It never has the user's passkey or root/admin key.
- `mega moss revoke <key>` revokes a delegated key on-chain.
- `mega moss logout` only deletes this CLI's local profile and delegated
  private key material.

## Setup

If `mega moss --help` is unavailable, install the wallet CLI with the public
installer:

```bash
curl -fsSL https://account.megaeth.com/install | sh
```

After install, make sure the install directory printed by the installer is on
`PATH`, then rerun `mega moss --help`.

Release installs check for updates automatically.

## Safety Rules

- Never print, log, request, or transmit private keys, bearer tokens, API keys,
  passkeys, WebAuthn material, or relay secrets.
- Treat profile files as local secrets. Never inspect profile files directly,
  including with `cat`, `sed`, `rg`, workspace-wide search, or editor reads,
  and do not copy profile contents into chat, issue comments, logs, or
  telemetry. Use `mega moss whoami`, `mega moss list`, `mega moss permissions`,
  and `mega moss debug` instead.
- Use `mega moss call` for read-only `eth_call` workflows.
- Use `mega moss execute` or `mega moss transfer` only when the user asked
  for a state-changing operation.
- Bundle an ERC20 `approve` and its consuming contract call in the same
  `mega moss execute --calls` transaction; the relay resets standalone
  approvals at the end of a transaction.
- Never guess a protocol contract address when defining a call scope. Prefer
  `megaeth-developer-skills` when it is installed. If it is unavailable, that
  absence alone is not a blocker: retrieve the protocol's current official
  deployment registry or address-book source, confirm the MegaETH network,
  and cross-check the address with read-only on-chain calls when possible.
  Ask the user only when no authoritative source can be verified.
- Prefer `--json` for machine-readable inspection output and `--terse` only for
  compact tab-delimited output. On device-auth commands, both modes suppress
  the terminal QR; `--terse` is not a headless or chat-presentation mode.

## Login And Browser Authorization

### Choose the authorization flow

Default to loopback for `login`, `create-key`, and `revoke`. Use
`--auth-flow device` only when the user explicitly requests device
authentication or approval must happen in a browser that cannot complete the
CLI's `127.0.0.1` callback, typically on another machine or device. Do not
choose device auth merely to obtain a user-visible URL; loopback prints its
authorization URL too.

Loopback normally attempts to open the system browser and prints its URL as a
fallback while waiting. The legacy `--no-browser` flag only suppresses the
automatic opener and prints the URL immediately; use it when that explicit
behavior is requested. An opener failure does not invalidate the request or
require another auth flow: keep the same process running and use its printed
URL. Switch to device auth only when the same-machine callback cannot be
completed.

Run ordinary browser-opened loopback auth in the foreground. Do not background
it or add fixed sleeps merely to wait for the browser callback. If a loopback
URL must instead be copied into chat, keep the command in a persistent session
that yields control while it remains alive, present the URL before continuing
to wait, and never use a fixed sleep to guess when the URL is ready.

For device auth in a text-capable chat, always use human output with none of
`--json`, `--terse`, or `--qr-file`. Capture the complete terminal QR and
present it once as preformatted text. This is the standard chat handoff.
`--qr-file` is an advanced host-integration option that an agent must not choose
autonomously; use it only when the user or host explicitly requests an image
file and a real attachment API has already been verified. File access and a
local path are not attachment capability.

The device handoff is a prerequisite for approval, not a completion summary.
In text chat, never invoke `mega moss ... --auth-flow device` directly as a
foreground shell/tool call. Even if that tool says it streams output, its raw
transcript is not the required assistant-visible handoff, and it may not return
control until authorization has already finished. Start the command
asynchronously in one persistent execution instead. The asynchronous boundary
must be the execution tool call itself whenever the tool has a native
background/session facility. For example, set Claude Code's Bash
`run_in_background` option to `true`, call `TaskOutput` with `block: false` to
read the prompt without waiting for authorization, then call `TaskOutput` with
`block: true` on the same task only after the handoff is visible. In Codex, let
the execution call yield a live session ID and keep polling that same session.
Do not put `setsid`, `nohup`, `disown`, or a trailing shell `&` inside an
otherwise foreground tool call: some hosts keep tracking its descendants and
will not return control, which deadlocks the user handoff.

Only when no native background/session facility exists, and the tool is known
to return while a child stays alive, use one background supervisor with stdout
and stderr redirected to a private temporary log. Have it write an atomic
completion/status file after `mega moss` exits. Do not use `kill -0` alone as
the completion condition: an exited child can remain as a zombie and still
satisfy that check. If neither execution method can return control while the
request remains alive, do not start device auth; give the user the exact local
command instead. Start exactly one authorization request. If its launch does
not return control as expected, terminate that request when possible and report
the execution limitation; never retry by creating a second request.

Inspect output immediately and wait for the `Waiting for approval...` marker,
which terminates the complete static prompt. Use output-conditioned polling,
not a blind fixed sleep. The readiness call must return control while the same
CLI process remains alive. While authorization is still pending, copy the QR,
clickable direct link, CLI-supplied user code, and expiry into an
assistant-visible message. Only after sending that message may you make another
tool call to wait for completion. Resume through the same native task/session
facility and treat its completion status as authoritative. Do not start a new
foreground shell loop that uses `kill -0`, guessed `grep` patterns, or sleeps to
watch the native background task; that can stall after the task has already
finished. Never wait for `Waiting for approval...` to disappear from captured
output; the CLI output is append-only, so that line remains after completion. A
handoff left in tool output or presented after approval or command completion
is not a successful device-auth handoff.

Before starting device auth or presenting any device-auth QR or link, read
[references/device-auth.md](references/device-auth.md) completely and follow
its handoff procedure. If the CLI says device-code auth is unavailable, use
loopback auth or a wallet backend that supports `/v1/cli-auth/device`.

### Loopback login

Run login on the same machine as the approving browser:

```bash
mega moss login
```

The CLI opens MegaETH Wallet in the system browser, listens on
`127.0.0.1:<random-port>/callback`, validates `state`, and stores the approved
account profile locally. The callback must not contain private keys or
transferable bearer credentials. Login alone is not enough for writes; create a
scoped delegated key before `execute` or `transfer`.

### Complete authorization safely

Do not reuse old authorization URLs or edit their query parameters. The wallet
may reject an authorization with an actionable reason, such as an unavailable
fee token or mismatched wallet account. Treat that reason as terminal for the
current request: correct the stated condition or ask the user what to do, and
do not rerun the same authorization unchanged. If a request genuinely expires
or is interrupted without an actionable rejection reason, start one fresh
request and use only its new URL or code.

For both browser-opened and `--no-browser` authorization flows, pass
`--timeout-ms 300000` when passkey approval may take longer than the default
120 seconds.

Authorization commands are interactive waiting processes. Before starting one,
make sure your execution tool will stream stdout/stderr immediately and keep
the session open. Continue monitoring the same process until it completes,
times out, or the user asks you to stop. If you cannot monitor live output, do
not start the auth flow; tell the user the exact command to run locally instead.

Use login only to connect a wallet profile when none exists. If the CLI reports
`Wallet already connected to ...`, do not rerun login. Use
`mega moss create-key` to add a delegated key to the existing profile, or
`mega moss logout` only when the user explicitly wants this CLI install to
forget the local wallet profile.

If `create-key` fails because the authorized wallet account does not match the
local profile, run `mega moss whoami`, then ask the user to switch the browser
wallet/profile to that account. `mega moss logout` deletes the local profile
and delegated private key material; run it only after the user explicitly
approves reconnecting this CLI to a different wallet.

Login defaults to mainnet, `https://account.megaeth.com`,
`https://wallet-api.megaeth.com`, and `https://mainnet.megaeth.com/relay`. Use
`--wallet-url`, `--wallet-api-url`, or `--relay-url` only when deliberately
targeting non-canonical endpoints. Use `--network testnet` for the wallet
testnet profile and chain config.

Create-key defaults keep the approval simple: one-week expiry, a `100 USDM`
workflow spend cap, and roughly `$1` of relay-fee capacity in the default fee
token.
The agent must provide call scope with `--allow-call <target:signature>`, copy a
known-good key with `--from`, or pass a complete `--permissions
./permissions.json` file. Do not create workflow keys with implicit broad call
authority. Use the narrowest call and spend scope that covers the requested
workflow.

Use `mega moss create-key --spend-limit <token_address>:<amount>:<period>
--allow-call ...` to add explicit spend rows. Token must be a 20-byte address;
use `0x0000000000000000000000000000000000000000` for native ETH. Amount is the
human token amount, and period is `minute`, `hour`, `day`, `week`, `month`, or
`year`. Repeat `--spend-limit` for multiple spend rows. Custom permission files
must include top-level `feeToken` and a non-empty `permissions.calls` array. Never omit
`permissions.calls`; omitted calls have produced keys that the relay rejects for
writes. Each call entry must include both `to` and `signature`.
Read [references/permissions.md](references/permissions.md) before building
custom `--permissions` files, debugging permission schema errors, or planning
nontrivial protocol writes.
Validate permission shape before running auth commands. Do not use
`mega moss create-key` as a validator for known invalid permission requests.
For native ETH transfers, use a native ETH spend row and the no-calldata
selector `0xe0e0e0e0` for the recipient target, for example
`--allow-call '<recipient_address>:0xe0e0e0e0'`. Never use the reserved wildcard
address `0x3232323232323232323232323232323232323232` or selector
`0x32323232`.

Use `--fee-token <symbol>` and optional `--fee-limit <amount>` on `create-key`
to request explicit delegated-key relay-fee metadata. `--fee-limit` is a human
amount in the selected fee token. If omitted, the CLI chooses an approximate
`$1` fee-token buffer and adds or merges that fee spend capacity into
`permissions.spend`; this default is fine for ordinary workflows. Set
`--fee-limit` only when you have a specific reason to optimize, using roughly
`$0.10` of the selected fee token per expected relay write transaction as a
starting point. Add explicit `--spend-limit` rows for workflow token/native
movement. If either fee option is present and no `--spend-limit` is supplied,
the CLI requests fee spend capacity but no workflow spend rows. Supported
shorthand fee-token symbols are `ETH`, `USDM`, `USDT0`, and `MEGA` on mainnet,
and `ETH`, `USDM`, and `TST` on testnet.

Before selecting a non-default fee token with `--fee-token` or a custom
permission file's `feeToken`, use read-only balance inspection to verify that
the wallet currently holds enough of that token for the expected relay fees.
A supported fee-token symbol is not evidence that the wallet is funded with
it. Do not select a workflow input or output token merely because the workflow
uses or may acquire it later. If sufficient current balance cannot be verified,
leave fee-token selection at the CLI default.

Relay fees use delegated-key fee metadata plus relay/account enforcement, while
workflow token/native movement uses `permissions.spend`. Future `execute` and
`transfer` calls default to the `authorizedKey.feeToken` returned by wallet
approval. The Gas Token shown during approval pays the approval transaction
itself and should not be treated as a mutation to the requested key scope.

## Inspect The Active Wallet

```bash
mega moss whoami --json
mega moss list --json
mega moss permissions 0xKEY_OR_ACCESS_ADDRESS --json
```

Use these before writes to verify the account, delegated access address, expiry,
approved permission limits, and current on-chain spend remaining. If you only
have a shortened key id from plain text output, run `mega moss list --json`
and copy the full `accessAddress` into `mega moss permissions`.
In `permissions --json`, treat `authorizedKey.permissions.spend` as the stored
request and `spendInfos[].remaining` as the live execution capacity.
`spendInfos` is Porto/account spend accounting, so it can include relay
fee-token allowance even when `authorizedKey.permissions.spend` is empty.

## Execute Writes

```bash
mega moss execute \
  --to 0x1234567890abcdef1234567890abcdef12345678 \
  --data 0x \
  --value 0
```

For multiple writes, pass `--calls ./calls.json`. Pass
`--key 0xKEY_OR_ACCESS_ADDRESS` only when the user has approved using a
non-default stored key. Confirm that the requested operation fits the approved
delegated-key permissions before executing.

When hand-writing raw calldata, verify the function selector first with an ABI
encoder or `cast sig`; mismatched selectors cause wrong calls. For
`--allow-call` and permission-file call scopes, prefer canonical
human-readable function signatures. Use raw selectors only when necessary; use
`0xe0e0e0e0` specifically for native ETH no-calldata transfer scopes and never
use wildcard/sentinel selectors such as `0x32323232`.

Spend permission is not call permission. A key with `calls: []` or omitted
`permissions.calls` cannot execute relay-backed writes, including native ETH
transfers, even when it has spend allowance. Do not request `calls: []` and do
not omit `permissions.calls`; use explicit `--allow-call <target:signature>`
scopes or permission-file call entries with both `to` and `signature`.

For workflows that move ERC20 value through another contract, the key usually
needs both spend permission for the token and call permission for each contract
function it invokes, such as ERC20 `approve` plus the downstream protocol call.
ERC20 spend accounting charges the larger of recognized calldata value
(`transfer`, `transferFrom`, `approve`, Permit2 approve) and observed wallet
balance decrease. Size spend caps for the larger amount in an approve plus
protocol-call batch, not the sum.

### Common Patterns

ERC20 approve plus protocol call, such as Aave supply or a swap:

```json
[
  {
    "to": "<TOKEN>",
    "data": "0x<approve(spender,amount) calldata>",
    "value": "0"
  },
  {
    "to": "<PROTOCOL>",
    "data": "0x<supply/swap/deposit calldata>",
    "value": "0"
  }
]
```

Use one `mega moss execute --calls ./calls.json` command for the array above.
Do not split approval and consumption across two `execute` calls.

## Read State

```bash
mega moss call \
  --to 0x1234567890abcdef1234567890abcdef12345678 \
  --data 0x
```

`call` is read-only and should be the default for inspection.
If `--from` is omitted, the CLI uses the logged-in wallet account when a local
profile exists. Pass `--from 0x...` only when a different simulation address is
needed.

## Manage Delegated Keys

```bash
mega moss list --json
mega moss list --show-inactive --json
mega moss permissions 0xKEY_OR_ACCESS_ADDRESS --json
mega moss switch 0xKEY_OR_ACCESS_ADDRESS
mega moss create-key \
  --allow-call '0xfafddbb3fc7688494971a79cc65dca3ef82079e7:transfer(address,uint256)' \
  --label "usdm-transfer"
mega moss create-key \
  --spend-limit 0xfafddbb3fc7688494971a79cc65dca3ef82079e7:25:week \
  --allow-call '0xfafddbb3fc7688494971a79cc65dca3ef82079e7:transfer(address,uint256)' \
  --label "agent"
mega moss label 0xKEY_OR_ACCESS_ADDRESS "agent"
mega moss revoke 0xKEY_OR_ACCESS_ADDRESS
mega moss revoke 0xKEY_OR_ACCESS_ADDRESS --fee-token USDm
```

Use `list` to inspect local keys. Revoked and expired keys are hidden unless
`--show-inactive` is present. Use `permissions` to inspect the exact approved
scope and remaining on-chain spend before a write. Plain-text output separates
the stored approved scope from live on-chain spend remaining. When operating on
testnet, pass `--network testnet` consistently on login, create-key,
inspection, writes, revoke, fund, and logout commands.

Use `create-key` when no existing key has the requested scope; it opens the
browser/passkey approval flow and requires explicit call scope unless using
`--from` or `--permissions`. Follow the authorization-flow selection rules above
for both `create-key` and `revoke`; read the device-auth reference before using
that flow. Use `revoke` to revoke a key on-chain; the CLI keeps an inactive audit
record but removes local private key material. Revoke defaults to the key's
stored fee token. On revoke, `--fee-token` selects the relay payment token for
that revoke transaction.

## Update And Uninstall

Release installs check for updates automatically. Use `mega moss update --check`
only when diagnosing version issues, and `mega moss update` when the user
explicitly asks to update immediately.

Do not uninstall unless the user explicitly asks. To remove installed CLI files
only:

```bash
~/.mega/wallet-cli/current/scripts/uninstall.sh
```

To remove installed CLI files plus local wallet profiles and delegated private
key material:

```bash
~/.mega/wallet-cli/current/scripts/uninstall.sh --config
```

Uninstalling or logging out does not revoke on-chain delegated keys; use
`mega moss revoke <key>` for on-chain revocation.

## Custom Permission Files

For the full permission schema and examples, read
[references/permissions.md](references/permissions.md).

For protocol-specific contract addresses, calldata, and workflow recipes, use
`megaeth-developer-skills` when it is installed; use this skill for `mega moss`
execution and delegated-key permission rules. When that optional skill is not
installed, follow the authoritative-source and read-only verification fallback
in the Safety Rules rather than stopping solely because the package is absent.

## Transfer Funds

Native ETH:

```bash
mega moss create-key \
  --spend-limit 0x0000000000000000000000000000000000000000:0.1:week \
  --allow-call '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd:0xe0e0e0e0'
mega moss transfer --to 0xabcdefabcdefabcdefabcdefabcdefabcdefabcd --amount 0.1
```

ERC20:

```bash
mega moss transfer \
  --token 0x1234567890abcdef1234567890abcdef12345678 \
  --to 0xabcdefabcdefabcdefabcdefabcdefabcdefabcd \
  --amount 100
```

`transfer` is a wrapper over `execute`; it is still a write operation.
For ERC20s, the CLI reads token decimals from RPC unless `--decimals` is
provided.
Pass `--key 0xKEY_OR_ACCESS_ADDRESS` only when the user has approved using a
specific non-default delegated key.

## Fund The Wallet

```bash
mega moss fund
mega moss fund --no-open --json
```

`fund` opens or prints the wallet deposit URL for the active account. It does
not transfer funds by itself.

## Debug

```bash
mega moss debug --json
mega moss debug --skip-chain --json
```

Use `debug` to inspect profile path/mode, account, delegated key expiry, native
balance, and relay key status. Do not print or copy profile files.

## Logout

```bash
mega moss logout
```

Logout deletes the local wallet profile, including locally stored delegated
private key material and key-selection metadata. It does not revoke delegated
keys on-chain. Use `mega moss revoke <key>` when the user wants on-chain
revocation; use `logout` only when the user explicitly wants this CLI install to
forget the wallet locally.
