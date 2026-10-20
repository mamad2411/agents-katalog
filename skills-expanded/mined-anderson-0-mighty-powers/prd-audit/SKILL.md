---
name: prd-audit
description: 'Audit frontend and backend implementation against every PRD file, one by one, using parallel subagents. Produces a full status table (done / partial / not-started), identifies critical-path blockers, and recommends next sprints. Use when you need to know where you stand against your PRDs.'
---

# PRD Audit

Cross-reference every PRD in the project against the actual frontend and backend implementation using parallel subagents, then synthesise a full status report with recommended next sprints.

## Conventions

- Bare paths resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}` resolves from the project working directory.
- `{skill-name}` resolves to `prd-audit`.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `python3 ${CLAUDE_PLUGIN_ROOT}/tools/lib/resolve-customization.py --skill {skill-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/.mighty-powers/custom/{skill-name}.toml` — team overrides
3. `{project-root}/.mighty-powers/custom/{skill-name}.user.toml` — personal overrides

Scalars override; arrays append; arrays-of-tables keyed by `code`/`id` replace matching entries and append new ones.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context for the whole run. Entries prefixed `file:` are paths/globs under `{project-root}` — load the referenced file contents as facts.

### Step 4: Load Config

Load config from `{project-root}/.mighty-powers/config.yaml` and resolve:

- `project_name`, `user_name`
- `communication_language`, `document_output_language`
- `implementation_artifacts`
- `date` as current datetime
- `project_context` = `**/project-context.md` (load if exists)
- ALWAYS SPEAK in `{communication_language}`

### Step 5: Greet the User

Greet `{user_name}` in `{communication_language}`.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete before the main workflow begins.

## Paths

- `prd_dir`      = `{project-root}/{workflow.prd_dir}`
- `frontend_dir` = `{project-root}/{workflow.frontend_dir}`
- `backend_dir`  = `{project-root}/{workflow.backend_dir}`
- `output_file`  = `{implementation_artifacts}/prd-audit.md`

## Execution

<workflow>

<!-- ═══════════════════════════════════════════════════════
     STEP 0 — Discover PRDs and validate configuration
     ═══════════════════════════════════════════════════════ -->
<step n="0" goal="Discover PRD files and validate configuration">
  <action>Check that `{prd_dir}` exists. If it doesn't, output an error and stop:
    > PRD directory not found: {prd_dir}
    > Set `prd_dir` in `.mighty-powers/custom/prd-audit.toml` or ensure your PRDs are in a `prd/` folder at the project root.
  </action>
  <action>Discover PRD files:
    Run: `find {prd_dir} -maxdepth 1 -name "*.md" | sort`
    Filter out index files (files named `00-*.md`, `index.md`, `README.md`).
    Store as: `prd_files` (sorted list of absolute paths).
  </action>
  <action>Count PRDs: `prd_count` = length of `prd_files`.</action>
  <check if="prd_count == 0">
    <output>> No PRD files found in {prd_dir}. Create PRDs with `mp:create-prd` first.</output>
    <action>Exit workflow</action>
  </check>
  <action>Check that `{frontend_dir}` and `{backend_dir}` both exist. Warn (but do not stop) for any that are missing — just mark that layer as "not configured" in the report.</action>
  <action>Announce to user: "Found {prd_count} PRDs in {prd_dir}. Starting parallel audit against {frontend_dir} (frontend) and {backend_dir} (backend)…"</action>
</step>

<!-- ═══════════════════════════════════════════════════════
     STEP 1 — Build and launch the parallel audit workflow
     ═══════════════════════════════════════════════════════ -->
<step n="1" goal="Run parallel PRD audit via Workflow tool">
  <action>Divide `prd_files` into batches of {workflow.batch_size} (default 5). Each batch becomes one subagent.
    Example: 48 PRDs → 10 batches of ~5 each, run concurrently up to the concurrency cap.
  </action>
  <action>
    Launch a Workflow with the following script (substitute actual values for ROOT, BATCHES, BATCH_SIZE, FRONTEND_DIR, BACKEND_DIR, STACK_NOTES):

    ```javascript
    export const meta = {
      name: 'prd-audit-inner',
      description: 'Parallel PRD audit — one subagent per batch, then synthesis',
      phases: [
        { title: 'Audit Batches' },
        { title: 'Synthesize' },
      ],
    }

    // ── Configuration (injected by the skill) ──────────────────────────────
    const ROOT         = '{project-root}'
    const FRONTEND_DIR = '{frontend_dir}'
    const BACKEND_DIR  = '{backend_dir}'
    const STACK_NOTES  = '{workflow.stack_notes}'   // e.g. "React/TS frontend, Go/Wails3 backend"
    const BATCHES      = {BATCHES_JSON}             // array of arrays of absolute PRD paths
    // ──────────────────────────────────────────────────────────────────────

    const PRD_STATUS_SCHEMA = {
      type: 'object',
      properties: {
        prds: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              id:               { type: 'string' },
              title:            { type: 'string' },
              frontend_status:  { type: 'string', enum: ['complete','partial','missing','not-applicable'] },
              frontend_notes:   { type: 'string' },
              backend_status:   { type: 'string', enum: ['complete','partial','missing','not-applicable'] },
              backend_notes:    { type: 'string' },
              overall:          { type: 'string', enum: ['done','in-progress','not-started','not-applicable'] },
              blockers:         { type: 'string' },
            },
            required: ['id','title','frontend_status','frontend_notes','backend_status','backend_notes','overall','blockers'],
          }
        }
      },
      required: ['prds']
    }

    phase('Audit Batches')

    const batchResults = await parallel(BATCHES.map((batch, idx) => () =>
      agent(`
You are auditing a batch of PRDs against a real codebase. Read each PRD file and the
relevant implementation files, then report the implementation status for each PRD.

Stack: ${STACK_NOTES}
Frontend root: ${FRONTEND_DIR}
Backend root:  ${BACKEND_DIR}
Project root:  ${ROOT}

PRDs to audit this batch:
${batch.map(p => `- ${p}`).join('\n')}

For EACH PRD in the batch:
1. Read the PRD file fully (goals, user stories, functional requirements, contract section).
2. Identify the likely frontend components (look in ${FRONTEND_DIR}/components/ or equivalent).
3. Identify the likely backend service files (look in ${BACKEND_DIR} for service, handler, or command files).
4. Read those implementation files. Do NOT skip this step — you must read the actual code.
5. Compare what the PRD requires against what is actually implemented.

Report for each PRD:
- id: numeric string extracted from the filename (e.g. "07" from "07-branching.md")
- title: feature name from the PRD heading
- frontend_status: complete | partial | missing | not-applicable
- frontend_notes: specific components that exist, specific components/features that are absent
- backend_status: complete | partial | missing | not-applicable
- backend_notes: specific files/functions that exist, specific ones that are absent
- overall: done | in-progress | not-started | not-applicable
- blockers: the single most important thing blocking full completion (or "none")
`, {
        label: `batch-${idx + 1}`,
        phase: 'Audit Batches',
        schema: PRD_STATUS_SCHEMA,
      })
    ))

    const allPRDs = batchResults
      .filter(Boolean)
      .flatMap(r => r.prds)
      .sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }))

    phase('Synthesize')

    const statusEmoji = { complete: '✅', partial: '🔶', missing: '❌', 'not-applicable': '⬜' }
    const overallEmoji = { done: '✅', 'in-progress': '🔶', 'not-started': '❌', 'not-applicable': '⬜' }

    const synthesis = await agent(`
You have a full PRD audit of a software project. Produce a comprehensive implementation
status report in Markdown.

Stack: ${STACK_NOTES}

Raw audit data:
${JSON.stringify(allPRDs, null, 2)}

Your report MUST contain these sections in order:

## 1. Executive Summary
3-5 bullet points: overall % complete (frontend separately, backend separately),
what phases are done, what's blocked, a one-line overall verdict.

## 2. PRD Status Table
One row per PRD. Columns: # | Title | Frontend | Backend | Overall | Primary Blocker
Use emoji: ✅ complete · 🔶 partial · ❌ missing · ⬜ N/A

## 3. Fully Done
List every PRD with overall=done. If none, say so explicitly.

## 4. In Progress / Partial
For each PRD with overall=in-progress: a brief bullet naming what exists and what's missing.
Group by theme if there are many (e.g., "Core Git Operations", "GitHub Cloud Features", "AI Features").

## 5. Not Started
List PRDs with overall=not-started. Note if the frontend OR backend layer is present but the other is absent.

## 6. Critical Path
Which 4-6 missing items block the most other PRDs? Be specific:
- Name the missing file / service / integration
- List the PRDs it unblocks
- Why it matters

## 7. Recommended Next Sprints
5 concrete sprint proposals, each with:
- Sprint name and target files/services
- Effort estimate (days)
- PRDs unlocked
- Rationale (ROI justification)

Order by ROI (highest first). Sprint A should be the single highest-leverage action available.

Return the full markdown report.
`, { label: 'synthesis' })

    return { allPRDs, synthesis }
    ```
  </action>

  <action>Wait for the Workflow to complete. Store `{workflow_result.allPRDs}` and `{workflow_result.synthesis}`.</action>
</step>

<!-- ═══════════════════════════════════════════════════════
     STEP 2 — Write and display the report
     ═══════════════════════════════════════════════════════ -->
<step n="2" goal="Write report and display summary">
  <action>
    Write the full synthesis report to `{output_file}`:
    ```
    # PRD Audit Report
    Generated: {date}
    Project: {project_name}
    PRDs audited: {prd_count}
    Frontend: {frontend_dir}
    Backend: {backend_dir}

    {workflow_result.synthesis}
    ```
  </action>
  <action>Display the full report to the user.</action>
  <action>Announce: "Report saved to {output_file}"</action>
</step>

<!-- ═══════════════════════════════════════════════════════
     STEP 3 — Offer follow-up actions
     ═══════════════════════════════════════════════════════ -->
<step n="3" goal="Offer follow-up actions">
  <ask>What would you like to do next?

1) Drill into a specific PRD (enter its number)
2) Start Sprint A (highest-ROI recommended sprint)
3) Generate stories for the critical-path items (`mp:create-story`)
4) Re-run the audit for a specific PRD range only
5) Exit

Choice:</ask>

  <check if="choice == 1">
    <ask>Enter the PRD number (e.g. "07"):</ask>
    <action>Find the matching entry in `{workflow_result.allPRDs}`. Display:
      - Full frontend_notes
      - Full backend_notes
      - Blockers
    Then ask: "Would you like to create a story for this PRD? (y/n)"
    If yes, say: "Run `mp:create-story` and reference PRD {prd_id}."
    </action>
  </check>

  <check if="choice == 2">
    <action>Display the Sprint A recommendation from the synthesis report.
    Say: "Start this sprint with `mp:dev-story` or `mp:quick-dev`."
    </action>
  </check>

  <check if="choice == 3">
    <action>List the critical-path blockers from the synthesis report.
    Say: "Run `mp:create-story` for each blocker. Reference the PRD numbers above when prompted."
    </action>
  </check>

  <check if="choice == 4">
    <ask>Enter PRD range (e.g. "01-10" or "24,25,26"):</ask>
    <action>Filter `prd_files` to the specified range. Re-run Step 1 with only that subset.
    Write a new report section appended to `{output_file}` with heading "## Re-Audit: PRDs {range}".</action>
  </check>

  <check if="choice == 5">
    <action>Run: `python3 ${CLAUDE_PLUGIN_ROOT}/tools/lib/resolve-customization.py --skill {skill-root} --key workflow.on_complete` — if non-empty, follow it as the terminal instruction.</action>
    <action>Exit workflow</action>
  </check>
</step>

</workflow>
