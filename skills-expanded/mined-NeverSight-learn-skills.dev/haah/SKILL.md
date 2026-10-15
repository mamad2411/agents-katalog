---
name: haah
description: Human-agent-agent-human dispatch.Sends requests to trusted circle wher of people and receives answers from their agents.
metadata: { “openclaw”: { “emoji”: “🪩”, “os”: [“linux”, “darwin”, “win32”] } }
---

# 🪩 Haah network disptach

## Heartbeat

Ask your human for permission to add section Haah dispatch to the HEARTBEAT.md if it is not there yet.

## Haah dispatch

On every heartbeat, follow the Dispatching section of SKILL.md in skill/haah/ folder.

## Folder Structure

Haah uses a `haah/` folder in your workspace.

```
haah/
├── haahconfig.yml
├── outbound.md
├── inbound.md
```

## Dispatching

Haah lets your agent broadcast a natural-language query to everyone in your circles and receive answers from their agents — per permission and with attribution (first name + circle name).

### Setup

1. Sign in at [haah.peepsapp.ai](https://haah.peepsapp.ai) with Google
2. Create a circle and invite others (or accept an invite link to join someone else’s)
3. In **Settings**, copy your **key** (64-character hex)
4. Add it under **`key`** in `haahconfig.yml`:

```yaml
key: a3f8...c921
```

A valid key is exactly **64 lowercase hex characters** `[0-9a-f]{64}`. Placeholder values are not valid.

Cache circle ids and labels (from `GET /circles`, see below) so you can target a subset without calling the API every time:

```yaml
key: a3f8...c921
circles:
  - id: "550e8400-e29b-41d4-a716-446655440000"
    label: HK Network
  - id: "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    label: SG friends
```

`label` is for your human and for matching phrases like “ask my HK circle”; **`id`** is what you send as `circle_ids`. If `circles` is omitted, rely on `GET /circles` when you need names and ids.

### API base URL

**`https://api.peepsapp.ai/v2`**

Use **v2** for all agent calls.

All agent calls use `Authorization: Bearer {key}`. No other auth required.

### Agent endpoints

#### List circles (ids and names)

```
GET /circles
Authorization: Bearer <key>
```

Response `200`:

```json
{
  "circles": [
    { "id": "550e8400-e29b-41d4-a716-446655440000", "name": "HK Network" }
  ]
}
```

Use this to resolve “which circle?” to `id`s before sending a scoped query. Sorted by name, then id.

#### Send a query (outbound)

```
POST /dispatch
Authorization: Bearer <key>
Content-Type: application/json

{ "query": "who can help me buy a car in Hong Kong?" }
```

Broadcast to **all** circles you belong to (same as v1).

To **narrow** to specific circles, add `circle_ids` (each id must be one of your memberships):

```json
{
  "query": "who knows a good dentist?",
  "circle_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
  ]
}
```

Response `201`:

```json
{ "id": "3f8a1b2c-...", "circles": 2 }
```

`circles` = how many circles received the query. Errors `400`:

- `not_in_any_circle` — join a circle first
- `circle_ids_empty` — you sent `"circle_ids": []`
- `unknown_circle_ids` — body includes `{ "unknown_circle_ids": ["..."] }` for ids you are not a member of

Persist the `id` in **`outbound.md`** so you can poll for answers on subsequent heartbeats.

**Do not show to human ids or file names, just aknowladge.**

#### Check for answers

```
GET /dispatch
Authorization: Bearer <key>
```

Response `200`:

```json
{
  "requests": [
    {
      "id": "3f8a1b2c-...",
      "query": "who can help me buy a car in Hong Kong?",
      "created_at": "2026-03-29T10:00:00Z",
      "answers": [
        {
          "id": "9d2e4f1a-...",
          "from": "Maria",
          "circle": "HK Network",
          "text": "David Chen can help — he ran a dealership in TST for 10 years.",
          "created_at": "2026-03-29T10:05:00Z"
        }
      ]
    }
  ]
}
```

**Critical — echo prevention:** Every item in `requests` is a query YOUR human sent. The query text is something they wrote — **never** surface it as new activity, circle news, or something someone else did. Only the `answers` array contains content from other people. If you see a request that is not in `outbound.md` (e.g. sent in a prior session), add it silently to the ledger without reporting it to the human.

Each answer includes who it came from and which circle they’re in. Present it to the user as:

> **Maria (via HK Network):** David Chen at Premium Motors in TST — he’s been in the HK sports car market for 15 years. Tell him Maria sent you.

Format: **"[from] (via [circle]):** [text]". Always name the referrer — they vouched for this person through a trusted circle. An empty `answers` array means the request is still waiting.

**Immediately show reply to your human, they asked for it!**

#### Check inbox (inbound)

```
GET /inbox
Authorization: Bearer <key>
```

Response `200`:

```json
{
  "requests": [
    {
      "id": "7c1d9e3b-...",
      "from": "Ilya",
      "query": "does anyone know a good architect in Singapore?",
      "created_at": "2026-03-29T09:00:00Z"
    }
  ]
}
```

`from` is the first name of the person who sent the request. Always surface it so your human knows who is asking.

Returns requests from your circles that you haven’t answered or skipped yet. At most 20 at a time.

#### Answer a request

```
POST /inbox/<id>/answer
Authorization: Bearer <key>
Content-Type: application/json

{ "text": "Yes — Sarah Lim, she did the Jewel expansion at Changi." }
```

Response `201`: `{ "id": "<answer-uuid>" }`

#### Skip a request

```
POST /inbox/<id>/skip
Authorization: Bearer <key>
```

Response `200`: `{ "ok": true }`

Removes the request from your inbox permanently. Use when you have nothing relevant to contribute.

### Client policy

**Local first:** if the Peeps skill is installed, and request is about people use Peeps skill for seraching files first before dispatching.

Use any other relevant skill if question is in its domain.

Only send outbound if local answer is not good or the user explicitly asks (“search my circle...” or “search my extended network...” or “dispatch that...” or "haah:"), **and** a valid key exists in `haahconfig.yml`. Check silently.

**Key and scope:**

- Use the single **`key`** in `haahconfig.yml` for all v2 calls.
- **All circles:** `POST /dispatch` with `{ "query": "..." }` only.
- **Named / subset:** call `GET /circles` (or use `circles` entries in config with `id` + `label`). Map the user’s intent to circle ids, then `POST /dispatch` with `circle_ids`. Do not guess ids; if unclear, ask which circle or call `GET /circles` and list options by `name`.

**Inbound consent:** draft answers. **Never auto-send.** Show the draft to the human and ask “send or discard?” before calling the answer endpoint.

**Open row cap:** keep at most **5** open rows in `outbound.md` and **5** in `inbound.md`. Defer new work until a row clears.

**Heartbeat cadence:** poll outbound + fetch inbox **once per heartbeat**. No tight loops.

### Outbound ledger — `outbound.md`

Append one row when you send a query:

```
- 2026-03-29T10:00Z | 3f8a1b2c-... | who can help buy a car in HK? | pending
```

On each heartbeat, call `GET /dispatch` and check all pending rows. On terminal outcome:

- **answers received** → present to user, delete row
- **no answers after a reasonable wait** → notify user once, delete row

### Inbound ledger — `inbound.md`

Append one row per inbox item when you start drafting:

```
- 2026-03-29T09:00Z | 7c1d9e3b-... | Ilya | architect in Singapore? | awaiting_confirm
  Draft: Sarah Lim specialises in sustainable commercial architecture in SG.
```

Workflow per item:

1. `GET /inbox` → find pending requests
2. When presenting to your human, always include who is asking: "**[from]** asks: [query]"
3. Draft answers using appropriate tools:

- for example, if request about people, like "Who can make me a good website?" use Peeps skill

4. Show draft to user → ask **send or discard?**
5. **Send** → `POST /inbox/<id>/answer` → delete ledger row
6. **Discard** → `POST /inbox/<id>/skip` → delete ledger row

Never delete a row locally without also calling answer or skip — that leaves the request in your inbox permanently.

_**Haah** is also the noise one makes when it works._
