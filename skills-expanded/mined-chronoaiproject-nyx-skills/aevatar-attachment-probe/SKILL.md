---
name: aevatar-attachment-probe
version: "1.0"
description: Boundary test for inbound Lark attachments — the user sends an image or file alongside this command and the bot reports exactly what it can observe on the chat path (text only, attachment refs, or nothing), without guessing. Detects when the platform wires chat-path attachment visibility so dependent skills can be upgraded.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - probe
    - attachments
    - vision
    - diagnostics
---

# Aevatar Attachment Probe

Use this to verify what the bot can see when a Lark user sends images or files. As of 2026-06-11
the documented boundary is: the relay extracts attachment refs (image_key / file_key) into the
platform envelope, but the chat LLM reply path receives TEXT ONLY; binary/file flows run on the
workflow engine path. This probe tells you whether that boundary still holds.

**You (the agent) report your actual observation honestly.** The expected outcome may be "I cannot
see the attachment" — that is a PASS, not a failure. Never invent attachment contents.

## How to run it

1. **Setup.** Ideal invocation: the user sends one message containing this command AND an image or
   file (or sends the file right before). If no attachment seems to be involved, ask them to send
   one and run the probe again on that turn.

2. **Observe the current turn.** Report exactly:
   - the text content you received, quoted;
   - whether ANYTHING attachment-like is visible to you in this turn's context: refs, keys
     (`image_key` / `file_key`), URLs, base64, structured attachment fields. List exact field names
     if present; say "nothing attachment-like visible" if not.

3. **Platform-side cross-check (optional, read-only).** If the user provides the Lark message id
   (`om_...`) of the message that carried the attachment, call `lark_messages_batch_get`
   `{message_ids:["om_..."]}` and report the message's `msg_type` and whether its content carries an
   `image_key` / `file_key`. This proves the key exists platform-side even when the chat path does
   not surface it to you — and that the bot identity can read this chat's messages.

4. **Verdict.** End with exactly one of:
   - `BOUNDARY HOLDS` — chat path is text-only as documented; attachment workloads must go through
     the workflow engine path (or ask the user for text / a link / a Base record instead).
   - `DRIFT DETECTED` — you can see attachment data in chat context. List the exact fields and
     announce that attachment-dependent skills (petty-cash, invoice-ocr, resume-screening,
     reimbursement intake) can now be upgraded to consume them.

## Guardrails

- Never claim to see image or file CONTENT on the chat path; key visibility is not content access.
- Never try to inline binary data into your reply; never fetch message resources as raw bytes.
- Only use real returned data from `lark_messages_batch_get`; quote tool errors verbatim.
- Never ask the user for tokens — your NyxID-brokered tools handle all credentials.
