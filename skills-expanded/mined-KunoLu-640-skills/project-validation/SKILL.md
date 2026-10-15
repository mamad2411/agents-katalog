---
name: project-validation
description: Use after code changes to choose and run validation commands for Node, JavaScript, TypeScript, Python, Go, Dart, Java, Kotlin, C++, Swift, or Objective-C projects. Prefer project-defined commands and report skipped checks and risks.
---

# Project Validation Skill

Use this Skill after code changes.

## General Rules

- Prefer commands already defined by the project.
- When `rtk` is available, prefer `rtk` for non-reporting commands; for unit tests, API / integration tests, Playwright Web E2E, Maestro Mobile / Hybrid E2E, or any command that must generate report files, first apply the `rtk` and reporting-test Gate.
- Do not bypass project configuration.
- Do not modify lock files unless required by the task.
- If full checks are expensive, run focused checks first.
- State which checks were skipped and the remaining risks.

## `rtk` and Reporting-Test Gate

`rtk` is a command-output compression layer, not a test runner. Before executing validation commands, first distinguish between “only terminal facts are needed” and “file side effects must be produced.”

- lint, typecheck, static analysis, build, read-only checks, or diagnostic commands that do not depend on persisted reports can generally prefer `rtk`.
- If unit tests, API / integration tests, Playwright Web E2E, Maestro Mobile / Hybrid E2E, Flutter / Xcode / Gradle / Maven, or similar test commands need to retain coverage, JUnit, HTML, JSON, trace, raw report, or Markdown summaries in the current run, use the project-native command by default, or a no-cache / report-safe command explicitly provided by the project.
- Wrap a reporting-test command with `rtk` only after confirming that `rtk` will not produce a cache hit, replay output, or skip the runner’s file-writing side effects for that command, and that the report path can be verified.
- If a reporting test has already been executed with `rtk`, verify that the expected report files exist, that their mtime / size changed after the current run, and that their contents correspond to the current command and case / spec / flow. If a file is missing, stale, empty, has mismatched contents, or the output shows a cache hit / replay / skipped write, immediately rerun with the native command and treat the native-command result and persisted reports as authoritative.
- stdout results from custom API scripts, Playwright, Maestro, or unit runners cannot replace the report-file gate; when such a command is part of formal validation, it must persist a raw report / native report and a same-stem Markdown summary, or be marked blocked.
- The final output must report `rtk`: `used` / `skipped-for-report` / `fallback-native` / `not-available` / `not-needed`, and explain the reason.

## Book-Derived Validation Supplement

Project validation is responsible for selecting and running commands such as lint / test / build / typecheck; it does not replace book-derived skills.

For production-path-related changes to services, APIs, background jobs, queues, external integrations, data pipelines, or deployment-sensitive components, after basic project validation you must proactively determine whether to invoke `book-release-readiness`. If validation exposes risks involving data consistency, migration, replay, idempotency, or cross-service data flows, return to `book-ddia-data-design` to complete the design / check conclusions before finishing.

This step records only the current task’s risks, validation gaps, and remaining risks; do not add task-unrelated refactoring or test frameworks because of the production risk review.

## BDD / Gherkin Validation Supplement

When the task adds or modifies user-visible behavior, or the diff contains `.feature` / persistent BDD specification paths, BDD consistency must be validated.

Return scenario authoring, review, or backfilling issues to the `gherkin-bdd` Skill; this Skill is responsible only for selecting and executing post-change validation and reporting risks.

Check in this order:

1. Confirm whether the user-visible behavior has a corresponding persistent BDD scenario; when skipping pure internal changes or semantically neutral UI polish, record the reason for skipping.
2. Check whether the language decision for `.feature` / persistent BDD specifications has been followed and is consistent with the file contents:
   - If the project already has `.feature` files, additions or modifications must follow the existing Gherkin language and keyword style of the same bounded context or functional area.
   - If the project previously had no `.feature` files and the user has not explicitly requested another language, scenario titles, descriptions, and step text in new `.feature` files must be in Chinese by default; use English for Gherkin structural keywords.
   - English product names, code identifiers, and domain-specific names may remain in English, but an entire new `.feature` file must not be written in English.
   - Do not rely only on `git diff --check` to determine language correctness; manually review it, or use lightweight checks to help identify obvious violations.
3. If the project previously had no `.feature` files, and a new `.feature` file contains no Chinese characters outside comments, tags, tables, doc strings, and structural keywords, with no user override or project-rule override, mark `BDD` as `blocked` and return to `gherkin-bdd` to correct the language first.
4. If the project already has a Gherkin runner, such as Cucumber, behave, pytest-bdd, or cucumber-js, or has a BDD command in a package / Makefile / CI configuration, prefer the project-defined BDD command.
5. If there is no Gherkin runner, do not proactively introduce a new framework; use the project’s existing test framework to run unit / integration / E2E tests traceable to the scenarios.
6. Confirm that every added or modified scenario is traceable to an automated test. Traceability may use test names, comments, directory structure, or project conventions.
7. Scenarios that cannot be automated must have `@todo` or a project-equivalent marker, the blocking reason, and temporary manual-validation instructions.
8. If the PRD, `.feature`, tests, and code conflict, return to specification alignment first; do not use validation results to conceal the conflict.
9. For separate frontend and backend repositories, cross-service flows, Web + API, Mobile + API, or Hybrid flows, check whether context completeness has been recorded as `Cross-repo context`: `complete` / `contract-only` / `environment-only` / `missing`.
10. When mocks are needed, confirm that mock behavior comes from an API contract, schema, real response sample, existing fixture, or user confirmation; otherwise mark `Mock Strategy` as `blocked` and do not generate tests using guessed mocks.

The final output must state:

- `BDD`: `run` / `traceable` / `blocked` / `skipped`.
- The affected `.feature` or persistent BDD specification paths.
- BDD language status: following the project’s existing style, default Chinese scenario text + English keywords, explicit user override, or the reason for `blocked`.
- The BDD runner or traceability-test command that was run.
- `Cross-repo context`: `complete` / `contract-only` / `environment-only` / `missing`; state `not-needed` if not relevant.
- `API Contract`: `verified` / `user-provided` / `stale` / `missing` / `not-needed`.
- `Mock Strategy`: `none` / `contract-backed` / `user-approved` / `blocked`.
- Unautomated scenarios, blocking reasons, and remaining risks.

## Validation Evidence Sources and Version Contract

Apply `references/validation-evidence-contract.md` only when formal test reports must serve as PR evidence or be read by the knowledge base. Ordinary local diagnostics, unpublished debugging reports, and one-off troubleshooting do not require an evidence sidecar.

When the project has a configured product registry, invoke the `decision` entry point of `knowledge-base-integration` to determine the Evidence Contract, Intent, and Targets; do not infer the purpose from report directories, branch names, or arbitrary CI environments. Knowledge-server smoke is generated by that Skill’s `smoke` entry point as a P1.1 bundle; this Skill remains responsible for project-native validation and the report-quality Gate. P1.1 accepts only runner reports newly created or refreshed after the current command began and same-stem Chinese Markdown; the aggregate envelope must reference the artifact manifest, checksums, and actual runner attestation. Evidence must not be marked as passed when it is stale, missing, not in Chinese, has inconsistent stems, has inconsistent report checksums / digests, fails schema / semantic validation, or comes from an untrusted environment.

- Developer-local evidence uses `Evidence Source: developer-local`; evidence generated by a CI runner uses `Evidence Source: ci`; independent revalidation by the knowledge-base server uses `Evidence Source: knowledge-server`. These three must not overwrite or impersonate one another.
- Formal evidence must record the repository key, original source ref, full commit SHA, worktree state, trigger, and creation time. `branch_slug` is used only for filenames and is not a code-version identifier.
- A dirty worktree may only be marked `Source Revision: dirty` and `Evidence Publication: local-only`; it cannot serve as formal proof of the PR head.
- PR evidence must exactly match the current PR head SHA; old evidence automatically becomes invalid after a new commit is added.
- Results produced before the Phase 3.4 commit plan or before creating a commit may only be recorded as local evidence status. After committing, and before publishing or updating the PR Check, evidence must be regenerated or revalidated against the final PR head SHA, and the same-stem sidecar / aggregate envelope must be updated; this applies to both `developer-local` and `ci`.
- `ci` evidence must come from a clean checkout and use `Source Revision: exact`. CI execution does not mean the evidence has been published: mark it `published` only after the target system receives it, `not-configured` when no publisher is configured, and `blocked` when publication is required but fails; CI evidence must not be marked `local-only`.
- Knowledge-base-server evidence must record the exact revision set of all participating repositories and record `Environment Alignment`. When a target branch such as `staging` is specified, resolve it to an exact SHA before running.
- `.feature` files are not required to add Feature IDs or Scenario IDs. Identify behavior sources using the repository key, feature path, Feature / Rule / Scenario name, optional Examples fingerprint, source ref, and SHA.
- Generic or historical report evidence continues to use `references/validation-evidence.schema.json` (`schemaVersion: 1`). v1 `featureSources[]` plus `reports[]` co-membership is not BDD traceability. The v1 Schema only checks digest shape; producers and consumers must recompute each referenced report SHA-256 against file bytes and reject mismatches.
- Scenario-backed execution evidence must use `references/validation-evidence.v2.schema.json` and `scripts/validate_validation_evidence.py`. The validator must parse SHA-verified `junit-xml-v1` or `playwright-json-v1` bytes and require the matched passed case to carry `sbtd.sourceLocatorDigest` equal to the recomputed locator. HTML/TXT/arbitrary JSON and sidecar labels alone fail closed.
- Each formal report may generate a same-report-stem `.evidence.json` in the same directory; a cross-tool orchestrator may also generate one aggregate envelope in an isolated runtime / evidence bundle. Every envelope must pass the matching Schema, and v2 envelopes must also pass the semantic validator.
- Evidence must be sanitized before publication. `published` only means that the target system has received the evidence; it does not mean the tests passed, and `smoke-only`, `contract-backed`, `mock-backed`, or `app-mocked` must not be promoted to `full-stack`.

For relevant tasks, additionally report in the final output:

- `Evidence Source`: `developer-local` / `ci` / `knowledge-server` / `not-needed`.
- `Source Revision`: `exact` / `dirty` / `unknown` / `not-needed`.
- `Environment Alignment`: `verified` / `unverified` / `mismatch` / `not-needed`.
- `Evidence Publication`: `local-only` / `published` / `blocked` / `not-configured` / `not-needed`.

## Web / Mobile Testing-Tool Gate

After modifying Web UI, routes, forms, login state, permissions, cross-page flows, API integration, release flows, Mobile App user journeys, Hybrid Apps, or critical user paths, you must proactively determine whether Chrome DevTools MCP, Playwright MCP, Playwright CLI, Maestro CLI, Maestro MCP, and `web-ui-autotest-generator` are applicable, according to the tool-responsibility boundaries in the global / project-level `AGENTS.md`.

This Skill is responsible only for the validation-stage gate:

- First select the smallest effective validation based on the scope of changes: project tests, browser diagnostics, Playwright Web regression, Maestro Mobile / Hybrid flows, or Web UI test-asset coverage assessment.
- For API / Web / Mobile / Hybrid flows, first determine `E2E Mode`: `full-stack` / `contract-backed` / `mock-backed` / `app-mocked` / `smoke-only` / `backend-only` / `blocked`. mock-backed, app-mocked, or contract-backed tests prove only that the corresponding contract / mock assumptions hold and must not be reported as passing full-stack validation.
- API / integration tests should inherit the project’s existing test framework and report configuration. If there is no project convention and a formal report is required for the current run, the default formal snapshot directory is `tests/api/reports/`. If the runner requires a temporary output directory that will be cleared or overwritten by the next run, use `tests/api/reports/.api-current/` by default, then copy / promote the output after the run to a report containing the current branch `branch_slug` and timestamp. If a custom API script only writes to the terminal, it counts only as a diagnostic; if it is part of formal validation for the current run, capture stdout, stderr, and the exit code as a raw report under `tests/api/reports/.api-current/`, then promote it to `tests/api/reports/` and generate a same-stem Chinese Markdown summary.
- Formal API / integration Markdown summaries must provide a URI coverage matrix: every coverage-scope description must map to a concrete `method + URI path`, and record the corresponding test script / case, expected status code or side effect, and associated `.feature` / contract / schema basis. When multiple endpoints support the same coverage scope, list each on a separate row; Base URL, environment name, and service name may be recorded separately, but script names, domain names, or high-level coverage summaries must not replace the URI path. Do not include real accounts, tokens, sensitive query/body data, or production data.
- Repeatable Web regression must prefer the project’s existing Playwright CLI command; Chrome DevTools MCP / Playwright MCP provide only diagnostics, exploration, or locator evidence. Playwright’s `--reporter=list` may only be used for diagnostics or targeted reruns; when Web E2E is within the formal validation scope, before finishing you must rerun the planned scope without overriding the project reporter, or mark the report status as `blocked`.
- Formal Web E2E HTML report snapshots go to `tests/e2e/reports/html/` by default, unless the project’s Playwright configuration has a stronger convention; the default `outputFolder` for the Playwright HTML reporter is the runner temporary directory `tests/e2e/reports/.playwright-html-current/`. That directory may be cleared by each Playwright run and may only serve as an intermediate artifact or source of tool-compatible artifacts; only the named HTML is the formal report.
- Maestro-related validation must first satisfy Java 17+ and Maestro CLI requirements; if MCP is unavailable but CLI is available, continue running existing `maestro test` flows and report MCP status separately.
- When Mobile / Hybrid Maestro flows must be generated or maintained from BDD scenarios, invoke `maestro-mobile-e2e` and confirm that committable flow assets are located under `maestro/flow/`.
- Formal Maestro reports must be written to `.maestro/reports/` at the project root; by default, generate only one native report format required by the project, named `maestro-report-{flow_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.xml` or `maestro-report-{flow_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.html`. `flow_name` is the Maestro flow filename stem, and smoke flows use `smoke`; generate HTML only when the project or user needs a human-readable report. Prefer having Maestro write directly to a file containing the branch name and timestamp; if a project wrapper command can only write to a directory that is rebuilt, use `.maestro/reports/.maestro-current/` as a temporary directory, then copy / promote the output to the formal report name. A stdout-only Maestro run may only be used for diagnostics or targeted reruns; when Mobile / Hybrid E2E is within the formal validation scope, before finishing you must use `--format` / `--output` or a project-equivalent reporter to generate a named report, or mark the report status as `blocked`.
- When Maestro execution on a physical iOS device encounters driver setup, port forwarding, view hierarchy, tap crash, or known-version issues, first have `maestro-mobile-e2e` lazily load the lesson by tag / keyword and apply the fix, then rerun the smallest failing flow.
- Invoke `web-ui-autotest-generator` only when Web UI regression must be persisted as in-repository test assets; when the environment, account, data preparation, cleanup strategy, or selectors are unstable, output only coverage gaps and blocking explanations.
- Before and after invoking `web-ui-autotest-generator`, you must follow this path contract to prevent its examples or script defaults from writing JSON to the project root:
  - `generate_manifest.py --root . --out tests/e2e/manifest/ui-test-manifest.json --pretty`
  - `audit_selectors.py --root . --out tests/e2e/manifest/ui-selector-audit.json --pretty`
  - `check_coverage.py --root . --manifest tests/e2e/manifest/ui-test-manifest.json --selector-audit tests/e2e/manifest/ui-selector-audit.json --tests-dir tests/e2e --out tests/e2e/manifest/ui-test-coverage.json --pretty`
  - `analyze_failures.py --report tests/e2e/reports/results.json --out tests/e2e/manifest/ui-test-repair-plan.json --pretty`
- After invoking `web-ui-autotest-generator`, verify that the committable JSON assets are actually located under `tests/e2e/manifest/`: `ui-test-manifest.json`, `ui-selector-audit.json`, and `ui-test-coverage.json`.
- If `ui-test-manifest.json`, `ui-selector-audit.json`, or `ui-test-coverage.json` exists in the project root, validation must not be marked complete; first move it to `tests/e2e/manifest/` and update references, or mark `Web UI test assets` as `blocked` and explain why.
- `ui-test-repair-plan.json` is a failure-analysis runtime artifact; if generated, the default path to check is `tests/e2e/manifest/ui-test-repair-plan.json`, and confirm that it will not be mistakenly committed as a long-lived test asset.
- If Playwright CLI, Java, Maestro CLI, MCP configuration, test accounts, authentication methods, test environments, devices, simulators, app binaries, appId / bundleId, or service URLs are unavailable, record `blocked` or `skipped`; do not claim that the corresponding validation passed.

In the final output, report the relevant tool statuses, executed commands, failure or blocking reasons, generated files, and remaining risks using the status enums defined by the global / project-level `AGENTS.md`.

## Test Reports and Rerun Closure

When API, Web E2E, Mobile E2E, Hybrid E2E, or pre-release smoke enters formal validation, follow the report and rerun rules below. Existing project CI / reporter configuration takes precedence; this template defines only default behavior and final report semantics.

Report rules:

- Debugging rounds may retain multiple named local test-report snapshots for later comparison of failures, fixes, and the final run; do not delete existing `playwright-report-*`, `maestro-report-*`, `api-report-*`, or `unit-report-*` snapshots from the same task. stdout-only, terminal-only, and diagnostic-only commands cannot satisfy the final report gate: Playwright `--reporter=list`, custom API scripts that only print terminal output, and Maestro runs without `--format` / `--output` or a project-equivalent reporter may only be recorded as diagnostics or targeted reruns. The final status is based only on the last planned-scope run recorded as `Final Full Rerun`.
- Reporting tests must first record the `rtk` decision: `skipped-for-report` means the native command was used directly to ensure the runner wrote report files; `fallback-native` means `rtk` output or cache behavior caused the report to be missing, stale, or unprovable, so the native command was used for revalidation. Do not declare that a report was generated or tests passed solely from `rtk` cache / replay output.
- Once a Playwright or Maestro run is executed and produces a runner-native report, regardless of whether the final full run passes, a named native report and same-stem Markdown summary must be generated in the formal report snapshot directory. The same rule applies to API / integration and unit tests if the current run generated native reports that must be retained as evidence. For Playwright, the “formal report snapshot directory” is `tests/e2e/reports/html/` by default, not the parent directory containing `results.json`, and not the temporary `outputFolder` of the Playwright HTML reporter. `Final Test Report: generated` only means the report file exists; whether the final result is fully green is recorded by `Final Full Rerun`.
- Default directories: API / integration formal snapshots use `tests/api/reports/`, and temporary API output uses `tests/api/reports/.api-current/`; temporary Playwright HTML reporter output uses `tests/e2e/reports/.playwright-html-current/`, and formal Playwright HTML report snapshots use `tests/e2e/reports/html/`; formal Maestro snapshots use `.maestro/reports/`, with temporary output using `.maestro/reports/.maestro-current/` when necessary; formal unit-test reports inherit project configuration by default, and when no convention exists but local evidence is required, use `tests/unit/reports/`, with temporary output using `tests/unit/reports/.unit-current/` when necessary.
- The branch name must be included in the formal API, Playwright, and Maestro report stem. First obtain the original branch name from the current git branch or an explicit project / CI branch ref; use `detached-{short_sha}` for detached HEAD; use `unknown-branch` outside a git environment. Use `branch_slug` when generating filenames: retain only letters, digits, `.`, `_`, and `-`, and replace `/`, spaces, and other special characters with `_`; record the original branch name and `branch_slug` in the Markdown summary.
- When a report serves as PR or knowledge-base evidence, also record the original source ref, full commit SHA, worktree state, evidence source, trigger, source revision, environment alignment, and publication status according to the validation evidence contract; do not use `branch_slug` as version identity.
- General overwrite-prevention rule: `coverage/`, `test-results/`, fixed `junit.xml`, runner `current` / `latest` directories, and the dot-prefixed temporary directories above are all considered runner-managed output. They may be cleared, overwritten, or rebuilt before the next run; when they must be retained, first copy / promote them to a formal snapshot directory with a timestamped stem before starting another command that rewrites the same runner output.
- Playwright naming: `playwright-report-{feature_file_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.html` + `playwright-report-{feature_file_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.md`. By default, `feature_file_name` is the associated BDD `.feature` filename without its extension; smoke tests always use `smoke`; when one run covers multiple `.feature` files, prefer an explicit suite name, otherwise use `multi-feature`. If it is not a smoke test and cannot be traced to a BDD `.feature`, do not invent a filename; first mark BDD traceability as `blocked`.
- Maestro naming: `maestro-report-{flow_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.xml` or `maestro-report-{flow_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.html`, and generate `maestro-report-{flow_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.md`. `flow_name` is the Maestro flow filename stem, smoke flows use `smoke`, and it must not be changed to `feature_file_name`; record the source `.feature` path and scenario name in the Markdown summary.
- When the Playwright default HTML reporter generates `index.html`, after every run that must be retained, copy it from `tests/e2e/reports/.playwright-html-current/` to the formal report name above; the named HTML is the formal report. Formal reports must not be stored in `.playwright-html-current/`, because the next Playwright run may clear that directory. The Markdown summary must have exactly the same stem as the named HTML; do not use the stem of `results.json`, `junit.xml`, `test-results/`, or the default `index.html` as the final Markdown filename. `results.md`, `result.md`, `junit.md`, and `index.md` do not satisfy `Run Summary MD: generated`. If Playwright has produced `results.json`, `junit.xml`, or an equivalent result but no `index.html`, rerun according to project configuration or enable the HTML reporter; do not substitute JSON / JUnit reports for the named HTML and same-stem `.md`. If the HTML reporter directory contains `data/`, traces, attachments, or other relative resources, copy the complete resource directory as well, or generate a complete snapshot directory with `playwright-report-{feature_file_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}/index.html` as its entry point and have the Markdown summary point to that entry point.
- API naming example: `api-report-{suite_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.xml` / `.json` / `.txt` + `api-report-{suite_name}-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}.md`; when there is no explicit suite, use the stem `api-report-{branch_slug}-{YYYY_mm_dd}-{HH_MM_SS}`. If an API / integration command has no native reporter but still serves as formal validation evidence for the current run, capture stdout, stderr, exit code, executed command, and timestamp as a `.txt` or `.json` raw report; do not merely paste terminal results into the final response.
- API Markdown summaries must include a “Coverage Scope -> API URI” mapping table. Recommended columns are: coverage scope, HTTP method, URI path, test script / case, expected status code, validated side effect or response field, and associated BDD / contract. When no route manifest exists, extract the information from test source code, OpenAPI / schema, client calls, or actual request logs; if the URI cannot be determined, mark that coverage item as `blocked` or `missing-uri`; do not present vague coverage descriptions as a complete report.
- Unit naming example: `unit-report-{suite_name}-{YYYY_mm_dd}-{HH_MM_SS}.xml` / `.json` / `.html` / `.lcov` + `unit-report-{suite_name}-{YYYY_mm_dd}-{HH_MM_SS}.md`. Unit tests are not required to generate formal reports on every run; however, once a project command or CI-compatible command has generated a report that must be retained for the current run, do not rely only on a fixed coverage or JUnit path that will be rewritten by the next run.
- If project configuration mandates multiple reporters, each retained run must generate only one set of named reports and one Markdown summary; the final conclusion is still determined by the last planned-scope run.
- If the final full run does not pass, still generate the named report and same-stem Markdown summary for that run, but do not claim “full pass” or “full-stack pass”; the final output must state the failure / blocking reasons, attempted commands, and remaining risks.
- If the CLI is not installed, environment prechecks block execution, or the runner crashes without producing any native report artifact, mark `Final Test Report` and `Run Summary MD` as `blocked` and explain the reason they are missing; once the runner has produced a native artifact, `Run Summary MD` must not be marked `not-needed`.

Failure handling and rerun order:

1. After the first failure, classify the root cause: product code, test code, BDD / specification, mock / contract drift, environment / account / data / device, flaky / timing, or an out-of-scope failure.
2. If it can be fixed within the current task scope, fix it and first rerun the failed case / failed spec / failed flow.
3. After the targeted rerun passes, run the affected subset, such as the same `.feature`, same API endpoint, same page flow, same test file, same Maestro flow, or same-platform smoke.
4. Finally, run the full validation within the planned scope; only if that run passes may you claim a final full pass, but whenever the runner produces a native report, a named report and Markdown summary must be generated regardless of pass or failure.
5. If the runner stops at the first failure because of fail-fast, after fixing it and passing the targeted rerun, continue running the remaining uncovered tests or directly rerun the full planned-scope validation.
6. Do not resume from the middle of a contaminated test environment by default; do so only when the project runner explicitly supports reliable resume.

The Markdown summary must record:

- The summary body must be written in Chinese; only status enum values, commands, file paths, case / spec / flow names, original error text, and technical identifiers may remain in English.
- Test scope, list of executed cases / specs / flows, `E2E Mode`, `Mock Strategy`, original branch name, `branch_slug`, `.feature` paths, and scenario names.
- When the report serves as PR or knowledge-base evidence, record `Evidence Source`, repository key, original source ref, full commit SHA, worktree state, `Source Revision`, trigger, `Environment Alignment`, `Evidence Publication`, and the evidence sidecar / envelope path.
- API / integration summaries must include a URI coverage matrix that maps each coverage scope to `method + URI path`, and identifies the corresponding test script / case and contract / schema / `.feature` basis.
- Final formal report paths, total number of execution rounds, and the command for each round.
- Failed cases / specs / flows for each round, failure-cause classification, corrective actions, and a summary of modified files.
- Results of targeted reruns, affected-subset reruns, and the final full rerun.
- Unexecuted items, reasons for skipping, remaining risks, and contract / mock / environment / account / device details.
- Do not include real accounts, secrets, PII, production data, full tokens, sensitive request headers, or production screenshots.

Additionally report in the final output:

- `Final Test Report`: `generated` / `blocked` / `not-supported` / `not-needed`.
- `Run Summary MD`: `generated` / `blocked` / `not-needed`.
- `Targeted Rerun`: `passed` / `failed` / `blocked` / `not-needed`.
- `Final Full Rerun`: `passed` / `failed` / `blocked` / `skipped-with-risk` / `not-needed`.
- `Evidence Source`: `developer-local` / `ci` / `knowledge-server` / `not-needed`.
- `Source Revision`: `exact` / `dirty` / `unknown` / `not-needed`.
- `Environment Alignment`: `verified` / `unverified` / `mismatch` / `not-needed`.
- `Evidence Publication`: `local-only` / `published` / `blocked` / `not-configured` / `not-needed`.

## General Language-Validation Rules

For every language, prefer commands defined by the project’s existing CI, README, Makefile, package scripts, Gradle / Maven wrapper, Xcode scheme, CMake preset, or deeper `AGENTS.md`. The commands below are only candidates when the project has no explicit convention.

During validation, also state:

- Whether code-style / lint / format checks were run.
- Whether unit tests were run.
- Whether integration / API / E2E is relevant to the current changes.
- Whether report paths were generated by project configuration; the template does not enforce a unified report directory for unit tests, but reports that will be cleared / overwritten by the runner must first be archived to a timestamped snapshot in the project-conventional directory or `tests/unit/reports/` before being referenced as evidence.
- Reasons for anything skipped or blocked.

## Node / JavaScript / TypeScript

Prefer the project package manager and CI scripts; do not switch package managers. Common commands:

Preferred for non-reporting commands such as lint / typecheck / build:

```bash
rtk npm run lint
rtk npm run typecheck
rtk npm run build
```

First apply the `rtk` and reporting-test Gate to test commands; when reports must be persisted, prefer:

```bash
npm run test
```

Fallback:

```bash
npm run lint
npm run typecheck
npm run build
```

Run typecheck when modifying:

- TypeScript types
- DTOs
- API return values
- Component props
- State structures
- Shared interfaces

If the project has no `typecheck` script, do not invent one; record it as undefined and run the type-checking or build command actually available in the project.

---

## Python

Preferred for non-reporting commands such as lint / format / typecheck:

```bash
rtk ruff check .
rtk ruff format .
rtk ty check .
```

First apply the `rtk` and reporting-test Gate to test commands; when reports must be persisted, prefer:

```bash
uv run pytest
```

Fallback:

```bash
uv run ruff check .
uv run ruff format .
uv run ty check .
```

Rules:

- After modifying Python code, run `ruff check`.
- When formatting is involved, run `ruff format`.
- When modifying types, function signatures, or return structures, run `ty check`.
- When modifying business logic, data processing, APIs, or fixing bugs, run `pytest`.
- Do not bypass `pyproject.toml`, `uv.lock`, `pytest.ini`, or `ruff.toml`.
- If the project uses `mypy`, `pyright`, `tox`, `nox`, `coverage`, or a test matrix defined by CI, prefer the project commands.

---

## Go

First apply the `rtk` and reporting-test Gate to test commands; when reports must be persisted, prefer:

```bash
go test ./...
```

Rules:

- When formatting changes are involved, run `gofmt`.
- When modifying concurrency, error handling, reflection, or format strings, run `go vet ./...`.
- Run `go mod tidy` only when dependencies change.
- Do not modify `go.mod` or `go.sum` without reason.
- If the project has a Makefile, CI matrix, race-test, coverage, or package-subset convention, prefer the project commands.

---

## Dart / Flutter

Prefer the project’s Flutter / Dart CI, Melos, Makefile, or package scripts.

Common candidates, where format / analyze may prefer `rtk`, and test must first apply the `rtk` and reporting-test Gate:

```bash
rtk dart format --set-exit-if-changed .
rtk dart analyze
dart test
```

Common candidates for Flutter projects:

```bash
rtk flutter analyze
flutter test
```

Rules:

- After modifying Dart code, run the project-conventional format / analyze commands.
- When modifying business logic, state management, data conversion, widget behavior, or fixing bugs, run unit tests / widget tests.
- Run Flutter integration tests, Maestro Mobile E2E, or platform builds only when changes affect the corresponding user journey, platform capability, or release risk.

---

## Java

Prefer the project wrapper and CI tasks; do not bypass Gradle / Maven configuration.

Common Gradle candidates, where test commands must first apply the `rtk` and reporting-test Gate and native commands are preferred when reports must be persisted:

```bash
./gradlew test
./gradlew check
```

Common Maven candidates:

```bash
mvn test
mvn verify
```

Rules:

- After modifying Java code, run the project-configured Checkstyle, Spotless, PMD, Error Prone, or equivalent lint / format gate.
- When modifying business logic, APIs, persistence, concurrency, or fixing bugs, run unit tests.
- When integrations, containers, databases, or external services are involved, run the integration-test profile according to project CI; if unavailable, state the blocking reason.

---

## Kotlin

Prefer the project’s Gradle wrapper, Android Gradle Plugin, Kotlin Multiplatform, or CI tasks.

Common candidates, where test commands must first apply the `rtk` and reporting-test Gate and native commands are preferred when reports must be persisted:

```bash
./gradlew test
./gradlew check
```

Common candidates for Android projects:

```bash
./gradlew testDebugUnitTest
```

Rules:

- After modifying Kotlin code, run the project-configured ktlint, detekt, Spotless, or equivalent lint / format gate.
- When modifying business logic, ViewModel, repository, domain layer, serialization, or fixing bugs, run unit tests.
- Run Android instrumentation tests, Compose UI tests, or Maestro Mobile E2E only when changes affect device behavior or user journeys.

---

## C++

Prefer the project’s CMake preset, Makefile, Bazel, Ninja, CTest, or CI commands; do not temporarily refactor the build system for validation.

Common candidates:

```bash
rtk cmake --build build
ctest --test-dir build --output-on-failure
```

Rules:

- After modifying C++ code, run the project-configured `clang-format`, `clang-tidy`, `cppcheck`, or equivalent static checks.
- When modifying core logic, memory ownership, concurrency, ABI/API, serialization, or fixing bugs, run unit tests.
- If the project has no configured build directory, create or select one according to the README / CI; if it cannot be determined, ask first or record the blocker, and do not arbitrarily generate long-lived build configuration.

---

## Swift

Prefer SwiftPM, Xcode scheme, xcodebuild, XcodeBuildMCP, or CI configuration.

Common SwiftPM candidates, where test commands must first apply the `rtk` and reporting-test Gate and native commands are preferred when reports must be persisted:

```bash
swift test
```

Common Xcode candidates:

```bash
xcodebuild test -scheme <scheme> -destination <destination>
```

Rules:

- After modifying Swift code, run the project-configured SwiftFormat, SwiftLint, `swift format`, or equivalent lint / format gate.
- When modifying business logic, models, services, view models, App Intents, serialization, or fixing bugs, run XCTest / Swift Testing unit tests.
- Run iOS UI tests, device tests, or Maestro Mobile E2E only when changes affect real-device behavior, permissions, camera, upload, deep links, system dialogs, or user journeys.
- If the Xcode scheme, destination, simulator, or signing is unclear, record the blocker; do not pretend tests were run.

---

## Objective-C

Prefer the Xcode workspace / project, scheme, xcodebuild, XcodeBuildMCP, or CI configuration.

Common candidates:

```bash
xcodebuild test -scheme <scheme> -destination <destination>
```

Rules:

- After modifying Objective-C / Objective-C++ code, run the project-configured clang-format, clang-tidy, OCLint, or equivalent lint / static-analysis gate.
- When modifying business logic, runtime, categories, delegates, bridge layers, memory management, C++ interop, or fixing bugs, run XCTest unit tests.
- When physical-device capabilities, system permissions, Hybrid bridges, or cross-page mobile flows are involved, run Xcode UI tests or Maestro Mobile E2E according to project conventions.
- If the workspace, scheme, destination, provisioning, or signing is unclear, record the blocker and state the required project facts.