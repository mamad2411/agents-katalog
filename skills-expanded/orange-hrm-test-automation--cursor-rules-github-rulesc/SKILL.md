---
description: GitHub MCP server rules for Orange HRM Automation Project, integrating Jira tickets in PRs
globs:
  - "*"
alwaysApply: true
---
# GitHub MCP Server Rules

When raising a pull request (PR), include the associated Jira ticket key (e.g., AUTH-123, OHR-456) in both the PR title and description.

**PR Title Format**:  
Use the format `[JIRA_KEY] Brief description of changes`, e.g., `[AUTH-123] Add login validation tests`.

**PR Description**:
- Include a section titled **"Jira Ticket"** with the ticket key and a link to the Jira issue, e.g.,  
  `Jira Ticket: [AUTH-123](https://your-domain.atlassian.net/browse/AUTH-123)`
- Provide a **summary of changes**, including the purpose of the PR and key files modified.
- Reference relevant commits or test files (e.g., `login.test.ts`) to provide context.
- Use the GitHub MCP server to automate PR creation and Jira ticket linking where possible, leveraging natural language commands like  
  `"Create a PR for AUTH-123 with description including test updates."`
- Ensure PRs follow team coding standards (e.g., Prettier with 2-space indentation, TypeScript usage) as defined in `@code-formatting.mdc`.

---

## 🔁 PR Pre-Check
- Before raising a PR, ensure the **Playwright tests pass locally via the MCP server**.
- Only after successful local validation, proceed to raise the PR.
- GitHub Actions will re-run the tests **on a single execution node** for consistency and resource control.

---

## 👥 Review & Workflow
- Assign at least **one reviewer**
- Link the PR to the **associated Jira ticket’s epic**, if applicable
- Assign **Co-Pilot as a reviewer** once the PR is raised

---

## 🧪 Test Results
- Include **test results** or **references to executed test files** (e.g., `*.test.ts`)
- Indicate which browser (e.g., **Chrome**) and environment the tests were run on, per `@test-automation.mdc`
