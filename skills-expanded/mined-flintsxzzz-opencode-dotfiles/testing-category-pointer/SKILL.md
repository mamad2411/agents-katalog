---
name: testing-category-pointer
description: "Pointer to a library of 30 specialized Testing skills. Use when working on testing-related tasks."
risk: none
---

# Testing Capability Library 🎯

This is a **pointer skill**. The 30 specialized Testing skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **ab-testing** — When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experimentation program.
- **agent-qa-authoring** — Create, edit, validate, and run Agent QA tests, suites, and hooks through MCP or CLI while preserving canonical IDs and schema contracts.
- **agent-qa-debug-fix** — Debug, patch, and verify failed Agent QA runs from MCP evidence, artifacts, logs, and local code without hiding product or infrastructure defects.
- **agent-qa-result-triage** — Triage failed Agent QA runs with MCP evidence, artifacts, logs, fixed failure categories, confidence, and actionable next steps.
- **android-ui-journey-testing** — XML-specified Android UI journey testing, interactive step execution, assertion verification, and JSON outcome reporting.
- **bats-testing-patterns** — Master Bash Automated Testing System (Bats) for comprehensive shell script testing. Use when writing tests for shell scripts, CI/CD pipelines, or requiring test-driven development of shell utilities.
- **brooks-test** — Review test-suite quality using established testing literature; identify brittleness, mock abuse, unclear fixtures, weak assertions, slow feedback, and maintenance risks.
- **browser-testing-with-devtools** — Test browser apps with Chrome DevTools MCP by inspecting live DOM, console logs, network traffic, screenshots, accessibility, and performance traces.
- **cypress-skill** — Generates production-grade Cypress E2E and component tests in JavaScript or TypeScript. Supports local execution and TestMu AI cloud. Use when the user asks to write Cypress tests, set up Cypress, test with cy commands, or mentions "Cypress", "cy.visit", "cy.get", "cy.intercept".
- **k6-load-testing** — Comprehensive k6 load testing skill for API, browser, and scalability testing. Write realistic load scenarios, analyze results, and integrate with CI/CD.
- **lambdatest-agent-skills** — Production-grade test automation skills for 46 frameworks across E2E, unit, mobile, BDD, visual, and cloud testing in 15+ languages.
- **mock-hunter** — Audit a live web page in five phases (catalog, click, trace, classify, report) to identify mock data, hardcoded values, LLM-generated metrics, and broken endpoints. Outputs a markdown report with REAL/MOCK/LLM/HARDCODED/BROKEN/UNKNOWN verdicts per visible value.
- **network-101** — Configure and test common network services (HTTP, HTTPS, SNMP, SMB) for penetration testing lab environments. Enable hands-on practice with service enumeration, log analysis, and security testing against properly configured target systems.
- **pypict-skill** — Pairwise test generation
- **pytest-skill** — Generates production-grade pytest tests in Python with fixtures, parametrize, markers, mocking, and conftest patterns. Use when user mentions "pytest", "conftest", "@pytest.fixture", "@pytest.mark", "Python test".
- **screen-reader-testing** — Practical guide to testing web applications with screen readers for comprehensive accessibility validation.
- **smartui-skill** — Generates SmartUI visual regression test configurations for screenshot comparison on TestMu AI cloud. Framework-agnostic — works with Playwright, Selenium, Cypress, Puppeteer. Use when user mentions "SmartUI", "visual regression", "screenshot comparison", "visual testing".
- **tdd-orchestrator** — Master TDD orchestrator specializing in red-green-refactor discipline, multi-agent workflow coordination, and comprehensive test-driven development practices.
- **tdd-workflow** — Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle.
- **tdd-workflows** — Use when working with tdd workflows tdd cycle (Alias for tdd-workflows-tdd-cycle)
- **tdd-workflows-tdd-cycle** — Use when working with tdd workflows tdd cycle
- **tdd-workflows-tdd-green** — Implement the minimal code needed to make failing tests pass in the TDD green phase.
- **tdd-workflows-tdd-red** — Generate failing tests for the TDD red phase to define expected behavior and edge cases.
- **tdd-workflows-tdd-refactor** — Use when working with tdd workflows tdd refactor
- **temporal-python-testing** — Comprehensive testing approaches for Temporal workflows using pytest, progressive disclosure resources for specific testing scenarios.
- **test-driven-development** — Use a failing behavioral test to guide a feature or bug fix, then implement and refactor with relevant regression checks.
- **test-framework-migration-skill** — Migrates and converts test automation scripts between Selenium, Playwright, Puppeteer, and Cypress.
- **test-guard** — Review generated or changed test code against universal testing rules before it ships or is presented for approval.
- **testing-patterns** — Jest testing patterns, factory functions, mocking strategies, and TDD workflow. Use when writing unit tests, creating test factories, or following TDD red-green-refactor cycle.
- **unit-testing-test-generate** — Generate comprehensive, maintainable unit tests across languages with strong coverage and edge case focus.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/testing/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/testing`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
