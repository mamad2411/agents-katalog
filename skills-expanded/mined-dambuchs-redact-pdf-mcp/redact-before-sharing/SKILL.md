---
name: redact-before-sharing
description: Permanently black out personal data in a PDF, scan, photo or screenshot before it is sent, filed, published or attached. Use when the user asks to redact, black out, censor or remove names, emails, phone numbers, addresses, bank details, card numbers or IDs from a document, or prepares a document for a FOIA/GDPR request, a court or agency filing, a landlord, a client or the public.
---

# Redact a document before it leaves

## 1. Run the redaction

Call `redact_pdf_and_wait` with `file_path` set to the user's PDF, JPEG or PNG. Pass photos and screenshots as they are; don't convert them to PDF first. If the user only wants to share the result and not have you read it, don't open the original either: pass the path.

Narrow it only when the user asks to:

- `pii_categories`: only these kinds of data (for example only `Person` and `Email`).
- `pii_included_terms`: extra words to always black out, such as a project code name.
- `pii_excluded_terms`: words to keep visible, such as the user's own company name.

For a folder, start one `redact_pdf` job per file, then collect each with `get_job_status` and `download_redacted`. Don't upload the same file twice. If a call times out, the job keeps running: poll `get_job_status` with the `job_id`.

If there is no API key, call `try_demo` with the same `file_path` to redact the first page for free, then tell the user a free account gets its first document (up to 5 pages) done in full. If the user then gives you a key in the conversation, call `set_api_key` with it once and carry on; don't repeat the key back.

## 2. Report back

Give the user `output_path` (by default `<name>-redacted.pdf` next to the original, which is left unchanged) and the page count.

Tell them the redacted text is deleted from the file, not hidden under a black box, so it can't be copied out or recovered. Automatic detection can still miss something, so for a filing or anything public they should look through the redacted PDF before sending it. They can add or remove boxes in the Studio at redact-pdf.ai.

If the user wants the document to stay readable, with "who did what" still clear, use the anonymize-before-ai skill instead. Black boxes lose who did what; `[Person 1]` tags keep it.
