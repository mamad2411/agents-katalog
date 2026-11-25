---
name: kei-openwebui
description: Set up, verify and troubleshoot Open WebUI with Kei guardrails, using the published openwebui-kei image (Open WebUI + the in-container kei-proxy daemon + the Kei connector). Use when someone wants to run Open WebUI with Kei; create the openwebui runtime installation (`kei bot init --platform openwebui`) and deliver KEI_RUNTIME_TOKEN; grant `tool:<name>` permits for tools behind Kei guardrails; optionally configure a model profile to pass model credentials; pull or mirror the image by digest (ECR Public, `az acr import`); run it as UID/GID 10001; set KEI_OPENWEBUI_TOOLS_FILE, KEI_PROXY_EGRESS_PROXY or WEBUI_SECRET_KEY; provide a v3 tool manifest at deployment and use the boot tool sync; link Open WebUI users (claim link, or Entra users via kei directory-sync); or debug "tool is not registered in the policy bundle", a container that refuses to start because a tool manifest or implementation is invalid, `identity.unlinked`, audit rows shown "via installation", no models listed. Other kei commands are kei-cli; the Entra side is kei-directory-sync.
---

# Open WebUI with Kei (openwebui-kei)

`openwebui-kei` is one container: Open WebUI, the **kei-proxy daemon** (not a
sidecar), and the Kei connector. The connector adds:

- the **Kei Pipe**, Open WebUI's only model provider;
- **`kei_guard`**, a global filter that refuses a turn when kei-proxy isn't
  ready or there is no Open WebUI user;
- the **Governor**, which every protected tool call goes through.

Model inference does not go through kei-proxy. The Open WebUI harness calls
its configured model endpoint itself; kei-proxy decides protected tool calls
and can release credentials to tools. Kei checks those calls against policy
and audits them. Anything Kei can't decide is refused: it **fails closed**.

The user is **Open WebUI's own user id**, whatever SSO is configured. Kei
links it to an email-keyed Kei user. Until then the user is **unlinked** and
refused.

**Tool definition invariant:** when `KEI_OPENWEBUI_TOOLS_FILE` is set, that file
is the only definition source. The plugin loads the manifest and registers
the tools once at boot; there is no hot reload. Restart the container to apply
file changes.

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Setup guide | the `kei-openwebui` repository, `docs/setup.md` | The full walk-through this skill follows |
| Tool definitions | `kei-openwebui` `docs/setup.md` section 3 and `docs/design.md` section “Tool specs from a file” | File-based v3 manifest, generated-catalog fallback, implementation entry points, and boot sync |
| Design | `kei-openwebui` `docs/design.md` | The gate, agent sessions, supervisor order, known gaps |
| Installed CLI | `kei help` | Exact `kei` flags for this release |
| In this skill | [references/image-and-env.md](references/image-and-env.md), [references/tool-definitions.md](references/tool-definitions.md) | Environment table, mirroring, manifest loading and boot sync |

The code wins over this file. Never invent a flag or an environment variable. The [tool definition reference](references/tool-definitions.md) covers manifest loading and implementation details.

## What every answer must say

- Name the real commands: `kei bot init --platform openwebui`,
  `kei bot credential ... | <secret manager>`, `kei policy create`,
  `kei directory-sync`.
- The model configured in Open WebUI or its harness works without a Kei model
  profile. Model profiles are optional and can pass model credentials; model
  inference does not go through kei-proxy. Write a `tool:<name>` permit for
  each protected tool, using its declared name exactly. Show the command.
- A policy must target the manifest tool name exactly as `tool:<name>`. When a
  tool implementation uses an optional `method`, it names the public `Tools`
  method for that definition.
- Deploy the image **by digest** (`@sha256:<digest>`), never by tag.
- The image runs as **UID/GID 10001**.
- Never print, echo or paste `KEI_RUNTIME_TOKEN`.
- When explaining tool registration, explicitly say that a set
  `KEI_OPENWEBUI_TOOLS_FILE` is the only definition source, is loaded and
  registered once at boot, and has no hot reload; restart to apply changes.
  When the variable is unset, the generated catalog remains the source. If a
  manifest `method` is used, it must name a public method on the installed
  `Tools` class; an unknown method fails boot.

## 1. Kei side (org owner or admin, after `kei login`)

1. **Agent.** Create the chat agent in the Kei console (the CLI has no agent
   create) and note its id.
2. **Installation**, platform `openwebui`:

   ```sh
   kei bot init --platform openwebui --name acme-chat --agent <agent-id> --workspace <ws>
   kei bot list                     # the installation id
   ```

3. **Credential.** Kei shows it once, and `kei bot credential` refuses to write
   to a terminal. Pipe it into the secret manager:

   ```sh
   kei bot credential --installation <installation-id> --workspace <ws> | <secret-manager import command>
   ```

   Rotation is the same command with `--rotate` (use `kei-credential-rotation`).
   The container also needs `KEI_RUNTIME_CONTROL_PLANE_URL`, the control
   plane's base URL with no `/api/v1`.
4. **Optional model profile.** A model already configured in Open WebUI or
   its harness works without a Kei model profile. Profiles are an opt-in
   convenience for passing model credentials:

   ```sh
   kei model-profiles create --workspace <ws> --display-name acme-chat-model \
     --endpoint https://models.acme.example/v1 --auth-type none \
     --default-model <model> --agent <agent-id>
   kei model-profiles assignment --workspace <ws> --agent <agent-id>
   ```

   `--auth-type api_key` reads the key from stdin and needs a runtime with a
   credential-sync key (`kei-runtime-setup`).
5. **Policies** for protected tools:

   ```sh
   kei policy create --workspace <ws> --group chat-users \
     --allow tool:acme.orders.list_orders
   ```

   - `--group` is the group the rule applies to: a group name such as
     `chat-users`, or `autogroup:member` / `autogroup:admin`. Policies apply
     to groups; there is no `user:` or `*` source on the CLI.
     Bare/wildcard/`model:`/`connector:` target patterns are silently
     skipped (HAI-673); write the exact `tool:<name>`.
   - A write tool runs as soon as a permit allows it.
   - A permit only applies to a **registered** tool (section 3).
   - A harness-executor tool (an Open WebUI tool implementation) needs an exact
     `tool:<name>` permit, a **registered** tool, and a **linked user**
     (section 4). It does not need an agent-connector binding: agent-connector
     bindings apply only to connector/MCP tools.
   - Read/write isn't in the request, so name the read and write tools
     separately.
6. **Users.** See section 4.

## 2. The image

- **Pull by digest**, no credentials needed:
  `docker pull public.ecr.aws/o1a1k4g0/openwebui-kei@sha256:<digest>`. The
  digest is the `image=` line of `IMAGE_DIGEST.txt` on the kei-openwebui
  GitHub release. Pin it; tags are for people.
- **Mirror by digest** into your registry so the digest doesn't change. For
  Azure: `az acr import --name <acr> --source public.ecr.aws/o1a1k4g0/openwebui-kei@sha256:<digest> --image openwebui-kei:<tag>`,
  then deploy `<acr>.azurecr.io/openwebui-kei@sha256:<digest>`.
- **UID/GID 10001.** Set the container user, `runAsUser`/`runAsGroup`/
  `fsGroup`, and volume owners to 10001. With 1000 the supervisor refuses to
  start: `KEI_RUNTIME_STATE_DIR (...) is not a writable directory`.
- **Environment:**
  - required: `KEI_RUNTIME_TOKEN`, `KEI_RUNTIME_CONTROL_PLANE_URL`,
    `WEBUI_SECRET_KEY`;
  - with a manifest file: `KEI_OPENWEBUI_TOOLS_FILE`;
  - optional: `KEI_PROXY_EGRESS_PROXY` / `KEI_PROXY_NO_PROXY` (kei-proxy and
    the tool sync only, never Open WebUI), and `KEI_PROXY_AUDIT` on a volume.

  Full table: [references/image-and-env.md](references/image-and-env.md).
- **Versions.** The boot tool sync needs image v0.1.1 or later. File-based definitions use the Agentware `kei.tool-manifest/v3` format.

## 3. Tool definitions and the boot tool sync

The plugin can load definitions from a deployment-provided manifest file. Set `KEI_OPENWEBUI_TOOLS_FILE` to the file path inside the container. The deployer’s CI/CD pipeline supplies the file (for example, mounts it read-only); keep it outside the image. The plugin reads it once at boot, so changes take effect after restart. Do not put a runtime token in the generated skill or manifest.

Use Agentware’s existing `kei.tool-manifest/v3` shape and `ToolSpec`, not a new Open WebUI-specific schema. The Acme sample at `examples/tools.example.yaml` demonstrates the format. A tool has a `name`, `service`, `source`, `operation_class`, `route.harness_executor` and other v3 ToolSpec fields. For example, `acme.orders.list_orders` can route to the Open WebUI harness executor. The name is the action: policies target the exact `tool:<name>`.

```yaml
schema: kei.tool-manifest/v3
tools:
  - name: acme.orders.list_orders
    service: acme_orders
    source: orders_api
    operation_class: read
    route:
      harness_executor:
        executor: openwebui
        registration: acme.orders.list_orders
    description: List recent Acme orders.
    enabled: true
```

The deployment’s CI/CD provides this file. When `KEI_OPENWEBUI_TOOLS_FILE` is set, it is the only definition source: the generated catalog and `tool_definitions` entry points are ignored. The plugin loads and registers tools once at boot; there is no hot reload, so restart to apply changes. When unset, the image uses the generated catalog from contract schemas as before.

Tool implementations are code, supplied by installed Python packages. Each package exposes its `Tools` class through the `kei_openwebui.tool_implementations` entry-point group, named exactly for the manifest’s `service` (for example, `acme_orders = "acme_orders.tools:Tools"`). Install the package in the image. Boot resolves the service to its installed implementation and seeds the Open WebUI tools. The manifest defines registration; the installed entry point supplies executable code.

**Boot tool sync.** At boot, the plugin unmarshals the file with Agentware `ToolSpec` and calls `haikeilabs.agentware.kei.tool_sync.sync_tool_manifest`, which registers the manifest with Kei using `PUT /api/v1/runtime/tools` and the runtime token. It is a one-time boot action; updating the file requires a restart. The image’s generated catalog follows the same sync route when the variable is unset.

The file loader fails closed on a missing or unreadable file, invalid YAML or manifest, an empty or duplicate tool list, an unavailable service implementation, or an unknown `method`. It reads exactly one safe YAML document, rejects anchors, aliases, merge keys, custom tags and duplicate mapping keys, and refuses files over 256 KiB. Missing or invalid implementation packages and sync failures also stop startup before Open WebUI serves. The file supports Agentware `kei.tool-manifest/v3`; see the [shared format documentation](https://github.com/HaikeiLabs/agentware/blob/main/docs/tool-manifest-v3.md).

When no file is configured, tools are generated from contracts schemas at image build. Definition updates in that mode require rebuilding and redeploying the image.


## 4. Linking users

- **Claim link (any SSO).** An unlinked user's protected tool call is refused
  `identity.unlinked`, and the tool body never runs. The connector shows that
  user, and only that user, a one-time claim link as an **Open WebUI
  notification**. It is never in the chat, the model's context or a log. They
  open it, sign in to Kei, and ask again.
- **Entra.** `kei directory-sync` creates the Kei users and groups from the
  Entra app's role assignments (load `kei-directory-sync`). Permits then use
  `group:<role value>`. Each user still links their Open WebUI identity once,
  with the claim link.
- **Check a user:** `kei users resolve --email <email>`,
  `kei users remote-identities list <user>`.

## 5. Verify

In a shell in the container (never print the token):

1. **Boot log:** `kei-seed: tool sync: registered N tool(s) with Kei at /api/v1/runtime/tools (...)`.
2. **Export:** `python -m kei_openwebui.boot --export-manifest` lists the tool
   names.
3. **Bundle:** `"$KEI_PROXY_PATH" policy show`. `tool_count` includes them;
   `policy_revision` and `last_success` are current.
4. **Models:** `GET /v1/models` on `$KEI_RUNTIME_SOCKET_PATH`, with the runtime
   token passed on stdin.
5. **One allowed call** as a linked user with a permit: the answer has data.
6. **One denied call** to a tool with no permit: `Refused (kei.denied): ...`,
   and the tool body never runs.
7. **Audit:** the Kei console's audit view shows both decisions under the
   user's Kei user. Before shipping, they are in the `$KEI_PROXY_AUDIT` spool.

From outside, `kei harness sync --harness openwebui --url <open-webui-url>` (admin
token in `OPENWEBUI_ADMIN_TOKEN`) checks that the Kei Pipe and `kei_guard` are
installed. It is read-only and exits 1 on drift.

## 6. Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| Tool call refused **`tool is not registered in the policy bundle`** (`tool_not_registered`) | Kei hasn't registered the tool: image older than v0.1.1, no generated definition or file-based manifest entry, the implementation is missing, the name differs from what the method sends, or the bundle hasn't refreshed | Boot log `tool sync: registered N tool(s)`; compare `--export-manifest` names with the refused name; wait a poll, check `policy show` `tool_count`. A permit can't help until the tool is registered |
| Container refuses startup while loading tool definitions | The configured manifest is missing or invalid, has no tools or duplicate names, references an unavailable implementation, or contains an unknown method | Correct the v3 manifest and install the matching `tool_implementations` entry point; restart |
| Container won't start: `tool sync with Kei failed: ... HTTP 401` | Wrong or rotated runtime token | Put the current credential in the secret manager, restart |
| Same, `HTTP 404` | `KEI_RUNTIME_CONTROL_PLANE_URL` has a path (e.g. `/api/v1`) or is the wrong host | Use the base URL |
| Same, `HTTP 409` | The tool name is registered by an admin or another installation | Rename, or remove the other registration |
| Same, network error | Egress | `KEI_PROXY_EGRESS_PROXY` / `KEI_PROXY_NO_PROXY` |
| `KEI_RUNTIME_STATE_DIR (...) is not a writable directory` | Not running as 10001 | Run as UID/GID 10001 |
| User refused **`identity.unlinked`** | Open WebUI user not linked to a Kei user | Open the claim link from the notification; no link → admin checks `kei users remote-identities list` |
| Audit rows show the installation's owner **"via installation"**, denied | No session user: the Open WebUI user is unlinked, so the console attributes the row to the installation subject | Link the user; later rows show their own Kei user |
| **No models** in Open WebUI | Model provider or model configuration in Open WebUI is missing or unavailable | Check Open WebUI's configured model provider, endpoint, credentials, and model name. Kei model profiles are optional credential convenience; inference does not go through kei-proxy. |
| Denied although a permit exists | User is unlinked, the tool is not registered, the policy does not match, or the bundle is stale | Link the Open WebUI user; confirm exact tool registration and permit target/source, then check `policy_revision`. Harness-executor tools do not require an agent-connector binding. |
| Turn fails `Kei governance is unavailable, so this request was not sent` | `kei_guard`: kei-proxy not ready | Check kei-proxy in the container log |

## Validation commands

```sh
kei help | grep -E 'bot init|model-profiles|policies|directory-sync'
kei bot status --installation <installation-id>
kei policy list --workspace <ws>
# in the container:
python -m kei_openwebui.boot --export-manifest
"$KEI_PROXY_PATH" policy show
```

## Realistic usage boundaries

- This is the published image's path. kei-proxy runs **in** the container;
  there is no sidecar mode. Nothing installs at runtime.
- `origin` and `automation_id` stay connector metadata and don't reach Kei's
  policy or audit yet (gap K9). Automations run as their owner and are decided
  like any other call.
- Knowledge embeddings don't go through Kei (no `/v1/embeddings`, gap K1).
- Read/write isn't in the authorize request; write separate permits for read
  and write tools.
- Agent creation is not exposed by the CLI; existing agents can move between
  workspaces with `kei agents move` (preview first). Check installed help for
  current `kei directory-sync` syntax.
- Agents: never print or ask for `KEI_RUNTIME_TOKEN`, never send an empty tool
  manifest (it unregisters every tool), and never run `kei` writes without the
  admin's go-ahead.
