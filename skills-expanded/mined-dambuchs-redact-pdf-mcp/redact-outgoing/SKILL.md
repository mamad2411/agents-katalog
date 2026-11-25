---
name: redact-outgoing
description: Redact personal data from PDFs, scans or screenshots in this repository before they are committed, attached to an issue, shared with a vendor or sent outside the company. Use when asked to redact, anonymize or clean a document before it leaves, or when a file under outgoing/ needs to be prepared.
allowed-tools: mcp__redact-pdf__redact_pdf_and_wait mcp__redact-pdf__restore_names
---

# Redact documents before they leave

Uses the `redact-pdf` MCP server from `.mcp.json`. Keep this file at `.claude/skills/redact-outgoing/SKILL.md` in the repository, next to `.claude/settings.json`: this skill only guides Claude, the deny rules in that file are what stop it reading the tables, the restored files and the originals under `outgoing/`.

## Never open the original

Do not Read, cat or preview the document before it is redacted. Pass its path to the tool and nothing else. The same goes for any `-correspondence.csv` and `-restored` file: they hold the real names.

## Keep the outputs out of git

The `-correspondence.csv` and `-restored` files hold the real names, and the originals are what you are protecting. They are written next to the original. Check that `.gitignore` covers them (for example `*-correspondence.csv`, `*-restored.*` and the folder that holds originals) before running `git add`.

## Redact (black boxes)

1. Call `redact_pdf_and_wait` with `file_path` set to the absolute path and `pii_categories` set to `["Person", "Email", "PhoneNumber", "Address", "Organization", "Date", "IBAN", "CreditCard"]`, unless the user asked to keep some of them.
2. Report `output_path` (the `-redacted.pdf` next to the original). If the result lists `categories_not_redacted`, tell the user those stay in the file.
3. Only the `-redacted.pdf` may be committed or sent. Remind the user that the original is unchanged.

## Work on it without seeing names

1. Call `redact_pdf_and_wait` with `mode: "pseudonymize"` and the same `pii_categories` list. If the result lists `categories_not_redacted`, stop and ask the user: names or other details would be in the text you read.
2. Work from `document_text` (or the file at `document_text_path`), keeping tags such as `[Person 1]` exactly as written.
3. Write the result to a `.md` file, then call `restore_names` with that file and `correspondence_path`. Do not pass `output_path`: the default `-restored` name is the one the deny rules cover.
4. Give the user the restored file's path. Do not open it. If `replacements` is 0, say that no tag was found and nothing was restored.
