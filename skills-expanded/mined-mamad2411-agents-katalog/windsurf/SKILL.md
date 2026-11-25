---
name: windsurf
description: "Customize and operationalize Windsurf / Cascade. TRIGGER when: user mentions Windsurf, Cascade, `.windsurf/`, Windsurf Rules, Memories, Workflows, Skills, AGENTS.md in Windsurf, Cascade modes, Windsurf MCP, or wants to adapt repo instructions for Windsurf. Also use when creating shared repo customizations that should work well in Windsurf. SKIP: generic coding with no Windsurf/Cascade customization angle, or provider/API work that belongs to OpenAI, Anthropic, Gemini, or GitHub Copilot instead."
---

# Working with Windsurf and Cascade

Use this skill when the task is about making **Windsurf / Cascade** behave better, not just writing ordinary code.

The main Windsurf control surfaces are:

- **Modes** for how Cascade should work right now
- **Rules** for persistent behavioral constraints
- **AGENTS.md** for directory-scoped repo guidance
- **Skills** for specialized multi-step tasks
- **Workflows** for manual slash-command runbooks
- **MCP** for external tools and data

Choose the smallest one that fits.

## Hard Rules

- Do not stuff everything into one giant rule file.
- If the need is directory-scoped, prefer `AGENTS.md`.
- If the need is reusable and multi-step, prefer a skill.
- If the need should run only when explicitly invoked, prefer a workflow.
- If the need is an external tool or integration, prefer MCP.
- Keep repo-shared behavior in **workspace files committed to the repo** whenever the team should inherit it.
- When exact Windsurf UI or config behavior matters, verify against the official Windsurf docs rather than guessing.

## First Decide: What Kind of Customization Is This?

### 1. Mode Choice

Use this when the user is asking how Cascade should approach a task right now:

- **Code mode** for autonomous implementation and file changes
- **Plan mode** for planning before implementation
- **Ask mode** for read-only learning or investigation

If the user wants a detailed implementation plan before edits, point them toward **Plan mode**. If they want immediate autonomous edits, use **Code mode**.

### 2. Rules

Use a Rule when the user wants persistent behavioral guidance such as:

- preferred package manager
- testing expectations
- coding conventions
- architectural guardrails
- safety constraints

Rules are best for cross-cutting constraints that should influence many tasks.

### 3. `AGENTS.md`

Use `AGENTS.md` for **location-based instructions**:

- frontend conventions in `frontend/AGENTS.md`
- backend conventions in `backend/AGENTS.md`
- docs-specific standards in `docs/AGENTS.md`

Root `AGENTS.md` applies broadly; nested files apply when Cascade works in that subtree.

### 4. Skills

Use a skill when the task needs:

- a workflow
- supporting files
- scripts
- templates
- checklists
- reference docs

Skills are best for repeated high-value tasks that Cascade should invoke when relevant.

### 5. Workflows

Use a workflow when the user wants a **manual slash command** for a repeatable runbook:

- `/deploy-staging`
- `/review-pr-comments`
- `/run-tests-and-fix`

Workflows are not automatically invoked. If the user wants automatic matching, use a skill instead.

### 6. MCP

Use MCP when Cascade needs external capabilities:

- GitHub
- issue trackers
- databases
- documentation servers
- internal services

## Windsurf File Locations

Use official Windsurf locations unless the user explicitly wants cross-agent portability first.

### Rules

- Workspace: `.windsurf/rules/*.md`
- Global: `~/.codeium/windsurf/memories/global_rules.md`
- Enterprise/system: OS-specific system directories

Rule activation modes include:

- `always_on`
- `glob`
- `model_decision`
- `manual`

Use:

- `always_on` for core repo constraints
- `glob` for path-specific behavior
- `model_decision` when the rule is relevant but not universal
- `manual` when the user should opt in explicitly

### Workflows

- Workspace: `.windsurf/workflows/*.md`
- Global: `~/.codeium/windsurf/global_workflows/*.md`

### Skills

- Workspace: `.windsurf/skills/<skill-name>/SKILL.md`
- Global: `~/.codeium/windsurf/skills/<skill-name>/SKILL.md`

Windsurf also supports cross-agent compatible skill locations such as:

- `.agents/skills/`
- `~/.agents/skills/`

If the user wants one skill that works across multiple agents, prefer `.agents/skills`.

### `AGENTS.md`

Place `AGENTS.md` directly in the directory whose scope it should control.

Examples:

- `AGENTS.md` at repo root -> whole repo
- `frontend/AGENTS.md` -> `frontend/**`
- `backend/payments/AGENTS.md` -> `backend/payments/**`

## Choosing Between Rules, AGENTS.md, Skills, and Workflows

Use this decision ladder:

### Short persistent constraint

Use a **Rule**.

Example:

- "Always use `bun`, never `npm`."

### Directory-specific conventions

Use **`AGENTS.md`**.

Example:

- "All files in `app/components` must be React server components unless annotated otherwise."

### Complex reusable procedure that should auto-trigger

Use a **Skill**.

Example:

- "Review a PR, run targeted tests, summarize risks, and update a changelog."

### Complex reusable procedure that should only run on command

Use a **Workflow**.

Example:

- "`/deploy-preview` should build, run checks, deploy, and post the preview URL."

### External tools or data

Use **MCP**.

Example:

- "Let Cascade query GitHub issues and Linear tickets."

## Best Practices for Rules

- Keep each rule narrow and explicit.
- Use multiple small rules instead of one omnibus file.
- Prefer examples and concrete commands over vague guidance.
- Avoid duplicating `AGENTS.md` content in Rules.
- Do not put volatile information in a long-lived rule.

## Best Practices for `AGENTS.md`

- Focus on the directory's purpose.
- Put build/test commands near the code they govern.
- Avoid repeating global guidance in every nested file.
- Use nested `AGENTS.md` only when conventions materially differ.
- Prefer operationally useful instructions:
  - where tests live
  - which commands to run
  - naming conventions
  - architectural boundaries

## Best Practices for Skills

- Keep frontmatter trigger text sharp and specific.
- Put supporting scripts/templates next to `SKILL.md`.
- Reference those files explicitly from the skill.
- Use progressive disclosure: keep essential decision logic in `SKILL.md`, move details into helper files if needed.
- Make the skill useful without requiring hidden project knowledge.

## Best Practices for Workflows

- Write them as deterministic step sequences.
- Use imperative phrasing.
- Assume manual invocation via `/workflow-name`.
- Avoid burying permanent repo conventions in a workflow.
- Prefer workflows for:
  - deploys
  - release checklists
  - PR comment triage
  - local environment setup

## MCP Guidance

Use MCP when the agent needs real capabilities, not just instructions.

Good MCP use cases:

- docs lookup
- GitHub or GitLab actions
- browser automation
- database introspection
- internal service tooling

Bad MCP use cases:

- replacing a simple style guide
- encoding project conventions
- serving content that belongs in a checked-in markdown file

## Reference Files

Read only what matches the task:

- `references/control-surfaces.md` -> decide between Modes, Rules, `AGENTS.md`, Skills, Workflows, and MCP
- `references/file-locations.md` -> exact Windsurf file placement
- `references/repo-patterns.md` -> practical layering patterns for a real repo

## Reading Guide

Only read what matches the task:

### User wants better ongoing project behavior

Read Windsurf docs for:

- Rules / Memories
- `AGENTS.md`
- Skills
- `references/control-surfaces.md`
- `references/repo-patterns.md`

### User wants a manual slash-command procedure

Read:

- Workflows
- `references/control-surfaces.md`

### User wants external tool integration

Read:

- MCP
- `references/control-surfaces.md`

### User wants to know how Cascade should work right now

Read:

- Modes
- `references/control-surfaces.md`

## Implementation Heuristics

- If the request is team-shared behavior, commit workspace files under `.windsurf/` or `AGENTS.md`.
- If the request is multi-agent compatible, prefer `.agents/skills` over Windsurf-only skill locations.
- If a rule is becoming long and procedural, refactor it into a skill or workflow.
- If a nested folder keeps violating conventions, add a local `AGENTS.md` instead of bloating the root file.

## Anti-Patterns

Do not:

- use a workflow for a behavior that should always be present
- use a skill for a one-line coding convention
- put repo architecture guidance only in global user config
- duplicate the same instructions across Rules, `AGENTS.md`, and a skill unless there is a deliberate layering reason
- assume Ask mode can safely perform edits

## Final Checklist

Before you finish:

- Did you choose the right Windsurf surface?
- Did you keep shared behavior in repo files when appropriate?
- Did you avoid mixing rules, workflows, and skills unnecessarily?
- Did you use `AGENTS.md` for directory scope rather than global files?
- Did you keep the configuration explicit and maintainable?
