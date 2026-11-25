---
name: conflict-resolution
description: Resolve state conflicts using 4 deterministic strategies (accept ADO, push local, manual merge, retry)
model: sonnet-4-6
token_budget: {input: 6000, output: 3000}
---

# Conflict Resolution Skill

Applies conflict resolution strategies to synchronize local SDLC memory with Azure DevOps state.

## Resolution Strategies

### Strategy 1: Accept ADO State
**When**: External changes from other team members
**Actions**: Update local to ADO, pull comments/metadata
**Outcome**: Local memory aligns with ADO (ADO wins)

### Strategy 2: Push Local State
**When**: Local represents intended progress not yet in ADO
**Actions**: Queue local changes for push, override ADO on next push
**Outcome**: ADO will be updated on next push cycle

### Strategy 3: Manual Merge
**When**: Both have valid, non-conflicting information
**Actions**: Display side-by-side, allow user to select fields
**Outcome**: Merged state in both systems

### Strategy 4: Retry After Delay
**When**: Temporary ADO unavailability
**Actions**: Activate offline mode, queue sync for retry
**Outcome**: Deferred sync, no blockage

## User Interaction for Manual Resolution

Presents conflict with options:
1) Accept ADO state
2) Push local state
3) Manual merge
4) Retry

## State File Updates

- `.sdlc/memory/{story-id}/state.json` - conflicting fields
- `.sdlc/state.json` - memory_synced_at timestamp
- `.sdlc/sync-log.json` - resolution operation log
- `.sdlc/pending-sync.json` - offline operations

## Configuration

```bash
SDLC_SYNC_TIMEOUT_SECONDS=30
SDLC_AUTO_RESOLVE_ARTIFACTS=true
SDLC_OFFLINE_RETRY_INTERVAL=1800
SDLC_CONFLICT_MODE=alert
```

## Triggers

Use this skill when:
- Manual conflicts detected
- User input required for resolution
- Implementing resolution strategy
- Updating state files after resolution

---
