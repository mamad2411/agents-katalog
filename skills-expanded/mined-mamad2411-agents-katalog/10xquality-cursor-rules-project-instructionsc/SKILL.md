---
description: Project-level instructions for the 10x Quality Framework
alwaysApply: true
---

# 10x Quality — AI-Powered UI Test Automation Framework

This is a QA test automation framework powered by Cursor AI and Chrome DevTools MCP. Test scripts are written in natural language and executed by the AI agent using browser automation.

## Project Structure

```
.
├── .cursor/rules/
│   ├── qa-script-executor.mdc              # Execute test scripts via Chrome DevTools MCP
│   ├── qa-recorder.mdc                     # Record manual browser interactions as test scripts
│   ├── script-to-bdd-converter.mdc        # Convert recorded scripts to Playwright+Cucumber tests
│   └── playwright-cucumber-conventions.mdc # BDD framework conventions + locator strategies
├── src/recorder/
│   ├── inject-recorder.js                  # Recorder script injected into browser
│   └── retrieve-events.js                  # Script to collect recorded events
├── scripts/
│   ├── template.md                         # Test script template
│   └── *.md                                # Test scripts (natural language)
├── reports/
│   └── test-report-*.md                    # Generated test reports
└── .mcp.json                               # MCP server configuration
```

## Three Ways to Create & Run Tests

### 1. Write manually (AI-powered execution)
Write a test script in `scripts/` using natural language, then ask:
"Please execute the test script at scripts/my-test.md"

### 2. Record from browser → Natural language script
Ask: "Record a test for https://example.com" — interact with the browser manually. The agent captures every click, type, and navigation with rich metadata (locators, labels, ambiguity counts), then generates a natural language script.

### 3. Record → Convert to Playwright + Cucumber BDD (recommended for CI/CD)
After recording, ask: "Convert scripts/my-test.md to Playwright + Cucumber tests."
The converter uses the recorded metadata (field labels, data-test attributes, DOM context) to generate Page Objects with reliable, unambiguous locators that work on the first run.

## Key Conventions

- Test scripts live in `scripts/` as markdown files
- Reports are generated in `reports/` with timestamp naming
- The Chrome DevTools MCP server is `chrome-devtools`
- Always use `take_snapshot` before interacting with page elements
- Scripts are enhanced in-place after successful execution
- Recorder scripts are in `src/recorder/` — injected via `evaluate_script`
