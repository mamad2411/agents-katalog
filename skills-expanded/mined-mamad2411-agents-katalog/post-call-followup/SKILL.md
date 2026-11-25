---
name: post-call-followup
description: After a customer meeting, draft a follow-up email with action items and key decisions. Reads meeting notes from a Google Doc URL, pasted text, or the most recent logcall doc. Saves a Gmail draft (never auto-sends), updates Salesforce UCO next steps, and presents a clean action item table. Use when the user says "follow up", "post-call", "send recap", "meeting follow-up", or "write follow-up email".
context: fork
agent: general-purpose
model: opus
user-invocable: true
---

# Post-Call Follow-Up

Turns raw meeting notes into a professional follow-up email draft and optional Salesforce update — after every customer call.

## Rules

- **Never auto-send.** Always save as a Gmail draft. The user reviews and sends manually.
- **Output:** Show short progress labels ("Reading notes...", "Drafting email...", "Saving draft..."). No raw API responses, IDs, or tokens.
- **Interaction:** All interaction is natural language. No menus. Ask multiple fields in one message.
- **Action items are explicit.** Extract only clearly stated action items — never infer. If owner or due date is missing, leave blank.
- **Email tone:** Professional and warm. Concise — respect the customer's time. No filler phrases ("As per our discussion...").
- **Documentation links are first-party only.** When the user requests docs, only link to Databricks (`docs.databricks.com`), AWS (`docs.aws.amazon.com`), Azure (`learn.microsoft.com`), or GCP (`cloud.google.com/docs`). Never link to third-party blogs, Stack Overflow, Medium, community forums, or unofficial sources.

## Initialization

Output the splash screen:

```
post-call-followup

Paste your meeting notes, drop a Google Doc URL, or say "last" to use your most recent logcall doc.
```

## Phase 1: Get Meeting Notes

Three input modes:

### Mode A — Google Doc URL

User provides a `docs.google.com` URL. Fetch the doc content:

```bash
DOC_ID=$(echo "<URL>" | sed -n 's|.*/d/\([^/]*\).*|\1|p')
TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
curl -s "https://docs.googleapis.com/v1/documents/$DOC_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" | python3 -c "
import json, sys
doc = json.load(sys.stdin)
content = doc.get('body', {}).get('content', [])
text = []
for elem in content:
    for para in elem.get('paragraph', {}).get('elements', []):
        t = para.get('textRun', {}).get('content', '')
        if t.strip():
            text.append(t)
print(''.join(text))
"
```

Extract from the doc: customer name, date, attendees (Databricks + customer with emails), topic, notes, and any action items already written.

### Mode B — Pasted notes

User pastes raw text. Parse directly. Ask for any missing context (customer name, attendee emails) in a single follow-up.

### Mode C — "last" (most recent logcall doc)

Find the most recent logcall doc by checking the config:

```bash
cat ~/.claude/fe-meeting-notes/config.json
```

Then find the most recent meeting doc across all customer meeting-log subfolders:

**Step 1 — Find all `meeting-log` subfolders under the root:**

```bash
TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
# Get all subfolders of root
SUBFOLDERS=$(curl -s "https://www.googleapis.com/drive/v3/files?q='<root_folder_id>'+in+parents+and+mimeType='application/vnd.google-apps.folder'&fields=files(id,name)&pageSize=100&supportsAllDrives=true&includeItemsFromAllDrives=true" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng")
# For each subfolder, find meeting-log child folder
# Collect their folder IDs
```

**Step 2 — Search inside meeting-log folders for recent Google Docs, sorted by modification time:**

```bash
curl -s "https://www.googleapis.com/drive/v3/files?q='<meeting_log_folder_id>'+in+parents+and+mimeType='application/vnd.google-apps.document'&orderBy=modifiedTime+desc&pageSize=5&supportsAllDrives=true&includeItemsFromAllDrives=true&fields=files(id,name,modifiedTime,webViewLink)" \
  -H "Authorization: Bearer $TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng"
```

**Step 3 — Present the most recent docs across all customers:**

If a single clear winner (modified today), use it directly. If ambiguous, present as a numbered list:

```
Recent meeting docs:
1. 2026-02-27 — Acme Technical Review
2. 2026-02-27 — Snowflake Migration Check-in
3. 2026-02-26 — Block POC Kickoff
Which one?
```

Then fetch the selected doc's content using the same pattern as Mode A.

## Phase 2: Extract Structure

From the notes, extract:

| Field | What to look for |
|-------|-----------------|
| **Customer** | Account/company name |
| **Date** | Meeting date |
| **Topic** | Subject or purpose of the meeting |
| **Databricks attendees** | Names + emails from @databricks.com |
| **Customer attendees** | Names + emails (non-@databricks.com) |
| **Key discussion points** | 3–5 bullet summary of what was covered |
| **Decisions made** | Explicit conclusions or agreements reached |
| **Action items** | Owner, description, due date (if stated) |
| **Open questions** | Items without a clear resolution |
| **Resources promised** | Docs, links, or info the SA/AE said they'd share |

**Action item format:**

```
| Owner | Action | Due |
|-------|--------|-----|
| Calvin (DB) | Share Unity Catalog migration guide | by EOW |
| Sarah (Acme) | Confirm cluster sizing requirements | next call |
```

If no action items are found, state that clearly in the email ("No action items from this call").

## Phase 2b: Attach Documentation (Optional)

This phase triggers when:
- The user explicitly asks to "include docs", "attach documentation", "send them the docs", "add links", or similar
- The meeting notes mention resources promised to the customer (e.g., "will share the UC migration guide")
- The user says "docs" during the Phase 4 review loop (e.g., "add docs about Unity Catalog")

If none of the above apply, **skip this phase entirely**.

### How to find documentation

**Step 1 — Identify topics** from the meeting notes and action items that need documentation (e.g., "Unity Catalog migration", "cluster autoscaling", "Private Link setup").

**Step 2 — Search Databricks docs via the llms.txt index:**

```bash
curl -s "https://docs.databricks.com/llms.txt" | head -500
```

Search the output for relevant page titles and URLs matching the topics. This file contains a structured index of all Databricks documentation pages.

**Step 3 — For cloud-specific topics, fetch from first-party sources:**

| Cloud | Base URL | Example topics |
|-------|----------|---------------|
| AWS | `https://docs.aws.amazon.com/` | IAM roles, S3 policies, VPC config, PrivateLink |
| Azure | `https://learn.microsoft.com/en-us/azure/` | ADLS, Azure AD/Entra, VNet injection, Private Link |
| GCP | `https://cloud.google.com/docs/` | GCS, IAM, VPC-SC, Private Google Access |

Use WebSearch or WebFetch scoped to these domains to find the specific page URL. Verify each link resolves (200 status) before including it.

**Step 4 — Present the doc links for approval before adding to the email:**

```
Found these docs to include:
1. Unity Catalog best practices — https://docs.databricks.com/en/data-governance/unity-catalog/best-practices.html
2. Migrate from Hive metastore — https://docs.databricks.com/en/data-governance/unity-catalog/migrate.html
3. AWS PrivateLink setup — https://docs.aws.amazon.com/vpc/latest/privatelink/...

Include all, or say which to drop/add?
```

### Allowed domains (strictly enforced)

| Source | Domain(s) |
|--------|-----------|
| Databricks | `docs.databricks.com` |
| AWS | `docs.aws.amazon.com`, `repost.aws` |
| Azure | `learn.microsoft.com` |
| GCP | `cloud.google.com` |

**Never include** links from: community forums, Medium, dev.to, Stack Overflow, Towards Data Science, personal blogs, GitHub READMEs, or any other third-party source. If a relevant first-party doc cannot be found, say so — do not substitute with unofficial sources.

### How docs appear in the email

Documentation links are added to the **Resources** section of the HTML email:

```html
<p><b>Resources</b></p>
<ul>
  <li><a href="https://docs.databricks.com/en/.../migrate.html">Migrate to Unity Catalog</a> — Databricks Docs</li>
  <li><a href="https://docs.aws.amazon.com/vpc/...">Configure PrivateLink</a> — AWS Docs</li>
</ul>
```

Each link includes the doc title as anchor text and the source (Databricks Docs, AWS Docs, Azure Docs, GCP Docs) as a suffix.

## Phase 3: Draft Follow-Up Email

Generate the email as **HTML** so action items render as a proper table in Gmail. Use the `--html` flag when saving the draft (Phase 5).

**Email structure:**

```
Subject: Follow-up: <Topic> — <Date>
```

```html
<p>Hi <Customer First Names>,</p>

<p>Thanks for the time today. Here's a quick recap of what we covered and next steps.</p>

<p><b>What We Discussed</b></p>
<ul>
  <li>bullet 1</li>
  <li>bullet 2</li>
  <li>bullet 3</li>
</ul>

<p><b>Decisions</b></p>
<ul>
  <li>decision 1 (if any)</li>
</ul>

<p><b>Action Items</b></p>
<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">
  <tr style="background:#f2f2f2;"><th>Owner</th><th>Action</th><th>Due</th></tr>
  <tr><td>owner</td><td>action</td><td>due</td></tr>
</table>

<p><b>Open Questions</b></p>
<ul>
  <li>question 1 (if any)</li>
</ul>

<p><b>Resources</b></p>
<ul>
  <li><a href="URL">doc title</a> (if any)</li>
</ul>

<p>Our next step is <next meeting or action>. <CTA if relevant></p>

<p>Best,<br><SA/user first name></p>
```

Rules for the email body:
- Address customer attendees by first name
- Skip sections that are empty — omit the entire `<p><b>Section</b></p>` block (no "N/A" or "None")
- Keep list items to one line each
- "Resources" section: use `<a href="URL">title</a>` for any links found in notes
- Sign off with just the user's first name (get from `git config user.name` or Google auth profile)
- Keep HTML minimal — no external CSS, no images. Gmail strips most styling beyond inline basics

## Phase 4: Review

Present the draft to the user as a formatted markdown block. Then ask:

```
Does this look good? Say "save" to create the Gmail draft, "edit <what>" to adjust, "docs" to find and attach relevant documentation, or "skip" to exit without saving.
```

Handle edits conversationally: "change the tone to be more formal", "add a bullet about X", "shorten the recap", "add docs about Unity Catalog". If the user says "docs", run Phase 2b to find and attach documentation links. Re-present after edits.

## Phase 5: Save Gmail Draft

Once the user approves, save as a Gmail draft:

```bash
GMAIL_BUILDER=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py 2>/dev/null | sort -V | tail -1)

python3 "$GMAIL_BUILDER" create-draft \
  --to "<customer_emails_comma_separated>" \
  --cc "<databricks_attendees_except_user_comma_separated>" \
  --subject "Follow-up: <Topic> — <Date>" \
  --html "<html_body>"
```

**Important:**
- `--to` = customer attendees only
- `--cc` = other Databricks attendees (not the sender)
- If no customer emails are available, omit `--to` and tell the user to add recipients before sending

On success, output:
```
Draft saved. Open in Gmail: https://mail.google.com/mail/#drafts
```

## Phase 6: Salesforce Update (Optional)

After saving the draft, ask:

```
Update Salesforce next steps for this UCO? (say "yes", a UCO ID, or "skip")
```

If yes, use the `fe-salesforce-tools:uco-updates` skill to find the relevant UCO and prepend a next-steps entry:

```
MM/DD/YY <INITIALS> - Follow-up email sent. Action items: <comma-separated owners + actions>. Next: <next step or next meeting date>.
```

Format date as MM/DD/YY, initials from user's name.

If the user provides a UCO ID directly, update it immediately without searching.

## Path Resolution

Use glob patterns to resolve plugin cache paths. Always use `sort -V | tail -1` to get the latest installed version:

```bash
# google-auth
GOOGLE_AUTH=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1)

# gmail_builder
GMAIL_BUILDER=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py 2>/dev/null | sort -V | tail -1)
```

If a path is not found, surface a clear error: "Could not find `gmail_builder.py` — is `fe-google-tools` installed? Run `claude plugin list` to check."

## Error Handling

| Error | Response |
|-------|----------|
| Google auth fails | "Run `/google-auth` to authenticate, then retry." |
| No customer emails found | Save draft without `--to`, tell user to add recipients |
| Doc not readable | "Couldn't read that doc — check sharing permissions or paste the notes directly." |
| gmail_builder not found | "Install `fe-google-tools` first: `claude plugin marketplace add fe-google-tools`" |
| Salesforce auth fails | "Salesforce update skipped — run `/salesforce-authentication` to reconnect." |
