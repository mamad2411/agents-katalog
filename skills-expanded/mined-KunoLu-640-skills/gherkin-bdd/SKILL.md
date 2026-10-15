---
name: gherkin-bdd
description: Use when adding, changing, reviewing, testing, synchronizing, or read-only ingesting user-visible behavior with BDD, Gherkin, Given/When/Then scenarios, .feature files, acceptance criteria, knowledge catalogs, or bug-fix behavior specs.
---

# Gherkin BDD

Use this Skill for user-visible behavior. In strict tasks, new or changed behavior that a user, administrator, API client, CLI user, integration system, exported file consumer, notification recipient, or permission/error-state observer can see must have a persistent BDD scenario before implementation is completed. In default/lite tasks, apply this Skill when user-visible behavior, project rules, risk, or explicit delivery requirements call for persistent behavior evidence.

BDD does not replace PRD, DDD, TDD, project validation, or task workflows. It turns confirmed acceptance behavior into executable examples. PRD explains intent and scope, DDD stabilizes vocabulary and boundaries, BDD specifies observable behavior, and TDD turns the scenario into red tests and green implementation.

## When To Use

Use this Skill when:

- The user asks for BDD, Gherkin, Given/When/Then, `.feature`, scenarios, acceptance criteria, or behavior specs.
- A task adds or changes UI, API, CLI, exported files, notifications, permissions, errors, status changes, or externally observable integration behavior.
- A user-visible bug is being fixed.
- A task has acceptance criteria that describe user-visible behavior.
- Existing code needs BDD coverage backfilled for touched behavior.
- A knowledge system needs to read repository-owned `.feature` files from configured refs without modifying them.

Skip BDD only when the change is not user-visible, such as internal refactoring, dependency or tool configuration, purely mechanical formatting, or visual/text-only polish that does not change behavior or meaning. When skipping after code changes, report the reason.

## Persistent Spec Location

Project conventions win:

1. If the project already has `.feature` files, a `features/` directory, or BDD runner configuration, follow the existing path, language, and naming style.
2. Otherwise, single-application projects use `<project-root>/features/<capability-slug>.feature`.
3. Larger projects may group by capability area, such as `features/authentication/login.feature` or `features/orders/order-cancellation.feature`.
4. Monorepos use the owning workspace root, such as `apps/web/features/checkout/cart-update.feature`, `services/billing/features/invoice-export.feature`, or `packages/cli/features/project-init.feature`.
5. Cross-package behavior belongs near the product entry point that owns the observable capability, not in every internal package.

Task artifacts can draft or reference scenarios, but they are not the default long-term behavior source of truth. Use another persistent BDD path only when project-level rules explicitly define it.

## Language Rules

- Existing `.feature` files define the language and keyword style for their bounded context or feature area.
- If no `.feature` files exist, write scenario titles, descriptions, and step text in Simplified Chinese by default.
- Use English Gherkin structural keywords by default: `Feature`, `Rule`, `Background`, `Scenario`, `Scenario Outline`, `Examples`, `Given`, `When`, `Then`, `And`, and `But`.
- Do not add `# language: zh-CN` when using English Gherkin keywords. Add it only when the project already uses localized Chinese Gherkin keywords or the user explicitly requests them.
- Avoid mixing keyword languages inside the same bounded context or feature area.
- Domain terms must follow the project glossary, `docs/CONTEXT.md`, context docs, `docs/spec`, and existing scenario vocabulary.

Before creating or rewriting a `.feature` file, make an explicit language decision:

1. Inspect existing `.feature` files, BDD runner configuration, and project-level BDD rules.
2. If matching `.feature` files already exist, follow the nearest bounded context or feature area language and keyword style.
3. If no `.feature` files exist and the user did not request another language, set scenario text language to Simplified Chinese, Gherkin keyword language to English, and omit `# language: zh-CN`.
4. Report the chosen scenario text language and keyword language before writing or patching the file.

Do not infer English scenario text merely from English Gherkin keywords, English PRD / design documents, code identifiers, package names, or product names. Proper nouns and established domain terms may remain in their project vocabulary inside Chinese sentences.

Default first-file pattern:

```gherkin
Feature: 用户登录
  用户需要使用账号进入工作区，以便继续管理自己的配置。

  Scenario: 已注册用户使用正确密码登录
    Given 用户已经注册账号
    When 用户提交正确的邮箱和密码
    Then 用户进入自己的工作区
    And 页面显示当前登录状态
```

## Scenario Rules

Write scenarios as product behavior, not implementation:

- Name `Feature` after the user-visible capability, not the implementation component.
- Use one behavior per scenario.
- Make scenarios independent and chronologically executable.
- `Given` states relevant preconditions.
- `When` states one user or system action.
- `Then` states visible, persisted, returned, emitted, or otherwise externally observable outcomes.
- Prefer concrete, realistic examples over placeholders.
- Keep step text free of selectors, mocks, fixtures, database fields, internal function names, and test helper names unless the behavior is inherently at that layer.
- Use `Rule` only for a policy or invariant shared by multiple scenarios.
- Keep `Background` short and only for facts true for every scenario in the file.
- Use `Scenario Outline` only when an examples table covers the same behavior with meaningful input variations.

For user-visible wording or UI changes, require scenarios when the change affects meaning, decisions, validation, status, permissions, flow, defaults, or accessibility semantics. Skip scenarios for typos, spacing, color polish, token/class rewrites, or layout cleanup that does not change behavior or meaning.

## Split-Repository Gate

When the behavior crosses repositories, services, clients, or mobile app boundaries, do not let `.feature` become a guess. Before drafting or finalizing scenarios, classify the available evidence:

- `complete`: product behavior, contract, environment, account, data setup, and observable outcomes are known.
- `contract-only`: a reliable API contract, schema, fixture, or real response sample exists, but the full chain cannot run locally.
- `environment-only`: a runnable environment exists, but contract details, ownership, or expected side effects are incomplete.
- `missing`: key behavior, contract, environment, account, device, selector, data, or side-effect facts are absent.

For API behavior, confirm request shape, authentication, roles, status codes, response body, error codes, persistence side effects, emitted events, and external integrations from OpenAPI / Swagger, proto, GraphQL schema, backend docs, real samples, or user confirmation.

For Web, Mobile, or Hybrid journeys, confirm page or screen flow, stable selectors or accessibility names, backend dependency, test account, data setup and cleanup, base URL or environment switching, and platform-specific prerequisites. For iOS / Android, also confirm app artifact, bundle id / app id, simulator / emulator / device, permissions, deep links, launch arguments, and system UI requirements.

If evidence is `missing`, ask for the smallest missing fact that blocks a truthful scenario. If a scenario must be kept as a placeholder, tag it `@todo` or the project's equivalent marker and add an adjacent blocker comment. Mock-backed or app-mocked scenarios are allowed only when the mock behavior comes from a contract, real sample, existing fixture, launch argument, or explicit user confirmation; mark them as contract-backed, mock-backed, or app-mocked in the related test trace, and do not present them as full-chain verification.

## Workflow

1. Decide whether the change is user-visible and whether BDD is the selected behavior-evidence method for the current mode, project rules, risk, or explicit delivery.
2. Read existing `.feature` files and project vocabulary before drafting.
3. Run the language decision gate and report the chosen scenario text language and Gherkin keyword language.
4. For split-repository or incomplete-chain behavior, run the split-repository gate and record the evidence class before treating the scenario as confirmed.
5. If domain terms or boundaries are unclear, use `grill-with-docs` and `book-ddd-distilled-modeling` before finalizing scenario wording.
6. Create or update the persistent `.feature` file before implementation.
7. Review scenarios for observable behavior, one-behavior focus, vocabulary consistency, realistic examples, absence of implementation details, and compliance with the language decision.
8. Derive tests from scenarios. If the project has a Gherkin runner, bind scenarios to step definitions or runner tests. Otherwise use the existing test framework and make each test traceable to a scenario by name, comment, file organization, or the project's established convention.
   For Mobile / Hybrid E2E scenarios, use `maestro-mobile-e2e` to derive repo-resident Maestro flows when device-level coverage is needed.
9. For new behavior or bug fixes, run the derived test first and confirm it fails for the intended behavior before implementation when the project test setup supports red runs.
10. Implement the smallest change that makes the scenario-backed tests pass.
11. During validation, confirm PRD, `.feature`, tests, code, and any contract / mock assumptions agree.

If a scenario cannot be automated yet, tag it `@todo` or the project's equivalent marker and add an adjacent comment explaining the blocker and temporary manual verification. Do not silently drop it.

## Existing Code Backfill

For existing projects, use `no new uncovered behavior`:

- When BDD is the selected behavior-evidence method, touched existing behavior must get or update relevant scenarios.
- When BDD is selected for a user-visible bug fix, first add the correct behavior scenario, then a failing regression test, then the fix.
- Untouched legacy behavior can remain uncovered until it is changed, an explicit BDD migration is requested, or the current mode/project rules require backfill.

When backfilling from code, record what the code does today in product language. If behavior appears suspicious or contradicts docs, names, comments, tests, or obvious user expectation, ask whether it is intended. If it is a defect, write the intended behavior as the scenario and let the derived test go red.

## BDD Sync Mode

When this Skill is actively used and the user's request includes either `sync` or `同步`, enter BDD Sync Mode. This mode syncs project `.feature` files with current product behavior; it does not mean local Codex configuration sync and does not copy this repository's templates to any global path.

BDD Sync Mode is a full repository behavior audit, not a diff-only update:

1. Build a whole-repository inventory with the current working tree, including uncommitted changes. Check `git status --short`, relevant `git diff` output, and a complete file list such as `rg --files`. Do not rely only on committed `HEAD` or only on changed files.
2. Locate every project `features/` directory and existing `.feature` file under the project's conventions, including workspace-level paths such as `apps/web/features/`, `services/*/features/`, or the product entry repository's `features/`.
3. Scan the code and durable project facts that can define user-visible behavior: routes, pages/screens, API schemas, controllers, services, permission checks, validation rules, CLI commands, exported file formats, notifications, integration adapters, tests, PRD/design artifacts, `docs/spec`, context docs, and README / runbooks that describe externally observable behavior.
4. Before updating existing `.feature` files, decide whether the current repository contains enough evidence for a truthful full sync. If behavior depends on another repository, service, app, or backend/frontend split that is not present locally, treat the scope as multi-repository.
5. For multi-repository scope, ask the user whether the other repositories have changed. If yes, request the local paths and scan those repositories together before updating `.feature` files. If the user confirms the other repositories have no relevant changes, record that confirmation and sync only from the current repository's current working tree. If the user cannot confirm or provide required paths, mark the affected features `blocked` or `@todo` instead of guessing.
6. Compare code behavior to existing scenarios and decide, per feature area, whether to update, create, delete, or leave files unchanged. Create new `.feature` files for newly discovered user-visible capabilities that lack coverage. Delete stale `.feature` files only when the audited behavior clearly no longer exists or has been intentionally superseded; when uncertain, report a deletion candidate instead of deleting.
7. Preserve the language and naming style for each bounded context. If a new `.feature` file is needed and no local convention exists, use the default language rules from this Skill.
8. After editing, verify that PRD / `.feature` / tests / code agree as far as the available repositories allow, and report any remaining `contract-only`, `environment-only`, `missing`, `blocked`, or `@todo` areas.

BDD Sync Mode output must include:

- `BDD Sync Mode`: `run` / `blocked`.
- Scan scope: current repository path, additional repository paths scanned, and whether uncommitted changes were included.
- Multi-repository decision: current repository sufficient, user confirmed other repositories unchanged, extra paths scanned, or blocked waiting for paths / confirmation.
- Feature files updated, created, deleted, unchanged, and deletion candidates, each with a short behavior summary.
- Conflicts found between code, PRD, existing `.feature`, tests, or cross-repository contracts.
- Remaining gaps, `@todo` scenarios, and any user confirmation used to limit the scan.

## Knowledge Ingest Mode

When this Skill is actively used, enter Knowledge Ingest Mode only when the user's BDD or knowledge-base request has explicit read-only intent (`read` / `读取`), does not request `sync` / `同步`, and contains no mutation intent such as `add / change / update / delete` or `写入 / 新增 / 修改 / 更新 / 删除`. A request that asks to read existing behavior and then mutate it follows the normal BDD workflow, not Knowledge Ingest. This mode builds a derived knowledge view from repository-owned `.feature` files without updating source specifications. If the request includes `sync` or `同步`, BDD Sync Mode remains higher priority even when reading is also required.

When `knowledge-base-integration` is available, use its P1.1 runtime for registry validation, ref resolution, Revision Set creation, complete no-ID Gherkin catalog generation, static or manifest binding scan, conflict candidates, idempotency and metrics. This Skill retains the BDD/SOT rules; the integration Skill owns deterministic execution. This addition does not alter BDD Sync Mode.

Knowledge Ingest Mode follows these rules:

1. Read the requested repository paths, configured target refs, and feature roots. A target ref may be a branch, tag, or commit SHA. Prefer the knowledge-base or product registry configuration; otherwise require an explicit ref. Do not silently fall back from a missing configured ref to the current checkout or default branch.
2. Resolve every requested ref to an exact commit SHA before parsing. Record both the requested ref and the resolved SHA. The configured target branch, such as `staging`, identifies which revision is authoritative; the exact SHA identifies the immutable snapshot that was ingested.
3. Do not switch branches in a developer's active worktree. Read Git objects directly or use an isolated, disposable worktree or runtime directory when a checked-out tree is required.
4. Parse the repository-owned `.feature` files without writing to the source repository. Capture repository key, ref, resolved SHA, feature path, Gherkin language, Feature, Rule, Scenario / Scenario Outline, Examples, tags, and source line where available.
5. Do not require or add Feature IDs, Scenario IDs, ownership tags, new naming conventions, or a Gherkin runner. Existing `.feature` content and project conventions remain unchanged.
6. Use a composite source locator such as repository key + feature path + Feature / Rule / Scenario name + Examples fingerprint + resolved SHA. Treat it as an ingestion locator, not a new persistent identifier written back to `.feature`.
7. Treat the aggregated behavior catalog as a derived, rebuildable view. The `.feature` files on each configured target ref remain the behavior source of truth. Similar or conflicting behaviors across repositories are overlap / conflict candidates for human review; do not automatically merge, rewrite, move, or delete them.
8. Do not create, update, delete, rename, or reformat `.feature` files, tests, reports, manifests, or source code. `Mutation` must remain `none`. If the requested ref, repository, or feature root cannot be read, report `partial` or `blocked` rather than guessing.

Knowledge Ingest Mode output must include:

- `Knowledge Ingest`: `run` / `partial` / `blocked`.
- For each repository: repository key or path, requested ref, resolved commit SHA, feature roots, parsed file / feature / scenario counts, and read status.
- Source locators for parsed behavior without requiring persistent Feature or Scenario IDs.
- Cross-repository overlap or conflict candidates, with evidence and confidence stated as candidates rather than SOT changes.
- Missing refs, unreadable repositories, parser gaps, unsupported Gherkin constructs, and any resulting coverage limitation.
- `Mutation`: `none`.

## Source Of Truth

For confirmed user-visible behavior, the persistent `.feature` file is the behavior source of truth.

- `prd.md` holds background, scope, constraints, non-goals, and acceptance intent.
- `.feature` holds the testable behavior examples.
- `design.md` and `implement.md` hold technical decisions and plans.
- Tests prove the implementation matches the scenarios.

If PRD, task artifacts, `.feature`, tests, and code disagree, do not implement through the conflict. First align the PRD and `.feature`, then adjust tests and code.

## Output

When drafting or updating BDD specs, report:

- Whether BDD Sync Mode was requested and, if so, the scan scope and multi-repository decision.
- Whether Knowledge Ingest Mode was requested and, if so, the repository / ref / resolved SHA scope, ingestion status, and `Mutation: none`.
- Feature files created or updated.
- Feature files deleted, unchanged, or proposed for deletion when BDD Sync Mode is used.
- BDD language decision: scenario text language, Gherkin keyword language, and whether it follows existing project convention or the first-file default.
- Split-repository evidence class when relevant: `complete` / `contract-only` / `environment-only` / `missing`.
- Scenarios added, changed, removed, or marked `@todo`.
- How each scenario is or will be traced to automated tests.
- Whether any derived test is `full-stack`, `contract-backed`, `mock-backed`, `app-mocked`, `smoke-only`, or `blocked`.
- `Mock Strategy`: `none` / `contract-backed` / `user-approved` / `blocked`, when a derived test cannot run against the complete real chain.
- Any BDD skip decision and reason.
- Any conflict found between PRD, existing `.feature`, tests, and code.
