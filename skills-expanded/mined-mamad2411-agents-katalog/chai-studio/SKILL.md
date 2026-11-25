---
name: chai-studio-skill
description: Use when a project is connected to Chai Studio MCP for application-aware design system work, Chai-governed redesigns, preset/ruleset selection, UI audits, audit uploads, and violation follow-up. Triggers when the user mentions Chai Studio, chai-studio.yaml, design-studio.yaml, Chai MCP, design presets, audit rulesets, redesign workflow, uploading UI audit results, or syncing project design guidance with MCP.
license: MIT
metadata:
  version: 1.0.0
  owner: akshayt
  short-description: Use Chai Studio MCP for design rules and audits
---

# Chai Studio MCP

Use this skill to make Chai Studio MCP the only source of truth for design context and audit rules.

## First Move

Before every other Chai Studio action, run the setup and sync gate below. This is mandatory for redesigns, audits, fixes, rule checks, preset lookups, and any tool use that depends on Chai Studio context.

1. Look for `chai-studio.yaml` at the project root and ensure `chai-studio.yaml` is listed in `.gitignore`.
2. If `chai-studio.yaml` is missing but `design-studio.yaml` exists, parse `design-studio.yaml`, call `get-applications`, and look for a matching application by exact application name.
3. If a match is found, create `chai-studio.yaml` from that application, then run the sync gate below.
4. If no match is found and `design-studio.yaml` is valid, ask the user for explicit approval to create a Chai Studio application from it. Only after approval call `create_application_from_yaml({ content, approved: true })`, then write the returned `design-studio.yaml` content and create `chai-studio.yaml`.
5. If neither file exists, call `get-applications`, ask the user to choose which application to configure, create `chai-studio.yaml`, then call `get_application_yaml(applicationId)` and write the returned content to `design-studio.yaml`.
6. Read the configured application, preset, and audit rulesets from `design-studio.yaml` before editing UI or running audits.
7. Delete any existing local design mirror files (`DESIGN.md`, `DESIGN-RULES.md`, `design.yaml`, or similar local design-spec copies) and do not recreate them.

`design-studio.yaml` must remain Chai Studio database agnostic. Do not write `application.id`, `preset.id`, `rulesets[].id`, `createdAt`, `updatedAt`, or other Chai Studio DB fields into it. Use IDs only in `chai-studio.yaml` and MCP tool input/output metadata.

`design-studio.yaml` is not supposed to be manually edited. Treat it as a synced Chai Studio artifact: update it by calling `get_application_yaml` or, when local changes are intentional, by running `sync_application_yaml` with the required user approval flow.

## Mandatory Sync Gate

After project identity is resolved and before every Chai Studio operation:

1. Call `get_application_yaml(applicationId)` and read its `lastUpdated`.
2. Read local `design-studio.yaml` and its top-level `lastUpdated`.
3. If the MCP `lastUpdated` is older than local `design-studio.yaml`, call `sync_application_yaml({ applicationId, content, approved: false })` to get the diff. Show the diff summary to the user and ask for approval. Only after approval call `sync_application_yaml({ applicationId, content, approved: true })`, then replace local `design-studio.yaml` with the returned `content` and update `chai-studio.yaml`.
4. If the MCP `lastUpdated` is newer than local `design-studio.yaml`, replace local `design-studio.yaml` with `get_application_yaml.content` and update `chai-studio.yaml`.
5. If timestamps match, keep using local `design-studio.yaml`; if the file is missing or invalid, replace it with `get_application_yaml.content`.

For the config schema and examples, read `references/config.md`.
For full workflows, redesign protocol, and payload patterns, read `references/workflows.md`.

## Default Project Contract

`chai-studio.yaml` identifies the project's default Chai Studio application. Once present, use it without repeatedly asking the user:

- `applicationId`: default application for audits and design context.
- `presetId`: preferred design preset; verify against Chai Studio when possible.
- `auditRuleSetIds`: default rulesets for audit uploads. Pick this from the selected application's `auditRuleSetIds`, then validate them with `get-rulesets` using `applicationId`.
- `sync.lastApplicationYamlUpdatedAt`: last MCP application YAML timestamp written locally.

Do not invent IDs. Fetch them from Chai Studio MCP.

## MCP Tool Map

- `get-profile`
  - **Purpose**: Confirm authentication when the connection is uncertain.
- `get-applications`
  - **Purpose**: Fetches all applications belonging to the authenticated user.
  - **Includes**: Crucial metadata linking each app to its design system (`presetId`) and its array of connected audit rulesets (`auditRuleSetIds`).
- `get-design-doc`
  - **Input**: `applicationId`
  - **Purpose**: Legacy markdown design representation. Prefer `get_application_yaml` + `design-studio.yaml` as the project source-of-truth file.
- `get_application_yaml`
  - **Input**: `applicationId`
  - **Purpose**: Returns `design-studio.yaml` content with application details, full linked preset, full linked rulesets, and `lastUpdated`.
- `create_application_from_yaml`
  - **Input**: `content`, `approved`
  - **Purpose**: Creates a new application, linked preset, and linked rulesets from valid `design-studio.yaml`. Requires explicit user approval before `approved: true`.
- `sync_application_yaml`
  - **Input**: `applicationId`, `content`, `approved`
  - **Purpose**: Diffs local `design-studio.yaml` against Chai Studio and updates the linked preset/rulesets only after explicit user approval.
- `get-presets`
  - **Purpose**: Fetches all raw design presets configuration data associated with the user.
- `get-rulesets`
  - **Input**: `applicationId`
  - **Purpose**: Looks up the `auditRuleSetIds` tied to the given application and returns the full rule definitions. This tells an agent exactly what constraints rules apply when editing the UI or performing an audit for that app.
- `get_audits`
  - **Input**: `applicationId` (optional)
  - **Purpose**: Fetches the history of audit runs (id, status, severity counts, etc).
- `get_audit_violations`
  - **Input**: `auditId` (plus optional filters like status, severity, category)
  - **Purpose**: Fetches the granular violations for a specific audit. Crucially, each finding returns an `aiFixPrompt`, the exact `codeSnippet`, and guidance to allow an agent to immediately patch the failing file.
- `start_audit_run`
  - **Input**: `applicationId`, `auditRuleSetId`, optional `summary`, optional `totalRulesEvaluated`
  - **Purpose**: Creates one audit run before analysis so findings can be uploaded as they are discovered.
- `add_audit_violation`
  - **Input**: `auditId`, `violation`
  - **Purpose**: Uploads one violation to the existing audit run. The server skips duplicates for the same audit when the same rule/file/line/snippet/description is uploaded again.
- `complete_audit_run`
  - **Input**: `auditId`, `status`, optional `summary`, optional `totalRulesEvaluated`
  - **Purpose**: Marks a streaming audit run `completed` or `failed` after all findings have been uploaded.
- `update_violation_status`
  - **Input**: `violationId`, `status`
  - **Purpose**: Allows the agent or IDE to automatically mark an open violation as resolved, ignored, or a `false_positive`. If all violations in an audit run are squashed, this tool auto-resolves the parent audit status.

Name hygiene matters: do not rename MCP tools when calling them. Chai Studio currently exposes both hyphenated (`get-profile`, `get-design-doc`, `get-rulesets`, `get-applications`, `get-presets`) and underscored (`get_application_yaml`, `create_application_from_yaml`, `sync_application_yaml`, `get_audits`, `get_audit_violations`, `start_audit_run`, `add_audit_violation`, `complete_audit_run`, `update_violation_status`) tool names.

`design-studio.yaml` is the only local design source-of-truth file for this skill, and it must be generated or synced through Chai Studio using `get_application_yaml` and `sync_application_yaml`.

If there is a `DESIGN.md`, `DESIGN-RULES.md`, `design.yaml`, or other local design mirror file already present in the workspace, you MUST delete it. The source of truth is strictly the Chai Studio MCP server. Do not create or maintain local design mirror docs outside `design-studio.yaml` synced from Chai Studio.

## Redesign Flow

When the user asks to redesign a page, component, app surface, visual system, or interaction, read `references/workflows.md#redesign-workflow` and follow that protocol. The mandatory loop is:

1. **Context**: Run the mandatory setup/sync gate, read `chai-studio.yaml`, then use `design-studio.yaml`, `get-rulesets`, and `get-presets` when needed.
2. **Plan**: Identify affected files/routes/components and translate Chai Studio preset/ruleset constraints into implementation decisions.
3. **Implement**: Redesign with `design-studio.yaml` and linked rulesets as the source of truth.
4. **Validate**: After write changes are done, always run the project build when a build command is available, plus relevant static checks. If Chrome DevTools MCP or Playwright MCP is available, ask the user whether they want browser tests/review through those MCPs.
5. **Audit**: Reconcile prior audits, then create a fresh streaming audit run per configured ruleset.
6. **Fix only when requested**: Treat remediation as a separate flow. Do not implement fixes for audit findings unless the user explicitly asks to fix, remediate, resolve, close, or update selected violations.

Do not stop after a visual pass. A Chai Studio redesign is complete only after implementation, validation, audit upload, and verified status updates for issues already fixed by the redesign are handled or explicitly blocked. Remaining audit findings should be reported as open unless the user asked for remediation.

## Project Spec Execution Protocol

To follow Chai Studio project specifications effectively, treat project rules as a layered contract:

1. Run the mandatory setup/sync gate, then read application-level `design-studio.yaml` and extract hard constraints.
2. Read configured rulesets via `get-rulesets(applicationId)` and map rule IDs/categories/severities.
3. Read configured preset via `get-presets` for token-level styling guidance.

Priority order when rules conflict:

1. Safety and explicit user instruction
2. Chai Studio `design-studio.yaml` hard constraints
3. Chai Studio ruleset severity and guidance
4. Preset/token conventions
5. Explicit user preferences for this task

When producing findings or fixes:

- Keep changes minimal and targeted; do not refactor unrelated surfaces.
- Provide exact path + line/snippet + impact + concrete fix.
- Prioritize critical accessibility, keyboard, focus/dialog, and metadata correctness issues before lower-severity visual polish.
- Avoid introducing prohibited patterns from project specs (for example unnecessary decorative motion or forbidden visual cliches).

## Font Asset Requirement

When implementing or auditing typography, always resolve each configured or chosen font family against Google Fonts first. If the family is available there, download the required font files into the codebase (for example `public/fonts/`, `src/assets/fonts/`, or the repo's established font asset directory) and wire the app to load those local files with the framework's local font API or `@font-face`.

If a required font is not available on Google Fonts, look for the closest suitable alternative, use the best fit for the Chai Studio design context, and document the fallback in the completion report.

## Audit And Fix Boundaries

Auditing and fixing are separate flows:

- An audit request means inspect, reconcile previously fixed violations, validate against configured rulesets, upload a fresh audit run, and report findings. It does not authorize code/UI changes to fix newly discovered findings.
- A fix/remediation request means implement selected fixes, re-validate, and update violation statuses.
- Only fix audit findings when the user explicitly asks to fix, remediate, resolve, close, or update those violations. Phrases like "audit this", "find issues", "upload an audit", or "check compliance" are audit-only.
- During audit reconciliation, it is still correct to mark prior violations `resolved` when they are already fixed in the current code/UI. That status update is not the same as implementing a new fix.

## Audit Standards

Audit flow is strictly:

1. Start audit (`start_audit_run`).
2. Add violations as the agent finds them (`add_audit_violation` per finding).
3. Stop audit (`complete_audit_run`).

Fixing audit flow is separate and runs only when the user asks for remediation:

1. Implement the requested code/UI fixes.
2. Re-validate each fix.
3. Update individual violations as each one is fixed (`update_violation_status` per violation).

Audit workflow is mandatory and always two-phase:

1. Reconcile previous audits first.
2. Start and upload a new audit run.

When the user asks for an audit, always run phase 1 before phase 2.
When auditing, regardless of previous conversation context, always execute this full flow and always perform ruleset-based validation against the configured `auditRuleSetIds`.

Audit depth is mandatory:

- Audit each and every relevant page and each and every relevant component in scope.
- Produce granular findings per page/component (do not collapse multiple issues into one vague item).
- Include exact artifact context in every finding: page/screen, component name, file path, and line/snippet when available.
- Component-level adherence is required for every audit: validate border radius, spacing, typography, color/semantic token usage, shadow/border treatment, and interaction states against `design-studio.yaml` and linked rulesets.

Before uploading an audit:

1. Identify the configured app and rulesets from `chai-studio.yaml`.
2. Get previous audits with `get_audits` for the same `applicationId`.
3. For relevant prior runs, fetch findings with `get_audit_violations`.
4. Verify in current code/UI whether prior issues are fixed.
5. For each verified fix, call `update_violation_status` before the new run.
6. Audit the actual files or UI surfaces requested by the user.
7. For each audited component, explicitly check design and rule adherence (including border radius and token-level styling fidelity).
8. Classify each finding into supported MCP categories and severities before upload.
9. Report each violation with exact file path, line/snippet, why it matters, and a concrete suggested fix.
10. Ensure each finding is grounded in Chai Studio `design-studio.yaml` and/or ruleset guidance.
11. Upload only genuine findings unless the user explicitly asks for dummy/test audits.
12. Start one new audit run with `start_audit_run`, upload each violation immediately with `add_audit_violation`, then call `complete_audit_run` when finished. If there are zero violations, still start and complete the run.
13. Keep an in-memory set of uploaded finding fingerprints for the current run and skip repeats before calling MCP. Use at least `ruleId`, `filePath`, `lineStart`, `lineEnd`, normalized `codeSnippet`, and normalized `violationDescription` in the fingerprint.
14. If `chai-studio.yaml` has multiple `auditRuleSetIds`, audit each ruleset separately. For every ruleset, create one audit run, evaluate that ruleset's rules, upload only findings from that ruleset to that run, then complete that run before moving on or after finishing the ruleset's pass.

Browser/runtime validation:

- If Chrome DevTools MCP, Playwright MCP, or equivalent browser MCP tooling is available, ask the user whether they want browser tests and runtime review through those MCPs before running them.
- If the user agrees, open the app and validate in runtime in addition to static code review.
- Use browser/devtools-style checks for rendered behavior: accessibility tree/labels, keyboard flow, focus handling, responsive behavior, and interaction states.
- Record whether each finding came from static review, runtime validation, or both.

Build verification:

- Once write changes are complete, always run the project build command when one exists (`build` script, framework build command, or documented equivalent).
- Run the build before final audit upload when feasible, so audit results reflect buildable code.
- If the build cannot run because dependencies, environment variables, or tooling are missing, report the exact blocker and run the strongest available fallback checks.

Each uploaded violation must include a self-contained `aiFixPrompt` that another agent could use without reading the whole conversation.

Chai Studio validation constraints to respect:

- `complete_audit_run.status` must be `completed` or `failed`.
- Use streaming uploads only (`start_audit_run` -> `add_audit_violation` -> `complete_audit_run`).
- `severity` must be one of: `critical`, `high`, `medium`, `low`.
- `category` must be one of: `accessibility`, `visual`, `typography`, `color`, `layout`, `motion`, `interaction`, `responsive`, `metadata`, `performance`, `content`.
- Provide line numbers as positive integers when present.

## Status Updates And Fix Flow

Only mark a violation resolved after verifying the code or UI changed. Use:

- `resolved`: fixed and verified.
- `ignored`: intentionally accepted by the team or outside scope.
- `false_positive`: rule did not actually apply.

When changing statuses, include the resolver identity when available.

When running audits, status reconciliation is mandatory:

- Always check previous audits first.
- Resolve already-fixed violations before creating a fresh audit run.
- Do not skip the new run after reconciliation.

Fix workflow requirement:

- Only run this flow when the user asks to fix, remediate, resolve, close, or update audit entries.
- When the user asks to fix audit entries, implement code/UI fixes for the selected violations.
- After each fix, re-validate (runtime when available).
- Then call `update_violation_status` so each fixed item is marked appropriately (`resolved`, `ignored`, or `false_positive` with evidence).

## Safety

- Do not create dummy audits unless the user asks for test data.
- Do not create or update local design-spec mirror files (`DESIGN.md`, `DESIGN-RULES.md`, `design.yaml`, or alternatives) as part of this skill. Keep only `design-studio.yaml` synced from Chai Studio.
- Do not migrate UI libraries, rewrite the design system, or refactor broad UI areas just to satisfy an audit.
- Prefer Chai Studio IDs and tokens over memory or guesses.
