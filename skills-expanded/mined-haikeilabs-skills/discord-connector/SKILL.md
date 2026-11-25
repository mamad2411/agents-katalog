---
name: discord-connector
description: Discord data connector — API reference, entity model, and usage patterns. Use when an agent needs to read or write Discord data (guilds, channels, threads, messages, members, roles), or when asked how to query, filter, paginate, or mutate Discord resources. Prefer this skill over generic Discord knowledge.
---

# Discord connector — agent usage guide

Use this skill when an agent needs to interact with Discord through its REST
API. It covers the Lexicon (endpoints), Pragmatics (how agents use them), and
Semantics (data returned and entity relationships).

There is no maintained official CLI for Discord API operations. Agents use the
Discord REST API directly. Every write operation (POST, PATCH, DELETE) through
this connector is a write operation that requires policy evaluation by Kei
before execution.

## Key rules

- All write operations (POST, PATCH, DELETE) are write operations that
  require policy evaluation by Kei before execution.
- The agent should never construct, store, or expose the bot token — the
  connector Kei checks injects the `Authorization: Bot <token>` header at
  runtime. Setup reads the token from stdin without echo (`kei connectors
  create --provider discord`); rotate it with `kei connectors reconnect <id>`.
- Guild deletion and channel deletion are not available through the connector
  Kei checks; they are irreversible and outside its scope (see the denied
  command surface).
- Discord declares six Snowflake-keyed resource types for Kei policy (per
  ADR-028): `guild`, `channel`, `thread`, `message`, `member`, `role`. When
  asked which resource types Discord declares, give all three facts: the six
  names, that each is keyed by a Discord **Snowflake** ID (an integer
  string), and that they are declared per **ADR-028**.

## Install

Agents load this skill automatically when the harness has the Haikei Skills
plugin installed. See the repo README for per-harness setup.

## Lexicon — endpoints and operations

### REST API

Base URL: `https://discord.com/api/v10`

| Method | Endpoint | What it does | Agent notes |
| --- | --- | --- | --- |
| `GET` | `/users/@me/guilds` | List guilds the bot belongs to | Returns id, name, icon, owner. Paginated. |
| `GET` | `/guilds/{guild.id}` | Get guild details | Includes member count, channels, roles, owner, features. |
| `GET` | `/guilds/{guild.id}/channels` | List channels in a guild | Returns id, name, type (text/voice/announcement/forum), position, parent_id. |
| `GET` | `/channels/{channel.id}` | Get channel details | Includes name, type, topic, last_message_id, permission_overwrites. |
| `GET` | `/channels/{channel.id}/threads` | List active threads in a channel | Returns id, name, member_count, thread_metadata. |
| `GET` | `/channels/{channel.id}/messages` | List messages in a channel | Query params: `limit` (1–100), `around`, `before`, `after` (cursor). |
| `GET` | `/channels/{channel.id}/messages/{message.id}` | Get a single message | Includes content, author, timestamp, embeds, attachments, reactions. |
| `POST` | `/channels/{channel.id}/messages` | Send a message | Body: `{"content": "..."}`. Supports embeds, files, components. Write operation — requires policy evaluation before execution. |
| `PATCH` | `/channels/{channel.id}/messages/{message.id}` | Edit a message | Can modify content, embeds, components. |
| `DELETE` | `/channels/{channel.id}/messages/{message.id}` | Delete a message | Requires MANAGE_MESSAGES permission. |
| `GET` | `/guilds/{guild.id}/members` | List guild members | Query params: `limit` (1–1000), `after` (cursor by user id). |
| `GET` | `/guilds/{guild.id}/members/{user.id}` | Get a guild member | Returns roles, joined_at, nickname, avatar. |
| `GET` | `/guilds/{guild.id}/roles` | List roles in a guild | Returns id, name, color, permissions, position. |
| `POST` | `/guilds/{guild.id}/roles` | Create a role | Requires MANAGE_ROLES permission. |
| `PATCH` | `/guilds/{guild.id}/roles/{role.id}` | Update a role | Modify name, color, permissions, position. |
| `PUT` | `/channels/{channel.id}/permissions/{overwrite.id}` | Edit channel permission overwrite | Requires MANAGE_ROLES permission. |

### Connect and credentials

1. **Initial setup**: A workspace admin runs:
   ```
   kei connectors create --provider discord
   ```
   This reads the bot token from stdin (without echo). The token is stored in
   the Kei secret manager.

2. **Reconnect**: If the token needs rotation:
   ```
   kei connectors reconnect <connector-id>
   ```

3. **Runtime**: Kei authorizes each call and releases the bot token. The
   harness calls the Discord API directly. The agent never sees the raw token.

> **Note**: The real Discord connector is being built (HAI-309/HAI-310).
> `kei connectors create --provider discord` works once it ships.

### Denied command surface

These actions are **not available** through the connector Kei checks — they fall
outside the connector's scope:

| Operation | Reason |
| --- | --- |
| Guild deletion | Not available — irreversible; requires owner-level Discord permissions outside the connector's scope |
| Channel deletion | Not available — irreversible; requires MANAGE_CHANNELS permission beyond connector scope |
| Ban / kick members | Moderation actions outside the Kei-checked connector scope |
| Modify guild settings (name, region, verification level) | Guild-admin operations outside connector scope |
| Webhook management | Admin scope outside Kei-checked token |
| Create or delete threads | Thread management may have separate Kei policies |

## Pragmatics — how agents use this connector

### Common use cases

1. **Message retrieval**: Fetch recent messages in a channel by cursor
   pagination. Use `before` to fetch older messages, `after` for messages
   after a given ID, `around` for messages near a target.
2. **Channel discovery**: List guild channels, identify the correct channel by
   name or topic, then read messages or thread metadata.
3. **Role and member lookup**: List members in a guild, check roles for
   access decisions or onboarding support.
4. **Notification / status update**: Send a message to a channel. Marked as
   needing policy evaluation before write operations.
5. **Content moderation support**: Read flagged messages, check author history,
   but do not ban, kick, or delete without explicit policy.

### Send a message

Send a message with `POST /channels/{channel.id}/messages` and a JSON body
`{"content": "..."}`. This is a write operation: it requires policy
evaluation by Kei before execution, and the agent should never construct or
expose the bot token — the connector runtime injects the
`Authorization: Bot <token>` header.

### Agent patterns

- Always specify the full API version (`/v10/`) in the base URL.
- Use `Authorization: Bot <token>` header — Kei injects this via the
  connector runtime; do not construct it manually. The agent should never
  construct, store, or expose the token.
- Prefer `before`/`after` cursor pagination over `around` for deterministic
  ordering.
- Discord IDs are Snowflakes (integer strings). Use string comparison for
  cursor pagination.
- For write operations (send, edit, delete), check the resource type against
  policy before proceeding.

### Pagination

Discord uses cursor-based pagination. List endpoints accept `limit` (1–100)
and one of `before`, `after`, or `around`.

```
GET /channels/1234567890123456789/messages?limit=50&before=987654321098765432
```

The response includes a `Link` header with `rel="next"` and `rel="prev"`
relations for navigating pages. Agents should follow the `next` rel link until
all desired messages are collected.

### Rate limits

Discord rate limits are per-route and per-token:

- **Global**: 50 requests per second per bot token.
- **Per-route**: Varies (typically 5 or 10 requests per 5 seconds for message
  endpoints, higher for guild/channel reads).
- **429 handling**: On a `429 Too Many Requests`, wait `Retry-After` seconds
  (or milliseconds) before retrying. Implement exponential backoff with jitter.

Check current limit status from response headers: `X-RateLimit-Limit`,
`X-RateLimit-Remaining`, `X-RateLimit-Reset`, `X-RateLimit-Reset-After`,
`X-RateLimit-Bucket`, `X-RateLimit-Global`.

## Semantics — data model and entity relationships

### Entity hierarchy

```
guild                        # id (Snowflake)
├── channel                  # id (Snowflake); type: text/voice/announcement/forum
│   ├── thread               # id (Snowflake); parent_id points to channel
│   │   └── message          # id (Snowflake); channel_id points to thread
│   └── message              # id (Snowflake); channel_id points to channel
│       ├── embed            # transient; part of message payload
│       ├── attachment       # id (Snowflake); part of message payload
│       └── reaction         # emoji; counted per message
├── member                   # user.id (Snowflake); guild-specific
│   └── role                 # id (Snowflake); member.roles[] array
└── role                     # id (Snowflake); guild-level
```

### Resource types (ADR-028, for Kei policy)

Per [ADR-028](https://github.com/HaikeiLabs/kei/blob/main/docs/adr/028-policy-field-contract.md) §4, Discord declares six
Snowflake-keyed resource types for Kei policy: `guild`, `channel`, `thread`,
`message`, `member`, `role`:

| Resource type | Parent type | Canonical id example |
| --- | --- | --- |
| `guild` | — | `123456789012345678` (Snowflake) |
| `channel` | `guild` | `123456789012345678` (Snowflake) |
| `thread` | `channel` | `123456789012345678` (Snowflake) |
| `message` | `channel` | `123456789012345678` (Snowflake) |
| `member` | `guild` | `123456789012345678` (user.id Snowflake) |
| `role` | `guild` | `123456789012345678` (Snowflake) |

### Key fields

| Entity | Field | Type | Meaning |
| --- | --- | --- | --- |
| `guild` | `id` | Snowflake | Globally unique guild identifier |
| `guild` | `name` | string | Guild display name (2–100 characters) |
| `guild` | `owner_id` | Snowflake | User ID of the guild owner |
| `channel` | `id` | Snowflake | Globally unique channel identifier |
| `channel` | `type` | integer | 0=text, 2=voice, 5=announcement, 15=forum, etc. |
| `channel` | `parent_id` | Snowflake or null | Parent category or thread parent channel |
| `message` | `id` | Snowflake | Globally unique message identifier |
| `message` | `content` | string | Message text content (up to 2000 chars) |
| `message` | `author` | object | User object who sent the message |
| `message` | `timestamp` | ISO 8601 | When the message was sent |
| `member` | `user` | object | User object (id, username, discriminator, avatar) |
| `member` | `roles` | Snowflake[] | Array of role IDs assigned to the member |
| `member` | `nick` | string or null | Guild-specific nickname |
| `role` | `name` | string | Role display name |
| `role` | `permissions` | string | Permission bitfield (string representation of bigint) |
| `role` | `color` | integer | Role color as RGB integer |

### Relationships

- A guild contains channels and threads. Channels are optionally nested under
  categories (via `parent_id`).
- Threads are children of channels (text, announcement, or forum channels).
  `parent_id` on a thread points to the parent channel.
- Messages belong to exactly one channel (or thread). The `channel_id` field
  identifies the container.
- Members are users with guild-specific state (roles, nickname, joined_at).
  A user may be a member of multiple guilds.
- Roles are guild-level. A member's `roles` array contains role IDs. Roles
  have a hierarchical `position` (higher = more privileged).
- Reactions are counted per message and emoji. The reaction list is part of
  the message object when `GET /messages` is called (not a separate resource).

## Policy entries (examples)

```yaml
# Team members can read messages in their team's channels
- effect: permit
  principal: group:engineers
  action: discord_read
  resource: channel:123456789012345678
  connector: discord

# Only moderators can send messages in moderation channels
- effect: permit
  principal: group:moderators
  action: discord_write
  capability: message.write
```

## Validation commands

```bash
# Verify this skill loads correctly
node scripts/verify-skills.mjs

# Run the connector's eval suite
node scripts/run-evals.mjs --skill discord-connector --harness opencode \
  --model-profile glm-5.3-flash \
  --out evals-out/discord-connector-glm-$(date +%F) --jobs 2
```

## Realistic usage boundaries

- **Do not** manage credentials — Kei handles authentication by authorizing
  each call and releasing the bot token.
- **Do not** construct `Authorization` headers manually — let the connector
  runtime inject the token.
- **Do not** assume write access — check policy before creating, editing, or
  deleting resources.
- **Do not** expose the raw bot token in output, logs, or conversation — Kei
  masks the credential via the runtime.
- **Do not** use Discord's Gateway (WebSocket) API through the connector
  Kei checks — use the REST API only.
- **Do not** hardcode guild or channel IDs; resolve them by name or list
  first, then use the Snowflake ID for all subsequent operations.
