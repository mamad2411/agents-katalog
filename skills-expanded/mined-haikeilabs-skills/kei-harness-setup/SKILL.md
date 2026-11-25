---
name: kei-harness-setup
description: "Choose and set up Kei harnesses: SDK (Agentware), Claude Code, Codex, Pi, OpenCode, Cursor, or Open WebUI. Install skills or adapters, pair with a runtime and kei-proxy, pass identity on governed calls, verify setup, and prove calls without matching permits are denied. See `kei-pi-setup` or `kei-openwebui`."
---

# Set up a harness with Kei

For Claude Code, Codex, OpenCode, or Pi, the advertised one-command path is
`kei connect HARNESS [--workspace NAME] [--yes]` (`HARNESS` is `claude-code`,
`codex`, `opencode`, `pi`, or `cursor`). Use the manual steps
below when you need to inspect or customize setup.

Kei puts guardrails on a harness through this chain:

`harness adapter → kei-proxy → kei-policy-catalog`

For long-lived SDK (Agentware) harnesses, the harness connects to
`kei-proxy serve` over its local socket and asks it to decide each protected
tool call. `kei-proxy` decides locally against the workspace policy bundle and runs allowed work
inside the tenant runtime. The catalog holds policy, connector metadata, and
redacted audit metadata only. Setting up a harness means installing the skills
that teach the agent this contract, then wiring the harness to a runtime.

## Answer checklist

Answer from this skill: setup steps, identity variables, and troubleshooting
are on this page, so you do not need to search a codebase first. If something
is not here, say so. Give the steps rather than asking questions first.
You do not need to open the files in `scripts/` to answer: what each one
does is summarised under "Per-harness setup scripts" below, so name the
script and its steps instead of reading it.
When a detail lives in another skill, end the answer with a **See also:**
line naming that skill (DeepSeek-style short answers still need it):

Installing the skills does not grant permission; Kei policy decides whether
protected tool calls are allowed.

- **Installing into an existing config:** install from
  `https://github.com/HaikeiLabs/skills`; skip, or ask about, same-named
  existing skills instead of overwriting them; show how to verify the harness
  discovered the skills; then do the runtime half (`kei login`, then runtime
  setup).
- **Making tool calls go through Kei:** installing skills does not by itself
  allow tool calls; policy decides. Include a deny check: a call without a
  matching permit must fail.

- **Model or tool formats:** `kei-openai-backends`. Never answer with the
  skill name alone, even in a one-line answer; always add the one-line
  summary: Anthropic uses `input_schema` with `thinking` content blocks;
  OpenAI and DeepSeek use OpenAI-compatible JSON function-calling with
  `reasoning_content` (DeepSeek may also emit `[THINK]` tags). Example: "Use
  `kei-openai-backends`. Anthropic's format differs: tools are declared with
  `input_schema`, and reasoning arrives as `thinking` content blocks."
- **Setup script walkthrough:** name `scripts/setup-<harness>.sh` (for
  example `setup-claude-code.sh`); on a fresh machine (no
  `~/.config/kei.yaml`) it creates the runtime installation; the credential is
  piped from `kei bot credential` into `kei setup` and never printed; and it
  ends by running `verify.sh` (name the file) to confirm the setup is valid.
- **Identity on protected calls:** set `KEI_PROXY_FRAMEWORK` (the harness kind)
  and `KEI_PROXY_INVOKING_SUBJECT` (the human); agent identity is
  auto-discovered. See also: `kei-runtime-setup` (runtime half) and
  `kei-openai-backends` (model half).
- **Stale bundle / "No registered harnesses selected":** stale policy bundle
  (HAI-403); a policy edit forces a refresh, else the 6-hour background
  refresh. Always add: desktop harnesses (claude_code, codex, opencode, cursor)
  are auto-discovered by sync, so no `kei harness add` is
  needed.
  End with: See also: `kei-harness-policy` `references/bundle-versioning.md`.
- **Rejected bundle or disabled proxy:** `kei-proxy` fails closed and denies
  every protected call until it is fixed.
- **Last setup step:** one protected tool call in the harness (for example, the agent
  running `git status`), confirmed in the console: **Audit Logs** shows it
  with the harness kind, **the installation's card shows the recent
  activity** (say this one too), and `kei runtime service status` shows the runtime service running (the
  audit upload needs it).

## Concepts

- **Harness** — software that lets an LLM act as an agent (for example Claude
  Code, OpenCode, or an SDK (Agentware) application).
- **Kei-enabled harness** — a harness with Kei policies through a **runtime
  installation**.
- **Runtime installation** — Kei's record for the one runtime deployed beside
  that harness (one harness : one runtime installation : one credential,
  `KEI_RUNTIME_TOKEN`). The console page is called **Runtime installations**.
- **Agent** — an LLM configuration the harness runs (model, system prompt,
  tools).

This is a workflow skill. Keep the two Kei executables straight: **`kei`** is
the platform admin CLI a person runs once to set things up (`kei-cli` skill);
**`kei-proxy`** is the runtime the harness calls on every protected tool call
(`kei-proxy` skill). Load **`kei-runtime-setup`** for the runtime half of the
setup. Pi has a separate extension and tokenless local-socket path; use
**`kei-pi-setup`** for Pi instead of applying this skill's desktop sync or
harness-token instructions to it.

### Per-harness setup scripts

This skill includes portable setup scripts in `scripts/` for Claude Code,
Codex, and OpenCode. Pi uses a separate package-based adapter; follow
`kei-pi-setup` instead of these scripts. Each script is self-contained POSIX
`sh` (with a shared `setup-lib.sh`) that checks prerequisites (including detecting an existing
`~/.config/kei.yaml` to decide whether a fresh runtime installation is
needed), creates a runtime installation if the machine does not have one,
syncs the harness (desktop kinds are auto-detected — no separate
registration needed), and runs `verify.sh` to confirm the setup is valid.
The shared `setup-lib.sh` calls `kei harness add` with `|| true` for
backward compatibility (the `add` may be rejected for desktop kinds that
sync auto-discovers; the `|| true` ensures the script does not halt), but
the primary registration path for desktop harnesses is `kei harness sync`.

**Installing from GitHub (clone + link):**

```sh
# 1. Clone the Haikei Skills repo (once; git pull to update)
git clone https://github.com/HaikeiLabs/skills.git ~/src/haikei-skills

# 2. Link each skill into the harness's skills directory
#    (skip already-existing skills — never overwrite without asking)
SKILLS_DIR=~/.config/opencode/skills   # or the correct dir for your harness
mkdir -p "$SKILLS_DIR"
for d in ~/src/haikei-skills/skills/*/; do
  name=$(basename "$d")
  dest="$SKILLS_DIR/$name"
  if [ -e "$dest" ]; then echo "exists, skipping: $name"; continue; fi
  ln -s "$d" "$dest"
done

# 3. Verify the harness discovers the skills
opencode debug skill | jq -r '.[].name' | grep '^kei'
```

**Using the setup scripts (preferred for first-time setup):**

```sh
# The per-harness scripts handle everything: prerequisites check,
# installation creation, credential piping (never printed to terminal),
# harness sync (desktop kinds auto-detected), and verification.
bash skills/kei-harness-setup/scripts/setup-opencode.sh
```

| Script | Harness |
| --- | --- |
| `scripts/setup-claude-code.sh` | Claude Code |
| `scripts/setup-codex.sh` | Codex |
| `scripts/setup-opencode.sh` | OpenCode |
| `scripts/setup-cursor.sh` | Cursor (kei-cli v0.3.0+) |
| `scripts/verify.sh <kind>` | All (run after any setup or as a standalone check) |

The scripts are safe to re-run (idempotent) and never print a runtime
credential to the terminal — tokens are piped directly from `kei bot
credential` into `kei setup`.

## Retrieval sources

| Source | How to retrieve | Use for |
| --- | --- | --- |
| Docs: Agent setup | `https://docs.haikeilabs.com/kei/connect-your-harness/harness-setup` | Supported harnesses, the harness → runtime → catalog flow, DENY rules |
| Docs: Get started | `https://docs.haikeilabs.com/kei/get-started/install-skills` | Per-harness skill install commands |
| Console: Agents page | **Agents →** a harness card → **Copy setup prompt** | The canonical per-harness setup prompt |
| Skills repo | `https://github.com/HaikeiLabs/skills#installing` | Current skill-directory table |
| The harness's own docs | Its skills documentation | Where that harness version discovers skills |

Append `.md` to any docs page URL for the raw page.

## Choose a harness type

The API/catalog kind `custom` maps only to SDK (Agentware), not Pi or Open WebUI.

- **SDK (Agentware):** choose this for an application built with the Agentware SDK, including pydantic-ai, Gemini SDK, AWS AgentCore, or a bespoke loop. From Agentware 0.12.0, the SDK uses `KeiProxyEvaluator` with the socket client from `kei-proxy serve`; the `kei-proxy authorize` CLI is a version and policy dependent fallback for one-shot environments without a daemon.
- **Claude Code:** choose this for interactive coding sessions in Claude Code; desktop sync discovers it automatically.
- **Codex:** choose this for interactive coding sessions in Codex; desktop sync discovers it automatically.
- **Pi:** choose this for the Pi coding agent; its `kei-lime-pi` adapter uses the local proxy socket. See `kei-pi-setup`.
- **OpenCode:** choose this for interactive coding sessions in OpenCode; desktop sync discovers it automatically.
- **Cursor:** choose this for interactive coding sessions in the Cursor CLI;
  desktop sync discovers it automatically. Native-first: Kei renders the policy
  bundle into Cursor's CLI config permissions (`~/.cursor/cli-config.json` —
  `Shell(base)`, `Read(glob)`, `Write(glob)`, `WebFetch(domain)`,
  `Mcp(server:tool)`; deny beats allow), with hooks only where the native config
  cannot express a policy. `kei connect cursor` and
  `kei harness sync --harness cursor` fail closed — they exit non-zero and write
  nothing — when the policy set contains a kind Cursor cannot gate, such as
  `skill:`. Needs a kei-proxy runtime like the other desktop harnesses.
  Released in kei-cli v0.3.0 (check `kei help` for the installed version).
  Whether the Cursor
  editor honors `cli-config.json` is undocumented — do not promise editor
  enforcement. There is no VS Code extension.
- **Open WebUI:** choose this for a chat UI deployment with Kei policies using the `openwebui-kei` image, Python library, and tool packs. See `kei-openwebui`.

The API/catalog kind value `custom` names only the **SDK (Agentware)** type; it
does not describe Pi or Open WebUI. Register an SDK harness with
`kei harness add --kind custom`. Its manifest sync command is
`kei harness sync --harness custom --manifest tools.json` (requires kei >=
0.1.33). The current kei-cli is 0.3.x and kei-proxy is v0.6.x.

For custom Agentware harnesses, install the published SDK package for your
language: `pip install haikeilabs-agentware`, `npm i @haikeilabs/agentware`,
or `go get github.com/haikeilabs/agentware/go`. Run `kei-proxy serve` beside
the harness and set `KEI_RUNTIME_SOCKET_PATH`; sync the tool manifest before
serving requests. From Agentware 0.12.0 the SDK also registers typed `ToolSpec` declarations
over the socket with `POST /v1/tools:register` (Python
`register_tool_specs`, TypeScript `registerToolSpecs`, Go
`toolsync.SocketRegistrar`). This is an alternative to the operator-managed
`kei harness sync --harness custom --manifest tools.json` flow.

Any other harness is unsupported and is denied until an adapter is explicitly
registered. Do not improvise one.

## Entry point: console setup prompt

The fastest path to an agent with Kei policies starts in the console. Open the
**Agents** page, find your harness card, and click **Copy setup prompt**.
The prompt tells the agent everything it needs:

> Use the kei-harness-setup skill to connect this &lt;agent&gt; to Kei:
> org … workspace … installation name …

Paste the prompt into the harness. The agent loads this skill, reads its
identity variables, and runs the setup steps below. If you do not have
console access or are writing instructions for a different person, follow
the numbered steps starting at section 1.

The prompt output is the single source of truth for the org, workspace, and
installation name this harness should target. Never guess or hard-code them.

## FIRST: find out which harness you are running in

Check the environment rather than assuming — the skills directory differs per
harness, and installing into the wrong one silently does nothing. Then check
whether the skills are already there (for example a `kei-cli` folder in the
harness's skills directory, or the harness's skill list) before installing
again.

> **Installing skills changes what the agent knows, not what it may do.**
> Policy in the workspace decides that. Until a deny check passes (step 6),
> the agent can see the Haikei Skills but cannot make protected tool calls.

## 1. Install the Haikei Skills

The repo is `https://github.com/HaikeiLabs/skills`. Skills are portable
`SKILL.md` folders, so every harness gets the same content.

**Plugin install (preferred where available):**

```text
# Claude Code
/plugin marketplace add HaikeiLabs/skills
/plugin install haikei@haikei

# Codex
codex plugin marketplace add HaikeiLabs/skills
codex plugin add haikei@haikei
```

Cursor: **Settings → Rules → Add Rule → Remote Rule (GitHub)** with
`HaikeiLabs/skills`.

**Clone and link (OpenCode, Pi, or any harness without a plugin flow):**

```sh
git clone https://github.com/HaikeiLabs/skills.git ~/src/haikei-skills
for d in ~/src/haikei-skills/skills/*/; do
  name=$(basename "$d")
  dest="$SKILLS_DIR/$name"                 # pick SKILLS_DIR from the table below
  if [ -e "$dest" ]; then echo "exists, skipping: $name"; continue; fi
  ln -s "$d" "$dest"
done
```

Symlinks keep the skills current with `git pull`; copy instead if the harness
does not follow symlinks. Either way: keep existing skills, never overwrite a
same-named skill without asking, and never copy `.git`.

| Harness | User directory | Project directory |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.agents/skills/` (older: `~/.codex/skills/`) | `.agents/skills/` |
| OpenCode | `~/.config/opencode/skills/` (or `$OPENCODE_CONFIG_DIR/skills/`) | `.opencode/skills/` |
| Pi | `~/.pi/agent/skills/` or `~/.agents/skills/` | `.pi/skills/` or `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | — |

OpenCode also reads `~/.claude/skills/` and `~/.agents/skills/`, and Pi reads
`~/.agents/skills/`. So one copy in `~/.agents/skills/` serves Codex, OpenCode,
and Pi. Avoid installing the same skill name in two directories that one
harness reads, or it may load a stale copy.

**Verify discovery.** Each `SKILL.md` must start with `---` frontmatter holding
`name` and `description`; a file that begins with anything else (even a
comment) is skipped. Then confirm the harness actually sees the skills.
OpenCode can list them:

```sh
opencode debug skill | jq -r '.[].name' | grep '^kei'
```

For the other harnesses, restart the session and check the skill list. A new
skill is not picked up by a session that is already running.

## 2. Pair the harness with a runtime

Protected calls need a runtime installation and `kei-proxy` on the same host or
container as the harness. Follow **`kei-runtime-setup`** — it starts with
`kei login`, which a person must approve in the browser. For a local coding
harness, create the installation with `--platform cli`.

For a Kei-enabled coding harness on a workstation, the current path is:

```sh
kei login                                       # admin, once; a person approves in the browser
kei bot init --platform cli --name "my laptop"
kei workspaces list                               # discover workspace name or ID
kei bot credential --installation ID --workspace WS | <secret-manager import>
<secret-manager read> | kei setup --control-plane-url https://app.haikeilabs.com   # token via pipe → ~/.config/kei.yaml
kei runtime bootstrap     # runs the bundled kei-proxy to verify + heartbeat
kei bot bind --installation ID
```

For a one-shot SDK harness with no daemon, the fallback `kei-proxy authorize`
process needs
`KEI_RUNTIME_TOKEN` and `KEI_RUNTIME_CONTROL_PLANE_URL` in its environment;
load these from the secret manager and never put the token in a repository
config. **Pi is the exception:** its `kei-lime-pi` extension uses the local
owner-only Unix socket, and the daemon retains the runtime token. Do not pass
the token to Pi; follow `kei-pi-setup`.

## 3. Sync the harness (auto-discovery) or register an SDK (Agentware) harness

> **Prerequisite:** use kei-cli 0.2.0 or later for current harness commands.
> Manifest-based SDK (Agentware) sync requires kei >= 0.1.33. Load
> **`kei-harness-policy`** for the full command reference.

### When to use `kei harness add`

`kei harness add` is **only for SDK (Agentware) harnesses** (`--kind custom`).
Desktop coding harnesses (Claude Code, Codex, OpenCode) are **sessions**
of one runtime installation per machine. They are auto-discovered by
`kei harness sync` — you do NOT need to run `kei harness add` for them. Pi uses
a separate adapter; see `kei-pi-setup`.

| Use case | Action |
|---|---|
| Desktop harness on a workstation | `kei harness sync` — no `add` needed |
| SDK (Agentware) harness you built | `kei harness add --kind custom [--installation ID] [--agent ID]` |

Flags: `--installation` defaults to the single installation on this machine;
`--agent` defaults to the default agent. Errors: `ALREADY_EXISTS` means the
agent already has a harness on that installation; `no default agent found`
means set a default agent with `kei bot agents add --default` or pass
`--agent`.

### Desktop harnesses: auto-discovered by sync

A harness is keyed by the **agent** (3NF): its identity is
`(installation_id, agent_id)`, and the console labels these harnesses "agents".
The agent must already be attached to the installation (`kei bot agents add`).

For desktop harnesses (`claude_code`, `codex`, `opencode`, `cursor`), you
skip `add` entirely — `sync` auto-discovers them:

```sh
kei harness sync --harness claude_code
```

The `custom` API kind is the SDK (Agentware) type. `--kind` accepts
`claude_code`, `codex`, `opencode`, `cursor`, or `custom`; Pi and Open WebUI
have their own adapters and are not `custom`.
Sync fetches the policy bundle and renders the native config for that kind:

```sh
kei harness sync --harness claude_code
```

After sync, Kei can render the policy bundle into the harness's native config
format (e.g. `~/.claude/settings.json` → `permissions.allow`). The first render
happens on sync; subsequent policy changes re-render through the background
bundle refresh in `kei-proxy serve`.

`kei harness sync` edits only the Kei-managed entries in the harness's native
config file and leaves your own entries alone; it saves
`<config-file>.kei-backup-<timestamp>` before every write and keeps only that
one backup, from before the latest successful sync (kei 0.1.31 or later). Roll
back by copying it over the native config. The setup scripts
also keep a one-time `<config-file>.kei.bak` copy from before the first sync.
See `kei-harness-policy` for removing your own entries so Kei is the only
source of permissions.

### Cursor

Cursor is the seventh harness kind (`cursor`, tool prefix `cursor.`). Kei policies apply native-first: Kei renders the policy bundle into Cursor's CLI config
permissions (`~/.cursor/cli-config.json` → `permissions.allow` /
`permissions.deny`, with tokens `Shell(base)`, `Read(glob)`, `Write(glob)`,
`WebFetch(domain)`, and `Mcp(server:tool)`; deny beats allow). Hooks are used
only where the native config cannot express a policy.

`kei connect cursor` and `kei harness sync --harness cursor` **fail closed**:
if the policy set contains a kind Cursor cannot gate — for example `skill:` —
they exit non-zero and write nothing. Fix it by scoping the `skill:` policy to
harnesses that can gate it (for example a `harness:claude_code` src pattern)
or removing it. Cursor needs a kei-proxy runtime like the other desktop
harnesses and is auto-discovered by sync. There is no VS Code extension, and
whether the Cursor editor honors `cli-config.json` is undocumented — do not
promise editor enforcement.

These commands shipped in kei-cli v0.3.0 (v0.3.7 is current). Check `kei help`
for what your installed version accepts.

## 4. Pass identity on every protected call

A tool call is **protected** when it touches tenant data, external systems, or
credentials: it goes through the Agentware socket client to `kei-proxy serve`
(or the `kei-proxy authorize` CLI fallback for a one-shot environment), Kei
policy decides, the decision is audited, and enrollment or approval can apply. A call that is
**local** runs locally and never reaches Kei. When unsure, treat the
tool as protected. The full distinction is in the `kei-proxy` skill.

Agentware applications use `KeiProxyEvaluator` with the selected socket client
so each protected tool call is decided by the daemon. A configured socket that
cannot be reached is a refusal; do not fall back to a subprocess. The CLI
fallback returns exit code `0` for allow; any non-zero exit (deny or error)
means do not run the tool. The full flag and env reference is in the
`kei-proxy` skill. Identity and delegation come from flags or environment:

```text
KEI_PROXY_FRAMEWORK=claude|codex|opencode|pi   # which harness
# Agent identity is auto-discovered from the runtime identity event
# (kei-proxy >= 0.1.11, agentware >= 0.4.0). No agent-ID env var needed.
KEI_PROXY_INVOKING_SUBJECT=<the human who started the task>
KEI_PROXY_PARENT_SPAN / KEI_PROXY_DELEGATION_DEPTH   # when a subagent delegates
```

Keep the human who started the task as the invoking subject through every
subagent hop; it is what the audit trail attributes the call to. Never put a
tenant, org, or workspace ID in agent-controlled tool parameters — scope comes
from the runtime token. The `kei-proxy authorize` endpoint does not require a
`platform_tenant_id` (there is no tenant concept for now); a request without a
chat subject simply reaches the policy decision.

To read the assigned agent ID at runtime, use the agentware SDK's
`link.identity()` (see `agentware-sdk` skill). If identity is not available,
deny protected calls — never guess a fallback agent ID.

### 4a. Use KeiProxyEvaluator with the socket client

Long-running Agentware harnesses use the socket client with
`KEI_RUNTIME_SOCKET_PATH`.

If your harness imports Agentware 0.12.0 or later (any of the three ports), run
`kei-proxy serve` beside it, sync a non-empty tool manifest before serving,
and construct `KeiProxyEvaluator` with the SDK selector and
`KEI_RUNTIME_SOCKET_PATH`. The selector chooses the socket client when the
socket is configured. An unavailable configured daemon is a refusal and must
not trigger a CLI fallback. The `kei-proxy authorize` CLI remains available
for one-shot environments with no daemon. It is not a v2 allow probe and
returns `preflight_required`; use the socket route for a v2 policy decision.
See `agentware-sdk` for the exact Python, TypeScript, and Go APIs, session
handling, ToolSpec registration, and the shared decision fixtures.

Do **not** keep a local allow list in the harness. The workspace policy bundle
(`kei-proxy` + `kei-policy-catalog`) is the single source of truth for what
is allowed. A local allow list is stale on deploy and invisible to audit.

> **Future (HAI-124):** Catalog-distributed policy bundles will let the
> control plane push policy updates to runtimes without a deploy. Until then,
> the runtime boots with the bundle it fetched at bootstrap. `KeiProxyEvaluator`
> works the same way either way — it asks `kei-proxy` every time.

## 5. Register tools and wire connectors (CLI first)

Registering and wiring never grant permission. A connector binding is
**wiring only, never a permission gate** (ADR-038 §4): it records that the
agent uses that connector, and is never consulted to decide allow or deny.
What the agent may do is decided by workspace policy — group membership plus
matching targets — and deny wins. The CLI's own usage line says the same:
"bindings are wiring only, never a permission gate".

**Register the harness and its tools.** Desktop kinds (`claude_code`,
`codex`, `opencode`) are auto-discovered by sync; an SDK (Agentware) harness
registers explicitly and syncs a tool manifest (section 3 above has the
detail):

```sh
kei harness sync --harness claude_code                    # desktop kinds: auto-discovered
kei harness add --kind custom --installation ID --agent ID   # SDK (Agentware) only
kei harness sync --harness custom --manifest tools.json      # SDK tool manifest
kei harness list --installation ID --json                    # verify what is registered
```

**Wire connectors to the agent** with `kei connector-bindings` (AIP routes
`/api/v1/organizations/{org}/workspaces/{ws}/connector-bindings`):

```sh
kei connector-bindings list [--workspace WORKSPACE] [--agent AGENT_ID] [--page-size N] [--page-token TOKEN] [--json]
kei connector-bindings get BINDING_ID [--workspace WORKSPACE] [--json]
kei connector-bindings create --agent AGENT_ID --connector CONNECTOR_ID [--capabilities A,B] --workspace WORKSPACE [--json]
kei connector-bindings delete BINDING_ID --workspace WORKSPACE --yes
```

`--agent` is the agent's UUID (find it with `kei bot agents list
--installation ID` or in the console); `--connector` takes a connector ID or
name; `--capabilities` defaults to the connector's declared capabilities;
`delete` removes the binding immediately, so it needs `--yes`. `create` wires
and nothing more: if connector calls are still denied after creating a
binding, the workspace policy has no matching allow — fix the policy, not the
binding.

`kei connector-bindings` shipped in kei-cli v0.3.0 (v0.3.7 is current); check
`kei --version` and `kei help` for the installed
binary: an older CLI prints `unknown command "connector-bindings"`. There is
no `kei connectors bind` — the binding command group is
`kei connector-bindings` (the similar-sounding `kei service-principals bind`
binds a service principal to an installation, not a connector to an agent).
Until you run a release that has it, the console can do the same registration
and wiring, and manages group membership and policies under
**Agents → Groups**.

### Grant access (console)

A harness-executor tool (for example, an Open WebUI tool pack) needs an exact
`tool:<name>` permit, a registered tool, and a linked user. It does not need an
agent-connector binding. Agent-connector bindings apply only to connector/MCP
tools. A tool is not allowed just because the adapter exposes it; manage group
membership and policies in the console under **Agents → Groups**.

## 6. Prove it fails closed

Run one permitted, disposable call and one deliberately denied call through
the harness. For a preflight check, use the daemon Unix-socket
`POST /v1/authorize` route. Do not run one-shot `kei-proxy authorize` as an
allow probe; v2 returns `preflight_required`. A harness-executor tool is
denied when it has no matching exact tool permit, is not registered, or the
user is unlinked. A denied call must fail without a provider call and produce
only redacted audit metadata. Invalid installation scope, stale policy, and
no matching policy must all be **DENY**. The harness
is not set up until you have seen a denial — until then the agent can see the
Haikei Skills but has not proven that protected calls actually go through Kei.

If you configured harness command policies (step 3), also verify the native
config was rendered correctly:

```sh
# Claude Code — check permissions.allow contains expected entries
cat ~/.claude/settings.json | jq '.permissions.allow'

# OpenCode — check permission.bash
cat opencode.json | jq '.permission.bash'

# Cursor — check the rendered CLI config permissions (kei-cli v0.3.0+)
cat ~/.cursor/cli-config.json | jq '.permissions'
```

Run a command that should be permitted and one that should be denied:

```sh
# Should be allowed (if shell:git is in your policies)
git status

# Should be denied (if shell:* deny is in your policies)
curl example.com
```

`KEI_PROXY_DISABLED=true` is a valid setting, but it turns permits off: a
disabled, missing, or misconfigured kei-proxy denies **every** protected call
(fail-closed, HAI-249) — it never permits a tool call. Tests that need an allow
inject a fake evaluator instead (see the `agentware-sdk` skill); a production
harness should not run with kei-proxy disabled.

## 7. Make one protected tool call in the harness (first use)

For SDK (Agentware), a successful socket-client authorization and `verify.sh`
prove the socket plumbing is configured; the daemon socket route can preflight
a policy decision. These checks do not prove the harness itself makes a
protected tool call. Setup is not complete until a real protected tool call has
been verified in the harness.

In the harness, make **one** protected tool call — for example, have the agent
run `git status` (a shell command your policies permit). For desktop harnesses
the call is decided natively by the harness from the Kei-rendered policy; the
`kei-proxy` hook records the decision for audit.

Then confirm it in the console:

- **Audit Logs** shows the call, recorded with the harness kind
  (`claude_code`, `codex`, `opencode`, `cursor`, ...).
- The installation's card shows the recent activity.

The audit upload needs the runtime service running. Check it with:

```sh
kei runtime service status
```

If the service is not running, the call is still protected, but the audit record
is not uploaded — so it will not appear in Audit Logs.

## 8. Enrolling chat users (claim links)

When a chat-platform user (Teams, Slack, or Discord) is not yet linked to a
Kei user, the authorize endpoint returns `decision: "enrollment_required"`
with an `enrollment` block instead of `deny`:

```json
{
  "decision": "enrollment_required",
  "reason": "provider identity is not linked to a kei user",
  "identity_status": "unlinked",
  "org_id": "...",
  "workspace_id": "...",
  "provider_user_id": "...",
  "enrollment": {
    "provider": "teams|slack",
    "provider_user_id": "...",
    "org_id": "...",
    "workspace_id": "...",
    "url": "https://...",
    "expires_at": "2026-09-28T12:00:00Z"
  }
}
```

The harness must:

1. **Show the claim link privately.** The `url` is a one-time link that enrols
   the user as a workspace member with default group access; treat it as
   sensitive — show it only to the user who needs it, never log it or echo it
   to a shared channel.
2. **Honour the expiry.** `expires_at` is ~15 minutes from issuance; after that
   the url is unredeemable and the user must be re-prompted to authorize again.
3. **Re-authorize after enrollment.** Once the user visits the link and
   completes the self-enroll flow, their provider identity is linked and the
   next authorize call returns `allow` or policy-driven `deny` instead of
   `enrollment_required`.
4. **Do not auto-retry enrollment.** If the url is expired or the user declines,
   the next authorize call from the same provider identity re-issues a fresh
   enrollment. Do not loop; let the user drive re-authorization.
5. **Self-enroll grants member + default group.** Redeeming the claim link
   creates a Kei user (if new) and links the provider identity with member-level
   access and the workspace's default group. Approval-based elevation
   (managed access-request flow) is for non-default groups or elevated roles.

The `enrollment` object may be absent (no url/expires_at) when the control
plane cannot issue a claim — for example when the runtime installation has no
workspace scope or `KEI_WEB_BASE_URL` is unset. In that case fall back to
`guest_requires_signup`.

**Always show the newest link.** Every `enrollment_required` response mints a
new claim and invalidates the previous live claim for that identity. A resent
old link fails with `claim_used` (409). Do not mint extra links yourself —
each authorize call already does that. If the user has not acted on a link and
you re-prompt, show the link from the latest response, not a cached one.

The claim-link lifecycle is documented in detail at the canonical API contract:
`kei-policy-catalog docs/chat-identity-claims.md`.

## Report a bug from your harness

When something in Kei misbehaves during a harness session, the user can send a
bug report from the terminal with `kei feedback`, with the harness transcript
attached. It needs `kei` 0.1.20 or later (`kei --version`; upgrade with
`kei upgrade`) and a `kei login` session. The **Report a bug** button in the
console header sends to the same place.

Run it from the project directory the harness session ran in: without
`--session`, `--export` picks the most recent session for the current working
directory. `--description` is required (1 to 4000 characters).

```bash
# Claude Code (also Claude Code inside the Claude Desktop app)
kei feedback --description "What happened and what you expected" --export claude
kei feedback --description "..." --export claude --session <session-id>

# Codex
kei feedback --description "What happened and what you expected" --export codex
kei feedback --description "..." --export codex --session <session-id>

# OpenCode (needs the opencode binary on PATH; it runs opencode export)
kei feedback --description "What happened and what you expected" --export opencode
kei feedback --description "..." --export opencode --session <session-id>

# Any other harness: attach transcript files directly (repeatable)
kei feedback --description "..." --session /path/to/transcript.jsonl
```

With `--export`, `--session` takes one session ID. Without `--export`, each
`--session` is a transcript file path. `--file PATH` and `--screenshot PATH`
attach other evidence (at most 8 files, 4 MiB in total).

What happens:

1. Kei finds the transcript (or uses the session or file given).
2. Token-shaped strings are redacted on the user's machine before anything is
   sent: API keys (Anthropic, OpenAI), GitHub and Slack tokens, AWS keys,
   JWTs and `Bearer` tokens, private-key blocks, Kei runtime tokens, and
   `password=` / `token=` / `secret=` style values. Each becomes
   `[REDACTED:<kind>]`.
3. The CLI prints a preview: the description, each evidence file with its
   size, and the redaction counts per kind (never the content). Then it asks
   `Send? [y/N]`.
4. Anything other than `y`/`yes` cancels: `Feedback not submitted.` and
   nothing leaves the machine.
5. If a Kei runtime token turns up in a transcript, the CLI warns that it is a
   leak: rotate the credential (`kei bot credential --rotate`, see
   `kei-credential-rotation`) and say where it came from in the report.

Only transcripts are redacted. `--file` and `--screenshot` are sent as they
are, so check them for secrets first. Plain Claude Desktop chat sessions
(not Claude Code) are not supported yet.

**As an agent, give the user the command; do not send it for them.** The
confirmation is the user's preview of what leaves their machine. Never add
`--yes`, which skips it. In Claude Code the user can run it in the session by
typing `! kei feedback ...`.

## Troubleshooting setup

This section catalogs real failures observed during harness setup (e2e,
2026-10-05/06) and in production (2026-10-08). Each entry lists the symptom, root cause, and fix. The
matching `kei-setup-doctor` skill has a condensed version for diagnosis
workflows.

### 1. oh-my-zsh alias shadows the Kei CLI

**Symptom:** `kei` runs `kubectl edit ingress` (oh-my-zsh kubectl plugin)
instead of the Kei CLI. `kei --version` returns kubectl help.

**Cause:** oh-my-zsh defines `alias kei='kubectl edit ingress'`, which
shadows the Kei binary on `PATH`.

**Fix:** `unalias kei` in the current shell, or add `unalias kei` after
`source $ZSH/oh-my-zsh.sh` in `~/.zshrc`. Use `command kei` to bypass
aliases.

### 2. kei or kei-proxy not installed, or wrong version

**Symptom:** `command -v kei` fails, or `kei --version` reports `< 0.1.13`
(resp. `kei-proxy --version` `< 0.1.26`).

**Cause:** The installer was not run, or the installed binary is outdated.

**Fix:** Re-run the installer and ensure `~/.local/bin` is on `PATH`:

```sh
curl -fsSL https://haikeilabs.com/install.sh | bash -s -- -d ~/.local/bin
```

### 3. Not logged in

**Symptom:** `kei workspaces list` fails with a login error.

**Cause:** No valid Kei session. `kei login` uses device-code flow — a
person must approve in the browser.

**Fix:** Run `kei login` and approve the code in the browser. The approving
account must be an owner or admin of the organization.

### 4. No runtime installation (new machine)

**Symptom:** `~/.config/kei.yaml` does not exist, or `kei runtime bootstrap`
returns 401.

**Cause:** This machine has never been set up with Kei, or its credential was
revoked. Each machine needs its own runtime installation and credential —
credentials are never shared across machines.

**Fix:** The setup scripts (`setup-*.sh`) create a new installation
automatically. Manual path:

```sh
INSTALL_NAME="<kind>@$(hostname -s)"
WS_ID=$(kei workspaces list | grep -oE '[a-f0-9-]{36}' | head -1)
INSTALL_ID=$(kei bot init --platform cli --name "$INSTALL_NAME" --workspace "$WS_ID" | grep -oE '[a-f0-9-]{36}' | head -1)
kei bot credential --installation "$INSTALL_ID" --workspace "$WS_ID" | kei setup --control-plane-url https://app.haikeilabs.com
kei runtime bootstrap
```

The credential is piped directly into `kei setup` and is never printed to the
terminal or stored in a file.

### 5. "pending" installation status (no heartbeat yet)

**Symptom:** `kei bot status` shows `"status":"pending"`.

**Cause:** The runtime has not sent its first heartbeat. `pending` is not an
error — it simply means heartbeat has not arrived yet.

**Fix:** Wait for the next heartbeat cycle. If it stays `pending` after
several minutes, check network outbound from the runtime to the control plane
and verify `KEI_RUNTIME_TOKEN` is present in the environment. Do not attempt
to bind, rotate credentials, or restart the runtime for a `pending` status
alone.

### 6. Background heartbeat service not installed

**Symptom:** No `kei runtime service` command, or the service is not
running. The runtime may stop heartbeating after the terminal session ends.

**Cause:** `kei runtime service install` ships in HAI-406 (not yet released).

**Fix:** After upgrading kei to a version that includes `kei runtime service
install`, run:

```sh
kei runtime service install
```

Until then, ensure the process has a supervision mechanism (systemd unit,
launchd plist, container restart policy) that keeps it running.

### 7. "No registered harnesses selected" after harness add

**Symptom:** `kei harness sync --harness <kind>` prints "No registered
harnesses selected" even though `kei harness add` succeeded.

**Cause:** The policy bundle cached by `kei-proxy` is stale (HAI-403). The
new harness registration is not reflected in the bundle until the next
refresh cycle (background poll interval, or a manual policy edit).

**Fix:** Any policy edit (e.g. adding or removing a harness command policy)
triggers a bundle refresh. If no policy edit is available, wait for the
background refresh (up to 6 hours). Workaround below. In your answer, point
to `kei-harness-policy` `references/bundle-versioning.md` for how bundle
versions and the 6-hour reuse window work. Workaround:

```sh
# Force a bundle refresh by touching a policy
kei policies update <any-policy> --workspace WS --description "no-op refresh"
kei harness sync --harness <kind>
```

### 8. Policy bundle version rollback after switching installations

**Symptom:** After switching to a different runtime installation (new
credential, new bootstrap), the policy bundle loaded by `kei-proxy` is a
stale version from the previous installation. Protected calls use incorrect
(or empty) policy rules.

**Cause:** `kei-proxy` caches the policy bundle on disk at
`~/Library/Application Support/kei-proxy` (macOS) or
`~/.local/share/kei-proxy` (Linux) keyed by installation ID. When the
installation changes, the old cached bundle may be loaded if the cache
directory is not cleared (HAI-404).

**Fix:** Move the proxy cache directory aside before bootstrapping with the
new installation:

```sh
mv ~/Library/Application\ Support/kei-proxy ~/Library/Application\ Support/kei-proxy.bak.$(date +%s)
# or on Linux:
# mv ~/.local/share/kei-proxy ~/.local/share/kei-proxy.bak.$(date +%s)
kei runtime bootstrap
```

After confirming the new bundle is correct, remove the backup directory.

### 9. "policy bundle candidate rejected: invalid policy bundle schema" — dst_pattern does not match

**Symptom:** `kei-proxy` logs or `kei-proxy runtime bootstrap` returns:
```
policy bundle candidate rejected: invalid policy bundle schema ... dst_pattern 'web_search' does not match
```

The specific tool (`web_search`) is denied, but other protected calls still
work — the bundle is accepted; the bare dst row is skipped.

**Cause:** A policy targets a bare tool name as its `dst_pattern` (e.g.
`web_search`), but the policy bundle schema requires a `tool:` prefix (e.g.
`tool:web_search`). The catalog now skips bare dst rows with
`skip_reason: bare_target` instead of rejecting the entire bundle. Each
skipped row grants nothing (HAI-372).

**Fix:** Update the policy's `dst_pattern` from the bare name to
`tool:<name>` in the Kei console (**Policies →** select the policy → edit
the destination pattern). For example, change `web_search` to
`tool:web_search` and `read_file` to `tool:read_file`.

```text
# Before (bare dst row, skipped)
dst_pattern: web_search

# After (enforced at call time)
dst_pattern: tool:web_search
```

If the policy was created through the CLI, re-create or update it:

```sh
kei policies update <name-or-id> --workspace WS --dst-pattern tool:web_search
```

Once the fix is applied, re-run `kei runtime bootstrap` or restart
`kei-proxy serve` to reload the bundle.

### 10. Every protected tool call denied (fail-closed)

**Symptom:** Every `kei-proxy authorize` returns a non-zero exit. Tools that
previously worked are now denied.

**Cause:** `KEI_PROXY_DISABLED=true` is set, `KEI_RUNTIME_TOKEN` is missing,
`KEI_RUNTIME_CONTROL_PLANE_URL` is wrong, or kei-proxy is not on `PATH`.
When kei-proxy is disabled, misconfigured, or unreachable, it denies every
protected call (fail-closed, HAI-249).

**Fix:** Check environment variables:

```sh
echo "KEI_PROXY_DISABLED=${KEI_PROXY_DISABLED:-unset}"
echo "KEI_RUNTIME_TOKEN=${KEI_RUNTIME_TOKEN:+present}"
echo "KEI_RUNTIME_CONTROL_PLANE_URL=${KEI_RUNTIME_CONTROL_PLANE_URL:-unset}"
command -v kei-proxy
```

Unset `KEI_PROXY_DISABLED` or set it to `false`, inject the token from the
secret manager, and confirm the URL is `https://app.haikeilabs.com` (no
trailing `/api/v1`). Then test with a known-permitted tool:

```sh
kei-proxy authorize --user U --tool T --action A --resource R; echo $?
```

### 11. Native config is stale after policy update

**Symptom:** Policy changes in the console are not reflected in the
harness's native config (e.g. `~/.claude/settings.json` still has old
`permissions.allow` entries).

**Cause:** The background bundle refresher updates `kei-proxy`'s in-memory
policy, but does not re-render the native config. Re-rendering needs an
explicit `kei harness sync`.

**Fix:**

```sh
kei harness sync --dry-run --harness <kind>   # preview changes
kei harness sync --harness <kind>             # apply
```

See `kei-harness-policy references/bundle-versioning.md` for the 6-hour
refresh window and versioning model.

### 12. Runtime credential was lost (no recovery)

**Symptom:** The `KEI_RUNTIME_TOKEN` environment variable is missing, and
the secret manager no longer has the value. There is no backup.

**Cause:** The credential was shown once at creation and never stored.

**Fix:** Kei stores only a hash — the plaintext cannot be recovered. Rotate
the credential:

```sh
kei bot credential --installation <ID> --rotate | <secret-manager import>
```

Update the environment variable on every consumer, then restart or reload the
runtime. Each rotation invalidates the previous credential immediately.

### 13. Every protected tool call denied with `policy_bundle_expired`

**Symptom:** Every protected tool is denied, including ones that worked
before and local tools such as `web_search`. The decision carries
`reason_code: policy_bundle_expired` and `deny_source: runtime_state`. The
console **Agents** page shows Policy bundle **Not ready** with the reason
**bundle expired**.

**Cause:** The bundle's `not_after` has passed. The catalog issues bundles
valid for 12 hours and does not reissue one when it expires ([HAI-427](https://linear.app/haikeilabs/issue/HAI-427)), so
every runtime in the workspace goes dark 12 hours after the last policy edit,
even while it is online and refreshing. (A runtime that was offline past
`not_after` shows the same symptom; restore connectivity first.)

**Check:** Look at the persisted bundle. `<state_dir>` is
`KEI_RUNTIME_STATE_DIR`, by default `~/Library/Application Support/kei-proxy`
(macOS) or `~/.local/share/kei-proxy` (Linux).

```sh
kei-proxy policy show                                   # state: expired
jq '{bundle_version, issued_at, not_after}' "<state_dir>/policy/bundle.json"
jq '{state, expires_at, highest_bundle_version}' "<state_dir>/policy/state.json"
```

`not_after` / `expires_at` in the past confirms it.

**Fix:** Make any policy edit in the workspace, in the console or with
`kei policies update`. A no-op change is enough: it forces the catalog to
issue a new bundle. A runtime running `kei-proxy serve` or
`kei-proxy runtime heartbeat` picks it up on its next poll (60 s by
default); otherwise run `kei-proxy policy sync`. `kei-proxy policy show`
should then report an active bundle with a future `not_after`. Until [HAI-427](https://linear.app/haikeilabs/issue/HAI-427)
ships, this recurs after every 12 hours without a policy edit.

## Validation commands

```sh
ls "$SKILLS_DIR" | grep '^kei'                          # skills installed
head -3 "$SKILLS_DIR/kei-cli/SKILL.md"                  # frontmatter starts with ---
kei-proxy runtime bootstrap | jq '.workspace_id'        # runtime scoped to a workspace
kei-proxy authorize --user U --tool T --action A --resource R; echo $?
kei harness list --installation INSTALLATION_ID --json | jq '.harnesses[].agent_name'   # registered harnesses (kei >v0.1.6)
kei connector-bindings list --workspace WS --json        # agent↔connector wiring (not a permission gate)
```

## Realistic usage boundaries

- Do not paste runtime tokens into harness config
  files in a repo, or into the conversation.
- Installing skills changes what the agent knows, not what it may do. Policy in
  the workspace decides that.
- A connector binding is wiring only (ADR-038 §4); it never gates permission.
  Allow/deny comes from workspace policy — group membership and matching
  targets — so a binding alone proves nothing about access.
- Agent creation/general CRUD remain outside the CLI; existing agents can be
  moved with `kei agents move` (preview with `--dry-run` first).
- The explicit Harness resource and short-lived runtime identity in the ADRs
  are planned. Do not present them as available.
- The installation-claim handshake IS available for chat-platform
   identities via the claim-link enrollment flow (see section 8 above), but is
   NOT available for generic harness-to-installation linking.

## Related skills

- `kei-harness-policy` — authoring harness command policies, importing native
  rules, and syncing the rendered config. See also the
  [permissions model reference](../kei-harness-policy/references/permissions-model.md)
  for how Kei compiles policies into native config, the audit-only hook, and
  Kei-only permission management.
- `kei-openai-backends` — model format support across five families (OpenAI,
  Anthropic, Qwen, DeepSeek, GLM), including tool-definition rendering, reasoning
  adapters, and eval ModelBackend variants. Each family has distinct tool-call
  formats: Anthropic uses `input_schema` with `thinking` content blocks; OpenAI
  and DeepSeek use JSON function-calling with `reasoning_content`; Qwen and GLM
  have their own variants. The skill covers the per-family tool-definition
  schemas (`render_tools`) and reasoning-content extraction.
- `kei-runtime-setup` — the runtime installation and bootstrap half of the
  harness setup workflow.
- `kei-proxy` — the runtime binary the harness calls for allow/deny decisions.
- `agentware-sdk` — the SDK with `KeiProxyEvaluator` and policy enforcement.
