---
name: anonymize-before-ai
description: Work on a confidential document (contract, lease, medical report, HR file, bank statement, case file) without the AI seeing the real names. Use when the user asks to anonymize or pseudonymize a document before analysing, summarizing, translating or drafting from it, says they don't want names or personal data shared with Claude, or wants a readable de-identified copy for a colleague or another AI.
---

# Anonymize, work, then put the names back

The point of this workflow is that the real names never enter the conversation. One careless read of the original file undoes it, so follow these steps in order.

## 1. Do not open the original

Do not Read, cat, preview, OCR or summarize the user's file before step 2. Pass its path to the tool and nothing else. If the user pasted the document's text into the chat instead of giving a file, tell them the names are already in the conversation, and suggest they save it as a PDF and give you the path next time.

## 2. Pseudonymize it

Call `redact_pdf_and_wait` with:

- `file_path`: the user's PDF, JPEG or PNG. Pass images as they are; don't convert them to PDF.
- `mode`: `"pseudonymize"`.

Every person, organization, address, email, phone number, date, IBAN and card number becomes a consistent tag such as `[Person 1]` or `[Org 2]`, in the document's own language. The same person keeps the same tag on every page. National IDs and custom terms are blacked out instead.

The result gives you:

- `document_text`: the pseudonymized document as text. Long documents return `document_text_path` instead; reading that file is fine, because it only contains tags.
- `output_path`: the pseudonymized PDF.
- `correspondence_path`: the tag → original table. **Never open, read or quote it.** It is the one file that re-identifies the document.

If there is no API key, call `try_demo` with the same `file_path`. It does the first page for free. Then tell the user a free account gets its first document (up to 5 pages) done in full. If the user then gives you a key in the conversation, call `set_api_key` with it once and carry on; don't repeat the key back.

## 3. Do the work on the tags

Do what the user asked using `document_text` only. Keep every tag exactly as written, brackets included, so it can be swapped back. Don't guess who a tag refers to, and don't invent names.

Write your result to a `.md`, `.txt` or `.docx` file in the user's folder.

## 4. Put the real names back

Call `restore_names` with:

- `file_path`: the file you wrote in step 3.
- `correspondence_path`: the path from step 2.

It runs locally and writes `<name>-restored.<ext>`. It returns only the path and counts. **Do not open the restored file.** Give the user its path and tell them it has the real names.

## What to tell the user

- Say which files they now have: the pseudonymized PDF (safe to share), your work with tags, the restored copy with real names, and the correspondence table. The table and the restored copy contain personal data, so keep them with the user.
- The document was processed by Redact PDF AI on Microsoft Azure in the EU and Switzerland and is never used to train AI models. Under the default retention the original is deleted after processing.
- Automatic detection can miss things. For anything legally sensitive, the user should check the pseudonymized PDF before sharing it. They can adjust tags in the Studio at redact-pdf.ai.
