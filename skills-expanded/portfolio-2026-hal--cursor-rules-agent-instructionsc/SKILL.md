---
description: PM agent instructions; HAL API usage; move ticket to Ready for QA
alwaysApply: true
---

# Agent Instructions (Local)

Instructions are loaded from `.cursor/rules` and `docs/`. See `docs/process/hal-tool-call-contract.mdc` for HAL API endpoints.

## API-only Data Access (ALL Agents)

**MANDATORY:** Agents must **never** call the database directly (no direct Supabase client usage, no `@supabase/supabase-js`, no `SUPABASE_*` env vars in agent runtime).

- **All ticket operations** (create/update/move/list/get) must go through HAL endpoints under `/api/tickets/*`.
- **All artifact operations** must go through HAL endpoints under `/api/artifacts/*`.
- HAL server endpoints use **server-side privileged Supabase credentials** (e.g. `SUPABASE_SECRET_KEY` / service role) to bypass RLS safely.

## Pre-Commit Build Verification

**MANDATORY:** Before committing ANY code changes, ALL agents **MUST** verify the build succeeds:

1. **Install dependencies (if not already done):**
   ```bash
   npm install
   ```

2. **Verify TypeScript compilation:**
   ```bash
   npx tsc -b --noEmit
   ```
   
   This must pass with zero errors. If it fails, fix all TypeScript errors before committing.

3. **Verify full build (if making changes that affect build):**
   ```bash
   npm run build:hal
   ```
   
   **Note:** `npm run build:hal` may fail due to vite 6.x scanning node_modules during config loading (pre-existing issue). If this happens, verify TypeScript compilation succeeds instead:
   ```bash
   npx tsc -b --noEmit
   ```
   
   If TypeScript compilation fails, you **MUST** fix the errors before committing. Do not commit code that breaks TypeScript compilation.

4. **For specific projects:**
   ```bash
   cd projects/kanban && npx tsc --noEmit  # Check kanban project specifically
   ```

**CRITICAL RULES:**
- **NEVER commit code without running `npx tsc -b --noEmit` first**
- **NEVER commit code that causes `npm run build:hal` to fail**
- **If build fails, fix it before committing - do not leave broken builds for others to discover**
- This applies to ALL agents (implementation, QA, PM) when making code changes

**This check prevents build failures in CI/CD and ensures code quality.**

## Moving Tickets After Implementation

**MANDATORY:** After implementation, the implementation agent **MUST** automatically move the ticket to **Ready for QA** before sending a completion summary. **DO NOT wait for user interaction or ask for permission - just move it.**

**Move ticket to Ready for QA (AUTOMATIC - NO USER INTERACTION REQUIRED):**
```javascript
const baseUrl = (await readFile('.hal/api-base-url', 'utf8')).trim()
const res = await fetch(`${baseUrl}/api/tickets/move`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ ticketId: '0167', columnId: 'col-qa' }),
})
const result = await res.json()
if (!result.success) {
  // If missing artifacts, store them and retry
  if (result.missingArtifacts && Array.isArray(result.missingArtifacts)) {
    // Store missing artifacts, then retry move
    // (implementation details in error handling below)
  } else {
    throw new Error(`Failed to move ticket: ${result.error}`)
  }
}
```

**When to move (AUTOMATIC WORKFLOW - NO USER INTERACTION):**
1. ✅ After all code changes are committed and pushed
2. ✅ After all 8 required artifacts are stored (plan, worklog, changed-files, decisions, verification, pm-review, git-diff, instructions-used)
3. ✅ **Automatically call get_artifacts** (or POST /api/artifacts/get) and confirm all 8 required implementation artifacts are present with substantive content
4. ✅ **AUTOMATICALLY MOVE THE TICKET TO READY FOR QA** (use the API call above) - **DO THIS AUTOMATICALLY, DO NOT ASK USER**
5. ✅ **THEN** send your final "implementation complete" summary message

**Error Handling for Ticket Move:**
- **If move returns success: false with missingArtifacts:** Automatically store each listed artifact via POST /api/artifacts/insert-implementation with the corresponding artifactType, then automatically retry POST /api/tickets/move. The move API will not allow moving to Ready for QA until all 8 artifacts are present.
- **If move fails for other reasons:** Log the error, but **STILL ATTEMPT TO MOVE**. The system is designed to handle failures gracefully. Do not block completion - move the ticket and note any issues in your summary.

**CRITICAL WORKFLOW RULES:** 
- **ALWAYS move the ticket automatically** - never ask the user for permission or wait for confirmation
- **DO NOT** send a completion summary or "done" message without first moving the ticket to Ready for QA
- **DO NOT** mark the ticket as complete in your message if you haven't moved it
- The ticket move is **part of the completion workflow**, not an optional step
- **If the move fails, retry automatically** - do not give up after one failure
- **The system is designed to handle failures** - if a move fails, it's okay, just note it and move on

**Available column IDs:**
- `col-unassigned` - Unassigned
- `col-todo` - To-do
- `col-doing` - Doing (Active Work)
- `col-qa` - Ready for QA
- `col-human-in-the-loop` - Human in the Loop
- `col-process-review` - Process Review
- `col-done` - Done
- `col-wont-implement` - Will Not Implement

**Note:** The HAL API endpoint `/api/tickets/move` uses server-side Supabase credentials, so agents don't need to provide credentials in the request body. The API uses the ticket's primary key (pk) for updates to ensure reliable ticket movement regardless of the ticket ID format provided.

## QA Notes in Completion Summary

**MANDATORY:** All final completion summaries from **Implementation agents** and **Project Manager agents** **MUST** include a **QA Notes** section that maps each Acceptance Criteria to a concrete UI verification location.

### Requirements

1. **Enumerate each Acceptance Criteria** — The QA Notes section must list **every single AC** from the ticket.

2. **Provide exact UI location/route** — For each AC, specify:
   - The exact UI route/path where the AC can be verified (e.g., `/settings`, `/tickets/HAL-0841`, `/kanban`)
   - Any relevant UI labels, buttons, or elements that demonstrate the AC is met (e.g., "Settings page → 'Dark mode' toggle switch", "Ticket detail page → 'Status' field shows 'Ready for QA'")
   - Clear navigation steps if needed (e.g., "Navigate to Settings → Appearance section → Verify 'Dark mode' toggle is visible")

3. **Mark non-UI-verifiable ACs as Blocked** — If any AC cannot be verified in the UI (e.g., requires terminal access, database inspection, or code review), the agent **MUST**:
   - Mark that AC as **Blocked** in the QA Notes section
   - **NOT** claim the ticket is complete if any AC is Blocked
   - Either move the ticket to an appropriate column (e.g., "To-do" if work remains) or create a follow-up ticket to address the non-UI-verifiable requirement

**CRITICAL:** If any AC is marked as **Blocked** (not UI-verifiable), the ticket **CANNOT** be marked complete or moved to "Ready for QA". The agent must either:
- Update the AC to be UI-verifiable, OR
- Document why the AC cannot be UI-verifiable and move the ticket to an appropriate status (e.g., "Will Not Implement" if the AC is intentionally non-UI-verifiable)

### QA Notes Section Format

The QA Notes section must appear in the **final completion summary** (the "done" message sent to the user). It should follow this format:

```markdown
## QA Notes

### AC 1: "[Full text of AC 1]"
- **UI Location:** `/settings` → Appearance section
- **Verification:** Navigate to Settings page, scroll to Appearance section, verify "Dark mode" toggle switch is visible and clickable
- **Status:** ✅ UI-verifiable

### AC 2: "[Full text of AC 2]"
- **UI Location:** `/tickets/HAL-0841` → Ticket detail page
- **Verification:** Open ticket HAL-0841, verify "Status" field displays "Ready for QA"
- **Status:** ✅ UI-verifiable

### AC 3: "[Full text of AC 3]"
- **UI Location:** N/A (requires database inspection)
- **Verification:** Cannot be verified in UI - requires direct database access
- **Status:** ⚠️ Blocked (not UI-verifiable)
```

### Example: Complete Final Summary with QA Notes

```markdown
## Summary

Implemented dark mode toggle feature with persistence. Added toggle switch to Settings page, implemented theme switching logic, and stored preference in localStorage.

## Key Decisions

- Used localStorage for persistence to avoid backend changes
- Implemented theme switching via CSS variables for performance

## QA Notes

### AC 1: "Settings page displays a 'Dark mode' toggle switch that is clearly visible and clickable"
- **UI Location:** `/settings` → Appearance section
- **Verification:** Navigate to Settings page, scroll to Appearance section, verify "Dark mode" toggle switch is visible and clickable
- **Status:** ✅ UI-verifiable

### AC 2: "Clicking the toggle immediately changes the app theme from light to dark (or vice versa) with a smooth transition"
- **UI Location:** `/settings` → Appearance section → "Dark mode" toggle
- **Verification:** Click the "Dark mode" toggle, observe entire app UI transitions from light to dark theme (or vice versa) with smooth animation
- **Status:** ✅ UI-verifiable

### AC 3: "The selected theme preference persists after page refresh (the toggle state matches the current theme on reload)"
- **UI Location:** `/settings` → Appearance section → "Dark mode" toggle
- **Verification:** Set theme to dark mode, refresh page (F5 or Cmd+R), verify page reloads with dark theme and toggle switch is in "on" position
- **Status:** ✅ UI-verifiable

Ticket HAL-0841 implementation completed and moved to QA.
```

### Integration with AC Confirmation Checklist

The QA Notes section **complements** the AC Confirmation Checklist (see `.cursor/rules/ac-confirmation-checklist.mdc`). Both sections should appear in the final completion summary:

- **AC Confirmation Checklist** — Enumerates each AC with "Met" / "Not met" status and evidence (file paths, artifacts, etc.)
- **QA Notes** — Maps each AC to exact UI location/route for human verification

Together, these sections ensure that:
1. All ACs are explicitly addressed (AC Confirmation Checklist)
2. All ACs can be verified in the UI (QA Notes)
3. Reviewers can quickly verify completion without terminal access (QA Notes)

### Scope

- **Applies to:** Implementation agents, Project Manager agents
- **Applies when:** Before sending final completion summary (after moving ticket to "Ready for QA" or final status)
- **Mandatory:** Yes - this is a required section in completion summaries, not optional
- **Location:** Must appear in the final chat completion summary message
