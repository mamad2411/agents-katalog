---
name: aha-workflow
description: Guided Aha! workflows - smart search from meeting notes, guided creation, contextual voting, and linking Aha ideas to UCOs as blockers. Use this skill when the user wants to link an Aha idea to a UCO, search for Aha ideas from meeting notes, or create new Aha ideas with guided workflows.
---

# Aha! Workflow

Opinionated multi-step workflows for common Aha! Ideas tasks. Builds on the `fe-internal-tools:aha-ideas` primitives with guided interactions and smart context extraction.

**Use when**: User wants a guided workflow vs direct operations

**Dependencies**: Requires `fe-internal-tools:aha-ideas` skill, `fe-salesforce-tools:uco-blockers` skill (for link-to-UCO flow)

## Workflows vs Primitives

**This skill** (`aha-workflow`):
- Guided, multi-step interactions with Q&A
- Smart topic extraction from meeting notes
- Duplicate detection and suggestion
- Contextual workflows that adapt to user needs

**Primitives** (`aha-ideas`):
- Direct operations (search, create, vote)
- Lower-level building blocks
- Fast, single-purpose commands

## Available Workflows

### 1. Smart Search from Meeting Notes

**Use when**: User has meeting notes (Google Doc or pasted text) and wants to find related Aha ideas

**What it does**:
- Extracts feature request topics from notes
- Searches for related Aha ideas
- Groups results by topic with relevance scoring
- Offers to create new ideas or vote on existing ones

### 2. Guided Idea Creation

**Use when**: User wants to create a new Aha idea with help

**What it does**:
- Helps draft clear title and description
- Checks for duplicates before creating
- Suggests product areas and categories
- Creates the idea and offers to add a proxy vote

### 3. Contextual Proxy Voting

**Use when**: User wants to add a customer vote with full context

**What it does**:
- Shows existing votes and status on the idea
- Gathers customer context (email, use case, value, deal link)
- Adds the vote with proper attribution
- Shows updated vote count

## Phase 1: Mode Selection

When the user invokes this skill, use AskUserQuestion to determine which workflow:

| Mode | Description |
|------|-------------|
| **Smart search from notes** | Extract topics from meeting notes and find related ideas |
| **Create new idea** | Guided workflow to file a feature request |
| **Add proxy vote** | Add customer endorsement with context |
| **Link to UCO as Blocker/Friction** | Link an Aha idea to a UCO as a blocker or friction item |
| **Quick search** | Just search by keyword (delegates to aha-ideas primitive) |

If the user chooses "Quick search", directly invoke `fe-internal-tools:aha-ideas` with the search operation.

## Phase 2a: Smart Search from Meeting Notes

### Step 1: Get Meeting Notes

Use AskUserQuestion to determine input method:

| Option | Description |
|--------|-------------|
| **Google Doc URL** | Read notes from a Google Doc |
| **Paste text** | Paste meeting notes directly |

**If Google Doc URL**:
- Use `fe-google-tools:google-docs` skill to read the document
- Extract the full text content

**If pasted text**:
- Ask user to paste their meeting notes
- Receive the content directly

### Step 2: Extract Topics

Analyze the meeting notes to identify feature requests and product feedback themes.

**Look for**:
- Explicit feature requests ("customer wants...", "need support for...")
- Pain points and workarounds ("struggling with...", "can't do...")
- Product gaps ("missing...", "no way to...")
- Competitive mentions ("Snowflake has...", "Redshift can...")

**Generate 3-5 search queries** that capture the key topics. Each query should be concise (2-4 words).

**Example extraction**:
```
Meeting notes: "Customer discussed their data governance needs. They need
row-level security in Unity Catalog for GDPR compliance. Also mentioned
HMS Federation not working with Streaming jobs - this is blocking their
migration. Would like better Iceberg table support."

Extracted topics:
1. "Unity Catalog row-level security"
2. "HMS Federation Streaming"
3. "Iceberg table support"
```

### Step 3: Search for Each Topic

For each extracted topic:
1. Invoke `fe-internal-tools:aha-ideas` search operation
2. Get top 3-5 results per topic
3. Deduplicate across topics (same idea may match multiple queries)

### Step 4: Present Results

Group results by the topic they matched:

```
Found 8 ideas related to your meeting notes:

## Unity Catalog row-level security
- DB-I-12345: Add row-level security to Unity Catalog (Status: Planned, 23 votes)
  https://databrickinternal.ideas.aha.io/ideas/DB-I-12345
- DB-I-12789: Fine-grained access control for Unity Catalog (Status: Investigating, 15 votes)

## HMS Federation Streaming
- DB-I-18242: Support HMS Federation with Structured Streaming (Status: Open, 8 votes)

## Iceberg table support
- DB-I-15903: Improve Iceberg REST catalog support (Status: In Progress, 31 votes)
- DB-I-16234: Iceberg table evolution support (Status: Shipped, 45 votes)
```

### Step 5: Next Actions

Use AskUserQuestion:

| Option | Description |
|--------|-------------|
| **Add proxy vote** | Vote on one of these ideas for your customer |
| **Link to UCO as blocker** | Link an idea to a UCO as a blocker or friction item |
| **Create new idea** | Topic not covered - create a new request |
| **View details** | Get full details on a specific idea |
| **Done** | Finished |

Route to the appropriate workflow based on selection. "Link to UCO as blocker" routes to Phase 2d.

## Phase 2b: Guided Idea Creation

### Step 1: Check for Duplicates First

Before creating, search for existing ideas:
1. Ask user for the feature they want to request
2. Invoke `fe-internal-tools:aha-ideas` search with keywords
3. Show top 5 results

Use AskUserQuestion:
- **"One of these matches"** → Go to proxy vote workflow
- **"None match, create new"** → Continue creation

### Step 2: Draft Title and Description

Help the user write a clear idea:

**Title guidelines**:
- Concise (< 80 chars)
- Action-oriented ("Add...", "Support...", "Enable...")
- Specific enough to be searchable

**Description guidelines**:
- What: What feature/capability is needed?
- Why: What business problem does it solve?
- Context: Customer segment, use case, or compliance driver

**Example prompts**:
```
You: "What feature do you want to request?"
User: "We need row-level security in Unity Catalog"

You: "Great! Let me help you draft this. Why do customers need this?"
User: "For GDPR and HIPAA compliance - they can't use Unity Catalog without it"

Drafted:
Title: "Add row-level security to Unity Catalog"
Description: "Customers need row-level security (RLS) in Unity Catalog for
regulatory compliance (GDPR, HIPAA). Without RLS, they cannot store sensitive
data in Unity Catalog tables, limiting adoption for healthcare and financial
services customers."
```

Show the draft and ask for approval or edits.

### Step 3: Select Product and Categories

**Product ID**: Usually "DB" for Databricks (can invoke `aha-ideas` to list products)

**Categories**: Suggest based on the description:
- Keywords → categories mapping
- Example: "Unity Catalog" → "Unity Catalog,Security"

### Step 4: Create the Idea

Invoke `fe-internal-tools:aha-ideas` create operation:
```
create_idea(
  title=<drafted_title>,
  description=<drafted_description>,
  product_id="DB",
  created_by=<user_email>,
  categories=<selected_categories>
)
```

### Step 5: Confirm and Offer Vote

Show the new idea reference and URL:
```
✓ Created: DB-I-12345
  https://databrickinternal.ideas.aha.io/ideas/DB-I-12345
```

Use AskUserQuestion:
- **"Add a proxy vote now"** → Go to proxy vote workflow for this idea
- **"Link to UCO as blocker"** → Go to Phase 2d with this idea
- **"Done"** → Finished

## Phase 2c: Contextual Proxy Voting

### Step 1: Select the Idea

If coming from another workflow (search or create), use that idea.

Otherwise:
- Ask for the idea reference (e.g., DB-I-12345)
- Or offer to search first

### Step 2: Show Context

Invoke `fe-internal-tools:aha-ideas` get-detail operation to show:
- Idea title and status
- Current vote count
- Existing proxy votes (voter names)
- Linked eng blockers (if any)

```
DB-I-12345: Add row-level security to Unity Catalog
Status: Planned
Current votes: 23

Recent proxy votes:
- Acme Corp ($500K ARR)
- Hinge Health ($250K ARR)
- ...

Linked eng blockers: 3 customers blocked ($1.2M impact)
```

### Step 3: Gather Vote Details

Ask for customer context:

**Required**:
- Customer email (for vote attribution)

**Recommended**:
- Use case description (why they need this)
- Dollar value (ARR, deal size, opportunity value)
- Salesforce link (opportunity or account URL)

**Example prompts**:
```
You: "What's the customer email for this vote?"
User: "eng-lead@acmecorp.com"

You: "Why does Acme Corp need this feature?"
User: "They can't deploy to production without RLS - compliance blocker"

You: "What's the dollar value? (ARR, deal size, or opp value)"
User: "$250K"

You: "Salesforce link? (optional)"
User: "https://databricks.lightning.force.com/lightning/r/Opportunity/006.../view"
```

### Step 4: Add the Vote

Invoke `fe-internal-tools:aha-ideas` add-proxy-vote operation:
```
add_proxy_vote(
  idea_id="DB-I-12345",
  customer_email="eng-lead@acmecorp.com",
  description="Critical for production deployment - compliance requirement",
  value=250000,
  link=<salesforce_url>,
  created_by=<user_email>
)
```

### Step 5: Confirm

Show updated vote count:
```
✓ Added vote from eng-lead@acmecorp.com
  Value: $250,000
  Updated vote count: 24 → 25
```

## Phase 2d: Link Aha Idea to UCO as Blocker/Friction

### Step 1: Select the Aha Idea

If coming from another workflow (search, create, or vote), use that idea.

Otherwise:
- Ask for the Aha reference number (e.g., DB-I-18242)
- Or offer to search first via `fe-internal-tools:aha-ideas`

### Step 2: Look Up the Aha Idea in Salesforce

The `Blocker__c.Aha_Idea__c` field requires the **Salesforce record ID** of the `ahaapp__AhaIdea__c` object, not the Aha reference number.

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')

sf data query --query "SELECT Id, Name, ahaapp__ReferenceNum__c, ahaapp__Status__c FROM ahaapp__AhaIdea__c WHERE ahaapp__ReferenceNum__c = '<REFERENCE_NUM>'" \
  --target-org "$SF_TARGET_ORG" --json
```

If not found, the idea may not be synced to Salesforce yet. Inform the user and offer to create the blocker without linking the Aha idea (it can be linked later).

### Step 3: Select UCO(s)

Use AskUserQuestion to determine the target UCO:

| Option | Description |
|--------|-------------|
| **Search by account name** | Find UCOs for a specific customer |
| **Search by UCO name** | Find a specific use case |
| **Enter UCO ID directly** | Paste a known UCO ID |

Search UCOs:
```bash
# By account name
sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c, Account__r.Name FROM UseCase__c WHERE Account__r.Name LIKE '%<ACCOUNT>%' AND Active__c = true AND Stages__c IN ('1-Validating','2-Scoping','3-Evaluating','4-Confirming','5-Onboarding') ORDER BY Account__r.Name, Stages__c" \
  --target-org "$SF_TARGET_ORG" --json

# By UCO name
sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c, Account__r.Name, Account__c FROM UseCase__c WHERE Name LIKE '%<TERM>%' AND Active__c = true" \
  --target-org "$SF_TARGET_ORG" --json
```

Present matching UCOs and let the user select one (or multiple if linking the same idea to several UCOs).

### Step 4: Choose Blocker Type

Use AskUserQuestion:

| Option | Description |
|--------|-------------|
| **Blocked** | Customer cannot adopt or move forward until this is resolved |
| **Friction** | Missing feature is slowing down the deal but not fully blocking |

### Step 5: Create the Blocker

Invoke `fe-salesforce-tools:uco-blockers` to create the `Blocker__c` record:

```bash
sf data create record --sobject Blocker__c \
  --values "Use_Case__c='<UCO_ID>' Type__c='<Blocked|Friction>' Blocker_Status__c='Open' Category__c='Product (Aha features, bugs, etc.)' Comment__c='<DESCRIPTION>' Account__c='<ACCOUNT_ID>' Aha_Idea__c='<AHA_IDEA_SF_ID>'" \
  --target-org "$SF_TARGET_ORG" --json
```

### Step 6: Optionally Update UCO Health

Use AskUserQuestion:

| Option | Description |
|--------|-------------|
| **Set UCO health to Red** | This blocker is preventing progression (recommended for "Blocked" type) |
| **Keep current health** | UCO health is already appropriately set |

If setting to Red:
```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Implementation_Status__c=Red" \
  --target-org "$SF_TARGET_ORG"
```

### Step 7: Confirm

Show a summary:
```
Blocker created successfully:

  UCO: <UCO Name> (<Account Name>)
  Type: Blocked
  Category: Product (Aha features, bugs, etc.)
  Aha Idea: DB-I-18242 - HMS Federation with Structured Streaming
  UCO Health: Updated to Red

  Blocker ID: <ID>
  View in Salesforce: https://databricks.lightning.force.com/lightning/r/Blocker__c/<ID>/view
```

## Error Handling

**Authentication errors** (from aha-ideas):
- Guide user through setup: `python3 aha_auth.py login`
- Or create API key at https://databrickinternal.aha.io/settings/api_keys

**Duplicate detection**:
- Always search before creating
- Show similarity score if possible
- Let user decide if duplicate or genuinely new

**Empty search results**:
- Suggest broader keywords
- Offer to create new idea immediately

**Invalid idea references**:
- Check format: DB-I-#####
- Offer to search by keyword instead

## Related Skills

**Dependencies**:
- `fe-internal-tools:aha-ideas` - Core operations (search, create, vote)
- `fe-salesforce-tools:uco-blockers` - Create and manage UCO blockers in Salesforce
- `fe-google-tools:google-docs` - Read meeting notes from Google Docs

**Related**:
- `fe-internal-tools:eng-blockers` - Find linked eng blockers for context
- `fe-salesforce-tools:uco-updates` - Update UCO health, stage, and next steps

## Notes

- **Workflow state**: This skill doesn't maintain state across turns - each invocation starts fresh
- **Topic extraction**: Use LLM reasoning to identify feature themes from natural language
- **Duplicate detection**: Search is fuzzy - better to surface possible duplicates than miss them
- **Vote context**: More context = better prioritization signal for PMs
