---
name: feip-dedup-sweep
description: "Search for duplicate and overlapping FEIP projects by topic area or keywords, identify clusters, and coordinate consolidation via Slack DMs and Jira comments. Two modes: topic similarity search (ai_similarity on logfood) or term-based JQL search. Use when the user mentions FEIP dedup, finding duplicate FEIP projects, FEIP consolidation, overlapping innovation projects, or sweeping a topic area for duplicates. Triggers on 'feip dedup', 'duplicate feip', 'feip sweep', 'find overlapping feip', 'consolidate feip projects', 'feip topic search', 'dedup sweep'."
user-invocable: true
---

# FEIP Dedup Sweep

A batch deduplication workflow for FEIP projects. Searches for overlapping innovation projects by topic area or keywords, identifies duplicate clusters, and coordinates consolidation through Slack outreach and Jira comments.

**Announce at start:** "I'm using the feip-dedup-sweep skill to find and consolidate overlapping FEIP projects."

**Data layer:** This skill queries the FEIP project data directly via logfood SQL (`ai_similarity()` on `main.field_innovation.jira_issues`) and Jira MCP. The SQL templates in `resources/` are the same queries used by the `fe-innovation-program` plugin's `feip-deduper` skill — they're included here so this skill works independently without requiring that plugin to be installed.

**Future integration:** When the `fe-innovation-program` plugin is published to the Vibe marketplace, this skill can optionally delegate search to `feip-project-discovery` and `feip-deduper` instead of running the SQL directly. Until then, this skill is fully self-contained.

---

## Prerequisites

### 1. Databricks logfood profile
```bash
/usr/local/bin/databricks auth profiles | grep logfood
```
If expired, re-authenticate:
```bash
/usr/local/bin/databricks auth login --profile logfood
```

### 2. Jira MCP
```
ToolSearch query: "select:mcp__jira__jira_read_api_call,mcp__jira__jira_write_api_call"
```

### 3. Slack MCP
```
ToolSearch query: "select:mcp__slack__slack_write_api_call,mcp__slack__slack_read_api_call"
```

### 4. Key constants
- **Schema:** `main.field_innovation.jira_issues` + `main.field_innovation.metrics_dashboard`
- **Warehouse ID:** `df7eb7e74dc8866d`
- **CLI path:** `/usr/local/bin/databricks` (avoid old CLI version in PATH)
- **Run queries from:** `/tmp` (avoids bundle config conflicts)
- **Async queries:** Always use `"wait_timeout": "0s"` — `ai_similarity()` takes 60-120s across 4,600+ tickets. Poll with `GET /api/2.0/sql/statements/{statement_id}` until state is `SUCCEEDED`.

---

## Mode Selection

Use AskUserQuestion to present the two modes:

**Menu — How would you like to search?** (2 options):
- "Topic similarity search" — description: "Describe a topic area (e.g., 'data warehousing migration tools') and find all FEIP projects that overlap using AI similarity scoring."
- "Term-based search" — description: "Search by specific keywords or product names (e.g., 'lakebridge', 'power bi migration') to find all matching FEIP tickets."

If the user's initial prompt clearly indicates a mode, skip the menu. E.g., "find duplicate FEIPs about migration" → Mode 1. "Find all lakebridge FEIPs" → Mode 2.

---

## Mode 1: Topic Similarity Search

### Step 1.1 — Collect Search Topic

Ask the user for the topic area to search. Accept free text. Examples:
- "data warehousing SQL analytics warehouse optimization"
- "AI-powered migration tool Snowflake Redshift SQL translation"
- "streaming real-time analytics Spark Structured Streaming"

If the user provides a short phrase, expand it with related terms to improve recall. E.g., "DWH migration" → "data warehousing migration tool Snowflake Redshift Synapse SQL translation conversion code migration accelerator".

Store as `{search_topic}`.

### Step 1.2 — Run Similarity Search

Run the query from `resources/topic_similarity_search.sql` with:
- `{SEARCH_TEXT}` = `{search_topic}`
- `{LIMIT}` = `25`

**Execution pattern:**
```bash
cd /tmp && /usr/local/bin/databricks api post --profile=logfood /api/2.0/sql/statements \
  --json '{"warehouse_id":"df7eb7e74dc8866d","statement":"<SQL>","wait_timeout":"0s"}'
```

Poll for results. The query typically takes 60-120s (cold warehouse may take longer).

### Step 1.3 — Present Initial Results

Show the top results above the collaboration threshold (>= 0.63) as a table:

```
| Score  | Ticket       | Status     | Summary                          | Owner          |
|--------|-------------|------------|----------------------------------|----------------|
| 0.7773 | FEIP-1631   | Idea       | DB SQL Query Tuning Insights     | Harika Mariyala|
```

**Important:** The logfood `metrics_dashboard` join often returns NULL for owner names. Note this to the user — we'll get real owners from Jira in the action phase.

Count and summarize: "Found N tickets above 0.63 threshold. N above 0.73 (likely duplicate range)."

### Step 1.4 — Pairwise Cross-Comparison

Take the top 15-20 results and run the query from `resources/pairwise_comparison.sql` to find actual duplicate pairs.

Present pairs above 0.73 as a table:

```
| Score  | Ticket A     | Summary A                    | Ticket B     | Summary B                    |
|--------|-------------|------------------------------|-------------|------------------------------|
| 0.8715 | FEIP-303    | DBSQL Serverless Scaling     | FEIP-304    | DBSQL Serverless Platform Rec|
```

### Step 1.5 — Cluster Analysis

Identify clusters by grouping tickets that appear in multiple high-scoring pairs. A ticket that scores >= 0.78 with 3+ other tickets is a cluster anchor.

**Scoring tiers** (calibrated on 4,632 tickets, max ~0.83):

| Tier | Score | Meaning |
|------|-------|---------|
| Near-Certain Duplicate | >= 0.78 | Same idea, block/consolidate |
| Likely Duplicate | 0.73-0.77 | Strong overlap, recommend consolidation |
| Consolidation Opportunity | 0.68-0.72 | Related work, consider coordinating |
| Collaboration Opportunity | 0.63-0.67 | Complementary, potential collaborators |

**Context-aware scoring:** Vague inputs rarely exceed ~0.75. A 0.73 from vague input is equivalent to a 0.80 from detailed input. Adjust interpretation accordingly.

Present each cluster with:
- Cluster name (derived from common theme)
- Member tickets with status and owner
- Recommended anchor (Active > Idea > Inactive; has working code > no code)

Use AskUserQuestion: "Which clusters would you like to action? (select by number, or 'all')"

→ Proceed to **Action Phase** (Step 3).

---

## Mode 2: Term-Based Search

### Step 2.1 — Collect Search Terms

Ask the user for keywords or product names. Examples:
- "lakebridge"
- "power bi migration"
- "liquid clustering"

### Step 2.2 — Search Jira

Use Jira MCP to search:
```
mcp__jira__jira_read_api_call with endpoint "issues.search":
  jql: "project = FEIP AND summary ~ '{search_terms}' ORDER BY created ASC"
  max_results: 30
```

Also run a supplementary logfood similarity search using the terms to catch tickets that don't use the exact keywords but are semantically similar:
- Run `resources/topic_similarity_search.sql` with `{SEARCH_TEXT}` = search terms
- Merge results, dedup by ticket key

### Step 2.3 — Present Results

Show all matching tickets as a table with key, summary, status, assignee, and created date.

If there are 5+ tickets, offer to run pairwise comparison (Step 1.4) to find which ones are actually duplicates vs. distinct workstreams.

Use AskUserQuestion: "Would you like to cross-compare these for duplicates, or proceed to action on specific tickets?"

→ If cross-compare: run Step 1.4 and Step 1.5, then proceed to Action Phase.
→ If action directly: proceed to Action Phase with selected tickets.

---

## Action Phase (Step 3)

### Step 3.1 — Get Real Owners from Jira

For each ticket in the selected cluster(s), fetch owner details via Jira MCP:
```
mcp__jira__jira_read_api_call with endpoint "issues.get":
  issue_id: "{ticket_key}"
  analysis_prompt: "Who is the reporter and assignee? Return display names and email addresses."
```

Also read existing comments to:
- Avoid posting duplicate dedup comments (check for "FEIP Dedup Pass" in existing comments)
- Check if consolidation discussions already happened
- Note any prior outreach by Franco or program leads

### Step 3.2 — Identify Anchor and Coordination Target

Per cluster, determine:
1. **Anchor ticket** — the one with most traction (Active status, working code, most contributors)
2. **Coordination target** — if there's a product/program that should own this area (e.g., Lakebridge for migration, a specific SME community), identify it

Present the recommendation to the user:
```
Cluster: "SQL Warehouse Optimization" (5 tickets)
Anchor: FEIP-1677 (QMetrics, Active, has working v1)
Coordination target: None identified (standalone cluster)
Owners to contact: Nikolaos Servos, Harika Mariyala, Nishant Deshpande
Tickets to comment: FEIP-1596, FEIP-1631, FEIP-1677, FEIP-1696, FEIP-2707
```

Use AskUserQuestion: "Approve this action plan? (yes / modify / skip this cluster)"

### Step 3.3 — Draft Slack Messages

For each unique owner, draft a personalized Slack DM:
- Reference their specific ticket(s)
- Name the overlapping tickets and their owners
- Note whether their tool is complementary or duplicate
- Suggest coordination
- If there's a coordination target (e.g., Lakebridge), mention it

Present all drafted messages to the user for approval before sending.

**Send via:**
```
mcp__slack__slack_write_api_call with endpoint "chat.postMessage":
  channel: "@{owner_username}"
  text: "{drafted_message}"
```

**Finding Slack usernames:** Use the owner's email from Jira to look up their Slack handle:
```
mcp__slack__slack_read_api_call with endpoint "users.lookupByEmail":
  email: "{owner_email}"
```

### Step 3.4 — Post Jira Comments

For each ticket in the cluster, post a structured comment:

**Comment template (ADF format):**
```json
{
  "type": "doc", "version": 1, "content": [{
    "type": "paragraph", "content": [
      {"type": "text", "text": "FEIP Dedup Pass — [Category]: ", "marks": [{"type": "strong"}]},
      {"type": "text", "text": "[Context-specific message with links to overlapping tickets and coordination target]"}
    ]
  }]
}
```

Each comment should include:
- Bold prefix: "FEIP Dedup Pass — {Category}:"
- Links to overlapping tickets (as Jira URLs)
- Similarity scores where notable
- Direction to coordinate (e.g., "coordinate with the Lakebridge team in #lakebridge")
- Posted via `mcp__jira__jira_write_api_call` with endpoint `issues.add_comment`

**Skip tickets that already have a "FEIP Dedup Pass" comment** (detected in Step 3.1).

### Step 3.5 — Escalation (Large Clusters)

If a cluster has 10+ tickets, additionally:
1. Message the FEIP program leads (Nikki Parekh / Fred Abood) via Slack with the cluster summary
2. If a product owner is identified (e.g., Guenia Izquierdo for Lakebridge), message them with the full list of overlapping FEIPs

### Step 3.6 — Log Results

After all actions are taken, present a summary:

```
## Dedup Sweep Summary

**Topic:** {search_topic}
**Date:** {today}

### Slack DMs Sent (N/N)
- {owner_name} — {ticket_keys}, {status}

### Jira Comments Posted (N/N)
- {ticket_key} — {comment_summary}

### Skipped (already commented)
- {ticket_key} — existing dedup comment from {date}

### Escalations
- {person} — {reason}
```

---

## Related: Single-Ticket Dedup

This skill is for **batch/topic-level sweeps** — finding all duplicates in an area. For checking a **single ticket** for duplicates, the `fe-innovation-program` plugin (maintained by Fred Abood in the `field-innovation` repo) has a dedicated `feip-deduper` skill invoked via `/fe-innovate check FEIP-XXX for dupes`. If the user asks about a single ticket, suggest that workflow instead.

**FEIP plugin repo:** `https://github.com/databricks-field-eng/field-innovation/tree/main/vibe-plugins`
**FEIP plugin Slack:** `#fe-ip`
**FEIP plugin maintainer:** Fred Abood (fred.abood@databricks.com)

---

## Resources

- `resources/topic_similarity_search.sql` — Semantic similarity search across all active FEIP projects. Parameters: `{SEARCH_TEXT}`, `{LIMIT}`. Uses `ai_similarity()` on logfood.
- `resources/pairwise_comparison.sql` — Cross-comparison for finding duplicate pairs within a candidate set. Parameters: `{TICKET_KEYS}`, `{LIMIT}`. Uses `ai_similarity()` between ticket pairs.
