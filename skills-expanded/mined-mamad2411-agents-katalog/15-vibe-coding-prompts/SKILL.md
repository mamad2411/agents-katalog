---
name: 15-vibe-coding-prompts
description: 15 high-leverage Claude Code prompts for full-stack vibe coding — from writing a PRD and CLAUDE.md through Ultra Plan Mode, spec-driven development, UI/UX briefs, MCP server wiring, database connection, security auditing, debugging, E2E testing, dead code cleanup, git commits, hooks as guardrails, and turning a task into a reusable skill. Use these as templates to get consistent, structured outputs from Claude Code on every project. Source: @your_ai_mentor.
---

# 15 Vibe Coding Prompts for Claude Code

Copy-paste-ready prompts for each phase of a Claude Code development workflow.

---

## 01. Write a Full PRD

```
Write a complete Product Requirements Document for [product name].

Include:
- Problem statement and target user
- Goals and non-goals
- User stories (As a [user], I want [action], so that [benefit])
- Functional requirements (numbered list)
- Non-functional requirements (performance, security, scalability)
- Success metrics
- Out of scope

Format as a structured markdown document.
```

---

## 02. Create Your CLAUDE.md

```
Analyse this codebase and generate a CLAUDE.md file that tells Claude Code:

1. Project overview (what it is, what it does)
2. Tech stack and key dependencies
3. Architecture overview (main directories and what lives in each)
4. How to run the project locally (exact commands)
5. How to run tests
6. Code style and conventions this project follows
7. Common patterns used in this codebase
8. Things Claude should NEVER do in this project
9. Frequently needed context (env vars, config, special setup)

Be specific. Use examples from the actual codebase.
```

---

## 03. Ultra Plan Mode

```
Before writing any code, enter Ultra Plan Mode.

For the task: [describe task]

Produce:
1. A clear restatement of what needs to be built
2. Files that will be created or modified (with reasons)
3. Step-by-step implementation plan (numbered)
4. Potential risks or blockers
5. Questions to resolve before starting

Do NOT write any code yet. Wait for my approval.
```

---

## 04. Spec-Driven Development

```
Create a detailed technical specification for: [feature name]

The spec must include:
- Data models / schema changes
- API endpoints (method, path, request body, response)
- Business logic rules
- Edge cases and how to handle them
- Error states
- Test cases (unit + integration)

Do not implement yet. I will review the spec first.
```

---

## 05. Full UI & UX Design Brief

```
Create a full UI/UX design brief for: [screen or feature name]

Include:
- Component hierarchy (what renders what)
- States: empty, loading, error, success, edge cases
- Interaction patterns (hover, click, keyboard)
- Responsive behaviour (mobile, tablet, desktop)
- Accessibility requirements (ARIA, keyboard nav, contrast)
- Copy / microcopy for all user-facing text
- Design tokens needed (colours, spacing, typography)

Output as a structured specification, not code.
```

---

## 06. Implementation Plan

```
Given the spec/PRD above, create a step-by-step implementation plan.

For each step:
- What to build
- Which files to touch
- Dependencies that must exist first
- Estimated complexity (S/M/L)
- Acceptance criteria

Order steps so each one is independently testable.
```

---

## 07. Wire Up an MCP Server

```
Wire up the [MCP server name] MCP server to this project.

Steps needed:
1. Install the server package
2. Add it to the Claude Code MCP configuration
3. Write a SKILL.md that documents what the server can do and when to use each tool
4. Test with a sample tool call

Show me the exact config changes and SKILL.md content.
```

---

## 08. Connect Your Database

```
Connect a [PostgreSQL / MySQL / SQLite / Supabase / MongoDB] database to this project.

Provide:
1. Connection configuration (env vars needed)
2. Connection pooling setup
3. A base query helper / ORM setup
4. Migration tooling setup
5. A seed script for development data
6. How to run migrations locally and in CI

Use the project's existing tech stack. Do not add unnecessary libraries.
```

---

## 09. Find Security Gaps

```
Audit this codebase for security vulnerabilities.

Check for:
- SQL injection (raw queries, ORM misuse)
- XSS (unescaped user input in HTML)
- CSRF (missing tokens on state-changing endpoints)
- Authentication gaps (unprotected routes, weak session management)
- Insecure direct object references (IDOR)
- Sensitive data in logs or error messages
- Hardcoded secrets or credentials
- Dependency vulnerabilities (outdated packages with known CVEs)

For each finding: severity (Critical/High/Medium/Low), location, and recommended fix.
```

---

## 10. Debug an Error Fast

```
I have this error:

[paste full error message and stack trace]

Context:
- What I was doing when it occurred: [describe]
- What I have already tried: [list]
- Relevant code: [paste or say "see attached file"]

Diagnose the root cause. Do not suggest generic fixes. Give me the specific line to change and why.
```

---

## 11. E2E Test Your Application

```
Write end-to-end tests for the [feature name] user flow using [Playwright / Cypress].

Cover:
1. Happy path — user completes the flow successfully
2. Validation errors — form submission with missing/invalid fields
3. Edge cases: [list specific edge cases]
4. Error states: [API failure, network timeout]

Use the existing test setup in this project. Add realistic test data, not generic lorem ipsum.
```

---

## 12. Clean Up Dead Code

```
Find and remove dead code in this codebase.

Look for:
- Unused exports (functions, components, constants exported but never imported)
- Commented-out code blocks
- Feature-flagged code for flags that are always-on or have been removed
- Duplicate implementations of the same utility
- Unreachable code paths

For each removal, confirm the code is truly unused before deleting. Show me the list first.
```

---

## 13. Write Clean Git Commits

```
Review the staged changes and write a git commit message that:

1. Uses the conventional commits format: type(scope): short description
   - Types: feat, fix, refactor, test, docs, chore, style, perf
2. Subject line: ≤72 characters, imperative mood ("add" not "adds")
3. Body (if needed): explains WHY, not WHAT
4. Breaks changes into multiple commits if they represent distinct logical changes

Show me the proposed commit message(s) before committing.
```

---

## 14. Hooks as Guardrails

```
Set up Claude Code hooks to enforce these guardrails in this project:

1. Pre-tool-call: Block any bash command that contains `rm -rf` unless it targets /tmp
2. Pre-tool-call: Warn before any git push to main/master
3. Post-tool-call: After any file edit, check that no console.log statements were added to production files
4. Notification: Alert when a tool call fails with a non-zero exit code

Write the hooks as shell commands in .claude/settings.json format.
```

---

## 15. Turn a Task Into a Skill

```
I just completed this task: [describe what you built or figured out]

Turn it into a reusable Claude Code skill by creating .claude/skills/[skill-name]/SKILL.md.

The skill should:
1. Have a clear one-line description for the YAML frontmatter
2. Explain WHEN to invoke this skill (trigger conditions)
3. Document the step-by-step process used
4. Include any reusable code snippets or commands
5. Note any gotchas or edge cases discovered

Make it specific enough to be useful, general enough to apply to future projects.
```

---

## Quick-reference by phase

| Phase | Prompt # |
|---|---|
| Planning | 01 PRD, 03 Ultra Plan, 04 Spec |
| Design | 05 UI/UX Brief, 06 Implementation Plan |
| Setup | 02 CLAUDE.md, 07 MCP Server, 08 Database |
| Build | (use specs from above) |
| Quality | 09 Security, 10 Debug, 11 E2E Tests |
| Cleanup | 12 Dead Code, 13 Git Commits |
| Automation | 14 Hooks, 15 Skill |

Source: @your_ai_mentor
