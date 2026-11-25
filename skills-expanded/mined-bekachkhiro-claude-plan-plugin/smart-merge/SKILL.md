# Smart Merge Skill

You are a smart merge algorithm handler for PlanFlow hybrid sync. Your role is to intelligently merge local and cloud task changes, detecting conflicts and auto-merging where safe.

## Objective

Provide Git-like smart merge capabilities for task synchronization between local PROJECT_PLAN.md and PlanFlow cloud, enabling seamless collaboration without data loss.

## When to Use

This skill is invoked internally by:
- `/update` - When hybrid sync mode is enabled
- `/sync` - For bidirectional sync operations
- Auto-sync - Background task status synchronization

**This is NOT a user-invocable skill.** It's a utility skill used by other commands.

---

## Core Concepts

### Merge Scenarios

| Local Changed | Cloud Changed | Same Task? | Same Value? | Result |
|---------------|---------------|------------|-------------|--------|
| T1.1 | T2.3 | No | N/A | **AUTO MERGE** |
| T1.1 → done | T1.1 → done | Yes | Yes | **AUTO MERGE** |
| T1.1 → done | T1.1 → blocked | Yes | No | **CONFLICT** |
| T1.1 → done | (unchanged) | Yes | N/A | **AUTO MERGE** |
| (unchanged) | T1.1 → done | Yes | N/A | **AUTO MERGE** |

### Merge Rules

```
Rule 1: Different tasks modified → AUTO MERGE (no overlap)
Rule 2: Same task, same value → AUTO MERGE (convergent change)
Rule 3: Same task, different values → CONFLICT (divergent change)
Rule 4: Only local changed → AUTO MERGE (push)
Rule 5: Only cloud changed → AUTO MERGE (pull)
```

---

## Data Structures

### TaskChange Object

Represents a change to a single task:

```typescript
interface TaskChange {
  taskId: string           // e.g., "T1.1"
  previousStatus: string   // Status before change
  newStatus: string        // Status after change
  updatedAt: string        // ISO 8601 timestamp
  updatedBy: string        // "local" or email address
  source: "local" | "cloud"
}
```

### MergeContext Object

Context for merge operation:

```typescript
interface MergeContext {
  taskId: string
  localChange: TaskChange | null
  cloudChange: TaskChange | null
  lastSyncedAt: string | null  // Last successful sync timestamp
  baseStatus: string           // Status at last sync (common ancestor)
}
```

### MergeResult Object

Result of merge operation:

```typescript
interface MergeResult {
  result: "AUTO_MERGE" | "CONFLICT" | "NO_CHANGE"
  reason: string
  action: "push" | "pull" | "skip" | "resolve"
  finalStatus?: string
  conflict?: ConflictDetails
}

interface ConflictDetails {
  taskId: string
  taskName: string
  local: {
    status: string
    updatedAt: string
    updatedBy: string
  }
  cloud: {
    status: string
    updatedAt: string
    updatedBy: string
  }
  base: {
    status: string
    syncedAt: string
  }
}
```

---

## Core Functions

### Function: smartMerge

Main entry point for smart merge algorithm.

**Pseudo-code:**
```javascript
/**
 * Perform smart merge for a task
 * @param {MergeContext} context - Merge context with local/cloud changes
 * @returns {MergeResult} Result of merge operation
 */
function smartMerge(context) {
  const { taskId, localChange, cloudChange, lastSyncedAt, baseStatus } = context

  // Normalize statuses
  const localStatus = localChange ? normalizeStatus(localChange.newStatus) : null
  const cloudStatus = cloudChange ? normalizeStatus(cloudChange.newStatus) : null
  const normalizedBase = normalizeStatus(baseStatus)

  // Case 1: No changes at all
  if (!localChange && !cloudChange) {
    return {
      result: "NO_CHANGE",
      reason: "no_changes",
      action: "skip",
      finalStatus: normalizedBase
    }
  }

  // Case 2: Only local changed - safe to push
  if (localChange && !cloudChange) {
    return {
      result: "AUTO_MERGE",
      reason: "local_only",
      action: "push",
      finalStatus: localStatus
    }
  }

  // Case 3: Only cloud changed - safe to pull
  if (!localChange && cloudChange) {
    return {
      result: "AUTO_MERGE",
      reason: "cloud_only",
      action: "pull",
      finalStatus: cloudStatus
    }
  }

  // Case 4: Both changed - check if same value (convergent)
  if (localStatus === cloudStatus) {
    return {
      result: "AUTO_MERGE",
      reason: "convergent_change",
      action: "skip",  // Already in sync
      finalStatus: localStatus
    }
  }

  // Case 5: Both changed to different values - CONFLICT
  return {
    result: "CONFLICT",
    reason: "divergent_change",
    action: "resolve",
    conflict: {
      taskId,
      taskName: localChange.taskName || cloudChange.taskName,
      local: {
        status: localStatus,
        updatedAt: localChange.updatedAt,
        updatedBy: localChange.updatedBy
      },
      cloud: {
        status: cloudStatus,
        updatedAt: cloudChange.updatedAt,
        updatedBy: cloudChange.updatedBy
      },
      base: {
        status: normalizedBase,
        syncedAt: lastSyncedAt
      }
    }
  }
}
```

---

### Function: normalizeStatus

Normalize status strings for comparison.

**Pseudo-code:**
```javascript
/**
 * Normalize task status for comparison
 * @param {string} status - Raw status string
 * @returns {string} Normalized status (TODO, IN_PROGRESS, DONE, BLOCKED)
 */
function normalizeStatus(status) {
  if (!status) return "TODO"

  const normalized = status.toUpperCase().trim()

  // Handle status with emoji suffixes (from PROJECT_PLAN.md format)
  if (normalized.includes("DONE") || normalized.includes("✅")) {
    return "DONE"
  }
  if (normalized.includes("IN_PROGRESS") || normalized.includes("🔄")) {
    return "IN_PROGRESS"
  }
  if (normalized.includes("BLOCKED") || normalized.includes("🚫")) {
    return "BLOCKED"
  }
  if (normalized.includes("TODO")) {
    return "TODO"
  }

  // Return as-is if no match
  return normalized
}
```

---

### Function: detectChanges

Detect what changed between base state and current state.

**Pseudo-code:**
```javascript
/**
 * Detect changes between base and current states
 * @param {Object} params - Detection parameters
 * @returns {TaskChange | null} Change object or null if unchanged
 */
function detectChanges(params) {
  const { taskId, baseStatus, currentStatus, updatedAt, updatedBy, source } = params

  const normalizedBase = normalizeStatus(baseStatus)
  const normalizedCurrent = normalizeStatus(currentStatus)

  // No change
  if (normalizedBase === normalizedCurrent) {
    return null
  }

  return {
    taskId,
    previousStatus: normalizedBase,
    newStatus: normalizedCurrent,
    updatedAt,
    updatedBy,
    source
  }
}
```

---

### Function: buildMergeContext

Build merge context from local and cloud task states.

**Pseudo-code:**
```javascript
/**
 * Build merge context for a task
 * @param {Object} params - Context parameters
 * @returns {MergeContext} Complete merge context
 */
function buildMergeContext(params) {
  const {
    taskId,
    localStatus,
    localUpdatedAt,
    cloudStatus,
    cloudUpdatedAt,
    cloudUpdatedBy,
    lastSyncedAt,
    baseStatus  // Status at last sync
  } = params

  // Detect local change
  const localChange = detectChanges({
    taskId,
    baseStatus,
    currentStatus: localStatus,
    updatedAt: localUpdatedAt,
    updatedBy: "local",
    source: "local"
  })

  // Detect cloud change (only if cloud updated after last sync)
  let cloudChange = null
  if (lastSyncedAt) {
    const syncTime = new Date(lastSyncedAt).getTime()
    const cloudTime = new Date(cloudUpdatedAt).getTime()

    if (cloudTime > syncTime) {
      cloudChange = detectChanges({
        taskId,
        baseStatus,
        currentStatus: cloudStatus,
        updatedAt: cloudUpdatedAt,
        updatedBy: cloudUpdatedBy,
        source: "cloud"
      })
    }
  }

  return {
    taskId,
    localChange,
    cloudChange,
    lastSyncedAt,
    baseStatus
  }
}
```

---

### Function: performHybridSync

Complete hybrid sync flow for a single task update.

**Pseudo-code:**
```javascript
/**
 * Perform hybrid sync for a task update
 * @param {Object} params - Sync parameters
 * @param {Object} config - Merged config object
 * @param {Object} t - Translation object
 * @returns {Object} Sync result
 */
async function performHybridSync(params, config, t) {
  const { taskId, newStatus, taskName } = params
  const cloudConfig = config.cloud || {}
  const { apiToken, projectId, lastSyncedAt, apiUrl } = cloudConfig

  // Step 1: Show syncing indicator
  console.log(t.commands.update.hybridSyncing)

  // Step 2: Pull cloud state
  console.log(t.commands.update.hybridPulling)
  const cloudState = await getCloudTaskState(projectId, taskId, apiToken, apiUrl)

  // Step 3: Handle task not found on cloud (new task)
  if (!cloudState.found && cloudState.isNew) {
    console.log(t.commands.update.hybridTaskNew)
    const pushResult = await updateCloudTaskStatus(
      projectId, taskId, newStatus, apiToken, apiUrl
    )
    if (pushResult.success) {
      console.log(t.commands.update.hybridSyncSuccess)
      return { success: true, action: "push", newTask: true }
    }
    return { success: false, error: pushResult.error }
  }

  // Step 4: Handle pull error
  if (!cloudState.found && cloudState.error) {
    console.log(t.commands.update.hybridPullFailed)
    console.log(t.commands.update.hybridLocalOnly)
    return { success: false, localOnly: true }
  }

  // Step 5: Build merge context
  // Base status = what we last synced (cloud status at lastSyncedAt)
  // For simplicity, use cloud status as base if no lastSyncedAt
  const baseStatus = lastSyncedAt ? cloudState.status : newStatus

  const context = buildMergeContext({
    taskId,
    localStatus: newStatus,
    localUpdatedAt: new Date().toISOString(),
    cloudStatus: cloudState.status,
    cloudUpdatedAt: cloudState.updatedAt,
    cloudUpdatedBy: cloudState.updatedBy,
    lastSyncedAt,
    baseStatus
  })

  // Step 6: Perform smart merge
  const mergeResult = smartMerge(context)

  // Step 7: Handle merge result
  switch (mergeResult.result) {
    case "NO_CHANGE":
      console.log(t.commands.update.hybridNoConflict)
      return { success: true, action: "skip", noChange: true }

    case "AUTO_MERGE":
      if (mergeResult.action === "push") {
        console.log(t.commands.update.hybridPushing)
        const pushResult = await updateCloudTaskStatus(
          projectId, taskId, newStatus, apiToken, apiUrl
        )
        if (pushResult.success) {
          console.log(t.commands.update.hybridAutoMerge)
          console.log(t.commands.update.hybridSyncSuccess)
          return { success: true, action: "push", merged: true }
        }
        console.log(t.commands.update.hybridPushFailed)
        return { success: false, error: pushResult.error }
      }

      if (mergeResult.action === "pull") {
        // Cloud has changes, update local
        console.log(t.commands.update.hybridAutoMerge)
        return {
          success: true,
          action: "pull",
          merged: true,
          cloudStatus: cloudState.status
        }
      }

      if (mergeResult.action === "skip") {
        console.log(t.commands.update.hybridNoConflict)
        return { success: true, action: "skip", alreadySynced: true }
      }
      break

    case "CONFLICT":
      console.log(t.commands.update.hybridConflict)
      return {
        success: false,
        action: "resolve",
        conflict: mergeResult.conflict
      }
  }

  return { success: false, error: "Unknown merge result" }
}
```

---

## Conflict Resolution

### Conflict Detection

A conflict occurs when:
1. Both local and cloud modified the same task
2. The modifications result in different values
3. Cloud modification happened after lastSyncedAt

**Conflict Check Flow:**
```
1. Get lastSyncedAt from config
2. Fetch cloud task state
3. If cloud.updatedAt > lastSyncedAt:
   a. Cloud was modified since last sync
   b. If local.status != cloud.status:
      → CONFLICT
   c. If local.status == cloud.status:
      → AUTO MERGE (convergent)
4. If cloud.updatedAt <= lastSyncedAt:
   → AUTO MERGE (safe to push)
```

### Conflict Data for UI

When a conflict is detected, provide rich data for the UI:

```typescript
interface ConflictDisplayData {
  taskId: string
  taskName: string

  local: {
    status: string
    statusEmoji: string      // ✅, 🔄, 🚫, etc.
    updatedAt: string        // Formatted time
    updatedAgo: string       // "5 minutes ago"
    updatedBy: string        // "You"
  }

  cloud: {
    status: string
    statusEmoji: string
    updatedAt: string
    updatedAgo: string
    updatedBy: string        // Email or name
  }

  base: {
    status: string
    statusEmoji: string
    syncedAt: string
    syncedAgo: string
  }
}
```

### Resolution Options

Users can resolve conflicts with:

1. **Keep Local** - Push local status, overwrite cloud
2. **Keep Cloud** - Pull cloud status, overwrite local
3. **Cancel** - Keep both as-is, no sync

**Resolution Actions:**
```javascript
async function resolveConflict(resolution, context, config) {
  const { taskId } = context.conflict
  const cloudConfig = config.cloud || {}

  switch (resolution) {
    case "local":
      // Push local status with force
      await updateCloudTaskStatus(
        cloudConfig.projectId,
        taskId,
        context.localStatus,
        cloudConfig.apiToken,
        cloudConfig.apiUrl
      )
      return { resolved: true, kept: "local" }

    case "cloud":
      // Update local file with cloud status
      await updateLocalTaskStatus(taskId, context.cloudStatus)
      return { resolved: true, kept: "cloud" }

    case "cancel":
      return { resolved: false, cancelled: true }
  }
}
```

---

## Integration with /update Command

### Modified /update Flow (Hybrid Mode)

```
/update T1.1 done
       ↓
1. Validate inputs
       ↓
2. Read PROJECT_PLAN.md
       ↓
3. Find task T1.1
       ↓
4. Update local status → DONE
       ↓
5. Save PROJECT_PLAN.md
       ↓
6. Check if hybrid sync enabled:
   - apiToken exists?
   - projectId exists?
   - storageMode === "hybrid"?
       ↓
7. If YES → performHybridSync()
       ↓
8. Handle result:
   - AUTO_MERGE → Show success
   - CONFLICT → Show conflict UI
   - ERROR → Show warning (local saved)
       ↓
9. Update lastSyncedAt on success
       ↓
10. Show confirmation
```

### Pseudo-code for /update Integration

```javascript
// In commands/update/SKILL.md Step 8

async function handleHybridSync(taskId, newStatus, config, t) {
  const cloudConfig = config.cloud || {}

  // Check if hybrid sync is enabled
  if (cloudConfig.storageMode !== "hybrid") {
    // Fall back to simple auto-sync if enabled
    if (cloudConfig.autoSync && cloudConfig.apiToken && cloudConfig.projectId) {
      return simpleAutoSync(taskId, newStatus, config, t)
    }
    return { skipped: true, reason: "not_hybrid" }
  }

  // Perform hybrid sync
  const result = await performHybridSync(
    { taskId, newStatus },
    config,
    t
  )

  // Handle conflict
  if (!result.success && result.conflict) {
    // Return conflict for UI to display
    return {
      conflict: true,
      conflictData: result.conflict
    }
  }

  // Update lastSyncedAt on success
  if (result.success && (result.action === "push" || result.action === "pull")) {
    await updateLastSyncedAt(new Date().toISOString())
  }

  return result
}
```

---

## Batch Merge (Multiple Tasks)

For syncing multiple tasks at once (e.g., /sync command):

**Pseudo-code:**
```javascript
/**
 * Merge multiple tasks between local and cloud
 * @param {Object} localTasks - Map of taskId -> status from local
 * @param {Object} cloudTasks - Map of taskId -> task object from cloud
 * @param {string} lastSyncedAt - Last sync timestamp
 * @returns {BatchMergeResult} Results for all tasks
 */
function batchMerge(localTasks, cloudTasks, lastSyncedAt) {
  const results = {
    autoMerged: [],    // Tasks that merged automatically
    conflicts: [],      // Tasks with conflicts
    localOnly: [],      // Tasks only in local (new)
    cloudOnly: [],      // Tasks only in cloud (deleted locally?)
    unchanged: []       // Tasks that didn't change
  }

  // Get all unique task IDs
  const allTaskIds = new Set([
    ...Object.keys(localTasks),
    ...Object.keys(cloudTasks)
  ])

  for (const taskId of allTaskIds) {
    const localTask = localTasks[taskId]
    const cloudTask = cloudTasks[taskId]

    // Task only exists locally
    if (localTask && !cloudTask) {
      results.localOnly.push({
        taskId,
        status: localTask.status,
        action: "push"
      })
      continue
    }

    // Task only exists on cloud
    if (!localTask && cloudTask) {
      results.cloudOnly.push({
        taskId,
        status: cloudTask.status,
        action: "pull"
      })
      continue
    }

    // Task exists in both - run smart merge
    const context = buildMergeContext({
      taskId,
      localStatus: localTask.status,
      localUpdatedAt: localTask.updatedAt || new Date().toISOString(),
      cloudStatus: cloudTask.status,
      cloudUpdatedAt: cloudTask.updatedAt,
      cloudUpdatedBy: cloudTask.updatedBy,
      lastSyncedAt,
      baseStatus: cloudTask.status  // Use cloud as base
    })

    const mergeResult = smartMerge(context)

    switch (mergeResult.result) {
      case "NO_CHANGE":
        results.unchanged.push({ taskId })
        break
      case "AUTO_MERGE":
        results.autoMerged.push({
          taskId,
          action: mergeResult.action,
          finalStatus: mergeResult.finalStatus
        })
        break
      case "CONFLICT":
        results.conflicts.push(mergeResult.conflict)
        break
    }
  }

  return results
}
```

### Batch Merge Summary

After batch merge, display summary:

```
🔄 Sync Summary

✅ Auto-merged: 5 tasks
   T1.1: TODO → DONE (pushed)
   T1.2: IN_PROGRESS → DONE (pushed)
   T2.1: TODO → IN_PROGRESS (pulled)
   T2.2: DONE → DONE (no change)
   T3.1: (new task pushed)

⚠️ Conflicts: 2 tasks
   T1.3: Local=DONE, Cloud=BLOCKED
   T2.3: Local=IN_PROGRESS, Cloud=DONE

💡 Run /sync resolve to fix conflicts
```

---

## Edge Cases

### Edge Case 1: First Sync (No lastSyncedAt)

When `lastSyncedAt` is null/undefined, this is the first sync:
- Local takes precedence
- Push all local changes to cloud
- Set lastSyncedAt after success

```javascript
if (!lastSyncedAt) {
  return {
    result: "AUTO_MERGE",
    reason: "first_sync",
    action: "push",
    finalStatus: localStatus
  }
}
```

### Edge Case 2: Task Deleted on One Side

If task exists locally but not on cloud (or vice versa):

```javascript
// Task deleted on cloud
if (localTask && !cloudTask) {
  // Options:
  // 1. Re-create on cloud (push)
  // 2. Delete locally (sync deletion)
  // Default: Push (preserve local work)
  return { action: "push", reason: "recreate_on_cloud" }
}

// Task deleted locally
if (!localTask && cloudTask) {
  // Options:
  // 1. Re-create locally (pull)
  // 2. Delete on cloud (sync deletion)
  // Default: Pull (preserve cloud work)
  return { action: "pull", reason: "recreate_locally" }
}
```

### Edge Case 3: Clock Skew

If local and cloud clocks are out of sync:

```javascript
function compensateClockSkew(localTime, cloudTime, tolerance = 60000) {
  // 1 minute tolerance
  const diff = Math.abs(
    new Date(localTime).getTime() - new Date(cloudTime).getTime()
  )

  if (diff < tolerance) {
    // Times are close enough, treat as simultaneous
    return "simultaneous"
  }

  return new Date(localTime) > new Date(cloudTime) ? "local_newer" : "cloud_newer"
}
```

### Edge Case 4: Rapid Updates

If multiple updates happen quickly (within seconds):

```javascript
const DEBOUNCE_MS = 2000  // 2 seconds

function shouldDebounce(lastUpdateAt) {
  if (!lastUpdateAt) return false
  const elapsed = Date.now() - new Date(lastUpdateAt).getTime()
  return elapsed < DEBOUNCE_MS
}

// In hybrid sync:
if (shouldDebounce(config.cloud.lastSyncedAt)) {
  // Skip cloud sync, will batch on next update
  return { skipped: true, reason: "debounce" }
}
```

### Edge Case 5: Offline Mode

When network is unavailable:

```javascript
async function hybridSyncWithOfflineSupport(params, config, t) {
  try {
    // Try normal hybrid sync
    return await performHybridSync(params, config, t)
  } catch (networkError) {
    // Network unavailable
    console.log(t.commands.update.hybridLocalOnly)

    // Queue for later sync
    await queuePendingSync(params.taskId, params.newStatus)

    return {
      success: true,
      offline: true,
      queued: true
    }
  }
}
```

---

## Configuration

### Storage Mode Options

```json
{
  "cloud": {
    "storageMode": "hybrid",  // "local" | "cloud" | "hybrid"
    "autoSync": true,
    "lastSyncedAt": "2026-02-01T10:00:00Z"
  }
}
```

| Mode | Behavior |
|------|----------|
| `local` | No cloud sync, PROJECT_PLAN.md only |
| `cloud` | Cloud is source of truth, local is cache |
| `hybrid` | Smart merge between local and cloud |

### When Each Mode is Used

```javascript
function getSyncBehavior(config) {
  const mode = config.cloud?.storageMode || "local"

  switch (mode) {
    case "local":
      return {
        pullBeforePush: false,
        autoSync: false,
        smartMerge: false
      }

    case "cloud":
      return {
        pullBeforePush: true,
        autoSync: true,
        smartMerge: false,  // Cloud always wins
        cloudIsAuthority: true
      }

    case "hybrid":
      return {
        pullBeforePush: true,
        autoSync: true,
        smartMerge: true,
        conflictResolution: "interactive"
      }
  }
}
```

---

## Translation Keys

Add these to `locales/en.json` and `locales/ka.json`:

```json
{
  "commands": {
    "update": {
      "hybridSyncing": "🔄 Syncing with cloud (hybrid mode)...",
      "hybridPulling": "   ↓ Pulling cloud state...",
      "hybridPushing": "   ↑ Pushing local changes...",
      "hybridNoConflict": "   ✓ No conflicts detected",
      "hybridAutoMerge": "   ✓ Auto-merged changes",
      "hybridConflict": "   ⚠️ Conflict detected!",
      "hybridTaskNew": "   → Task is new, pushing...",
      "hybridPullFailed": "   ⚠️ Could not fetch cloud state",
      "hybridLocalOnly": "   → Changes saved locally only",
      "hybridSyncSuccess": "☁️ ✅ Synced to cloud (hybrid)",
      "hybridPushFailed": "☁️ ⚠️ Push failed"
    },

    "sync": {
      "mergeTitle": "🔄 Smart Merge Results",
      "autoMerged": "✅ Auto-merged:",
      "conflicts": "⚠️ Conflicts:",
      "unchanged": "No changes:",
      "resolveHint": "💡 Run /sync resolve to fix conflicts"
    }
  },

  "smartMerge": {
    "conflictTitle": "⚠️ Sync Conflict Detected!",
    "taskLabel": "Task:",
    "localVersion": "📍 LOCAL",
    "cloudVersion": "☁️ CLOUD",
    "statusLabel": "Status:",
    "timeLabel": "Time:",
    "authorLabel": "Author:",
    "you": "You",
    "chooseVersion": "Which version to keep?",
    "keepLocal": "Keep local",
    "keepCloud": "Keep cloud",
    "cancel": "Cancel",
    "conflictResolved": "✅ Conflict resolved!",
    "kept": "Kept {version} version"
  }
}
```

---

## Testing Scenarios

### Test 1: Different Tasks Modified (Auto Merge)

```
Setup:
- Local: T1.1 → DONE
- Cloud: T2.1 → IN_PROGRESS

Expected:
- Result: AUTO_MERGE
- Action: Push local T1.1, keep cloud T2.1
- No conflict
```

### Test 2: Same Task, Same Value (Convergent)

```
Setup:
- Local: T1.1 → DONE
- Cloud: T1.1 → DONE

Expected:
- Result: AUTO_MERGE
- Action: Skip (already in sync)
- No conflict
```

### Test 3: Same Task, Different Values (Conflict)

```
Setup:
- Local: T1.1 → DONE
- Cloud: T1.1 → BLOCKED
- Cloud updated after lastSyncedAt

Expected:
- Result: CONFLICT
- Action: Resolve
- Show conflict UI
```

### Test 4: Only Local Changed

```
Setup:
- Local: T1.1 → DONE
- Cloud: T1.1 → TODO (unchanged since lastSyncedAt)

Expected:
- Result: AUTO_MERGE
- Action: Push
- No conflict
```

### Test 5: Only Cloud Changed

```
Setup:
- Local: T1.1 → TODO (unchanged)
- Cloud: T1.1 → DONE (updated after lastSyncedAt)

Expected:
- Result: AUTO_MERGE
- Action: Pull
- Update local
```

### Test 6: First Sync

```
Setup:
- lastSyncedAt: null
- Local: T1.1 → DONE
- Cloud: T1.1 → TODO

Expected:
- Result: AUTO_MERGE
- Reason: first_sync
- Action: Push local
```

---

## Performance Considerations

1. **Single Task Sync**: O(1) - one API call
2. **Batch Sync**: O(n) - one API call to get all tasks, then merge locally
3. **Network Latency**: Use timeouts (5s connect, 10s total)
4. **Debouncing**: Avoid rapid consecutive syncs (2s debounce)

---

## Security Considerations

1. **No token in logs**: Never log API tokens
2. **HTTPS only**: All API communication over HTTPS
3. **Conflict data**: Don't expose sensitive info in conflict details
4. **Local storage**: Tokens stored in config files (standard CLI practice)

---

## Success Criteria

A good smart merge implementation should:
- ✅ Auto-merge non-conflicting changes seamlessly
- ✅ Detect conflicts accurately
- ✅ Provide rich conflict data for UI
- ✅ Never lose user work
- ✅ Handle edge cases gracefully
- ✅ Work offline (queue for later)
- ✅ Be fast (minimal API calls)
- ✅ Support both single-task and batch operations

---

## Important Notes

1. **This is an internal skill** - not user-invocable
2. **Preserve user work** - when in doubt, don't overwrite
3. **Be transparent** - show what's happening during sync
4. **Handle errors gracefully** - local updates should succeed even if cloud fails
5. **Support all storage modes** - local, cloud, and hybrid
6. **Test thoroughly** - merge algorithms are tricky

This skill provides the foundation for intelligent sync in the PlanFlow plugin.
