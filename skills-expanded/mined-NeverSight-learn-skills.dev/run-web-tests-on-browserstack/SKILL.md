---
name: run-web-tests-on-browserstack
description: Run automated web tests on BrowserStack Automate using setupBrowserStackAutomateTests MCP tool. Use for cross-browser testing with Selenium/Playwright/Cypress.
---

# Run Web Tests on BrowserStack

## When to Use

- Running web tests across multiple browsers
- Setting up CI/CD pipeline with BrowserStack
- Testing on real desktop browsers (Chrome, Firefox, Safari, Edge)
- Debugging cross-browser compatibility issues

## MCP Tools Used

- `setupBrowserStackAutomateTests` - Integrate BrowserStack SDK and run tests
- `fetchAutomationScreenshots` - Get screenshots from test sessions
- `getFailureLogs` - Retrieve error logs for failed tests

## Steps

### 1. Setup and Run Tests

Use the `setupBrowserStackAutomateTests` MCP tool:

```
"Run my Selenium tests on Chrome and Firefox using BrowserStack"
"Setup my Playwright tests for BrowserStack and run on Safari 17"
"Run my Cypress tests on Chrome 120 (Windows 11) and Edge (Windows 11)"
```

**What the tool does:**
- Integrates BrowserStack SDK into your test framework
- Configures browser capabilities automatically
- Runs tests on BrowserStack infrastructure
- Optionally enables Percy for visual testing

**Example:**
```
"Run my Selenium-JUnit5 tests written in Java on Chrome and Firefox. Enable Percy for visual testing."
```

### 2. Get Screenshots

Fetch screenshots from test sessions using `fetchAutomationScreenshots`:

```
"Get screenshots from Automate session ID abc123xyz"
"Show me screenshots from my last test run"
```

### 3. Debug Failures

Retrieve error logs using `getFailureLogs`:

```
"Get error logs from session ID 21a864032a7459f1e7634222249b316759d6827f"
"Show me failure logs from my last Automate test"
```

## Common Scenarios

**Setup Different Test Frameworks:**
```
"Setup my Playwright tests for BrowserStack Automate"
"Run my Selenium WebDriver tests on Chrome, Firefox, and Safari"
"Configure my Cypress tests to run on BrowserStack"
```

**Enable Visual Testing:**
```
"Run my tests on BrowserStack with Percy enabled for visual regression testing"
```

**Debug Failed Tests:**
```
"Get screenshots and error logs from session abc123"
"Show me what went wrong in my last Automate test run"
```

## Example Workflow

**User**: "I need to run my Playwright tests on Chrome, Firefox, and Safari"

**Steps**:
1. Setup: `"Setup my Playwright tests for BrowserStack and run on Chrome 120, Firefox 122, Safari 17"`
2. Tool executes: `setupBrowserStackAutomateTests` configures and runs tests
3. View results from BrowserStack dashboard or test output
4. If failures: `"Get error logs from the failed session"`
5. Debug: `"Show me screenshots from session XYZ"`

## Quick Tips

- Specify test framework (Selenium/Playwright/Cypress) in your prompt
- Include browser names and versions for precise targeting
- Use Percy integration for visual regression testing
- Session IDs are returned after test runs for debugging
- Screenshots and logs help diagnose cross-browser issues
