---
name: state-merge
description: Merge state from local memory and ADO across branches, managing tags, comments, and metadata
model: sonnet-4-6
token_budget: {input: 6000, output: 3000}
---

# State Merge Skill

Merges state across local memory and Azure DevOps branches, handling non-conflicting changes, artifacts, and metadata.

## Merge Operations

### 1. Tag Merging
**When**: Non-conflicting tag differences
**Process**: Union both tag sets, update both sources
**Example**: Local [reviewed, testing] + ADO [blocked] = [reviewed, testing, blocked]

### 2. Comment & Attachment Pulling
**When**: ADO has newer artifacts and SDLC_AUTO_RESOLVE_ARTIFACTS=true
**Process**: Pull new comments, store in ado-context.json
**Result**: Local memory enriched with ADO artifacts

### 3. Cross-Branch State Sync
**When**: Merging changes from one branch to another
**Process**: 3-way merge with base/local/remote
**Resolution**: Auto-resolve non-conflicts, flag conflicts

### 4. Metadata Merging
**When**: Updating sync information
**Process**: Update memory_synced_at, sync status, sync version

## Merge Decision Logic

- Both have same value → No action
- Only local has value → Use local
- Only ADO has value → Use ADO (for artifacts)
- Both differ → Escalate or merge intelligently

## Precedence Rules

- Comments/Attachments: ADO wins (authoritative)
- Tags: Merge (union)
- Status/Assignee: Conflict (escalate)
- Timestamps: Most recent
- Artifacts: Keep all

## Merge Report

Documents merged items, changes made, status.

## State File Modifications

- `.sdlc/memory/{story-id}/state.json` - merged tags, timestamps
- `.sdlc/memory/{story-id}/ado-context.json` - new comments
- `.sdlc/state.json` - memory_synced_at
- `.sdlc/sync-log.json` - merge operation log

## Error Handling

- Corrupt JSON: Use defaults, log error
- Missing file: Create with merge results
- Timestamp issues: Use current time
- Duplicate tags: Remove, keep union

## Triggers

Use this skill when:
- Merging non-conflicting changes
- Pulling artifacts from ADO
- Reconciling cross-branch state
- Updating metadata after resolution

---
