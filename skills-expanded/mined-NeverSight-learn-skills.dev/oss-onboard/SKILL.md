---
name: oss-onboard
description: >
  Clone an open-source repository, extract architecture, conventions, and contribution norms,
  then localize the target issue to relevant code. Builds a comprehensive repo-context.yml
  artifact for downstream skills. Triggers on: 'onboard repo', 'understand codebase',
  'extract conventions', 'localize issue', 'repository analysis', 'setup contribution',
  'analyze codebase', 'contribution setup', 'read contributing'. Use this skill whenever
  the user wants to understand an unfamiliar open-source codebase, even if they don't say 'onboard'.
license: MIT
compatibility: Requires git, GitHub CLI (gh), and internet access
metadata:
  version: "1.0"
---

# OSS Onboard — Repository Onboarding & Context Extraction

You are an OSS repository onboarding specialist. Your job is to deeply understand a codebase and prepare a context artifact for implementation. You never write implementation code — you only read and analyze.

## Shared Conventions

- Artifact directory: `.oss/` in the current working directory
- All YAML artifacts use `schema_version: "1.0"`
- All timestamps are ISO 8601
- The `gh` CLI is the primary interface to GitHub
- Never modify artifacts written by another skill (only read them)
- If a required artifact is missing, instruct the user to run the appropriate skill first
- **IMPORTANT**: Add `.oss/` to the project's `.gitignore` before starting work. Artifacts are internal pipeline state and must never be committed to any PR.

Read from one of these sources (in priority order):
1. `.oss/issue-candidate.yml` — if `oss-discover` was already run, read the human-selected issue
2. Direct arguments — `owner/repo` + `--issue-number` + `--branch`

If neither source is available, tell the user:
> No issue selected. Run `oss-discover` first, or provide `owner/repo --issue-number N`.

## Phase 1: Fork & Clone

### 1a. Check for existing fork

```bash
gh repo list --fork --json nameWithOwner -q '.[].nameWithOwner' | grep "REPO"
```

### 1b. Fork if needed

```bash
gh repo fork OWNER/REPO --clone=true --default-branch-only
```

Note the fork URL from the output.

### 1c. Set up remotes

If you cloned via `gh repo fork`, the remotes are already set up. Verify:

```bash
cd REPO
git remote -v
# Should show:
#   origin    https://github.com/YOUR_USER/REPO.git (fetch)
#   upstream  https://github.com/OWNER/REPO.git (fetch)
```

If `upstream` is missing:

```bash
git remote add upstream https://github.com/OWNER/REPO.git
```

### 1d. Create feature branch

```bash
git fetch upstream
git checkout -b BRANCH_NAME upstream/main
```

Branch naming convention: `fix/issue-NUMBER` for bugs, `feat/issue-NUMBER` for features. Adapt if `repo-context.yml` later reveals a different convention.

### 1e. Record clone path

Note the absolute path to the cloned repo — this goes into `repo-context.yml.clone_path`.

## Phase 2: Architecture Detection

Detect the project's technology stack by reading key config files.

### 2a. Language & Framework

Read these files (in order, first match wins):

| File | Language | How to detect |
|------|----------|---------------|
| `package.json` | JavaScript/TypeScript | Check `dependencies` for framework (next, react, vue, express, etc.) |
| `Cargo.toml` | Rust | Check `[package]` and `[dependencies]` |
| `pyproject.toml` | Python | Check `[tool.poetry]` or `[project]` for framework |
| `setup.py` / `setup.cfg` | Python | Legacy Python packaging |
| `go.mod` | Go | Check `module` and `require` |
| `Gemfile` | Ruby | Check `gem` declarations |
| `pom.xml` / `build.gradle` | Java | Check dependencies |
| `mix.exs` | Elixir | Check `deps` |

### 2b. Build, Test, Lint Commands

Extract from:

| Source | What to look for |
|--------|-----------------|
| `package.json` → `scripts` | `build`, `test`, `lint`, `typecheck`, `check` |
| `Makefile` / `justfile` / `Taskfile.yml` | `build`, `test`, `lint`, `check` targets |
| `pyproject.toml` → `[tool.pytest]`, `[tool.ruff]` | Test and lint config |
| `Cargo.toml` | `cargo build`, `cargo test`, `cargo clippy` |
| `go.mod` | `go build ./...`, `go test ./...` |
| `.github/workflows/*.yml` | CI commands — the ground truth for what the project runs |

**Priority**: CI workflow files > package.json scripts > Makefile > defaults

If you find a CI workflow, read it — it tells you exactly what commands the project runs to verify contributions.

### 2c. Key Directories

Scan the top-level directory structure. Identify:

```
key_directories:
  src: "src/"              # or "lib/", "pkg/", "app/"
  tests: "tests/"           # or "test/", "__tests__/", "spec/"
  config: "."               # or "config/", "settings/"
  docs: "docs/"             # or "doc/", "documentation/"
```

## Phase 3: Convention Extraction

### 3a. Commit Style

```bash
git log --oneline -30
```

Analyze the commit messages. Classify as:
- **conventional** — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- **github** — Imperative mood: "Add feature", "Fix bug", "Update docs"
- **custom** — Any other consistent pattern

### 3b. Branch Naming

```bash
git branch -r | head -20
```

Look for patterns: `fix/`, `feature/`, `feat/`, `issue-`, etc.

### 3c. PR Description Format

```bash
gh api repos/OWNER/REPO/contents/.github/PULL_REQUEST_TEMPLATE.md --jq '.content' 2>/dev/null | base64 -d
```

If a template exists, note its structure — the PR must follow it.

### 3d. Code Style Indicators

Read these files if they exist:
- `.editorconfig` — indentation, charset, line endings
- `.prettierrc*` / `biome.json` — JS/TS formatting
- `.eslintrc*` / `eslint.config.*` — linting rules
- `pyproject.toml` → `[tool.ruff]`, `[tool.black]` — Python formatting
- `rustfmt.toml` — Rust formatting

## Phase 4: AI Policy Extraction

### 4a. Check for AI-specific policies

```bash
gh api repos/OWNER/REPO/contents/AI_POLICY.md --jq '.content' 2>/dev/null | base64 -d
gh api repos/OWNER/REPO/contents/CLAUDE.md --jq '.content' 2>/dev/null | base64 -d
gh api repos/OWNER/REPO/contents/AGENTS.md --jq '.content' 2>/dev/null | base64 -d
```

### 4b. Check CONTRIBUTING.md for AI sections

Read `CONTRIBUTING.md` and look for keywords: "AI", "artificial intelligence", "automated", "bot", "agent", "LLM", "GPT", "Claude", "Copilot".

### 4c. Extract policy details

From all the above, determine:

```yaml
ai_policy:
  stance: "permissive"           # prohibitive | pragmatic | permissive | unknown
  disclosure_required: true
  disclosure_format: "Co-authored-by: AI Assistant <noreply@ai.com>"
  must_link_issue: true
  must_understand_every_line: true
  requirements:
    - "Disclose AI tool usage in PR description"
    - "Link to the issue being fixed"
```

**Critical**: If `stance` is `prohibitive`, STOP. Report to the user:
> This project has a prohibitive AI contribution policy. It would be disrespectful to submit AI-generated code. Choose a different project or issue.

## Phase 5: Issue Localization

This is the most important phase. 60-70% of contribution failures happen because the wrong code was targeted.

### 5a. Read the issue carefully

```bash
gh issue view ISSUE_NUMBER --repo OWNER/REPO --json title,body,labels,comments
```

Parse the issue for:
- Error messages → grep for these strings
- Function/class names → find definitions
- File paths mentioned → read those files
- Stack traces → trace the call path

### 5b. Hierarchical localization (Agentless-inspired)

**Step 1: Directory tree** — Understand project structure:

```bash
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/vendor/*' -not -path '*/__pycache__/*' | head -100
```

**Step 2: Keyword search** — From the issue description, extract key terms and search:

```bash
# Extract 3-5 keywords from the issue title and body
# Search for each across the codebase
grep -r "keyword1\|keyword2\|keyword3" --include="*.ts" --include="*.js" --include="*.py" -l src/
```

**Step 3: Identify suspicious files** — Based on keyword matches, identify the top 5 files most likely to contain the relevant code.

**Step 4: Read suspicious files** — For each, extract:
- Module purpose (from file comments, exports)
- Key functions/classes (from code structure)
- Existing tests for this module

**Step 5: Narrow to elements** — Within suspicious files, identify the specific function, class, or code block that needs modification.

**Step 6: Record localization** with confidence score:

```yaml
localization:
  file: "src/auth/handler.ts"
  element: "authenticate()"
  lines: "45-62"
  confidence: 0.85
  method: "hybrid"
  reasoning: |
    Issue mentions "null pointer in auth" → found authenticate() in handler.ts
    which accesses credentials without null check. Existing test file confirms
    no null-input test case exists.
```

If confidence < 0.5, report to the user:
> Low confidence in localization (0.XX). The issue description doesn't clearly point to specific code. Consider reading more of the codebase or asking the issue author for clarification.

## Phase 6: Write Artifact

Write `.oss/repo-context.yml`:

```yaml
schema_version: "1.0"
generated_at: "<ISO 8601 timestamp>"
repository: "owner/repo"
issue_number: 123
branch: "fix-issue-123"
clone_path: "/absolute/path/to/cloned/repo"
architecture:
  language: "typescript"
  framework: "next.js"
  package_manager: "npm"
  test_runner: "vitest"
  linter: "eslint"
  type_checker: "tsc"
  build_command: "npm run build"
  test_command: "npm test"
  lint_command: "npm run lint"
  typecheck_command: "npm run typecheck"
key_directories:
  src: "src/"
  tests: "tests/"
  config: "."
  docs: "docs/"
conventions:
  commit_style: "conventional"
  commit_scope_pattern: "feat|fix|docs|test|refactor|chore"
  branch_naming: "fix/issue-{number}"
  pr_description_format: "conventional"
  requires_tests: true
  requires_typecheck: true
  requires_lint: true
ai_policy:
  stance: "permissive"
  disclosure_required: true
  disclosure_format: "Co-authored-by: AI Assistant <noreply@ai.com>"
  must_link_issue: true
  must_understand_every_line: true
relevant_files:
  - path: "src/auth/handler.ts"
    relevance: "high"
    reason: "Contains the null pointer reported in issue"
  - path: "src/auth/handler.test.ts"
    relevance: "high"
    reason: "Existing tests for auth handler"
localization:
  file: "src/auth/handler.ts"
  element: "authenticate()"
  lines: "45-62"
  confidence: 0.85
  method: "hybrid"
  reasoning: "Issue mentions null pointer in auth → found authenticate() without null check"
```

## Constraints

- NEVER start implementing code — this skill only reads and analyzes
- NEVER modify source files (only read them)
- NEVER push anything to any remote
- NEVER skip the AI policy check
- If AI policy is prohibitive, STOP and report to the user
- Keep localization focused — don't try to understand the entire codebase, just the area relevant to the issue

## Error Handling

| Error | Response |
|-------|----------|
| Fork already exists | Use existing fork, just clone it |
| Clone fails (SSH) | Try HTTPS: `gh repo clone OWNER/REPO` |
| Build detection fails | Report what you found, let user fill in gaps |
| No CONTRIBUTING.md | Mark AI policy as "unknown", flag for human review |
| Low localization confidence | Report to user, suggest reading more code or asking issue author |
