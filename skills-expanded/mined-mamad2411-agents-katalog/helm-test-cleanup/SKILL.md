---
name: helm-test-cleanup
description: "Purge all Helm ADE test data for a repo from Supabase and local filesystem. Use when you need to clean up after testing, reset to a clean state, or purge test data. Triggers on: clean up helm, reset test data, purge test data, helm cleanup, clean slate."
---

# Helm ADE Test Data Cleanup

> Load this skill when: the user wants to clean up test data from Helm ADE after testing. Triggers on: clean up helm, reset test data, purge test data, helm cleanup, clean slate.

## Overview

Purges all Helm ADE test data for a specific repo from both Supabase and local filesystem. Used after manual testing sessions to reset to a clean state.

The default target repo is **FlooringSoft Scheduler** (`mdmagnuson-creator/flooringsoft-scheduler`), which is the standard test repo for Helm development.

**Known UUID**: `d181c9ec-5917-430c-bc18-daaaeaf6c64d` (verify before use — may change if repo is re-registered)

---

## Prerequisites

- **psql**: `/opt/homebrew/opt/libpq/bin/psql` (installed via `brew install libpq`)
- **Supabase CLI**: `supabase` (for credential retrieval via `supabase db dump --linked --dry-run`)
- **Project directory**: `/Users/markmagnuson/code/helm-ade-macos` (must have linked Supabase project)

---

## Quick Run (Copy-Paste)

To purge all FlooringSoft Scheduler test data, run Phase 1 → Phase 2 → Phase 3 below. The app should be **quit first** to avoid stale state.

---

## Phase 1: Kill App & Opencode Processes

```bash
# Kill Debug app
for pid in $(pgrep -f '/Build/Products/Debug/HelmADE.app/' 2>/dev/null); do kill $pid 2>/dev/null; done
WAITED=0; while pgrep -f '/Build/Products/Debug/HelmADE.app/' >/dev/null 2>&1; do if [ $WAITED -ge 30 ]; then for pid in $(pgrep -f '/Build/Products/Debug/HelmADE.app/' 2>/dev/null); do kill -9 $pid 2>/dev/null; done; sleep 1; break; fi; sleep 0.5; WAITED=$((WAITED + 1)); done

# Kill orphaned opencode serve processes
pkill -f "opencode serve" 2>/dev/null || true
```

---

## Phase 2: Purge Supabase Data for Repo

### Connection Setup

> ⚠️ **CRITICAL: The Supabase CLI provides a `cli_login` user, NOT the `postgres` user.**
> This user can connect but has NO direct table permissions.
> You MUST run `SET ROLE postgres;` as the first statement in every psql session.
> Without this, all queries will fail with `permission denied for table`.

```bash
cd /Users/markmagnuson/code/helm-ade-macos
PSQL="/opt/homebrew/opt/libpq/bin/psql"

# Extract ALL connection params from Supabase CLI dry-run output
eval $(supabase db dump --linked --dry-run 2>&1 | grep -E '^export PG(HOST|PORT|USER|PASSWORD|DATABASE)=')

# Verify connection works (SET ROLE is mandatory!)
$PSQL -c "SET ROLE postgres; SELECT count(*) FROM repos;"
```

**Why `SET ROLE postgres`?** The `cli_login_postgres.*` user provided by `supabase db dump --dry-run` authenticates via the Supabase pooler but has no direct table grants. `SET ROLE postgres` assumes the `postgres` role which owns all public tables. This is safe for the linked development database.

**Do NOT use the pooler URL from `supabase/.temp/pooler-url`** — it lacks credentials and uses a different user format that also requires `SET ROLE`.

### Identify Target Repo

```bash
$PSQL -c "SET ROLE postgres; SELECT id, full_name FROM repos WHERE full_name = 'mdmagnuson-creator/flooringsoft-scheduler';"
```

> ⚠️ **Always verify the UUID before running deletes.** The UUID may change if the repo is re-registered.

### Delete Data (Single Transaction, FK-Ordered)

> All deletes run in a single `BEGIN`/`COMMIT` transaction for atomicity.
> If any statement fails, the entire cleanup rolls back — no partial state.

```bash
REPO_ID="d181c9ec-5917-430c-bc18-daaaeaf6c64d"

$PSQL -c "SET ROLE postgres;

BEGIN;

-- =====================================================
-- SESSION CHILDREN (highest volume — delete first)
-- =====================================================

-- Session messages (FK: session_id → sessions.id)
DELETE FROM session_messages WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Session signals (FK: session_id → sessions.id)
DELETE FROM session_signals WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Session todos (FK: session_id → sessions.id)
DELETE FROM session_todos WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Session-task junction (FK: session_id → sessions.id)
DELETE FROM session_tasks WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Session read state (FK: session_id → sessions.id)
DELETE FROM session_read_state WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Session commits (FK: session_id → sessions.id)
DELETE FROM session_commits WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Session exchanges (FK: session_id → sessions.id)
DELETE FROM session_exchanges WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Helm events (FK: session_id → sessions.id)
DELETE FROM helm_events WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Command results (FK: session_id → sessions.id)
DELETE FROM command_results WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
);

-- =====================================================
-- THREAD CHILDREN → THREADS
-- =====================================================

-- Thread checkouts (FK: thread_id → helm_threads.id)
DELETE FROM thread_checkouts WHERE thread_id IN (
  SELECT id FROM helm_threads WHERE repo_id = '$REPO_ID'
);

-- Assistant messages (FK: thread_id → assistant_threads.id, but check if linked via helm_threads)
-- Note: assistant_threads/assistant_messages use their own thread_id, not helm_threads.
-- Only delete if your assistant_threads reference helm_threads (uncommon).

-- Threads (FK: repo_id → repos.id)
DELETE FROM helm_threads WHERE repo_id = '$REPO_ID';

-- =====================================================
-- SESSIONS
-- =====================================================
DELETE FROM sessions WHERE repo_id = '$REPO_ID';

-- =====================================================
-- TASK CHILDREN → TASKS
-- =====================================================

-- Task activity (FK: task_id → tasks.id)
DELETE FROM task_activity WHERE task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
);

-- Task comments (FK: task_id → tasks.id)
DELETE FROM task_comments WHERE task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
);

-- Task attachments (FK: task_id → tasks.id)
DELETE FROM task_attachments WHERE task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
);

-- Task assignees (FK: task_id → tasks.id)
DELETE FROM task_assignees WHERE task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
);

-- Task test runs (FK: task_test_id → task_tests.id)
DELETE FROM task_test_runs WHERE task_test_id IN (
  SELECT id FROM task_tests WHERE task_id IN (
    SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
  )
);

-- Task tests (FK: task_id → tasks.id)
DELETE FROM task_tests WHERE task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
);

-- Test runs (FK: task_id → tasks.id, session_id → sessions.id)
DELETE FROM test_runs WHERE task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
);

-- Task links (columns: source_task_id, target_task_id — NOT task_id/linked_task_id)
DELETE FROM task_links WHERE source_task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
) OR target_task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
);

-- Comment attachments (FK: comment_id → task_comments.id)
-- Clean via task_comments that were already deleted — safe to run before or after
DELETE FROM comment_attachments WHERE comment_id IN (
  SELECT id FROM task_comments WHERE task_id IN (
    SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
  )
);

-- Tasks (FK: repo_id → repos.id)
DELETE FROM tasks WHERE repo_id = '$REPO_ID';

-- =====================================================
-- PRD CHILDREN → PRDs
-- =====================================================

-- PRD stories junction (FK: prd_id → prds.id, story_id → stories.id)
DELETE FROM prd_stories WHERE prd_id IN (
  SELECT id FROM prds WHERE repo_id = '$REPO_ID'
);

-- PRD stories junction (alternate table)
DELETE FROM prd_stories_junction WHERE prd_id IN (
  SELECT id FROM prds WHERE repo_id = '$REPO_ID'
);

-- PRD comments (FK: prd_id → prds.id)
DELETE FROM prd_comments WHERE prd_id IN (
  SELECT id FROM prds WHERE repo_id = '$REPO_ID'
);

-- PRD comment mentions (FK: comment_id → prd_comments.id)
DELETE FROM prd_comment_mentions WHERE comment_id IN (
  SELECT id FROM prd_comments WHERE prd_id IN (
    SELECT id FROM prds WHERE repo_id = '$REPO_ID'
  )
);

-- PRD attachments (FK: prd_id → prds.id)
DELETE FROM prd_attachments WHERE prd_id IN (
  SELECT id FROM prds WHERE repo_id = '$REPO_ID'
);

-- Stories (FK: repo_id → repos.id)
DELETE FROM stories WHERE repo_id = '$REPO_ID';

-- PRDs (FK: repo_id → repos.id)
DELETE FROM prds WHERE repo_id = '$REPO_ID';

-- =====================================================
-- NOTES
-- =====================================================

-- Note attachments (FK: note_id → notes.id)
DELETE FROM note_attachments WHERE note_id IN (
  SELECT id FROM notes WHERE repo_id = '$REPO_ID'
);

-- Notes (FK: repo_id → repos.id)
DELETE FROM notes WHERE repo_id = '$REPO_ID';

-- =====================================================
-- OTHER REPO-SCOPED DATA
-- =====================================================

-- Notification queue (no repo_id — filter via session_id and task_id)
DELETE FROM notification_queue WHERE session_id IN (
  SELECT id FROM sessions WHERE repo_id = '$REPO_ID'
) OR task_id IN (
  SELECT id FROM tasks WHERE repo_id = '$REPO_ID'
);

-- Queued signals (no repo_id — filter via source_session_id which is TEXT, not UUID)
DELETE FROM queued_signals WHERE source_session_id IN (
  SELECT id::text FROM sessions WHERE repo_id = '$REPO_ID'
);

-- Code index state (FK: repo_id → repos.id)
DELETE FROM code_index_state WHERE repo_id = '$REPO_ID';

-- Embeddings (FK: repo_id → repos.id)
DELETE FROM embeddings WHERE repo_id = '$REPO_ID';

-- Sidebar items (FK: repo_id → repos.id)
DELETE FROM sidebar_items WHERE repo_id = '$REPO_ID';

COMMIT;

-- =====================================================
-- VERIFICATION (outside transaction)
-- =====================================================
SELECT 'tasks' AS tbl, count(*) FROM tasks WHERE repo_id = '$REPO_ID'
UNION ALL SELECT 'sessions', count(*) FROM sessions WHERE repo_id = '$REPO_ID'
UNION ALL SELECT 'helm_threads', count(*) FROM helm_threads WHERE repo_id = '$REPO_ID'
UNION ALL SELECT 'prds', count(*) FROM prds WHERE repo_id = '$REPO_ID'
UNION ALL SELECT 'stories', count(*) FROM stories WHERE repo_id = '$REPO_ID'
UNION ALL SELECT 'notes', count(*) FROM notes WHERE repo_id = '$REPO_ID';
"
```

All counts should be 0. If any are non-zero, the transaction was rolled back — check error output above.

---

## Phase 3: Clean Local Filesystem

```bash
BUILD_SUFFIX="-DEV"

# Message cache for sessions (all sessions — can't easily filter by repo)
rm -rf ~/Library/Application\ Support/Helm${BUILD_SUFFIX}/cache/messages/

# Worktrees for flooringsoft-scheduler
rm -rf ~/code/.helm-worktrees-dev/flooringsoft-scheduler/

# Prune git worktree references in the scheduler repo
cd /Users/markmagnuson/code/flooringsoft-scheduler && git worktree prune 2>/dev/null

# Clear chat attachments (all — can't filter by repo)
rm -rf ~/Library/Application\ Support/HelmADE/attachments/

# Clear today's log file (optional — useful if you want a clean log for next test)
# rm -f ~/Library/Application\ Support/Helm${BUILD_SUFFIX}/logs/helm-debug-$(date +%Y-%m-%d).log

# Opencode data (per-org, not per-repo — only clear if testing is single-org)
# rm -rf ~/Library/Application\ Support/Helm${BUILD_SUFFIX}/opencode-data/
```

---

## Phase 4: Rebuild & Relaunch (Optional)

```bash
cd /Users/markmagnuson/code/helm-ade-macos

# Build
xcodebuild -project HelmADE.xcodeproj -scheme HelmADE -destination 'platform=macOS' -configuration Debug -quiet build

# Verify no stale process
pgrep -f '/Build/Products/Debug/HelmADE.app/' >/dev/null 2>&1 && echo 'ERROR: Debug app already running' && exit 1 || true

# Launch (resolve build dir from xcodebuild — NEVER use find in DerivedData)
BUILD_DIR=$(xcodebuild -project HelmADE.xcodeproj -scheme HelmADE -configuration Debug -showBuildSettings 2>/dev/null | grep ' TARGET_BUILD_DIR ' | awk '{print $3}') && open "$BUILD_DIR/HelmADE.app"
```

---

## Cleanup Levels

| Level | What It Does | When to Use |
|-------|-------------|-------------|
| **Phase 2 only** | Purge Supabase data for repo | Quick reset between test runs |
| **Phase 2 + 3** | Supabase + local cache/worktrees | Full test data reset |
| **Phase 1 + 2 + 3 + 4** | Kill → purge → clean → rebuild | Complete clean slate |

---

## What This Does NOT Touch

| Item | Why |
|------|-----|
| `repos` table entry | The repo registration itself is preserved — only data _within_ the repo is deleted |
| `organizations` / `org_members` | Org structure is shared across all repos |
| `devices` / `device_tab_state` / `device_split_state` | Device identity should persist across test resets |
| `repo_clones` | Clone state is device-level, not test data |
| `project_settings` / `project_dashboard_layouts` / `project_dashboard_tabs` | Project configuration is not test data |
| `user_project_preferences` / `user_views` / `workspace_projects` | User preferences should persist (technically repo-scoped, but not test data) |
| `profiles` / `github_accounts` / `user_providers` | User identity data |
| Keychain (GitHub OAuth token) | Auth should persist — re-login is slow |
| `~/Library/Application Support/Helm-DEV/auth/` | Supabase auth tokens should persist |
| Other repos' data | Cleanup is strictly scoped to the target repo UUID |

---

## Complete Table Reference

All 65 public tables in the Helm ADE Supabase schema, grouped by cleanup behavior:

### Cleaned by this skill (repo-scoped test data)

| Table | FK Path to Repo | Cleaned Via |
|-------|----------------|-------------|
| `sessions` | `repo_id` | Direct |
| `session_messages` | `session_id → sessions` | Join |
| `session_signals` | `session_id → sessions` | Join |
| `session_todos` | `session_id → sessions` | Join |
| `session_tasks` | `session_id → sessions` | Join |
| `session_read_state` | `session_id → sessions` | Join |
| `session_commits` | `session_id → sessions` | Join |
| `session_exchanges` | `session_id → sessions` | Join |
| `helm_events` | `session_id → sessions` | Join |
| `command_results` | `session_id → sessions` | Join |
| `helm_threads` | `repo_id` | Direct |
| `thread_checkouts` | `thread_id → helm_threads` | Join |
| `tasks` | `repo_id` | Direct |
| `task_activity` | `task_id → tasks` | Join |
| `task_comments` | `task_id → tasks` | Join |
| `task_attachments` | `task_id → tasks` | Join |
| `task_assignees` | `task_id → tasks` | Join |
| `task_tests` | `task_id → tasks` | Join |
| `task_test_runs` | `task_test_id → task_tests` | Join (2-level) |
| `task_links` | `source_task_id / target_task_id → tasks` | Join |
| `test_runs` | `task_id → tasks` | Join |
| `comment_attachments` | `comment_id → task_comments` | Join (2-level) |
| `prds` | `repo_id` | Direct |
| `prd_stories` | `prd_id → prds` | Join |
| `prd_stories_junction` | `prd_id → prds` | Join |
| `prd_comments` | `prd_id → prds` | Join |
| `prd_comment_mentions` | `comment_id → prd_comments` | Join (2-level) |
| `prd_attachments` | `prd_id → prds` | Join |
| `stories` | `repo_id` | Direct |
| `notes` | `repo_id` | Direct |
| `note_attachments` | `note_id → notes` | Join |
| `notification_queue` | `session_id / task_id` | Join (no repo_id) |
| `queued_signals` | `source_session_id (TEXT)` | Join with cast |
| `code_index_state` | `repo_id` | Direct |
| `embeddings` | `repo_id` | Direct |
| `sidebar_items` | `repo_id` | Direct |

### NOT cleaned (preserved across resets)

| Table | Why Preserved |
|-------|---------------|
| `repos` | Repo registration itself |
| `organizations` | Shared org structure |
| `org_members` | Org membership |
| `org_providers` / `org_provider_routing` | Org-level config |
| `profiles` | User identity |
| `github_accounts` | GitHub OAuth |
| `user_providers` | Auth providers |
| `devices` | Device identity |
| `device_tab_state` / `device_split_state` | Device UI state |
| `repo_clones` | Clone state (device-level) |
| `project_settings` | Project config |
| `project_dashboard_layouts` / `project_dashboard_tabs` | Dashboard config |
| `project_actions` | Project action config |
| `user_project_preferences` | User prefs (repo-scoped but not test data) |
| `user_views` | User views (repo-scoped but not test data) |
| `user_dashboard_widgets` | Dashboard widgets |
| `user_device_preferences` | Device prefs |
| `workspace_projects` / `workspaces` | Workspace config |
| `assistant_threads` / `assistant_messages` | AI assistant threads (separate from sessions) |
| `checkouts` | Checkout state |
| `command_queue` | Pending commands |
| `comment_mentions` | Task comment mentions (cleaned implicitly with task_comments) |
| `push_log` | Push notification log |
| `reminders` | User reminders |

---

## Schema Gotchas

These caused errors during the initial skill creation (2026-04-12) — documented to prevent repeats:

| Issue | Details |
|-------|---------|
| `task_links` columns | Uses `source_task_id` and `target_task_id` — NOT `task_id` / `linked_task_id` |
| `notification_queue` has no `repo_id` | Filter via `session_id` and `task_id` columns |
| `queued_signals` has no `repo_id` | Filter via `source_session_id` which is `TEXT` type, not `UUID` — requires `::text` cast on the subquery |
| `labels` table | Does NOT exist (as of 2026-04-12) |
| `task_labels` table | Does NOT exist (as of 2026-04-12) |
| `comment_attachments` → `task_comments` | 2-level join: `comment_id → task_comments.id`, then `task_id → tasks.id` |
| `prd_comment_mentions` → `prd_comments` | 2-level join: `comment_id → prd_comments.id`, then `prd_id → prds.id` |

---

## Customizing for a Different Repo

Replace the `REPO_ID` variable with the UUID of the target repo. Find it via:

```bash
$PSQL -c "SET ROLE postgres; SELECT id, full_name FROM repos ORDER BY full_name;"
```

Or from Helm command logs:
```bash
grep "repoFullName" ~/Library/Application\ Support/Helm-DEV/logs/helm-debug-$(date +%Y-%m-%d).log | tail -5
```
