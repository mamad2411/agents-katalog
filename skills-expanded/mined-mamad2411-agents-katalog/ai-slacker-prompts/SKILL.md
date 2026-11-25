---
name: ai-slacker-prompts
description: Eight battle-tested AI prompts for core dev tasks — PRD writing, UI/UX design brief, security audit, fast debugging, E2E tests, dead code cleanup, clean git commits, and turning a task into a reusable skill.
---

# AI Slacker Prompts

Eight prompts from the @ai_slacker "8 Claude prompts for devs" series.
Each covers a distinct dev workflow. Paste or adapt as needed.

## 01 — WRITE A FULL PRD

> Act as a senior product manager. Before writing anything, ask me 5 questions about users, scope and constraints. Then write a full PRD: problem, target user, user stories, core features (MVP vs later), success metrics, edge cases, and out-of-scope.

## 02 — FULL UI & UX DESIGN BRIEF

> Act as a product designer. From this PRD, produce a design brief: user flows, screen inventory, layout for each screen, component list, design tokens (colors, type scale, spacing), states (empty/loading/error/success), and accessibility notes.

**Tag line**: Design before you code. Always.

## 03 — FIND SECURITY GAPS

> Audit this codebase like a security engineer. Find auth flaws, exposed secrets, injection risks, insecure API routes, missing rate limits and unsafe data exposure. Rank by severity, explain the exploit, then give the exact fix.

## 04 — DEBUG AN ERROR FAST

> Here's the error + relevant code. Do NOT change anything yet. List the 3 most likely root causes ranked by probability, tell me exactly what to log or check to confirm each, and only after we confirm, write the fix.

## 05 — E2E TEST YOUR APP (PLAYWRIGHT)

> Set up Playwright for this project. Write E2E tests covering the critical user journeys: signup, login, core action, payment, logout. Include happy path + failure states. Use data-testid selectors, add fixtures for auth, and a script I can run in CI.

## 06 — CLEAN UP & REFACTOR DEAD CODE

> Scan this repo for dead code: unused files, components, imports, deps, env vars and commented-out blocks. Show me the list with proof it's unused BEFORE deleting. Then refactor duplicated logic into shared utils — behaviour must stay identical.

## 07 — WRITE CLEAN GIT COMMITS

> Review my staged changes. Split them into logical atomic commits. For each: a Conventional Commits message (feat/fix/refactor/chore), a scope, and a body explaining WHY not what. Give me the git commands to run in order.

## 08 — TURN A TASK INTO A SKILL

> I just did this task with you. Turn it into a reusable Skill: a clear name, a description of exactly when to trigger it, step-by-step instructions, examples, and common failure modes. Write it so a fresh model with zero context can execute it perfectly.

## When to use which

| Prompt | Stage |
|---|---|
| 01 PRD | Idea → spec |
| 02 Design Brief | Spec → screens |
| 03 Security Audit | Pre-launch / post-merge |
| 04 Debug Fast | Broken build / prod incident |
| 05 E2E Tests | Before shipping |
| 06 Dead Code | Refactor sprint |
| 07 Git Commits | Before PR |
| 08 Skill Creator | After any repeatable task |
