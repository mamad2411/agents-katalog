---
name: kei-pi-setup
description: "Install and configure Kei's Pi adapter (`kei-lime-pi`), connect Pi to the local `kei-proxy` Unix socket, recommend a starter policy set (`shell:kei`, `shell:kei-proxy`, read-only shell basics, `tool:pi.read`) and create only the rows the user accepts, use existing `shell:` policies for Pi Bash, and verify fail-closed behavior. Use when setting up or updating Pi for Kei, choosing Pi's first policies, installing the Pi package, checking whether Pi calls use the daemon, or asking about Pi Bash policy and audit behavior. For generic Claude Code/Codex/OpenCode setup use `kei-harness-setup`; for creating or bootstrapping the runtime use `kei-runtime-setup`."
---

# Set up Pi with Kei

Pi uses the `HaikeiLabs/kei-lime-pi` extension package to connect to the
same-host `kei-proxy` runtime. Pi has no policy engine and never receives the
runtime credential. Use the package source and its README as the implementation
contract; do not infer support from a policy or tool row alone.

## Quick answers

- Installing packages does not itself grant policy permission; an active policy
  must separately authorize an operation.
- The current Pi package does not implement `search_wiki` or `web_search`. If
  asked, say explicitly that the current package **does not implement** the
  named tool and a policy does not create its Pi-side executor. Do not call a
  provider directly as a fallback; fail closed. Do not answer only that a
  policy is insufficient; state the missing implementation plainly.
- The raw command text is not stored or logged.
- Pi Bash uses existing `shell:` policies, not a broad `tool:pi.bash` grant. If
  asked whether to grant `tool:pi.bash`, explicitly say no: use a `shell:` rule
  instead. It requires `kei-proxy` 0.2.4 or later. Compound or unsupported
  syntax is denied before execution. State explicitly that raw command text is
  **not stored or logged** in the audit; the audit retains the SHA-256 argument
  digest. Do not rely on saying only that a digest is retained.
- Before setting Pi up, show the user the recommended starter policies below
  and ask which to create. Create only the ones they accept.

## Recommend starter policies before setup

Pi's Kei gate permits only what a policy allows, so a fresh setup without
policies blocks almost every call. Before you install or configure anything,
show the user this starter set, explain each row, and ask which rows to create.
The user may drop any row. Do not create a policy the user has not accepted,
and do not add rows of your own.

| Target | Why |
| --- | --- |
| `shell:kei` | Lets Pi run the `kei` admin CLI. |
| `shell:kei-proxy` | Lets Pi check the runtime (`kei-proxy policy show`). |
| `shell:git status`, `shell:git diff`, `shell:git log` | Read-only Git. |
| `shell:ls`, `shell:rg`, `shell:cat`, `shell:pwd` | Read-only basics. |
| `tool:pi.read` | Lets Pi's `read` tool open files. |

Tell the user these things when you present the set:

- **`shell:kei` and `shell:kei-proxy` are broad on purpose.** They permit every
  subcommand. The user is an admin, and Kei's server-side authorization still
  limits what any `kei` call can do.
- **`kei` acts with the user's own session, without a prompt.** The `kei` login
  token is in the OS keychain of the same OS user that runs Pi. Any `kei`
  command the agent runs uses the user's session, including write commands
  such as `kei policy create` and `kei policy delete`. Accepting `shell:kei`
  lets the agent change policies, including its own.
- **A `shell:` row is an argv prefix.** `shell:git status` permits
  `git status --short` but not `git push`. `shell:cat` reads any file the OS
  user can read. One simple command is evaluated at a time.
- **`shell:*` and `tool:pi.bash` never permit a shell call.** Only a literal
  `shell:` prefix can, so do not offer either one as a shortcut.
- **`tool:pi.read` is decided by tool name.** The runtime records the file's
  canonical path in the audit, but it does not match the path against policy,
  so this row permits reads of any path, and a `path:` policy does not permit
  Pi's file tools. It also needs the `pi.read` registration from the adapter's
  `tool-manifest.v4.json` (see "Local filesystem tools"). Leave out
  `tool:pi.write` and `tool:pi.edit` unless the user asks for them.
- **These rules are not limited to Pi.** A standing policy names a group, not a
  harness: `harness:` sources and harness conditions are retired. The rules
  apply to every member of the group, and `kei harness sync` also renders the
  `shell:` rows into Claude Code, Codex and OpenCode settings.

Ask which group the rules apply to. A group the user belongs to keeps them
narrow; `autogroup:admin` reaches every admin and owner in the workspace. List
groups with `kei groups list --workspace WORKSPACE`; create one only if the
user asks. Then create each accepted row with its own command:

```sh
kei policy create --workspace WORKSPACE --group GROUP --allow shell:kei
kei policy create --workspace WORKSPACE --group GROUP --allow shell:kei-proxy
kei policy create --workspace WORKSPACE --group GROUP --allow "shell:git status"
kei policy create --workspace WORKSPACE --group GROUP --allow tool:pi.read
```

Quote a target that has a space. Check `kei policy create -h` first, and use
the `kei-harness-policy` skill for the policy model. The older `kei policies`
alias and its `--src-pattern`/`--dst-pattern` flags are
deprecated; do not use them. Confirm a rule with
`kei policy test "shell:git status" --workspace WORKSPACE --as group:GROUP`.

## Separate the two Pi packages

- `HaikeiLabs/skills` installs the agent instructions. It does not install the
  Pi adapter or grant access.
- `HaikeiLabs/kei-lime-pi` installs the Pi extension. It does not create a
  runtime installation, connector binding, tool plan, or permission.

Installing the packages does not itself grant policy permission; an active
policy must separately authorize the operation. Tell users this when giving
setup instructions. Install both from GitHub with Pi's package manager:

```sh
pi install git:github.com/HaikeiLabs/skills
pi install git:github.com/HaikeiLabs/kei-lime-pi
pi list
```

Use `pi install -l ...` to store either package in the current project's
`.pi/settings.json` instead of user settings. For a temporary test without
changing settings, use `pi -e git:github.com/HaikeiLabs/kei-lime-pi`. Pi loads
package extensions on startup; restart Pi or use `/reload` after installation.
The adapter is a trusted extension with full Pi-user permissions. Review its
source before installing it. Do not install from npm; the supported package
source is the GitHub repository.

## Runtime prerequisite

Set up the customer-owned runtime on the same machine as Pi using the
`kei-runtime-setup` and `kei-cli` skills. The installed `kei-proxy` must support
the tokenless owner-session Unix-socket path and v2 connector invocation.
Pi Bash policy support requires `kei-proxy` 0.2.4 or later. Check the daemon
and bundle with:

```sh
kei runtime bootstrap
kei-proxy policy show
```

The extension uses `KEI_RUNTIME_SOCKET_PATH` when set; otherwise it uses the
proxy's platform default (`$TMPDIR/kei-proxy/runtime.sock` on macOS,
`/run/kei-proxy/runtime.sock` on Linux). Keep `KEI_RUNTIME_TOKEN` in the
runtime's protected configuration/secret store. **Do not put it in Pi's
settings, environment, prompt, or project files.** Pi calls only the owner-only
Unix socket; the daemon holds the credential and binds supported calls to the
installation-owner session. The socket is a same-OS-user boundary, not a
process-specific one.

## What the adapter checks

### Local filesystem tools

Pi `read`, `write`, and `edit` calls are intercepted before execution and
mapped to `pi.read`, `pi.write`, and `pi.edit`. The request includes the
canonical absolute path, an argument digest, framework, and span metadata; it
does not send file contents or raw arguments. Only an explicit permit lets Pi
execute the original local tool. Policies for these local file operations are
separate from connector authorization. The active bundle must include the matching
`pi.read`, `pi.write`, or `pi.edit` tool registration and policy; a missing
registration or policy denies the call. A connector permit does not grant
local file access.

### Bash command policies

**Short answer:** Pi Bash uses existing v2 `shell:` argv-prefix policies with
harness kind `pi`, not a broad `tool:pi.bash` permission. Pi Bash requires
`kei-proxy` 0.2.4 or later. Only one simple command in a restricted grammar is
supported; compound commands and unsupported syntax are denied before execution.
When answering Bash questions, explicitly state all of these facts: existing
`shell:` policies authorize the command; `kei-proxy` 0.2.4 or later is required;
compound or unsupported syntax is denied before execution; raw command text is
not stored or logged in audit; and the audit retains the SHA-256 argument digest.
Do not answer the audit question with only “the audit stores a digest.”

The command text is sent only over the local Unix socket for policy matching;
it is not sent to the control plane or stored in audit.
Audit records retain the SHA-256 argument digest, decision, span ID, and any
denial reason. Do not expect the original command to be shown or recovered from
the digest.

A permitted command still runs with Pi's user permissions; this gate is not an
OS sandbox. Do not add a broad `tool:pi.bash` permit as a substitute for a
`shell:` policy.

### Connector tools

The extension registers one Pi tool, `kei_connector`. It accepts the exact
registered v2 `tool_name` plus that tool's `arguments` and `context`, then:

1. sends the complete operation for `POST /v1/preflight`;
2. proceeds only with a valid, explicit permit and preflight handle;
3. obtains the credential via `POST /v1/credentials:release`.

Pi then calls the upstream API directly with the released credential. The
daemon validates the plan, consumes the handle once, decides policy, and
resolves the credential. Pi must not call a provider directly without the
released credential. The tool name and argument and context schemas must
exactly match the v2 tool plan in the active bundle.
Connector calls also require an agent binding and a matching policy.

### Unsupported tools

The extension blocks unknown Pi tool calls. It currently does not implement
`web_search` or `search_wiki`; policy or harness registration does not create a
Pi-side executor or grant permission. When asked about an unsupported tool,
explicitly answer that the current Pi package does not implement it, then state
that the executor is missing and reject calling a provider directly as a
fallback; unsupported calls fail closed. Do not answer only that policy is
insufficient. Supporting another tool requires a reviewed Pi-side executor plus
the corresponding runtime registration and policy path. Until one is registered,
the block stays fail-closed: do not call a provider directly as a fallback for
the missing tool. Connector-backed work must use the connector flow (preflight,
credential release, then the provider call with the released credential), not a
local permit followed by a direct provider call.

## Verify the setup

1. `pi list` shows both packages, or the project `.pi/settings.json` contains
the project-scoped entries.
2. Start Pi and confirm the extension loads and `kei_connector` is available.
3. Confirm `kei-proxy policy show` reports an active v2 bundle.
4. Test a known-permitted operation and a deliberately unbound operation.
   The denied call must not execute, and a missing daemon, malformed response,
   timeout, stale/invalid bundle, or missing policy must fail closed.
5. For Bash, test one permitted simple command, an unmatched command, and
   compound/unsupported syntax. Confirm denied calls do not execute and audit
   records contain a digest rather than raw command text.
6. For connector tests, use a disposable read. Verify the decision in
   redacted audit metadata; do not log credentials or provider payloads.

Installing packages is not proof that Pi calls are checked. Do not claim
success until the extension has been loaded and a denied operation has been
observed before execution.

## Troubleshooting

- **`kei_connector` is missing:** check `pi list`, project trust for a project
  install, then restart Pi or run `/reload`.
- **Runtime socket unavailable:** verify `kei-proxy serve` is running as the
  same OS user and that `KEI_RUNTIME_SOCKET_PATH` points to its socket. Do not
  expose the runtime token to Pi as a workaround.
- **Connector preflight denies:** verify the exact tool name and schemas, active
  v2 bundle, connector tool plan, agent binding, and matching policy. The
  extension cannot manufacture any of them.
- **Bash reports unsupported simple-command syntax:** only one supported simple
  command is evaluated. Remove shell composition or unsupported syntax; do not
  retry by bypassing the adapter.
- **An unrecognized tool is blocked:** this is intentional. Add a reviewed Pi
  executor and runtime registration; do not bypass the gate or call the
  provider without the released credential.

## Validation commands

In a checkout of `kei-lime-pi`:

```sh
npm test
npm run typecheck
pi -e .
```

For the running installation:

```sh
pi list
kei-proxy policy show
```

## Realistic usage boundaries

- Pi Bash is limited to the supported simple-command grammar and existing
  `shell:` policies. This is not an OS sandbox for permitted commands. MCP and
  arbitrary Pi extensions remain outside the gate.
- Policy and runtime registration determine what is allowed; package
  installation does not grant permission.
- The starter set is a recommendation, not a default: nothing is created until
  the user accepts it. Standing policies cannot be limited to Pi, and the
  current runtime cannot narrow `tool:pi.read` to a path.
- Pi receives connector credentials only via the release step and calls the
  provider directly only with the released credential, never as an ungated
  fallback.
- For general harness setup use `kei-harness-setup`; for runtime installation,
  credential delivery, or bootstrap use `kei-runtime-setup` and `kei-cli`.
- Source of truth: `HaikeiLabs/kei-lime-pi` README and code, Pi's package and
  extension documentation, and the active v2 policy bundle.
