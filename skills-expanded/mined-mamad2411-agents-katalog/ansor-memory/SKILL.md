---
name: ansor-memory
description: Read and write to the Product OS memory graph (Ansor). Use when logging evidence, recording decisions, tracking action items, or querying project/person data across PM workflows.
---

# Ansor Memory Skill

Procedural knowledge for using the **Product OS** database in Ansor as shared memory across PM workspace agents.

**MCP Server:** `ansor`
**Database slug:** `product_os`

## When to Use

- Logging evidence items from Slack, Linear, meetings, or HubSpot signals
- Recording decisions and their rationale after `/ingest` or `/research`
- Tracking action item candidates before promoting to Linear
- Looking up project IDs to link evidence/decisions to the right initiative
- Looking up person IDs to assign action items

---

## Schema Reference

### `project_registry`
Central list of all active initiatives. Used as FK target for evidence, decisions, and actions.

| Field | Type | Notes |
|---|---|---|
| `name` | string | Initiative display name |
| `notion_id` | string | Notion project page UUID |
| `linear_team_id` | string | Linear team ID if set |
| `slack_channels` | string[] | Associated Slack channels |

### `person`
Team members. Used as FK target for `action_item_candidate.proposed_owner`.

| Field | Type | Notes |
|---|---|---|
| `name` | string | Full name |
| `slack_id` | string | Slack member ID |
| `github_handle` | string | GitHub username |
| `linear_id` | string | Linear user ID |

### `evidence_item`
A captured signal or piece of evidence linked to a project.

| Field | Type | Notes |
|---|---|---|
| `source_tool` | string | `slack`, `linear`, `gmail`, `meeting`, `hubspot` |
| `url` | string | Permalink to source |
| `snippet` | string | Relevant quote or summary |
| `timestamp` | string | ISO 8601, e.g. `"2026-03-02T14:00:00Z"` |
| `project_id` | string | FK → `project_registry.id` |

### `decision_record`
A product or process decision with rationale and evidence links.

| Field | Type | Notes |
|---|---|---|
| `decision` | string | What was decided |
| `rationale` | string | Why |
| `evidence_refs` | string[] | Array of `evidence_item.id` values |
| `project_id` | string | FK → `project_registry.id` (required) |

### `action_item_candidate`
A proposed task extracted from a signal, not yet committed to Linear.

| Field | Type | Notes |
|---|---|---|
| `text` | string | Task description |
| `proposed_owner` | string | FK → `person.id` |
| `status` | string | `pending`, `committed`, `rejected` |
| `project_id` | string | FK → `project_registry.id` |

---

## Common Patterns

### Look up a project_id by initiative name

```
CallMcpTool: ansor / query_records
{
  "databaseSlug": "product_os",
  "entityKey": "project_registry",
  "filterJson": "{\"name\": \"Chief of Staff Experience\"}"
}
```

Returns `records[0].id` — use this as `project_id` in evidence/decisions/actions.

### Look up a person_id by name

```
CallMcpTool: ansor / query_records
{
  "databaseSlug": "product_os",
  "entityKey": "person",
  "filterJson": "{\"name\": \"Tyler Sahagun\"}"
}
```

### Log an evidence item

```
CallMcpTool: ansor / create_record
{
  "databaseSlug": "product_os",
  "entityKey": "evidence_item",
  "payloadJson": "{\"source_tool\":\"slack\",\"url\":\"https://askelephant.slack.com/archives/C.../p...\",\"snippet\":\"Customer said they can't find the settings page\",\"timestamp\":\"2026-03-02T10:15:00Z\",\"project_id\":\"<project_registry_id>\"}"
}
```

### Record a decision

```
CallMcpTool: ansor / create_record
{
  "databaseSlug": "product_os",
  "entityKey": "decision_record",
  "payloadJson": "{\"decision\":\"Scope settings redesign to admin users only in V1\",\"rationale\":\"Rep feedback shows admins are blocked; reps rarely change settings\",\"evidence_refs\":[\"<evidence_item_id>\"],\"project_id\":\"<project_registry_id>\"}"
}
```

### Create an action item candidate

```
CallMcpTool: ansor / create_record
{
  "databaseSlug": "product_os",
  "entityKey": "action_item_candidate",
  "payloadJson": "{\"text\":\"Schedule follow-up with Dylan on signal table schema\",\"proposed_owner\":\"<person_id>\",\"status\":\"pending\",\"project_id\":\"<project_registry_id>\"}"
}
```

### Promote action item to Linear (mark as committed)

```
CallMcpTool: ansor / update_record
{
  "databaseSlug": "product_os",
  "entityKey": "action_item_candidate",
  "recordId": "<action_item_id>",
  "payloadJson": "{\"status\":\"committed\"}"
}
```

### Query all pending action items for a project

```
CallMcpTool: ansor / query_records
{
  "databaseSlug": "product_os",
  "entityKey": "action_item_candidate",
  "filterJson": "{\"project_id\": \"<project_registry_id>\", \"status\": \"pending\"}"
}
```

---

## Integration Points

| Agent | When to use Ansor |
|---|---|
| `signals-processor` | Log `evidence_item` per signal; create `action_item_candidate` per extracted action |
| `research-analyzer` | Log `evidence_item` for research findings; record `decision_record` for scoping choices |
| `linear-triage` | Mark `action_item_candidate` as `committed` after creating Linear issue |
| `hypothesis-manager` | Query `evidence_item` by `project_id` to find supporting evidence |
| `workspace-admin` | Query all tables for cross-initiative reporting |

---

## Project Registry (Seeded)

Quick reference IDs — use `query_records` to get live IDs:

| Initiative | Notion ID |
|---|---|
| Global Chat | `2c0f79b2-c8ac-8199-8b42-c3e9126cac78` |
| Agent Command Center | `301f79b2-c8ac-8162-89dc-e4b4b298eb19` |
| Chief of Staff Experience | `30af79b2-c8ac-8125-b850-d5df42f68e76` |
| Feedback Intelligence | *(no Notion ID yet)* |
| Universal Signal Tables | `2e2f79b2-c8ac-81e0-9481-e3a196a216ea` |
| FGA Engine | `2c5f79b2-c8ac-807a-8a11-d430594431ff` |
| Feature Flag Audit | `2e7f79b2-c8ac-81a4-bd34-c955b8d07595` |
| Settings Redesign | `2eaf79b2-c8ac-812e-a058-fe0ae17dfd7e` |
