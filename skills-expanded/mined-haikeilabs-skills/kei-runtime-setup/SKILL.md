---
name: kei-runtime-setup
description: Stand up a customer-hosted Kei runtime end to end — create the runtime installation, deliver its credential (shown once) to a secret manager, configure `kei-proxy` beside the harness, bootstrap, keep heartbeats running, and bind. Use whenever someone is installing, configuring, containerizing, bootstrapping, or first-activating a Kei runtime, kei-proxy, or kei-connector-runtime, or asks what KEI_RUNTIME_* variables to set, or about credential sync, KEI_CREDENTIAL_SYNC_KEY_ID, Azure Key Vault or managed identity for the runtime, or how a deployed runtime and its harness use a Kei model profile (IAM to read its secret_ref, `kei-proxy model profile`), even if they only say "get the bot talking to Kei" or "set up the proxy". For diagnosing an installation that already exists and is misbehaving, use kei-setup-doctor instead.
---

# Set up a Kei runtime

A Kei runtime is the tenant-side half of Kei. The control plane keeps policy,
connector metadata, and redacted audit metadata; the runtime makes the live
allow/deny decision and executes allowed work locally, so provider payloads,
results, and credentials never enter Kei. This skill takes a runtime from
"nothing" to "bound and heartbeating".

The order, start to finish (sections 0–8 below have the commands):

1. `kei login`: an org owner or admin approves the device flow in a browser.
2. `kei bot init` creates the runtime installation.
3. Pipe `kei bot credential` straight into the secret manager.
4. Configure the runtime: `kei setup` on a workstation, or `KEI_RUNTIME_*`
   environment variables on a deployed runtime.
5. Bootstrap with `kei-proxy runtime bootstrap`. On a workstation,
   `kei runtime bootstrap` runs the configured `kei-proxy` for you.
6. Keep kei-proxy runtime heartbeat running: `kei-proxy runtime heartbeat`
   beside a one-shot CLI harness, or `kei-proxy serve`, which sends the
   heartbeat itself. Name the `kei-proxy` binary when you give this step; it
   is the runtime on every path.
7. Bind with `kei bot bind` only after the first heartbeat is reported.
8. Confirm a call without a matching tool permit is denied (fail closed).

## Concepts

- **Harness** — software that lets an LLM act as an agent (for example Claude
  Code, OpenCode, or a custom bot).
- **Kei-enabled harness** — a harness with Kei policies through a **runtime
  installation**.
- **Runtime installation** — Kei's record for the one runtime deployed beside
  that harness (one harness : one runtime installation : one credential,
  `KEI_RUNTIME_TOKEN`). The console page is called **Runtime installations**.
- **Agent** — an LLM configuration the harness runs (model, system prompt,
  tools).

This is a workflow skill that uses both Kei executables: `kei`, the platform
admin CLI a person runs (command reference: **`kei-cli`**), and `kei-proxy`,
the runtime the harness runs for agent interaction (command reference:
**`kei-proxy`**). This skill decides the order and the checks between them.

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Installed binaries | `kei help`, `kei-proxy help`, `kei-proxy runtime --help` | Exact subcommands, flags, env vars for the installed versions |
| Docs: CLI authentication and identity | `https://docs.haikeilabs.com/kei/reference/cli` | Login, installations, `kei setup`, credentials |
| Docs: Configure the tenant-side proxy | `https://docs.haikeilabs.com/kei/runtime/tenant-runtime` | Runtime env vars, bootstrap output, container build |
| Docs: Agent setup | `https://docs.haikeilabs.com/kei/connect-your-harness/harness-setup` | Harness → runtime → policy catalog flow, DENY rules |

Append `.md` to any docs page URL for the raw page.

When this skill and the binaries' help disagree, trust the binary and tell the
user.

## Two binaries, two jobs

| Binary | Role | Who runs it | Auth | What it does |
| --- | --- | --- | --- | --- |
| `kei` | Platform admin | An org owner/admin, on their workstation | `kei login` (browser device flow) | Logs in, creates installation metadata, emits the runtime credential, writes local runtime config, binds |
| `kei-proxy` | Runtime for agent interaction | The harness, as a subprocess, inside the runtime | `KEI_RUNTIME_TOKEN` env | Bootstraps the installation, sends heartbeats, authorizes each protected tool call |

Steps 0–3 and 7 below are admin work with `kei`. Steps 4–6 configure and
bootstrap the runtime: on a workstation with `kei setup` + `kei runtime
bootstrap` (which drive the bundled `kei-proxy` for you), in a deployed runtime
with `kei-proxy` directly. Step 7 is the runtime answering real calls. The
runtime never needs `kei login`.

Protected tool calls are decided on the same host as the harness. `kei-proxy`
supports two modes:

- **One-shot CLI** — the runtime invokes `kei-proxy authorize` as part of its
  execution flow. Do not use it as an allow probe: v2 returns
  `preflight_required`.
- **Daemon mode (opt-in)** — `kei-proxy serve` runs as a long-lived daemon
  exposing HTTP over a Unix socket (`KEI_RUNTIME_SOCKET_PATH`). The normal
  deployment is a same-host daemon (bare metal) or a same-container daemon
  (Docker); on Kubernetes it can run as an optional same-pod companion
  container. The socket default is `$TMPDIR/kei-proxy/runtime.sock` on macOS
  and `/run/kei-proxy/runtime.sock` on Linux (`KEI_RUNTIME_SOCKET_PATH`
  overrides both). The daemon serves readiness (`/healthz`, `/readyz`) and
  protected `POST /v1/authorize` plus `PUT`/`DELETE /v1/session` routes on the owner-only
  socket. Use its `POST /v1/authorize` route to preflight whether a tool call
  is allowed. The decision is made **locally** by the runtime PDP against the
  synced policy bundle (no per-call catalog round trip), and a background
  refresher keeps the bundle current (see "Keep the heartbeat running"). Model
  inference does not go through kei-proxy.

See the `kei-proxy` skill for the full CLI/daemon comparison and the socket
contract (`docs/unix-socket.md` in the kei-connector-runtime repo). Do not
design a network-exposed listener or bind a port for protected calls outside of
the validated daemon contract.

## Before you start

- The organization already exists; create it in the console/API (there is no
  `kei org` command). Workspaces can be created with
  `kei workspaces create --name NAME` or discovered with `kei workspaces list`.
- The operator is an org `owner` or `admin`. Anyone else is refused at login
  with `403 organization administrator role is required`.
- The `kei` CLI is installed (see the `kei-cli` skill) and `kei --version`
  works.
- The customer has a secret manager the runtime can read from. The runtime
  credential goes there and nowhere else.

## 0. Log in first

Every `kei bot …` command (`init`, `credential`, `agents`, `status`, `bind`,
`delete`) calls the control plane with the operator's CLI token, so run
`kei login` before any of them:

```sh
kei login                                       # add --no-browser when headless
```

It is a browser device flow: the CLI prints a URL and a verification code, an
org owner/admin approves it in a signed-in browser, and the token is stored in
the OS keychain — never printed, never in a config file. Things that trip
people up:

- The token is bound to the organization chosen at approval and to the API URL
  host. Logging in to one environment does not log you in to another; log in
  again per environment.
- The token is short-lived. A `not logged in; run kei login first` error, or a
  401 partway through a long session, means log in again and retry.
- An agent cannot approve the device flow for the user. Run `kei login`, show
  the user the URL and code, and wait for them to approve before continuing.
- `kei setup`, `kei runtime bootstrap`, and everything `kei-proxy` does
  authenticate with the **runtime token**, not the login token — a runtime
  never needs `kei login`.

## 1. Create the installation

One installation per customer-owned runtime boundary. It is the identity used
for bootstrap, heartbeats, policy delivery, and audit context — separate from a
user login.

From the CLI (after `kei login`):

```sh
kei bot init --platform cli --name "Acme local runtime"
```

`--platform` takes `cli`, `teams`, `discord`, `slack`, `whatsapp`, or
`openwebui` (the last two since v0.1.15); confirm with `kei help` because older
releases and the console docs list only `teams|discord|slack`. Use `cli` for a local coding harness runtime. Record the
returned `installation_id` — it is not secret.

From the web app instead: **Agents → Runtime installations → Create**. The
console creates the installation and reveals the credential in a single step
(atomic create+credential). Copy the credential immediately — it is shown once
only.

## 2. Discover the workspace

The credential must be scoped to a workspace. If you don't know the workspace
name or ID, list them from the CLI:

```sh
kei workspaces list
```

`--workspace` on `bot credential` accepts a workspace name or ID. Using the
name is fine — the CLI resolves it server-side.

## 3. Deliver the credential to the secret manager

The runtime credential is shown or emitted once. Send it straight into the
secret manager so it never lands in a terminal, a transcript, a file in the
repo, or a command-line argument:

```sh
kei bot credential --installation INSTALLATION_ID --workspace WS | <your secret-manager import command>
```

`--workspace` accepts the workspace name or ID. If omitted, the credential is
scoped to the installation's existing workspace (set at creation time). The CLI
refuses to write the credential to an interactive terminal; that refusal is the
guard working, not a bug to route around. If the installation already has a
credential the command fails with
`bot credential already exists; use --rotate to replace it` — that is a
rotation, and rotation breaks the running runtime immediately, so load
`kei-credential-rotation` before using `--rotate`.

### Recovery: installation stuck in "pending · unverified"

If the credential was never received (lost the reveal — it is shown only at creation) or the creation
step failed, the console shows **pending · unverified** with RUNTIME CREDENTIAL
**Not configured**. Recover by creating a credential for the existing
installation — do not recreate the installation under the same name (that
returns `409`). Either:

- **Console:** open the installation card's **Create credential** action.
- **CLI:** `kei bot credential --installation INSTALLATION_ID --workspace <name|id>`.

To recreate with a different name, delete the old installation first:
`kei bot delete --installation INSTALLATION_ID --yes`.

The web reveal shows `KEI_RUNTIME_CONTROL_PLANE_URL`, `KEI_RUNTIME_TOKEN`,
and the bootstrap command. `KEI_CREDENTIAL_STORE_INSTALLATION_ID` (the
**credential-store installation ID** (an installation used for secret-sync routing)
is **not** in the reveal — find it on the **Credential store** page or via
`kei credential-store get`. A runtime that receives model-profile API keys or
connector secrets through credential sync needs it: bootstrap registers the
runtime's sync key only when it is set (see
[Credential store and credential sync](#credential-store-and-credential-sync)).
A runtime that never receives synced secrets doesn't.

## 4–6. Configure and bootstrap — pick your path

There are two supported paths. They end in the same place (the installation
verified and heartbeating); they differ in where the runtime settings live.

| | **Workstation / local harness (current default)** | **Deployed runtime — one-shot CLI** | **Deployed runtime — daemon (same-host / same-container)** |
| --- | --- | --- | --- |
| Get `kei-proxy` | Comes with `kei`: since kei-cli v0.1.4 the release installer also installs a pinned `kei-proxy` next to `kei` | Build `kei-proxy:local` from the Kei repo (below) or copy the bundled binary into the image | Same as one-shot CLI; the daemon is the same binary invoked via `kei-proxy serve` |
| Settings live in | `~/.config/kei.yaml` (mode `0600`), written by `kei setup` | Harness process environment, from the secret manager | Harness process environment; daemon inherits `KEI_RUNTIME_SOCKET_PATH` |
| Bootstrap with | `kei runtime bootstrap` | `kei-proxy runtime bootstrap` | `kei-proxy runtime bootstrap` before starting `serve` |
| Check whether a protected call is allowed | `POST /v1/authorize` over daemon Unix socket | `POST /v1/authorize` over daemon Unix socket | `POST /v1/authorize` over daemon Unix socket (local PDP) |

### Path A: workstation — `kei setup` then `kei runtime bootstrap`

```sh
<secret-manager read> | kei setup --control-plane-url https://app.haikeilabs.com --harness-url http://127.0.0.1:8088
kei runtime bootstrap   # verifies the installation and sends the first heartbeat
```

- Feed the token to `kei setup` on stdin straight from the secret manager
  (for example `op read …`, `aws secretsmanager get-secret-value … --query
  SecretString --output text`), so no one copies or pastes it. When stdin is
  not a terminal, `kei setup` reads the token as the first line and uses
  defaults for anything else not given as a flag. Run interactively, it
  prompts with hidden input instead. Avoid `--runtime-token`: it lands in shell
  history and the process list.
- `kei setup` verifies the token against the control plane before saving.
  Use `--config PATH` for a separate environment.
- `kei runtime bootstrap` loads that config and runs the local `kei-proxy
  runtime bootstrap`, passing the URL and token in the child's environment —
  the same thing the harness will do. It finds `kei-proxy` via the configured
  path, then `PATH`; override with `--proxy-path`.
- Neither command needs `kei login`; they use the runtime token, not the admin
  login.

### Path B: deployed runtime — environment + `kei-proxy runtime bootstrap`

Set these on the harness process; `kei-proxy` inherits them as a child process:

```text
KEI_RUNTIME_CONTROL_PLANE_URL=https://YOUR_KEI_GATEWAY
KEI_RUNTIME_TOKEN=<loaded from the secret manager>
KEI_RUNTIME_VERSION=<your deployed runtime version>
KEI_SECRETS_BACKEND=aws-secrets-manager   # required by kei-proxy >= 0.7 to read model-profile/connector secrets
```

`KEI_SECRETS_BACKEND` must name the configured secret backend (for example
`aws-secrets-manager`; use the value matching the runtime's secret store).
Kei-proxy 0.7+ requires it when reading model-profile or connector secrets.

- The control-plane URL is deployment-specific. Production and staging must be
  HTTPS. Do not append `/api/v1`; the runtime adds its own paths.
- Load `KEI_RUNTIME_TOKEN` from the secret manager or a protected env file,
  never from an argument.
- Do not supply an org, tenant, or workspace ID as scope. The token determines
  installation, organization, and workspace.

To build a container, use the private `HaikeiLabs/kei` repository, from its
root (the Dockerfile copies from both `cmd/kei-connector-runtime/` and
`contracts/connectors/`):

```sh
docker build -f cmd/kei-connector-runtime/Dockerfile -t kei-proxy:local .
```

The image contains only `kei-proxy`; add the harness to the same image. No
public `kei-proxy` image is published; do not invent a registry URL. When
someone asks for a sidecar "listening on a port", answer with all three:

1. There is no image to pull; build `kei-proxy:local` as above.
2. The runtime may use the one-shot CLI execution flow or the long-running
   daemon (`kei-proxy serve`), which runs on the same host or container.
3. To check whether a tool call is allowed, use the daemon's `POST
   /v1/authorize` route over its Unix socket (decided locally by the runtime
   PDP), not TCP. One-shot `kei-proxy authorize` returns `preflight_required`
   and is not an allow probe.

Then, in the runtime, before the harness accepts work:

```sh
kei-proxy runtime bootstrap
```

#### Optional: run as a daemon (same-host or same-container)

For v2 policy preflight, the harness can use `kei-proxy serve` as a long-lived
daemon. The normal deployment is a same-host daemon (bare metal) or a
same-container daemon (Docker); on
Kubernetes it can run as an optional same-pod companion container. The daemon
communicates over a Unix domain socket. This is optional and opt-in.

The socket default is `$TMPDIR/kei-proxy/runtime.sock` on macOS and
`/run/kei-proxy/runtime.sock` on Linux; set `KEI_RUNTIME_SOCKET_PATH` to
override. In a Kubernetes pod, mount an `emptyDir` volume at the socket
directory path so the harness and the companion container can access it. The
socket file mode is `0600` — both must run as the same UID.

```sh
# Start the daemon after bootstrap
kei-proxy serve
```

The daemon serves readiness (`/healthz`, `/readyz`), and a protected
`POST /v1/authorize` plus `PUT`/`DELETE /v1/session` on the owner-only socket.
Model inference does not go through kei-proxy. The authorize decision is made
locally from the synced policy bundle; a background refresher polls the bundle
and swaps in updates. Kei-proxy 0.9.1+ refreshes its identity after an agent
workspace move, so a runtime using `serve` does not need a restart or
`kei-proxy policy sync --force` after the move. For older kei-proxy versions,
restart the runtime and force a policy refresh after the move.

The daemon also accepts `KEI_PROXY_LISTEN_ADDR` (TCP, default `:8085`) for
existing same-container OpenWebUI deployments that cannot use a Unix socket;
the protected authorize and session routes are **socket-only** (the TCP
listener returns 404 for them). See `docs/unix-socket.md` in the
kei-connector-runtime repo for the full socket contract.

#### Use a model profile from a deployed runtime

Kei returns profile **metadata** only: `endpoint`, `default_model`,
`auth_type`, `secret_backend` and `secret_ref` (for example
`aws-secrets-manager://us-east-1/kei/model-profiles/<profile_id>`). The key
never passes through Kei (ADR-011). With `auth_type: api_key`, kei-proxy reads
the key **itself** from `secret_ref`, using the runtime's cloud identity (IRSA,
an instance role, a managed identity). The region comes from the ref, so no
extra environment is needed.

Which path applies:

| Runtime | What it needs |
|---|---|
| Same cloud account as the credential store | **Read on that one secret.** No sync key, no delivery, no write. |
| Its own, different store | Credential sync (next section) to deliver a new or rotated key into that store. |

Set `KEI_SECRETS_BACKEND` to the backend configured for the runtime (for
example `aws-secrets-manager`); kei-proxy >= 0.7 requires this setting to read
model-profile or connector secrets.

The AWS statement for the same-account case (read only, one secret):

```json
{
  "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": "arn:aws:secretsmanager:<region>:<account>:secret:kei/model-profiles/<profile_id>-*"
}
```

The default AWS-managed KMS key needs no grant; a customer-managed key also
needs `kms:Decrypt` on that key.

**Harness pattern.** Never hardcode the endpoint or the key, and never put the
key in an env var, values file or image. Ask kei-proxy at run time:

- `kei-proxy model profile` (JSON on stdout), or `GET /v1/model-config` on the
  `kei-proxy serve` socket. Both resolve the profile **assigned to the
  runtime's default agent**, never an org default. Assign it with
  `kei model-profiles assign PROFILE --workspace WS --agent AGENT_ID`.
- Refresh periodically (the Pedro harness uses 300 s) so a reassignment or
  rotation is picked up.
- Fail closed when the profile is required: no profile, no model call. Don't
  fall back to a hardcoded model.
- Check that the endpoint host resolves before swapping in a new config. An
  endpoint on a tailnet (for example
  `https://spark-f5ea.<tailnet>.ts.net/v1`) needs network egress from the
  runtime to that tailnet.

Inference does not go through kei-proxy; the harness calls the provider
directly. If kei-proxy says `model profile credential unavailable` or the
profile is not assigned, see `kei-setup-doctor`.

#### Credential store and credential sync

Credential sync **delivers** a new or rotated model-profile key or connector
secret into a runtime's **own** store. A runtime in the same cloud account as
the credential store doesn't need it (see above). Everything stays in your
environment:
1. When an admin sets or rotates a key, the control plane seals it to the
   runtime's public sync key and queues a delivery.
2. `kei-proxy credential sync` claims the delivery, opens it with the private
   sync key, writes it to **your** secret store, and acknowledges it.
3. kei-proxy reads it from that store when it calls the model or connector.

Kei never holds the private sync key, and plaintext stays in the container
and the vault. Delivering **model-profile keys** this way is live. Only
identity-mode `opaque_ref` connectors are gated (see below).

**1. Create the credential store** (org owner/admin, once):

```sh
# Azure Key Vault
kei credential-store put --secret-backend azure-key-vault \
  --backend-config '{"key_vault_uri":"https://<vault>.vault.azure.net"}'
kei credential-store get    # shows the store and its installation ID
```

The runtime only accepts Azure secret references of the form
`https://<vault>.vault.azure.net/secrets/<name>[/<version>]`. Other backends
are `aws-secrets-manager` and `gcp-secret-manager`; check `kei credential-store
put --help` for flags.

**2. Generate the sync key pair.** kei-proxy has no keygen command.
- `KEI_CREDENTIAL_SYNC_PRIVATE_KEY` is a **raw 32-byte X25519 private key,
  base64-encoded** (padded or unpadded).
- `KEI_CREDENTIAL_SYNC_KEY_ID` is a free-form identifier. Keep it stable and
  unique per installation (for example `chat-sync-1`), and use a new ID when you
  rotate the key.

Generate the key straight into your secret manager so it's never printed.
This needs OpenSSL 3 (macOS LibreSSL may not support X25519). The last 32 bytes
of the DER output are the raw key:

```sh
openssl genpkey -algorithm X25519 -outform DER | tail -c 32 | base64 \
  | <your secret manager's write-from-stdin command>
```

Inject it into the runtime as a secret-referenced environment variable, the
same way as `KEI_RUNTIME_TOKEN`.

**3. Registration is automatic.** `kei-proxy runtime bootstrap` derives the
public key and registers it with the control plane itself (`PUT
/api/v1/runtime/credential-sync-keys`), and `kei-proxy runtime heartbeat`
repeats the same idempotent registration. There's no separate registration
step. It happens **only when all three** are set:
- `KEI_CREDENTIAL_STORE_INSTALLATION_ID`
- `KEI_CREDENTIAL_SYNC_KEY_ID`
- `KEI_CREDENTIAL_SYNC_PRIVATE_KEY`

If one is missing, registration is skipped without an error and nothing is
ever sealed to this runtime.

**4. Cloud identity and permissions.**
- **Azure:** kei-proxy uses `DefaultAzureCredential`. With a
  **user-assigned managed identity**, set `AZURE_CLIENT_ID` to that identity's
  client ID; without it the credential can't pick the identity.
- **What to grant:** sync writes secrets and serve reads them, so grant
  **get and set** on secrets in that vault only. "Key Vault Secrets User" is
  read-only, which isn't enough. Use a custom role with get + set.
- **Deleting:** sync does not delete secrets. Remove an old one by hand if you
  ever need to; don't grant delete for it.
- **AWS and GCP:** kei-proxy uses the AWS default credentials chain (for
  example IRSA or an instance role) or GCP Application Default Credentials
  (workload identity). Grant the same get + set, no delete.

**5. Run sync after every key or secret change.** Supervisors don't run it for
you. For example, the openwebui-kei image's entrypoint starts bootstrap,
`serve` and heartbeat, but it does not run credential sync.
- Each run claims **one** pending delivery. Repeat until the output shows
  `"claimed": false`, e.g. after each profile or key change, or on a schedule
  next to heartbeat.
- Run it with the same `KEI_RUNTIME_STATE_DIR` as `kei-proxy serve`.
- The output names what was delivered, never the value.

```sh
kei-proxy credential sync | jq '{claimed, success}'
```

**Keep it private.**
- kei-proxy serves on a Unix socket; keep its TCP listener on loopback
  (`KEI_PROXY_LISTEN_ADDR=127.0.0.1:...`), never on an ingress port.
- Only the harness's own UI belongs behind your ingress.
- Keep the secret store on private networking.
- Never put the sync private key, `KEI_RUNTIME_TOKEN` or provider keys in argv,
  logs or an image.

#### Identity mode: deliver each `opaque_ref` secret first

Not live yet: this needs the catalog's `POLICY_BUNDLE_V2_CONNECTORS` gate
enabled and kei-proxy 0.2.5 or newer deployed (see the release status below).

With `KEI_CREDENTIAL_RELEASE=identity` the daemon holds the credential in
session memory. The harness obtains it via `POST /v1/credentials:release` over
the socket, then calls the upstream API directly. A user's own OAuth connection
(github, gmail,
google_drive, linear) loads when their session starts. An `opaque_ref`
connector works differently: an `http_api` connector such as the one named
`crm`, or notion, discord or tito. The daemon reads its secret from your
tenant secret store, and it can only find that secret if
**`kei-proxy credential sync` has already delivered it to this runtime**.

**Air-gapped-after-session-start principle (HAI-672):** Connector credentials
are loaded into the daemon's memory only after a session starts (`POST
/v1/session`). Before that the runtime holds no tenant credentials — not even
for `opaque_ref` connectors whose secrets were synced earlier. This means a
compromised runtime process cannot exfiltrate credentials unless a session is
explicitly open. Idle sessions are reaped after `KEI_SESSION_IDLE_TTL`
(default 30 minutes), which also evicts their in-memory credentials.

1. The runtime needs a credential-sync key (`KEI_CREDENTIAL_SYNC_KEY_ID`,
   `KEI_CREDENTIAL_SYNC_PRIVATE_KEY`, registered at bootstrap with
   `KEI_CREDENTIAL_STORE_INSTALLATION_ID`; see
   [Credential store and credential sync](#credential-store-and-credential-sync))
   next to `KEI_RUNTIME_TOKEN` and `KEI_RUNTIME_CONTROL_PLANE_URL`. Without a
   runtime that can receive secrets, `kei connectors create` refuses the
   secret ("set up a credential store and a runtime with a credential-sync key
   first").
2. Setting a connector secret (`kei connectors create`, or
   `kei connectors reconnect ID --workspace WS` for a replacement, with the
   value on stdin) seals it to the runtime and queues a delivery. The
   connector stays `pending` until a runtime acknowledges the delivery.
3. Run `kei-proxy credential sync` on the runtime. Each run claims one pending
   delivery, writes it to the secret store and acknowledges it. Repeat until
   the output shows `"claimed": false`. The JSON names the connector and
   field, never the value.
4. Run `credential sync` with the same `KEI_RUNTIME_STATE_DIR` as
   `kei-proxy serve`. Sync records each delivery in the connector reference
   index (`connector-credentials.json` in that directory), and that index is
   where the daemon looks the secret up. The runtime's cloud identity must be
   able to read the secret (AWS Secrets Manager or Azure Key Vault).

A connector whose secret was never delivered, or was synced into another state
directory, denies `credential_unavailable`. A secret delivered to a different
backend than the bundle names denies `credential_backend_mismatch` (see
`kei-setup-doctor`). Rotating a secret is another `reconnect` plus
`credential sync`, and does not re-issue the policy bundle.

**Release status: not live yet.** Running `opaque_ref` connectors in identity
mode needs both of these: a kei-proxy release that contains the change
(kei-connector-runtime 719866b), which is kei-proxy 0.2.5 or newer
(proxy-v0.2.4 and older don't have it), deployed on the runtime; and the
catalog's `POLICY_BUNDLE_V2_CONNECTORS` gate enabled in the control plane,
which is off by default. Only with the gate on does the control plane send
the connector descriptors. Until both are in place, those connectors deny
`credential_source_not_supported` in identity mode. Delivering the secrets
now is still the right first step.

### Check the bootstrap output (both paths)

Bootstrap prints safe JSON: `installation_id`, `org_id`, `platform`, `status`,
`binding_status`, and `workspace_id`.

When someone asks what `kei runtime bootstrap` does, cover all three: it
verifies the runtime credential against the control plane, sends the first
heartbeat, and prints the installation status; the output must include
`workspace_id`; and on a deployed runtime the same step is
`kei-proxy runtime bootstrap` (the workstation `kei runtime bootstrap` runs
the configured `kei-proxy` for you).

**If `workspace_id` is missing, stop.** The credential was minted before the
workspace boundary existed. Re-mint it (rotation) rather than using a
workspace-less credential. Do not fall back to the organization: using the org
instead of a workspace would widen the runtime's scope to org-wide, and Kei
denies rather than broadening scope.

### Keep the heartbeat running (both paths)

When someone asks what a heartbeat does or what happens during a runtime
heartbeat, answer with all three points, and use the exact command and the
words "fail closed". Include this sentence: "Run `kei bot status
--installation INSTALLATION_ID` to see the installation's heartbeat status."

1. Purpose: a periodic liveness signal that the installation is alive and
   connected.
2. How to see it: `kei bot status --installation INSTALLATION_ID` shows the
   status (`pending` until the first heartbeat).
3. Failure mode: if heartbeats stop and the policy bundle is missing,
   revoked, or expired, protected calls fail closed (every call is denied).

Ongoing liveness is the runtime's job, run under the same supervisor as the
harness:

- **One-shot CLI runtimes:** run `kei-proxy runtime heartbeat --interval 1m`
  beside the harness.
- **Daemon (`kei-proxy serve`):** the daemon sends the heartbeat itself (every
  `KEI_RUNTIME_HEARTBEAT_INTERVAL`, default `1m`). Do not also start
  `kei-proxy runtime heartbeat`; it refuses to run beside `serve` because
  `serve` owns the runtime state directory.
- **Workstation:** `kei runtime service install` (kei v0.1.14 or later)
  installs a launchd (macOS) or systemd user (Linux) service that keeps
  `kei runtime heartbeat` running; `kei runtime service status` checks that
  local service (the installation's heartbeat status is `kei bot status`) and
  `kei runtime service uninstall` removes it.

What a heartbeat does: each tick is a periodic heartbeat
(`POST /api/v1/runtime:heartbeat`) that tells the control plane this
installation is alive and connected. It is the runtime-to-catalog
**liveness** leg; a local `/healthz` or `whoami` shows readiness only. The
installation, org, and workspace come from the token, and the heartbeat body
never carries identity, credentials, provider payloads, or results. Binding
needs a reported heartbeat, and `kei bot status --installation INSTALLATION_ID`
shows the installation's status (`pending` until the first heartbeat arrives).
Failure modes: a transient catalog failure (unreachable, timeout, 5xx) is
retried once within the tick and the loop carries on; a `429` stretches the
next tick to its `Retry-After`. A revoked or rotated-away token is terminal:
the runtime removes its policy bundle and denies; re-mint the credential.
Losing heartbeats never widens access. Protected calls **fail closed**: once
the policy bundle is missing, revoked, or past its `not_after`, every call is
denied, with no fallback to an older bundle or a built-in allow.

## 7. Bind

Once the runtime has reported a heartbeat, activate it:

```sh
kei bot bind --installation INSTALLATION_ID
kei bot status --installation INSTALLATION_ID
```

Binding is deliberately explicit so a runtime cannot activate itself. Then
attach the agents this runtime serves:

```sh
kei bot agents add --installation INSTALLATION_ID --agent AGENT_ID --default
kei bot agents list --installation INSTALLATION_ID
```

Agent creation and general CRUD are not exposed by the CLI; use the console
or API to create an agent. To move an existing agent across workspaces, use
`kei agents move` (preview with `--dry-run` first; see `kei-cli`).

### Pair the runtime with a harness

`kei bot bind` takes only `--installation`; it has no `--harness` flag. A
harness is paired with the installation through `kei harness` (kei v0.1.7 or
later):

- **Desktop harnesses (Claude Code, Codex, OpenCode)** are sessions of the
  installation. They need no `kei harness add`: run `kei harness sync` (add
  `--harness KIND` for one kind, `--dry-run` to preview, `--check` to report
  drift) to render Kei policy into the harness's native config.
- **A custom (SDK) harness** is registered first with
  `kei harness add --kind custom --installation INSTALLATION_ID --agent AGENT_ID`,
  then kept current with `kei harness sync`.
- `kei harness list` shows what is paired; `kei harness remove` unpairs.

When asked how to pair a runtime with a harness, name `kei harness sync`, say
when `kei harness add` is needed first (custom harnesses only), and that
`kei bot bind --installation` activates the runtime. Per-harness detail is
in `kei-harness-setup`.

## 8. Prove it fails closed

A runtime is not set up until a denial has been observed. Run one permitted,
disposable operation and one that no policy allows (for example a connector
with no matching policy), and use the daemon Unix-socket `POST /v1/authorize`
route to check the policy decision. One-shot `kei-proxy authorize` returns
`preflight_required`; it is not an allow probe. The denied call must fail
without a provider call and produce only redacted audit metadata. Unsupported
harnesses, invalid installation scope, stale policy, and requests with no
matching policy are all explicit **DENY** — never a fallback to broader scope.

If the runtime writes local audit JSONL through `KEI_PROXY_AUDIT`, ship it:

```sh
kei-proxy collector                          # once
kei-proxy collector --poll --poll-interval 1m
```

## Validation commands

```sh
kei --version && kei help                    # confirms platform list and flags
kei-proxy help                               # confirms runtime subcommands and env vars
kei bot status --installation INSTALLATION_ID
kei runtime bootstrap | jq '{installation_id, status, binding_status, workspace_id}'        # workstation
kei-proxy runtime bootstrap | jq '{installation_id, status, binding_status, workspace_id}'  # deployed runtime
# Daemon mode: confirm socket is listening (after kei-proxy serve is running).
# Default socket: $TMPDIR/kei-proxy/runtime.sock on macOS, /run/kei-proxy/runtime.sock on Linux.
curl -s --unix-socket "${KEI_RUNTIME_SOCKET_PATH:-/run/kei-proxy/runtime.sock}" http://localhost/healthz || \
  echo "socket not ready — check KEI_RUNTIME_SOCKET_PATH and daemon logs"
# Identity mode with opaque_ref connectors: repeat until claimed is false (never prints a value)
kei-proxy credential sync | jq '{claimed, success, connector_id, field}'
kei connectors list --workspace WS           # the connector is active once its secret was acknowledged
```

## Realistic usage boundaries

- The CLI does not provision cloud infrastructure. There is no `bot install`,
  `deploy`, or `destroy` (`kei bot list` only lists installations); the
  customer owns hosting and secrets.
- `kei bot delete --installation ID --yes` removes the control-plane record and
  revokes the credential. It does not touch customer cloud resources.
- Never print, paste, commit, or pass the runtime token as an argument, and do
  not ask the user to paste it into the conversation.
- **Secrets never surface via the CLI.** `kei-proxy` never prints resolved
  credential values in output, flags, logs, audit, or errors. Values reach the
  harness only through `kei-proxy run`, which injects them into the child
  environment and masks the child's stdout/stderr. Keep values out of
  transcripts and logs.
- Registering the harness's skills and tool IDs against an installation has no
  CLI command or resource-oriented API yet; do that in the web app.
- Kei's own control plane runs on AWS EKS (production) and a Tailscale cluster
  (staging). The earlier GCP runtime was retired on 2026-08-31 and is not a
  deployment target.

## Response requirements

- Whenever an answer walks through setting up a runtime, YOU MUST name the
  `kei-proxy` binary for the bootstrap and heartbeat steps: bootstrap with
  `kei-proxy runtime bootstrap`, then keep kei-proxy runtime heartbeat
  running, then bind.
- Delivering **model-profile API keys** with `kei-proxy credential sync` is
  live: do not call it "not live". When an answer covers it, give the sync key
  format (base64 32-byte X25519), say bootstrap registers the key only when
  `KEI_CREDENTIAL_STORE_INSTALLATION_ID`, `KEI_CREDENTIAL_SYNC_KEY_ID` and
  `KEI_CREDENTIAL_SYNC_PRIVATE_KEY` are all set, and say sync must be run (one
  delivery per run) because supervisors don't run it.
- Whenever an answer covers a deployed runtime using a model profile, YOU
  MUST say which path applies: a runtime in the **same account** as the
  credential store needs only **`secretsmanager:GetSecretValue`** (AWS) on
  `kei/model-profiles/<profile_id>-*`, with **no credential sync** and no
  write; credential sync is only for delivering a key into a runtime's own,
  different store. Say the harness calls **`kei-proxy model profile`** (or
  `GET /v1/model-config`) for the profile **assigned** to the runtime's agent,
  refreshes it, and **fails closed**; never hardcode the endpoint or key.
- Whenever someone asks whether a supervisor or entrypoint (such as the
  openwebui-kei image) runs credential sync, YOU MUST start the answer with
  "No: it does not run credential sync", say to run `kei-proxy credential
  sync` yourself after each key change, and say each run claims one pending
  delivery.
- Whenever an answer covers Azure Key Vault or a managed identity for
  credential sync, YOU MUST say to set `AZURE_CLIENT_ID` for a user-assigned
  managed identity, to grant **get and set** on secrets, and to grant **no
  delete** (admins remove old secrets by hand).
- Whenever an answer covers identity-mode connector descriptors or
  `opaque_ref` connector secrets, YOU MUST say that path is not live yet: it
  needs the catalog's **`POLICY_BUNDLE_V2_CONNECTORS`** gate
  enabled (off by default) and kei-proxy **0.2.5 or newer** deployed.
