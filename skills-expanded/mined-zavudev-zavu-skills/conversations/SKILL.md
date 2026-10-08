---
name: conversations
description: Read the inbox — list conversation threads, fetch their messages, mark them read, and reply from the right sender.
---

# Conversations

## When to Use

Use this skill when building anything that reads an inbox: a shared inbox UI, a helpdesk sync, a "show me this customer's history" tool, or an agent that needs the thread before it answers.

`GET /v1/messages` returns a flat log with no thread to hang it on. Conversations are the thread.

## What a conversation is

One thread with one contact, spanning every channel. A contact who writes on WhatsApp and later by email stays in the same conversation, and `channels` lists what it has carried.

| Field | Meaning |
|-------|---------|
| `id` | Thread ID. Same value as `conversationId` on messages and webhooks. |
| `contactIdentifier` | The key the thread is filed under. **Not always a phone number** — see below. |
| `contactId` | The contact, when resolved. Absent on group threads. |
| `channels` | Every channel this thread has carried. |
| `lastMessage` | Denormalized preview (`id`, `text`, `channel`, `direction`, `at`) so a thread list needs no extra fetch. |
| `senderId` | Sender that last handled the thread. Pass it back as `Zavu-Sender` when replying. |
| `unreadCount` | Inbound messages not yet marked read. |
| `whatsapp` | `bsuid` + `username`, when the contact adopted a WhatsApp username. |
| `group` | Present on group chats: `id`, `subject`, `participantCount`. |

### contactIdentifier is not a phone number

It holds whichever identifier keys the thread: an E.164 phone, a WhatsApp BSUID (`US.13491208655302741918`), a numeric chat ID (Telegram/Instagram/Messenger), or a group JID (`<id>@g.us`). Parsing it as a phone number breaks on every non-SMS channel. Use `channels` and `group` to decide how to render it.

## Endpoints

These are not in the generated SDKs yet. Use REST.

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/v1/conversations` | List threads, most recently active first. |
| `GET` | `/v1/conversations/{conversationId}` | One thread. |
| `GET` | `/v1/conversations/{conversationId}/messages` | Messages in the thread, newest first. |
| `POST` | `/v1/conversations/{conversationId}/read` | Reset `unreadCount` to zero. |

### List threads

```bash
curl "https://api.zavu.dev/v1/conversations?limit=25" \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY"
```

Filters: `senderId` scopes to one number, `channel` keeps only threads that have carried that channel.

```bash
curl "https://api.zavu.dev/v1/conversations?senderId=sender_12345&channel=whatsapp" \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY"
```

**TypeScript:**
```typescript
const res = await fetch("https://api.zavu.dev/v1/conversations?limit=25", {
  headers: { Authorization: `Bearer ${process.env.ZAVUDEV_API_KEY}` },
});
const { items, nextCursor } = await res.json();
```

### Search threads

`search` finds a thread by **who it is with**: phone number, email address, WhatsApp group subject, WhatsApp username, or BSUID. Phone formatting does not matter — `+1 (555) 123-4567` and `15551234567` both match the same thread.

```bash
curl "https://api.zavu.dev/v1/conversations?search=%2B56912345678" \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY"

# by email, by its local part, or by group name
curl "https://api.zavu.dev/v1/conversations?search=maria" \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY"
```

Matching is by whole word with prefix matching on the last term: `mar` finds `maria@example.com`, and `+1555` finds `+15551234567`. A fragment from the middle or the end of a number (`4567`) does **not** match — search the full number or a prefix.

Three things to know before you build on it:

- **It does not search message bodies.** `search` matches the thread's identity, never what was said inside it.
- **Results are ranked by relevance, not recency.** The usual "most recently active first" ordering does not apply while `search` is set.
- **An empty `search` returns nothing**, not everything. Drop the parameter to list all threads.

`search` combines with `senderId` and `channel`, and paginates with `cursor` like any other list.

```typescript
const params = new URLSearchParams({ search: "+56912345678", channel: "whatsapp" });
const res = await fetch(`https://api.zavu.dev/v1/conversations?${params}`, {
  headers: { Authorization: `Bearer ${process.env.ZAVUDEV_API_KEY}` },
});
const { items } = await res.json();
```

### Paginate

`nextCursor` is opaque. Pass it back verbatim as `cursor`; never build one by hand. `nextCursor` is `null` on the last page.

```typescript
async function allConversations() {
  const out = [];
  let cursor: string | undefined;
  do {
    const url = new URL("https://api.zavu.dev/v1/conversations");
    url.searchParams.set("limit", "100");
    if (cursor) url.searchParams.set("cursor", cursor);
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${process.env.ZAVUDEV_API_KEY}` },
    });
    const page = await res.json();
    out.push(...page.items);
    cursor = page.nextCursor ?? undefined;
  } while (cursor);
  return out;
}
```

The `channel` filter is applied to each page after it is fetched, so a filtered page can come back shorter than `limit` — even empty — while `nextCursor` is still set. Keep paginating until `nextCursor` is `null`; do not stop on a short page.

### Telling the two sides apart

Every message carries `direction` (`inbound` or `outbound`). Use it — **`status` cannot tell them apart**, because an inbound message is stored as `delivered` too. Deriving it by comparing `to` against `contactIdentifier` works for one-to-one threads and breaks on groups, where `from` is the participant rather than the thread key.

```typescript
for (const m of items) {
  const mine = m.direction === "outbound";
  console.log(`${mine ? "→" : "←"} ${m.text}`);
}
```

### Read a thread

```bash
curl "https://api.zavu.dev/v1/conversations/$CONV_ID/messages?limit=50" \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY"
```

Returns the same `Message` objects as `GET /v1/messages`, newest first, across every channel in the thread.

### Mark read

```bash
curl -X POST "https://api.zavu.dev/v1/conversations/$CONV_ID/read" \
  -H "Authorization: Bearer $ZAVUDEV_API_KEY"
```

This clears the counter in **your** inbox. It does not send a read receipt to the contact. To show a WhatsApp read receipt plus a typing indicator, use `POST /v1/messages/{messageId}/typing` on the inbound message instead.

## Replying in a thread

Send with `POST /v1/messages`, addressing the thread's identifier and passing its `senderId` as `Zavu-Sender` so the reply leaves from the number the contact already knows.

```typescript
const conv = await getConversation(conversationId);

await zavu.messages.send({
  to: conv.contactIdentifier,
  channel: conv.lastMessage.channel,
  text: "Thanks — shipping today.",
  "Zavu-Sender": conv.senderId,
});
```

The sender override is a header param inside the send params object, not a second argument.

Two constraints still apply when replying:
- **WhatsApp 24-hour window.** Outside it, free-form text is rejected with `whatsapp_window_closed`; send an approved template instead. See the `whatsapp-templates` skill.
- **Channel availability.** Reply on a channel the sender actually has. Trust `channels` on `GET /v1/senders/{senderId}`, not the presence of a phone number.

## Getting a conversation from a webhook

`message.inbound` carries `data.conversationId`. It is `null` while the thread row is still being created — the first inbound message of a brand-new thread, or several near-simultaneous first messages from an unknown address.

Recovery order:
1. Use `data.conversationId` when present.
2. Otherwise take it from the `conversation.new` event, which carries the id.
3. Otherwise `GET /v1/messages/{messageId}`, whose `conversationId` is always populated.

Do not fall back to listing conversations and matching on the phone number: on a busy project the thread may not be at the top yet, and the identifier may be a BSUID rather than the number you expected.

## Building an inbox

The API gives you threads, messages, and read state. It does not store assignment, open/done status, internal notes, or saved replies — that workspace state belongs to your app. Key it by `conversation.id`, which is stable across channels and survives WhatsApp identity re-keying (a BSUID-only thread that later gains a phone number keeps its id).

For live updates, subscribe a webhook to `message.inbound`, `message.sent`, `message.delivered`, `message.read`, `message.failed`, and `conversation.new`, then patch your local view. Polling `GET /v1/conversations` is the fallback when you cannot receive webhooks. See the `webhook-setup` skill.

## Gotchas

| Trap | Reality |
|------|---------|
| Treating `contactIdentifier` as a phone | It can be a BSUID, chat ID, or group JID. |
| Building a cursor | Cursors are opaque; only echo `nextCursor` back. |
| Stopping pagination on a short page | The `channel` filter shrinks pages. Stop on `nextCursor === null`. |
| Expecting `contactId` everywhere | Absent on group threads and unresolved contacts. |
| Expecting `/read` to notify the contact | It only clears your own counter. |
| Assuming `conversationId` is always on `message.inbound` | It is `null` on a brand-new thread. Recover it as described above. |
