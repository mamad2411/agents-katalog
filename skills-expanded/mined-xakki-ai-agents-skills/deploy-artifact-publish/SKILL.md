---
name: deploy-artifact-publish
description: Set up project-specific or shared artifact publication and publish self-contained HTML with verified public readback. Use when asked to configure or publish an artifact or page.
---

# deploy-artifact-publish

Set up and use a publisher appropriate to the project and its actual infrastructure. A
publisher may be a project command, static server, object store, or other supported
backend; do not assume Make, nginx, a fixed route, or local file storage.

## Select and configure a destination

1. Inspect the current project's instructions and existing publication, domain, storage
   and deployment configuration. Reuse its supported publisher if suitable. A configured
   project publisher and public HTTPS base URL take precedence over global settings.
2. If the project has a public domain but no publisher, integrate one using its existing
   conventions and durable storage. Keep routes isolated and preserve existing behavior.
3. If it has no public domain, use the owner's configured global publisher and public
   HTTPS base URL. A URL alone is not a publisher: verify its matching write interface,
   routing, TLS, and project-specific namespace. If the global service is absent, set it
   up within the authorized infrastructure; select an unused owned name after checking
   DNS, TLS and routing. Wildcard resolution does not prove that a name is unused.
4. Resolve settings from the runtime's supported environment/configuration interface.
   On hosts that use `~/.bash_ai`, place owner-specific global settings there, without
   embedding credentials, domain names, storage paths or implementation assumptions in this
   shared skill. Existing processes may need a refreshed environment. Project settings
   override global settings; do not silently fall back when a configured project publisher
   fails. See [reference.md](reference.md) for the integration contract.

## Publish

Read the entire input before publication. Publish only self-contained HTML (inline CSS/JS,
no external hosts). Never publish impersonation, fabricated records/reviews, or deceptive
credential/payment collection. Invoke the selected publisher according to its documented
contract, using a unique project namespace and a nonconflicting slug. Read back the exact
public HTTPS URL and compare the complete response with the expected published document,
including any intentional transformation, before claiming success. Report the URL and any
incomplete verification. Publication is an external write and needs user authorization.

## Publication notifications

Follow the owner's configured Telegram routing, not a hardcoded DM or Saved
Messages destination. When `telegram-ops-notifications` is available, load it
and use its verified Gateway helper with `--kind notification`. Its notification
topic is authoritative; never fall back to a DM, General, another topic or sender.
Keep private chat IDs and credentials in that owner-local skill, not this shared
plugin. Do not read a Hermes credential store directly or create another sender.

When the user explicitly authorizes a notification to the configured recipient,
after successful public readback send one concise, quiet notification containing
the session ID, actual findings and the bare public URL on its own final line.
Resolve the helper through the active runtime's supported skill interface; if it
is unavailable, report the notification as not sent. Run its read-only
preflight and offline payload check, then send the authorized message with a
stable event ID. Verify the returned sender, chat, topic and message ID; perform
exact-message readback when the configured user connection is available.
An ACK alone is not independent readback. Preserve an uncertain send outcome;
do not resend with a new key or change the route on access/policy refusal.
Return the URL to the user even when publication succeeded but notification
verification remains incomplete, distinguishing both outcomes.

## Explicit publication smoke tests

When the owner requests an end-to-end test, use a fresh slug and a clearly labeled
standalone test report with a unique nonsecret marker. Do not overwrite an existing
report or claim Telegram delivery in the page before it has been verified.
Compare the complete public response with the authored document. If a notification
is separately authorized, send it once with the same marker and the bare report URL
as the final line. Use the owner's
notification skill for identity, routing, credentials and access checks; do not
embed private destinations or provision access in this shared skill.

Record publication/readback, notification preflight, sender ACK and independent
message readback separately. A saved Bot credential is not a successful preflight.
If preflight is refused, preserve the published URL and report notification as not
sent; do not change accounts, grants, API authorization or send paths to force the
test through. Do not republish or resend solely to turn an incomplete check green.
