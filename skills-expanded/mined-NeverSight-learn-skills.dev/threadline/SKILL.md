---
name: threadline
description: >
  Use when the user wants to resume interrupted work, reconstruct context, find buried
  commitments, explain why a file or tab is still open, prepare a handoff, safely clean
  Downloads, list or inspect threads, show activity history, search past work sessions,
  split or merge threads, export/import threads for sharing, or search raw events.
  Requires a running Threadline MCP server.
version: 1.1.0
tools:
  - health
  - list_recent_threads
  - get_thread_details
  - get_thread_timeline
  - resume_last_thread
  - search_threads
  - search_events
  - find_commitments
  - list_projects
  - prepare_handoff
  - safe_clean_downloads
  - explain_why_open
  - open_thread_artifacts
  - capture_checkpoint
  - archive_thread
  - undo_last_cleanup
  - split_thread
  - merge_threads
  - export_thread
  - import_thread
---

# Threadline Skill

Threadline is a local-first work-memory layer. It captures lightweight events from your
filesystem, git repos, clipboard, browser history, Claude Code sessions, Beads memory
files, and task/plan files, clusters them into resumable threads grouped by project,
and exposes them through MCP tools.

**Primary mode: fully inside Claude Code.** Use these tools directly. No external UI needed.

---

## When to trigger

Trigger this skill when the user says or implies:

- "resume", "continue", "pick up where I left off"
- "what was I working on", "what changed", "show my work"
- "show threads", "show history", "show recent work"
- "open this thread", "what is this file about"
- "why is this tab open", "explain this file"
- "find my commitments", "what did I promise", "what's due today"
- "prepare handoff", "summarize my work"
- "clean downloads", "safe cleanup"
- "checkpoint", "save my progress"
- "show projects", "list projects", "what projects", "group by project"
- "search events", "show raw events", "what happened on", "show git commits"
- "split thread", "merge threads", "combine these threads"
- "export thread", "share this thread", "import thread"

---

## Tool usage patterns

### Listing and inspecting threads

```
list_recent_threads → show list to user
get_thread_details(threadId) → show details
get_thread_timeline(threadId) → show timeline
```

### Resuming work

```
resume_last_thread() OR resume_last_thread(query="<keyword>")
→ show summaryCard to user
→ show commitments
→ suggest next actions
```

### Searching

```
search_threads(query="<keyword>") → show matches
find_commitments(query="<keyword>") → show commitments
search_events(source="git", kind="commit", from="2026-03-01") → show raw events
```

### Explaining presence of a file or URL

```
explain_why_open(path="/path/to/file") OR explain_why_open(url="https://...")
→ show explanation
→ show linkedThread if found
```

### Preparing a handoff

```
prepare_handoff(threadId?) OR prepare_handoff(query="<keyword>")
→ format and show the handoff document
```

### Safe cleanup

```
safe_clean_downloads(dryRun=true) → show preview
safe_clean_downloads(dryRun=false) → perform cleanup, show manifest
undo_last_cleanup() → restore files
```

### Projects

```
list_projects() → show all projects with thread counts and open commitments
```

### Checkpoints

```
capture_checkpoint(title="...", note="...") → save checkpoint, extract commitments
```

### Thread management

```
# Split: first show timeline, then split selected events
get_thread_timeline(threadId) → show events to user
split_thread(threadId, eventIds=[...]) → create new thread from events

# Merge two threads into one
merge_threads(targetThreadId, sourceThreadId) → source archived, target updated

# Export / import for sharing or backup
export_thread(threadId) → returns JSON string
import_thread(data="<json>") → creates [imported] thread copy
```

### Health and alerts

```
health() → daemon status, per-collector stats, overdue commitment alerts
```

---

## Response patterns

### Thread list response

```
## Recent Threads

**[ACTIVE]** fix oauth callback in api repo
  Last active: 2h ago | Artifacts: 3 | Commitments: 1
  > 12 events; repos: api; includes git commits; ~2h session

**[STALE]** vendor invoice reconciliation
  Last active: 5d ago | Artifacts: 2 | Commitments: 3
```

### Resume card response

```
## fix oauth callback in api repo
**State:** active | **Last active:** 2h ago

> 12 events across 2 source(s); repos: api; includes git commits

**Recent activity:**
- committed: fix: validate redirect URI
- modified: auth.ts
- tab_opened: OAuth 2.0 documentation

**Open commitments:**
- [ ] Add integration test for callback handler

**Key artifacts:**
- `/projects/api/src/auth.ts` (file)
- `https://oauth.net/2/` (url)
```

### Handoff response

```
## Handoff: fix oauth callback in api repo

**Summary:** This thread covers "fix oauth callback" with 12 recorded events...

**Timeline:** [recent events listed]

**Open commitments:**
- [ ] Add integration test for callback handler

**Next steps:**
- Complete: Add integration test for callback handler
- Review code in /projects/api
```

### Cleanup preview response

```
## Downloads Cleanup Preview

Found 8 candidate files older than 3 days (total: 42 MB):

- invoice-march.pdf (45 days, 200 KB)
- zoom-recording.mp4 (30 days, 50 MB)
...

Run `safe_clean_downloads(dryRun=false)` to move to quarantine.
Files can be restored with `undo_last_cleanup()`.
```

### Commitment report response

```
## Open Commitments

**fix oauth callback** (active)
- [ ] Add integration test for callback handler (confidence: 85%)

**vendor invoices** (stale)
- [ ] Send invoice to accounting by Friday (due: 2024-03-22)
- [ ] Follow up with vendor about dispute
```

### Health response

```
## Threadline Health

Status: ok | Version: 1.0.0 | Schema: v3

Collectors:
- filesystem   ✓ enabled | 128 events | last: 2m ago
- git          ✓ enabled | 44 events  | last: 5m ago
- clipboard    ✓ enabled | 12 events  | last: 1h ago
- browser_ext  ✓ enabled | 87 events  | last: 3m ago

Alerts:
- [ ] Send invoice to accounting — due today
```

---

## Privacy notes

- All data is local. No cloud calls.
- Incognito browser sessions are ignored by default.
- Secrets in clipboard text are redacted before storage.
- Cleanup moves files to quarantine; nothing is permanently deleted.

---

## Prefer in-Claude workflow

When the user asks about threads, history, or context — use the MCP tools and render
the output directly in the conversation. Only mention the local web UI at
`http://127.0.0.1:47821/ui` if the user explicitly asks for a visual overview.
