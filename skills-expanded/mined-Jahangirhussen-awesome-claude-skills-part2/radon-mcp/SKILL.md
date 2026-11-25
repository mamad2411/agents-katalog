---
name: radon-mcp
description: "Best practices for using Radon IDE's MCP tools when developing, debugging, and inspecting React Native and Expo apps. Use when interacting with a running app through Radon IDE - viewing screenshots, reading logs, inspecting the component tree, debugging network requests, reloading the app, or querying React Native documentation and library info. Trigger on: 'debug React Native', 'fix UI', 'network issues', 'build issues', 'Radon IDE', 'view screenshot', 'app logs', 'component tree', 'network inspector', 'reload app', 'React Native docs', 'library description', 'emulator', 'development viewport', 'view_screenshot', 'view_application_logs', 'view_component_tree', 'reload_application', 'view_network_logs', 'view_network_request_details', 'query_documentation', 'get_library_description', and every request involving live app inspection, debugging or development in a Radon IDE session."
---

# Radon IDE MCP Tools

Best practices for Radon IDE's MCP tools for live React Native / Expo app inspection and debugging.

Read the relevant reference for the tool at hand. All references are in `references/`.

## References

| File                                         | When to read                                                                                       |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `references/view-application-logs.md`        | When debugging any issues - call `view_application_logs` first for build, native, and runtime logs |
| `references/view-screenshot.md`              | Inspecting the current visual state of the app, fixing visual bugs, making UI changes              |
| `references/view-component-tree.md`          | Understanding mounted component structure, resolving layout issues, finding context providers      |
| `references/view-network-logs.md`            | Inspecting network requests - paginated list of all HTTP traffic coming from and into the app      |
| `references/view-network-request-details.md` | Drilling into a specific network request's headers, body, and metadata                             |
| `references/reload-application.md`           | Reloading the app - choosing between JS reload, process restart, or full rebuild                   |
| `references/query-documentation.md`          | Looking up React Native / Expo API docs from a curated knowledge base                              |
| `references/get-library-description.md`      | Evaluating what an npm library does and whether it fits the task                                   |

## Purpose
Rules for using Radon IDE MCP tools to inspect and debug a running React Native/Expo app.

## When to use
A Radon IDE session is active and the task involves screenshots, logs, component tree, network requests, reloads or React Native docs.

## When NOT to use
- No Radon IDE session or the app is not React Native/Expo.
- Pure code edits that need no live app inspection.

## Inputs
A running app in Radon IDE; the symptom (UI bug, crash, network failure, build error).

## Core workflow
1. Call `view_application_logs` first for any problem (build, native, runtime).
2. Use `view_screenshot` to confirm the visible state.
3. Use `view_component_tree` for layout/props issues.
4. Use `view_network_logs` then `view_network_request_details` for API problems.
5. Apply the fix, `reload_application`, and re-check logs and screenshot.
6. Open the matching file in `references/` for tool-specific guidance.

## Edge cases and failure handling
- Logs empty -> reload and reproduce, then re-read.
- Screenshot does not match code -> app is stale; reload.
- Docs lookup needed -> `query_documentation` / `get_library_description`.

## Validation
- After the fix, logs show no new errors and the screenshot/network response matches expected behaviour.

## Output requirements
Findings (log line, request, component), the fix applied, and verification evidence.

## Example
```text
Blank screen -> logs show undefined prop -> component tree confirms -> fix -> reload -> screenshot shows content.
```

## Related skills
react-native-best-practices, react-native-expert, expo-horizon
