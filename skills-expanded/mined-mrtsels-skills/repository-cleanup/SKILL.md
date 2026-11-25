---
name: repository-cleanup
description: "Systematically audit and clean up junk files from a git repository — MySQL data dirs, build artifacts, runtime uploads, prototype code, IDE configs, and anything else that doesn't belong in version control."
---

# Repository Cleanup

Systematic pattern for entering a messy git repo, identifying what's junk, removing it from tracking and disk, and hardening `.gitignore` to prevent recurrence.

## When to use

- Entering an existing project that has accumulated garbage in git
- Before handing off a repo to someone else
- After discovering large binary/runtime files in git status or commit history
- When `.git/` directory size is suspiciously large compared to source

## Workflow

### 0. Pre-check: verify file isn't referenced before deleting

Before deleting any script, config, or doc file, **check if any active workflow references it**:

```bash
# Search across scripts, configs, and docs
grep -rn "TARGET_FILE" --include="*.{sh,yml,yaml,md,ps1,conf,py,txt}" . | grep -v ".git/"

# Also check active automation
grep -rn "TARGET_FILE" install.sh enterprise doctor.sh start.sh deploy.sh verify.sh docker-compose.yml 2>/dev/null
```

**Only delete if zero active references.** If referenced, trace the dependency chain (is the caller still used? is it a dead script calling another dead script?). Don't assume self-referencing comments count as real references.

File types to check before deleting:
- Scripts (`.sh`, `.ps1`) — may be called by CI, cron, or other scripts
- Configs (`.yml`, `.yaml`, `.conf`) — may be loaded by Docker Compose, Nginx, or Spring Boot
- Docs (`.md`) — may be linked from README or other docs
- Python/JS files — may be imported or loaded at runtime

### 1. Scan for junk signals

```bash
# Large files (>500KB)
find . -not -path './.git/*' -type f -size +500k -exec ls -lh {} \; | sort -k5 -rh | head -30

# Untracked files
git status --porcelain

# Build/compile artifacts
find . -not -path './.git/*' \( -name 'target' -o -name 'build' -o -name 'dist' -o -name '*.class' -o -name '*.jar' \) -type f

# DS_Store / Thumbs.db / logs / cache
find . -not -path './.git/*' -name '.DS_Store'
find . -not -path './.git/*'  \( -name '*.log' -o -name '*.tmp' -o -name '*.cache' -o -name 'npm-debug*' -o -name 'Thumbs.db' \)

# Hidden dirs in project root
find . -maxdepth 1 -not -path './.git' -name '.*'

# Node / Python / Maven artifact dirs
find . -not -path './.git/*' -type d \( -name 'node_modules' -o -name '__pycache__' -o -name '.venv' -o -name 'venv' \)

# Runtime data (uploads, DB files, logs)
find . -not -path './.git/*' -type d \( -name 'uploads' -o -name 'logs' -o -name 'tmp' -o -name 'data' \)
```

### 2. Check .gitignore coverage

```bash
cat .gitignore
```

Common missing patterns:
```
# Runtime / build
.mysql84/
uploads/
logs/
frontend/
.vscode/
**.class
**/target/
node_modules/
__pycache__/
.env
```

### 3. Classify what you find

| Category | Treatment | Example |
|----------|-----------|---------|
| **Runtime data** (MySQL data, uploads, logs) | `--cached` — keep on disk, stop tracking | `.mysql84/`, `uploads/` |
| **Sensitive / PII / submission material** (AI-use acknowledgements with name+ID, admin docs, deliverable PDFs duplicate of tracked sources) | `--cached` + gitignore — keep on disk, **never delete** | `docs/ai-acknowledgement.*`, `docs/reports/` |
| **Prototype/obsolete code** | `git rm` — remove from disk AND tracking | `frontend/`, old mock files |
| **Personal IDE config** | `git rm` — remove from disk AND tracking | `.vscode/`, `.idea/`, `.settings/` |
| **Build artifacts** | Already ignored by `**/target/` etc. Check git-ls-files | `target/`, `build/` |
| **OS junk** | Add to `.gitignore`, then `git rm --cached` to clean up | `.DS_Store`, `Thumbs.db` |

### 4. Update .gitignore first

Always update `.gitignore` BEFORE running `git rm` so the files are protected from accidental re-addition later.

```bash
# Add patterns
echo ".mysql84/" >> .gitignore
echo "uploads/" >> .gitignore
```

### 5. Remove from tracking

```bash
# Runtime data (keep on disk)
git rm --cached -r .mysql84/

# Source files / prototype code (delete from disk too)
git rm -r frontend/

# IDE config
git rm .vscode/settings.json

# OS junk already tracked
git rm --cached '*.DS_Store'
```

### 6. Physically clean disk if needed

`--cached` leaves files on disk. Delete them too if they're truly disposable:

```bash
rm -rf .mysql84/ frontend/ uploads/ .vscode/
```

### 7. Commit

```bash
git add .gitignore
git commit -m "chore: 清理仓库垃圾文件

- 移除 .mysql84/ (MySQL 数据目录)
- 移除 uploads/ (运行时上传文件)
- 移除 frontend/ (已弃用原型)
..."
```

### 8. Verify

```bash
git status
du -sh .git/      # Note: history still contains these files
```

> **Note:** `git rm --cached` + commit only stops tracking files going forward. The `.git/` directory size may not shrink because the objects still live in commit history. To truly remove them from history, see the options below.

### 9. Clean-Remote Push (Orphan Branch Rebuild)

When the remote is **empty** (or you're creating a new remote for a repo with bloated history), rebuild history from scratch instead of pushing the mess:

```bash
# 1. Create orphan branch — no shared history
git checkout --orphan clean-main

# 2. Unstage everything, then stage only what you want
git rm -rf --cached .
git add <desired-files-and-dirs>

# 3. First commit: text files only
git commit -m "Initial commit: text source files"

# 4. Push first batch
git push --set-upstream origin clean-main:main

# 5. Add binaries in a separate commit
git add <binary-assets>
git commit -m "Add binary assets: workbooks, slides, archives"
git push origin HEAD:main

# 6. Rename local branch to match remote
git branch -D main
git branch -m clean-main main
```

**Why this works:** The orphan branch has zero parent commits — the bloated history is discarded entirely. No `filter-repo` rewrite needed. The remote never sees the large files.

**Best for:** Repos where the remote exists but is empty, or where you're creating a fresh remote with consent to force-push.

**Batch strategy for scalpel push** — push large repos in graduated batches:

| Batch | What to include | Typical size |
|-------|----------------|--------------|
| 1 | `.md`, `.py`, `.ipynb`, `.csv`, config files | <1MB |
| 2 | `.pdf`, `.xlsx`, `.zip`, `.key`, slides | <10MB |
| 3 | Data files, checkpoints, models | as needed |

Push each batch as a separate `git commit && git push` cycle. This way if the connection drops on a large binary, only that batch is lost, not the entire push.

See `github` skill → `references/bloated-history-recovery.md` for advanced history-rewrite techniques (git-filter-repo, BFG).

### 3a. Cache vs Content Triage

When untracked items include a mix of generated/transient files and real content, classify each:

| Category | Treatment | .gitignore | Examples |
|----------|-----------|------------|----------|
| **IDE/agent cache** | Delete + gitignore | Yes | `.serena/`, `.cursor/`, `.claude/`, `.vscode/` |
| **Build artifacts / generated output** | Delete + gitignore | Yes | `README.html` + `README_files/` (quarto output), `target/`, `dist/` |
| **Tool-generated cache** | Delete + gitignore | Yes | `graphify-out/` (code analysis cache), `__pycache__/` |
| **Local tool config** | Delete + gitignore | Yes | `config/` (MCP server config), `.env` |
| **Documentation / content** | Commit | No | `docs/graph-entity.html`, user-created markdown |

Workflow:
```bash
# 1. List all untracked
git status --porcelain

# 2. Count files inside dirs to understand actual volume
find .serena/ README_files/ graphify-out/ -type f 2>/dev/null | wc -l

# 3. For each item: is it reproducible (cache) or unique (content)?
#    Cache -> rm -rf, then add path to .gitignore
#    Content -> git add, commit with meaningful message

# 4. After cleanup, verify
git status
```

## Common junk to watch for

| File/Dir | Why it's junk | How it got in |
|----------|--------------|---------------|
| `.mysql84/`, `mysql/data/` | Full MySQL data directory, 80-150MB | Init project with `git init` inside an existing app |
| `uploads/` | User-uploaded files, test data | Running the app creates files that get committed |
| `frontend/` | Prototype/pages | Multiple iterations of SPA, old versions left in |
| `.serena/` | AI agent IDE cache (like .cursor/ .claude/) | Running agent tooling in the repo |
| `.vscode/` | Personal IDE preferences | `git add .` without `.gitignore` |
| `*.log` | Application logs | Runtime output tracked accidentally |
| `*.class` | Compiled Java bytecode | Maven build output before `.gitignore` was added |
| `node_modules/` | NPM dependencies | Rare but happens |
| `README.html` + `README_files/` | Quarto/Markdown-rendered HTML | Running doc tooling, generated artifact |
| `*.pdf`, `*.zip`, `*.key` | Binary source materials | Lecture slides, datasets, archives |

See `references/binary-asset-gitignore.md` for a comprehensive pattern catalog.

## Public-repo readiness pass

When the repo will be made public (GitHub showcase), extra rules apply on top of the junk triage above:

1. **Ask the deletion scope upfront** — present options via clarify (e.g. delete all internal process docs / keep sensitive / archive-only). Users often override part of the scope mid-task, so keep destructive deletions reversible (`git rm`, never `rm -rf`).
2. **Sensitive/submission files: untrack, never delete.** Files with personal data (name, student ID in AI-use acknowledgements), admin submission materials, and deliverable PDFs that duplicate tracked sources → `git rm --cached` + add to `.gitignore`, keep the local copies. User's rule: "不适宜公开的你把它ignore 别直接删库".
3. **ALL-CAPS root docs may be off-limits.** `TASK.md`, `AGENTS.md`, `CLAUDE.md`, `README.md` — ask before touching; they often link to the other docs (deleting linked files leaves dangling links in them).
4. **README must reflect actual state — no unfinished content.** Before rewriting: run the test suite, pull real result numbers from `report/`/experiment JSONs, take the URL from `git remote get-url origin` (replace `your-org` placeholders), and create a `LICENSE` file if the README claims a license. Fold "research directions" that are actually implemented into a Results section instead of leaving them as future plans. The same rule extends to phase-tracking docs (`TASK.md`): never mark a feature ✅ before verifying it exists (`search_files` for the module/endpoint) — see `repo-documentation` skill → "Phase-tracking docs".
5. **Documentation language strategy (EN/ZH).** When the user asks to localize docs or split a bilingual README:
   - Split into `README.md` (English) + `README.zh-CN.md` (Chinese), each starting with a language-switch link (`**English** | [简体中文](README.zh-CN.md)` and vice versa). Keep both in sync.
   - Localize narrative text only; keep code identifiers, class/function names, metric names (Precision, AUROC…), file paths, and model names in English — translating them breaks accuracy and grep-ability.
   - **Verify code state before translating**: stale docs written at stub time ("3 prediction heads", "no message passing", "constraint extraction: 🔶 Stub") silently diverge from the implemented system. Grep `src/` for actual heads/losses/encoder before writing, and sync content while translating.
   - When the user says "公式用$包裹", wrap math in `$...$` LaTeX delimiters in markdown (e.g. `$\mathcal{L} = w_c\,\mathcal{L}_{\text{coord}} + \dots$`), not plain-text formulas.
   - LaTeX reports: name the source file after the deliverable (`report/report.tex`) so `latexmk -xelatex` defaults to `report.pdf`; add `*.xdv` to .gitignore (xelatex intermediate).

## Pitfalls

- **For public repos, default sensitive/submission/PII files to `git rm --cached` + gitignore, not deletion** — a user may approve a broad "delete internal docs" scope but still expect personal/admin material preserved locally ("不适宜公开的 ignore 别直接删库").
- **When user says a path pattern (e.g. "delete references/06-"), check that exact path level first** — run `ls -d references/06-*` before searching recursively. Don't assume the files are deeper in a subdirectory just because similar prefixes exist elsewhere. The user specifies a literal path; search it literally.
- **Don't `git rm` runtime data without `--cached`** — MySQL data dirs can't be regenerated. Use `--cached` to stop tracking but preserve the data.
- **Check if frontend/ was referenced by build scripts** before deleting — verify `sync-frontend.sh` or similar before removing.
- **`.gitignore` order matters** — patterns are evaluated in order, first match wins. Put specific patterns before catch-alls.
- **If repo is shared**, coordinate with the team before `git rm` to avoid conflicts.
- **`filter-repo` rewrites history** — only do this if the repo has never been shared or everyone is prepared to rebase.

## Post-restructuring: update all doc references

After moving, renaming, or deleting files, stale references in documentation silently rot. Run this check:

```bash
# 1. List all CAPITALLETTERS.md that might reference old paths
find . -maxdepth 2 -name '[A-Z]*.md' -not -path './.git/*'

# 2. Search for old paths in ALL of them
grep -rn "old/path/pattern" $(find . -maxdepth 2 -name '[A-Z]*.md' -not -path './.git/*') 2>/dev/null

# 3. Also search for old filenames that were renamed/deleted
grep -rn "old-filename\\|another-deleted-file" $(find . -maxdepth 2 -name '[A-Z]*.md' -not -path './.git/*') 2>/dev/null
```

Common CAPITALLETTERS.md locations: project root (`README.md`, `HANDBOOK.md`, `CLAUDE.md`), `docs/` dir (`ARCH.md`, `DEPLOY.md`, `DEMO.md`, etc.), and `docker/README.md`.

The pattern is: **grep then read then patch** — find the hits, read the surrounding context, update the path. Batch changes across multiple files when the replacement is the same (e.g. all old path → new path).

### Root Documentation Split Convention

When a project accumulates both AI-agent guidance and human usage docs, split AGENTS.md into two files:

| File | Audience | Content |
|------|----------|---------|
| `AGENTS.md` | AI agents (Codex, Hermes, Claude Code) | Constraints, conventions, coding standards, testing rules |
| `README.md` | Human collaborators | Project overview, tech stack, directory structure, setup |

Additionally, create `CLAUDE.md` as a **symlink** to `AGENTS.md` so Claude Code and Hermes/Codex both honor the same rules:

```bash
ln -s AGENTS.md CLAUDE.md
# Git tracks symlinks natively — no special config needed
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md as symlink to AGENTS.md"
```

This symlink approach (mode `120000` in git) means any update to `AGENTS.md` is immediately visible to CLAUDE.md readers with zero maintenance overhead.
