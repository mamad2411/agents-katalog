---
description: Add a new legal source (URL or PDF path) to the loaded jurisdiction's reference set. Drops it into sources.yml and creates a stub domain file if needed.
argument-hint: "<url | pdf-path> [-- <one-line description>]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "Bash"]
---

# Legal & Compliance: Add Source

Adds a new primary source to your jurisdiction's reference set. Use when:

- The skill says "I don't have a reference for X" while answering a question
- A new law or ministerial decision was gazetted
- You're populating a non-UAE jurisdiction for the first time
- A regulator publishes an updated portal you want the skill to consult

This command does NOT auto-extract law text from the source. It registers the source and (if a domain file is missing) creates a stub. The user fills the domain file as they ask questions and the skill quotes the source.

## Procedure

1. **Verify install.** If `core/identity.md` does not exist, reply: `Founder OS not set up here. Say "set up Founder OS" first.` and stop.

2. **Parse the argument.** Expected forms:
   - `https://...` → URL source
   - `C:\path\to\file.pdf` or `/path/to/file.pdf` → local PDF
   - `<url> -- <description>` → URL with inline description

   If no argument was passed, ask: "What source do you want to add? Paste a URL, a PDF path, or both. Optionally add `-- <description>` for context."

3. **Resolve jurisdiction.** Read `core/identity.md` `jurisdiction:` field. If missing, reply: `No jurisdiction set. Say "set up legal" first.` and stop.

4. **For URL sources: WebFetch the URL** to confirm it resolves. If it returns 4xx/5xx or redirects to an unrelated page, warn the user: "URL returns <status>. Add anyway? (yes / no)". If 200, capture the page title and a one-paragraph summary for the source's `notes:` field.

5. **For PDF sources:** verify the file exists at the path given. If not, reply: "Path `<path>` does not exist. Check the path and re-run." and stop. If it exists, capture filename + size.

6. **Ask the user three classification questions** (one at a time):

   a. "Which domain(s) does this source cover? Pick one or more: company-formation, employment, tax-vat, visas-immigration, contracts-commercial, ip-trademarks, data-protection, dispute-resolution, industry-specific, federal-law-text. Comma-separated."

   b. "What's a short key for this source in `sources.yml`? Lowercase, dash-separated, e.g., `mohre`, `irs-2024-amendments`, `companies-act-2006`. (suggest one based on the URL/filename)"

   c. "One-line description for the `notes:` field? Or `skip`."

7. **Append to `sources.yml`.** Read `skills/legal-compliance/references/<jurisdiction>/sources.yml`. If it doesn't exist, ask: "No `sources.yml` exists for `<jurisdiction>`. Create the scaffold first? (yes / no)". If yes, copy `references/_template/sources.yml.template` and populate the `jurisdiction:` and `display_name:` fields, then continue.

   Append the new source under the `sources:` block:

   ```yaml
     <key>:
       name: <captured page title or PDF filename>
       url: <url or local path>
       covers: [<domain1>, <domain2>]
       last_checked_on: <today>
       notes: <description from step 6c, or page summary from step 4>
   ```

8. **Check for missing domain files.** For each domain in the source's `covers:` field, check whether `skills/legal-compliance/references/<jurisdiction>/<domain>.md` exists. If not, ask: "No `<domain>.md` file exists in this jurisdiction folder. Create a stub now? (yes / no)".

   If yes, write a stub file with this structure:

   ```markdown
   # <Display Name> <Domain Title>

   **Last Verified: <today>** (stub - populate as questions are asked)

   This file is a stub. The legal-compliance skill will quote from sources listed in `sources.yml` for the `<domain>` domain. Add law text, calculations, escalation guidance, and tables as you ask the skill questions and confirm the answers it gives.

   Sources covering this domain (from sources.yml):
   - <key>: <name> - <url>

   ## Table of Contents
   _(populate as content is added)_

   ## Escalation
   - 🟢 Green: standard / public information
   - 🟡 Amber: rule is clear but specific circumstances could change outcome - recommend professional review
   - 🔴 Red: active dispute / regulatory matter - professional counsel required
   ```

9. **Confirm.** Print:

   ```
   Source added: <key>
   Jurisdiction: <jurisdiction>
   Domains: <list>
   sources.yml: updated
   Domain stubs created: <list, or "none">

   The skill will now consult this source when answering <domain> questions.
   ```

## Rules

- Never modify a domain file's substantive content from this command. Stubs only. Substantive law goes in via skill responses the user confirms.
- Never overwrite an existing source key. If the user picks a key that exists, ask: "Key `<key>` already maps to `<existing-url>`. Replace? (yes / no)".
- Do not add the same URL twice under different keys. If the URL already exists, point to the existing key.
- Local PDFs: the path is recorded as-is in `sources.yml`. If the user later moves the PDF, the source becomes broken. Warn once: "Local paths in `sources.yml` break if the file moves. Consider hosting the PDF or storing under `references/<jurisdiction>/raw/`."
- No em dashes or en dashes.
