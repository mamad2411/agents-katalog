---
name: chrome-devtools-tools
description: "An overview of the automation, debugging, and memory tracking tools exposed by the Chrome DevTools MCP server."
---

# Chrome DevTools MCP Tools

When connected to `chrome-devtools-mcp`, your agent gains dozens of specialized tools to interact with web pages, eliminating the need to write custom Puppeteer scripts for basic validation tasks.

## Tool Categories

### 1. Navigation & Automation
*   **`navigate_page` / `new_page`**: Drive the browser to target URLs.
*   **`click` / `fill` / `type_text`**: Interact with DOM elements natively.
*   **`wait_for`**: Pauses execution until a specific DOM element appears or a network idle state is reached.

### 2. Debugging & Network
*   **`take_screenshot`**: Captures the viewport (supports `png`, `jpeg`, and resizing via `--screenshotMaxWidth`).
*   **`evaluate_script`**: Runs arbitrary JavaScript in the page context to extract data or manipulate the DOM.
*   **`get_network_request` / `list_network_requests`**: Inspect payloads, headers, and response codes of network traffic.
*   **`get_console_message`**: Pulls warnings, errors, and standard logs from the browser console, complete with source-mapped stack traces.

### 3. Performance & Memory
*   **`lighthouse_audit`**: Triggers a full Lighthouse scan directly through the browser.
*   **`performance_start_trace` / `performance_stop_trace`**: Generates highly granular performance traces for Core Web Vitals analysis.
*   **`take_heapsnapshot` / `get_heapsnapshot_summary`**: Powerful tools for debugging memory leaks in JavaScript applications by analyzing retained objects and dominators.

### 4. Extensions
*   **`install_extension` / `reload_extension`**: Automates the testing of Chrome Extensions by loading them into the active browser session.
