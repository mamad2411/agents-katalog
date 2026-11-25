---
name: project-adaptation
description: Adapt to and collaborate with the project you're working in — detect its tech stack, honor its CLAUDE.md and conventions, and reuse its existing skills and agents before adding anything new. Use at the START of any claude-dream-team task (devops, development, or QA), on existing repos as well as fresh ones. Shared by all three agents.
---

# Project Adaptation

The first move for every claude-dream-team agent. Adapt to the project as it is; never impose a default stack or workflow.

## 1. Detect the stack
Read manifests and lockfiles to learn the truth of the project — don't assume:
- Language/runtime & package manager: `package.json`, `composer.json`, `requirements.txt`/`pyproject.toml`, `go.mod`, `pom.xml`/`build.gradle`, `Gemfile`, `Cargo.toml`.
- Frameworks, test runner, build tooling, and scripts (e.g. `package.json` "scripts").
- Infra/deploy signals: `Dockerfile`, `docker-compose.yml`, `.github/workflows`, `cloudbuild.yaml`, Terraform, `app.yaml`.
- In-code conventions: formatter/linter config, directory layout, naming.

## 2. Honor the project's conventions
- Read `CLAUDE.md` (and `AGENTS.md` / `.cursorrules` if present) and follow it. **On any conflict, the project's instructions win** over this plugin's defaults.
- Match existing patterns, style, and idioms over personal preference.

## 3. Reuse before you add
- Discover the project's own skills (`.claude/skills`, installed plugin skills) and agents (`.claude/agents`) and **prefer them**. Use the project's existing commands and scripts.
- This plugin's skills layer ON TOP of the project's — they fill gaps and add expertise; they do not override the project's own guidance.

## 4. Existing vs fresh repos
- **Existing repo:** adapt to what's there. Extend current patterns; don't rewrite or re-stack without being asked.
- **Fresh repo:** apply the dream-team's opinionated defaults (see each domain skill).

## Team handoffs
claude-dream-team agents collaborate through the main session. When the qa-engineer routes a finding to `[fullstack-developer]` or `[devops-engineer]`, that agent implements the fix within its own boundaries, then QA re-verifies. The routing protocol lives in `qa-testing` → `references/code-review.md`; the `/dream-team-review` command automates the loop.
