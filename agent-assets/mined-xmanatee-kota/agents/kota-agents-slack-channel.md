# Slack Channel Module

This directory owns the bidirectional Slack bot channel for KOTA.

- Uses Slack Socket Mode (WebSocket) to receive messages without a public HTTP endpoint.
- Interactive input is default-deny. Messages must be direct messages from a
  configured `allowedUserIds` member in the configured `workspaceId`, and
  callbacks must match that workspace and user policy before any action runs.
  Inbound-signal actor trust is separate downstream metadata, not admission.
- One `AgentSession` per Slack user in the current default scope — free-form
  DMs resolve the live daemon default, and default changes close sessions from
  the previous scope. Durable ownership includes Slack workspace, user and scope,
  so replacement recovers context without mixing workspaces or users.
- Prefix-configured automation messages emit `inbound.signal.received` with
  scope scope, Slack source metadata, and sender trust. The shared
  inbound-signals dispatcher decides source eligibility and workflow routing;
  Slack does not decide what the signal means.
- First-class slash commands match the Telegram channel's surface
  (`/recall`, `/answer`, `/answer-log`, `/answer-show`, `/capture` plus the
  four `/capture-to-{memory,knowledge,tasks,inbox}` twins, the four
  `/retract-{memory,knowledge,tasks,inbox}` correction commands, the
  per-store semantic-search seams `/memory`, `/knowledge`, `/history`,
  `/tasks`, and the on-demand `/attention` and `/digest` seams) — one-shot
  calls that bypass the per-user session, route through the matching
  `KotaClient` namespace (or attention/digest snapshot), and reuse the
  same module-owned plain-text renderers Telegram uses, so a Slack reply
  matches the Telegram reply byte-for-byte for the same envelope.
- Semantic read commands delegate query validation, request defaults and reply
  selection to each domain's `commands.ts`, using the selected scope client.
  Channels retain parsing, admission and output limits; recall uses only its
  cross-store client seam.
- Capture and retract commands use their capability owners for empty-input
  handling, request construction and replies, with the selected scope client.
- Answer commands delegate request validation, defaults and reply text to the
  answer owner, using the selected client; Slack retains parsing and delivery.
- Slash-command parsing tolerates leading whitespace, a leading bot-mention
  prefix, and matches the command head case-insensitively.
- Approval requests are posted as plain-text Block Kit messages with the reviewed
  input, operator-safe conversation context, review digest, and Approve/Reject buttons.
- Approve button values carry the displayed digest; clicks resolve through the
  scope-scoped approvals client and fail closed when the review changed.
- Separate from `../slack/` (one-way incoming webhook notifications).

## Config

- Channel sessions use configured autonomy explicitly. Missing session-autonomy
  config is a startup error, not a hidden fallback.
- Channel-owned session ids participate in daemon scope-drain inspection.
- Keep the module-owned config shape, generated schema fragment, and focused
  startup tests aligned.
- Connection-loop health clears only after Socket Mode opens successfully;
  adapter construction alone is not recovery.

## Slack App Setup

Create a Slack App (api.slack.com/apps > Create New App > From Scratch).

Configure bot messaging scopes, enable Socket Mode with an app-level token,
subscribe to DM events, and enable interactivity. Configure `workspaceId` and
at least one `allowedUserIds` entry for interactive access. Socket Mode handles
the endpoint; install the app to the workspace and keep tokens in the shared
secret store through `$SLACK_BOT_TOKEN` and `$SLACK_APP_TOKEN` config references.

## Boundaries

- Does not own the one-way Slack webhook notification path (that lives in `../slack/`).
- Does not own the approval queue itself (`src/core/daemon/approval-queue.ts`).
- Does not add HTTP routes — all inbound traffic comes through Socket Mode WebSocket.
- Does not plan or classify chat-origin automation locally; it only normalizes
  configured updates into the shared inbound-signals dispatcher path.

## Verification ownership

Bot delivery fixtures use real sessions, module loaders and scoped stores with
controlled model and HTTP responses. Assert incoming identity, scoped delivery
and denied routing; shared session continuity journeys own restart persistence.
Do not replace AgentSession or its transports with constructor spies.

Command tests exercise the production dispatcher through its narrow client ports.
Keep Socket Mode scenarios for workspace/user admission, callback binding, session
routing and connection behavior. Result variants and plain-text domain rendering
belong to the corresponding client module; shared HTTP retries belong to
`notification`. Do not start a socket/session fixture for each command result.
