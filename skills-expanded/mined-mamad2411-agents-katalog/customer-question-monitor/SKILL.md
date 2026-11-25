---
name: customer-question-monitor
description: "Automated inbox scanning for customer questions with research-backed draft replies. Scans Gmail/Teams, researches via Glean/Slack/docs, creates Gmail drafts (never sends). Uses checkpoint dedup for scheduled runs. Use when the user says 'monitor inbox for customer questions', 'auto-scan and draft replies', or 'check for unanswered customer emails'."
user-invocable: true
---

# Customer Question Monitor

Scans Gmail and Teams for customer questions, researches answers using Glean, Slack, and public documentation, and creates Gmail draft replies for human review. **Never sends customer-facing emails — only creates drafts.** (A self-notification summary email is sent to the user when new drafts are created.)

> **How this differs from similar skills:**
> - **`fe-answer-customer-questions`** requires manual input — you paste questions, provide a Google Doc URL, or share a Slack thread. This skill **automatically scans your inbox** without manual intervention.
> - **`draft-replies-email`** scans for unanswered emails and drafts replies matching your writing style, but does **not** research answers via Glean, Slack, or documentation. This skill adds **deep product research** to produce technically accurate customer-facing replies with confidence ratings.
>
> Use `fe-answer-customer-questions` for ad-hoc question answering, `draft-replies-email` for general inbox catch-up, and this skill for **automated, research-backed customer Q&A monitoring** on a schedule.

## Quick Start

```
Monitor my inbox for customer questions and draft replies
```

```
Check for customer emails from Acme Corp and auto-draft responses
```

```
Scan my last 4 hours of email for unanswered customer questions
```

## Prerequisites

| Dependency | Required | Purpose |
|-----------|----------|---------|
| Google Auth (`google-auth` skill) | Yes | Gmail read/draft access |
| Glean MCP | Optional | Internal docs, runbooks, wikis |
| Slack MCP | Optional | Channel discussions, similar questions |
| Teams MCP | Optional | External chat messages and mentions |

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `accounts` | No | All external senders | List of account names to filter (e.g., `["Acme Corp", "Contoso"]`) |
| `checkpoint_file` | No | `~/.vibe/scripts/.qa-checkpoint.json` | Path to checkpoint JSON for dedup tracking |
| `scan_hours` | No | `4` (first run) | How far back to scan on the first run; subsequent runs use checkpoint timestamp |

## Safety Rules

> **CRITICAL — Read before running**
>
> 1. **NEVER sends customer-facing emails** — only creates Gmail drafts for customer replies
> 2. **Self-notification only** — a summary email is sent to the user (not to customers) when new drafts are created
> 3. **All drafts require human review** before sending to customers
> 4. **Checkpoint prevents duplicate processing** — each message is processed at most once
> 5. **Only processes genuine customer questions** — filters out notifications, newsletters, calendar invites, auto-replies, and other noise

## Workflow

### Step 1: Authenticate

Invoke the `google-auth` skill to obtain a valid access token with Gmail scopes (read, compose, modify).

If Glean MCP, Slack MCP, or Teams MCP are available, verify connectivity. These are optional — the workflow proceeds without them but produces richer answers when they are present.

### Step 2: Read Checkpoint

Load the checkpoint file (default `~/.vibe/scripts/.qa-checkpoint.json`). The schema:

```json
{
  "last_run": "2025-07-10T14:30:00Z",
  "processed_messages": ["msg_id_1", "msg_id_2"]
}
```

- If the file does not exist or `last_run` is null, treat this as the first run and scan the last `scan_hours` hours (default 4).
- If `last_run` is set, scan from that timestamp to now.

### Step 3: Scan Gmail

Search Gmail for messages from external senders (non-`@databricks.com`) received since `last_run`.

**Gmail search query pattern:**

```
after:{epoch_seconds} -from:databricks.com -label:sent -label:drafts
```

If `accounts` is provided, add sender filters for those domains/names.

**Filter OUT (skip these):**

- Automated notifications (DMARC, noreply, no-reply, mailer-daemon)
- Calendar invites (`.ics` attachments, "invitation" subjects)
- Newsletters and marketing (unsubscribe links, bulk headers)
- Receipts and order confirmations
- Out-of-office auto-replies (`X-Auto-Reply`, `Auto-Submitted` headers)
- Messages where the user is only CC/BCC (not direct To recipient)
- Messages already in `processed_messages`
- Messages that already have a draft reply in the same thread (secondary dedup — search Gmail drafts with `in:drafts` for the thread ID before processing)

**Keep (process these):**

- Direct questions from customers
- Issue reports and bug descriptions
- Feature requests and "how do I…" questions
- Follow-ups that need a response
- Requests for documentation or guidance

### Step 4: Scan Teams (if Teams MCP available)

Query Teams MCP for recent mentions and direct chats with external contacts since `last_run`.

Apply the same filtering rules as Gmail — skip automated messages, keep genuine questions.

### Step 5: Research Answers

For each question found in Steps 3–4, research using all available sources:

1. **Glean** (if available): Search internal docs, runbooks, wikis, and knowledge bases
2. **Slack** (if available): Search relevant channels for similar questions and PM/engineering answers
3. **Public docs**: Fetch relevant pages from `docs.databricks.com`

Compile **two versions** of each answer:

#### Customer-Facing Reply

- Professional tone, suitable for sending directly to the customer
- Reference **only public documentation** — no internal links
- Use inline hyperlinks naturally in the text (e.g., "You can configure this using [Unity Catalog](https://docs.databricks.com/...)")
- Do NOT include a "Sources" or "References" section — all links are inline
- Keep it concise and actionable

#### Internal Investigation Notes

- Full technical depth with root cause analysis
- Include Slack thread links, Glean doc links, JIRA ticket references
- Note any caveats, known issues, or workarounds not suitable for customers
- Use inline hyperlinks throughout

### Step 6: Create Gmail Draft Replies

For each processed message, create a Gmail draft:

- **Gmail questions**: Create a reply draft in the same thread (use `threadId` and `In-Reply-To` headers)
- **Teams questions**: Create a standalone Gmail draft addressed to the sender as a reminder to reply in Teams

**Draft HTML format** (use this exact structure):

```html
<div style="font-family: Arial, sans-serif; max-width: 700px;">

  <!-- Customer-Facing Reply -->
  <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 16px; margin-bottom: 16px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #2e7d32;">Customer-Facing Reply</h3>
    <p><!-- answer with inline hyperlinks, public docs only --></p>
  </div>

  <!-- Internal Notes -->
  <div style="background: #e3f2fd; border-left: 4px solid #1976d2; padding: 16px; margin-bottom: 16px; border-radius: 4px;">
    <h3 style="margin-top: 0; color: #1565c0;">Internal Investigation Notes</h3>
    <p><!-- technical depth, Slack/Glean/JIRA links --></p>
  </div>

  <!-- Confidence -->
  <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 12px; border-radius: 4px;">
    <strong>Confidence:</strong> <span style="color: #e65100;">Medium</span>
    — <em>brief justification</em>
  </div>

</div>
```

**Confidence levels:**

| Level | Meaning |
|-------|---------|
| **High** | Answer confirmed by public docs and/or PM statements |
| **Medium** | Answer supported by internal docs or Slack discussions but not fully confirmed |
| **Low** | Best-effort answer; recommend verifying with PM/engineering before sending |

### Step 7: Update Checkpoint

After all drafts are successfully created:

1. Add all newly processed message IDs to `processed_messages`
2. Set `last_run` to the current timestamp
3. Trim `processed_messages` to the most recent 200 entries to prevent file bloat
4. Write the updated checkpoint file

**Only update the checkpoint after successful draft creation** — if drafting fails for a message, leave it unprocessed so it is retried on the next run.

### Step 8: Send Summary Notification

**Skip this step entirely if zero new drafts were created.**

If new drafts were created, send a short notification email **to yourself** with a summary table:

```html
<table style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
  <thead>
    <tr style="background: #f5f5f5;">
      <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Source</th>
      <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">From</th>
      <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Subject</th>
      <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Confidence</th>
    </tr>
  </thead>
  <tbody>
    <!-- one row per draft -->
    <tr>
      <td style="padding: 8px; border: 1px solid #ddd;">
        <span style="background: #D93025; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">Gmail</span>
      </td>
      <td style="padding: 8px; border: 1px solid #ddd;">sender@example.com</td>
      <td style="padding: 8px; border: 1px solid #ddd;">Subject line</td>
      <td style="padding: 8px; border: 1px solid #ddd;">High</td>
    </tr>
  </tbody>
</table>
```

**Source badge colors:**

| Source | Color |
|--------|-------|
| Gmail | `#D93025` (red) |
| Teams | `#6264A7` (purple) |

Subject line: `[Q&A Monitor] {count} new draft replies ready for review`

## Scheduling

To run this skill automatically, use the `fe-macos-scheduler` plugin to create a recurring task:

```
Schedule "monitor customer questions" to run every 2 hours during business hours (8AM-10PM)
```

The checkpoint file ensures no duplicate processing across runs.

## Example Invocations

```
User: Monitor my inbox for customer questions and draft replies
→ Scans Gmail (and Teams if available), researches answers, creates drafts

User: Check for customer emails from Acme Corp and Contoso
→ Filters to those accounts only, creates drafts for their questions

User: Run the Q&A monitor for the last 8 hours
→ Overrides scan_hours to 8, processes all matching messages

User: Auto-draft replies to any unanswered customer questions
→ Full scan with default settings, creates drafts for review
```
