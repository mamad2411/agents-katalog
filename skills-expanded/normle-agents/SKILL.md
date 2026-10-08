# AGENTS.md

Repository-specific agent contract for Normle.

## Repository Rules

- Use English for branch names, code comments, documentation, and identifiers
  unless UI localization or legal content requires otherwise.
- Follow existing architecture and source style; keep changes small and
  repository-local.
- Markdown must follow
  <https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>.
- Swift code must comply with the repository SwiftLint configuration.

## Build and Test Entry Point

Agents MUST prefer XcodeBuildMCP for Apple build, test, run, Simulator,
runtime log, screenshot, and UI snapshot verification.

Before the first XcodeBuildMCP build, test, or run call in a session, run
XcodeBuildMCP `session_show_defaults`. If defaults do not point at this
repository, set them for the current session before continuing.

Treat library tests, surface builds, and runtime/UI evidence as separate
verification capabilities. Choose the smallest set that proves the current
change, and prefer stronger evidence when public APIs, wire contracts,
SwiftData schema, app lifecycle wiring, or visible UI behavior are affected.

- For shared-library logic, model, or test changes, use XcodeBuildMCP
  `test_sim` with the `NormleLibrary` scheme.
- For public `NormleLibrary` APIs, shared contracts, SwiftData schema, or
  adapter-facing contracts, also use XcodeBuildMCP `build_sim` with the
  `Normle` scheme.
- For app compile checks, use XcodeBuildMCP `build_sim` with the `Normle`
  scheme.
- For runtime or UI-sensitive changes, use XcodeBuildMCP `build_run_sim`,
  `launch_app_sim`, `snapshot_ui`, and `screenshot` as appropriate.

When Swift files are edited, agents should run:

```sh
bash ci_scripts/tasks/format_swift.sh
```

Use the retained aggregate shell gate when the task needs repository-state
artifacts or when MCP coverage is unavailable:

```sh
bash ci_scripts/tasks/verify_task_completion.sh
```

SwiftLint is resolved from the `SimplyDanny/SwiftLintPlugins` package declared
in `Normle.xcodeproj`, not from a separately installed `swiftlint` binary.

Compatibility scripts may write disposable data under `.build/ci/shared/` or
`.build/ci/runs/<RUN_ID>/`.

## Release UI Smoke Audit

Release UI smoke auditing is separate from the standard verification entrypoint.
Keep it non-destructive by default: do not erase simulator data, reset
containers, or add UI test targets solely for the audit unless explicitly
requested.
