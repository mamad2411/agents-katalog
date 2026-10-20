---
name: midscene-test
description: AI-driven UI automation testing using Midscene.js with Playwright. Write and run visual E2E tests using natural language descriptions. Supports multiple vision models (Doubao, OpenAI, Qwen3-VL, Gemini).
license: MIT
compatibility: opencode
metadata:
  type: testing
  framework: midscene.js
---

# Midscene.js Test Skill

AI-driven UI automation testing using Midscene.js with Playwright. Midscene.js is a vision-based testing framework that uses AI to understand and interact with web interfaces through natural language.

## Prerequisites

- Node.js (>=18)
- npm
- Playwright browsers (installed via `npx playwright install chromium`)

## Scripts Reference

Scripts are located at: `C:\Users\Administrator\.codebuddy\skills\midscene-test\scripts\`

### generate-test.js

Generate basic Midscene.js test files:

```bash
node C:\Users\Administrator\.codebuddy\skills\midscene-test\scripts\generate-test.js <target-url> <test-name>
```

Generates:
- `test.js` - Main test file with basic Playwright + Midscene.js structure
- `package.json` - Project dependencies

### run-test.js

Run Midscene.js tests with Playwright:

```bash
node C:\Users\Administrator\.codebuddy\skills\midscene-test\scripts\run-test.js <project-dir>
```

Automatically installs npm dependencies and Playwright browsers if needed.

## How To Test A Project

1. **Start the project server** - Make sure the web app is running and accessible
2. **Create test directory** - Create `midscene-test/` in the project root
3. **Generate test template** - Run the generate script with the target URL
4. **Customize tests** - Edit the generated `test.js` to add specific test cases
5. **Run tests** - Execute the test script
6. **View reports** - Check the generated report in `midscene-report/`

## Test Writing Tips

- Use `page.aiAct()` to describe actions in natural language
- Use `page.aiAssert()` to verify page state
- Use `page.aiLocate()` to find specific elements
- Use `page.aiWaitFor()` to wait for AI-identified states
- Keep test descriptions clear and specific
- Use the visual report to debug failed tests

## Model Configuration

Midscene.js supports multiple vision models. Set the `MIDSCENE_MODEL_API_KEY` environment variable or update the config file.

Supported providers:
- Doubao Seed (豆包) - Default
- OpenAI-compatible APIs
- Qwen3-VL
- Gemini
