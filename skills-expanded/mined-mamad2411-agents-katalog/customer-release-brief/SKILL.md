---
name: customer-release-brief
description: Generate a customer-specific Databricks product update brief filtered to features the customer actively uses. Use when the user says "what's new for <customer>", "product updates for <customer>", "release notes for <customer>", "what should I tell <customer> about new features", "recent Databricks updates for my customer", "prepare product update talking points", "what's changed since my last meeting with <customer>". Distinct from databricks-learning-assistant (self-education) and product-question-research (general questions).
user-invocable: true
context: fork
agent: general-purpose
model: sonnet
---

# Customer Release Brief

Generates a concise, customer-relevant product update brief showing only Databricks releases that apply to features that customer actively uses — no noise, no generic changelog.

**Announce at start:** "I'm using the customer-release-brief skill to build your personalized product update brief for [customer]."

## Differentiation

| Skill | Purpose |
|-------|---------|
| `/databricks-learning-assistant` | Internal SA education on Databricks features |
| `/product-question-research` | Answer specific product questions |
| `/account-review-deck` | Full QBR deck with product usage |
| `/customer-release-brief` (this) | Personalized update brief: what's new in what THIS customer uses |

## User Input

Parse the user's message for:

| Input | Example | How it's used |
|-------|---------|---------------|
| **Customer name** | "Acme Corp", "Octopus Energy" | Filter Salesforce + logfood to this account |
| **Time range** | "last 30 days", "since January", "last quarter" | Override default look-back (default: 30 days) |
| **Format** | "email", "Slack message", "Google Doc", "bullet points" | Control output format |
| **Specific areas** | "just Unity Catalog updates", "focus on AI/ML" | Narrow to specific product areas |
| **Last meeting date** | "since our last meeting on Feb 15" | Use as the look-back start date |

If only a customer name is provided, use defaults: 30-day look-back, markdown output for copy-paste.

## Prerequisites

Run auth checks before starting:

```bash
# Auth 1 — Logfood (product usage data)
databricks auth describe --profile logfood 2>/dev/null && echo "LOGFOOD_OK" || echo "LOGFOOD_FAIL"
```

```bash
# Auth 2 — Salesforce (UCO/account context)
sf org display 2>/dev/null && echo "SF_OK" || echo "SF_FAIL"
```

Degrade gracefully: if logfood auth fails, skip usage filtering and generate a broader brief based on UCO data only. If Salesforce fails too, ask the user to describe which Databricks products the customer uses.

## Workflow

### Phase 0: Confirm Customer + Time Range

If the customer name is missing, ask:
> "Which customer are you preparing this update brief for, and do you want a specific time range? (default: last 30 days)"

Otherwise proceed immediately.

### Phase 1: Get Customer's Databricks Product Footprint

**Goal:** Understand WHAT Databricks products the customer actively uses so we can filter release notes.

Run the usage footprint query from `resources/usage_footprint.sql`. This identifies:
- Active products/SKUs (Delta Live Tables, Model Serving, SQL Warehouse, etc.)
- Usage tier (light / moderate / heavy) per product area
- Recently adopted features (started in past 90 days)

```bash
# Get warehouse first
# Use /databricks-warehouse-selector with --profile=logfood
```

```sql
-- Parameterized: replace :account_name with actual account name
-- Use fuzzy match to handle name variations
```

Load the SQL from `resources/usage_footprint.sql` and execute it.

Also query Salesforce UCOs for additional signal on what the customer is evaluating or piloting:

```bash
sf data query --query "SELECT Name, Use_Case_Stage__c, Primary_Product__c, Secondary_Product__c, Use_Case_Description__c FROM UseCase__c WHERE Account__r.Name LIKE '%:ACCOUNT_NAME%' AND Use_Case_Stage__c IN ('U2 - Evaluated','U3 - PoC/Testing','U4 - Production Approved','U5 - Scaled') ORDER BY LastModifiedDate DESC LIMIT 20" --json 2>/dev/null
```

**Output of Phase 1:** A structured list of active product areas with usage tier. Example:
```
Active products: Unity Catalog (heavy), Delta Live Tables (moderate), Model Serving (light), SQL Warehouses (heavy)
Evaluating: Lakebase, AI/BI Dashboards
```

### Phase 2: Gather Recent Release Notes

Search for Databricks product updates in the look-back window using Glean (preferred) and web search as fallback.

**Step 2a: Glean search (if available)**

```
# Via Glean MCP
Search: "Databricks release notes <MONTH YEAR> <product-area>"
Search: "Databricks product updates <quarter>"
Search: "Databricks What's New <date-range>"
```

**Step 2b: Databricks docs web search (fallback)**

Use WebSearch or WebFetch to pull from the official Databricks release notes:
- Databricks Runtime release notes
- Platform release notes (Unity Catalog, Delta, Spark)
- AI/ML product updates
- SQL Analytics updates

Search for release note pages relevant to the customer's active products. Do NOT fetch the entire changelog — only sections relevant to the customer's product footprint identified in Phase 1.

**Step 2c: Filter to what's relevant**

Cross-reference the release notes against the customer's product footprint:
- Include: Updates to features the customer uses heavily or moderately
- Mention briefly: Updates to features the customer uses lightly or is evaluating
- Exclude: Features the customer has zero usage of (unless they're in UCO stage U1-U2 evaluating them)

### Phase 3: Categorize and Score Updates

For each relevant update, classify it:

| Category | Label | Description |
|----------|-------|-------------|
| **GA announcements** | `🟢 Now GA` | Features that moved from preview to generally available |
| **Performance improvements** | `⚡ Faster` | Speed/cost improvements to features they use |
| **New capabilities** | `✨ New` | Net-new functionality in products they use |
| **Security/compliance** | `🔒 Security` | Security or compliance changes that may require attention |
| **Deprecations** | `⚠️ Action needed` | Features being deprecated that the customer uses |
| **Pricing changes** | `💰 Pricing` | DBU or pricing changes affecting their usage |

**Scoring priority:**
1. Deprecations affecting current usage — always include, flag prominently
2. GA announcements for features they're evaluating (could accelerate adoption)
3. Performance improvements for their heaviest-used products
4. New capabilities in their core products
5. Nice-to-know improvements in lighter-use areas

Keep the brief to 5-8 items maximum. If more than 8 are relevant, keep the highest-scoring ones.

### Phase 4: Generate the Brief

Format the output based on the user's requested format (default: markdown):

---

**Default markdown output template** (stored in `resources/brief_template.md`):

```markdown
## Databricks Product Updates for [Customer Name]
*Updates from [DATE_FROM] to [DATE_TO] · Filtered to your active products*

---

### 🟢 Now Generally Available
[List GA announcements relevant to customer]

### ✨ New Capabilities
[New features in products they use]

### ⚡ Performance & Cost
[Performance improvements, including estimated impact if quantifiable]

### ⚠️ Action Required
[Deprecations, breaking changes, or items requiring customer action]

---
*Based on usage of: [list active product areas]*
*Questions? [Add your contact / SA name if desired]*
```

---

**Email format:**

Opens with a warm subject line like "What's new in Databricks for your team" and wraps the content in professional email language. Keep to 3-5 bullet points max for email.

**Slack message format:**

Lead with a 1-line hook, then a bulleted list of 3-5 items with emojis. End with a CTA ("Happy to demo any of these — just say the word").

**Google Doc format:**

Use `google-docs` skill to create a doc with the full structured brief including sections for each product area, links to official docs, and an "Ask your SA" section with space for notes.

### Phase 5: Review + Output

Print the brief and confirm with the user:
> "Here's your [format] for [customer]. Want me to adjust the focus, add/remove any items, or convert to a different format?"

If the user asks to save as Google Doc, invoke the `google-docs` skill to create the document.

## Anti-patterns

- **No generic changelogs.** Never paste raw Databricks release notes. Always filter and contextualize.
- **No speculation.** Only include confirmed/shipped features. If unsure of GA status, say "entering preview" or "recently announced" accurately.
- **No internal jargon.** Use customer-friendly language. "Delta Live Tables" not "DLT". "AI-powered dashboards" not "AI/BI".
- **No wall of text.** The brief should be scannable in 60 seconds. If it takes longer to read, trim it.

## Example Invocations

```
User: What's new for Octopus Energy?
→ Fetches their product footprint (heavy: Unity Catalog, SQL, Delta; evaluating: Lakebase)
→ Pulls last 30 days of release notes filtered to those products
→ Generates 6-item markdown brief

User: Prepare product update talking points for my Acme meeting tomorrow, focused on AI/ML
→ Fetches Acme's AI/ML footprint
→ Focuses on Model Serving, MLflow, AI Functions updates in last 30 days
→ Generates concise 4-item talking points

User: What should I tell Stripe about recent Databricks updates? Format as Slack message, last 60 days
→ Fetches Stripe's footprint (90-day look-back to confirm active products)
→ 60-day release note window
→ Formats as a Slack message with emojis

User: customer release brief for GlobalCorp since our last meeting on Jan 10
→ Uses Jan 10 as look-back start date
→ Generates full brief from that date
```
