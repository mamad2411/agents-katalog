---
name: git-repo-init
description: >-
  Use when the user says "init repo", "create repo", "make this a git repo",
  "github init", or a new folder needs a GitHub or Origin repository.
---

# Git Repository Initializer

Initialize the current folder as a git repository and create it on GitHub
(via `gh`) or Origin. Ask for owner and visibility; do not assume a fixed org
list.

Private context remotes are out of scope.

## Workflow

### 1. Gather Information

Ask the user for:

**Host:**
- GitHub (`gh`)
- Origin (`origin` CLI), when that is the intended workshop

**Repository owner:**
- A GitHub user or org login, or an Origin namespace
- If the user explicitly names an owner, use it; do not ask again
- Do not hard-code a personal allow-list of orgs

**Repository visibility:**
- Public or private — ask; do not invent a host-specific default without
  confirmation

**Repository name:**
- Default: current folder name
- User can specify a custom name

**Repository purpose:**
- If unclear from context, ask what the repo will be used for
- This informs README.md content

**Primary language:**
- Detect from existing files if possible
- Ask user if ambiguous or no code present

**Author metadata (templates only):**
- Substitute `${AUTHOR_NAME}` and `${AUTHOR_EMAIL}` in paper/README author
  blocks; ask if unset. Never paste a hard-coded personal email or postal
  address into generated files.

### 2. Detect Project Language

Scan current directory for language indicators:

```
.py files → Python
.c/.h files → C
.js/.ts files → JavaScript/TypeScript
.rs files → Rust
.go files → Go
.tex files → LaTeX
Makefile → C/Make project
```

If multiple languages detected or unclear, ask user which is primary.

### 2b. LaTeX Manuscript Projects

If `.tex` files are present:
- Treat the repo as a paper/manuscript repo, not generic code.
- If the target venue is not obvious, ask whether the template should be Phys. Rev. Fluids (`PRF`) or Phys. Rev. Letters (`PRL`).
- Use `references/latex-paper-template.md` to seed `main.tex` and the author/affiliation block with `${AUTHOR_NAME}` / `${AUTHOR_EMAIL}` and a placeholder affiliation the user confirms.
- Add the helper scripts at the repo root: `compile_tex.sh`, `check_citations.sh`, and `paperctl.sh`.
- If a `Makefile` is missing, create one with `all`, `check-citations`, and `clean` targets; if one already exists, leave it alone and let `paperctl.sh` bridge to it.
- Mention both `make` and `./scripts/paperctl.sh` in README.md and AGENTS.md.

### 3. Create Repository Files

**Order of operations:**

1. Create `.gitignore` (use templates from `references/gitignore-templates.md`)
2. Create `README.md` (use template from `references/readme-template.md`)
3. Create `AGENTS.md` (use template from `references/agents-template.md`)
4. Create `CLAUDE.md` (with text: `@AGENTS.md`)
5. For a GitHub repository, create `.coderabbit.yaml` (use templates from
   `references/coderabbit-yaml-templates.md`, selected by the repo type
   detected in step 2/2b). Adapt to the actual repo context: if the repo will
   commit auto-generated output (docs sites, rendered PDFs, search databases),
   exclude that output via `path_filters` and keep the scripts that generate it
   reviewable — review the generators, not the generated. It must be created
   before `git add .` so it ships in the initial commit, and must never appear
   in `.gitignore`. If the `coderabbit` CLI is installed, run `coderabbit config
   validate` after writing. Otherwise validate YAML syntax with an available
   parser or `yamllint` and report explicitly that CodeRabbit schema validation
   did not run. Skip `.coderabbit.yaml` for non-GitHub hosts unless the user
   asks for it.

When adapting the README template, keep the opener specific.
**Bad:** "This repository contains code for the project." **Good:** "CLI that
exports CSV reports from the inventory API — entry point `src/cli.ts`."

### 4. Initialize Git Repository

```bash
# Initialize git repo
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit"
```

### 5. Create Remote Repository

**GitHub:**

```bash
gh repo create <owner>/<repo-name> --source=. --push [--public|--private]
```

**Origin:**

```bash
origin auth status
origin repo create <namespace>/<repo-name> [--visibility public|private]
# then add the remote and push per Origin CLI docs for the session
```

**Flags (GitHub):**
- `--source=.` - Use current directory as source
- `--push` - Push local commits to remote
- `--public` or `--private` - Set visibility

### 6. Confirm Success

Output:
- Repository URL
- Files created (for GitHub repositories, including `.coderabbit.yaml` and
  which template it used)
- Next steps for the user (for GitHub repos, note whether the CodeRabbit App is
  installed on the owner account so PRs get automatic reviews)
- Optional Origin twin for a new GitHub repo, only when the user asks:
  ```bash
  origin auth status
  origin repo create-mirrored <github-owner/name>
  ```
  If mirror creation fails, report the partial state and ask before deleting
  anything.

## Gotchas

1. **Existing `.git` folder kills `git init`** — always check for a pre-existing `.git` directory before running `git init`. Re-initialising a git repo on a folder that already has one can silently reset HEAD and lose the commit graph.
2. **`gh repo create --push` without a default branch set will fail** — make sure the initial commit exists locally (i.e. `git commit` ran successfully) before calling `gh repo create --push`; an empty repo push causes a non-obvious GitHub API error.
3. **Visibility is not guessed** — always confirm public vs private with the user before creating; a private repo accidentally made public exposes draft code.
4. **`CLAUDE.md` must contain only `@AGENTS.md`** — do not put actual content in CLAUDE.md; it is an include pointer. Adding content directly breaks the standard agent-discovery path for sub-agents.
5. **Owner is whatever the user named** — do not silently substitute another account; that changes the repository's security and recovery owner.
6. **In GitHub repositories, `.coderabbit.yaml` is a tracked file, not local config** — never add it to `.gitignore`. Both the GitHub App and the guarded local CLI read it from the repo root, so it only works when committed.

## Error Handling

- Run `gh auth status` (GitHub) or `origin auth status` (Origin) before
  creation. If the authenticated identity cannot create under the explicit
  target owner, stop and report the mismatch; do not fall back to another
  owner.
- If repo name exists: Suggest alternative name or ask user
- If not a clean directory: Warn about existing .git folder
- If repo create fails: show error and suggest fixes

## Decision Tree

```
Start
├── Is there an existing .git folder?
│   ├── Yes → Warn user, ask to proceed or abort
│   └── No → Continue
├── Can detect primary language?
│   ├── Yes → Use for .gitignore
│   └── No → Ask user
├── Is repo purpose clear?
│   ├── Yes → Generate README
│   └── No → Ask user
├── Owner and visibility confirmed?
│   ├── Yes → Continue
│   └── No → Ask user
└── Create repo on named host under named owner
```
