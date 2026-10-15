---
name: intellij-platform-sdk
description: >
  IntelliJ Platform plugin development with the v2 SDK / IntelliJ Platform Gradle Plugin 2.x.
  Use this skill whenever the user mentions IntelliJ plugins, plugin.xml, AnAction, PSI,
  inspections, intentions, code completion, custom language support, tool windows, settings,
  notifications, indexing, VFS, dumb mode, plugin verifier, Marketplace publishing, or target IDEs
  like IntelliJ IDEA, WebStorm, PyCharm, GoLand, Android Studio, Rider, or CLion.
  Also trigger for: Gradle IntelliJ Plugin, runIde, buildPlugin, extension point, EP registration,
  light service, @Service, persistent state, PersistentStateComponent, plugin descriptor,
  WriteCommandAction, run configuration, file type, syntax highlighter, ParserDefinition,
  CompletionContributor, LocalInspectionTool, ToolWindowFactory, DialogWrapper, Kotlin UI DSL,
  dynamic plugins, coroutine scope in plugins, ActionUpdateThread, or any build.gradle.kts
  referencing org.jetbrains.intellij.platform.
---

# IntelliJ Platform SDK Skill

Use this skill for **IntelliJ Platform plugin development** based on the modern **v2 SDK**.

This skill is intentionally split into focused references so the main file stays small and the model can load only the material relevant to the task.

## What this skill helps with

- creating or updating IntelliJ Platform plugins
- configuring `build.gradle.kts`, `settings.gradle.kts`, and `plugin.xml`
- implementing actions, services, tool windows, settings, and notifications
- working with PSI, references, indexing, VFS, and dumb mode
- building custom language support
- implementing inspections, intentions, quick fixes, completion, formatting, and documentation
- testing plugins and preparing Marketplace publication
- handling version compatibility and Gradle plugin migration

## How to use this skill

First, identify the user’s real task. Then read only the relevant reference files.

### Read `references/getting-started.md` when the task is about

- creating a new plugin
- setting up v2 SDK / Gradle Plugin 2.x
- choosing target IDEs
- adding bundled plugins or optional dependencies
- writing or fixing `plugin.xml`

### Read `references/platform-basics.md` when the task is about

- `AnAction`, action groups, menus, toolbars
- services (`@Service`, project/application/module services)
- Virtual File System (`VirtualFile`, VFS listeners)
- threading, read/write actions, dumb mode
- Kotlin coroutine patterns in plugins (`readAction`, `writeAction`, `CoroutineScope`)
- dynamic plugin loading/unloading
- general plugin architecture decisions

### Read `references/psi-and-indexing.md` when the task is about

- PSI traversal or modification
- references, resolve, rename, find usages
- code generation using PSI factories
- file-based indexes, stub indexes, gists
- `IndexNotReadyException`, dumb mode, PSI performance

### Read `references/language-support-and-analysis.md` when the task is about

- custom language plugins
- lexer, parser, `ParserDefinition`
- syntax highlighting, annotators, completion
- inspections, intentions, quick fixes
- formatter, folding, structure view, documentation provider

### Read `references/ui-settings-and-toolwindows.md` when the task is about

- Kotlin UI DSL v2 (`panel { row { } }`, `BoundConfigurable`)
- dialogs and IntelliJ UI components
- tool windows
- settings/configurables
- persistent state
- notifications
- popups (`JBPopup`, `ListPopup`, chooser popups)
- project wizard, module type, project view integration

### Read `references/testing-and-publishing.md` when the task is about

- test fixtures and plugin tests
- parser/completion/inspection tests
- plugin verifier
- signing and publishing to Marketplace

### Read `references/compatibility.md` when the task is about

- build compatibility
- `sinceBuild` / `untilBuild`
- migrating from legacy Gradle plugin 1.x to 2.x
- API changes across platform versions
- Java/Kotlin version expectations

### Read `references/extension_points.md` when the task is about

- exact `plugin.xml` registration syntax
- locating the right extension point
- action group IDs and XML patterns

### Read `references/code_samples.md` when the task is about

- finding the closest official SDK sample
- copying an official implementation pattern
- understanding what each JetBrains sample demonstrates

### Read `references/patterns.md` when the task is about

- reusable implementation patterns
- editor/document helpers
- progress handling
- dialog/tool-window patterns
- PSI/editor/VFS utilities

### Read `references/troubleshooting.md` when the task is about

- you are not yet sure which troubleshooting bucket the issue belongs to
- actions not appearing
- threading assertions
- service initialization failures
- PSI write-action errors
- verifier warnings
- test setup failures

### Read `references/troubleshooting-build-runtime.md` when the task is about

- Gradle or repository resolution failures
- `plugin.xml` wiring or class loading issues
- action registration/runtime visibility issues
- verifier/signing/release failures

### Read `references/troubleshooting-psi-ui-testing.md` when the task is about

- PSI validity or write-action assertions
- `IndexNotReadyException`
- editor/document synchronization
- UI refresh or EDT access errors
- fixture/test-data/debugging problems

## Working principles

When solving IntelliJ Platform tasks:

1. Prefer **official platform concepts** over ad-hoc hacks.
2. Put reusable logic in **services**, not in actions.
3. Keep `AnAction.update()` **extremely fast**.
4. Respect **threading and dumb mode** before optimizing behavior.
5. Use **PSI-aware** approaches for structural code tasks.
6. Use **platform UI components** and conventions for user-facing surfaces.
7. Keep plugin dependencies and target IDE scope as small as practical.

## High-value reminders

- `AnAction` implementations should not store request-specific state in fields.
- Actions must implement `getActionUpdateThread()` (required since 2022.3).
- PSI/document changes must happen inside write commands.
- Not every feature is safe in dumb mode; do not mark things `DumbAware` casually.
- For Kotlin plugins on 2024.1+, prefer coroutine-based read/write APIs when appropriate.
- Light services must be `final` and must not inject dependency services via constructors.
- Avoid internal APIs unless there is no viable public alternative and the tradeoff is explicit.

## Typical response strategy

When a user asks for implementation help:

1. Determine the feature surface: action, service, PSI, UI, language support, test, or publishing.
2. Read the matching reference files.
3. Follow the closest official sample or extension-point pattern.
4. Implement the smallest correct solution that matches IntelliJ Platform rules.
5. If publishing or compatibility matters, also review verifier/signing/build-range concerns.

## Reference map

- `references/getting-started.md`
- `references/platform-basics.md`
- `references/psi-and-indexing.md`
- `references/language-support-and-analysis.md`
- `references/ui-settings-and-toolwindows.md`
- `references/testing-and-publishing.md`
- `references/compatibility.md`
- `references/extension_points.md`
- `references/code_samples.md`
- `references/patterns.md`
- `references/troubleshooting.md`
- `references/troubleshooting-build-runtime.md`
- `references/troubleshooting-psi-ui-testing.md`
