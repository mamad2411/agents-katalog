# poll-cf

A Slack polling bot deployed as a Cloudflare Worker. Users invoke `/poll` to create polls with a modal, then vote via buttons in channel messages. State is stored in a Durable Object backed by SQLite.

## Tech Stack

- **Runtime**: Cloudflare Workers (TypeScript)
- **State**: Durable Objects with SQLite (`ctx.storage.sql`)
- **Slack SDK**: `@slack/web-api` (posting/updating messages), `@slack/types` (type definitions)
- **Tooling**: Wrangler 4, TypeScript 5.5, Prettier

## Development

```bash
npm run dev      # local dev with Miniflare (wrangler dev)
npm run deploy   # deploy to Cloudflare
npm run cf-typegen  # regenerate worker-configuration.d.ts after wrangler.jsonc changes
```

Secrets are set via `wrangler secret put SLACK_BOT_TOKEN` and `wrangler secret put SLACK_SIGNING_SECRET`. Locally, put them in `.dev.vars`.

## Architecture

### Request Flow

```
POST / (Cloudflare Worker)
  → verify Slack HMAC-SHA256 signature
  → parse body (JSON or URL-encoded)
  → route by payload type:
      slash_command  → handleSlashCommand()   open poll creation modal
      view_submission → handleViewSubmission() create poll + post message
      block_actions   → handleBlockAction()   vote / close / duplicate / add option
      event_callback  → handleSlackEvent()    app_mention and message events
      url_verification → return challenge
```

### Key Files

| File | Purpose |
|------|---------|
| `src/index.ts` | Worker entry point, signature verification, all routing and handlers |
| `src/handlers/view-submission.ts` | Modal submission → create poll + post Slack message |
| `src/durable-objects/poll-object.ts` | Durable Object: SQLite schema, vote logic, HTTP endpoints |
| `src/views/poll-modal.ts` | Builds the poll creation/duplication modal Block Kit JSON |
| `src/views/poll-message.ts` | Builds the in-channel poll message Block Kit JSON |
| `src/helpers/buildVoteGraph.ts` | ASCII progress bar for vote counts |
| `src/helpers/rich-text.ts` | Converts Slack rich text format to markdown |
| `src/types/slack.ts` | TypeScript interfaces for all Slack payload shapes |

### Durable Object Endpoints

All routes go through `POLL_OBJECT.get(id).fetch(...)` where `id` is the `poll_id`:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/create` | Create poll record (question, options, settings) |
| POST | `/vote` | Toggle a vote; respects multi-vote setting |
| GET | `/data` | Return full poll + votes for rendering or duplication |
| POST | `/close` | Mark poll as closed |
| POST | `/update-message` | Store channel/ts for later `chat.update` calls |

### SQLite Schema

```sql
-- polls table
CREATE TABLE polls (
  id TEXT PRIMARY KEY,
  question TEXT,          -- JSON (Slack rich text blocks)
  options TEXT,           -- JSON array of option strings
  multi_vote INTEGER,     -- 0 | 1
  anonymous INTEGER,      -- 0 | 1
  closed INTEGER,         -- 0 | 1
  creator_id TEXT,
  creator_name TEXT,
  creator_avatar TEXT,
  channel TEXT,
  message_ts TEXT,
  created_at INTEGER
);

-- votes table
CREATE TABLE votes (
  poll_id TEXT,
  user_id TEXT,
  user_name TEXT,
  user_avatar TEXT,
  option_index INTEGER,
  created_at INTEGER,
  PRIMARY KEY (poll_id, user_id, option_index)
);
```

### Poll ID

Derived from Slack message metadata: `poll_id` is embedded in `metadata.event_payload.poll_id` when the message is posted, so it can be recovered from any block action on that message.

## Conventions

- **UI language**: Vietnamese (Tiếng Việt) — keep all user-facing strings in Vietnamese
- **Formatting**: Prettier with tabs, 140 char line width, single quotes (see `.prettierrc`)
- **Block Kit**: Use `@slack/types` for type safety on all Block Kit objects
- **No framework**: Raw `fetch` handler in the Worker — keep routing in `index.ts` simple and explicit
- **Error responses**: Return `new Response("error text", { status: 400/500 })` for Slack errors; Slack expects HTTP 200 for most interactive payloads even on logic errors
- **Durable Object fetch**: Always use relative URLs like `/create`, not absolute URLs

## Environment Bindings (`Env`)

```ts
interface Env {
  SLACK_BOT_TOKEN: string;
  SLACK_SIGNING_SECRET: string;
  POLL_OBJECT: DurableObjectNamespace;
}
```

## Adding Features

- **New slash command**: Add a branch in `handleSlashCommand()` in `index.ts`; open a modal with `client.views.open()`
- **New block action**: Add a case in `handleBlockAction()` matching `action.action_id`
- **New modal**: Add a new view builder in `src/views/`, return Block Kit JSON
- **New DO endpoint**: Add a route in `PollObject.fetch()` in `poll-object.ts`
- **New Slack event**: Add a case in `handleSlackEvent()` matching `event.type`
