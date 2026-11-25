---
name: follow-dot-github
description: Manage the .github directory fully — workflows, templates, policies, and automation config
argument-hint: "[scope]"
related:
  - follow-tool-github-actions
  - deep-analyze
  - check-monorepo
  - create-github-issue
  - update-references
  - report

---

## Goal

Manage the `.github` directory completely and systematically — covering CI/CD workflows, issue/PR templates, community files, automation config, and security policies

## Scope

Used to create, improve, and audit the entire `.github` directory, including invoking `/follow-tool-github-actions` to select and write workflows

### Standard Project

```
.github/
├── workflows/           # CI/CD workflows (YAML)
├── ISSUE_TEMPLATE/       # Issue templates
│   ├── bug_report.yml
│   ├── feature_request.yml
│   └── config.yml
├── PULL_REQUEST_TEMPLATE.md
├── CODEOWNERS
├── dependabot.yml
├── FUNDING.yml           # optional
├── SECURITY.md
├── CODE_OF_CONDUCT.md    # optional
└── CONTRIBUTING.md       # optional
```

### Monorepo

```
.github/
├── workflows/
├── ISSUE_TEMPLATE/
├── PULL_REQUEST_TEMPLATE.md
├── CODEOWNERS
├── dependabot.yml
├── SECURITY.md
└── CONTRIBUTING.md
```

## Execute

### 1. Analyze Existing .github

> Goal: read and analyze the existing `.github` directory to understand the current state

1. Read the whole `.github/` directory
2. Inventory existing files and missing files
3. Read existing files to verify correctness
4. If there is no `.github/` directory → start from scratch
5. If a file cannot be read → stop and report

### 2. Analyze Project

> Goal: analyze the project to determine which files are needed

1. Run `/deep-analyze` to see the tech stack and structure
2. Run `/check-monorepo` to determine the project type
3. Identify whether it is open source, private, or an organization repo
4. Identify whether there are multiple contributors
5. If the project type is unclear → stop and report

### 3. Setup CI/CD Workflows

> Goal: manage CI/CD workflows by delegating to the specialized workflow

1. Run `/follow-tool-github-actions` to select and write workflow YAML
2. Verify workflows use the latest action versions
3. Check `permissions` and `concurrency` settings
4. If the existing workflows are already correct and complete → skip this step

### 4. Setup Issue Templates

> Goal: create issue templates for bug reports, feature requests, plans, tests, questions, and agent tasks

1. Run `/create-github-issue` (per `create-github-issue/references/issue-forms.md`) to create or update `.github/ISSUE_TEMPLATE/`
2. Verify `bug_report.yml`, `feature_request.yml`, `plan.yml`, `test.yml`, `questions.yml`, `agents_task.yml` exist
3. Check `config.yml` with `blank_issues_enabled` and contact links
4. If `/create-github-issue` is unavailable → author the templates manually per `create-github-issue/templates/forms/index.md`

### 5. Setup PR Template

> Goal: create a pull request template to guide contributors

1. Create `.github/PULL_REQUEST_TEMPLATE.md`
2. Include sections: Summary, Changes, Type, Testing, Checklist
3. Fill the checklist from project conventions (tests, docs, lint)
4. If monorepo → note the affected workspace
5. If a correct PR template already exists → update only the missing parts

### 6. Setup CODEOWNERS

> Goal: create CODEOWNERS assigning code owners by directory structure

1. Create `.github/CODEOWNERS`
2. Assign owners by the project's directory structure
3. For monorepos → assign owners per workspace (e.g. `apps/website/ @owner1`)
4. Set a default owner for the root directory
5. If a solo project → skip this step

### 7. Setup Dependabot

> Goal: create `dependabot.yml` for automated dependency updates

1. Create `.github/dependabot.yml`
2. Set `package-ecosystem` per package manager used (npm, github-actions, etc.)
3. Set `directory` per project structure (`/` for root, each workspace for monorepos)
4. Set `schedule.interval` to `weekly` or `daily`
5. Set `open-pull-requests-limit` as appropriate
6. For monorepos → add an entry per workspace plus the `github-actions` ecosystem
7. Set the `commit-message` prefix per conventional commits
8. If a correct dependabot.yml already exists → add only the missing entries

### 8. Setup Community Files

> Goal: create community files by project type

1. Create `.github/SECURITY.md` with the vulnerability reporting method and response timeline
2. Create `.github/CONTRIBUTING.md` if open source or with multiple contributors
3. Create `.github/CODE_OF_CONDUCT.md` if open source (use the Contributor Covenant)
4. Create `.github/FUNDING.yml` if accepting funding (GitHub Sponsors, Open Collective, etc.)
5. If a private repo with no contributors → skip CONTRIBUTING.md, CODE_OF_CONDUCT.md, FUNDING.yml

### 9. Validate And Update References

> Goal: verify correctness and update references

1. Validate YAML syntax of every `.yml`/`.yaml` file
2. Validate Markdown syntax of every `.md` file
3. Validate CODEOWNERS format per the GitHub spec
4. Validate dependabot.yml format per the GitHub spec
5. Run `/update-references` if there were file operations or moves
6. Update `AGENTS.md` if new files were added that the project must know about
7. If validation fails → fix and re-validate (max 3 rounds → stop/report)

## Rules

### 1. No Overlap With Specialized Workflows

- Use `/follow-tool-github-actions` to select and write CI/CD workflows
- `follow-dot-github` manages the other files in `.github/` and coordinates calls to specialized workflows

### 2. File Format Standards

- Issue templates: use GitHub Forms syntax (YAML), not Markdown
- PR template: use Markdown
- CODEOWNERS: use the GitHub CODEOWNERS format (`path @owner`)
- dependabot.yml: use the GitHub Dependabot v2 format
- SECURITY.md: state the response timeline and contact method

### 3. Monorepo Guidelines

- dependabot.yml must have an entry for every workspace and the `github-actions` ecosystem
- CODEOWNERS must assign owners per workspace
- The PR template must note the affected workspace
- ISSUE_TEMPLATE is shared at the root `.github/`

### 4. Security First

- SECURITY.md must contain at least: reporting method, response timeline, scope
- Never list unfixed vulnerabilities in public files
- dependabot.yml must set a `commit-message` prefix per conventional commits
- Never hardcode secrets, tokens, or credentials in any file under `.github/`

### 5. Deterministic And Measurable

- Output must be deterministic — same project type → same files every time
- Validation criteria must be measurable: YAML syntax passes, CODEOWNERS format correct, dependabot.yml matches spec
- If an existing file is already correct → do not recreate it, update only the missing parts
- File creation order must be fixed per the step order

### 6. High Impact Content

- Keep only files the project actually uses — no contributors means no CONTRIBUTING.md
- A private repo does not need CODE_OF_CONDUCT.md or FUNDING.yml
- A solo project does not need CODEOWNERS
- Verify every file contains content actually relevant to the project, not generic boilerplate

## Expected Outcome

- `.github/` has exactly the files the project type needs — none missing, none extra
- CI/CD workflows complete (delegated to `/follow-tool-github-actions`)
- Issue templates use GitHub Forms syntax (YAML) with the full form set
- PR template has all sections: Summary, Changes, Type, Testing, Checklist
- CODEOWNERS assigns reviewers per directory (when contributors exist)
- Dependabot covers every workspace and the `github-actions` ecosystem
- SECURITY.md clearly states reporting method, response timeline, and scope
- Every file passes validation: YAML syntax, Markdown syntax, CODEOWNERS format, dependabot.yml format
- `AGENTS.md` updated if new files were added
