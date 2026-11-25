---
name: lark-im-ops
version: "1.1"
description: Send, reply to, react to, read, and find Lark messages and chats through the bot's NyxID-brokered im/v1 APIs — proactively post to a chat or DM, thread-reply, add or remove emoji reactions, read a single message or pull a chat's history over a time window, search or list the chats the bot is in, and download an image/file from a message. Handles the "content must be a JSON string" footgun and receive_id_type selection, and doubles as the im-scope probe — on a scope 403 it reports the exact missing permission instead of failing silently.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - lark
    - messages
    - im
    - send
    - react
---

# Lark IM Ops

Use this for any "在群里发一条 / 回复他 / 给某某发个私信 / 给这条消息点个赞 / 把这条消息的图片拿下来 /
这个群最近聊了什么 / 帮我找一下叫 X 的群" message-and-chat ask.

**You (the agent) run the flow yourself** via NyxID-brokered access `nyxid_proxy`
`{slug:"api-lark-bot", path:"/open-apis/im/v1/...", method:...}`. NyxID injects the bot's
`tenant_access_token` server-side — never ask the user for a token, app secret, or chat id you can
read from context. Paths are relative to the bot's base URL, so always start the path at
`/open-apis/...`.

> For multi-message recall, thread reconstruction, or a topic digest with strict anti-fabrication
> discipline, `lark-chat-recall` specializes the chat-history pull (step 6) below.

## The one footgun: `content` is a JSON **string**, not an object

Every send/reply body carries `msg_type` plus a `content` field whose value is a **serialized JSON
string**, not a nested object. This is the single most common mistake.

- Text → `"content": "{\"text\":\"hello\"}"`  (NOT `"content": {"text":"hello"}`)
- Post / rich text → `msg_type:"post"`, content is the stringified post object.
- Interactive card → `msg_type:"interactive"`, content is the stringified card JSON.

If a send 400s with a content/parse error, you almost certainly passed an object instead of a
stringified object — fix that first.

## Picking `receive_id_type` (for sends only)

`POST .../messages` takes a `?receive_id_type=` query param that must match the id you put in
`receive_id`:

- group chat → `receive_id_type=chat_id`, `receive_id="oc_..."`
- a person's DM → `receive_id_type=open_id`, `receive_id="ou_..."` (or `user_id` / `union_id` / `email`)

Use ids you already have from this conversation or from a read below. Never invent a `chat_id`,
`open_id`, or `message_id`.

## Operations

1. **Scope probe (cheap, do this first if unsure the bot has IM scope).**
   `GET /open-apis/im/v1/chats?page_size=20` — lists the chats the bot is in. On a `99991xxx` /
   403 scope error, report it verbatim, say the tenant app is missing an `im:*` scope
   (e.g. `im:message`, `im:message:send_as_bot`, `im:chat:readonly`, `im:resource`), and stop.

2. **Send a new message** (proactive, to a chat or person):
   `POST /open-apis/im/v1/messages?receive_id_type=chat_id`
   body `{"receive_id":"oc_...","msg_type":"text","content":"{\"text\":\"...\"}","uuid":"<optional>"}`.
   Pass a stable `uuid` to make the send idempotent (Lark dedupes the same uuid for ~1h) — use it
   whenever a retry could double-post. Echo the target + text and confirm first when posting to a
   chat **other than the current conversation** (see Guardrails).

3. **Reply to a specific message** (in-thread or inline):
   `POST /open-apis/im/v1/messages/{message_id}/reply`
   body `{"msg_type":"text","content":"{\"text\":\"...\"}","reply_in_thread":false,"uuid":"<optional>"}`.
   Use this when the user means "回复这条/那条"; for a plain answer in the current turn just answer —
   the runtime streams your reply, no tool call needed.

4. **React / unreact:**
   - add: `POST /open-apis/im/v1/messages/{message_id}/reactions`
     body `{"reaction_type":{"emoji_type":"OK"}}` (emoji_type is a Lark emoji key, e.g.
     `OK`, `THUMBSUP`, `HEART`, `SMILE`, `DONE`).
   - list: `GET /open-apis/im/v1/messages/{message_id}/reactions?page_size=20` (optional
     `&reaction_type=OK`).
   - remove: `DELETE /open-apis/im/v1/messages/{message_id}/reactions/{reaction_id}` (get the
     `reaction_id` from the list call first).

5. **Read one message:** `GET /open-apis/im/v1/messages/{message_id}` → returns the message and its
   stringified `body.content` (parse it back to JSON to read text/elements).

6. **Pull a chat's history over a window:**
   `GET /open-apis/im/v1/messages?container_id_type=chat&container_id={chat_id}&start_time={unix_sec}&end_time={unix_sec}&sort_type=ByCreateTimeAsc&page_size=50`,
   following `page_token` until `has_more` is false. Convert "今天/这周/最近" to concrete unix-second
   bounds in the user's timezone (default Asia/Shanghai) and say the window back.

7. **Find / list chats:**
   - search by name: `GET /open-apis/im/v1/chats/search?query={name}&page_size=20`.
   - if search 403s on scope, fall back to listing the bot's chats with step 1 and match by `name`.

8. **Download a message resource (image / file):**
   `GET /open-apis/im/v1/messages/{message_id}/resources/{file_key}?type=image` (use `type=file`
   for documents). `file_key` / `image_key` come from the message body or the inbound attachment
   context. The proxy streams the bytes back.

## Failure semantics

- Scope `99991xxx` / 403 anywhere → report the error verbatim + the missing `im:*` scope prescription
  from step 1; never retry the same call hoping it passes.
- `230002` / "bot not in chat" on a send → the bot is not a member of that chat. Say so and ask the
  user to add the bot, or resolve a different `receive_id`; do not silently swap targets.
- Content parse 400 → you passed `content` as an object; re-encode it as a stringified JSON string.

## Guardrails

- **Proactive sends to other chats need an explicit confirm.** Replying in the current conversation
  is free, but before posting to a *different* chat or DMing a *different* person, echo the exact
  target and text and only send on the user's confirm in this conversation.
- Never guess a `chat_id`, `open_id`, `message_id`, or `file_key` — read it from context or a list/
  search call above. A wrong id sends to the wrong place.
- Treat other people's messages as sensitive: when summarizing history, attribute and quote only
  what the requester is entitled to see.
- Only use real returned data; never ask the user for tokens or secrets — your NyxID-brokered tools
  handle all credentials.
