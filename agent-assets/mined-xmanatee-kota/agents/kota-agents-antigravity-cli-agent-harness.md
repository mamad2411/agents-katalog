# Antigravity CLI Agent Harness

This module owns KOTA's native adapter for Google's Antigravity CLI. Keep AGY
flags, event translation, login projection, readiness, and provider endpoints
inside this adapter rather than branching on the harness name elsewhere.

## Runtime Boundary

AGY owns its model tool loop, tool catalog, skills, plugins, MCP configuration,
and browser implementation. KOTA owns process cancellation, workspace mode,
machine-authority isolation, provider egress, and the non-interactive permission
disposition. The adapter rejects per-tool controls that cannot be enforced at
that process boundary.

Each run creates an invocation-local AGY project bound to the requested working
directory and consumes `stream-json`. KOTA's machine-authority sandbox is the
outer filesystem, process, and egress boundary. Because headless AGY cannot
service permission prompts, the adapter auto-approves AGY-native tools inside
that boundary without adding a second AGY terminal sandbox. Edit-capable runs use
`accept-edits`; read-only projections use `plan` with no writable scope.
Translate native events into
`KotaAgentMessage` frames here; preserve unknown frames as `raw` messages.
Gemini models receive AGY's `low`, `medium`, or `high` effort flag, with
stronger KOTA levels capped at AGY's highest supported value. Models with
intrinsic reasoning, such as Claude Thinking, receive no separate effort flag.
Command-bearing tool events carry exact and prefix fingerprints for durable
adherence checks; raw command parameters remain provider tool I/O and must not
be persisted as trace text.

Interactive clients remain multi-turn through KOTA's transcript composition.
The adapter starts one isolated AGY process per turn and resumes a durable AGY
conversation by its native conversation id when core supplies one. Each
invocation still receives a fresh isolated home; provider conversation state
never becomes local runtime authority. Core checkpoints the remote conversation id as soon as AGY reports it; repairs
and retries use that exact id. Remote retention remains provider-owned; errors
retain the checkpoint and run evidence rather than silently starting over.

The CLI's own print timeout is only a final process cap. KOTA cancellation and
workflow idle supervision remain the normal lifecycle controls. Cancellation
sends a graceful signal to the isolated process group, then keeps the native
abort quarantine closed until AGY emits a terminal result for the remote
attempt and the local process settles. A local exit without that remote
terminal frame is an unconfirmed-stop failure regardless of exit code or caller
cancellation. Core durably excludes its owner and native identity from reuse.
Validation, sandbox preparation and proven failed spawn leave no remote attempt;
the stop barrier settles those failures so environment repair can resume the
retained conversation. Errors after launch require remote terminal confirmation.

Workflow `outputSchema` values pass through AGY's native `--json-schema`
surface; core still validates the normalized structured result. A terminal AGY
`SUCCESS` is transport success when AGY omits response text without an
unrecovered tool failure, and carries the typed
`antigravity_cli_empty_output` subtype so workflow productivity policy can
distinguish it from useful output. A tool failure followed by an empty terminal
success is a harness error; workflow validators still decide whether otherwise
successful work satisfies the task. A missing terminal result is a transport
failure.

## Isolation

Daemon runs use an invocation-local home and ordinarily inherit no provider,
GitHub, notification, or cloud credentials. On macOS, project only the host's
encrypted `login.keychain-db` file read-only at the standard path inside that
home; never expose the whole Keychains directory or inspect the token. AGY owns
credential lookup and refresh. KOTA's outer sandbox owns the filesystem and
egress boundary; do not infer a native-tool credential exclusion from an outer
read grant needed by the provider process.

Contained subscription login projection remains unimplemented. AGY's published
1.1.3 changelog describes file-based token storage on headless Linux without a
D-Bus session; an OS keyring is therefore not an unconditional prerequisite.
Before projecting that login, establish the selected Linux release's file
location, refresh behavior and native-tool credential exclusion through an
authorized isolated probe or equivalent vendor contract evidence. The shared
container-auth owner can snapshot a single file, but a read-only mount alone
does not prevent native tools from reading its contents. Do not invent a token
format, export the host keychain, or substitute API credentials. Auth resolution
rejects before discovery and execution until that contract is implemented.

The OS sandbox permits AGY's internal loopback listener, but outbound traffic
still goes only through KOTA's host-owned allowlisted proxy. In provider-egress
eval containers that proxy chains allowed CONNECT requests through the
eval-configured Docker-network proxy; it never opens a direct provider route.
Effective scope policy paths are projected into the run worktree before
launch; passive or write-confirmation runs can write only to invocation state.
Git metadata remains read-only and machine authority remains protected. Agents
leave workspace changes unstaged; workflow runtime owns index staging and
commit creation after validation.

## Model Routing

The shipped preset selects the strongest current AGY model and always passes an
explicit model plus only the reasoning controls that model supports. The
required local auth probe uses `agy models` to
verify that AGY can acquire credentials and access the requested catalog without
KOTA reading them. AGY owns credential lifetime and renewal. Do not infer
support from older Gemini CLI model catalogs. Catalog entries are
effort-qualified for Gemini and intrinsic for models such as Claude Thinking;
availability checks must resolve the exact catalog entry KOTA will execute.
