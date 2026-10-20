---
name: builder-dashboard
description: "Dashboard rendering templates for Builder sessions. Covers resume dashboard, fresh dashboard, vectorization status logic, and dashboard section descriptions."
---

# Builder Dashboard Skill

> Load this skill when rendering the startup dashboard (fresh or resume).

## Resume Dashboard

If a `session.json` exists with work in progress (in `docs/sessions/current/`), show options without auto-starting the PRD:

```
═══════════════════════════════════════════════════════════════════════
                    [PROJECT NAME] - BUILDER STATUS
═══════════════════════════════════════════════════════════════════════
⚠️  RESUMING PREVIOUS SESSION (last active: 15 min ago)

VECTORIZATION
───────────────────────────────────────────────────────────────────────
  🟢 Enabled | 8,453 chunks | Updated 2 hours ago
  [Or other status per Vectorization Status Logic]

IN-PROGRESS PRD
───────────────────────────────────────────────────────────────────────
  PRD: print-templates (feature/print-templates)
  Progress: 2/5 stories complete
  Current: US-003 - Add print preview modal
  
  [R] Resume PRD
  [X] Restart this PRD from story 1 (recovery)

OTHER OPTIONS
───────────────────────────────────────────────────────────────────────
  [P] Pick a different ready PRD
  [U] Review pending project updates
  [A] Switch to ad-hoc mode

PENDING AD-HOC WORK (if exists)
───────────────────────────────────────────────────────────────────────
  ✅ adhoc-001: Fix footer alignment (completed, needs E2E tests)
  🔨 adhoc-002: Add loading spinner (in progress)
  
  [C] Continue working    [T] Run E2E tests    [D] Discard

> _
═══════════════════════════════════════════════════════════════════════
```

---

## Fresh Dashboard

If no WIP or user chose fresh start:

```
═══════════════════════════════════════════════════════════════════════
                    [PROJECT NAME] - BUILDER
═══════════════════════════════════════════════════════════════════════

VECTORIZATION
───────────────────────────────────────────────────────────────────────
  [Show one of these based on state:]
  
  🟢 Enabled | 8,453 chunks | Updated 2 hours ago
  
  [Or if disabled:]
  ⚪ Not enabled — run 'vectorize init' to enable semantic search
  
  [Or if stale (user chose Skip):]
  🟡 Enabled | 8,453 chunks | ⚠️ Stale (updated 3 days ago)
  
  [Or if missing index:]
  🔴 Enabled but index missing — run 'vectorize init'
  
  [Or if disabled for session:]
  ⚫ Disabled for this session

───────────────────────────────────────────────────────────────────────

READY PRDs
───────────────────────────────────────────────────────────────────────
  1. prd-error-logging (4 stories)
  2. prd-export-csv (2 stories)
  3. prd-notifications (6 stories)

COMPLETED PRDs (recent)
───────────────────────────────────────────────────────────────────────
  ✅ prd-customers-addresses

[If pending updates exist:]
⚠️ 2 pending project updates — type "U" to review

═══════════════════════════════════════════════════════════════════════
[P] PRD Mode    [A] Ad-hoc Mode    [S] Status

> _
═══════════════════════════════════════════════════════════════════════
```

## Dashboard Sections

- **Vectorization** — Shows semantic search status: enabled/disabled, chunk count, index age
- **Ready PRDs** — PRDs with `status: "ready"` from `prd-registry.json`
- **Completed PRDs** — Recent PRDs with `status: "completed"` (for context)
- **Pending updates** — If `project-updates/[project-id]/` has files

> 💡 **Dashboard only needs these prd-registry fields:** `id`, `name`, `status`, `estimatedStories`
>
> Use: `jq '[.prds[] | {id, name, status, estimatedStories}]' docs/prd-registry.json`
> This reduces a 50KB file to ~2KB of dashboard-relevant data.

## Vectorization Status Logic

Read status from multiple sources and display appropriately:

```
1. Check session memory for `vectorizationDisabledForSession`
   → If true: "⚫ Disabled for this session"

2. Check `project.json` → `vectorization.enabled`
   → If false/missing: "⚪ Not enabled — run 'vectorize init' to enable semantic search"

3. Check `.vectorindex/metadata.json` exists
   → If missing: "🔴 Enabled but index missing — run 'vectorize init'"

4. Read metadata.json → lastUpdated, chunkCount
   → Calculate age from lastUpdated
   → If age > 24h AND session has `vectorizationStaleAcknowledged`:
     "🟡 Enabled | {chunkCount} chunks | ⚠️ Stale (updated {age} ago)"
   → If age <= 24h:
     "🟢 Enabled | {chunkCount} chunks | Updated {age} ago"
```
