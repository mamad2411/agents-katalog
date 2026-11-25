---
name: plan
description: 'Plan a task from Notion ticket. Reads ticket, detects cross-stack, creates branch + plan. Use for medium/large tasks.'
---

# /plan - Task Planning

Plan implementation from a Notion ticket or task description.

**Input:** Notion ticket link or task description via `$ARGUMENTS`

## When to use /plan vs just /implement

- **Skip /plan** (use `/implement` directly): single file change, bug fix, simple CRUD, config tweak
- **Use /plan**: 2-5 files affected, new entity, new service, cross-module changes
- **Use /plan and split into phases**: 6+ files, new module, multiple entities, needs multiple PRs

## Workflow

### Step 1: Read the ticket and spec document

- Use Notion MCP to read the ticket properties and description
- **Extract and save the ticket ID** — read `userDefined:ID` property from Notion response (e.g., `CRM-1279`) — you will use this for branch naming in Step 5
- **Read the "Stacks" property** (multi-select: BE, FE, App) to determine scope
- **Read the linked Document** (the "Document" property on the ticket) - detailed spec with use cases, schema, business rules, acceptance criteria
- **Images/Diagrams:** If spec mentions diagrams/mockups, ask user to share them before proceeding
- Also read parent task description if it exists
- If no Notion link provided, use `$ARGUMENTS` as task description
- If Notion MCP is unavailable, ask user to paste ticket + spec content
- **If ticket has no linked Document or spec lacks key details**: flag as blocker in Step 3

### Step 2: Detect stack and cross-stack scope

**Detect current stack:** Read `package.json` to determine current repo's stack (nestjs/nextjs/react-native).

**Determine scope from ticket status fields:**
- **Cross-stack**: ticket has BOTH `BE Status` AND `FE Status` properties → each stack plans and implements separately
- **Single-stack BE**: ticket has `BE Status` only (no `FE Status`)
- **Single-stack FE**: ticket has `FE Status` only (no `BE Status`)
- **Neither field**: infer from ticket description, or ask user

**For cross-stack tasks, also check Notion comments:**
- If another stack already posted an **API contract** → reference it in your plan
- If no API contract yet and current stack is BE → you will create one in Step 5

### Step 3: Analyze the codebase using docs

**3a — Read the index first (no scouting):**
- Read `docs/module-index.md` → identify which modules/files will be affected
- Read `docs/code-standards.md` and `docs/system-architecture.md` for patterns and architecture

**3b — Read targeted files:**
- Use file paths from `module-index.md` to open only the files relevant to this feature
- Check for existing similar implementations as reference
- Trace dependencies: check what imports/consumes the files you plan to change

**If `module-index.md` doesn't exist:** run `/docs init` first, or fall back to targeted Grep. Broad codebase scouting is a last resort.

### Step 4: Flag unclear or missing details

After reading BOTH the spec AND the codebase, check for:
- **Ambiguous requirements**: vague descriptions, conflicting use cases
- **Missing information**: no schema, missing field types/constraints
- **Assumptions needed**: edge cases not covered, integration points not specified
- **Conflicts with existing codebase**: spec differs from current architecture
- **Missing spec**: ticket has no Document — this is a **blocker**

**If concerns found**: STOP and ask user. List all questions.
**If clear**: Proceed. Note minor assumptions in plan's "Key decisions" section.

### Step 5: Create branch

**Check current branch:**
- If already on a feature branch → skip branch creation
- If on `main` or `master` → create a new branch

**Branch naming:** Use the ticket `ID` extracted in Step 1 (e.g., `RRR-351`):
```bash
git checkout -b feature/{ticket-id}-{short-slug}

# Examples:
git checkout -b feature/RRR-351-user-profile-api     # feature (BE)
git checkout -b feature/RRR-351-user-profile-ui      # feature (FE)
git checkout -b fix/RRR-351-payment-timeout          # bug fix
git checkout -b chore/upgrade-next-15                # chore (no ticket)
```

> Never use the Notion page UUID from the URL — always use the `ID` property value.

**Determine type from ticket:** feature → `feature/`, bug → `fix/`, hotfix → `hotfix/`, chore → `chore/`

If no ticket ID available, use descriptive slug only: `feature/user-profile-api`

### Step 6: Create the plan file

Save to `plans/[brief-task-name].md`. Create `plans/` directory if needed.
Also display the plan in the conversation.

**Plan file format (single-stack or scoped for current stack):**

```markdown
# Plan: [task title]

**Ticket:** [link if provided]
**Spec:** [link to Document]
**Branch:** `feature/RRR-351-slug`
**Stack:** [current stack: nestjs/nextjs/react-native]
**Cross-stack:** [Yes (BE + FE) / No]
**Created:** [date]

## Context

[Brief summary: what this feature does, why, key user flows]

## API Contract (cross-stack only)

| Method | Endpoint | Request body | Response |
|--------|----------|-------------|----------|
| GET | /api/... | - | { field: type } |
| POST | /api/... | { field: type } | { field: type } |

## Schema / data changes (if any)

- [ ] [migration, model, or schema change with exact field definitions]

## New files

- [ ] `src/path/file.ts`: [purpose and what it contains]

## Modified files

- [ ] `src/path/file.ts`: [what to change and why]

## Implementation order

Follow the order from `.claude/rules/stack-rules.md`. List numbered steps specific to this task.

## Business rules to enforce

- [inline key rules from spec that affect implementation logic]

## Tests

- [ ] `src/path/file.spec.ts`: [what to test — business logic, edge cases, error paths]

## Key decisions

- [architectural decisions, trade-offs, assumptions made]

## Risks

- [potential issues to watch for]
```

**For cross-stack plans:** Only include files/tasks for the CURRENT stack. The other stack gets its own plan when `/plan` is run in that repo.

### Step 7: Post to Notion

**Always (if ticket provided):**
- Comment on ticket: "📋 Plan created ({stack})\n Branch: {branch}\n Plan: plans/{name}.md"
- Set ticket status to "In Progress"
- If status field name or options differ, report to user instead of guessing

**If cross-stack and current stack defines the API:**
- Post a separate comment with the API contract:
  ```
  📄 API Contract:
  GET /api/users/:id/profile → { name: string, email: string, avatar: string | null }
  PUT /api/users/:id/profile ← { name: string, avatar: string }
  ```
- This comment becomes the shared reference for other stacks

### Step 8: Handoff

**Single-stack task:**
```
Next: /implement plans/[task-name].md
```

**Cross-stack task (more stacks remaining):**
```
Cross-stack task detected. BE plan created.
After completing BE: /implement → /review → /commit
Then switch to FE repo and run: /plan [same ticket URL]
```

**Cross-stack task (this is the last stack):**
```
FE plan created (API contract from BE).
Next: /implement plans/[task-name].md
```

## Rules

- Keep plans simple and actionable - one file, not a folder structure
- Each checklist item should be a clear, executable task
- Include specific file paths, not vague descriptions
- **Inline critical details from the spec**: field names, types, enums, validation rules. Plan must be implementable without re-reading the full spec
- When no Notion ticket exists, plan must be fully self-contained
- Include schema/model changes with exact field definitions when applicable
- Include key business/permission rules with enough detail to implement
- Follow `.claude/rules/development-rules.md`
- DO NOT implement code - only create the plan file
- DO NOT include code examples or pseudocode. Describe WHAT, not HOW
- Do not create, modify, or scaffold any source files
- Plan files should be committed to git on the feature branch. Delete after merge
- Plan file name: short, descriptive, kebab-case
- **Cross-stack scope**: only plan for the current stack. Other stacks get their own plan
- **API contract**: if current stack defines the API (usually BE), post it to Notion for other stacks
