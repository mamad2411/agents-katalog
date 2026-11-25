---
name: mailflat-inboxes
description: Create, list and delete MailFlat inboxes, and control how long their messages live. Use when an agent manages addresses for itself, for tests, or per customer.
---

# Managing inboxes

The inbox and its address are permanent: they stay until you delete them. Only the messages inside expire, on a retention window set by the plan. This is not a throwaway address service.

## Open and clean up

```python
inbox.delete()                        # inbox and every message, immediately

# or leave it: messages expire on their own at the retention you asked for
inbox = mf.create(label="ci", retention_hours=2)
```

```javascript
await inbox.delete();                  // inbox and every message, immediately

// or leave it: messages expire on their own at the retention you asked for
const inbox = await mf.create({ label: "ci", retentionHours: 2 });
```

## Endpoints

| Endpoint | What it does | Returns |
| --- | --- | --- |
| POST /api/v1/inboxes | Open an inbox | { ok, address, api_key, retention_hours } |
| GET /api/v1/inboxes | Every inbox this key opened | { ok, inboxes: [...] } |
| GET /api/v1/inboxes/{address}/latest | Newest message, the polling call | { ok, email: {...} \| null } |
| GET /api/v1/inboxes/{address}/messages | Every message, newest first | { ok, emails: [...] } |
| POST /api/v1/inboxes/{address}/send | Send from this address | { ok } |
| DELETE /api/v1/inboxes/{address} | Drop the inbox and its mail | { ok } |
| DELETE /api/v1/inboxes/{address}/messages/{id} | Drop one message | { ok } |

## Core rules

- Every call to `https://mailflat.net/api/v1` carries `X-API-Key: mf_live_...`. Keep the key in an environment variable, never in the repo.
- `prefix` decides the address. `label` is a display name and never reaches the local part.
- `retention_hours` is a ceiling set by the plan; asking for more than the plan allows is clamped, not refused.
- Anything after a `+` in the local part is a tag: `shop+promo@...` lands in the `shop` inbox and stays filterable.
- Delete in teardown so the list stays readable, and set `retention_hours` so a crashed run still cleans itself up. Use both.
- You can receive on your own domain. Connect it, verify the DNS records, then create inboxes on it.
- Inbox and domain ceilings come from the plan. Read them from `GET /api/plans`.

## API gotchas

1. **Deleting an inbox deletes its mail.** There is no archive step and no undo.
2. **Retention deletes messages, never the address.** An empty inbox is working as intended.
3. **Tags do not create inboxes.** `shop+promo@` and `shop+news@` are one inbox with two labels on the mail inside.
4. **A deleted address is not immediately reusable in every case.** Treat address reuse as a new creation, not a rename.

## References

- [Inboxes and email addresses](https://mailflat.net/docs/inboxes)
- [Plans and message retention](https://mailflat.net/docs/plans-and-retention)
- [Custom domains (BYOD): use your own domain](https://mailflat.net/docs/custom-domains)
- [Agents and Testing modes](https://mailflat.net/docs/agents-and-testing)
- [Full documentation as one file](https://mailflat.net/llms-full.txt) - every page as plain markdown
- Any documentation page also serves raw markdown: add `.md` to its URL
