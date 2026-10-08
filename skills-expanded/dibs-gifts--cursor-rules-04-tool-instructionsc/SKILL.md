---
description: **IMPERATIVE:** You must confirm that you have access to and have loaded the required "MCPs" (Model Context Protocols, or tool instructions) before beginning any task.
---

# 04: Tool & "MCP" Instructions

**IMPERATIVE:** You must confirm that you have access to and have loaded the required "MCPs" (Model Context Protocols, or tool instructions) before beginning any task.

## 1. Pre-Task Checklist

Before you write or modify any code, you must verify the following:

1.  **DaisyUI Blueprint Loaded:** Confirm that you have loaded the `daisyui-blueprint` MCP. This is essential for all UI-related tasks. Your instructions are located in `/.github/instructions/daisyui.instructions.md`.

2.  **NO AUTOMATED BROWSER SCREENSHOTS:** You are **STRICTLY PROHIBITED** from using any browser MCP tools to take screenshots automatically. This includes but is not limited to:
    *   `mcp__browsermcp__take_screenshot`
    *   `mcp__browsermcp__browser_screenshot`
    *   Any other browser automation screenshot functionality

**If you cannot confirm both of these points, do not proceed. State what is missing and await further instructions.**

## 2. Screenshot Policy - CRITICAL

**MANDATORY RULE:** You must **NEVER** attempt to take screenshots using browser automation tools.

*   **What you MUST do:** Always request that the user manually take and send you a screenshot of the UI you need to review.
*   **What you MUST NOT do:** Never use browser MCP screenshot tools, navigate to pages to capture screenshots, or attempt any automated screenshot capture.
*   **Reasoning:** Manual screenshots ensure the user controls what is shared and prevents potential errors or unexpected behavior from automated browser tools.

### How to Request Screenshots

When you need to see the UI, use this approach:

```
To help you with [specific task], I need to see the current state of the UI. 

Please take a screenshot of [specific page/component] and share it with me. 
I'll then be able to provide feedback and suggestions.
```

**This rule applies to EVERY conversation and EVERY UI-related task without exception.**

## 3. How to Use the Instructions

*   **DaisyUI:** When asked to create or modify UI, you should use the `daisyui-blueprint` tool to find the correct components and then implement them according to the guidelines in `03-styling.md`.

*   **Browser Validation:** The user will provide screenshots for you to review. You should analyze these screenshots to ensure components appear correctly, are responsive, and match the requested design.

## 4. Development Server

The application's development server can be started from the `app/` directory.

*   **Command:** `npm run dev`
*   **URL:** The server typically runs on `http://localhost:3000`.

The user should have this server running when they provide screenshots of their work.

## 5. Updating Rules

Everytime MCP or rules are adjusted, they're adjusted in `.rulesync/rules/*`. Then the following command is run:

```bash
npx rulesync generate --targets copilot,cursor,claudecode --features "*"
```
