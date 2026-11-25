---
name: nextjs-feature-development
description: Orchestrate end-to-end Next.js feature development from idea or plan to reviewed, committed code. Use this skill proactively when the user wants to implement a feature, page, component, route, or Server Action in a Next.js application — even if they just say "implement this", "build this", "add this to the app", "develop this plan", or "create this screen". Spawns parallel specialist subagents for codebase exploration, UX design, Next.js implementation, testing, and code review, then guides the user through approval, commit, and optional PR creation.
license: MIT
metadata:
  author: Wesley Egberto
  version: "1.0.0"
  domain: frontend
  triggers: Next.js, App Router, Server Components, Server Actions, feature, implement, build, develop, plan, component, page, route, UI, screen, interface, frontend
  role: orchestrator
  scope: implementation
  output-format: code + summary
  related-skills: nextjs-expert, nextjs-app-router-patterns, react-expert, react-patterns, frontend-design, e2e-testing-patterns, terminal-monitor
---

# Next.js Feature Development Orchestrator

## Objective

Orchestrate the complete development of a Next.js feature — from requirements through implementation, testing, review, and delivery. Uses specialized subagents running in parallel where possible to accelerate the workflow without sacrificing quality.

---

## Subagent Team

This skill **starts a team of specialist subagents** to parallelize and accelerate the implementation. Before proceeding, inform the user which agents will be used:

```
This skill will coordinate a team of specialist subagents to implement your feature:

  🔍 Code Explorer      — maps the existing codebase, patterns, and impact areas
  🎨 UX Designer        — designs user flows, component hierarchy, and interaction states
  ▲  Next.js Developer  — implements routes, layouts, Server/Client Components, Server Actions
  🧪 Test Automator     — writes unit, component, integration, and E2E tests
  🔎 Code Reviewer      — reviews for correctness, performance, security, and consistency

Agents run in parallel where possible to save time.
Each agent will open in a dedicated terminal pane (tmux or iTerm2) so you can follow progress in real time.

Shall I start the team and begin the feature development workflow?
1. Yes — let's go
2. No — I'll implement manually
```

Use `AskUserQuestion` to present this message and wait for confirmation before continuing.
If the user selects option 2, stop and let them proceed on their own.

---

## Terminal Monitoring

Each agent step MUST open a dedicated terminal pane before launching so the user can follow progress in real time.

use skill `programming-skills:terminal-monitor` — handles detection (tmux / iTerm2 / none) and pane opening. Call it once per agent with the parameters below.

### Pane parameters per step

| Step | `mode` | `label` | `pane-name` | `output-file` |
|------|--------|---------|------------|---------------|
| 2a – Code Explorer | `subagent` | `🔍 Code Explorer` | `🔍 explorer` | `.nextjs-dev/02-analysis.md` |
| 2b – UX Designer | `subagent` | `🎨 UX Designer` | `🎨 ux` | `.nextjs-dev/02-analysis.md` |
| 3 – Next.js Developer | `subagent` | `▲ Next.js Developer` | `▲ nextjs` | `.nextjs-dev/03-implementation.md` |
| 4a – Test Automator | `subagent` | `🧪 Test Automator` | `🧪 tests` | `.nextjs-dev/04-quality.md` |
| 4b – Code Reviewer | `subagent` | `🔎 Code Reviewer` | `🔎 reviewer` | `.nextjs-dev/04-quality.md` |

---

## CRITICAL BEHAVIORAL RULES

Follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.nextjs-dev/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval using `AskUserQuestion`. Do NOT continue automatically.
4. **Halt on failure.** If any agent errors or a step cannot be completed, STOP immediately and ask the user how to proceed.
5. **Respect scope.** This is a Next.js-focused orchestrator. For a non-Next.js React SPA use `frontend:react-feature-development` instead; for full-stack features spanning a separate backend, use the general `feature-development` command.
6. **Never enter plan mode autonomously.** Do NOT call `EnterPlanMode` — this skill IS the plan. Execute it.

---

## Pre-flight Checks

### 1. Check for existing session

Check if `.nextjs-dev/state.json` exists:

- If `status` is `"in_progress"`: Read it and ask the user via `AskUserQuestion`:

  ```
  Found an in-progress Next.js feature session:
  Feature: [name from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session to .nextjs-dev/archive/)
  ```

- If `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.nextjs-dev/` directory and `state.json`:

```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

The feature description (`$FEATURE`) is the full content of `$ARGUMENTS`.

---

## Phase 1: Discovery (Steps 1–2) — Interactive

### Step 1: Requirements Gathering

Gather requirements through interactive Q&A using `AskUserQuestion`. Ask ONE question at a time — do NOT dump all questions at once.

**Questions to ask (in order):**

1. **Feature description**: "Describe the feature, page, or route to be built. What is its purpose and who will use it?"
2. **Routes and components**: "Which routes (App Router segments) or existing components are affected or need to be created?"
3. **Acceptance criteria**: "What are the key acceptance criteria? When is this feature 'done'?"
4. **Design references**: "Are there mockups, Figma files, or design references? If so, share them. If not, should I propose a design approach?"
5. **Data source**: "Does this feature fetch data from an API, database, or CMS? Should it use Server Components / `fetch` with caching, Server Actions for mutations, or a client-side data library (SWR, React Query)? Share any endpoint/data contracts."
6. **Technical constraints**: "Any technical constraints? (e.g., must use specific rendering mode — SSR/SSG/ISR/PPR, existing component library, performance budget, edge vs. node runtime)"

After gathering answers, write:

**Output file:** `.nextjs-dev/01-requirements.md`

```markdown
# Requirements: $FEATURE

## Feature Description

[From Q1]

## Routes and Components Affected

[From Q2]

## Acceptance Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Design References

[From Q4 — mockup links, descriptions, or "design to be proposed"]

## Data Source

[From Q5 — API/DB/CMS, Server Component fetch vs. Server Action vs. client library, contracts]

## Technical Constraints

[From Q6]
```

Update `state.json`: set `current_step` to 2, add `"01-requirements.md"` to `files_created`.

---

### Step 2: Parallel Analysis — Codebase + UX Design

Read `.nextjs-dev/01-requirements.md`. Then open monitoring panes and launch TWO agents in parallel in a single response using the `Agent` tool:

use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🔍 Code Explorer`, `pane-name: 🔍 explorer`, `output-file: .nextjs-dev/02-analysis.md`
use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🎨 UX Designer`, `pane-name: 🎨 ux`, `output-file: .nextjs-dev/02-analysis.md`

**2a. Codebase Explorer:**

```
Agent:
  subagent_type: "programming-skills:code-explorer"
  description: "Explore Next.js codebase for $FEATURE"
  prompt: |
    You are a codebase explorer. Analyze the Next.js project to map the existing
    patterns and identify what needs to change to implement this feature.

    ## Feature Requirements
    [Insert full contents of .nextjs-dev/01-requirements.md]

    ## What to explore and document:
    1. **App Router structure**: `app/` directory layout, route groups, layouts,
       templates, parallel/intercepting routes relevant to this feature.
    2. **Component patterns**: How existing Server and Client Components are
       structured (file naming, `"use client"` boundaries, prop types).
    3. **Data fetching**: How data is fetched — `fetch` with caching options,
       Server Actions, Route Handlers (`app/api/`), or a client library
       (SWR, React Query) — and where those live.
    4. **Rendering strategy**: SSR/SSG/ISR/PPR usage, `revalidate`/`dynamic`
       exports, and the `use cache` directive if used in this project.
    5. **State management**: What library is used for client-side state
       (Context, Zustand, Redux, URL state) and how it's organized.
    6. **Styling approach**: CSS modules, Tailwind, styled-components, or other
       — with examples.
    7. **Testing patterns**: Existing test setup, libraries used (Jest, Vitest,
       RTL, Playwright), and test file conventions.
    8. **Impact map**: List the specific files/directories that will likely be
       created or modified for this feature, with a brief reason for each.

    Write your findings as a structured markdown document with clear headings.
    Focus on what a developer needs to know to implement this feature consistently
    with the existing codebase.
```

**2b. UX Designer:**

```
Agent:
  subagent_type: "frontend:ui-ux-designer"
  description: "Design UX approach for $FEATURE"
  prompt: |
    You are a UX designer specializing in Next.js applications.
    Analyze the feature requirements and propose a detailed UX/UI design approach.

    ## Feature Requirements
    [Insert full contents of .nextjs-dev/01-requirements.md]

    ## Your deliverables:
    1. **User flows**: Step-by-step interaction flow from the user's perspective. Use a simple numbered or flowchart-style format.
    2. **Route and component hierarchy**: Propose the route segments and component tree for new screens/components (server vs. client boundary called out explicitly).
    3. **State and interaction design**: Identify loading states (`loading.tsx`, `<Suspense>`), empty states, error states (`error.tsx`), and optimistic updates needed for Server Actions.
    4. **Accessibility considerations**: Key ARIA roles, keyboard navigation requirements, focus management.
    5. **Responsive behavior**: How the UI should adapt across breakpoints (if applicable).
    6. **Design decisions**: Explain key UI/UX choices and trade-offs.

    If design references were provided in the requirements, use them as the primary source.
    If no references exist, propose a design that is consistent with a modern Next.js application.

    Write your findings as a structured markdown document.
    Use the `Skill` tool with skill name "frontend:frontend-design" to guide your aesthetic and UX decisions.
```

After both agents complete, consolidate their outputs into:

**Output file:** `.nextjs-dev/02-analysis.md`

```markdown
# Codebase & UX Analysis: $FEATURE

## Codebase Findings

[Full output from code explorer — App Router structure, patterns, impact map]

## UX Design Approach

[Full output from UX designer — user flows, route/component hierarchy, state design]
```

Update `state.json`: set `current_step` to `"checkpoint-1"`, add step 2 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — Analysis Review

You MUST stop here. Present a concise summary and ask via `AskUserQuestion`:

```
Analysis complete. Review .nextjs-dev/02-analysis.md for full details.

Codebase summary: [2-3 bullet points from explorer — key patterns and impact map]
UX design summary: [2-3 bullet points from designer — user flows and route/component hierarchy]

1. Approve — proceed to implementation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1.
If they select option 2, revise the relevant section of `.nextjs-dev/02-analysis.md` and re-checkpoint.
If option 3, update `state.json` status to `"paused"` and stop.

---

## Phase 2: Next.js Implementation (Step 3)

### Step 3: Implement the Feature

Read `.nextjs-dev/01-requirements.md` and `.nextjs-dev/02-analysis.md`.

use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: ▲ Next.js Developer`, `pane-name: ▲ nextjs`, `output-file: .nextjs-dev/03-implementation.md`

Then launch the Next.js developer agent:

```
Agent:
  subagent_type: "frontend:nextjs-developer"
  description: "Implement Next.js feature: $FEATURE"
  prompt: |
    You are a senior Next.js developer. Implement this feature based on the approved
    requirements and analysis.

    ## Feature Requirements
    [Insert full contents of .nextjs-dev/01-requirements.md]

    ## Codebase & UX Analysis
    [Insert full contents of .nextjs-dev/02-analysis.md]

    ## Implementation Instructions
    1. Follow the route/component hierarchy and user flows from the UX analysis exactly.
    2. Match the existing code patterns documented in the codebase analysis — naming
       conventions, file structure, Server/Client Component boundaries, data fetching
       style, and styling method.
    3. Default to Server Components; add `"use client"` only where interactivity requires it.
    4. Use Server Actions for mutations where appropriate, with proper validation and
       revalidation (`revalidatePath`/`revalidateTag`).
    5. Implement all required states: loading (`loading.tsx`/`<Suspense>`), empty,
       error (`error.tsx`), success, and any optimistic updates.
    6. Add accessibility: semantic HTML, ARIA labels where needed, keyboard navigation.
    7. Keep components focused and composable — avoid monolithic components.
    8. Add inline comments only where logic is non-obvious.
    9. Do NOT introduce new libraries unless clearly necessary and not already available in the project.

    Use the `Skill` tool with the following skills as needed:
    - "frontend:nextjs-expert" — for Next.js 16 App Router, Cache Components, Turbopack
    - "frontend:nextjs-app-router-patterns" — for routing, layouts, and data-fetching patterns
    - "frontend:react-expert" — for React 19+ patterns and hooks
    - "frontend:react-patterns" — for reusable component patterns

    Write all code files directly to the project directory.
    After implementation, report a complete summary as a markdown document listing:
    - Every file created or modified (with path and brief description of changes)
    - Key implementation decisions and patterns used
    - Any deviations from the analysis and why
```

Save the agent's summary to:

**Output file:** `.nextjs-dev/03-implementation.md`

```markdown
# Implementation Summary: $FEATURE

## Files Created

- `app/(feature)/feature-name/page.tsx`: [description]
- `app/(feature)/feature-name/loading.tsx`: [description]
- `app/(feature)/feature-name/error.tsx`: [description]
- `app/(feature)/feature-name/actions.ts`: [description — Server Actions]
- `components/FeatureName/FeatureName.tsx`: [description]

## Files Modified

- `app/layout.tsx`: Added navigation entry for new feature.

## Key Decisions

- [Decision 1 and rationale]
- [Decision 2 and rationale]

## Deviations from Analysis

- [Any deviations and why — or "None"]
```

Update `state.json`: set `current_step` to `"checkpoint-2"`, add step 3 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — Implementation Review

You MUST stop here. Present a summary and ask via `AskUserQuestion`:

```
Implementation complete. Review .nextjs-dev/03-implementation.md for full details.

Files created: [count] | Files modified: [count]
Key changes: [2-3 bullet points of most important changes]

1. Approve — proceed to testing and code review
2. Request changes — tell me what to fix
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 3 until the user selects option 1.

---

## Phase 3: Quality — Testing & Review (Step 4)

### Step 4: Parallel Testing and Code Review

Read `.nextjs-dev/01-requirements.md`, `.nextjs-dev/02-analysis.md`, and `.nextjs-dev/03-implementation.md`.

use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🧪 Test Automator`, `pane-name: 🧪 tests`, `output-file: .nextjs-dev/04-quality.md`
use skill `programming-skills:terminal-monitor` with: `mode: subagent`, `label: 🔎 Code Reviewer`, `pane-name: 🔎 reviewer`, `output-file: .nextjs-dev/04-quality.md`

Launch TWO agents in parallel in a single response:

**4a. Test Automator:**

```
Agent:
  subagent_type: "programming-skills:test-automator"
  description: "Create test suite for $FEATURE"
  prompt: |
    You are a frontend test engineer. Create a comprehensive test suite for this
    Next.js feature.

    ## Requirements
    [Insert full contents of .nextjs-dev/01-requirements.md]

    ## Implementation Summary
    [Insert full contents of .nextjs-dev/03-implementation.md]

    ## Testing Instructions
    1. Write unit tests for all new Server Actions and utility functions.
    2. Write component tests using React Testing Library for all new Client
       Components — cover: render, user interactions, loading states, error states, empty states.
    3. Write integration tests for key user flows (as described in requirements),
       mocking data fetching where Server Components are involved.
    4. Write at least one E2E test for the primary happy path using the project's E2E framework (Playwright).
    5. Follow the existing test patterns and file conventions found in the codebase analysis.
    6. Target 80%+ coverage for new code.
    7. Mock external APIs and dependencies appropriately.

    Use the `Skill` tool with "frontend:e2e-testing-patterns" for E2E test guidance.

    Write all test files directly to the project directory.
    Report a summary of: test files created, what each covers, and any coverage gaps identified.
```

**4b. Code Reviewer:**

```
Agent:
  subagent_type: "programming-skills:code-reviewer"
  description: "Code review for $FEATURE"
  prompt: |
    You are a senior Next.js code reviewer. Perform a thorough review of this
    feature implementation.

    ## Requirements
    [Insert full contents of .nextjs-dev/01-requirements.md]

    ## Codebase Patterns (for consistency check)
    [Insert the "Codebase Findings" section from .nextjs-dev/02-analysis.md]

    ## Implementation Summary
    [Insert full contents of .nextjs-dev/03-implementation.md]

    ## Review Dimensions
    Review ALL of these dimensions. For each finding, include severity
    (Critical, High, Medium, Low), the affected file:line if known, and a specific fix recommendation.

    1. **Correctness**: Logic errors, off-by-one bugs, incorrect API usage, missing null checks.
    2. **Server/Client boundary**: Unnecessary `"use client"` directives, client-only APIs
       used in Server Components, secrets/env vars leaking to the client bundle.
    3. **Next.js patterns**: Correct use of `fetch` caching options, `revalidatePath`/`revalidateTag`
       after Server Action mutations, correct `loading.tsx`/`error.tsx`/`not-found.tsx` usage,
       missing `key` props in lists.
    4. **Code consistency**: Does the code match existing patterns documented in the codebase analysis?
    5. **Accessibility**: Missing ARIA attributes, keyboard navigation issues, insufficient color contrast descriptions.
    6. **Performance**: Unnecessary client-side data fetching that could be a Server Component,
       missing `Suspense` boundaries causing waterfalls, unoptimized images (not using `next/image`), large bundle additions.
    7. **Security**: XSS vectors (`dangerouslySetInnerHTML`), unvalidated input in Server Actions,
       sensitive data returned from Server Components to the client.
    8. **Maintainability**: Overly complex components, missing error boundaries, hardcoded values that should be constants.

    Format your findings as a structured markdown list:
    ```
    - **Severity**: High
      **File**: `app/(feature)/feature-name/actions.ts:18`
      **Finding**: Server Action does not validate input before writing to the database.
      **Fix**: Validate with a schema (Zod) before calling the data layer.
    ```

    Provide an overall assessment: Approved / Approved with minor fixes / Requires changes.
```

After both complete, consolidate into:

**Output file:** `.nextjs-dev/04-quality.md`

```markdown
# Quality Report: $FEATURE

## Test Suite

[Summary from test automator — files created, coverage areas, gaps]

## Code Review Findings

[Consolidated findings list from code reviewer]

### Overall Assessment

[Approved / Approved with minor fixes / Requires changes]

## Action Items (Critical & High severity)

[List of Critical and High findings that MUST be addressed before delivery]
```

**If Critical or High severity findings exist**, address them now:
1. Apply fixes directly or spawn a focused `frontend:nextjs-developer` agent to fix them.
2. Update `.nextjs-dev/03-implementation.md` with any additional files changed.
3. Re-run the code reviewer on the changed files only.

Update `state.json`: set `current_step` to `"checkpoint-3"`, add step 4 to `completed_steps`.

---

## PHASE CHECKPOINT 3 — Quality Review

You MUST stop here. Ask via `AskUserQuestion`:

```
Testing and code review complete. Review .nextjs-dev/04-quality.md for full details.

Tests: [number of test files created] test files | [coverage summary]
Code review: [count Critical] Critical | [count High] High | [count Medium] Medium findings
Overall assessment: [Approved / Approved with minor fixes / Requires changes]

Critical/High items addressed: [Yes / None found]

1. Approve — proceed to final delivery
2. Request changes — tell me what to fix
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 4 until the user selects option 1.

---

## Phase 4: Delivery (Step 5)

### Step 5: Summary, Review, and Commit

#### 5a. Generate Final Summary

Read all `.nextjs-dev/*.md` files and write:

**Output file:** `.nextjs-dev/05-summary.md`

```markdown
# Feature Delivery Summary: $FEATURE

## What Was Built

[2-4 sentence description of the feature and its purpose]

## Files Created

[Complete list from 03-implementation.md + 04-quality.md test files]

## Files Modified

[Complete list of modified files]

## Quality Assurance

- Tests: [list of test files and what they cover]
- Code review assessment: [overall assessment]
- Issues resolved: [list of Critical/High findings addressed, or "None found"]

## Points of Attention

[List any Medium/Low review findings NOT fixed — explain why deferred and recommended follow-up]
[List any known limitations or TODOs left in the code]
[Any areas where the implementation deviates from requirements and why]

## Impact Map

[From codebase analysis — which parts of the app were touched and how they interact]

## How to Test Manually

1. [Step 1 to verify the feature works end-to-end]
2. [Step 2]
3. [Step 3 — edge cases to check]
```

Present the summary to the user and then ask via `AskUserQuestion`:

```
Feature implementation is complete. Here's what was built:

[Paste the "What Was Built" and "Points of Attention" sections inline]

Please:
1. Review the code in the files listed above
2. Run the test suite: [insert the project's test command, e.g., `npm test`]
3. Perform manual verification using the steps in .nextjs-dev/05-summary.md

When you're ready:
1. Approve — commit the changes
2. Request changes — tell me what to fix
3. Abort — discard all changes
```

Wait for user response. If they request changes, implement them and return to this checkpoint.

#### 5b. Commit

Once the user approves, perform the commit:

1. Run `git status` to confirm the changed files match the implementation summary.
2. Stage all implementation and test files (be explicit — do NOT use `git add .`).
3. Create a commit with a descriptive message following the project's commit convention (check recent `git log` to match the style):

```
feat(nextjs): [brief description of the feature]

- [Key change 1]
- [Key change 2]
- [Key change 3]

Co-Authored-By: Claude Code
```

4. Confirm the commit succeeded with `git status`.

Then ask via `AskUserQuestion`:

```
Changes committed successfully.

Branch: [current branch name]
Commit: [commit hash and message]

Would you like to open a Pull Request?

1. Yes — create a PR now
2. No — I'll open the PR manually later
```

#### 5c. Pull Request (if requested)

If the user says yes, create the PR using `gh pr create`:

- **Title**: `feat: [feature name]` (short, under 70 characters)
- **Body**: Include What Was Built, files changed, how to test manually, and the points of attention from `.nextjs-dev/05-summary.md`

Return the PR URL to the user.

---

## Completion

Update `state.json`:

```json
{
  "status": "complete",
  "last_updated": "ISO_TIMESTAMP"
}
```

#### Move artifacts to feature docs folder

Derive the feature folder name from `$FEATURE`: lowercase, spaces replaced by hyphens, special characters removed (e.g., `"User Profile Page"` → `user-profile-page`). Call this `$FEATURE_SLUG`. Also capture today's date as `$DATE` (format `YYYY-MM-DD`).

Create the destination directory and move all generated files:

```bash
DATE=$(date +%Y-%m-%d)
mkdir -p .specs/features/$DATE-$FEATURE_SLUG/artifacts/nextjs
mv .nextjs-dev/01-requirements.md    .specs/features/$DATE-$FEATURE_SLUG/artifacts/nextjs/
mv .nextjs-dev/02-analysis.md        .specs/features/$DATE-$FEATURE_SLUG/artifacts/nextjs/
mv .nextjs-dev/03-implementation.md  .specs/features/$DATE-$FEATURE_SLUG/artifacts/nextjs/
mv .nextjs-dev/04-quality.md         .specs/features/$DATE-$FEATURE_SLUG/artifacts/nextjs/
mv .nextjs-dev/05-summary.md         .specs/features/$DATE-$FEATURE_SLUG/artifacts/nextjs/
mv .nextjs-dev/state.json            .specs/features/$DATE-$FEATURE_SLUG/artifacts/nextjs/
```

After moving, remove the now-empty `.nextjs-dev/` directory:

```bash
rmdir .nextjs-dev
```

Present the final message:

```
Next.js feature development complete: $FEATURE

Artifacts saved to .specs/features/$DATE-$FEATURE_SLUG/artifacts/nextjs/:
- 01-requirements.md    — Requirements
- 02-analysis.md        — Codebase & UX analysis
- 03-implementation.md  — Implementation summary
- 04-quality.md         — Tests & code review
- 05-summary.md         — Final delivery summary

Next steps (if any):
[List any deferred items from points of attention]
```
