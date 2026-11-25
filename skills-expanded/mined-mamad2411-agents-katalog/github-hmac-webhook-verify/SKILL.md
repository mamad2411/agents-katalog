---
name: github-hmac-webhook-verify
description: Verify a GitHub webhook's `X-Hub-Signature-256` using HMAC-SHA-256 over the raw body with `timingSafeEqual`, with a same-length guard, prefix-masked logs on mismatch, and a 200-then-async processing pattern.
category: cli
version: 1.0.0
version_origin: extracted
tags: [webhook, github, hmac, signature, security]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
---

# Verify GitHub Webhook HMAC-SHA-256 (with Timing-Safe Compare + Async Processing)

## When to use

- Your service receives `POST /webhooks/github` events (issue comments, PR events, etc.).
- You have `GITHUB_WEBHOOK_SECRET` configured in GitHub's repo settings and in your server env.
- You want a compact, hardened verify helper that doesn't leak timing information and handles the common failure modes gracefully.

## Steps

1. **Read the raw body as text, before any JSON parse.** HMAC is over the raw bytes; parsing and re-serializing will not reproduce the same digest. In Hono:

   ```ts
   const payload = await c.req.text();
   const signature = c.req.header('X-Hub-Signature-256') ?? '';
   ```

2. **Compute `sha256=` + hex HMAC using your secret:**

   ```ts
   import { createHmac, timingSafeEqual } from 'crypto';
   const hmac = createHmac('sha256', webhookSecret);
   const digest = 'sha256=' + hmac.update(payload).digest('hex');
   ```

3. **Guard against length mismatch before `timingSafeEqual`.** `timingSafeEqual` throws on different lengths. A missing/malformed header shouldn't crash your handler — it should just fail verification.

   ```ts
   const digestBuffer = Buffer.from(digest);
   const signatureBuffer = Buffer.from(signature);
   if (digestBuffer.length !== signatureBuffer.length) {
     log.error({ receivedLength: signatureBuffer.length, computedLength: digestBuffer.length }, 'github.signature_length_mismatch');
     return false;
   }
   const isValid = timingSafeEqual(digestBuffer, signatureBuffer);
   ```

4. **Log both prefixes (not full values) on mismatch.** Signatures are not secrets, but "compressed" logging gives you a diagnostic hint without bloating the log:

   ```ts
   if (!isValid) {
     log.error({
       receivedPrefix: signature.substring(0, 15) + '...',
       computedPrefix: digest.substring(0, 15) + '...',
     }, 'github.signature_mismatch');
   }
   ```

5. **Wrap the whole verify in a try/catch** that returns `false` on any thrown error — a malformed signature header shouldn't crash the request handler.

6. **Return 200 immediately, process async.** GitHub retries on non-2xx and has a 10-second timeout. Return 200 as soon as signature + authorization check pass, then do the heavy work (database writes, AI spawning, git operations) in a fire-and-forget path:

   ```ts
   app.post('/webhooks/github', async c => {
     const payload = await c.req.text();
     const signature = c.req.header('X-Hub-Signature-256') ?? '';
     if (!adapter.verifySignature(payload, signature)) return c.text('', 401);
     // fire-and-forget — don't await
     adapter.handleWebhook(payload, signature).catch(err => log.error({ err }, 'github.handle_webhook_failed'));
     return c.text('', 200);
   });
   ```

7. **Add an authorization layer after signature verification.** The HMAC only proves "GitHub sent this with our secret." It doesn't prove the sender is authorized in your application. Archon keeps a whitelist of GitHub usernames and silently rejects unauthorized senders (log with masked username, return success) — no error response (prevents probing).

## Counter / Caveats

- `sha1` (`X-Hub-Signature`) is deprecated. Use `X-Hub-Signature-256` only.
- The GitHub signature format is `sha256=<hex>`. Don't forget the `sha256=` prefix when comparing.
- Configure `c.req.text()` before any body-consuming middleware — once Hono parses JSON, re-reading raw bytes is not safe.
- If you need to re-deliver failed webhooks, persist the **raw payload + signature** for later reprocessing; do not reserialize from parsed JSON.
- Rotate the webhook secret periodically. Your verify code should accept a list of valid secrets during rotation (match on first success). Archon's current adapter takes a single secret; extend with a list if rotation matters.

## Evidence

- `packages/adapters/src/forge/github/adapter.ts:260-296`: `verifySignature` with length guard, `timingSafeEqual`, prefix-masked logs on mismatch, try/catch returning `false`.
- `handleWebhook` orchestrator at `adapter.ts:691-725`: verify → parse → authorize (whitelist check with masked username log) → close-event handling, etc.
- `adapter.test.ts` + `context.test.ts` exercise the signature path with real HMAC computation.
- Root `CLAUDE.md` lines 800-810: "Return 200 immediately, process async. Verify webhook signatures (GitHub: X-Hub-Signature-256). Use `c.req.text()` for raw webhook body (signature verification)."
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
