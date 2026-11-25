---
name: frontend-testing
description: The project's unique and mandatory frontend testing playbook, which must be consulted whenever doing anything related to testing and during the plan of any coding session. Without consulting this skill, you might perform things that deviate from the organization's standards.
allowed-tools: Read Grep Glob Bash mcp__playwright__* mcp__test-coverage__* Task  
metadata:
  version: "1.5.0"
---

# 🧪 Testing Skill

A key guide on how to plan and code with testing in mind inclding how to write tests efficiently, how run/debug tests and other crucial information for any coding session. Use this skill whenever planning any development, before coding, while planning tasks, during coding, and during testing. This ensures tests are considered from the start and written correctly

**Path tokens:**
- `{{TESTING_SKILL_DIR}}` resolves to the directory containing this SKILL.md file (the plugin's installed location). Agent and command files use this token so the skill works with any AI coding tool.
- `{{CONTEXT_ROOT}}` resolves to the root of the app/lib under test — the first directory above the current file that contains a `testskill.config.toml`. See [Skill UX & Behaviour](./references/skill-ux-and-behaviour.md) for the full resolution rule and STOP condition.

<div align="left">
  <img src="./assets/the-testing-skill.png" alt="Testing Skill Overview" width="150" />
</div>

---

## 📚 Skill Documents

| Document                                                              | Purpose                                                                                                           | When to Use                                                                                                                                                                                                                                                |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [IMPORTANT: The Test Workflow](./references/test-workflow.md)                    | The sequence of steps that must be followed when planning, writing, and verifying tests.                          | **MUST be read before any feature or test coding.** Follow this workflow from start to finish for any testing task - it ensures thorough context gathering before writing and proper verification after.                                                   |
| [🚀 Useful Commands](./references/test-commands.md)                              | Commands to start the application and run tests.                                                                  | Use these commands to get the system running for investigation, run tests before adding new ones to establish baseline, and run again after writing tests to verify they pass.                                                                             |
| [🎯 Testing Strategy & Tooling](./references/testing-strategy-and-tooling.md)    | Guidance on test types (page vs component vs unit), what outcomes to test, and which frameworks/libraries to use. | Consult during planning to decide test types, understand what to verify, and ensure you're using the recommended frameworks.                                                                                                                               |
| [📐 Test Code: Patterns & Practices](#-test-code-patterns--practices) | Mandatory rules and best practices for writing tests.                                                             | These rules must be read and followed every time tests are written. See detailed breakdown below.                                                                                                                                                          |
| [🔧 Test Tools (MCP) & Agents](./references/tools-and-agents.md)                 | MCP tools and specialized agents for testing workflows.                                                           | Reference when you need browser automation (Playwright), coverage measurement, test planning, fixing failing tests, or fixing accessibility issues. Includes testskill.planner, testskill.test-fixer, testskill.verifier, and testskill.locator-fixer agents. |

---

## 📐 Test Code: Patterns & Practices

**Read [The Test Anatomy](./references/rules/the-test-anatomy.md) before writing any test.**

**📌 Canonical Example:** For a real, working example that demonstrates all patterns, read the test configured in `{{CONTEXT_ROOT}}/testskill.config.toml` under `[canonical_example]`.

| Document                                                                                        | When to Use                                                                                                    |
| ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [The Test Anatomy](./references/rules/the-test-anatomy.md)                                | **Mandatory first read** - Core structure, 6 critical rules, AAA pattern, and examples                         |
| [File Structure](./references/rules/file-structure.md)                                    | Where to put test files and companion files (actions.tsx, factories.ts, httpMocks.ts, worker.ts)               |
| [The Test Data](./references/rules/the-test-data.md)                                      | When working with JSONs, entities, or any test input data                                                      |
| [Assertions](./references/rules/assertions.md)                                            | When writing expect statements and verifying outcomes                                                          |
| [Mocking](./references/rules/mocking.md)                                                  | When mocking external systems or network requests                                                              |
| [Testing with DOM](./references/rules/testing-with-dom.md)                                | When testing React components with testing-library or Playwright                                               |
| [Testing with Database](./references/rules/testing-with-database.md)                      | When tests interact with a real database                                                                       |
| [What to Test](./references/rules/what-to-test.md)                                        | When deciding coverage scope and edge cases                                                                    |
| ⚠️ [System-Wide E2E Best Practices](./references/rules/system-wide-e2e-best-practices.md) | **ONLY for system-wide E2E tests** spanning multiple processes - NOT for unit/component/integration/page tests |
