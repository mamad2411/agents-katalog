---
name: gh-create-issue
description: Create high-quality GitHub issue tickets from identified problems, bug reports, technical debt, feature gaps, or refactoring requests. Use when a user asks to create, draft, open, file, split, or prepare GitHub issues in an online repository, especially when the work needs clear problem statements, requirements, goals, subtasks, acceptance criteria, SOLID design expectations, clean architecture guidance, safe legacy cleanup, validation steps, and durable tests.
---

# GitHub Issue Creation

**Session shape:** inline sub-skill — loaded into the calling agent's context
(gh-refine epic conversions, gh-resolve / gh-fixer deferred-scope follow-ups);
fully runnable standalone.
**Conventions scope:** read only §§1, 2, 3 of
the pipeline CONVENTIONS.md — resolve it at `gh-workflow/CONVENTIONS.md`
alongside this installed skill set, else `agents/gh-workflow/CONVENTIONS.md` in
the skill source repo (github.com/JAndrew13/agent-skills); it is NOT in the
target repo. `grep -n "^## "` it for section offsets and read just those
ranges; open any other section only at the moment a step cites it.

## Overview

Turn a discovered problem or requested change into one or more GitHub issues that a capable but context-poor agent can implement without ambiguity. Prefer clear, testable tickets over broad narratives.

**Taxonomy, statuses, the state machine, and the project board are owned by
[`CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md).** This skill
**references** those sections (title tags §1, kind labels §2, the board §3)
and **never restates** their tables — re-inlining any of them here is the
duplication debt that file exists to prevent. Refinement (premise validation,
Complexity/Blast Radius scoring, epic conversion) is now its own pipeline
stage (`gh-refine`, #672): this skill's job is to author a ticket at the
evidence/AC quality bar below and land it on the board in the correct
starting state, not to fully refine it at authoring time.

## Workflow

1. Confirm repository context.
   - Use the GitHub app or `gh` when available to identify the target owner, repo, existing related issues, the label set (`gh label list` — see [Labels](#labels), CONVENTIONS.md §2), and issue templates.
   - If the target repo is not discoverable and multiple repos are plausible, ask one concise question before creating tickets.
   - If the user asks only to draft, do not create the issue online unless they later approve creation.

2. Gather evidence before writing.
   - Inspect local code, failing tests, logs, PR comments, user reports, or relevant docs.
   - Validate facts directly whenever possible. Do not encode assumptions as requirements.
   - Link files, functions, test names, logs, screenshots, or reproduction steps that explain the problem.

3. Decide whether to split the work.
   - Create one issue when the work has a single coherent goal and one implementation path.
   - Split into subtasks when the work spans multiple modules, requires independent design decisions, mixes refactor and behavior change, or contains separable testing and migration work.
   - Make each subtask independently actionable with a specific scope, explicit dependencies, and completion criteria.

4. Write the issue body.
   - Start with the user-visible or engineering problem, not the proposed code change.
   - Separate facts from hypotheses.
   - Include the goal, non-goals, requirements, acceptance criteria, implementation guidance, validation plan, and test expectations.
   - Name expected SOLID design considerations when relevant: single responsibility, dependency inversion, interface boundaries, open/closed extension points, and avoiding inheritance or abstraction unless it earns its keep.
   - Require solutions to be encapsulated behind clear module, class, function, or service boundaries so future changes do not leak across unrelated parts of the system.
   - Require relevant README, CLI help text, command documentation, tests, and MCP server behavior or docs to be updated when the issue changes development behavior, user workflows, commands, integrations, or removals.

5. Create or present the issue.
   - Title the issue with the **`[TAG] AREA - description` convention** — see [Title convention](#title-convention) (CONVENTIONS.md §1). This is required for every newly authored issue.
   - If authorized to create online, use the GitHub app or `gh issue create`.
   - Apply the right **kind/category label(s)** at creation — see [Labels](#labels) (CONVENTIONS.md §2). This is a required step, not optional; pick the label(s) matching the work, reconciled against live `gh label list`. Map the title's `[TAG]` to its label where one exists (see [Title convention](#title-convention)).
   - **Put the issue on the board at its starting Status** (CONVENTIONS.md §3 — the "Getting issues onto the board" contract; do not skip this): run `gh project item-add <board-number> --owner <board-owner> --url <issue-url> --format json` to add the just-created issue to the project board — pass `--format json` and capture its `.id` (a `PVTI_...` board item id; without `--format json` the id is not printed) — then `gh project item-edit --id <that PVTI_... item id> --project-id <project-node-id> --field-id <status-field-id> --single-select-option-id <option-id:Needs Refinement>` to set its Status to `Needs Refinement` — so no issue ever lands on the board with an unset Status. **Exception:** for a bulk/operator far-future ticket seeded ahead of its sprint, set Status to `Backlog` (`<option-id:Backlog>`) instead of `Needs Refinement` (the §3 override — the sweeper never dispatches `Backlog`). Never apply a status *label* — status is board-owned only (the D1 veto). *(All `<…>` ids resolve from PROFILE.md, per CONVENTIONS.md §3 — if they ever drift, the profile is authority; update there, not here.)*
   - Apply assignees, milestone, and project fields only when known or requested.
   - After creation, return the issue URL(s), its board Status, and a short summary of any split/dependency structure.

## Title convention

Every newly authored issue title MUST follow this single format:

```
[TAG] AREA - Concise action-oriented description
```

- Examples: `[EPIC] WEB UI - Build a new dashboard website`; `[CHILD] WEB UI - Make a button for the dashboard`; `[TASK] CONFIG - Add a volatility entry gate setting`.
- `[TAG]` is one value from the **closed set owned by [`CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md) §1** — do not invent new tags and do not restate the set here; reconcile against §1 if in doubt.
- `AREA` is a short, consistent component/scope tag in caps (e.g. `WEB UI`, `BACKTEST`, `CONFIG`, `MCP`, `GH WORKFLOW`). Reuse an existing area when one fits rather than coining a near-duplicate. **Children reuse their parent epic's `AREA`** so an epic and its children are scannable as one group.
- The description is the action-oriented phrase from [Splitting Rules](#splitting-rules) (good titles say what changes and where).

See CONVENTIONS.md §1 for the closed tag table (including which tags were
retired and moved to kind labels) and §2 for how each tag maps to a kind
label at creation (e.g. `[EPIC]`/parents → `architecture`; a `[CHILD]` carries
its own kind label, never `architecture`).

## Labels

Apply a **kind/category** label at creation so the ticket is triageable —
the full label table (with each label's meaning and lead action) lives in
[`CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md) **§2**; this
skill does not keep a second copy. Always reconcile against live
`gh label list` at authoring time — labels are added/renamed in GitHub, not
in either doc. **Status is never a label** (board-owned only — §3; see
[Step 5](#workflow) for the creation-time board contract).

## Issue Format

Use this structure unless the repository issue template requires a different one:

```markdown
## Problem

Describe the verified problem, observed behavior, impact, and evidence. Include reproduction steps or links when available.

## Goal

State the desired end state in one or two sentences.

## Requirements

- Concrete requirement that can be verified.
- Concrete requirement that cannot be misread by another agent.

## Design Guidance

- **Reuse this repo's canonical components — do not regrow duplication.** For work touching `/src`, point the worker at `CLAUDE.md`'s contribution standard: route exit logic through the shared exit engine (`monitoring/exit_policy.py` / `exit_engine.py`), add config settings in the registry (`server/config_loader.py` `CONFIG_FIELDS`), pass typed domain objects across boundaries (not raw dicts), run post-model policy through `services/entry_gates.py`, and use typed `Protocol` ports. Prefer this concrete standard over generic SOLID advice when the repo has a canonical home.
- Keep responsibilities focused and dependencies explicit.
- Encapsulate behavior behind cohesive classes, functions, or interfaces with narrow public contracts.
- Prefer reusable interfaces or small composable helpers where they reduce duplication or isolate change.
- Clean up nearby legacy code only when it directly supports the issue goal and can be validated safely.
- Preserve existing behavior unless the issue explicitly changes it.
- Add file header comments or function comments when they clarify intent, invariants, side effects, integration constraints, or non-obvious design choices. Avoid comments that merely restate the code.
- Update relevant READMEs and user-facing docs for all new development, updates, deprecations, and removals.
- Keep CLI documentation and `--help` output aligned with supported commands, options, defaults, examples, and error behavior.
- Keep MCP server tools, schemas, prompts, documentation, and tests current when the issue affects MCP-facing behavior.

## Acceptance Criteria

- Observable criterion for completion.
- Observable criterion for completion.

## Validation

- Unit/integration/regression tests to add or update.
- Manual or automated verification commands.
- Edge cases and failure modes to cover.

## Notes

Relevant files, related issues, risks, constraints, or open questions.
```

## Splitting Rules

When splitting work, create a parent issue plus child issues or a numbered issue set.

Parent issue:
- Define the full problem and target outcome.
- List child issues with dependency order.
- Keep acceptance criteria at integration level.
- Avoid implementation details that belong in child issues.

Child issue:
- Scope one coherent unit of implementation.
- Include exact files or components to inspect when known.
- State prerequisites and what must not be changed.
- Include local tests and validation specific to that unit.

Prefer titles that follow the [Title convention](#title-convention) — `[TAG] AREA - action-oriented description`:
- `[BUG] ORDERS - Fix order reconciliation when partial fills arrive out of order`
- `[TASK] MARKET DATA - Extract market data normalization behind a reusable interface` (kind label `Refactor` — see CONVENTIONS.md §1 on the retired `[REFACTOR]` tag)
- `[TASK] WEBSOCKET - Add regression coverage for reconnect backoff`
- `[EPIC] BACKTEST - Rework the backtest exit-parity harness` with children `[CHILD] BACKTEST - …` (children reuse the parent's `AREA`).

Avoid titles that are vague or skip the convention:
- `Improve code`
- `Fix bug`
- `Refactor system`
- `Add a button` (no `[TAG]` prefix, no `AREA` scope)

## Quality Bar

Every issue should be specific enough that another agent can start without asking what the ticket means. Include constraints that protect maintainability:

- Favor clean code, clear names, small units, and explicit contracts.
- Require strong encapsulation: keep state ownership local, expose minimal APIs, and avoid scattering business rules across call sites.
- Avoid broad rewrites unless the evidence shows the existing design blocks the goal.
- Ask for comments in file headers and on functions when they communicate purpose, constraints, or rationale that a future maintainer would not infer quickly from names and types.
- Require durable tests for bug fixes and behavior changes.
- Require all relevant tests to pass before completion, and specify the commands to run when discoverable.
- Require README updates whenever user-visible behavior, setup, CLI usage, integration contracts, or operational workflows change.
- Require CLI commands to be explained both in README-level documentation and in command help output.
- Require MCP server updates when affected by the change, including tool schemas, handler behavior, documentation, and validation coverage.
- Include cleanup of obsolete or duplicated code only when it is safely bounded.
- Require validation commands or repository-specific test targets when discoverable.
- Call out risks, migrations, compatibility concerns, and rollback considerations when relevant.

### App version bump (main-targeting tickets only)

The app carries one canonical version (the profile's `<version-file>`, read
via `<version-read-command>`), and it bumps once per relevant change that merges to `main`.
When authoring a ticket whose work will touch files under `/src`, `/scripts`,
`/agents`, or `/tests`:

- If the ticket is **main-targeting** — a standalone ticket or an **epic/parent**
  whose PR merges to `main` — include a "bump app version" item in its acceptance
  criteria. Use a **patch** bump for a normal change (advance the third semver
  position); call out any deliberate minor/major bump.
- **Child issues are exempt.** Children land on the epic branch, not `main`, so a
  child ticket must **not** carry a version-bump item — the epic's single merge to
  `main` performs one bump for the whole change, preventing N child bumps from
  colliding. (The `gh-lead` role performs the bump at merge time; this rule only
  ensures the requirement is written on the right tickets.)
- A ticket touching none of those four directories (e.g. docs-only) does not need
  a version-bump item.

## Acceptance criteria that can't be gamed (secure / refactor-safe standard)

Most escaped defects in this codebase passed a *green* gate — the gate measured a
proxy, not the property. When writing requirements and acceptance criteria, make
the criterion fail when the goal is unmet, not merely when an unrelated proxy is:

- **Test the property, not a proxy.** "Parity test green" is not "the modes are
  identical" if the test feeds only constant/hand-picked inputs that make the
  property trivially true. Require inputs that *could* expose a divergence
  (moving/varied/boundary/fuzzed values), and — for any bug fix — require a test
  that is shown to FAIL without the fix (negative/adversarial test). State this
  in Validation, e.g. "add a moving-price scenario; verify it fails on `main`."
- **"Built" is not "wired."** For any ticket that adds infrastructure (a
  registry, validator, typed boundary, helper, gate), the acceptance criteria
  MUST require a *production* caller — not just tests. Add a criterion like
  "`grep` shows the execution path calls X" and a test that exercises X through
  the real entry point. A symbol used only by its own tests is dead
  infrastructure even if coverage/vulture are green.
- **The code owns defaults and ranges; reference docs are illustrative.** READMEs
  and example templates are references, not a second source of truth — config
  values work within ranges and a template shows one valid example, not "the"
  default. Update them in the same change as a behavior change (co-locate), but do
  NOT build heavy guards that pin reference values to code defaults; enforce
  *behavior* (the code's default + range validation), not documentation prose.
- **Scope gates to intent, and define them with the work — not after.** A
  coverage floor that excludes the module the ticket hardens, or a size budget
  written *after* a decomposition to grandfather the leftovers, certifies the
  goal by definition. Require the gate's scope to cover the code the goal is
  about, and prefer defining the gate in (or before) the same change as the work
  it polices.
- **No silent caps.** If a ticket bounds coverage (allowlist, `--deselect`,
  sampling, "grandfather"), it must say so loudly in code/comments AND file a
  tracked follow-up issue with the unfinished scope. "Grandfathered for safety"
  must read as "incomplete, tracked in #N," never as an intended end state.

### Parent / epic issues: require an integration-acceptance pass
A pipeline of independently-resolved child issues produces seam bugs (built-not-
wired, gate-scope, partial migrations) that no single child owner sees. The
parent issue MUST include a final, explicit **integration-acceptance** task,
performed after all children land, that re-verifies *each* integration acceptance
criterion against the composed whole — independently of the child PRs that
claimed them — and is adversarial (tries to break the criterion, defaults to
"unmet" when unsure). Treat partial migrations as incomplete: if a mechanism is
applied to the easy cases and the hard cases keep the old pattern, the criterion
is not met even if every child PR is green.

## Creation Checklist

Before creating the issue online:

- Verify the repo and branch/context are correct.
- Search for related open issues to avoid duplicates when practical.
- Confirm whether the user wants online creation or a draft if intent is unclear.
- Ensure the title is action-oriented and scoped.
- Ensure requirements and acceptance criteria are testable.
- Ensure validation does not depend on assumptions or unavailable services unless explicitly stated.
- Ensure docs, CLI help, README updates, passing tests, and MCP server updates are included whenever relevant.
- Apply the correct **kind/category label** at creation — see [Labels](#labels) (CONVENTIONS.md §2); reconcile against live `gh label list`. Never apply a status label.
- Put the issue on the project board (`<board-name>`, PROFILE.md) and set its starting Status (`Needs Refinement`, or `Backlog` for the seeded-ahead override) per [Step 5](#workflow) / CONVENTIONS.md §3 — every created issue must land with a Status set.
