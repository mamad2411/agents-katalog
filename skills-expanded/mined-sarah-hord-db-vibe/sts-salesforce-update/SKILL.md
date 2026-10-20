---
name: sts-salesforce-update
description: "Research and update ASQ (Account Specialist Request) tickets in Salesforce. Gathers context from Slack, Gmail, and Google Drive, then applies field updates."
user-invocable: true
---

# STS Salesforce Update Skill

Research and update ASQ (Account Specialist Request) tickets in Salesforce. Automates gathering context from Slack, email, and docs, then updating ASQ fields.

> **IMPORTANT:** This skill is for **updating** existing ASQs. To **create** a new ASQ, use `/salesforce-actions`.

## How to Invoke

```
/sts-salesforce-update
```

### Example Prompts
- "Update ASQ-00012345 with my latest engagement hours"
- "Help me update the ASQ for Acme Corp"
- "Find and update the open ASQ for Block Inc"

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Salesforce Auth | Run `/salesforce-authentication` first |
| Google Auth | Run `/google-auth` for Gmail/Drive research (optional but recommended) |

## Related Skills
- `/salesforce-actions` - Salesforce CLI patterns, ApprovalRequest object reference, `--target-org` setup
- `/gmail` - Gmail API search/read patterns, auth module, helper scripts

---

## Workflow

### Step 1: Locate the ASQ

Use `/salesforce-actions` patterns to query `ApprovalRequest__c`. The ASQ-specific queries are:

**By ASQ name:** `WHERE Name = '<ASQ_NAME>'`

**By account name (open tickets only):**
```sql
SELECT Id, Name, Status__c, Account__r.Name, Request_Description__c,
  Support_Type__c, Resource__r.Name, Hours_Consumed__c, Start_Date__c, End_Date__c
FROM ApprovalRequest__c
WHERE Account__r.Name LIKE '%<ACCOUNT_NAME>%'
  AND Status__c NOT IN ('Complete', 'Delivered', 'Rejected')
ORDER BY LastModifiedDate DESC LIMIT 10
```

**By current user (my ASQs):**
```sql
WHERE (Resource__r.Email = '<USER_EMAIL>' OR Requestor__r.Email = '<USER_EMAIL>')
  AND Status__c NOT IN ('Complete', 'Delivered', 'Rejected')
```

If multiple results, present a summary table and ask which ASQ to update.

### Step 2: Read Full ASQ Details

Query all relevant fields for the selected ASQ record:

```sql
SELECT Id, Name, Status__c, Request_Type__c, Account__r.Name,
  Requestor__r.Name, Resource__r.Name, Resource__c,
  Request_Description__c, Situation_Details__c, Additional_Comments__c,
  Support_Type__c, Urgency__c, Activity_Type__c,
  Start_Date__c, End_Date__c, Approved_Start_Date__c, Approved_End_Date__c,
  Total_Hours__c, Hours_Consumed__c, Remaining_Hours_of_Investment__c,
  Actual_Effort_in_Days__c, Actual_Completion_Date__c, BVA_Complete_Date__c,
  JIRA_link__c, LastModifiedDate, LastModifiedBy.Name
FROM ApprovalRequest__c WHERE Id = '<ASQ_ID>'
```

Present current state in a readable table.

### Step 3: Research Context

Gather context from **Slack**, **Gmail**, and **Google Drive** to build a complete picture of recent engagement.

#### 3a: Slack

Search Slack for messages about the account using the Slack MCP tools:

```
search.messages with query: "<COMPANY_NAME>"
```

Also look for dedicated internal channels (e.g., `internal-<company>`, `ext-<company>`) using:
```
conversations.list with types: "public_channel,private_channel"
```
Then fetch recent history from any matching channels. Slack often has the most up-to-date context on ongoing engagements, action items, and internal discussions.

#### 3b: Gmail

Use `/gmail` skill patterns to search for recent communications about the account:

| Query | Purpose |
|-------|---------|
| `<COMPANY_NAME> newer_than:30d` | Recent emails about the account |
| `subject:<COMPANY_NAME> newer_than:30d` | Emails with company in subject |
| `from:@<COMPANY_DOMAIN> newer_than:30d` | Emails from the customer |
| `<COMPANY_NAME> ASQ newer_than:60d` | ASQ-specific communications |

Also extract keywords from `Request_Description__c` to refine searches.

#### 3c: Google Drive

Search Google Drive for related documents (use Drive API via `/gmail` auth patterns). In particular, look for **Gemini automated meeting recordings** from Google Meet — these contain transcripts and summaries of customer calls and are a valuable source of context.

#### Summarize findings

List top 3-5 relevant Slack messages/threads, emails (date, subject, key takeaway), meeting recordings/transcripts, and other Drive docs found.

### Step 4: Compose Updates

Update the following three sections in the Salesforce ASQ page, unless the user explicitly asks to only update a particular section:

#### Request Status Notes
- These are notes taken on a per-day basis every time there is a relevant interaction with the customer related to the account.
- They must follow this structure: `Internal Sync [✅] | CAST [✅] | First Session [✅]`
- There should be a very short note for each day stating the date and the relevant update.
- Example:

```
Internal Sync [✅] | CAST [✅] | First Session [✅]

March 6th: Delivered a session on observability best practices. Covered system tables, pre-built dashboards, resource tagging, and budgets. The team will explore the observability options from Databricks and get back to us, in case additional help is required.

March 2nd: Observability session was moved to March 6th.

Feb 11th: Customer meeting scheduled for March 2nd, will review observability and optimizations in a 1 hour session.
```

#### CAST
- The CAST should be added as a standard comment in Salesforce and include the following sections.
- Keep each section **concise** — use short bullet points, not full paragraphs. Aim for 1-2 sentences or a few bullets per section. Do not repeat the request description verbatim.

  - Context 📝
  
  - Scope (or Actions) 🔭
  
  - Success Criteria 📈
  
  - Timeline ⏱️
  
  - Sessions
  
  - Action Items



#### Request Close Notes or Reject Reason
- The Salesforce field name is `Request_Closure_Note__c` (label: "Request Close Notes or Reject Reason").
- This is a separate section in Salesforce that should be filled **ONLY once there is certainty that the ASQ is fully resolved**.
- It should follow the STAR template:

```
STAR Method - Situation, Task, Action, Result
------------------------------------------------------------------------
SITUATION -
What was the context? You can summarize from the request description
------------------------------------------------------------------------

------------------------------------------------------------------------
TASK -
What was the task assigned to you? You can summarize from the scoping notes
------------------------------------------------------------------------

------------------------------------------------------------------------
ACTION -
How many and what sessions did you deliver?
------------------------------------------------------------------------

------------------------------------------------------------------------
RESULT -
What were the results of the action you took?
------------------------------------------------------------------------
```

### Step 5: Propose Updates

> **CRITICAL:** Always confirm with the user before writing. Never auto-apply.

> **CRITICAL:** Show the user every single change being proposed in Salesforce. Do not change any field other than the ones described in Step 4.

> **CRITICAL:** Present ALL drafted sections together in a single proposal. This means drafting Request Status Notes, CAST, and Close Notes (if applicable) and showing them all to the user at once before applying any changes. Do NOT apply one section while forgetting to draft another.

> **CRITICAL:** You are **FORBIDDEN** from editing, updating, or modifying ANY Salesforce fields or information other than the three sections described in Step 4 (Request Status Notes, CAST comment, and Request Close Notes). Do not change Status, Hours, Dates, or any other ASQ field under any circumstances.

### Step 6: Apply Updates

Use `sf data update record --sobject ApprovalRequest__c --record-id <ASQ_ID>` per `/salesforce-actions` patterns.

### Step 7: Verify

Re-query the ASQ and confirm updates were applied successfully.

---
## Common Issues

| Issue | Solution |
|-------|----------|
| **NoDefaultEnvError** | See `/salesforce-actions` for `--target-org` setup |
| **ASQ not found by name** | Search by account name or current user instead |
| **Cannot update formula fields** | Update `Hours_Consumed__c`, not `Total_Hours__c` |
| **Gmail auth fails** | Run `/google-auth` |
| **Restricted picklist error** | Check valid Status__c values above |
