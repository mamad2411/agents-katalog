---
name: xcode
description: "Interact with Xcode via Apple's MCP bridge for building, testing, previewing, and debugging Apple platform projects. Use this skill whenever the user is working on Swift or SwiftUI code, building iOS/macOS/watchOS/tvOS/visionOS apps, wants to run or fix builds, run tests, render SwiftUI previews, search Apple documentation or WWDC transcripts, check Xcode diagnostics, or do any development that involves an Xcode project (.xcodeproj, .xcworkspace, or Package.swift). Also use when the user mentions Xcode by name, asks about build errors or warnings, wants to evaluate Swift snippets, or is iterating on UI with SwiftUI previews. Trigger even if the user doesn't explicitly mention Xcode — if they're working on Apple platform code and could benefit from Xcode integration, this skill applies."
---

# Xcode MCP Integration

You have access to Xcode through the `xcode` MCP server (`xcrun mcpbridge`). This gives you 24 tools that let you build projects, run tests, render SwiftUI previews, search Apple documentation, and more — all through Xcode's own engine.

## Prerequisites

Xcode must be running with a project open. The MCP bridge connects to the active Xcode instance — there's no headless mode. If tools return errors about connection or missing windows, ask the user to confirm Xcode is open with their project loaded, and that MCP is enabled (Settings > Intelligence > Model Context Protocol > Xcode Tools).

## The tabIdentifier: Your Session Key

Almost every Xcode MCP tool requires a `tabIdentifier` — a string that identifies which Xcode window/tab to operate on. You get it by calling `XcodeListWindows` first.

**Always start by calling `mcp__xcode__XcodeListWindows`** at the beginning of any Xcode workflow. Cache the `tabIdentifier` and reuse it for all subsequent calls in the session. The only exception is `DocumentationSearch`, which doesn't need one.

If a tool call fails with a tabIdentifier error, call `XcodeListWindows` again — the identifier may have changed if the user switched projects or tabs.

## Tool Reference

### Discovery
- **`XcodeListWindows`** — Returns open windows with `tabIdentifier` values. Call this first.

### File Operations
Use these when you need Xcode-aware file operations (e.g., so Xcode tracks changes for diagnostics and builds). For simple reads of files outside the project, Claude's native `Read` tool is fine.

- **`XcodeRead`** — Read file contents
- **`XcodeWrite`** — Write entire file contents
- **`XcodeUpdate`** — String-replacement edits (like Claude's `Edit` tool, but Xcode-aware)
- **`XcodeLS`** — List directory contents
- **`XcodeGlob`** — Glob pattern file search
- **`XcodeGrep`** — Regex search with context lines and output modes
- **`XcodeMakeDir`** — Create directories
- **`XcodeRM`** — Remove files
- **`XcodeMV`** — Move/rename files

### Build & Test
- **`BuildProject`** — Trigger an incremental build (typically very fast, ~1s for incremental)
- **`GetBuildLog`** — Retrieve build logs; filter by severity to focus on errors or warnings
- **`RunAllTests`** — Run the full test suite
- **`RunSomeTests`** — Run specific tests by target and test identifier
- **`GetTestList`** — List all available test targets and test identifiers

### Diagnostics
- **`XcodeListNavigatorIssues`** — List all current issues (errors, warnings) from the Issue Navigator
- **`XcodeRefreshCodeIssuesInFile`** — Force Xcode to re-check a specific file for issues

### Execution & Preview
- **`ExecuteSnippet`** — Run Swift code in a REPL-like environment with access to the project's module context. Useful for testing expressions, checking API behavior, or prototyping logic.
- **`RenderPreview`** — Render a SwiftUI preview as an image. Returns the rendered preview so you can see what the UI looks like.

### Documentation
- **`DocumentationSearch`** — Semantic search across Apple's developer documentation and WWDC session transcripts. Powered by on-device ML embeddings, so results are high quality. This is the only tool that does NOT require a `tabIdentifier`. Use it to look up APIs, find usage examples, or understand frameworks.

## Core Workflow: Build-Fix Loop

The most common pattern when developing Apple platform code:

1. **Get your session key**: Call `XcodeListWindows` → save the `tabIdentifier`
2. **Edit code**: Use `XcodeUpdate` for targeted changes or `XcodeWrite` for new files
3. **Build**: Call `BuildProject` to compile
4. **Check results**: If the build fails, call `GetBuildLog` filtered to errors. Read the diagnostics.
5. **Fix and repeat**: Edit the problematic code, build again. Keep looping until clean.
6. **Run tests**: Once building, run `RunAllTests` or `RunSomeTests` to verify behavior
7. **Preview UI**: For SwiftUI work, call `RenderPreview` to see the visual output

This loop is fast — incremental builds are typically under a second, so you can iterate quickly.

## When to Use Xcode Tools vs Claude's Native Tools

| Task | Use Xcode MCP | Use Claude Native |
|------|--------------|-------------------|
| Edit Swift files in the project | `XcodeUpdate` (Xcode tracks the change) | `Edit` works too, but Xcode won't see changes until it re-indexes |
| Read a config file | Either works | `Read` is simpler |
| Build the project | `BuildProject` | N/A |
| Search for an API | `DocumentationSearch` | Web search |
| Find files by pattern | `XcodeGlob` | `Glob` |
| Run tests | `RunAllTests` / `RunSomeTests` | `Bash` with `xcodebuild test` (slower, less integrated) |

The general rule: use Xcode MCP tools when you want Xcode to be aware of the change (for builds, diagnostics, previews) or when you need Xcode-specific capabilities (documentation search, SwiftUI preview rendering, build system). Use Claude's native tools for quick reads or edits where Xcode awareness isn't important.

## Tips

- **Use absolute paths** — the MCP bridge runs in a sandboxed environment and doesn't inherit your shell's working directory.
- **Check diagnostics after edits** — call `XcodeRefreshCodeIssuesInFile` after editing to get real-time feedback before building.
- **Documentation search is free** — `DocumentationSearch` doesn't need a tabIdentifier and is great for quickly looking up API signatures, parameter types, or framework capabilities. Use it liberally when you're unsure about an API.
- **Test selectively** — use `GetTestList` to find test identifiers, then `RunSomeTests` to run only relevant tests instead of the full suite.
- **Preview SwiftUI iteratively** — after editing a SwiftUI view, call `RenderPreview` to see the result visually. This is much faster than building and running on a simulator.

## Limitations

- **No simulator control** — you can build and test, but can't launch or interact with the iOS Simulator.
- **No debugging** — no breakpoints, stepping, or LLDB integration.
- **No UI automation** — can't tap buttons or navigate app screens.
- **Single connection** — only one client can connect to the MCP bridge at a time.
- **Requires running Xcode** — no headless or CI usage.
