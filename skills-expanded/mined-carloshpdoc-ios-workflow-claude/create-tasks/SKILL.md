---
name: create-tasks
description: >
  Creates Jira tasks from meeting notes, specs, or feature descriptions.
  Supports both iOS (Swift/SwiftUI) and Backend (Node.js/TypeScript) platforms.
  Use this skill whenever a user pastes meeting notes, a spec, a feature request, or any description of work to be planned.
  Triggers on: "create tasks", "break this into tickets", "plan this feature", "create Jira tickets", "turn this into tasks",
  or when a user pastes meeting notes or a feature spec and asks what to do with it. Always use this skill for task
  planning — even if the user doesn't say "Jira" or "tickets" explicitly.
---

> **Project context:** Values in angle brackets below (e.g. `<scheme>`, `<JIRA_KEY>`, `<flag-key-enum>`) are resolved at runtime — detect them from the project (`xcodebuild -list -json` for the scheme, `git`/`gh` for repo & owner, the branch name for the Jira key, a codebase search for flag/font files), or ask if they cannot be inferred. This plugin ships no per-project config.
 
# Create Tasks from Meeting Notes / Specs
 
Take meeting notes, specs, or a feature description as input. Detect the platform, explore the codebase, plan the implementation, and create Jira tickets.
 
## Usage
 
```
/create-tasks <description or paste meeting notes>
```
 
- `$ARGUMENTS` — Feature description, meeting notes, specs, or any context about work to be planned
---
 
## Platform Detection
 
Detect the platform automatically from the current repository:
 
| Signal | Platform |
|--------|----------|
| `Package.swift`, `*.xcodeproj`, `Tuist/`, `*.swift` files | **iOS** |
| `package.json`, `tsconfig.json`, `src/api/`, `serverless.yml` | **Backend** |
 
If ambiguous (e.g., meeting notes mention both platforms), ask the user which platform to create tasks for — or create tasks for both if explicitly requested.
 
---
 
## Jira Configuration (Shared)
 
- **Project:** <JIRA_KEY>
- **Issue type:** Task
- **Story points field:** `customfield_10034`
- **Allowed story point values:** 1, 2, 3 only
- **Board:** https://<jira-host>/jira/software/c/projects/<JIRA_KEY>/boards/<jira-board-id>/backlog
- **Epic:** Link tasks to an epic via `"parent": "<EPIC-KEY>"` in `additional_fields`. Ask the user which epic to use if not specified.
- **Assignee:** Ask the user who to assign tasks to before creating tickets. Use email or display name for the `assignee` field.
- **Sprint:** Default to the current active sprint. Fetch via `mcp__mcp-atlassian__jira_get_sprints_from_board` (board ID `<jira-board-id>`, state `active`). Set via `"customfield_10020": <sprint_id>` in `additional_fields`. If no active sprint or the user specifies a different one, ask for input.
- **Next sprint (for feature flag cleanup tickets):** Fetch via `mcp__mcp-atlassian__jira_get_sprints_from_board` (board ID `<jira-board-id>`, state `future`) and take the first result. If no future sprint exists yet, ask the user whether to create the cleanup ticket in the backlog (omit `customfield_10020`) or wait.
---
 
## Platform-Specific Configuration
 
### iOS
 
- **Labels:** Apply all relevant labels per task:
  - **Team:** `frontend`
  - **Module:** e.g., `explore`, `feed`, `plan-tab`
  - **Report:** exactly one of `report-feature`, `report-improvement-fix`, `report-tech-improvement`, `report-analytics-fix`
- **Story Point Scale:**
  | Points | Scope | Examples |
  |--------|-------|----------|
  | **1** | Trivial / mechanical change, < 1 hour | Rename a file/struct, add a field to a model, update a CodingKeys enum, delete dead code |
  | **2** | Moderate change, 1–3 hours | Update a query + response models, create a simple view, wire a new case into an existing switch |
  | **3** | Significant change, 3–6 hours | Create a new UI component from Figma, build a new repository layer end-to-end, refactor a view model with new data flow |
### Backend
 
- **Labels:** `["backend"]`
- **Story Point Scale:**
  | Points | Time estimate | Scope |
  |--------|--------------|-------|
  | **1** | ~1–4 hours | Small, focused change — add a field to a Mongoose model, update a GraphQL type, minor refactor, add a DataLoader |
  | **2** | ~5–8 hours | Moderate — new service method + tests, new repository query, wiring a new GraphQL resolver with validation and permissions |
  | **3** | ~9–16 hours | Significant — new domain module end-to-end, complex data pipeline, new Lambda function, major refactor across multiple layers |
**Hard rule (both platforms):** If a task would exceed 3 points, split it. No task should be larger than 3 story points.
 
**Trivial task rule (both platforms):** If a task is purely mechanical and small enough to be part of another task (e.g., adding a feature flag, adding a constant, updating an env variable), fold it into the most relevant adjacent task. No standalone tickets for these.

**Feature flag cleanup rule (both platforms):** Whenever any task in the plan introduces a new feature flag (A/B test, experiment, gradual rollout, kill switch), pair it with a mandatory cleanup ticket scheduled in the **next sprint**. See [Feature Flag Cleanup](#feature-flag-cleanup-both-platforms) below for the full rule. Folding the flag *creation* into an adjacent task (trivial task rule above) does not exempt you from creating the *cleanup* ticket.
 
---
 
## Workflow
 
### Phase 1: Understand the Request
 
1. Parse `$ARGUMENTS` to extract:
   - What is being built or changed
   - Any GraphQL queries/mutations or API contracts provided
   - UI/UX requirements or Figma references (iOS)
   - Which modules/domains are affected
   - Any explicit non-goals or out-of-scope items
2. **Extract only tasks for the detected platform.** Ignore:
   - Tasks for the other platform (unless explicitly requested)
   - Process or organizational discussions
   - Non-engineering items
3. If the scope is ambiguous, note open questions and ask before proceeding.
### Phase 2: Explore the Codebase
 
4. Launch up to **3 parallel explore agents** to understand the current implementation:
   **iOS agents:**
   - Find existing files, models, views, view models, repositories related to the feature
   - Find existing patterns and components that can be reused
   - Understand the data pipeline (query → response model → mapper → repository → use case → view model → view)
   **Backend agents:**
   - **Agent 1 — Domain model:** Find `*.model.ts` and `*.entities.ts` in the relevant domain; check for existing migrations
   - **Agent 2 — API layer:** Find the relevant `src/api/*-api.ts`; identify existing `typeDefs`, resolver signatures, Joi validations, and shield permissions
   - **Agent 3 — Service/repository layer:** Find `*.service.ts` and `*.repository.ts` in the relevant domain; identify methods, patterns, and event bus usage
5. Read the critical files identified to verify details before planning.
6. Specifically look for:
   - **Existing patterns** for similar features — always follow them, never invent new conventions
   - **(iOS)** Reusable UI components, existing design system tokens, AppStrings keys
   - **(Backend)** DataLoaders in `src/dataLoaders/`, feature flag infrastructure in `src/domain/config/`, event bus usage, Lambda functions in `src/functions/`
### Phase 3: Plan the Implementation
 
7. Break the work into **discrete, independently deliverable tasks**. Each task must:
   - Have a single clear concern
   - Be completable in one PR or less
   - Follow natural dependency order
8. **Dependency ordering:**
   - **iOS:** Data layer → domain → presentation (models → repository → view model → view)
   - **Backend:** Schema/model + migrations → repository → service → API resolver → event listeners → cleanup
9. **Per-task detail to include:**
   - Exact file paths to create or modify
   - Existing patterns or utilities to reuse
   - Whether unit tests need to be added or updated
   - **(Backend)** Whether a DataLoader needs to be created or extended
10. Estimate each task using the platform-specific story point scale.
11. **Detect feature flag creation.** Scan the plan for any task that introduces a new feature flag (A/B test, experiment, gradual rollout, kill switch). For each new flag, generate a paired cleanup task per [Feature Flag Cleanup](#feature-flag-cleanup-both-platforms) below. The cleanup task targets the **next sprint**, not the current one.
### Phase 4: Confirm with User
 
12. Present the plan as a table. Add a **Sprint** column so the user can see at a glance which tickets land in the current sprint vs. the next one (feature flag cleanup tickets always show `next`):
```
| # | Task | SP | Sprint  | Files affected |
|---|------|----|---------|----------------|
| 1 | ...  | 2  | current | path/to/file.swift |
| 2 | Remove <flag> feature flag and keep <variant> flow | 1 | next | path/to/file.swift |
```
 
13. Include:
    - Total story points (broken out by sprint if any tickets target the next sprint)
    - Any open questions (ambiguous scope, missing specs, unclear domain ownership)
    - Any tasks folded together and why
    - For each feature flag cleanup ticket: which experiment flow is being kept and whether the user needs to confirm it
14. **Ask for confirmation before creating any Jira tickets.** Confirm both the current-sprint plan and the next-sprint cleanup tickets.
### Phase 5: Create Jira Tickets
 
15. Once confirmed, create each Task in the <JIRA_KEY> project via the Atlassian MCP:
    - **Summary:** `[FEATURE] <concise task description>`
    - **Description:** What to implement, which files to touch, which patterns to follow, key technical notes (include test requirements)
    - **Labels:** Per platform configuration above
    - **Assignee:** As specified by the user
    - **Additional fields:** `{"customfield_10034": <points>, "parent": "<EPIC-KEY>", "customfield_10020": <sprint_id>}`
    - **Sprint targeting:**
      - Implementation tickets → current sprint ID (state `active`)
      - Feature flag cleanup tickets → next sprint ID (state `future`, first result)
      - If no future sprint exists, follow the fallback set in the [Jira Configuration](#jira-configuration-shared) section
16. Present the final ticket summary, grouped by sprint:
```
| # | Task | SP | Sprint  | Key |
|---|------|----|---------|-----|
| 1 | ...  | 2  | current | <JIRA_KEY>-XXXX |
| 2 | ...  | 3  | current | <JIRA_KEY>-XXXX |
| 3 | Remove <flag> feature flag and keep <variant> flow | 1 | next    | <JIRA_KEY>-XXXX |
|   | **Total (current)** | **5** | | |
|   | **Total (next)**    | **1** | | |
```
 
---
 
## Architecture Reference (template — adapt to your project)

> Replace the sections below with the structure of your own project. The default template assumes a Tuist-based iOS app + a Node.js GraphQL backend; trim or rewrite the sections that don't apply.

### iOS (Swift / SwiftUI) — example layout

```
Projects/
  App/<scheme>/         → Main app target
    Modules/           → Feature modules
  UIComponents/        → Reusable UI components (design system)
  SharedModels/        → Shared data models across modules
  Service/             → Network layer, repositories
  FeatureToggle/       → Feature flags
  Analytics/           → Tracking events
  AppStrings/          → Localization
```

**Architecture:** MVVM + Coordinator + Factory (adapt to your stack)

**Data pipeline:** GraphQL query → Response model → Mapper → Repository → ViewModel → View

**Key conventions (customize per project):**
- Fonts: `<font-scale-tokens>` tokens only — no `Font.custom(...)`
- Colors: design-system color tokens only — no hardcoded hex
- Strings: localization module only — no hardcoded user-facing strings
- Tests: mandatory for every feature

### Backend (Node.js / TypeScript) — example layout

```
src/api/              → GraphQL typeDefs + resolvers + validations + permissions (thin layer)
src/domain/           → Business logic grouped by bounded context (preferred for new code)
  <context-1>/        → e.g. user, billing, content — one folder per domain
  <context-2>/
  config/             → Feature flags
src/services/         → Legacy modules (do not add new code here)
src/functions/        → Serverless handlers (Lambda, Cloud Functions, etc.)
src/integrations/     → External APIs
src/dataLoaders/      → Per-request batched loaders (prevent N+1)
```

**Architecture:** Domain-driven layers (API → Service → Repository → Model)

**Key conventions (customize per project):**
- New features in `src/domain/`, never `src/services/`
- Resolvers stay thin — business logic in services
- Schema changes need migrations
- Use an event bus for cross-domain side effects
- DataLoaders for any relationship lookup
---
 
## Guidelines (Both Platforms)
 
- **Reuse over create:** Always look for existing models, components, patterns before proposing new ones
- **Data layer first:** Order tasks so data/model changes come before UI/API changes
- **One concern per task:** Don't mix layers in the same task
- **Rename/cleanup last:** Renames and dead code cleanup should be the final tasks
- **Be specific:** Task descriptions should mention exact file paths and what changes
- **Don't over-split:** 3–7 tasks is ideal. Don't create a task for trivial one-line changes
- **Fold trivial work:** Feature flags, env vars, config values go into the adjacent task, never standalone
- **Pair every new feature flag with a cleanup ticket in the next sprint:** see [Feature Flag Cleanup](#feature-flag-cleanup-both-platforms)
---

## Feature Flag Cleanup (Both Platforms)

Feature flags are introduced to ship safely, run experiments, or roll out gradually — but a flag left in the code after the experiment ends turns into dead code that nobody owns. To prevent that, every time a task creates a new flag this skill must also create a paired cleanup ticket scheduled for the **next sprint**.

### When this rule fires

A task triggers a cleanup ticket if it introduces any of the following:

- A new A/B test or experiment flag
- A new gradual rollout / kill switch
- Any new entry in the feature flag system (iOS `FeatureToggle` module, Backend `src/domain/config/`)
- Any conditional that branches on a remote config value not previously used

If the task only *reads* an existing flag, no cleanup ticket is needed.

### The cleanup ticket

For each new flag, generate one cleanup task with the following shape:

- **Summary:** `[FEATURE] Remove <flag_name> feature flag and keep <kept_variant> flow`
  - `<kept_variant>` is the experiment branch the team expects to win (e.g., `treatment`, `control`, `variant_A`, the new UI, etc.)
  - If the winner is not known at planning time, use `winning variant` and call out the TBD in the description
- **Description must include:**
  1. The flag identifier and where it is defined
  2. A short description of both flows (control vs. treatment / off vs. on)
  3. Which flow to keep (or "Winning variant TBD — update before pickup" if unknown)
  4. The files that read the flag (from Phase 2 exploration) plus the dead-flow files that will be deleted
  5. A reminder to remove the flag entry from the feature flag system itself
  6. A note that tests asserting the dead flow must be removed and tests for the kept flow must remain green
  7. (iOS) Reference the `/feature-flag-remove` skill as the execution playbook
- **Story points:** Start at **1** (mechanical cleanup). If the flag is read in many places or branches across multiple modules, split into multiple cleanup tickets rather than going above 3 SP.
- **Labels:** Same as the creation ticket's platform labels, plus `report-tech-improvement` (iOS) since this is internal cleanup, not user-facing work.
- **Assignee:** Same as the creation ticket unless the user specifies otherwise.
- **Epic:** Same epic as the creation ticket.
- **Sprint:** Next sprint (state `future`, first result from board 105). See [Jira Configuration](#jira-configuration-shared) for the fallback when no future sprint exists.

### What to ask the user

Before creating the cleanup ticket, confirm:

1. **Which experiment flow should be kept?** (treatment / control / specific variant)
   - If the experiment outcome is genuinely unknown, accept "TBD" and embed that in the ticket description.
2. **Is the next sprint the right target?** (default yes — only ask if no future sprint exists or the user has previously specified a different cadence)

Do not ask about whether the cleanup ticket should exist — it is mandatory.

### Anti-patterns

- **Don't** create a standalone "Add the feature flag" ticket in the current sprint. The flag setup folds into the implementation ticket (trivial task rule).
- **Don't** put the cleanup ticket in the current sprint — the whole point is that the cleanup happens *after* the experiment runs.
- **Don't** skip the cleanup ticket because "we'll remember" — institutional memory is exactly what this rule exists to replace.
- **Don't** combine cleanup of multiple unrelated flags into one ticket. One flag, one cleanup ticket.

---
 
## Example Output
 
### iOS Example — "Add feed shortcuts to editorial feed"
 
| # | Task | SP | Key |
|---|------|-----|-----|
| 1 | Implement new editorialFeedItemsWithShortcuts query and response models | 3 | <JIRA_KEY>-XXXX |
| 2 | Change feed container from HStack to horizontal ScrollView | 1 | <JIRA_KEY>-XXXX |
| 3 | Decode new response into dynamic FeedShortcuts buttons | 3 | <JIRA_KEY>-XXXX |
| 4 | Rename CategoryButton to FeedShortcutsButton | 1 | <JIRA_KEY>-XXXX |
| 5 | Remove hardcoded NEW tag code | 2 | <JIRA_KEY>-XXXX |
| | **Total** | **10** | |
 
### Backend Example — "Add travel history export endpoint"
 
| # | Task | SP | Key |
|---|------|----|-----|
| 1 | Add `exportedAt` field to `UserTravel` Mongoose model + migration | 1 | <JIRA_KEY>-XXXX |
| 2 | Add `findExportableByUserId` to `userTravel.repository.ts` | 2 | <JIRA_KEY>-XXXX |
| 3 | Implement `exportTravelHistory` in `userTravel.service.ts` with CSV serialization + unit tests | 3 | <JIRA_KEY>-XXXX |
| 4 | Add `exportTravelHistory` mutation to `user-travel-api.ts` (typeDefs, resolver, Joi, shield) | 2 | <JIRA_KEY>-XXXX |
| 5 | Remove legacy `travelDump` debug resolver | 1 | <JIRA_KEY>-XXXX |
| | **Total** | **9** | |

### iOS Example with Feature Flag — "A/B test new editorial feed card layout"

The implementation introduces a `editorial_card_v2_enabled` flag. The flag setup itself is folded into task 2 (no standalone "add flag" ticket), and a paired cleanup ticket lands in the next sprint.

| # | Task | SP | Sprint  | Key |
|---|------|-----|---------|------|
| 1 | Build EditorialFeedCardV2 component from Figma | 3 | current | <JIRA_KEY>-XXXX |
| 2 | Gate EditorialFeedItem behind `editorial_card_v2_enabled` flag (add flag entry + branch rendering) | 2 | current | <JIRA_KEY>-XXXX |
| 3 | Add analytics events for V2 card impression/tap | 2 | current | <JIRA_KEY>-XXXX |
| 4 | Remove `editorial_card_v2_enabled` flag and keep V2 flow (delete legacy `EditorialFeedCard`, remove flag entry, drop dead-flow tests) | 1 | next    | <JIRA_KEY>-XXXX |
| | **Total (current)** | **7** | | |
| | **Total (next)**    | **1** | | |
 
