---
name: tpl-situacao-setup-inicial-projeto
description: Template do pack (situacao/07-setup-inicial-projeto.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/07-setup-inicial-projeto.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: New Project Setup from Scratch

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/07-setup-inicial-projeto.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when initializing a new software project — before writing any business logic. The first days of a project set patterns that persist for years. Skipping linting, testing infrastructure, or CI setup "to move faster" guarantees slower development within weeks. This session is about building the foundation correctly.

## OBJECTIVES
- Set up all scaffolding before writing a single line of business code
- Establish conventions that the whole team (or future self) will follow
- Make it impossible to accidentally break things (automated checks)
- Create a "Definition of Done" for project setup that leaves nothing to chance

## APPROACH RULES

1. **Infrastructure before features.** CI pipeline, linting, testing setup, and environment variables must be in place before any business code is committed. If CI is added later, it will keep failing until someone fixes it.

2. **Automate code style — never debate it.** Choose a formatter (Prettier, Black, gofmt). Configure it. Add a pre-commit hook. The team should never spend a PR comment on formatting.

3. **12-factor app from day one.** No hardcoded configuration. Everything configurable goes in environment variables. `.env.example` contains keys without values. `.env` is gitignored forever.

4. **Git conventions from the first commit.** Choose a commit message convention (Conventional Commits recommended) and enforce it with a commit-msg hook. The first commit is a great first test of the convention.

5. **Test infrastructure must run before business tests can be written.** `npm test` / `pytest` / `go test` should run and report "0 tests, 0 failures" before you've written business tests. Blank slate, no errors.

6. **Dependency management is day-one work.** Lock files committed, exact versions pinned (not `^`), Renovate/Dependabot configured for automated updates.

7. **The README is the contract.** A new developer should be able to read the README and have a running local environment within 30 minutes. Any step that takes longer needs documentation or automation.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| Missing `.gitignore` | Add it before any other commit. Use gitignore.io for the stack. Include: `.env`, `node_modules/`, `dist/`, `*.log`, IDE files |
| Environment config in code | Extract to `.env`. Create `.env.example` with all keys and empty values. Document each key in a comment |
| No linter configured | Add ESLint/Biome (JS/TS), Pylint/Ruff (Python), golangci-lint (Go). Run on CI. Fail build on errors. |
| No formatter configured | Add Prettier (JS/TS), Black/Ruff (Python), gofmt (Go). Add pre-commit hook. Add CI check. |
| No test runner configured | Initialize: `jest --init` / `pytest --co` / `go test ./...`. Confirm it runs with zero tests. |
| No CI pipeline | Create `.github/workflows/ci.yml` with at minimum: lint, type-check, test on push to main and on PRs |
| No pre-commit hooks | Use Husky + lint-staged (Node) or pre-commit framework (Python). Block: bad commits, failing tests |
| Secrets committed accidentally | git-filter-repo or BFG to purge. Rotate ALL secrets that touched git. Add to pre-commit hook. |
| Missing CONTRIBUTING.md | Create it with: how to set up dev environment, branch naming, commit message format, PR process |
| No logging setup | Initialize structured logger (winston, pino, structlog) from day one. Never use console.log in production. |

## Project Setup Checklist

### Version Control
- [ ] Repository created with default branch named `main`
- [ ] Branch protection rules: require PR, require CI, no force push on main
- [ ] `.gitignore` configured for the stack
- [ ] First commit: only infrastructure (no business code)
- [ ] Commit message convention documented (Conventional Commits recommended)

### Code Quality
- [ ] Linter installed and configured (zero warnings on empty project)
- [ ] Formatter installed, configured, and enforced via pre-commit hook
- [ ] TypeScript strict mode enabled (if TypeScript project)
- [ ] Pre-commit hooks installed: runs linter + formatter on staged files

### Testing
- [ ] Test runner installed and runs cleanly with 0 tests
- [ ] Test directory structure created: `tests/unit/`, `tests/integration/`, `tests/e2e/`
- [ ] Coverage tool configured with minimum threshold (e.g., 80%)
- [ ] First test written: a trivial test that just imports main entry point

### Configuration & Secrets
- [ ] `.env.example` created with all keys defined, no values
- [ ] `.env` in `.gitignore` (verify with `git check-ignore .env`)
- [ ] Secret scanning pre-commit hook installed (`detect-secrets` or `gitleaks`)
- [ ] All third-party service API keys loaded from environment

### CI/CD
- [ ] CI pipeline runs on: push to main, any PR
- [ ] CI checks: lint, type-check, tests, build
- [ ] Build artifact produced and versioned
- [ ] Failed CI blocks PR merge (branch protection rule)

### Dependencies
- [ ] Lock file committed (`package-lock.json`, `Pipfile.lock`, `go.sum`)
- [ ] Renovate or Dependabot configured for automatic dependency updates
- [ ] `npm audit` / `pip audit` runs cleanly with zero high-severity issues

### Documentation
- [ ] README.md with: project description, prerequisites, getting started steps
- [ ] CONTRIBUTING.md with: local setup, branch naming, PR process
- [ ] Architecture diagram or description (even if basic)
- [ ] `docs/adr/` directory created for Architecture Decision Records

## DO NOT

- **DO NOT** write business code before linting and testing pass on CI
- **DO NOT** commit a `.env` file with real values — rotate any secrets that touch git
- **DO NOT** use `^` version ranges in package.json for direct dependencies — pin exact versions
- **DO NOT** skip the README — writing it forces you to validate your own setup instructions
- **DO NOT** configure CI "later" — it will never happen, and fixing it will be painful
- **DO NOT** skip pre-commit hooks "to save time" — the time cost is much higher after bad commits accumulate

## OUTPUT FORMAT

At the end of project setup, produce a **Project Setup Summary**:

```markdown
## Project Setup Complete

### Stack
- Runtime: Node.js 20 / TypeScript 5.3
- Framework: Fastify 4
- Database: PostgreSQL 15 + Prisma ORM
- Testing: Vitest + Supertest
- Linting: ESLint + Prettier
- CI: GitHub Actions

### How to Start
1. cp .env.example .env && fill in values
2. npm install
3. npm run db:migrate
4. npm run dev → http://localhost:3000

### Conventions
- Branches: feat/, fix/, chore/, docs/
- Commits: Conventional Commits (enforced by commitlint)
- PRs: require 1 approval + all CI checks green

### What's NOT set up yet
- [ ] Staging environment
- [ ] Production deployment pipeline
- [ ] Error monitoring (Sentry)
```

## QUALITY GATES

- [ ] `npm install && npm run lint && npm test && npm run build` succeeds on a fresh clone
- [ ] `git check-ignore .env` returns `.env` (confirms it's gitignored)
- [ ] CI pipeline visible in repository and shows green on initial commit
- [ ] A second developer followed the README and got the app running without asking questions
- [ ] Zero high-severity dependency vulnerabilities (`npm audit --audit-level=high`)
- [ ] Pre-commit hook triggers on `git commit` with staged files
- [ ] README answers: what, prerequisites, how to run, how to contribute
