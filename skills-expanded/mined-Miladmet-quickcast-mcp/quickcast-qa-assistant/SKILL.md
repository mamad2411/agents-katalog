---
name: quickcast-qa-assistant
description: Turn screen recordings into production Playwright E2E tests, high-precision GitHub/Jira bug reports with timestamped video links, and step-by-step SOP documentation via the QuickCast Screen-to-Action MCP server.
compatibility: Claude Code, Cursor, Windsurf, Copilot Workspace, Antigravity, AGY
version: 1.0.0
author: Milmann (Watermark & Resize Studio)
license: MIT
mcp_server: quickcast-mcp
tags:
  - qa-automation
  - playwright
  - e2e-testing
  - bug-reporting
  - sop-generation
  - screen-recording
  - mcp
---

# QuickCast QA Assistant (Screen-to-Action)

The **QuickCast QA Assistant** empowers AI agents to convert screen recordings into actionable engineering assets:
1. **Executable Playwright E2E test suites** (TypeScript/JavaScript) replicating user flows.
2. **High-fidelity GitHub/Jira bug reports** with deep-linked video timestamps (`[00:15](video_url#t=15)`).
3. **Operational SOP guides** for team documentation and onboarding.

---

## ⚡ When to Activate This Skill

Activate this skill when the user requests:
- *"Convert my screen recording into a Playwright test"*
- *"Write an E2E test reproducing what happened in my recording"*
- *"File a GitHub issue / bug report from the latest QuickCast session"*
- *"Create an SOP or walkthrough guide from my demo video"*
- *"Inspect recent screen recordings and extract the user journey"*

---

## 🔌 MCP Server Setup

This skill interacts with the **`quickcast-mcp`** server.

### 1. Claude Code / Claude Desktop (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "quickcast": {
      "command": "npx",
      "args": ["-y", "quickcast-mcp"]
    }
  }
}
```

### 2. Cursor (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "quickcast": {
      "command": "npx",
      "args": ["-y", "quickcast-mcp"]
    }
  }
}
```

---

## 🛠️ MCP Tool Reference

| Tool Name | Purpose | Key Parameters |
| :--- | :--- | :--- |
| `get_latest_session` | Retrieves metadata, video URL, duration, and user actions from the latest or specified session | `sessionId` (optional) |
| `list_recent_sessions` | Lists the most recent recordings stored in the local profile | `limit` (default: 10) |
| `scaffold_playwright_test` | Generates runnable Playwright E2E test code matching recording actions | `sessionId`, `language` (`"typescript"` or `"javascript"`), `targetUrl` |
| `format_github_bug_report` | Generates a structured bug report with video timestamp bookmarks | `sessionId`, `title`, `expectedBehavior`, `actualBehavior` |
| `generate_sop_guide` | Generates step-by-step Standard Operating Procedure (SOP) in Markdown | `sessionId`, `procedureTitle`, `targetAudience` |
| `ingest_session` | Ingests new recording session telemetry into `~/.quickcast/sessions.json` | `session` (JSON payload) |

---

## 🚀 Execution Workflows

### Workflow 1: Screen Recording ➔ Executable Playwright Test

When the user asks to generate test automation from a recording:
1. **Fetch Session**:
   Call `get_latest_session` (or specify `sessionId`). Note the target URL, user click sequences, input fields, and timings.
2. **Scaffold the Test**:
   Call `scaffold_playwright_test` with `language: "typescript"` and the application base URL.
3. **Harden the Test**:
   - Ensure resilient locators are used (`page.getByRole`, `page.getByLabel`, `page.locator`).
   - Add assertion checkpoints (`expect(page).toHaveURL(...)`, `expect(locator).toBeVisible()`).
   - Integrate silent error trapping (`page.on('pageerror')`) to detect runtime crashes during reproduction.
4. **Save and Run**:
   Save the test into the project's test directory (e.g. `tests/` or `e2e/`) and offer to run `npx playwright test`.

---

### Workflow 2: Video Recording ➔ Timestamped GitHub Bug Report

When the user wants to log an issue based on a screen capture:
1. **Fetch Session & Markers**:
   Call `get_latest_session` to retrieve the Cloudflare R2 video watch URL and duration.
2. **Format the Report**:
   Call `format_github_bug_report`. Ensure the output includes:
   - **Video Evidence**: Clickable timestamp links jumping to the exact millisecond of failure (e.g. `[00:23](https://watch.quickcast.app/...#t=23)`).
   - **Environment Matrix**: Browser, OS, screen resolution, and target page URL.
   - **Step-by-Step Reproduction**: Discrete chronological steps.
   - **Console / Network Diagnostics**: Correlated network 4xx/5xx or runtime exceptions observed.
3. **Present Output**:
   Render the formatted Markdown directly or commit it to `.github/ISSUE_TEMPLATE/` as requested.

---

### Workflow 3: Demo Recording ➔ Team SOP Guide

When turning an onboarding or workflow recording into documentation:
1. **Fetch Session Data**:
   Call `get_latest_session`.
2. **Generate SOP**:
   Call `generate_sop_guide` with a descriptive `procedureTitle`.
3. **Refine Output**:
   Structure the generated guide into:
   - **Objective**: What the SOP achieves.
   - **Prerequisites**: Required permissions, roles, or environment.
   - **Visual Action Walkthrough**: Numbered steps with timecode references to the demo video.
   - **Troubleshooting & FAQs**: Common failure modes and fixes.

---

## 🛡️ Best Practices & Quality Standards

- **Strict URL Validation**: Always confirm the target domain before executing tests against live endpoints.
- **Flakiness Prevention**: Avoid hardcoded sleeps (`page.waitForTimeout`); prefer auto-waiting Playwright assertions (`expect(locator).toBeVisible()`).
- **Telemetry Privacy**: Never log credentials, API secrets, or personally identifiable data (PII) captured in screen telemetry into public bug reports.

---

## 🌐 Enterprise & Managed QA Services

For development teams that require dedicated, high-volume automated testing pipelines without manual configuration:
- Explore **Automated Testing as a Service (TaaS)**: [https://watermarkresizestudio.com/qa-automation/](https://watermarkresizestudio.com/qa-automation/)
- Comprehensive end-to-end regression protection, zero-cost CI monitoring, and rapid 48-hour suite scaffolding.
