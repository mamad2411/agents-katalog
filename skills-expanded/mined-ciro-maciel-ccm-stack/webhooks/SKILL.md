---
name: webhooks
description: Send and receive Standard Webhooks (x-ccm headers): signatures, replay protection, idempotency, rotation. Use for any webhook.
---

# Webhooks the standard way

Follow [Standard Webhooks](https://www.standardwebhooks.com), the same scheme large API providers use. Anyone who has integrated one of them can integrate yours without reading a special guide.

## The message

Three headers and a JSON body. CCM Stack projects use the `x-ccm` prefix; the spec's default is `webhook-`. Pick one prefix and keep it everywhere.

| Header | Value |
|---|---|
| `x-ccm-id` | Unique event id. The receiver's key against duplicates. |
| `x-ccm-timestamp` | Unix seconds when it was sent. |
| `x-ccm-signature` | `v1,<base64 HMAC-SHA256 of "{id}.{timestamp}.{body}">`. Several values separated by spaces during a secret rotation. |

Body: `{ "type": "post.published", "timestamp": "2026-11-09T12:00:00Z", "data": { ... } }`.

The secret is shown once, starts with `whsec_`, and the part after the prefix is base64.

## Sign (sender)

```js
import { createHmac } from 'node:crypto'

export function sign(secret, id, timestamp, body) {
	const key = Buffer.from(secret.replace(/^whsec_/, ''), 'base64')
	const mac = createHmac('sha256', key).update(`${id}.${timestamp}.${body}`).digest('base64')
	return `v1,${mac}`
}
```

## Verify (receiver)

```js
import { createHmac, timingSafeEqual } from 'node:crypto'

export function verify(secret, headers, rawBody, toleranceSeconds = 300) {
	const id = headers['x-ccm-id']
	const timestamp = Number(headers['x-ccm-timestamp'])
	if (!id || Math.abs(Date.now() / 1000 - timestamp) > toleranceSeconds) return false
	const key = Buffer.from(secret.replace(/^whsec_/, ''), 'base64')
	const expected = createHmac('sha256', key).update(`${id}.${timestamp}.${rawBody}`).digest()
	return (headers['x-ccm-signature'] || '').split(' ').some((part) => {
		const [version, value] = part.split(',')
		const given = Buffer.from(value || '', 'base64')
		return version === 'v1' && given.length === expected.length && timingSafeEqual(given, expected)
	})
}
```

## Rules

- **Verify the raw body**, byte for byte, before parsing JSON. Re-serialized JSON breaks the signature.
- **Refuse anything older than 5 minutes** (replay protection), and compare signatures in constant time.
- **Handle each id once.** Store processed ids; a retried event must not charge, send or create twice.
- **Answer 2xx fast** and do the work afterwards. Senders retry on timeouts, with growing delays.
- **Rotate without downtime:** sign with both secrets for a while, then drop the old one.
- **Say what each event type means** in your docs, with one real example body per type.
