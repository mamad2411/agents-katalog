---
name: ssagent-sfdc
description: Salesforce reference for the SSA ASQ workflow. Provides validated field names, object relationships, status lifecycle, note format conventions, and reusable query patterns for ApprovalRequest__c. Auto-loaded as context for all ssagent-* skills — not user-invocable.
user-invocable: false
---

# ASQ Salesforce Reference

Validated against live Salesforce data (Mar 2026).

---

## Write Safety Rules

All ssagent skills must follow these rules for every Salesforce write:

1. **Confirm before writing.** Show the exact field(s) and value(s), then use `AskUserQuestion` with options: Approve (Recommended), Edit, Skip. Never use text-based `[A/E/S]` prompts.
2. **Append-only for long text.** `Request_Status_Notes__c` and `Additional_Notes_or_Doc_Links__c`: prepend only, never replace. `Request_Closure_Note__c`: set only during close.
3. **Dates forward only.** `End_Date__c` must not be set earlier than today.
4. **Status changes require confirmation.**
5. **Read-back after write.** After any long text update, query the field back and check for literal `\n` — warn if found.
6. **Post to Chatter based on profile `sf_update_channel`.** After writing a status note, post to Chatter if `sf_update_channel` is `chatter` or `dual`. Write to `Request_Status_Notes__c` if `sf_update_channel` is `notes` or `dual`. Default is `dual` (both channels). See the Dual-Write Pattern section below for details.

---

## Object: ApprovalRequest__c

Record type: `Account_Resource_Request` (`0123f000000GrMvAAK`), filtered by `Request_Type__c = 'Specialist SA (SSA) Request'`.

### Key Fields

| Field | Type | Notes |
|-------|------|-------|
| `Name` | Auto-number | AR-XXXXXXXXX format — use for human-readable lookup |
| `Id` | ID | Salesforce record ID — use for all updates and related queries |
| `Status__c` | Picklist | See lifecycle below |
| `Account__c` | Lookup | Account ID — use for consumption queries and related ASQ lookups |
| `Account_Name__c` | Text | Account name (denormalised) |
| `Support_Type__c` | Picklist | Type of SSA engagement |
| `Technical_Specialization__c` | Picklist | Required for routing — SSA teams filter by this field. Values: `Data Engineering`, `Data Governance`, `Data Science incl Machine Learning`, `Data Analytics incl SQL and Data Warehousing`, `Platform (incl. Cloud Security, OEM, and Cloud Integrations)`, `CyberSecurity (beta)`, `Genomics (beta)`, `Geospatial (beta)`, `SAP`, `Other` |
| `AssignmentDate__c` | Date | When ASQ was assigned to the SSA |
| `End_Date__c` | Date | Due date — extending is normal, no re-approval needed |
| `Request_Description__c` | Long Text | Original context written by requestor |
| `Submit_Comments__c` | Long Text | Additional context from submitter |
| `Request_Status_Notes__c` | Long Text | SSA work log field — prepend, never overwrite. **Also post to Chatter** for sidebar visibility |
| `Request_Closure_Note__c` | Long Text | Brief outcome summary set at completion |
| `Additional_Notes_or_Doc_Links__c` | Long Text | Doc links, supplementary notes — prepend, never overwrite |
| `Actual_Effort_in_Days__c` | Double | Actual effort expended — set at completion |
| `Approver_Comments__c` | Long Text | Manager notes during review |

### Status Lifecycle

```
New → Under Review → In Progress → Complete
                                 ↘ On Hold
          ↘ Rejected
```

- **New** — sits in SSA queue awaiting assignment
- **Under Review** — manager reviewing
- **In Progress** — assigned to SSA (OwnerId = individual user ID)
- **Complete** — set `Request_Closure_Note__c`, `Actual_Completion_Date__c`, and `Actual_Effort_in_Days__c`
- **On Hold** — paused, retains assignee

Valid SSA status values: `New`, `Under Review`, `In Progress`, `On Hold`, `Complete`

**ASQ Creation Routing Requirements:**
- `Status__c` must be `New` (not `Unassigned`) — some SSA teams only triage `New` tickets
- `OwnerId` must be the regional SSA queue (see Queue IDs below), not an individual user
- `Technical_Specialization__c` must be set — SSA teams filter incoming tickets by this field
- UCOs should be associated by the SA/Account team — managers will send back requests without one

### Note Format Convention

All SSA status notes use the format:
```
<INITIALS> YYYY-MM-DD: <note text>
```

Example: `TR 2026-02-19: Reviewed architecture with customer. Agreed on hybrid MPI pattern.`

**Always prepend** — newest entry at the top. Never delete existing content.

To build combined notes:
```python
existing = "<current Request_Status_Notes__c value>"
new_entry = "<INITIALS> <YYYY-MM-DD>: <note>"
combined = new_entry + "\n" + existing if existing.strip() else new_entry
```

---

## SSAgent Profile

All skills load the profile via `scripts/load_profile.py`, which reads `~/.ssagent/profile.yml` and merges with defaults:

```bash
LOAD_PROFILE=$(ls ~/.claude/plugins/cache/fe-vibe/fe-ssagent/*/skills/ssagent-sfdc/scripts/load_profile.py 2>/dev/null | sort -V | tail -1)

# Full profile as JSON
python3 "$LOAD_PROFILE"

# Single value by dotted key
python3 "$LOAD_PROFILE" --key sf_org
python3 "$LOAD_PROFILE" --key lookback.calendar_past_days
```

**Defaults** (applied for any missing key):

| Key | Default | Used by |
|-----|---------|---------|
| `sf_org` | *(none)* | all skills |
| `sf_user_id` | *(none)* | weekly, sfdc queries |
| `initials` | *(none)* | notes, weekly, close, researcher |
| `sf_update_channel` | `dual` | notes, weekly, close |
| `note_format.prefix` | `<INITIALS> YYYY-MM-DD` | notes, weekly, close |
| `note_format.template` | `<prefix>: <summary>. Next: <next steps>.` | notes, weekly |
| `note_format.separator` | `single` | notes, weekly, close |
| `note_location` | `local-only` | researcher |
| `asq_root` | `~/ASQ` | new-asq, researcher |
| `auto_create_dab` | `true` | new-asq |
| `default_catalog` | `users` | new-asq |
| `lookback.calendar_past_days` | `7` | notes, weekly |
| `lookback.calendar_future_days` | `14` | notes, weekly |
| `lookback.email_days` | `14` | notes, weekly |
| `custom_instructions` | *(empty)* | notes, weekly, close |
| `closure_doc` | `ask` | close |
| `closure_folder_id` | `14c9jL-k4GusjRr6kwqdUCtpXGennm-70` | close |

**Identity fields** (`sf_org`, `sf_user_id`, `initials`): Set once during `/ssagent-profile` and reused by all skills. If `None`, skills fall back to `fe-salesforce-tools:salesforce-authentication` and the User query pattern below.

---

## Object Relationships

```
ApprovalRequest__c (ASQ)
  ├── Approved_UseCase__c   (junction — rel: Approved_UseCases__r)
  │     └── Use_Case__c     → UseCase__c (UCO)
  ├── ASQ_Contact_Link__c   (rel: Resources__r)
  │     └── Resource__c     → User / Contact
  └── Account__c            → Account
```

---

## Object: UseCase__c (UCO)

| Field | Notes |
|-------|-------|
| `Stages__c` | Stage U1–U6 — **NOT** `Stage__c` |
| `Amount__c` | Total deal value |
| `MonthlyTotalDollarDBUs__c` | Monthly projected $DBU |
| `ProjectedConsumption__c` | Projected annual consumption |
| `Business_Value_Description__c` | Business outcome |
| `POCStatus__c` | Eval/POC status |
| `Competitor_Status__c` | Competitive landscape |
| `Customer_Notes__c` | Notes from customer |

---

## Queue IDs

| Queue | Group ID | Region | Use For |
|-------|----------|--------|---------|
| SSA_AMER | `00G3f000000bbidEAA` | Americas | AMER BU accounts |
| SSA_EMEA | `00G3f000000bbifEAA` | EMEA | EMEA BU accounts |
| SSA_APAC | `00G3f000000bbieEAA` | APAC | APAC BU accounts |

SSA requests must have `OwnerId` set to the correct regional queue for proper triage routing.

---

## Fuzzy ASQ Lookup

Used by `ssagent-notes` and `ssagent-close` when the user passes a customer name instead of an AR number.

### Argument Parsing

Parse `$ARGUMENTS` as follows:

- If it starts with `AR-` → **direct lookup** by AR number. Everything after the AR number (trimmed) is an optional note hint.
- Otherwise → **fuzzy lookup** by customer name. Split on the first `, ` or ` - ` to separate customer name from an optional note hint.

Examples:
| Input | Customer search | Note hint |
|-------|----------------|-----------|
| `AR-000098660` | *(skip)* | *(none)* |
| `AR-000098660 reviewed architecture` | *(skip)* | `reviewed architecture` |
| `santander, reviewed architecture` | `santander` | `reviewed architecture` |
| `sta lucia seguros - running tests` | `sta lucia seguros` | `running tests` |
| `santander` | `santander` | *(none)* |

### Fuzzy Lookup Steps

**1. Fetch all open ASQs owned by the logged-in user:**
```bash
sf data query --query "SELECT Id, Name, Account_Name__c, Status__c, End_Date__c FROM ApprovalRequest__c WHERE OwnerId = '<USER_SFDC_ID>' AND Status__c IN ('In Progress', 'Under Review', 'On Hold') AND Request_Type__c = 'Specialist SA (SSA) Request' ORDER BY AssignmentDate__c DESC" --target-org <SF_ORG_USERNAME> --json
```

**2. Match against the customer name fragment** (case-insensitive substring):
```python
query = "<CUSTOMER_NAME_FRAGMENT>".lower()
matches = [r for r in records if query in r['Account_Name__c'].lower()]
```

**3. Handle results — use `AskUserQuestion`:**
- **One match** → confirm via `AskUserQuestion`: "Found AR-XXXXXXXXX — [Account Name] — [Status] — due [End_Date]. Is this the right ASQ?" Options: Yes (Recommended), No.
- **Multiple matches** → present as `AskUserQuestion` options, each labeled `AR-XXXXXXXXX — [Account Name] — [Status]`. User picks one.
- **No matches** → tell the user and show the full open ASQ list so they can choose manually.

**Always confirm the ASQ with the user before writing anything to Salesforce.**

---

## Reusable Query Patterns

**Find all open ASQs for the logged-in user:**
```bash
sf data query --query "SELECT Name, Status__c, Account_Name__c, Support_Type__c, AssignmentDate__c, End_Date__c, Request_Status_Notes__c FROM ApprovalRequest__c WHERE OwnerId = '<USER_ID>' AND Status__c IN ('In Progress', 'Under Review', 'On Hold') AND Request_Type__c = 'Specialist SA (SSA) Request' ORDER BY AssignmentDate__c DESC" --target-org <SF_ORG_USERNAME> --json
```

**Get the logged-in user's ID and initials:**
```bash
sf data query --query "SELECT Id, FirstName, LastName FROM User WHERE Username = '<SF_ORG_USERNAME>'" --target-org <SF_ORG_USERNAME> --json
```

**Fetch a single ASQ by AR number:**
```bash
sf data query --query "SELECT Id, Name, Status__c, Account_Name__c, Account__c, Support_Type__c, AssignmentDate__c, End_Date__c, Request_Description__c, Submit_Comments__c, Request_Status_Notes__c, Request_Closure_Note__c, Additional_Notes_or_Doc_Links__c FROM ApprovalRequest__c WHERE Name = '<AR-XXXXXXXXX>'" --target-org <SF_ORG_USERNAME> --json
```

## User Lookup by Name

**Single-word input** — broad OR across first/last:
```sql
SELECT Id, Name, FirstName, LastName, Username
FROM User
WHERE (FirstName LIKE '%<word>%' OR LastName LIKE '%<word>%')
  AND IsActive = true
LIMIT 10
```

**Two-word input** — directed first + last:
```sql
SELECT Id, Name, FirstName, LastName, Username
FROM User
WHERE FirstName LIKE '<word1>%' AND LastName LIKE '<word2>%'
  AND IsActive = true
LIMIT 10
```
If zero results, retry with words swapped. If still zero, fall back to the single-word OR search.

`LIKE` is case-insensitive for standard fields but cannot handle transpositions (e.g., "Jonh" won't match "John") — truncated prefixes are more resilient.

**Resolution — use `AskUserQuestion`:**
- **1 match** → confirm: "Found [Name] ([Username]). Is this the right person?" Options: Yes (Recommended), No.
- **2–4 matches** → present as options, each labeled `Name (Username)`. User picks one.
- **>4 matches** → too broad, ask user to be more specific.
- **0 matches** → suggest checking spelling or trying a shorter prefix.

Once resolved, use the returned `Id` as `OwnerId` in the open-ASQ query pattern above.

---

## Chatter — Primary Visibility Channel

Status updates must be posted as **Chatter FeedItems** so they appear in the ASQ record's right sidebar alongside the rest of the team's activity. Writing only to `Request_Status_Notes__c` leaves updates invisible to collaborators browsing the record.

**Post a Chatter update using sf_update.py:**
```bash
python3 "$SF_UPDATE" chatter \
  --record-id "<SFDC_ID>" \
  --text "<NOTE TEXT>" \
  --org "<SF_ORG_USERNAME>"
```

**Read Chatter feed on an ASQ:**
```bash
sf api request rest "/services/data/v66.0/chatter/feeds/record/<SFDC_ID>/feed-elements" \
  --target-org <SF_ORG_USERNAME> --json
```

**Conditional write pattern:** All ssagent skills check the profile's `sf_update_channel` setting to decide where to write:
- `chatter` — post to Chatter only (via `sf_update.py chatter`)
- `notes` — write to `Request_Status_Notes__c` only (via `sf_update.py prepend`)
- `dual` (default) — write to both channels using the same note text

The `sf_update_channel` is auto-detected during `/ssagent-profile` setup by analysing the user's historical Chatter and notes field usage via `detect_sf_update_channel.py`.

---

## sf_update.py — Safe Write Script

All Salesforce writes use `scripts/sf_update.py` instead of inline Python heredocs. The script handles double-quote wrapping, smart-quote substitution, newline preservation, and automatic read-back verification.

**Resolve the script path:**
```bash
SF_UPDATE=$(ls ~/.claude/plugins/cache/fe-vibe/fe-ssagent/*/skills/ssagent-sfdc/scripts/sf_update.py 2>/dev/null | sort -V | tail -1)
```

**Prepend a note:**
```bash
python3 "$SF_UPDATE" prepend \
  --record-id "<SFDC_ID>" \
  --field "Request_Status_Notes__c" \
  --new-text "<APPROVED NOTE>" \
  --existing "<CURRENT Request_Status_Notes__c>" \
  --org "<SF_ORG_USERNAME>" \
  --separator "<single|double>"
```

**Close an ASQ:**
```bash
python3 "$SF_UPDATE" close \
  --record-id "<SFDC_ID>" \
  --closure-note "<CLOSURE_NOTE>" \
  --final-note "<INITIALS> YYYY-MM-DD: Closing. <outcome>." \
  --existing-notes "<CURRENT Request_Status_Notes__c>" \
  --effort-days <N> \
  --org "<SF_ORG_USERNAME>" \
  --separator "<single|double>"
```

**Post to Chatter:**
```bash
python3 "$SF_UPDATE" chatter \
  --record-id "<SFDC_ID>" \
  --text "<APPROVED NOTE>" \
  --org "<SF_ORG_USERNAME>"
```

**Verify a field (standalone):**
```bash
python3 "$SF_UPDATE" verify \
  --record-id "<SFDC_ID>" \
  --field "Request_Status_Notes__c" \
  --org "<SF_ORG_USERNAME>"
```

### Newline Safety

The script enforces these rules internally — skills do not need to handle them:
- Values passed via `subprocess.run()` list args (never `shell=True`)
- Wrapped in `"..."` for the sf CLI parser
- `json.dumps()` is **never** used on values (would convert `\n` to literal `\\n`)
- Inner `"` replaced with smart quotes (`\u201c`)
- Read-back verification runs automatically after every write
- `--separator single` (default) joins notes with `\n`; `--separator double` uses `\n\n` (blank line)

### Validated (live-tested 2026-02-20)

26/27 tests pass against live Salesforce (AR-000110874). Confirmed safe: ASCII, colons, quotes, backslashes, HTML/SQL-like content, all bracket types, shell metacharacters, equals signs, Unicode (accents, CJK, emoji), tabs, 5000-char strings, prepend stacking, embedded newlines, and the close workflow. Full test matrix in `scripts/test_sf_update.py`.

### Known Limitations

- **Whitespace-only values** are nullified by Salesforce (platform behavior, not a script bug).
- **Double quotes** are replaced with smart quotes (`\u201c`) by design.
