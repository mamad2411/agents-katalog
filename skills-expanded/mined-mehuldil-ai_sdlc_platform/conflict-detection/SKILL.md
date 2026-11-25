---
name: conflict-detection
description: Detect state conflicts between local memory and Azure DevOps by comparing attributes and identifying divergences
model: sonnet-4-6
token_budget: {input: 6000, output: 3000}
---

# Conflict Detection Skill

Compares local SDLC memory state with Azure DevOps work items to identify conflicts, drifts, and divergences.

## State Comparison Attributes

| Attribute | Source | Comparison | Conflict? |
|-----------|--------|-----------|-----------|
| Status | Work item state | Exact match | Yes if differ |
| Assignee | Work item assignment | Exact match | Yes if differ |
| Tags | Work item tags | Set comparison | No (merge) |
| Comments | Comment count/thread | ADO > Local? | No (pull) |
| Attachments | File list | ADO > Local? | No (pull) |
| Updated timestamp | Last modification | Compare recency | Informational |

## Conflict Detection Rules

### Status Conflict
- **Triggered when**: local_status != ado_status AND both have values
- **Severity**: Major
- **Action**: Mark for manual escalation

### Assignee Conflict
- **Triggered when**: local_assignee != ado_assignee AND both have values
- **Severity**: Major
- **Action**: Mark for manual escalation

### Comment Drift
- **Triggered when**: ado_comment_count > local_comment_count
- **Severity**: Minor
- **Action**: Auto-pull if SDLC_AUTO_RESOLVE_ARTIFACTS=true

### Tag Mismatch
- **Triggered when**: ado_tags != local_tags (set difference)
- **Severity**: Minor
- **Action**: Auto-merge (pull ADO tags, preserve local additions)

### No Conflict
- **Condition**: State is synchronized
- **Action**: Proceed with stage execution

## Detection Process

1. Fetch ADO State via MCP
2. Get Local State from memory files
3. Compare Each Attribute
4. Categorize Conflicts
5. Generate Detection Report
6. Record Timestamp

## Triggers

Use this skill when:
- Before pipeline stage execution
- Detecting state drift before operations
- User requests state check
- Pre-sync validation

---
