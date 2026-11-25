---
name: browser-testing
description: Automated browser testing and debugging using Browser DevTools MCP. Use when testing web pages, debugging frontend issues, verifying UI behavior, or automating browser interactions.
---

# Browser Testing Skill

Automated browser testing and debugging skill using Browser DevTools MCP.

**Page structure:** To understand what is on a page, use **ARIA snapshot first** (`a11y_take-aria-snapshot` or `a11y_take-ax-tree-snapshot`), not screenshot. Use **screenshot** only when you need to verify how something looks visually (e.g. design check, visual bug).

## When to Use

This skill activates when:
- User asks to test a web page or application
- User wants to debug frontend issues
- User needs to verify UI behavior
- User asks about page performance or accessibility
- User wants to automate browser interactions

## Capabilities

### Ref-Based Workflow (Recommended)
1. **ARIA snapshot first** (`a11y_take-aria-snapshot`) — Returns refs (e1, e2, …) and a refs map. Options: `interactiveOnly`, `cursorInteractive` (for div/span buttons), `selector` (scope).
2. **Use refs in interactions** — Click, fill, hover, etc. accept CSS selector **or ref** (e.g. `e1`, `@e1`). Refs valid until next snapshot or navigation.
3. **Annotated screenshot** — `content_take-screenshot` with `annotate: true` overlays labels [1],[2],… mapping to e1,e2,…

### Navigation & Interaction
- Navigate to URLs (`navigation_go-to`) — **returns ARIA snapshot and refs by default**; use response refs for interactions without calling `a11y_take-aria-snapshot` again
- Same for `navigation_go-back-or-forward` and `navigation_reload` (includeSnapshot: true)
- Click, fill, hover — **selector or ref** (e.g. `e1`, `#submit`)
- Press keys (`interaction_press-key`), scroll (`interaction_scroll`), drag (`interaction_drag`)

### Content Capture
- Screenshots (`content_take-screenshot`) — optional `annotate`, `annotateContent`, `cursorInteractive`
- HTML/text content, PDF

### Debugging & Observability
- Get console messages (`o11y_get-console-messages`)
- Monitor HTTP requests (`o11y_get-http-requests`)
- Get Web Vitals (`o11y_get-web-vitals`)
- OpenTelemetry tracing (`o11y_get-trace-id`, `o11y_set-trace-id`)

### Accessibility
- ARIA snapshot (`a11y_take-aria-snapshot`) — returns refs; options: `interactiveOnly`, `cursorInteractive`, `selector`
- AX tree (`a11y_take-ax-tree-snapshot`) — bounding box, occlusion, styles

### Mocking & Stubbing
- Intercept HTTP requests (`stub_intercept-http-request`)
- Mock HTTP responses (`stub_mock-http-response`)
- List stubs (`stub_list`)
- Clear stubs (`stub_clear`)

### React DevTools
- Get React component for element (`react_get-component-for-element`)
- Get element for React component (`react_get-element-for-component`)

### Code Execution
- **Run JavaScript in browser:** use **execute** with `page.evaluate()` (e.g. `return await page.evaluate(() => document.title)`). See [commands/browser/execute.md](../../commands/browser/execute.md) for `callTool` and `page`.
- Run JavaScript in server VM: use **execute** (no `page`; use built-ins and `callTool`). On Node platform, **execute** runs in the session VM (callTool only).

### Batch Execution (advanced)
- **`execute`** — Run custom JavaScript that can call multiple tools in one request via `await callTool(name, input, returnOutput?)`. Use to batch click/fill/select/navigation and reduce round-trips. Code runs in async IIFE (no wrapper); browser platform exposes `page` (Playwright). Prefer when you have a fixed sequence of steps; use individual tools when you need to inspect results between steps. **Also supported**: browser-devtools-mcp CLI subcommand `run execute`, and daemon HTTP API (POST `/call` with `toolName: "execute"`).

## Best Practices

1. **ARIA snapshot first** — Do not use screenshot to understand page structure. After navigation, use the refs returned by go-to/go-back-or-forward/reload; otherwise call `a11y_take-aria-snapshot`, then use refs (e1, e2) in interactions or take annotated screenshots.
2. **Wait for network idle** after navigation before interacting
3. **Use refs for interactions** — Refs from ARIA snapshot are stable; prefer refs over CSS selectors when available
4. **Annotated screenshots** — Use `annotate: true` when you need visual labels that match refs for vision-driven actions
5. **Re-snapshot after navigation** — Refs are invalid after navigation or major DOM changes
