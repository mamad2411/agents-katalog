---
name: git-init
description: "Initialize a new git repository with standard structure: .gitignore, README, initial commit, and optional remote setup. Use when: init git, new repo, setup git project, create repository."
argument-hint: "optional remote URL or platform (github/gitlab)"
tools: [run_in_terminal, create_file]
---

## Step 1 — Check Environment

Run `git status` to check if a git repo already exists.
- If already initialized, report "Git repo already exists" and stop.

Detect project type by scanning for common config files:
- `package.json` → Node.js
- `requirements.txt` / `pyproject.toml` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `pom.xml` / `build.gradle` → Java
- None detected → generic

## Step 2 — Create .gitignore

If `.gitignore` does not exist, create one based on the detected project type.

**Node.js:**
```
node_modules/
dist/
.env
.env.local
*.log
.DS_Store
```

**Python:**
```
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.env
.venv/
venv/
.DS_Store
```

**Go:**
```
bin/
*.exe
*.test
.env
.DS_Store
```

**Rust:**
```
target/
.env
.DS_Store
```

**Java:**
```
target/
*.class
*.jar
.mvn/
.env
.DS_Store
```

**Generic:**
```
.env
.DS_Store
*.log
tmp/
```

## Step 3 — Create README (if missing)

If `README.md` does not exist, create a minimal one:
```
# <project folder name>

> TODO: Add project description.
```

## Step 4 — Initialize & Initial Commit

Run:
1. `git init`
2. `git add -A`
3. `git commit -m "chore: initial commit"`

Report the commit hash.

## Step 5 — Set Up Remote (optional)

Ask the user (or infer from their argument) which situation applies:

### 场景 A — 用户已有远程仓库 URL
设置代理并关联推送：
```
export http_proxy="http://127.0.0.1:10080" https_proxy="http://127.0.0.1:10080"
git remote add origin <url>
git branch -M main
git push -u origin main
```

### 场景 B — 需要在 GitHub 上新建仓库（使用 gh CLI）

检查 `gh` 是否可用：`which gh`

若可用，运行：
```
gh repo create <repo-name> --public --source=. --remote=origin --push
```
- 默认使用当前文件夹名作为 `<repo-name>`
- 可按需改为 `--private`
- `--source=. --remote=origin --push` 会自动关联并推送

若 `gh` 不可用，提示用户安装：
```
brew install gh   # macOS
gh auth login
```

### 场景 C — 需要在 GitHub 上新建仓库（使用 MCP GitHub 工具）

若环境中有 `mcp_github_create_repository` 工具可用：
1. 调用该工具创建仓库，获取返回的 `clone_url`
2. 然后关联并推送：
```
git remote add origin <clone_url>
git branch -M main
export http_proxy="http://127.0.0.1:10080" https_proxy="http://127.0.0.1:10080"
git push -u origin main
``` — 不需要远程仓库

跳过此步骤，仅提示用户后续可用以下命令手动添加：
```
git remote add origin <url>
git push -u origin main
```
