---
name: chrome-webmcp
description: Reference for WebMCP, Chrome's proposed web standard (document.modelContext) that lets a web page register structured tools an AI agent can call directly, instead of the agent guessing at buttons and fields via simulated clicks. Use whenever the user wants to make a website "agent-friendly", expose actions (checkout, search, form submission, filters) to AI browser agents, is building or debugging a WebMCP tool with the Imperative API (document.modelContext.registerTool) or the Declarative API (toolname/tooldescription HTML attributes on a form element), or wants to write evals for whether an agent calls their tools correctly. Trigger on mentions of WebMCP, document.modelContext, agent actuation, "agent-friendly forms", or making a site usable by browser AI agents. Do NOT use for Model Context Protocol (MCP) servers running outside the browser (stdio/HTTP tool servers for Claude/other LLM clients) — WebMCP is the in-page, JS/HTML version for browser agents acting on a live webpage.
---

# WebMCP

WebMCP is a proposed web standard (currently behind an origin trial / the `chrome://flags/#enable-webmcp-testing` flag) that lets a web page declare tools — named, schema'd actions like `checkout` or `filter_results` — that an AI browser agent can call directly, instead of trying to infer intent by simulating clicks and keystrokes on human-facing UI ("actuation"). Reach for this skill any time the task is "make my page's actions legible to an agent," not "build a general MCP server."

**Why this matters over plain actuation:** an agent guessing at buttons is slow, brittle, and easy to misinterpret across a multi-step flow (a complex checkout, a multi-passenger trip booking). Declaring a tool with a name, description, and JSON Schema removes the guesswork — the page tells the agent exactly what's possible and what inputs are expected, and the tool executes visibly on the page so the user can see and trust what happened. WebMCP tools always run with a browsing context open — there's no headless/background calling.

Two ways to define tools; pick based on how the page already works:

- **Imperative API** (`document.modelContext`) — plain JavaScript, for anything: form input, navigation, state management, arbitrary functions. Full detail in `references/imperative-api.md`.
- **Declarative API** (`toolname`/`tooldescription` HTML attributes) — turns an existing `<form>` into a tool with zero JS, by annotating the form and its fields. Full detail in `references/declarative-api.md`.

Both produce the same underlying shape: a name, a description, and a JSON Schema for inputs, discoverable by any WebMCP-aware agent. Read the relevant reference file before writing tool code — the two APIs have different registration mechanics (`registerTool()` vs. HTML attributes) and different event models (`toolchange` vs. `toolactivated`/`toolcancel`).

## Good candidates for a WebMCP tool

- **Structured form submission**: map a conversational request cleanly onto form fields the agent might otherwise fill in incorrectly (e.g. distinguishing "full name" vs. separate first/last name fields).
- **Human-first UI an agent can't parse well**: a complex date/time picker widget — wrap it as a `date_pick` tool instead of hoping the agent can operate the widget via clicks.
- **Buried but useful actions**: a `run_diagnostics` tool on a settings page that's otherwise behind several menu clicks.
- **Sensitive actions**: anything like a purchase should still route through a real user-facing confirmation step — WebMCP doesn't remove the need for that, it just gets the agent to the right point faster.

## Origin trial and local dev setup

Production use requires the [WebMCP origin trial](https://developer.chrome.com/origintrials/#/register_trial/4163014905550602241) (from Chrome 149) — register per Chrome's standard [origin trial process](https://developer.chrome.com/docs/web-platform/origin-trials).

For local development, no token needed:
1. Go to `chrome://flags/#enable-webmcp-testing`.
2. Set to **Enabled**.
3. Relaunch Chrome.

To manually exercise tools during development without a full agent loop, install the **Model Context Tool Inspector** Chrome extension — it shows registered tools on a page, lets you call them manually, validates your JSON Schema against what the browser actually parses, and lets you chat with an agent (backed by `gemini-3-flash-preview`, separate from Gemini in Chrome) to see whether natural-language prompts correctly trigger your tools.

## Security and permissions

Two gates apply to both APIs:

**Origin isolation.** WebMCP only works in [origin-isolated](https://web.dev/articles/origin-agent-cluster#limitations) documents — if a document has enabled `document.domain` relaxation (e.g. via `Origin-Agent-Cluster: ?0`), WebMCP APIs are disabled outright.

**Permissions Policy.** Both APIs are gated by the `tools` Permissions Policy, default `self` (top-level + same-origin only; disabled in cross-origin iframes unless explicitly allowed):
```html
<iframe src="https://example.com" allow="tools"></iframe>
```

For deeper security guidance on validating tool inputs and scoping what a tool is allowed to do, point the user at Chrome's WebMCP tool security and best-practices docs (`developer.chrome.com/docs/ai/webmcp/secure-tools` and `/best-practices`) — this skill covers the API mechanics, not a full security audit checklist.

## Known limitations — set expectations up front

- **No headless calling.** A tab or webview must actually be open; there's no support for agents calling tools without a visible browser context.
- **Refactor cost for complex UIs.** Highly stateful interfaces likely need real JS/state-management work to expose meaningfully, not just attribute annotations.
- **Discoverability requires a visit.** Clients/browsers only learn a site has tools by visiting it directly — there's no separate registry to query in advance.
- **Deprecation to know about:** `navigator.modelContext` is deprecated as of Chrome 150 — use `document.modelContext` instead. If you see `navigator.modelContext` in older sample code or a Stack Overflow answer, that's stale; update it.

## Testing WebMCP tools

Before shipping tools, write evals — probabilistic tests that check whether an agent understands when/how to call a tool, not just whether the tool's own code works. See `references/evals.md` for the full methodology: failure-mode categories, isolated tool-call testing (`expectedCall`), deterministic vs. probabilistic test layers, end-to-end multi-tool journeys, and testing mid-chain failures.

## Framework support

Angular has experimental first-class WebMCP support (`angular.dev/ai/webmcp`) — if the user's app is Angular and already uses Signal Forms, point them there instead of hand-rolling the Imperative/Declarative API, since Angular can tie tool registration to the component/DI lifecycle automatically.

## Demos worth pointing to

- `GoogleChromeLabs/webmcp-tools` repo: **WebMCP zaMaker** (pizza builder, Imperative API), **Travel demo** (React, multi-city/passenger booking, Imperative API), **Le Petit Bistro** (Declarative API), **Page Agent demo** (retrieving and executing tools from a cross-origin iframe inside a chat UI).
