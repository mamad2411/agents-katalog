---
name: agent-workflow-kit
description: Evaluate whether and how to add AI-assisted development workflow rules to a new or existing software project. Use when asked to onboard AI agents into a repo, create or update AGENTS.md, choose a workflow level, decide whether to use a spec layer such as OpenSpec or Spec Kit, decide whether to use agent discipline such as Superpowers, decide whether to add specialist review such as gstack, decide whether to add harness/tooling packs such as ECC, or produce an Agent Workflow Kit decision for maintainers.
---

# Agent Workflow Kit

Evaluate the repository first, then recommend the smallest AI workflow that reduces real project risk. Do not install tools, enable hooks, add MCP servers, or modify project rules until the maintainer approves the proposed integration.

## Core Rule

Use this order:

```text
inspect repo -> score risk -> choose workflow level -> recommend files/rules -> ask approval -> edit if approved
```

Never assume OpenSpec, Spec Kit, Superpowers, gstack, ECC, or any other tool is required. They are examples, not defaults.

## Inspect First

Before recommending changes, inspect available project context:

- `README.md`
- existing AI rules: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `.github/copilot-instructions.md`
- toolchain files: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.
- source structure: `src/`, `app/`, `pages/`, `components/`, `lib/`
- tests and E2E config: `tests/`, `spec/`, `e2e/`, Playwright/Cypress config
- CI/deploy config: `.github/workflows/`, `.gitlab-ci.yml`, `vercel.json`, `Dockerfile`, infrastructure files
- risk surfaces: auth, permissions, tokens, cookies, payments, user data, scraping, publishing, browser automation, production data

If no repository is available, ask for the project context or provide a generic evaluation checklist instead.

## Score Risk

Score each dimension 0-2:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Lifecycle | one-off | occasionally maintained | long-lived product |
| Users | author only | internal users | public users/customers |
| UI/UX | none | simple UI | complex UI/editor/dashboard |
| Release risk | no release | manual release | staging/production/CI release |
| Security/accounts | none | API keys/limited permissions | auth/cookies/tokens/user data/payments |
| External platforms | none | third-party API calls | scraping/publishing/browser automation |
| Testing difficulty | unit tests enough | integration tests needed | E2E/screenshots/accessibility/performance |
| Collaboration | solo short-term | solo long-term | team or multi-agent work |

Workflow level:

- `0-4`: Level 1 minimal workflow, or Level 0 if AI will not edit code.
- `5-9`: Level 2 standard workflow.
- `10+`: Level 3 full workflow.

Overrides:

- Security/accounts or external platforms at `2`: add security/external action rules.
- UI/UX or testing difficulty at `2`: add browser/E2E verification rules.
- Collaboration at `2`: add explicit project-level AI rules.

## Choose Layers

Choose only layers justified by risk.

| Layer | When to add | Examples |
|---|---|---|
| Spec layer | non-trivial behavior/architecture/data/automation changes need durable memory | OpenSpec, Spec Kit, ADR/RFC, GitHub issues, `docs/changes/` |
| Agent discipline | AI writes or edits code | Superpowers, custom AGENTS rules, team checklist |
| Specialist review | product/design/QA/security/release risk exists | gstack, human review checklist, QA/security gates |
| Harness/tooling pack | team needs cross-agent rules/hooks/MCP/memory/language guidance | ECC, custom rules/hooks |

Spec-layer choice:

- Prefer OpenSpec or lightweight `docs/changes/` for general existing projects and small teams.
- Prefer Spec Kit for formal team/enterprise SDD with explicit constitution/spec/plan/tasks phases.
- Prefer ADR/RFC/design docs for architecture decisions.
- Prefer GitHub issues/project docs for small open-source projects.
- Do not use two spec tools as competing sources of truth.

## Output Decision First

Before changing files, output this decision and ask for approval unless the user already authorized edits:

```markdown
## Agent Workflow Kit Decision

Project: <project-name>

### Summary

- Project type: <library / CLI / web app / automation / data pipeline / editor / internal tool / etc.>
- Lifecycle: <one-off / maintained / long-lived>
- Users: <author / internal / public / customers>
- Risk level: <low / medium / high>
- Score: <0-16>

### Decision

- Workflow level: <0 / 1 / 2 / 3>
- Spec layer: <none / light / required>
- Agent discipline: <none / recommended / required>
- Specialist review: <none / light / full>
- Harness/tooling pack: <none / optional / recommended>

### Reasoning

- <reason 1>
- <reason 2>
- <reason 3>

### Proposed Files

- <file to create/update, or "none">

### Verification Commands Found

- Install: `<command or unknown>`
- Test: `<command or unknown>`
- Lint/typecheck: `<command or unknown>`
- Build: `<command or unknown>`
- E2E/browser: `<command or unknown>`
```

## If Approved To Edit

Create or update the smallest useful set of project rules.

Recommended mapping:

- Level 1: base AGENTS block only.
- Level 2: base + spec layer + agent discipline + external action safety.
- Level 3: Level 2 + specialist review; add harness/tooling pack only if the team actually uses one.

Use `references/agents-templates.md` for copy-ready blocks.

When editing existing rules:

- Preserve existing project instructions.
- Add missing workflow rules instead of replacing everything.
- Keep rules short enough for agents to follow.
- Fill in real verification commands when discoverable.
- Leave `<fill in>` only if the command cannot be determined and mention it in the final response.

## Safety Rules

- Treat external/networked actions as approval-required unless explicitly authorized.
- Ask before pushing, opening/merging PRs, deploying, modifying production data, posting, sending messages, changing credentials, running paid jobs, or operating real third-party accounts.
- Do not send private code, customer data, secrets, production logs, database exports, or credentials to untrusted agents, MCP servers, browser automation, or external services.
- For high-risk workflows, produce a local plan or report first.

## Optional References

Load these only when needed:

- `references/agents-templates.md`: copy-ready `AGENTS.md` blocks and full standard example.
- `references/engineering-references.md`: optional engineering guideline catalog and when to reference each item.

