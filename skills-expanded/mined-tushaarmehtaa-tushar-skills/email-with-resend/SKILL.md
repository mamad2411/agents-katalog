---
name: email-with-resend
description: Implement or audit Resend email with templates, queues, preferences, contacts, topics, broadcasts, webhooks, and delivery safety. Use when an app needs consent-aware email or Resend repair.
license: MIT
---

# Email with Resend

Implement email as a reliable, permission-aware subsystem. This is not a cold-outreach workflow.

## Workflow

1. Inspect framework/runtime, installed Resend SDK version, queues/jobs, database and user fields, auth/admin roles, existing templates, email events, consent/preferences, suppression data, webhooks, and verified-domain configuration.
2. Classify each requested message as transactional, security, lifecycle, or marketing. Do not scaffold re-engagement or campaigns by default. Ask about sender identity, jurisdiction/consent, and preference policy only when not established by the product.
3. Read [the Resend guide](references/guide.md) for send/batch/webhook patterns, sender authentication and the dated Gmail/Yahoo/Outlook sender rules, Contacts/Segments/Topics, suppression handling, unsubscribe design, and copy guidance relevant to the selected class. Facts there carry a check date; re-check any older than 90 days, or when the installed SDK differs, before relying on it. For raw API shapes, use Resend's official agent skill if installed, otherwise its docs.
4. Centralize provider calls. Detect the installed SDK API, handle both returned `error` values and thrown transport/runtime errors, use idempotency keys for event-triggered sends, and return a typed result to the caller.
5. Escape untrusted template values or use React/provider templates. Generate both HTML and useful text. Keep sender/reply-to configuration server-side and use a verified sending subdomain where appropriate. Treat SPF, DKIM, and an aligned DMARC record (`p=none` minimum) as required before any marketing or bulk volume, not as optional hardening.
6. Do not block or silently abandon the primary transaction. Use a durable outbox/queue, or a runtime-supported post-response primitive with observability when loss is acceptable. Unawaited promises are not reliable in serverless runtimes.
7. For campaigns, use Broadcasts to a Segment, scoped to a Topic for per-category opt-out, or a durable campaign job, rather than a long request loop. Do not hand-build per-category unsubscribe when Topics fit. Enforce consent, preferences, suppression, per-recipient idempotency, rate limits, cancellation, and an audit record. Require role-based admin authorization and confirmation of segment/count before send.
8. Verify Resend webhook signatures over the raw body, deduplicate events, and process bounces/complaints/delivery failures into a suppression model. Never trust an unsigned event.
9. Provide one-click unsubscribe (`List-Unsubscribe` plus `List-Unsubscribe-Post: List-Unsubscribe=One-Click`, RFC 8058) and a visible body link on marketing and subscribed mail, and stop sending within 48 hours. Do not expose raw email addresses in URLs when an opaque signed identifier can be used. Keep transactional/security opt-outs separate from marketing preferences.

## Verification

Test provider success plus returned API error, thrown network error, duplicate event, queue retry, invalid recipient, escaped user content, text rendering, verified sender/reply-to, signed/invalid/replayed webhook, bounce/complaint suppression, one-click unsubscribe `POST`, Topic opt-out, SPF/DKIM/DMARC alignment in received headers, unsubscribe/preferences, unauthorized campaign access, segment preview, and rate-limit behavior. Run repository lint/type/test/build commands and send only to designated test recipients until production setup is confirmed.

## Output

Report message classes and triggers, files/templates/jobs changed, sender and environment-variable names, consent/preferences/suppression behavior, webhook and idempotency design, verification evidence/message IDs, SPF/DKIM/DMARC status and expected daily volume against the dated sender rules, and remaining DNS/dashboard/production checks.
