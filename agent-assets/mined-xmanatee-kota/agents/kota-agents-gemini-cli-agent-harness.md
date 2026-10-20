# Gemini CLI Agent Harness Module

Adapter module that registers the `gemini-cli` harness. The harness shells out
to the installed Gemini CLI in headless structured-output mode instead of using
`@google/genai` directly and honors Gemini CLI's cached Google sign-in / Code
Assist auth state.

Route work here with the `gemini-cli` preset, default harness config, or a
per-step `harness` value.

Gemini CLI remains the Google enterprise and API-key native CLI path. Google
individual-account OAuth is not served by Gemini CLI; use the existing
`antigravity-cli` preset for that account type.

## Provider Routing

Models are passed to `gemini --model` verbatim. The shipped `gemini-cli`
preset intentionally uses the same Gemini model tier names as the SDK-backed
`gemini` preset; the difference is the runtime and auth boundary, not a
separate model catalog.

Credential-bearing native launches currently fail closed. The readiness probe
reports cached Gemini CLI OAuth / Code Assist credentials and Gemini API keys
as unavailable until a provider-only broker can keep them outside Gemini's
native process tree. Runs force Gemini's encrypted file credential backend
into the invocation-isolated home and create a credential-free
`GEMINI_CLI_HOME` containing only a non-API-key selected auth mode plus
KOTA-owned system settings. An API-key selection is itself rejected because it
may refer to a system-Keychain-backed key. Those settings disable MCP,
extensions, skills, and local environment loading. The outer OS
sandbox hides repository `.gemini/` and `.agents/` trees so hooks, policies,
discovery commands, and other executable workspace configuration cannot load,
even though the session-only `--skip-trust` flag is still required for Gemini
CLI's headless bootstrap.

## Loop Shape

The adapter runs one non-interactive CLI process per KOTA harness call:

1. Compose the KOTA system prompt, workflow rails, and task prompt into one
   `--prompt` payload.
2. Spawn `gemini --sandbox --skip-trust --prompt <payload> --output-format
   stream-json --model <model>`.
3. Run the CLI inside KOTA's outer native-CLI OS sandbox. Gemini's nested tool
   sandbox keeps model tools offline and hides provider login state. Plan mode
   is read-only; autonomous bounded writes use `auto_edit`, so shell or other
   permission-requiring effects fail closed in headless mode. Scope-policy
   paths are the only worktree writes;
   allowed scope-policy paths are projected into the run worktree. Reads stay
   within system/tool runtime, workspace dependencies,
   workspace, and invocation roots; Git metadata and machine authority stay
   read-only, while workflow runtime owns index staging and commits. Network
   access is restricted to declared Google model and
   authentication endpoints through KOTA's host-owned proxy.
4. Parse newline-delimited JSON events. Normalize init, assistant text, tool,
   error, and result events into `KotaAgentMessage`; preserve unknown events as
   raw adapter frames. Assistant message chunks also stream to the optional
   `AgentHarnessWriter`.
5. Return the neutral `AgentHarnessResult`.

Cancellation terminates the CLI process group so spawned tools cannot outlive
the CLI, and the run-local quarantine barrier stays pending until the group
leader has closed.

`autonomyMode: "passive"`, denied writes, and denied destructive effects map to
Gemini CLI plan mode. Other runs use `auto_edit`; permission requests KOTA
cannot route fail closed in headless mode.

## Capability Boundary

Gemini CLI owns its own tool runtime, MCP configuration, checkpointing, and
approval loop. KOTA also requires Gemini's nested tool sandbox.
This adapter does not expose KOTA's tool registry, `canUseTool`, MCP servers,
owner-question tool, or supervised approvals to the CLI. It declares
`toolControl: "native"`. Scope writes are enforced by the shared OS sandbox,
and stricter live policy revisions abort the process. It still injects
KOTA workflow rails into the prompt, but those rails are prompt-level
instructions rather than KOTA-enforced tool guardrails. Structured CLI events
do feed KOTA's message-stream and trajectory diagnostics; observation does not
change which runtime owns tool authorization.

Do not treat this adapter as an autonomous builder-equivalent until guarded
tool control and provider-only authentication both exist. Credential-free
launches remain available for boundary diagnostics, but authenticated provider
runs are intentionally unavailable.
The unsupported tool-control options are declared on the harness and reported
through readiness; direct callers that pass them fail before Gemini CLI starts.

## Release Channel

Assume the operator-installed `gemini` binary is from the stable Gemini CLI
channel unless the operator explicitly installs preview or nightly. Readiness
reports the exact local path and `gemini --version` output.

Persistence/resume remains an explicit capability exception while authenticated
execution is unavailable: an invocation home cannot safely become durable state
inside the same native tool process tree. The Gemini SDK adapter supplies durable
reconstruction without this native credential boundary. Credential-free native
diagnostics retain ordinary run evidence, not a claimed recoverable conversation.
