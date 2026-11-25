---
name: auto-qa
description: Autonomous intent-driven QA testing engine supporting dual-mode operation (Antigravity Agent Skill CLI and Stdio MCP Server). Features self-healing Playwright execution, native .spec.ts compiler, active modal isolation, and black-box surface crawler for client websites or localhost apps. Use whenever the user asks to test web workflows, audit client websites without source code, run automated QA, or generate TestSprite-compliant plans.
---

# Auto-QA: Autonomous Intent-Driven QA Engine

An autonomous web QA testing toolchain that executes end-to-end user journeys against any web application (local dev server or live website) using plain-English human intents, self-healing W3C accessibility heuristics, active modal isolation, and native `@playwright/test` compilation.

---

## 1. Dual-Mode Operation Decision Rule

Before taking any action, inspect your declared tools:

* **MODE 1: MCP Tool Mode**:
  If tools starting with `auto_qa_` (e.g. `auto_qa_execute_and_heal`) are available in your active tool list, call them directly via JSON-RPC.
* **MODE 2: Antigravity Skill CLI Mode (Default & Standalone)**:
  If no `auto_qa_*` MCP tools are declared, execute all QA actions via `run_command` using the unified CLI:
  ```bash
  node "<skillPath>/scripts/cli.js" <command>
  ```
  *(Resolve `<skillPath>` to `~/.gemini/config/skills/auto-qa` or the repository root).*

---

## 2. The 3-Stage Testing Lifecycle

### Stage 1: Surface Discovery (Map Accessible Controls)
Crawl the target URL to extract interactive buttons, inputs, links, and modal dialogs.
* **MCP Mode**: Call `auto_qa_generate_code_summary(projectPath, url)`.
* **Skill CLI Mode**:
  ```bash
  node "<skillPath>/scripts/cli.js" discover http://localhost:3000 -o auto_qa_tests/tmp/surface.json
  ```

### Stage 2: Intent Plan Authoring (`auto_qa_frontend_test_plan.json`)
Author the declarative test plan in `auto_qa_tests/auto_qa_frontend_test_plan.json`.
* **MCP Mode**: Call `auto_qa_generate_frontend_test_plan(projectPath, name, planSteps)`.
* **Skill CLI Mode**: Write the JSON file directly using your file creation tool:

```json
{
  "$schema": "https://raw.githubusercontent.com/TestSprite/testsprite-cli/main/schemas/plan.schema.json",
  "projectId": "project-name",
  "type": "frontend",
  "name": "User Registration & Login Flow",
  "targetUrl": "http://localhost:3000",
  "priority": "p0",
  "planSteps": [
    { "type": "action", "description": "navigate to http://localhost:3000/login" },
    { "type": "action", "description": "type 'qa-tester@example.com' into 'Email'" },
    { "type": "action", "description": "type 'TestPass123!' into 'Password'" },
    { "type": "action", "description": "click 'Sign In'" },
    { "type": "assertion", "description": "verify 'Dashboard' is visible" },
    { "type": "assertion", "description": "verify URL contains '/dashboard'" }
  ]
}
```

#### Supported Intent Verbs (Case-Insensitive, Single or Double Quotes):
* **Actions**:
  * `navigate to <http(s)://url>` / `go to </path or http(s)://url>`
  * `type '<text>' into '<target>'` / `fill '<text>' into '<target>'`
  * `click '<target>'` / `press '<target>'`
  * `select '<option>' from '<target>'`
  * `check '<target>'` / `tick '<target>'`
* **Assertions**:
  * `verify '<target>' is visible` / `appears`
  * `verify '<target>' is not visible` / `disappears`
  * `verify text '<text>'` / `contains '<text>'`
  * `verify URL contains '<path>'`

### Stage 3: Execution, Self-Healing & Code Compilation
Execute the declarative test plan with self-healing element resolution, capture failure screenshots, and export native code.
* **MCP Mode**:
  * Run: `auto_qa_execute_and_heal(projectPath, planFile, baseUrl)`
  * Export: `auto_qa_compile_to_playwright(planPath, outputPath)`
* **Skill CLI Mode**:
  * **Execute Test**:
    ```bash
    node "<skillPath>/scripts/cli.js" run auto_qa_tests/auto_qa_frontend_test_plan.json -u http://localhost:3000
    ```
    *(Note: Exit code 1 indicates an assertion failure under test. Inspect `auto_qa_tests/artifacts/` for screenshots and `auto_qa_tests/auto-qa-test-report.md` for step timings and error traces).*
  * **Compile to Native Playwright TypeScript**:
    ```bash
    node "<skillPath>/scripts/cli.js" compile auto_qa_tests/auto_qa_frontend_test_plan.json -o tests/e2e/flow.spec.ts
    ```

---

## 3. CLI Subcommand Summary

| Subcommand | Purpose | Default Output |
| :--- | :--- | :--- |
| `doctor` | Preflight check for Node, Playwright, and Chromium binary. | Terminal status |
| `discover <url> [-o <file>]` | Crawls website and extracts buttons, inputs, links, modals, and accessibility tree. | JSON surface map |
| `run <planFile> [-u <url>] [-o <dir>]` | Executes intent plan with self-healing resolution. | `auto_qa_tests/artifacts/` + `auto-qa-test-report.md` |
| `compile <planFile> [-o <file>]` | Compiles declarative plan into native `@playwright/test` `.spec.ts`. | `<planName>.spec.ts` |
| `bootstrap [dir] [-u <url>]` | Initializes `auto_qa_tests/tmp/config.json`. | `config.json` |
| `mcp` | Starts the stdio JSON-RPC 2.0 MCP server. | stdio stream |

---

## 4. The 5-Layer Verification Strategy

When asked to *"Test everything"* or audit an unfamiliar web application:
1. **Layer 1: Navigation & Routes**: Crawl navbar and footer links; assert no 404 responses.
2. **Layer 2: Interactive Controls**: Test dropdowns, accordions, theme toggles, and filter buttons.
3. **Layer 3: Form Validation Funnels**:
   - **Happy Path**: Submit valid inputs → assert success banner or state update.
   - **Error Path**: Submit empty required fields → assert inline validation alerts.
4. **Layer 4: Authentication Lifecycle**: Valid login, invalid credentials rejection, session persistence, and logout.
5. **Layer 5: Core CRUD Workflows**: Create item → assert listed; modify item → assert updated; delete item → assert removed.
