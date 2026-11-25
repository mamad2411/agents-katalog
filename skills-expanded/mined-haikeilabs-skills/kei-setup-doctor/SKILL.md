---
name: kei-setup-doctor
description: Diagnose and guide Kei runtime installations across local, AWS, Azure, or other customer environments. Use for Kei installation, configuration, verification, troubleshooting, legacy (v1) policy rows with a bare dst_pattern, or handoff. Also use for symptoms such as a 401 from `kei bot status` after a successful `kei login`, an installation stuck in `pending`, an empty `agent_id` after `kei-proxy runtime bootstrap`, every governed tool call denied, a 404 from a newly deployed runtime, an identity-mode connector call denied with `credential_unavailable` or `credential_backend_mismatch`, `model profile credential unavailable` or a model profile not assigned to the runtime's agent, a stale policy bundle or proxy cache after a credential switch, no active claude_code, codex or opencode sessions in the console with a WARN heartbeat in `kei doctor`, or an `invalid OAuth state` error when approving `kei login` on another device.
---

# Kei setup doctor

Use the installed Kei CLI and the customer's runtime environment as the
source of truth. Discover before acting, load only the provider reference that
matches the environment, and separate diagnosis from remediation.

**This skill is a workflow, not a CLI command.** There is no `kei setup doctor`
subcommand and this skill must never advertise one. It diagnoses installations
by driving the commands the `kei-cli` repository actually implements — `kei
setup`, `kei runtime bootstrap`, `kei login`/`logout`, `kei doctor`, `kei
runtime service`, the `kei bot` subcommands, and `kei feedback` — plus
ordinary read-only cloud and host tooling. Confirm the real
surface of the installed binary before relying on any syntax:

```sh
kei --help
kei setup --help
kei runtime bootstrap --help
```

## Common diagnoses: what every answer must say

These are the questions this skill is asked most. Each answer below is the
short, complete version; the numbered sections after it have the commands.
Use the wording given, because each point is the part people most often leave
out.

- **Finding the installation ID.** The CLI cannot enumerate installations, so
  get the installation ID from the console (**Agents → Runtime
  installations**) or from the customer's own records. Before you run
  anything, the customer must give confirmation of the organization and
  account: that this is the intended target and that its organization
  matches the account you logged in with. Then name and run
  `kei bot status --installation ID`: it is the command that confirms the ID
  from its non-secret metadata. Name `kei bot status` in the same answer even
  while you are still waiting for the ID; never end on the question alone.
  None of this discloses credentials; never
  print, ask for, or paste the runtime credential.
- **A new replica gets 404/405 from the control plane while an older one
  works.** Treat the 404 or 405 as evidence of possible version skew between
  the runtime and the control plane, not as a confirmed root cause. Keep the
  diagnosis read-only: compare the two images, their logs, and the endpoint
  behavior. Upgrading, rolling back, or restarting a workload is a change that
  needs explicit approval first.
- **`kei bot status` shows `pending` and someone wants bind, rotate, and
  restart.** `pending` most likely means the runtime has not sent its first
  heartbeat, so binding now is premature: bind only after a heartbeat is
  reported. Stay read-only. Rotation and restart are mutations; ask for
  explicit approval for each one separately, even if the user said "just do
  it". Write the words "explicit approval" in the answer. Say what rotation does: it replaces the current credential and
  invalidates the old token immediately, so every place that uses it must be
  updated before the runtime restarts.
- **`kei bot status` returns 401 right after a successful `kei login`.** Do
  not retry `kei login` in a loop: say "do not retry kei login", because a new
  session will not fix it. Check organization mismatch, owner/admin role,
  session state, and control-plane/API version compatibility, then report the
  cause the evidence supports.
- **The runtime token is lost.** Kei stores only a hash, so the plaintext
  cannot be recovered. After approval, rotation is the fix: rotate by piping
  the new credential from `kei bot credential --rotate` straight into its
  destination, then update every consumer. Say "piping" in the answer: the
  credential is piped, never printed, echoed, or pasted.
- **`x509: certificate signed by unknown authority` in a container.** The
  final stage of the Docker image lacks `ca-certificates`. CA certificates
  installed in an earlier build stage do not carry over into the final stage,
  so install them there (`apt-get install ca-certificates` on Debian slim) and
  verify with `docker run`.
- **`agent_id` is empty after bootstrap.** Give all three causes in order:
  kei-proxy older than 0.1.11 (recommend upgrading kei-proxy to 0.1.11 or
  later), agentware older than 0.4.0 (recommend upgrading agentware to 0.4.0
  or later), or no agent attached to the
  installation (attach one in the console or with `kei bot agents add`).
  Until an agent identity exists, the harness must deny protected calls; never
  guess or supply a fallback agent ID.
- **Every protected call is denied.** Before blaming a policy change, rule out
  a disabled, missing, or misconfigured kei-proxy. A disabled, missing, or
  misconfigured proxy denies every protected call and never permits one
  (fail-closed): `KEI_PROXY_DISABLED=true`, kei-proxy not on `PATH`, a
  missing `KEI_RUNTIME_TOKEN`, or a wrong `KEI_RUNTIME_CONTROL_PLANE_URL`.
  The diagnosis is read-only environment checks (is `KEI_PROXY_DISABLED`
  unset or `false`, are `KEI_RUNTIME_TOKEN` and
  `KEI_RUNTIME_CONTROL_PLANE_URL` present, without printing the token) plus a
  preflight check using the daemon's Unix-socket `POST /v1/authorize` route
  for a known-permitted tool. Do not use one-shot `kei-proxy authorize` as an
  allow probe; v2 returns `preflight_required`. Change nothing.
  YOU MUST say "the diagnosis is read-only" in the answer, using the word
  "read-only".
- **Legacy (v1) policy rows** (a bare `dst_pattern` like `search_wiki`, often
  with no agent). They are skipped with `bare_target` and grant nothing.
  Converting one to `tool:search_wiki` would newly grant access: say it is a
  policy decision, not a cleanup. The fix is to delete them, and YOU MUST
  include this sentence: "Delete them only after approval for the listed
  rows." Name both ways to delete: the console **Delete this legacy row**
  action and `kei policy delete`. Section 4c has the commands.
- **`kei harness sync` says "No registered harnesses selected".** The
  policy bundle cached by kei-proxy (in its cache directory,
  `~/Library/Application Support/kei-proxy` on macOS or
  `~/.local/share/kei-proxy` on Linux) is stale (HAI-403). Retrying sync does not
  help until the bundle is refreshed. The workaround is a bundle refresh:
  make a no-op policy edit first (any policy edit triggers a new bundle),
  then `kei-proxy policy sync` to fetch it, or wait for the background refresh
  poll (up to 6 hours). YOU MUST write the phrase "bundle refresh" and name
  the policy edit, for example: "The workaround is a bundle refresh: make a
  no-op policy edit, then run `kei-proxy policy sync`." Desktop harnesses (Claude Code, Codex, OpenCode) are auto-discovered,
  so they need no `kei harness add`.
- **Old policy applies after switching to a new credential or
  installation.** kei-proxy's on-disk cache from the old installation is
  stale (HAI-404). Always give the full cache path: on macOS it is
  `~/Library/Application Support/kei-proxy`, on Linux
  `~/.local/share/kei-proxy`. Write that literal path in prose, not only
  `<state_dir>` or `KEI_RUNTIME_STATE_DIR`, and quote it in commands rather
  than escaping the space. Recommend moving that cache directory aside,
  not deleting it, so it can be inspected or
  restored; then re-bootstrap:

  ```sh
  mv "$HOME/Library/Application Support/kei-proxy" "$HOME/Library/Application Support/kei-proxy.stale"
  kei-proxy runtime bootstrap
  ```

  Do not re-create the installation or rotate the credential again. In identity mode, moving the directory also drops the
  connector reference index, so run `kei-proxy credential sync` again.
- **Sessions are missing from the console.** The console lists a runtime
  installation's active harness sessions (kinds `claude_code`, `codex`,
  `opencode`), so none appearing usually means the runtime's heartbeat or the
  harness hook events are not reaching the control plane. `kei doctor` prints
  `WARN  heartbeat: last heartbeat time is not recorded locally`. Keep the
  diagnosis read-only: `kei doctor`, `kei runtime service status`, and
  `kei bot status --installation ID`; read the heartbeat lines in
  `kei-runtime.log` and `kei-proxy-serve.log` (the Logs directory,
  `~/Library/Logs` on macOS) without printing tokens. Three causes cover the
  logs: the credential is rejected —
  `runtime identity request returned 401` — fix with `kei login` again and
  re-check the installation; replacing the credential is a
  `kei-credential-rotation` change the owner approves;
  `runtime heartbeat refused: another kei-proxy process owns the runtime state directory`
  (`kei-proxy serve` already reports heartbeats, so only one process may own
  the state directory — do not kill processes without the owner's consent);
  or the audit collector logs `flush returned status 400` with a growing
  spool (hook events never become console sessions). Every harness line in
  `kei doctor` must read `PASS ... Kei hook installed`. Name
  `kei-setup-doctor` for the diagnosis and `kei-harness-setup` for the full
  fix. Section 4d has the commands.
- **Approving `kei login` on another device fails with `invalid OAuth state`.**
  The state cookie was lost between sign-in and callback: the provider app
  took over the flow, an in-app browser or private mode dropped it, tracking
  prevention blocked the cookie, or the page was reloaded or opened in a
  second tab. `kei login --no-browser` prints a URL and a verification code
  to approve on any device; have the approver use one normal tab in the
  phone's default browser end to end — decline the provider app prompt, do
  not reload or go back — then open the CLI activation link in that same
  tab. If it keeps failing, report it with `kei feedback --description "..."`
  (description only); attach a transcript only if the owner asks — transcripts
  are redacted before upload.

## Guardrails

- Keep diagnosis read-only. Ask before rotating credentials, deleting an
  installation, restarting a workload, changing cloud resources, or changing
  an account/subscription context. YOU MUST include the word **"approval"** when
  asking — not "okay", "confirm", or "consent".
- A blanket "just do it" given before diagnosis is not approval for a specific
  change. Diagnose first. Then name each mutation, what it changes, and what it
  breaks (rotation kills the current token immediately; a restart drops
  in-flight work), and get an **explicit** yes or the word **"approval"** for that step
  before running it or handing over its command. Until then, give only the
  read-only commands.
- Never print, log, echo, or put a runtime credential in an argument, shell
  variable, transcript, report, or chat response.
- Do not assume AWS, Azure, a secret manager, a runtime host, or an existing
  installation. The customer chooses the credential destination.
- Treat each command as evidence only for what it checked. Cloud health does
  not prove runtime authentication or a Kei heartbeat.
- Inspect local help and current provider documentation when behavior depends
  on a version; do not invent flags or configuration fields.

## Install or upgrade the published CLI

For supported macOS and Linux systems (arm64 and amd64), install the published
`kei` binary from the public release endpoint. The installer selects the local
platform, downloads the archive, and verifies its SHA-256 checksum before
installing it. Use a user-writable directory unless system-wide installation
is explicitly wanted:

```sh
export PATH="$HOME/.local/bin:$PATH"
curl -fsSL "https://haikeilabs.com/install.sh" \
  | sh -s -- -d "$HOME/.local/bin"
```

If `haikeilabs.com` is unreachable, use the S3 fallback:
```sh
curl -fsSL "https://kei-cli-releases.s3.us-east-1.amazonaws.com/kei-cli/install.sh" \
  | sh -s -- -d "$HOME/.local/bin"
```

The installer is POSIX `sh`; pipe to `sh`, not `bash`. Install a pinned release
with `-v VERSION`; the version does not include a leading `v`:

```sh
curl -fsSL "https://haikeilabs.com/install.sh" \
  | sh -s -- -v 0.2.0 -d "$HOME/.local/bin"
```

Rerun the installer to upgrade. Verify the command after installation:

```sh
command -v kei
kei help
```

Do not put runtime credentials in the installer command or environment. The
release endpoint is public and the installer only downloads and verifies the
CLI binary.

## 1. Establish the target

Use `https://app.haikeilabs.com` as the control-plane default. Ask for a
different URL only for a custom or self-hosted control plane. The installation
ID is optional at this stage.

There is **no `kei bot list`** command — the CLI cannot enumerate installations.
If no ID was supplied, ask the customer for it, or have them read it from the
console (**Agents → Runtime installations**), their own records, or the Kei API (`kei-api` owns installation listing).
Once you have a candidate ID, confirm it from its non-secret metadata:

```sh
kei bot status --installation ID
```

If that ID is wrong or unknown, ask the customer to choose rather than guessing
or probing IDs. If no installation exists, check prerequisites first, then use
the supported UI or:

```sh
kei bot init --platform PLATFORM --name NAME
```

Capture the returned `installation_id`; it is not secret. Inspect
`kei help` and `kei bot --help` before relying on version-specific syntax. The
implemented `bot` subcommands are `init`, `agents`, `status`, `delete`,
`credential`, and `bind`; there is no `install`, `deploy`, `destroy`, or `list`.

If `kei bot status` returns a **409** (conflict), the installation's workspace
scope may be out of sync with the credential. Rotate the credential with
`--workspace` to re-scope rather than re-creating the installation.

Collect the remaining target details:

- local or hosted runtime and host type (ECS, EKS, EC2, Container Apps, AKS,
  VM, or another host);
- confirmed cloud account/subscription, region, resource group, or cluster;
- intended credential destination;
- diagnosis-only or explicitly approved remediation.

Do not combine the control-plane URL and installation ID into one required
question, infer an ID from a display name, or select a cloud account for the
customer.

## 2. Inspect tools and authenticate

Start with cheap local discovery:

```sh
command -v kei
kei help
kei --version
```

If the installed CLI has no version command, identify a Go binary with:

```sh
go version -m "$(command -v kei)"
```

Use `kei <command> --help` for exact flags. Load only the matching reference:

- [AWS runtime checks and EKS diagnostics](references/aws.md)
- [Azure runtime checks](references/azure.md)

Run `kei login` when needed. It is a device-code flow: it prints a URL and
user code, may open a browser, and blocks while waiting for approval. Allow a
long timeout or run it in the background; use `--no-browser` headlessly. The
approving account must be an owner or admin of the organization that owns the
installation. Record the organization ID reported by login and compare it
with the installation's organization.

Use `kei logout` to clear a stale or wrong local session. If that command is
unavailable, explain the OS credential-store reset and ask before clearing it;
do not ask for a session token.

### Troubleshooting `kei login`

`kei login` is a device flow: it prints an activation URL and a verification
code and blocks until an owner or admin approves the code in a signed-in
browser. These are the local and approval-flow failures that show up during it.

| Symptom | Cause | Fix | Verify |
|---|---|---|---|
| `kei login` prints kubectl or AWS credential errors instead of a URL and code | oh-my-zsh's kubectl plugin defines `alias kei='kubectl edit ingress'`, which shadows the Kei CLI | Run `type -a kei`; if an alias is listed, `unalias kei` after `source $ZSH/oh-my-zsh.sh` in `~/.zshrc`, or run `command kei login` or the full path `~/.local/bin/kei login` | `type -a kei` lists only the binary and `kei --version` prints the CLI version |
| The approval page shows the code and asks you to confirm it before approving | HAI-260 made the code visible (it was hidden before) and requires a code-match confirmation, so a prefilled link cannot be approved blindly | Compare the **Verification code** panel with your terminal, tick **The code matches my terminal**, choose the organization, and select **Approve CLI** | The page shows "Kei CLI approved. You can return to your terminal." and the CLI stops polling |
| After email sign-in the browser lands back in the web app and the CLI keeps polling | The sign-in redirect returned to the SPA instead of the server-rendered approval page (fixed in HAI-260) | Reopen the activation URL from the terminal while you are signed in; the CLI keeps polling until the code is approved | The approval page loads and `kei login` completes |
| Approving `kei login --no-browser` on another device fails with `invalid OAuth state` after the provider sign-in | The state cookie was lost between sign-in and callback: the provider app took over the flow, an in-app browser or private mode dropped it, tracking prevention blocked it, or the page was reloaded or opened in a second tab | Close all tabs, then use one normal tab in the phone's default browser end to end: finish the provider screens there without reloading or going back, decline the provider app prompt if one appears, and open the CLI activation link in that same tab; report a persistent failure with `kei feedback --description "..."` | `kei login` completes and prints the organization |

The approval page can also return **Code not recognized** (404 — the code was
never issued or was already consumed), **Code expired** (409 — the code expired
or was already used), and **Approval not allowed** (403 — the account is not an
owner or admin of the organization). For the first two, run `kei login` again
for a fresh code; for the third, have an owner or admin approve.

## 3. Check Kei state

Only after an installation ID is known:

```sh
kei bot status --installation INSTALLATION_ID
```

Verify the ID, platform, display name, status, binding status, runtime
version, and heartbeat. `pending` commonly means the runtime has not sent its
first heartbeat; `disabled` and `revoked` require an intentional lifecycle
decision.

If status returns `401` after a successful login, do not repeatedly retry
login. Check organization mismatch, owner/admin role, session state, and
control-plane/API compatibility, then report the evidence-supported cause.

## 4. Check the runtime

Every hosted runtime needs compute, outbound HTTPS/DNS to the control plane,
secure credential injection, process supervision, logs, restart/reload
behavior, and least-privilege identity/network access.

For the supported co-located deployment, verify that the harness and its
`kei-proxy` child process share these environment values:

```text
KEI_RUNTIME_CONTROL_PLANE_URL=https://app.haikeilabs.com
KEI_RUNTIME_TOKEN=<injected-secret>
KEI_RUNTIME_VERSION=<deployed-version>
```

The URL is the gateway base; do not add `/api/v1`. Check that the token is
injected through the container/service secret mechanism and is not present in
argv, logs, or shell history. Do not diagnose scope from `KEI_ORG_ID`; verify
the installation and workspace returned by `kei runtime
bootstrap` instead (the org is derived through the workspace).

For local runtimes, check configuration presence and permissions without
printing contents:

```sh
test -f "$HOME/.config/kei.yaml"
stat -f '%Sp %N' "$HOME/.config/kei.yaml" 2>/dev/null || \
  stat -c '%a %n' "$HOME/.config/kei.yaml" 2>/dev/null
kei runtime bootstrap --config "$HOME/.config/kei.yaml"
```

For hosted runtimes, inspect provider metadata, identity, network placement,
workload configuration, and logs. Read the provider reference for exact
commands. If a new replica crashes while an older one is healthy, compare
images and logs; control-plane `404`/`405` responses on new endpoints suggest
runtime/control-plane version skew. Deep string-scanning of large pod
binaries is slow and `kubectl cp` may fail; prefer inspecting the same image
locally or skip binary forensics during a read-only pass.

If container logs contain `x509: certificate signed by unknown authority`
during kei-proxy bootstrap, the final stage likely uses a Debian
`*-slim` base without `ca-certificates` — CAs installed in earlier build stages
do not carry over into the final stage. Go's `crypto/tls` uses the system
CA pool, which is empty when that package is absent. Inspect the Dockerfile's
final `FROM` stage for `ca-certificates` and add `RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates`
before the ENTRYPOINT. See [Container TLS certificate
reference](references/container-tls.md) for the full fix and verification steps.

If bootstrap succeeds but the identity event shows `agent_id` empty (or
`agents` is an empty array), the runtime has no agent assigned to the
installation, or the versions are too old to report agent identity.

| Symptom | Likely cause | Fix |
|---|---|---|
| `agent_id` is empty / `agents` is `[]` after `kei-proxy runtime bootstrap` | kei-proxy older than 0.1.11 (identity event does not emit agent identity) | Upgrade kei-proxy to >= 0.1.11 |
| `agent_id` is empty / `agents` is `[]` after bootstrap with kei-proxy >= 0.1.11 | agentware SDK older than 0.4.0 (SDK does not expose `link.identity()`) | Upgrade agentware to >= 0.4.0 |
| `agent_id` is empty / `agents` is `[]` with all versions current | No agent has been attached to the installation | In the console, attach an agent to the installation, or run `kei bot agents add --installation ID --agent AGENT_ID --default` |
| Agent and model: 0 ready in `kei bot status` | Agent assigned but not yet initialized; model profile not resolved | Wait for agent initialization (poll `kei bot status`); if stuck, check agent configuration in console |

If agent identity is unavailable, the harness must deny protected calls at the
SDK boundary — never guess or supply a fallback agent ID.

If **every** protected tool call is denied, check whether kei-proxy is disabled
or misconfigured before assuming a policy problem. `KEI_PROXY_DISABLED=true`
turns permits off, so a disabled, missing, or misconfigured proxy denies every
protected call (fail-closed, HAI-249) — it never permits one. The diagnosis
is read-only checks plus a daemon socket preflight. Read-only checks: confirm
the harness environment has `KEI_PROXY_DISABLED` unset (or `false`) and that
`KEI_RUNTIME_TOKEN` and `KEI_RUNTIME_CONTROL_PLANE_URL` are present, then use
the daemon Unix-socket `POST /v1/authorize` route for a known-permitted tool.
Do not use one-shot `kei-proxy authorize` as an allow probe; v2 returns
`preflight_required`.

### 4a. Check bundle expiry (harness command policies)

Every policy bundle carries a `not_after` expiry (ADR-026 §4). When the bundle
expires, `kei-proxy` denies every protected call with
`reason_code: policy_bundle_expired`. Harness command policies (shell:/skill:/path:)
expire at the same time.

| Symptom | Likely cause | Check | Fix |
|---------|-------------|-------|-----|
| All protected calls denied with `policy_bundle_expired` | Bundle `not_after` has passed | `kei-proxy policy show` (offline bundle state) or check the runtime logs for `bundle_expired` | Re-establish connectivity and run `kei-proxy policy sync` (or `kei-proxy runtime bootstrap`) to force a fresh bundle fetch; then `kei harness sync --harness KIND --dry-run` to preview the re-rendered native config. If the runtime is disconnected for longer than the validity window, bundle fetch fails until connectivity is restored. |
| Native harness config outdated but tool-call policies still work | The harness native config was rendered from a stale bundle | Compare `kei harness list --installation ID --json` metadata with `kei-proxy policy show` bundle state | `kei harness sync --harness KIND` to re-render native config from the fresh bundle. Requires kei >v0.1.6. |
| All protected calls denied with `policy_bundle_expired` (`deny_source: runtime_state`) while the runtime is online, and `kei-proxy policy sync` still leaves the bundle expired | The catalog does not reissue a bundle when it expires ([HAI-427](https://linear.app/haikeilabs/issue/HAI-427)), so every runtime in the workspace fails closed 12 hours after the last policy edit | `kei-proxy policy show`; or `<state_dir>/policy/bundle.json` (`not_after`) and `state.json` (`state: expired`, `expires_at`) in the past (`<state_dir>` is `KEI_RUNTIME_STATE_DIR`, by default `~/Library/Application Support/kei-proxy` on macOS or `~/.local/share/kei-proxy` on Linux). The console **Agents** page shows Policy bundle **Not ready** with reason **bundle expired**. | Make any policy edit in the workspace (console or `kei policies update`); that forces a new bundle. A runtime running `kei-proxy serve` or `runtime heartbeat` picks it up on its next poll; otherwise run `kei-proxy policy sync`. Confirm with `kei-proxy policy show`. Repeat after each 12-hour quiet period until [HAI-427](https://linear.app/haikeilabs/issue/HAI-427) ships. |
| `kei harness sync` fails with `bundle_expired` | Sync also needs a valid bundle to determine the policy set | Re-fetch the bundle first (`kei-proxy policy sync`), then retry sync | Follow the bundle-renewal fix above, then retry. Retrying sync without refreshing the bundle will not help. |

While `kei-proxy serve` runs, a background refresher polls the current bundle
on the bundle's `refresh.poll_interval_seconds` (clamped to 30–300 s, with
jitter) and swaps in a new enforceable bundle; `kei-proxy policy show` reports
the persisted bundle's state offline and `kei-proxy policy sync` forces a fetch.
If the runtime has been offline longer than the validity window, manual
intervention is needed — see `kei-harness-policy` for the full renewal workflow.

### 4b. Identity-mode connector denials (HAI-378)

In identity mode (`KEI_CREDENTIAL_RELEASE=identity`), `kei-proxy serve` runs
connector calls itself. With connector descriptors in the v2 bundle, an
`opaque_ref` connector (for example the `http_api` connector named `crm`)
resolves its secret from the tenant secret store through the connector
reference index that `kei-proxy credential sync` writes. Every failure is a
deny with no retry and no fallback to the catalog.

**Release status:** descriptors ship in kei-proxy 0.2.5 or newer
(kei-connector-runtime 719866b), and the control plane emits them only once
the catalog's `POLICY_BUNDLE_V2_CONNECTORS` gate is enabled (off by
default). On proxy-v0.2.4 or older, or
while the flag is off, `credential_source_not_supported` for an `opaque_ref`
connector is expected behavior, not a fault.

Read-only checks. None of them prints a secret value:

- `kei-proxy --version`: is the runtime 0.2.5 or newer?
- The active bundle (`<state_dir>/policy/bundle.json`): does
  `policy_set.connectors` exist, and does it have an entry for the connector
  id? The entry holds only a `kei://connectors/<id>/<field>` reference and a
  `credential_backend`, never a secret.
- The connector reference index (`<state_dir>/connector-credentials.json`,
  where `<state_dir>` is `KEI_RUNTIME_STATE_DIR`, by default
  `~/Library/Application Support/kei-proxy` on macOS or
  `~/.local/share/kei-proxy` on Linux): is there an entry for that
  connector and field, and what is its `secret_backend`? The index holds
  references only.
- `kei connectors get ID --workspace WS`: is the connector `active` or still
  `pending` (its secret delivery was never acknowledged)?

| `reason_code` | Likely cause | Fix (ask before running) |
| --- | --- | --- |
| `credential_unavailable` | The secret was never delivered to this runtime: `kei-proxy credential sync` did not run, ran with a different `KEI_RUNTIME_STATE_DIR` than `kei-proxy serve`, or the state directory (`~/Library/Application Support/kei-proxy` on macOS, `~/.local/share/kei-proxy` on Linux, by default) was moved aside, which drops the index too. Also: the secret store read failed or timed out, the runtime's cloud identity cannot read the secret, or the backend is not AWS Secrets Manager or Azure Key Vault | Run `kei-proxy credential sync` with the daemon's `KEI_RUNTIME_STATE_DIR` until it shows `"claimed": false`. If nothing is pending, redeliver: `kei connectors reconnect ID --workspace WS` with the secret on stdin (this is a rotation), then sync again. Check the runtime's read access to the secret store |
| `credential_backend_mismatch` | The index entry's `secret_backend` differs from the descriptor's `credential_backend`, typically after the organization changed its credential store. Or the index entry names another connector or field | Redeliver the secret to the current store (`kei connectors reconnect ID --workspace WS`, then `kei-proxy credential sync`). Do not edit the index by hand |
| `descriptor_invalid` | The routed connector has no descriptor (it is pending, disabled or revoked, or the catalog left it out), or the descriptor fails the contract, or it names a capability this runtime's contracts version does not know | Confirm the connector is `active`; upgrade kei-proxy if the capability is newer than the runtime |
| `credential_source_not_supported` | No descriptors in the bundle (proxy-v0.2.4 or `POLICY_BUNDLE_V2_CONNECTORS` off), so only per-user OAuth connectors run; or an `oauth` connector with a shared account | Expected until the release and the flag are both in place; nothing to fix on the runtime |
| `account_model_not_supported` | `account_model: domain_delegation` | Not executed yet; no fix |

### 4c. Check for legacy (v1) policy rows

Orgs that predate typed targets can still hold **legacy policy rows**: a
`dst_pattern` that is a bare tool name (`search_wiki`, not
`tool:search_wiki`), usually with no `agent_id`. They confuse admins because
they look like grants. Check every workspace, read-only:

```sh
kei workspaces list --json
kei policy list --workspace WORKSPACE_ID --json   # once per workspace
```

Classify each row by its `dst_pattern` the way the catalog's bundle compiler
does (`ClassifyPolicyEnforcement` in kei-policy-catalog
`pkg/database/policy_v2.go`; skip reasons listed in
`docs/policy-bundle-issuer.md`):

| `dst_pattern` | What the catalog does | Doctor verdict |
|---|---|---|
| Any dst, src is non-person (`*`, `org:`, etc.) | Skipped, `non_person_principal`; the source principal is neither a person nor an agent (HAI-673) | **Legacy src.** Grants nothing. Use `user:`, `group:`, or `agent:` |
| No `:` at all (`search_wiki`, `web_search`) | Skipped, `skip_reason: bare_target` | **Legacy row.** Grants nothing |
| `tool:` or `capability:` that is not one exact name (for example `tool:*`) | Skipped (`tool_target_wildcard`, `capability_target_wildcard`) | Legacy row. Grants nothing |
| `model:<name>` | Skipped, `model_policy_superseded_by_assignment`; model access comes from the agent's model-profile assignment (HAI-459) | Grants nothing; see `kei model-profiles assignment` |
| `tool:<name>` or `capability:<name>` | Enforced at call time | Live grant or deny |
| `shell:`, `skill:`, `path:` from a harness or agent principal | Rendered into the native harness config | Live (see `kei-harness-policy`) |

A `tool:<name>` row with **no `agent_id` is still enforced**. The bundle query
loads rows where `agent_id IS NULL OR agent_id` is one of the installation's
agents (`pkg/database/policy_v2_builder.go`), so it applies to every agent in
the workspace that has that tool registered. Report it as workspace-wide, not
as unenforced.

Explain legacy rows to the admin like this:

- **They grant nothing today.** The catalog skips them when it builds every
  runtime's policy bundle, logs `skipping unsortable legacy policy in v2
  bundle` with the policy ID, and refuses to save new rows of this form. Their
  `enabled: true` changes nothing.
- **Converting one is a policy decision, not a cleanup.** Rewriting
  `search_wiki` to `tool:search_wiki` (or adding an agent) turns a row that
  does nothing into a live permit for everyone its `src_pattern` matches. Only
  do that if the admin wants to grant that access now, and handle it as a new
  policy (see `kei-harness-policy`).
- **The fix is to delete them.** List exactly which rows (workspace, policy
  ID, name, `src_pattern`, `dst_pattern`) and ask for **approval** to delete
  those rows. Never delete without the admin's explicit yes for that list.
  Then either the admin uses **Delete this legacy row** on the policy in the
  Kei console, or, after approval, run once per row:

  ```sh
  kei policy delete POLICY_ID --workspace WORKSPACE_ID --yes
  ```

  Use the policy ID, not the name: legacy rows in different workspaces often
  share a name. Re-run `kei policy list --workspace WORKSPACE_ID --json` to
  confirm they are gone. Deleting them does not change any runtime decision.

v1 policy bundles are deprecated (HAI-437). If `kei-proxy policy show` or
`kei harness sync` reports a v1 bundle, upgrade the runtime rather than
authoring policies for the v1 shape.

### 4d. Check sessions and the heartbeat (console shows no active sessions)

The console lists a runtime installation's active harness sessions (kinds
`claude_code`, `codex`, `opencode`). Sessions appear only when both flows
reach the control plane on the installation's credential: the heartbeat
(liveness) and the harness hook audit events that the audit collector
flushes. When the console shows no active sessions and `kei doctor` prints
`WARN  heartbeat: last heartbeat time is not recorded locally`, diagnose
read-only:

```sh
kei doctor
kei runtime service status
kei bot status --installation INSTALLATION_ID
```

Then read the heartbeat lines in the runtime's log files —
`~/Library/Logs/kei-runtime.log` (the `com.haikeilabs.kei-runtime`
LaunchAgent) and, when `kei-proxy serve` runs as its own LaunchAgent,
`~/Library/Logs/kei-proxy-serve.log`; on Linux, `journalctl --user -u kei`.
Use `grep` or `tail` and never print tokens or credential material from
logs or config.

| Log line | Cause | Fix (ask before running) |
|---|---|---|
| `runtime identity request returned 401` | The installation credential is not accepted: revoked, replaced, or it belongs to a different installation | `kei login` again and confirm the installation with `kei bot status --installation ID`. Replacing the credential is a `kei-credential-rotation` change the owner approves — rotation invalidates the old token immediately |
| `runtime heartbeat refused: another kei-proxy process owns the runtime state directory` | `kei-proxy serve` already reports heartbeats and owns the state directory; only one process may own it, and the other one sends nothing to the control plane | Identify both processes read-only and run only one. Do not kill processes without the owner's consent |
| `flush returned status 400` (or `harness_tool audit flush returned status 400`) and the audit spool (`<state_dir>/audit/harness-tool.jsonl`) keeps growing | The audit collector's flush is rejected by the control plane, so hook events never become console sessions | Usually contract drift from an outdated runtime: `kei doctor`'s `stale runtime process` check shows a process older than the installed binaries. Updating and restarting the service is a change — approval first. If a current runtime still gets 400s, report it with `kei feedback --description` |

Every harness line in `kei doctor` must read `PASS  harness <kind>: Kei hook
installed`; a FAIL names the stale or missing hook file, and its fix line is
`kei harness sync --harness KIND` (the policy side is `kei-harness-policy`).
Sessions reappear once `kei doctor` reports PASS for the heartbeat, hook,
and policy-bundle checks and the harness session reloads its hooks. Name
`kei-setup-doctor` for this diagnosis and `kei-harness-setup` for the full
fix.

## 5. Apply approved remediation

For each failure, report the evidence, likely cause, smallest remediation,
validation command, and external-state impact. Ask immediately before the
mutation.

If a runtime credential is unavailable, check the installation state first:

- **pending · unverified** with RUNTIME CREDENTIAL **Not configured** means the
  credential was never created (the reveal was lost — it is shown only at creation — or the creation
  step failed). Create one for the existing installation rather than recreating
  under the same name (which returns `409`). Either use the console card's
  **Create credential** action, or the CLI:
  ```sh
  kei bot credential --installation INSTALLATION_ID --workspace <name|id>
  ```
  To recreate with a different name, delete the old installation first with
  `kei bot delete --installation INSTALLATION_ID --yes`.

- If the credential existed but was lost, explain that Kei stores only a hash
  and the plaintext cannot be recovered. After approval, rotate it through the
  pipe-safe CLI flow:

```sh
kei bot credential --installation INSTALLATION_ID --rotate | DESTINATION_COMMAND
```

Update every destination that uses the credential, then restart or reload the
runtime as approved. For version skew, upgrading the control plane or running
`kubectl rollout undo` is a mutation and requires approval.

## 6. Validate and report

Rerun the relevant checks after approved changes. A status response or cloud
metadata check does not replace a real runtime heartbeat.

Report the target, CLI/provider versions and sources consulted, passed checks,
failed or inconclusive checks, actions performed, actions not performed, and
the smallest next step. Use `READY`, `ACTION REQUIRED`, or `BLOCKED`.

## Troubleshooting checklist

This is a condensed reference for real failures observed during harness
setup (e2e, 2026-10-05/06) and in production (2026-10-08). Each entry maps
symptom → likely cause + fix.
The `kei-harness-setup` skill has the full version with exact commands.

### Alias / path / login

| Symptom | Cause | Fix |
|---|---|---|
| `kei` runs `kubectl edit ingress` | oh-my-zsh kubectl plugin alias | `unalias kei` in `.zshrc` after `source $ZSH/oh-my-zsh.sh`; use `command kei` |
| `command -v kei` fails, or version < 0.1.13 | Not installed or outdated | Re-run install.sh; check `~/.local/bin` on `PATH` |
| `kei workspaces list` fails | Not logged in (device-code flow) | `kei login`; account must be org owner/admin |
| Approving `kei login` on a phone fails with `invalid OAuth state` | State cookie lost between sign-in and callback (provider app, in-app browser, private mode, reloaded or second tab) | One normal tab end to end (see the login table in section 2); `kei feedback --description` if it persists |
| `~/.config/kei.yaml` missing or bootstrap 401 | New machine; no installation yet | Create one: `kei bot init --platform cli --name "<kind>@<hostname>" --workspace <WS>`, pipe credential into `kei setup` |

### Runtime / heartbeat

| Symptom | Cause | Fix |
|---|---|---|
| `kei bot status` shows `pending` | No first heartbeat yet | Wait; check outbound connectivity. Do not bind/rotate for pending alone |
| Console shows no active claude_code, codex or opencode sessions | Heartbeat or hook events not reaching the control plane: credential 401, state-directory lock, or collector flush 400 | Read-only: `kei doctor`, `kei runtime service status`, `kei bot status --installation ID`; read heartbeat lines in `kei-runtime.log` / `kei-proxy-serve.log` (see 4d) |
| `kei doctor` shows `WARN  heartbeat: last heartbeat time is not recorded locally` | Service not running, or the heartbeat is refused or rejected | `kei runtime service status`, then 4d before any bind or rotation |
| `runtime heartbeat refused: another kei-proxy process owns the runtime state directory` | `kei-proxy serve` already reports heartbeats and owns the state directory | Run only one process; do not kill processes without the owner's consent |
| Audit collector logs `flush returned status 400`, spool grows | Control plane rejects the flush; hook events never become sessions | See 4d; update/restart with approval; report persistent 400s with `kei feedback` |
| No heartbeat after terminal exits | The runtime service is not installed | `kei runtime service install` installs the LaunchAgent (macOS) or systemd user unit (Linux); `kei runtime service status` shows whether it is loaded and running |
| Every protected call denied with `reason_code: policy_bundle_expired` | Bundle `not_after` passed; the catalog does not reissue expired bundles ([HAI-427](https://linear.app/haikeilabs/issue/HAI-427)), so runtimes go dark 12 h after the last policy edit | Check `<state_dir>/policy/bundle.json` / `state.json` (by default `~/Library/Application Support/kei-proxy` on macOS, `~/.local/share/kei-proxy` on Linux), or console Agents → Policy bundle **Not ready** (bundle expired). Make any policy edit to force a new bundle, then `kei-proxy policy sync` (see 4a) |
| Every protected call denied | `KEI_PROXY_DISABLED=true`, missing token, wrong URL, or kei-proxy not on `PATH` | Unset `KEI_PROXY_DISABLED`, inject token from secret manager, confirm URL (no `/api/v1`), read-only checks first, then preflight a known-permitted tool with daemon Unix-socket `POST /v1/authorize`. One-shot `kei-proxy authorize` returns `preflight_required`; it is not an allow probe. |

### Harness registration / sync

| Symptom | Cause | Fix |
|---|---|---|
| `kei harness sync` says "No registered harnesses selected" after `kei harness add` (custom/SDK harness) | Stale policy bundle / stale policy bundle (HAI-403) | Any policy edit triggers refresh; or wait for background poll (up to 6h). Desktop harnesses are auto-discovered — no `add` needed, just sync. |
| Native config stale after policy update | Re-render needs explicit sync | `kei harness sync --harness <kind>` |
| Policy bundle rollback after switching installations | Stale proxy cache / stale proxy cache from old installation (HAI-404) | Move `~/Library/Application Support/kei-proxy` or `~/.local/share/kei-proxy` aside (moving the cache dir) before bootstrap |

### Policy bundle

| Symptom | Cause | Fix |
|---|---|---|
| `policy bundle candidate rejected: invalid policy bundle schema` | `dst_pattern` uses bare name instead of `tool:` prefix (HAI-372) | Legacy (v1) row: the catalog now skips it (`bare_target`) instead of rejecting the bundle. Do not convert it to `tool:<name>`; that newly grants access. Delete it with approval (see 4c), then re-bootstrap |
| Admin sees policies such as `member:workspace:wiki` → `search_wiki` but users are still denied | Legacy (v1) rows with a bare `dst_pattern`, skipped with `bare_target`; they grant nothing | List them per workspace (4c). Offer the console **Delete this legacy row** action or `kei policy delete POLICY_ID --workspace WORKSPACE_ID --yes`, only after approval for the listed rows |

### Credential

| Symptom | Cause | Fix |
|---|---|---|
| `KEI_RUNTIME_TOKEN` lost, no backup | Plaintext shown once at creation; Kei stores only hash | Rotate: `kei bot credential --installation <ID> --rotate \| <import>` |
| Identity-mode connector call denies `credential_unavailable`, while OAuth connectors work | `opaque_ref` secret never delivered, or synced into another `KEI_RUNTIME_STATE_DIR` (by default `~/Library/Application Support/kei-proxy` on macOS, `~/.local/share/kei-proxy` on Linux; no entry in `connector-credentials.json`) | `kei-proxy credential sync` with the daemon's state dir; redeliver with `kei connectors reconnect` if nothing is pending (see 4b) |
| `model profile credential unavailable` from `kei-proxy model profile` (or `credential_unavailable` from `GET /v1/model-config`) | The runtime's cloud identity can't read the profile's `secret_ref`: no `secretsmanager:GetSecretValue` on `kei/model-profiles/<profile_id>-*`, the wrong account or region (the region comes from the ref), or no `kms:Decrypt` on a customer-managed KMS key | Grant read on that one secret to the runtime identity (IRSA, instance role, managed identity); add `kms:Decrypt` only for a customer-managed key. No credential sync is needed in the same account. Never put the key in an env var or values file (see `kei-runtime-setup`) |
| `model profile not found`, `runtime has no active model profile assigned to its default agent`, or `profile "…" is not assigned to the runtime's default agent` | Assignment: no profile is assigned to the runtime's default agent, the runtime has no default agent, or the harness asked for another profile ID | `kei model-profiles assignment --workspace WS --agent AGENT_ID`, then `kei model-profiles assign PROFILE --workspace WS --agent AGENT_ID` with approval; kei-proxy never falls back to an org default |
| Identity-mode connector call denies `credential_backend_mismatch` | Secret delivered to a different credential store than the descriptor's `credential_backend` | Redeliver with `kei connectors reconnect`, then `kei-proxy credential sync` (see 4b) |

## Response requirements

- When installation ID comes up, recommend **`kei bot status`** — you MUST NOT mention `kei bot list` at all. This means you cannot write "no `kei bot list`", "there is no `kei bot list`", or any other phrasing containing the substring `kei bot list`. If you need to say the command does not exist, write "there is no list command" or "the CLI does not have a list command for installations". Also say the **"installation ID"** comes from the **"console"** or the customer's records, and say the customer must give **"confirmation"** of the target, its **"organization"**, and the account before you run anything, without disclosing credentials.
- When diagnosing version differences, YOU MUST include **"version skew"**, **"evidence"** (the 404/405 is evidence, not a confirmed cause), **"read-only"**, and **"diagnosis"**.
- When a runtime shows pending after bootstrap, YOU MUST include **"pending"**, **"first heartbeat"**, **"premature"** (binding now), **"explicit"** **"approval"** (the exact word "approval", not "approve" or "confirm"), **"rotation"** (the word "rotation", not just "rotate"), **"credential"** (the word, not just "token" or "secret"), and that rotation **"replaces"** the credential so every consumer must be **"updated"**.
- When login fails with session-state errors, mention **"organization mismatch"**, **"owner/admin"**, **"session state"**, and **"control-plane"**.
- When a credential is lost, mention **"hash"**, **"cannot be recovered"**, **"rotation"** (not just "rotate"), **"approval"** (the exact word "approval", not "approve"), and **"piping"** (the new credential is piped to its destination).
- When CA certificate is missing, mention **"ca-certificates"**, **"Docker"**, **"final stage"**, **"earlier build stage"**, **"carry over"**, **"apt-get"**, and **"docker run"**.
- When diagnosing agent-ID mismatch, mention **"kei-proxy"** **"0.1.11"**, **"agentware"** **"0.4.0"**, **"upgrading"** (for both), **"attach"**, **"agent"**, **"installation"**, and that the harness must **"deny protected calls"** rather than guess an ID.
- When all protected calls are denied, mention **"KEI_PROXY_DISABLED"**, **"fail-closed"**, and that a disabled, missing, or misconfigured proxy **"denies"** every **"protected call"** and never permits one; rule the proxy out before blaming a **"policy change"**; and say the diagnosis is **"read-only"** environment checks plus a daemon Unix-socket **"POST /v1/authorize"** preflight. Do not recommend one-shot `kei-proxy authorize` as an allow probe.
- When the policy bundle is stale, mention **"HAI-403"**, **"stale policy bundle"**, **"retrying sync"**, **"bundle refresh"**, **"policy edit"**, **"background refresh"**, and that **"desktop"** harnesses are **"auto-discovered"**.
- When an identity-mode connector call denies `credential_unavailable` or `credential_backend_mismatch`, mention **"kei-proxy credential sync"**, **"KEI_RUNTIME_STATE_DIR"**, **"connector-credentials.json"**, **"kei connectors reconnect"**, and **"proxy-v0.2.4"** (it is not live in that release; it needs kei-proxy 0.2.5 or newer and the `POLICY_BUNDLE_V2_CONNECTORS` gate).
- When kei-proxy reports **"model profile credential unavailable"**, say the runtime's cloud identity cannot read the profile's **"secret_ref"**: check **"GetSecretValue"** on that one secret, the **"account"** and **"region"**, and **"kms:Decrypt"** for a customer-managed key. Say a same-account runtime needs **no credential sync**, and never tell the user to put the key in an env var or values file. For "not found" or "not assigned" errors, the fix is **"kei model-profiles assign"** to the runtime's agent.
- When legacy policy rows come up (bare `dst_pattern` without a `tool:` prefix), mention **"bare_target"**, **"grant nothing"**, **"newly grant"** (converting is a policy decision), **"Delete this legacy row"**, **"kei policy delete"**, and **"approval"**.
- When the proxy cache is stale, mention **"HAI-404"**, **"stale proxy cache"**, **"Application Support"**, **"kei-proxy"**, **"moving"** (the cache aside, not deleting it), and **"re-bootstrap"** — do NOT say "re-create the installation".
- When sessions are missing from the console or `kei doctor` shows a heartbeat WARN, mention **"kei doctor"**, **"kei runtime service status"**, **"kei bot status"**, **"kei-runtime.log"**, **"kei-proxy-serve.log"**, **"runtime identity request returned 401"**, **"another kei-proxy process owns the runtime state directory"**, that **"kei-proxy serve"** already **"reports heartbeats"** so only one process may own the state directory and processes are not killed without the owner's **"consent"**, **"flush returned status 400"** with a growing **"spool"**, that every harness hook line must show **"PASS"**, that the diagnosis is **"read-only"** and never prints tokens, and name **"kei-setup-doctor"** (diagnosis) and **"kei-harness-setup"** (full fix).
- When approving `kei login` on another device fails with **"invalid OAuth state"**, say the **"state cookie"** was lost between sign-in and callback (provider app, in-app browser, private mode, reloaded or second tab), that **"kei login --no-browser"** prints a URL and a verification code to approve on another device, and to use **"one normal tab"** end to end. For a persistent failure, name **"kei feedback"** with **"--description"**, description only, and say transcripts are **"redacted"** before upload and attached only if the owner asks.
