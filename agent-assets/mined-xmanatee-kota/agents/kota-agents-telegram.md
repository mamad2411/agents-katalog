# Telegram Module

This directory owns the Telegram integration — interactive bot access and
notification forwarding.

- Contributes two daemon channels: `telegram-status` for readiness/status
  command declaration and `telegram-interactive` for chat sessions. The
  interactive channel owns the single Bot API `getUpdates` stream; never add
  a second daemon long-poll loop for the same token.
- On-demand digest and attention commands render directly and reply in-band,
  without cadence writes, counter changes, digest events or quiet-hour gating.
  Distinguish no attention items from command failure. These operator surfaces
  must never enter autonomy-agent prompts.
- Read, capture, and retract commands are thin wrappers over their
  `KotaClient` namespace and render through the owning module's
  plain-text helper — no copy of CLI rendering on the Telegram side.
  They are allowlist-gated, do not advance cadence counters or emit
  workflow events, and are operator-facing only.
- On multi-scope daemons, Telegram resolves one scope per chat
  before running commands or interactive sessions. Defaults live in
  `modules.telegram.chatScopeBindings`; `/scope` lists hosted
  scopes and updates the daemon-owned per-chat selection. Unbound
  chats fail with an explicit reply instead of falling back to the
  active/default scope. Single-scope daemons do not show scope
  labels and do not need `/scope`.
- Per-store search uses the client semantic-search boundary. Empty queries
  return usage without calling it; distinguish empty results from failures.
  Unavailable semantic search must not silently degrade to keyword search.
- `/recall` is the unified-recall entry point — one ranked,
  source-tagged list spanning every registered store. The recall seam
  owns merge, normalize, and ranking; the Telegram handler does not
  fan out to per-store search seams. Distinguish empty hits from missing
  contributors in the reply.
- Answer commands use the answer owner's shared command replies with the selected
  scope client. Telegram owns command parsing, truncation and detail segmentation.
  The seam owns retrieval, synthesis, citation parsing and retries; Telegram adds no prompt, parser or budget.
- Semantic read commands delegate query validation, request defaults and reply
  selection to each domain's `commands.ts`, using the selected scope client.
  Channels retain parsing, admission and output limits; recall uses only its
  cross-store client seam.
- Capture and retract commands delegate empty-input handling, request construction
  and replies to their capability owners. Telegram retains target mapping,
  parsing and output limits; the umbrella `/retract` only prints help.
- Contributes notification subscriptions for workflow events.
  Optional event filters must not suppress urgent owner/approval
  escalation notifications.
- Notification subscriptions, pending callbacks, and poll-conflict deduplication
  are activation-local; the returned activation disposer releases only the
  loader host that created them.
- Bind each approval button to its chat/message, approval id, and review digest;
  never let reused short ids reactivate stale buttons.
- Owner-question answer and dismiss callbacks require the stored chat/message
  binding before accessing either the scoped client or the local queue.
- Interactive sessions use configured autonomy explicitly. Missing
  session-autonomy config is a startup error, not a hidden fallback.
- Interactive harness sessions own one scope-scoped tool-runtime identity
  for the conversation and erase its credential overlay on clear, scope
  switch, or bot shutdown. They carry the host's live runtime resolver on
  every turn so provider withdrawal cannot reopen canonical storage directly.
- Harness and direct ModelClient continuity bind the public bot identity, chat, and scope. Credential
  rotation and bot restart preserve it; `/clear` retires disk state even before
  a replacement process has opened its first in-memory session. Reset awaits
  adapter settlement before retirement; concurrent clears share that transition,
  and incoming messages receive a wait response until the closed cached agent
  has been removed.
- Interactive sessions report scope ids for drain inspection and resolve the
  live daemon default instead of retaining the startup runtime.
- Inbound voice/audio messages route through the `transcription` module
  before reaching the session loop. The bot never calls a transcription
  vendor API directly; absence of a registered provider surfaces as an
  explicit failure, not a silent drop.
- Prefix-configured Telegram updates emit `inbound.signal.received` with
  scope identity, Telegram source metadata, and chat trust. Supported update
  kinds include text, media captions, transcribed voice/audio, edited messages,
  reactions, generic callbacks, and chat membership/status updates. True
  online presence and message deletion signals are not exposed to bots, so the
  adapter records them as unavailable rather than synthesizing events. The
  shared inbound-signals dispatcher decides source eligibility and workflow
  routing; Telegram does not decide whether a signal becomes a task, answer,
  owner question, or no-op.
- The interactive channel does not own the scheduler. The daemon owns
  it; the channel subscribes to `schedule.fire` bus events and
  broadcasts reminders to active chat sessions.
- The channel reports retry episodes through scoped module-operation health;
  HTTP telemetry remains transport diagnostics. Successful `getUpdates` clears
  the episode, including startup retries, and subsequent failures rearm reporting.
  Adapter construction, token validation and empty polls do not prove a reply.
  Deliberate cancellation is quiet; verified host suspension stays diagnostic
  instead of creating an issue. Authentication and poll ownership failures exit.

## Boundaries

- Does not own Slack or generic webhook notification (those belong in `slack/` and `webhook/`).
- Does not own inbound webhook validation for other services.
- Does not own transcription. Voice input is delegated to the
  `transcription` module's `TranscriptionProvider` boundary.
- Does not add provider-local automation planning for chat messages; configured
  updates enter the shared inbound-signals dispatcher.

Owner-question escalations share the core queue: the first resolution wins;
stale or unrelated replies fall through to the interactive session. The chat
allowlist applies to replies as it does to ordinary messages.

@verification.md

## Deployment

The operator artifact and supervisor inputs live in
`deploy/telegram-assistant/README.md`. Its entrypoint owns deployment configuration
for Docker and systemd. Keep secret-input handling and rollback proof beside that
artifact; Telegram transport behavior stays with this module. An isolated launch
with fake credentials is not evidence of a real staging chat exchange.
