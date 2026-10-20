---
name: intellij-plugin-dev
description: >-
  Senior-level guidance for developing IntelliJ Platform plugins in Kotlin (extension
  points, plugin.xml, services, listeners, actions, tool windows, custom languages /
  file types, Grammar-Kit lexer/parser/PSI, LSP4IJ, threading model, Gradle IntelliJ
  Platform plugin) AND for inspecting a live IDE via the IDE Introspector MCP tools
  (arch.*, ui.*, psi.*, code.*, services.*, events.*, editor.*, screenshot.*, exec.*)
  surfaced through the JetBrains "idea" MCP server. Use when writing, reviewing, or
  debugging IntelliJ/JetBrains plugin code; registering extension points; deciding
  between application/project/module services or light @Service; wiring listeners or
  message-bus topics; building actions, tool windows, annotators, references, or
  completion; defining a custom language with Grammar-Kit; configuring the Gradle build;
  or asking "how is X done in IntelliJ", "what extension point / service / listener
  exists", or "inspect the running IDE".
metadata:
  author: xepozz
  version: "1.0"
  category: ide-plugin-development
  sources:
    - https://plugins.jetbrains.com/docs/intellij/ (IntelliJ Platform SDK, llms.txt)
    - https://github.com/j-plugins/ide-introspector-plugin (IDE Introspector manual)
---

# IntelliJ Platform Plugin Development

Senior guidance for building IntelliJ Platform (IntelliJ IDEA / PhpStorm / etc.) plugins
in **Kotlin** on **IntelliJ Platform 2025.1+** with the **Gradle IntelliJ Platform plugin (2.x)**,
plus how to introspect a running IDE with the **IDE Introspector** MCP tools.

Two reference files hold the detail — read the relevant one before non-trivial work:

- **[references/PLUGIN-DEVELOPMENT.md](references/PLUGIN-DEVELOPMENT.md)** — extension points,
  `plugin.xml`, services, listeners/message bus, actions, threading & coroutines, PSI,
  custom languages & Grammar-Kit, LSP4IJ, Gradle build, testing, common pitfalls.
- **[references/IDE-INTROSPECTOR.md](references/IDE-INTROSPECTOR.md)** — the 37 IDE Introspector
  MCP tools (by group), how they surface through the `idea` MCP server, and task→tool recipes.

## When to verify against the running IDE vs. the docs

- **Architecture questions** ("does an extension point for X exist?", "who implements Y?",
  "what services does plugin Z register?") → prefer the **IDE Introspector `arch.*` / `services.*` /
  `events.*` tools**: they read the *actual running IDE*, so they reflect installed plugins,
  versions, and dev builds — more accurate than docs or memory.
- **Conceptual / how-to questions** ("how do I declare a light service?", "what's the threading
  rule for PSI writes?") → use `references/PLUGIN-DEVELOPMENT.md` and, when in doubt about
  current API, the IntelliJ Platform SDK docs (`https://plugins.jetbrains.com/docs/intellij/`).
- **Resolving a concrete class** ("what does `ProjectFileIndex` expose?", "show me the source")
  → IDE Introspector **`code.*` / `psi.*`** tools against the live project.

## Core rules (do these by default)

1. **Register, don't hardcode.** Behavior is contributed through **extension points** declared in
   `src/main/resources/META-INF/plugin.xml`. Reach for an existing EP before inventing a mechanism.
2. **Prefer light services.** Use `@Service` (`@Service(Service.Level.PROJECT)` for project scope)
   with `project.service<T>()` / `service<T>()` over `<applicationService>`/`<projectService>` XML
   unless you need an interface/impl split or test override. Never `new` a service.
3. **Respect the threading model.** Reads of PSI/VFS/indexes need a **read action**; writes to
   the document/PSI need a **write action on EDT** (`WriteCommandAction`). Don't block the EDT;
   move slow work to a background coroutine/dispatcher and bounce back with `withContext` /
   `invokeLater`. Mark long-running UI as `DumbAware` only when it truly tolerates dumb mode.
4. **One class per file; `Wippy`-style prefix** for plugin-owned types (match the host project's
   convention). `val` over `var`, expression bodies, scope functions, deliberate null-safety.
5. **Don't edit generated code.** Grammar-Kit output under `src/main/gen/` is built from
   `src/main/grammars/*.flex` / `*.bnf`. Change the grammar and regenerate
   (`generateLexer` / `generateParser`), never the generated Java.
6. **Scope activation.** Gate language/LSP/inspection features to relevant projects (e.g. via a
   `DocumentMatcher` or project detector) instead of activating globally.
7. **User-facing text via resource bundles** (`MyBundle` / `messages/*.properties`) and the
   platform `Logger` (`com.intellij.openapi.diagnostic.Logger`) — never `println` or hardcoded strings.

## Quick decision: which service level / mechanism?

| Need | Use |
|------|-----|
| Stateless helper, app-wide | application-level `@Service` |
| Per-project state/cache | `@Service(Service.Level.PROJECT)` |
| Persist state across restarts | service implementing `PersistentStateComponent<T>` |
| React to platform events declaratively | `<applicationListeners>` / `<projectListeners>` + a `Topic` |
| Run once on project open | `ProjectActivity` (suspend) registered at `postStartupActivity` |
| Add a menu/toolbar command | `AnAction` registered under `<actions>` |
| Background-safe symbol resolution | wrap in `ReadAction` / coroutine read action; check `DumbService` |

## Workflow for a typical task

1. **Clarify the extension surface.** Identify the EP(s) involved. If unsure they exist or what
   plugs into them, query the live IDE: `arch.list_extension_points nameContains="…"`,
   `arch.find_extenders_of target="…"` (see IDE-INTROSPECTOR reference).
2. **Read the relevant reference** section before writing code.
3. **Implement** following the core rules. Keep registration in `plugin.xml` next to the code it wires.
4. **Verify in a sandbox** with `./gradlew runIde`, then introspect: `ui.get_tree`,
   `arch.get_plugin_details pluginId="<your id>"`, or `exec.execute_kotlin_in_ide` for one-off checks.
5. **Test** with the IntelliJ Platform test framework (`BasePlatformTestCase` / fixtures under `testData/`).

## IDE Introspector at a glance

The IDE Introspector is an **IntelliJ plugin** (not an npx server). Its 37 tools register via the
`com.intellij.mcpServer.mcpToolset` extension point and become visible to MCP clients **through the
bundled JetBrains MCP Server** — i.e. the **`idea` MCP server** in this session. To use them:
ensure the IDE Introspector plugin is installed and enabled and the JetBrains MCP Server plugin is on.
Tool names appear as `arch__list_plugins`, `ui__get_tree`, etc. Full catalog and recipes:
**[references/IDE-INTROSPECTOR.md](references/IDE-INTROSPECTOR.md)**.

`exec.execute_kotlin_in_ide` is the escape hatch (off by default, per-call confirmation, 10 s cap):
prefer a pre-built tool when one fits — it is ~100× faster than spinning up the Kotlin compiler.
