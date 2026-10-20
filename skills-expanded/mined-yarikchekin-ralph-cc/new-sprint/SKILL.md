---
name: new-sprint
description: Generate the next sprint from the PRD, backlog, tech debt, or GitHub Issues — detects completed features, picks the next chunk of work, and builds user stories with minimal user input
---

# /new-sprint — Generate Next Sprint

Creates a new `scripts/ralph/prd.json` by reading the PRD, backlog, tech debt, and (when `Github.enabled`) open GitHub Issues, detecting what's already been built. The user should only need to confirm or tweak — not describe features from scratch.

## Gate

Before anything else, check that `RALPH.md` exists in the project root and has `Documents.prd` defined with a non-empty path.

- **If RALPH.md is missing:** Stop immediately. Tell the user:
  > "No RALPH.md found. Run `/ralph-init` to set up ralph in this project."
- **If Documents.prd is missing or empty:** Stop immediately. Tell the user:
  > "No PRD found. Run `/prd-plan` to create one."
- **If the PRD file itself doesn't exist at the configured path:** Stop immediately. Tell the user:
  > "PRD file not found at `[path]`. Run `/prd-plan` to create one, or update the path in RALPH.md."

Once validated, read all paths from RALPH.md and capture settings:

- `Audit.mode` — `off | sprint-close | per-story` (default `sprint-close`)
- `Github.enabled` — `true | false` (default `false`)

Proceed.

---

## Step 1: Detect What's Been Built

Silently read all of these:

1. **PRD** (from RALPH.md Documents.prd) — the full product requirements document
2. **Backlog** (from RALPH.md Documents.backlog, if exists) — planned improvements with Status fields
3. **Tech debt** (from RALPH.md Documents.tech_debt, if exists) — tracked tech debt items with severity and effort
4. **Ideas** (from RALPH.md Documents.ideas, if exists) — idea backlog
5. **GitHub Issues** (only if `Github.enabled`): run
   ```bash
   gh issue list --state open --label "enhancement" --json number,title,body,labels,createdAt --limit 50
   gh issue list --state open --label "bug" --json number,title,body,labels,createdAt --limit 50
   gh issue list --state open --label "tech-debt" --json number,title,body,labels,createdAt --limit 50
   ```
   If `gh` is not installed or auth fails, warn the user once and continue without GitHub data.
6. **Archived sprints** — list all directories in `scripts/ralph/archive/` to see completed features
7. `scripts/ralph/prd.json` — current sprint (may be complete or in-progress)
8. `scripts/ralph/progress.txt` — the "Codebase Patterns" section at the top for implementation context
9. `CLAUDE.md` — tech stack, project structure, key patterns (if exists)
10. `AGENTS.md` — codebase conventions (if exists)
11. The design doc from RALPH.md Documents.design (if configured) — UI/UX guidelines

Build a mental map of all sources:

**PRD features:**

Parse the PRD for feature sections dynamically. Look for `## N.` or `### N.N` headings under the Features section. Each numbered feature section is a potential sprint source.

| PRD Section | Feature | Sprint Status |
|-------------|---------|---------------|
| [N.1] | [Feature name] | Check archive for matching sprint IDs |
| [N.2] | [Feature name] | Check archive/current |
| ... | ... | ... |

**Backlog items:**

If the backlog file exists, parse each section heading. Check the `**Status:**` field — items that say "Complete" or "Done" are finished. Everything else is available.

**Tech debt:**

If the tech debt file exists, parse the active items. Each typically has an ID (TD-NNN), severity (High/Medium/Low), and effort (Trivial/Small/Medium/Large). Items in "Resolved Items" are already fixed.

**GitHub Issues** (when `Github.enabled`):

| Type | # | Title | Priority | Source label |
|------|---|-------|----------|--------------|
| bug | #N | ... | P0/P1/P2 | user-feedback / agent-audit |
| enhancement | #N | ... | P0/P1/P2 | ... |
| tech-debt | #N | ... | P0/P1/P2 | ... |

Deduplicate GitHub tech-debt issues against the local tech debt file.

---

## Step 2: Identify the Next Sprint

Present all sources to the user. Show what's available from each:

```
## Sprint Sources

### PRD Features
- Completed: [list completed features]
- In Progress: [current sprint feature, if any]
- Next up: **[Section N.N: Feature Name]** (or "All v1 features complete")
- Later: [features marked as "later" or post-v1, if any]

### Backlog
[If no backlog file or empty: "No backlog items" and skip.]
- Completed: [list completed items]
- Available: [list items where Status != Complete/Done]

### Tech Debt
[If no active items: "No active tech debt" and skip.]
- **Can fold into next sprint** (Trivial/Small): [list TD-IDs + titles]
- **Could be its own sprint** (Medium/Large): [list TD-IDs + titles, with severity noted]

### GitHub Issues (when Github.enabled)
- P0: [list any P0-critical items]
- P1: [list P1-important items]
- P2: [list P2-nice-to-have items]
```

### Priority Recommendations

1. **Any v1/MVP feature in the PRD that's incomplete** (highest priority)
2. **P0 bugs and high-severity tech debt** (launch-blocking)
3. **High-priority items from the backlog or GitHub Issues**
4. **Medium/Large effort tech debt items** (warrant their own sprint)
5. **Other backlog items**
6. **User can always override**

Trivial/Small tech debt items don't get their own sprint option — they're noted as things that can be folded into whatever sprint is selected.

Present options to the user with the recommendation:

- **[PRD Feature Name]** — next PRD feature (Recommended if v1 features remain)
- **[Backlog Item: Title]** — from the backlog doc
- **[GitHub Issue #N: Title]** — from the GitHub backlog (when Github.enabled)
- **[Tech Debt: TD-NNN Title]** — only for Medium/Large effort items
- **Something else** — let user specify

**Multiple issues as one sprint:** the user might want to combine related GitHub Issues into a single sprint (e.g., "fix all P1 bugs" or "do enhancement #12 and #15 together"). Support this — `sourceIssues` can list multiple numbers.

Ask: "Which one should we sprint on?"

---

## Step 3: Archive Current Sprint

If `scripts/ralph/prd.json` exists and has stories:

1. Count completed vs total stories
2. **If incomplete stories remain**, warn the user:
   > "This sprint has [N] incomplete stories out of [total]. Archive anyway?"

   Wait for confirmation. If declined, stop — they may want to finish the current sprint first.

3. **If confirmed or all stories are complete**, archive:

   ```bash
   DATE=$(date +%Y-%m-%d)
   FEATURE=$(echo "[branchName from prd.json]" | sed 's|^[^/]*/||')
   ARCHIVE_DIR="scripts/ralph/archive/$DATE-$FEATURE"
   if [ -d "$ARCHIVE_DIR" ]; then
     COUNTER=2
     while [ -d "${ARCHIVE_DIR}-${COUNTER}" ]; do
       COUNTER=$((COUNTER + 1))
     done
     ARCHIVE_DIR="${ARCHIVE_DIR}-${COUNTER}"
   fi
   mkdir -p "$ARCHIVE_DIR"
   cp scripts/ralph/prd.json "$ARCHIVE_DIR/"
   cp scripts/ralph/progress.txt "$ARCHIVE_DIR/"
   ```

4. After archiving, reset `progress.txt` with a fresh header (preserve the Codebase Patterns section from the old progress.txt at the top — those patterns carry forward).

---

## Step 4: Generate Stories

Based on the selected source, extract the details needed to write stories.

### From PRD Section

Read the specific PRD feature section in detail. Extract:
- **Requirements** listed in the section (FR-X.Y.Z items)
- **Data models** from the Data Model section
- **User flows** or interaction descriptions
- **UI specs** from the design doc (if configured)
- **API integrations** or external services mentioned

### From Backlog Item

Read the specific backlog item. Extract:
- **Problem** — what's wrong and why it matters
- **Decided Approach** — the implementation plan (if documented)
- **What Remains** — concrete work items
- **PRD Sections Affected** — for cross-referencing requirements

### From GitHub Issue (when Github.enabled)

Read the full issue with `gh issue view [NUMBER]`. Extract:
- **Problem** — what's wrong or missing
- **Decided Approach / Recommendation** — implementation plan from the body
- **Checklist items** — if the issue has a "What Remains" checklist, use those as story seeds
- **Priority** — from the issue labels

### From Tech Debt Item

Read the specific tech debt item (from `docs/tech-debt.md` or from a GitHub Issue labeled `tech-debt`). Extract description, severity/effort, affected files, fix approach.

### Common to All Sources

Also read:
- `progress.txt` Codebase Patterns section
- Existing codebase structure

**Before writing stories**, explore the codebase to understand current patterns relevant to the sprint. Use Grep/Glob/Read to find files that will be created or modified, existing patterns to follow, dependencies between components.

### Folding in Trivial/Small Tech Debt

If there are Trivial or Small effort tech debt items that relate to the sprint feature area, fold them into the sprint as additional stories or extra acceptance criteria. Mention this to the user.

### Story Generation Rules

1. **Order by dependency**: DB schema/migrations first → backend logic/utilities → UI components → screens/pages → integration/polish
2. **One context window per story**: completable in ~30-60 minutes by the agent
3. **Acceptance criteria from source**: pull specific requirements directly — don't invent
4. **Quality command in every story**: include the relevant quality check from RALPH.md (e.g., "Typecheck passes") as one AC in every story
5. **testFlow only if E2E configured**: if RALPH.md has `e2e_single`, set `testFlow` for stories that create new screens or user-facing flows; `null` for backend-only stories or refactors. If `e2e_single` is not configured, always set `testFlow` to `null`.
6. **5-8 stories per sprint**: if a feature would need more, consider splitting
7. **Story notes reference the codebase**: specific file paths, existing patterns to follow, implementation hints. Never write generic notes.
8. **ID prefix**: short, memorable abbreviation derived from the feature name (3-6 chars)
9. **Branch name**: `[branch_prefix from RALPH.md][kebab-case-feature-name]`
10. **No story depends on a later story**: reorder if necessary

### Acceptance Criteria — object form (v2)

Acceptance criteria are objects: `{ "text": string, "humanGated"?: boolean }`. Legacy string-form ACs are still accepted (treated as `humanGated: false`), but **always emit the object form for new sprints**.

**When to set `humanGated: true`:** ACs the auditor cannot verify alone — the operator must take action on a system the coding agent can't reach. Examples:

- Operator confirms an OTA update reached a TestFlight / Android device
- Operator updates a third-party dashboard (CDN, auth provider, app store)
- Operator enables a capability in a third-party portal
- Operator verifies real-device gesture/haptic feel that automated tests can't capture
- Operator provides a tap/swipe verification that the E2E framework can't
- Operator runs a local-only command (mobile build, dev-only tool)

When the auditor encounters these ACs it will (a) audit every non-humanGated AC immediately, (b) mark the humanGated ones `PENDING (human-gated)`, (c) verdict becomes `PASS-PENDING-HUMAN`. The lead surfaces the exact AC text and waits for confirmation before flipping `passes: true`.

**Default to `humanGated: false`.** Only set `true` when the AC genuinely cannot be verified without the human. Code-verifiable ACs (typecheck, lint, test, file presence, exact text in source) are NOT humanGated even if you mention "verify in browser" — E2E flows handle UI verification.

### Wrap timing — decided live, not authored

Do **not** emit a `wrapPoints` array. Wrap timing is no longer planned at PRD-authoring time — story-clustering was a guess at future context burn. `/start` decides **live, in-process**: before each next story it runs `/ctx` and wraps based on the actual context % (nudge at 40%, strongly recommended at 60%). This measures real burn instead of predicting it. See `skills/start/SKILL.md` step 10.

### Story Structure

```json
{
  "id": "PREFIX-NNN",
  "title": "Concise imperative title",
  "description": "What needs to happen and why",
  "acceptanceCriteria": [
    { "text": "Specific, testable criterion from source doc" },
    { "text": "Another criterion" },
    { "text": "Typecheck passes" },
    { "text": "Operator confirms behavior on a real device", "humanGated": true }
  ],
  "priority": 1,
  "passes": false,
  "testFlow": "path/to/test.yaml or null",
  "notes": "Implementation hints referencing existing patterns and specific file paths"
}
```

### prd.json Structure

```json
{
  "project": "[Project Name from RALPH.md]",
  "source": "prd",
  "sourceItem": "3.1",
  "sourceIssues": [42, 45],
  "branchName": "ralph/feature-name",
  "description": "Feature description — what this sprint delivers",
  "userStories": [
    { "...story objects..." }
  ]
}
```

**Source field values by sprint type:**

| Sprint source | `source` value | `sourceItem` value | `sourceIssues` |
|---------------|----------------|--------------------|----------------|
| PRD feature section | `"prd"` | Section number as string (e.g., `"3.1"`) | omit or empty |
| Backlog item | `"backlog"` | Item number as integer | omit or empty |
| Tech debt item | `"tech-debt"` | Tech debt ID as string (e.g., `"TD-003"`) | optionally `[N]` if also tracked as a GitHub Issue |
| GitHub Issue | `"github-issue"` | omit | array of issue numbers (`[42]` or `[42, 45]`) |

The completion flow (`/start` Case D / D2) uses `sourceItem` to mark backlog/tech-debt items complete, and `sourceIssues` to close GitHub Issues (verifying `Fixes #N` auto-close first, then closing the rest manually).

---

## Step 5: Auditor PRD review (gated by Audit.mode)

**If `Audit.mode = per-story`:** Before writing the prd.json, send the draft through the auditor for a structured PRD review. The auditor catches problems while they're cheap to fix.

**If `Audit.mode = sprint-close` or `off`:** Skip this step. Jump to Step 6 (Review and Write).

### Spawn the auditor (or reuse existing team)

Write the draft PRD to a temp path so the auditor can read it without conflicting with any existing `scripts/ralph/prd.json`:

```bash
# write the draft to a temp path (the lead's tooling, not bash here)
# echo "<draft prd json>" > /tmp/draft-prd.json
```

> **Team name (`<team>`):** resolve once per session — `team_name` from RALPH.md's `## Audit` section if set, otherwise `ralph-<project-folder>` (the kebab-cased basename of the repo root, e.g. `ralph-closetize-website`). Never use the bare name `ralph`: teams are machine-global (`~/.claude/teams/`), shared across every terminal and directory, so a fixed literal name cross-wires concurrent Ralph projects — a lead in one repo can wake an idle session in another repo and send it work.

Then check if the `<team>` team already exists at `~/.claude/teams/<team>/config.json`. If yes (a sprint is in progress, auditor is alive), reuse it. If not, create one:

```
TeamCreate({ team_name: "<team>", agent_type: "team-lead", description: "Ralph sprint coordination" })
```

Spawn the auditor (skip if already a member):

```
Agent({
  subagent_type: "auditor",
  team_name: "<team>",
  name: "<auditor>",
  description: "Ralph sprint auditor — PRD review mode",
  model: "<Audit.model>",  // tier name from RALPH.md (default sonnet) — overrides the agent-file pin
  prompt: "You are joining the '<team>' team as the auditor. Your first task is PRD review. Run setup per agents/auditor.md. Then go idle and wait for an 'audit prd' message."
})
```

### Send the PRD review task

```
SendMessage({
  to: "<auditor>",
  summary: "audit draft PRD",
  message: "audit prd /tmp/draft-prd.json — run your PRD review mode flow per agents/auditor.md. Write the report to <Audit.reports_dir>/PRD-AUDIT-<branchName>.md. SendMessage the verdict + finding counts + report path back when done."
})
```

Wait for the auditor's reply.

### Show user both the draft AND the audit findings

Once the auditor returns its verdict, show:

1. **Draft summary:** total stories, testFlows, dependency order, source.
2. **Auditor verdict** (READY TO COMMIT / FIX BEFORE COMMIT / RECONSIDER SCOPE) with the report path.
3. **Critical findings** (must fix) and **important findings** (strongly recommend) — surface inline so the user doesn't have to open the file.

Use AskUserQuestion with options:
- **Apply auditor's critical fixes + commit** (Recommended if critical findings exist) — auto-apply and commit.
- **Looks good, commit as-is** (Recommended if verdict is READY TO COMMIT) — write the draft to `scripts/ralph/prd.json`.
- **Apply some fixes manually** — let the user describe which to apply, regenerate, re-audit if scope changed materially.
- **Reconsider scope** — back to Step 4, possibly drop or split stories.

If the user picks "apply critical fixes," apply them to the draft and re-message the auditor with `"re-audit prd /tmp/draft-prd.json"` to confirm fixes resolved the findings. Loop until verdict is READY TO COMMIT or user explicitly accepts a residual finding.

---

## Step 6: Review and Write

Show the complete generated `prd.json` to the user. Highlight:

- **Total number of stories** and whether that's a reasonable sprint size
- **Which stories have E2E tests** (non-null testFlow)
- **The dependency order** — confirm no story depends on a later one
- **Source** — which PRD section, backlog item, tech-debt item, or GitHub Issues this sprint covers
- **Folded-in tech debt** — if any Trivial/Small items were included
- **humanGated ACs** — list them so the user knows what they'll need to verify manually

If Step 5 ran, also note the auditor verdict for transparency.

Ask: "Does this look good? Any stories to add, remove, or adjust?"

Offer options:
- **Looks good, create the sprint**
- **I have adjustments** — let user describe changes, regenerate the affected stories

### After Approval

1. Write to `scripts/ralph/prd.json`
2. Reset `scripts/ralph/progress.txt` — keep the Codebase Patterns section at the top if it exists; clear all previous sprint entries below it. If no Codebase Patterns section exists, create a minimal header:
   ```
   # Ralph Progress Log

   ## Codebase Patterns
   [Will be populated as stories are completed]

   ---
   ```
3. Show the sprint summary:

```
## Sprint Created!

Feature: [name]
Source: [PRD section N.N / Backlog item #N / Tech debt TD-NNN / GitHub Issue #N]
Branch: [branchName]
Stories: [count]
E2E tests: [count with testFlow] / [total]
humanGated ACs: [count, with story IDs that have them]

Run /start to begin working on the first story.
```

### Sprint-plan artifact (gated on SprintPlan.artifact)

After the summary, check RALPH.md `SprintPlan.artifact` (default `off`):

- `off` — skip.
- `ask` — offer once: "Want a visual sprint-plan page for this sprint?" Respect the answer.
- `on` — build it automatically.

When building, spawn a `general-purpose` agent (background is fine — deliver the URL when it completes):

1. Read the freshly written `prd.json`.
2. Build a self-contained HTML page: a short hero header (sprint name, branch, N stories, source issues), then one card per story in priority order — story ID + title, one line on what it fixes/adds (from the description, not pasted verbatim), a small badge for humanGated ACs and test flows, and dependency arrows/notes where a story depends on an earlier one. Typographic card grid (there are no screenshots at plan time) — scannable in under a minute, no AC tables, no prose sections.
3. Load the `artifact-design` skill BEFORE writing the page, publish via the Artifact tool (stable favicon, e.g. "🗺️"; one artifact per sprint plan, named after the branch, e.g. `plan-<branch-name>`), and report the URL.
4. If the Artifact tool isn't available, write the HTML to `<Audit.reports_dir>/plan-<branch-name>.html` instead and tell the user to open it locally.

The point: the human approves scope by reading the PLAN page in one glance, and at close-out the Recap page shows what actually shipped — the pair brackets the sprint.

## Right-Sized Stories — Reference

**Good story size (fits one context window):**
- Add a database table and migration
- Create a reusable UI component
- Add a server action or API endpoint with logic
- Wire up a screen that uses existing components and hooks
- Add filtering or sorting to an existing list
- Refactor a module to a new pattern

**Too big (split these):**
- "Build the entire dashboard" — split into: schema, queries, UI components, layout, filters, integration
- "Add authentication" — split into: schema, middleware, login UI, signup UI, session handling
- "Refactor the API layer" — split into one story per endpoint or pattern change

**Rule of thumb:** If you cannot describe the change in 2-3 sentences, it is too big.

---

## Checklist Before Saving

Before writing prd.json, verify:

- [ ] Gate passed — PRD exists at the RALPH.md Documents.prd path
- [ ] All sources were checked (PRD, backlog, tech debt, GitHub Issues when enabled)
- [ ] Current sprint archived (if one existed)
- [ ] Each story is completable in one context window (~30-60 min)
- [ ] Stories are ordered by dependency
- [ ] Every story has a quality command criterion from RALPH.md
- [ ] testFlow is set correctly (only if e2e_single is configured, only for UI stories)
- [ ] Acceptance criteria are objects with `text` (and `humanGated` where applicable)
- [ ] humanGated correctly applied (only for ACs the auditor can't verify alone)
- [ ] No story depends on a later story
- [ ] Story notes reference specific files and existing patterns
- [ ] 5-8 stories (split into multiple sprints if more)
- [ ] `source` and `sourceItem` / `sourceIssues` fields are set correctly
- [ ] Branch name uses the prefix from RALPH.md Git.branch_prefix
- [ ] No `wrapPoints` array (wrap timing is decided live by `/start`)
- [ ] If Audit.mode = per-story: auditor PRD review completed (Step 5) before commit
- [ ] User has reviewed and approved the sprint
