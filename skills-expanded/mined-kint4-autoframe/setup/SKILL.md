---
name: setup
description: Bootstrap the Autoframe framework for a specific product: asks about the app, then wires a ready-to-run Playwright suite. Use when the user runs /setup, asks to set up or initialize Autoframe, or wants to start a test suite for their app.
---

# /setup — Bootstrap the Autoframe Project

**Type:** Setup
**Description:** Bootstraps the entire Autoframe framework for a specific product. Asks for the app URL, auth type, stack details, and CI platform, then produces a fully wired, ready-to-run Playwright project. Includes a simple mode for non-technical users.

---

## Input Format

The user runs `/setup`. Gather the following before generating anything:

1. **App URL** — the base URL of the product under test (`BASE_URL`)
2. **API URL** — base URL for API tests, if any (`API_URL`)
3. **Auth type** — none / form login / token / SSO
4. **First feature to cover** — e.g. `auth`, `checkout`
5. **CI platform** — defaults to GitHub Actions

If the user signals they are non-technical (Persona 1 or 4), switch to **simple mode**: ask only for the app URL and what they want to test first, and explain each step in plain language.

## Output Format

A fully scaffolded project that matches the folder structure in CLAUDE.md, with:
- `playwright.config.ts`, `tsconfig.json`, `package.json`
- `.env.example` populated with the discovered variables
- `.gitignore`
- The three GitHub Actions workflows (`e2e.yml`, `api.yml`, `load.yml`)
- One starter Page Object, spec, and fixture for the first feature
- A short summary of what was created and how to run it

## Step-by-Step Instructions

1. Read `CLAUDE.md` and `AUTOFRAME.md` completely.
2. Detect the persona from the user's language (see CLAUDE.md). Adjust tone and depth.
3. Ask the clarifying questions above (max 3 at a time). In simple mode, ask the minimum.
4. Verify the folder structure exists; create any missing directories exactly as defined in CLAUDE.md.
5. Generate or confirm the baseline config files. Never substitute the stack.
6. Write `.env.example` with every required variable (`BASE_URL`, `API_URL`, `API_TOKEN`, `TEST_USER_EMAIL`, `TEST_USER_PASSWORD`). Never write a real `.env`.
7. Generate a starter Page Object + spec + fixture for the first feature, following the POM and spec conventions exactly.
8. Confirm the three CI workflows exist.
9. Summarize what was created and give the exact commands to install and run (`npm install`, `npx playwright install`, `npm test`).
10. Suggest the next skill to run (usually `/new-page` or `/tc-to-spec`).

## Rules

- Never deviate from the CLAUDE.md folder structure or stack.
- Never commit secrets; only ever write `.env.example`.
- In simple mode, never show config internals unless asked — explain outcomes.
