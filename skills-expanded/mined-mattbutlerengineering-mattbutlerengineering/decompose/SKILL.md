---
name: decompose
description: Create ready-labeled GitHub issues from a feature description so /idea-to-prod:implement-queue can drain them — analyzes the codebase and files a dependency-ordered chain of child issues plus a tracking issue. Produces GitHub issues, not a design document. Invoke with /decompose.
user-invocable: true
---

# Decompose

Break a feature request into a chain of ordered GitHub issues that `/idea-to-prod:implement-queue` (or the scheduled issue-worker) can implement autonomously.

## When to Use

- "Build a reservation system" → 5-8 ordered issues
- "Add dark mode to the hospitality app" → 3-4 ordered issues
- "Create an admin dashboard" → 6-10 ordered issues

## Workflow

### Step 1: Understand the Feature

Read the user's feature description. If invoked with arguments, use those. Otherwise ask:

- What should the feature do?
- Which app/service does it affect?
- Any constraints or preferences?

### Step 2: Analyze the Codebase

Before decomposing, understand what exists:

```bash
# Check relevant areas
ls apps/ services/ packages/
# Read CLAUDE.md for architecture context
# Read relevant service/app CLAUDE.md files
# Check existing patterns in the target area
```

Key questions:

- Which existing files/components need modification?
- What new files need creation?
- Are there existing patterns to follow (routes, components, schemas)?
- What dependencies exist between the pieces?

### Step 3: Decompose into Issues

Break the feature into **3-10 issues**, each representing a single agent-workable unit. Each issue should be:

- **Self-contained**: Can be implemented without other issues being done first (unless explicitly dependent)
- **Testable**: Has clear acceptance criteria
- **Agent-sized**: 15-60 minutes of work, touching 1-5 files
- **Ordered**: Later issues build on earlier ones

#### Issue Sizing Guide

| Size   | Files Changed | Lines Changed | Example                                           |
| ------ | ------------- | ------------- | ------------------------------------------------- |
| Small  | 1-2           | 10-50         | Add a config value, fix a type                    |
| Medium | 2-4           | 50-200        | Add an API endpoint, create a component           |
| Large  | 4-6           | 200-500       | Add a full feature slice (route + service + test) |

Target **medium** size. Split large items. Combine tiny items.

#### Dependency Ordering

Issues are numbered with a `[N/total]` prefix in the title. The implement-queue works them in order (oldest first via `--sort created`), so create them in dependency order.

For parallel-safe issues (no dependencies between them), note it in the body so the implement-queue can batch them.

### Step 4: Create GitHub Issues

For each issue in order:

````bash
gh issue create \
  --title "[Feature] <feature-name> [N/M]: <specific task>" \
  --label "feature" --label "ready" \
  --body "$(cat <<'EOF'
## Context

Part N of M for: **<feature name>**

<Why this piece is needed, what it enables>

## Task

<Specific, actionable description of what to implement>

## Files to Modify/Create

- `path/to/file.ts` — <what to change>
- `path/to/new-file.ts` — <what to create>

## Acceptance Criteria

- [ ] <Specific testable criteria>
- [ ] <Another criteria>
- [ ] Tests pass: `pnpm lint && pnpm typecheck && pnpm test`

## Verification Commands

Run these after implementation to confirm the work is correct:

```bash
# Type-check and test affected packages
pnpm turbo typecheck test --filter=...[HEAD~1]

# <Add task-specific verification, e.g.:>
# curl -s https://localhost:3001/api/v1/users | jq '.data | length'
# npx vitest run src/routes/users.test.ts --grep "GET /api/v1/users"
```

## Dependencies

- Depends on: #<previous issue number> (if applicable)
- Blocks: #<next issue number> (if applicable)
- Parallel-safe: yes/no

## Patterns to Follow

<Reference a SPECIFIC existing file as a template, e.g.:>

- Route handler: follow `services/users/src/routes/users.ts` (schema + handler + test pattern)
- React component: follow `apps/hospitality/src/pages/ReservationsPage.tsx` (Rialto + API client pattern)
- Test file: follow the adjacent `*.test.ts` in the same directory

---

_Created by /decompose for feature: <feature name>_

```yaml agent
model: sonnet  # feature slices touch multiple layers — sonnet by default
budget: 1.00
```
EOF
)"

````

### Step 5: Create a Tracking Issue

Create one parent issue that tracks the overall feature:

```bash
gh issue create \
  --title "[Feature] <feature-name>: tracking issue" \
  --label "feature" --label "tracking" \
  --body "## Feature: <name>

<Full description>

## Done when

<2-5 user-visible outcomes that mean this feature has shipped, fixed now and
not extended later>

## Implementation Plan

- [ ] #<issue1> — <title>
- [ ] #<issue2> — <title>
- [ ] #<issue3> — <title>
...

## Notes

- Total issues: N
- Estimated complexity: <low/medium/high>
- Target area: <apps/services/packages affected>

---
*Decomposed by /decompose*"
```

The tracking issue does NOT get the `ready` label — it's for visibility only.

**Done is fixed at decompose time (#8742).** `tracking-checkbox.yml` ticks
each child's box as it closes and closes the tracking issue once every task
line is ticked. So put only shippable work in the task list: an Owner-only
step (teardown, backfill, sign-off) goes in its own `ready-for-human` issue,
linked under Notes, never as an unticked line that holds the feature open.
Audit or polish findings after the feature closes go in a new issue; never
reopen or extend a closed tracking issue.

### Step 6: Confirm

Show the user:

- Summary of all issues created with links
- The dependency order
- Which issues are parallel-safe
- Estimated total effort

## Labels

This skill uses these labels (create if missing):

```bash
gh label create feature --color "1D76DB" --description "New feature implementation" 2>/dev/null
gh label create tracking --color "C5DEF5" --description "Tracking issue for multi-part feature" 2>/dev/null
```

## Dependency Handling

The implement-queue picks the **oldest ready issue** first. Since we create issues in order, dependencies are naturally respected. For explicit dependencies:

1. Only the first issue (and parallel-safe issues) get the `ready` label immediately
2. Dependent issues get created with `ready` label too, but include "Depends on: #N" in the body
3. The implement-queue worker should check: if an issue says "Depends on: #N", verify #N is closed before starting work. If not, skip and try the next issue.

## Example Decomposition

**Feature**: "Add a guest check-in kiosk page to the hospitality app"

1. `[1/5] Add GuestCheckin route and page shell` — Create route, empty page component, navigation link
2. `[2/5] Add check-in API endpoint` — POST /api/v1/reservations/:id/checkin, service method, tests
3. `[3/5] Build check-in form component` — Form with reservation lookup, guest details, Rialto components
4. `[4/5] Connect form to API and add loading/error states` — API client call, error handling, success flow
5. `[5/5] Add E2E test for check-in flow` — Playwright test covering the happy path

Issues 1 and 2 are parallel-safe. Issues 3-5 depend on their predecessors.

## Safety Rules

- **Max 10 issues per feature** — if more are needed, decompose into sub-features
- **Always check the codebase first** — don't create issues for things that already exist
- **Include file paths** — the agent needs to know WHERE to work, not just WHAT
- **Include patterns** — reference SPECIFIC existing files as templates, not just "follow patterns"
- **Include verification commands** — every issue MUST have at least one executable command the agent can run to verify its work (curl, vitest --grep, etc.). The agent's orchestrator instructs it to run these.
- **Don't over-specify** — give the agent room to make implementation decisions
