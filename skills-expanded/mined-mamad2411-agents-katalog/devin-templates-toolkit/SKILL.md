---
name: devin-templates-toolkit
description: Templates for web, TUI, CI/CD, and docs — copy and adapt to each project
argument-hint: "[scope]"
related:
  - devin-scripts-toolkit
  - follow-create-web
  - follow-create-plugins
  - create-cloudflare
  - setup-cicd
  - update-project
  - write-how-to
  - update-docs

---

## Goal

Collect starter templates for creating projects, CI/CD, docs, and TUI apps

## Scope

- Web templates (landing, saas, paas) for `/follow-create-web`
- TUI templates (`/follow-create-tui-ratatui`) in Ratatui style
- CI/CD templates (GitHub Actions) for `/setup-cicd`
- Package setup templates for `/update-project` `### setup-package`
- Documentation templates (`/write-how-to`, `/update-agents-md`, README.md)
- Cloudflare templates for `/create-cloudflare-worker`

## Execute

### 1. Choose Template

> Goal: pick the template matching the project type

1. Detect the project type
2. Choose a template from `templates/<category>/`
3. Copy it into the project directory

### 2. Adapt Template

> Goal: adapt the template to the project

1. Replace placeholders such as `<project-name>`, `<repo-name>`
2. Remove unnecessary parts
3. Use `/devin-scripts-toolkit` to check after copying

### 3. Verify

> Goal: confirm the template works

1. Run `/deep-review-codebase`
2. Run `/report-config-files`
3. Run `/review-devin-global-harness`

## Templates

| Category | Templates |
|----------|-----------|
| `templates/web/` | landing, saas, paas starter templates |
| `templates/tui/` | ratatui app starter |
| `templates/cicd/` | GitHub Actions deploy workflows |
| `templates/docs/` | AGENTS.md, README.md, how-to templates |

## Rules

- Use these templates before creating a project
- Adapt each template to the actual stack
- Do not commit an unadapted template
- Pair with `/devin-scripts-toolkit`
- Use /follow-create-plugins if needed
- Use /update-docs if needed


## Expected Outcome

- Faster project creation
- Less setup time
- Consistent results
