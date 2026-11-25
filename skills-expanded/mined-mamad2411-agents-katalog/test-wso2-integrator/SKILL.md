---
name: test-wso2-integrator
description: Test WSO2 Integrator UI
license: Apache 2.0
---

# WSO2 Integrator

WSO2 Integrator is a visual integration development tool. It lets you build integration services (HTTP APIs, proxies, etc.) through a graphical flow editor rather than writing code by hand.

## Key Characteristics of WSO2 Integrator

- VS Code-based — Runs inside VS Code as an extension with a webview UI (guest frame) alongside VS Code's native chrome (host frame)
- Visual flow editor — You design service logic by adding nodes (Return, If, etc.) to an SVG-based flow diagram, connecting them visually
- Code generation — Behind the scenes it generates Ballerina (.bal) source code from the visual flow
- Connectors — Supports HTTP connections and others via a connector palette
- Integrated run/debug — Has "Run Integration" that compiles and runs the Ballerina project, starting an HTTP listener (default on localhost:9090)
- Ships with a monitoring tool, WSO2 ICP.

## Testing

Use Playwright based cli tool `wso2ipw` to drive Integrator programmatically. Install with user consent (npm install -g wso2ipw).

Break the task into chunks, for each chunk create a sh, run and test, repeat until success, move to next chunk. See examples dir.

It's always possible to modify the Ballerina code directly to get the output. Yet, the whole point of this effort the Integrator **UI**. Try to mimic a real user’s UI actions as much as possible. **NEVER** edit bal file directly. It's OK to use CLI (curl) background tasks such as verify the produced service is up.

You may sometimes need some mocks to write the integrations, prompt users for a couple of options and implement those (e.g. create a hello service in node). The user is not interested in technical minutiae of the mocks, only about issues in ICP, pre pick answers and only get confirmation.

Don't try to open project, the cli can't control the native open dialog box.

Try to avoid timed wait and sleep, instead use wait-for-text. Try to avoid conditional flows (except in final testing)

## Commands

- app: open [--user-data-dir=path], close
- inspect: snapshot, screenshot [file], eval <g:|h:><js>
- interact: click/dblclick <g:|h:><ref> [--force], fill <g:|h:><ref> <text> (fill will auto detect input type (plain, cm) and act. Use fill over type for input boxes)
- keys: type <text>, press <key>
- util: wait [ms], wait-for-text <text> [--timeout=N] [--hidden]
- flags: --force (bypass overlay/pointer-event checks, default for g:)

# Report

At the end, **MUST** report bugs, limitations, and UX issues in WSO2 Integrator (not in wso2ipw). Try to focus on bugs that would be detrimental to a real user not an automation/screen reader.
