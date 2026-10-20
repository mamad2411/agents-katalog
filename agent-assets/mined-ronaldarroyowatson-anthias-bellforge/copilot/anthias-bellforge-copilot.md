# Copilot Instructions - Bellforge Project

**Project**: Bellforge (derivative of Anthias by Screenly, Inc.)
**Maintainer**: Ronald Arroyo-Watson
**License**: GPLv2 (consistent with upstream Anthias)
**Purpose**: Custom distribution with enhancements while maintaining upstream compatibility

## Bellforge-Specific Guidelines

1. **Public Branding** - Update splash screen, web UI, and documentation with "Bellforge" branding
2. **Internal Compatibility** - Keep `anthias_*` naming in code, Docker services, file paths, and databases
3. **Attribution** - Always credit Screenly, Inc. and the Anthias project as the upstream source
4. **Differentiation** - Clearly mark Bellforge-specific features and modifications
5. **Upstream Synchronization** - When merging upstream Anthias changes, preserve both Bellforge branding and Anthias compatibility

## Ronald Style Conventions

1. Naming and clarity
- Use explicit, descriptive names for variables, functions, classes, and files.
- Prefer unambiguous names over abbreviated names.
- Do not use metaphors when a concrete name is possible.

2. Function and file structure
- Keep functions small, single-purpose, and deterministic.
- Keep each file focused on one responsibility.
- Do not create utility dumping grounds.

3. Code style and readability
- Keep control flow linear and obvious.
- Prefer simple formulas and straightforward branching.
- Avoid deep nesting; extract helper functions.

4. Comments and docs
- Add short comments that explain why, not what.
- Document assumptions and edge cases near related logic.
- Begin new files with a one-line purpose statement.

5. Error handling
- Handle exceptions explicitly.
- Never swallow exceptions silently.
- Emit actionable error messages.

6. Data and state
- Prefer minimal, explicit state.
- Avoid hidden side effects.
- Use immutable patterns where practical.

7. Architecture discipline
- Keep strict boundaries between UI, logic, data, and service layers.
- Avoid cross-layer leakage and implicit coupling.

8. Testing expectations
- Add deterministic and isolated tests.
- Use fail-first tests when fixing regressions.
- Prefer explicit test setup over excessive mocking.

9. Copilot generation behavior
- Do not invent APIs.
- Follow existing repository patterns unless explicitly changing architecture.
- Avoid broad rewrites when a scoped patch solves the issue.

## Display Pipeline Workflow

When working on display startup or splash behavior:

1. Add fail-first tests before runtime changes.
2. Add debug instrumentation that exposes branch decisions and failure paths.
3. Implement minimal scoped fix.
4. Re-run targeted tests and then broader affected tests.
5. Log each discovered issue in docs/display-pipeline-fix-log.md with:
- symptom
- impact
- evidence
- files changed
- status
6. Emit structured startup timeline markers (phase + elapsed time) for startup-path changes.
7. Ensure Linux execution coverage for display tests via bin/run_display_pipeline_tests.sh and CI workflow step.
8. Maintain machine-readable render telemetry (last command/result + short history) so display intent can be inspected remotely.

## Append-Only Documentation Rule

For architecture, codex, and fix-log documentation, use append-only updates where practical:
- add new dated entries
- do not delete historical findings
- mark superseded entries with a status update instead of removal

## Bugfix Workflow Contract

When the user requests to initiate the bugfix workflow, execute this full sequence unless explicitly scoped down:

1. Run full automated tests:
- frontend tests
- backend/unit tests
- integration tests
- Linux display pipeline tests

2. Run smoke tests and live Pi verification:
- verify service/container health
- verify `/`, `/settings`, `/system-info`, and `/splash-page` endpoints return HTTP 200
- verify render telemetry indicates successful display command/result state

3. Run installer/uninstaller/repair simulation on Pi:
- execute full update/upgrade path
- execute backup + restore validation
- simulate corruption (for example DB/data corruption), then verify repair/restore path recovers runtime

4. Validate user-visible runtime behavior:
- verify display path is working after restart/reboot checks
- verify settings page sections/elements are present, visible, and scrollable

5. Release and synchronization steps:
- bump BellForge bugfix version only (X.Y.Z, increment Z)
- update version metadata needed for reboot/update detection
- update related docs/handoff/fix-log entries
- commit and push all relevant bugfix changes to remote

6. Report completion with evidence:
- include pass/fail status per phase
- include blockers and residual risks if any phase cannot pass in current environment
