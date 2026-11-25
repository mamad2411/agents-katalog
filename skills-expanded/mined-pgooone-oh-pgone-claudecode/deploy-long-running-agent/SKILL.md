---
name: deploy-long-running-agent
description: |
  Deploy a complete long-running AI coding agent workspace from a PRD document.
  Use this skill whenever the user wants to set up an autonomous multi-session AI coding pipeline,
  mentions "auto coding agent", "long running agent", "CLAUDE.md workflow", or asks to scaffold
  a project for iterative AI development based on a PRD or spec.
  Also trigger when the user says things like "turn this PRD into an agent project",
  "help me build a task-driven AI coding harness", or references SamuelQZQ / Anthropic long-running agents.
  Also trigger when the user wants to UPDATE an existing agent workspace with new PRD requirements.

  ## Usage Examples

  **Create from scratch:**
  ```
  "帮我把 PRD.md 部署成自动编程 Agent 工作区"
  "将这个产品需求文档转为 AI 编码 Agent 项目"
  "用 SamuelQZQ 的方法给我的 PRD 搭一套自动化开发环境"
  ```

  **Update existing workspace:**
  ```
  "在这个已有项目上追加新 PRD 的需求"
  "给现有 Agent 项目添加新功能模块"
  "更新 task.json 加入这些新需求"
  ```

  After the skill finishes scaffolding, it will present a native Claude Code choice
  for how to start development (Manual / Semi-Auto / Full-Auto). Do not proceed
  with task execution until the user explicitly selects a mode.
---------------------------------------------------------------------------------------------------------

# Deploy Long-Running Agent Workspace

This skill reads a Product Requirements Document (PRD) and scaffolds or updates a workspace for long-running autonomous AI coding using the "artifacts over context compaction" methodology (inspired by SamuelQZQ's auto-coding-agent-demo and Anthropic's "Effective Harnesses for Long-Running Agents").

## Core Philosophy

Instead of relying on LLM context compression to remember state across sessions, this methodology uses **environment artifacts**:

- `CLAUDE.md` — fixed workflow rules (system prompt)
- `task.json` — structured task list (single source of truth)
- `progress.txt` — human-readable session logs
- `init.sh` — standardized environment recovery
- `git commit` — code change history

Each new Claude Code session starts with a **clean context window**, reads these artifacts, and completes **exactly one task**.

## Inputs

The user should provide:

1. **Path to a PRD file** (markdown or text)
2. **Target directory name** (optional; defaults to a slug derived from the product name)

If the user does not explicitly provide both, ask for the PRD path before proceeding.

## Mode Detection

Before starting, check if the target directory already exists and contains a valid agent workspace (look for `CLAUDE.md`, `task.json`, `init.sh`).

- **If NO existing workspace** → Enter **Create Mode** (Steps 1–10)
- **If existing workspace IS FOUND** → Enter **Update Mode** (Steps 11–14)

Report which mode was detected to the user.

---

## CREATE MODE — Build from Scratch

### Step 1: Read and analyze the PRD

Read the PRD file thoroughly. Extract:

- Product name and description
- Target users and positioning
- Tech stack (language, framework, database, external APIs, etc.)
- Feature list with priorities (P0/P1/P2)
- MVP scope
- Data models / schemas
- API requirements
- Notification / integration requirements
- Any special constraints (rate limits, auth methods, etc.)

### Step 2: Detect tech stack

Based on the PRD, determine the primary stack. Use these signals:

- **Python**: mentions Python, FastAPI, Django, Flask, pandas, pytest, APScheduler, SQLite, PostgreSQL, httpx, requests
- **Node.js / Next.js**: mentions Next.js, React, TypeScript, npm, Express, Prisma, Tailwind
- **Go**: mentions Go, Gin, Echo, GORM
- **Java / Spring**: mentions Java, Spring Boot, Maven
- **Rust**: mentions Rust, Actix, Tokio
- **Other**: generic web, mobile, etc.

Store this decision; it will shape `init.sh`, `CLAUDE.md`, and directory structure.

### Step 3: Create target directory and basic structure

Create the target directory and subdirectories based on the stack. Typical structure:

**Python backend:**

```
project-name/
├── api/
├── core/
├── notify/
├── storage/
├── utils/
├── data/
└── tests/
```

**Next.js full-stack:**

```
project-name/
├── src/
│   ├── app/
│   ├── components/
│   └── lib/
├── supabase/
└── tests/
```

**Generic:**

```
project-name/
├── src/
├── tests/
└── docs/
```

Create empty `__init__.py` or `index.ts` placeholder files as needed.

### Step 4: Generate `architecture.md`

Write a comprehensive architecture document. Each section must contain specific content, not just a heading:

1. **Project Overview** — 1-2 sentences: what the product does, who the target users are, and what problem it solves.

2. **Tech Stack Table** — Use a markdown table: | Layer | Technology | Purpose |

3. **System Architecture Diagram** — Mermaid flowchart showing the complete data flow: Frontend → Backend → Database → External Services. Include all components mentioned in the PRD.

4. **Core Business Process Diagrams** — At least one Mermaid flowchart for the primary user journey (e.g., user registration → create item → process → result). Cover the main use case from the PRD.

5. **Data Model** — Mermaid ER diagram showing entity relationships. Follow with a table for each entity: | Field | Type | Constraints | Description |

6. **API Design** — Table: | Method | Path | Description | Request Body | Response Body |. Include authentication requirements if mentioned in PRD.

7. **External Service Integration** — For each external API: endpoint URL pattern, auth method, a concrete request example, and expected response example. Use placeholders like `your_api_key_here` for sensitive data.

8. **Configuration Design** — Table: | Config Key | Description | Default | Required |. Include all env vars from `.env.example`.

9. **Notification / Message Templates** — If the PRD mentions notifications (webhooks, emails, IM), include the exact message template format with placeholders.

Use concrete details from the PRD. Do not make up endpoint URLs or API keys unless the PRD provides them.

### Step 5: Generate `task.json`

Convert the PRD feature list into **5–15 executable tasks**, ordered by dependency:

1. **Project scaffold** — dependencies, config templates, directory structure
2. **External API / client modules** — wrappers for third-party APIs
3. **Data layer** — database schemas, migrations, models, CRUD
4. **Core business logic** — domain services, analyzers, schedulers
5. **Integration layer** — notifications, webhooks, exports
6. **Entry point / orchestration** — main.py, server startup, scheduler registration
7. **Testing** — unit tests, integration tests
8. **Final polish** — linting, end-to-end validation, documentation

Each task must be a JSON object:

```json
{
  "id": 1,
  "title": " concise task title",
  "description": "what this task accomplishes",
  "steps": [
    "specific verifiable step 1",
    "specific verifiable step 2",
    "specific verifiable step 3"
  ],
  "passes": false
}
```

Task granularity rules:
- A single task should be completable in **30–60 minutes** by an AI agent
- If a task has more than **8 steps**, split it into two tasks
- If a task touches **multiple unrelated modules**, split it into multiple tasks
- Keep foundational tasks (scaffold, DB, auth) before feature tasks
- Keep integration tasks (notifications, webhooks) after core logic tasks
- Keep testing tasks near the end, after the features they test exist

Rules:

- `steps` should be concrete enough that an AI agent can verify them
- foundational tasks (scaffold, DB, auth) come before feature tasks
- `passes` is always `false` initially
- IDs must be sequential starting from 1

### Step 6: Generate `CLAUDE.md`

This is the **Agent Workflow Bible**. It must include:

1. **Project Context** — one-line summary
2. **Mandatory Agent Workflow** — 6 steps:
   - Step 1: Initialize Environment (`./init.sh`)
   - Step 2: Select Next Task (`task.json`, `passes: false`)
   - Step 3: Implement the Task
   - Step 4: Test Thoroughly (stack-specific commands)
   - Step 5: Update `progress.txt`
   - Step 6: Commit Changes (all in one commit)
3. **Blocking Issues Section** — Detailed rules for when an Agent must STOP and ask for human help. This is critical for preventing wasted API tokens and incorrect commits.

   Must include ALL of the following subsections:

   **a. Blocking Scenarios (when to stop):**
   List at least these 4 scenarios:
   - Missing environment config: API keys in `.env` not filled, external service accounts not created, database not initialized
   - External dependency unavailable: third-party API down, OAuth requiring human approval, paid service upgrade needed, rate limit exceeded
   - Testing impossible: feature requires real user accounts, depends on undeployed external systems, needs specific hardware, API behavior does not match documentation
   - Ambiguous requirements: PRD lacks detail needed to implement, two tasks have conflicting requirements

   **b. DO NOT / DO rules:**
   ```
   **DO NOT (禁止):**
   - ❌ Submit a git commit
   - ❌ Set task.json passes to true
   - ❌ Pretend the task is complete
   - ❌ Skip the failing step and move to the next one

   **DO (必须):**
   - ✅ Record current progress and blocking reason in `progress.txt`
   - ✅ Output a clear blocking message explaining what human help is needed
   - ✅ STOP the task and wait for human intervention
   - ✅ Preserve all code changes in the working directory (do not revert)
   ```

   **c. Blocking message format (强制模板):**
   The Agent must output blocking information in this exact format:

   ```
   🚫 任务阻塞 - 需要人工介入

   **当前任务**: [task title from task.json]

   **已完成的工作**:
   - [completed code/config]

   **阻塞原因**:
   - [specific reason why cannot continue]

   **需要人工帮助**:
   1. [specific step 1]
   2. [specific step 2]
   ...

   **解除阻塞后**:
   - 运行 [command] 继续任务
   ```

   **d. progress.txt logging requirement:**
   When blocked, the Agent must also append to `progress.txt`:

   ```
   ## [Date] - BLOCKED: [task title]

   **Blocked at step**: [which step in the task]
   **Reason**: [blocking reason]
   **Completed before block**: [what was done]
   **Needs human**: [what human needs to do]
   ```

4. **Project Structure** — directory map
5. **Commands** — stack-specific dev/test/build commands
6. **Coding Conventions** — at least 3-5 specific rules (naming, file organization, error handling, logging)
7. **Key Rules** — one task per session, test before commit, never remove tasks
8. **New Session Onboarding** — If you are a NEW Claude Code session with no prior conversation history, read this file first, then task.json, then progress.txt, then run `git log --oneline -20`

Tailor testing commands to the detected tech stack:

- **Python**: `python -m pytest tests/`, `python -m py_compile`, `ruff check .`, `mypy`
- **Node.js**: `npm run lint`, `npm run build`, `npm test`, browser tests with Playwright
- **Go**: `go test ./...`, `go build`, `go vet`
- **Java**: `./mvnw test`, `./mvnw compile`

### Step 7: Generate `init.sh`

Write a bash script that:

- Checks required language/runtime version
- Installs dependencies (creates venv / runs npm install / go mod download)
- Starts dev server if needed
- Checks for `.env` and warns if missing
- Runs a quick syntax/compilation check
- Handles Windows (Git Bash/msys) vs Unix path differences for virtual envs

Make `init.sh` executable (`chmod +x init.sh`).

### Step 8: Generate automation scripts

Read the bundled templates from `assets/run-automation.sh.template` and `assets/run-automation.ps1.template`. Adapt them for the current project by replacing ALL placeholders:

- Replace `[PROJECT_NAME]` with the actual product name from the PRD
- Replace `[TEST_COMMANDS]` with stack-specific test commands (e.g., `python -m pytest tests/` for Python, `npm test` for Node.js, `go test ./...` for Go)
- Remove any stack-specific references that do not match the detected tech stack

Save both files to the target directory and make `run-automation.sh` executable.

### Step 9: Generate remaining scaffold files

**`.env.example`**

- All API keys, tokens, webhook URLs, database URLs mentioned in the PRD
- Section comments for readability

**`README.md`**

- Project title and one-line description
- Core features bullet list
- Quick start (run `./init.sh`, configure `.env`, start development)
- Test command

**`QUICKSTART.md`**

- Environment requirements
- Unzip / clone instructions
- `./init.sh` → `cp .env.example .env` → `git init` → start agent workflow
- All three run modes (manual, semi-auto, full-auto) with platform-specific commands
- Windows users get `.\run-automation.ps1 -Runs 10`
- Linux/macOS/Git Bash users get `./run-automation.sh 10`

**`TECH-NOTES.md`**

- Explain the long-running agent methodology
- Why artifacts beat context compaction
- The role of `CLAUDE.md`, `task.json`, `progress.txt`, `git`
- Reference links with real URLs:
  - SamuelQZQ's project: `https://github.com/SamuelQZQ/auto-coding-agent-demo`
  - Anthropic article: `https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents`

**`next-task.txt`** (required for Semi-Auto and Full-Auto modes)

A minimal prompt file used by `claude -p`. Must follow the single-source principle: do not repeat rules from CLAUDE.md, only reference them.

```
你正在启动一个全新的 Claude Code session，没有任何历史上下文。

请严格按以下顺序执行：

1. 读取 CLAUDE.md — 这是你的工作流圣经，包含完整的文件读取顺序、任务执行步骤和阻塞处理规则
2. 按照 CLAUDE.md 中的工作流，完成 task.json 中下一个 passes: false 的任务
3. 每次只完成一个任务，然后停止

⚠️ 不要假设任何历史上下文。所有项目状态都在文件中。
```

**`progress.txt`**

- Header comment only: `# Progress Log`

**`main.py`** **/** **`index.ts`** **/** **`main.go`** **stub**

- A minimal runnable entry point that prints "\[Project] initialized, waiting for full implementation"

**`config.py`** **/** **`config.ts`** **/** **`config.go`** **stub**

- A minimal configuration dataclass/struct with placeholders for key env vars

### Step 10: Package into a zip file

Create a zip archive of the target directory, excluding any virtual environments or cache files.

Report the final file path to the user.

---

## UPDATE MODE — Incremental PRD Changes

If an existing agent workspace is detected (contains `CLAUDE.md`, `task.json`, `init.sh`), follow these steps instead of creating from scratch.

### Step 11: Read existing workspace state

Read the current files to understand what's already done:
- `task.json` — note which tasks have `passes: true` vs `passes: false`
- `progress.txt` — understand development history
- `architecture.md` — understand current architecture
- `CLAUDE.md` — understand existing workflow rules

### Step 12: Read the new/updated PRD

Read the new PRD and identify what's **new or changed** compared to the existing workspace:

- New features not in current `task.json`
- Changed requirements for existing features
- New external APIs or integrations
- Tech stack changes

**DO NOT** modify tasks that are already `passes: true`. Those are considered completed.

### Step 13: Merge task.json

Update `task.json` following these rules:

1. **Keep all existing tasks** with their current `passes` status
2. **Append new tasks** at the end with the next sequential IDs
3. **Mark modified tasks** (requirements changed) as `passes: false` even if they were previously `passes: true`
4. **Preserve completed work** — do not delete or renumber existing tasks

Example merge:

```json
{
  "project": "My Project",
  "tasks": [
    // Existing tasks preserved
    { "id": 1, "title": "Scaffold", ..., "passes": true },
    { "id": 2, "title": "Auth", ..., "passes": true },
    { "id": 3, "title": "Old Feature", ..., "passes": false },
    // NEW tasks appended
    { "id": 4, "title": "New Feature from PRD", ..., "passes": false },
    { "id": 5, "title": "Another New Feature", ..., "passes": false }
  ]
}
```

### Step 14: Update affected files

Only update files that are affected by the PRD changes:

- **`architecture.md`** — add new components, APIs, data models
- **`CLAUDE.md`** — update if tech stack or testing commands changed
- **`init.sh`** — add new dependencies if needed
- **`.env.example`** — add new environment variables
- **`README.md`** — update feature list
- **`QUICKSTART.md`** — update if workflow changed
- **`progress.txt`** — append a note: `## [Date] - PRD Update: [description]`

Do NOT touch `run-automation.sh`, `run-automation.ps1`, or `TECH-NOTES.md` unless their content is directly affected.

---

## AFTER BUILD / UPDATE — User Execution Guide

Whether in Create Mode or Update Mode, after all files are generated or updated, **DO NOT start executing tasks automatically**. First perform pre-execution checks, then use the `AskUserQuestion` tool to let the user choose a mode.

### Pre-execution Checks

Before presenting choices, verify:
- [ ] `next-task.txt` exists in the target directory
- [ ] `.env` file exists (if not, warn: "请先运行 cp .env.example .env 并填写配置")
- [ ] Git is initialized and has at least one commit (if not, warn: "请先运行 git init && git add . && git commit -m 'Initial commit'")

### AskUserQuestion — Primary Choice

**Question**: `Agent Workspace Ready — 选择开发模式`

**Options**:

1. **Manual Mode（推荐前 1-2 个任务）**
   - Description: `交互式 session，每个工具调用都需确认。适合验证 Agent 是否理解项目。`
   - Preview: `claude\n然后输入: "请按照 CLAUDE.md 完成下一个任务。"`

2. **Semi-Auto Mode（跑顺后推荐）**
   - Description: `非交互式，每次运行一个 task 后自动退出，下次再手动触发。上下文干净。`
   - Preview: `claude -p --dangerously-skip-permissions < next-task.txt`

3. **Full-Auto Mode（人离开时用）**
   - Description: `脚本自动循环 N 次，每次启动全新 Claude Code 进程。`
   - Preview: `Linux/macOS/Git Bash: ./run-automation.sh 10\nWindows PowerShell: .\run-automation.ps1 -Runs 10`

### Actions by Mode

**If user selects Manual Mode:**
- Tell the user: `运行 claude，然后输入："请按照 CLAUDE.md 中的工作流，完成 task.json 中的下一个任务。"`
- Do NOT execute `claude` yourself. The user must start it manually.

**If user selects Semi-Auto Mode:**
- Confirm `next-task.txt` exists in the project directory.
- AskUserQuestion secondary: `现在立即执行第一个 task？`
  - **Yes**: `cd [project-dir] && claude -p --dangerously-skip-permissions < next-task.txt`
    - Execute via Bash tool. This will block until `claude -p` finishes (one task completes and exits).
    - After completion, read `task.json` to check if `passes` flipped to true.
    - Report: "Task X [completed/skipped/blocked]. [Y] tasks remaining."
  - **No**: Tell user to run the command manually when ready.

**If user selects Full-Auto Mode:**
- AskUserQuestion secondary: `现在立即启动自动化循环（默认 10 次）？`
  - **Yes**: `cd [project-dir] && ./run-automation.sh 10` (or `.un-automation.ps1 -Runs 10` on Windows)
    - Execute via Bash tool. The script handles the loop.
    - Report: "Automation started. Logs will be saved to automation-logs/."
  - **No**: Tell user to run the command manually when ready.

### Important Rules

- Manual Mode: never execute — the user must control the interactive session.
- Semi-Auto Mode: execute one run only, then stop and report.
- Full-Auto Mode: execute the loop script, which itself handles multiple runs.
- If the user does not confirm execution in the secondary AskUserQuestion, **stop here**.

---

## Output Checklist

Before finishing, verify that the target directory contains:

- [ ] `architecture.md`
- [ ] `task.json` (valid JSON, 5–15 tasks for create mode; properly merged for update mode)
- [ ] `CLAUDE.md`
- [ ] `init.sh` (executable)
- [ ] `run-automation.sh` (executable)
- [ ] `run-automation.ps1`
- [ ] `.env.example`
- [ ] `README.md`
- [ ] `QUICKSTART.md`
- [ ] `TECH-NOTES.md`
- [x] `progress.txt`
- [ ] `next-task.txt`
- [ ] Basic project directory structure
- [ ] A runnable stub entry point
- [ ] A zip file of the entire workspace (create mode only)

## Important Notes

- Do NOT assume the user wants a Next.js app if the PRD says Python. Match the PRD exactly.
- Do NOT invent fake API endpoint URLs or keys. Use placeholders like `your_api_key_here`.
- If the PRD lacks detail on a topic (e.g., database schema), infer a reasonable minimal design and document it.
- The goal is a **ready-to-use agent harness**, not a fully implemented product. The AI will write the actual code in subsequent sessions.
- **NEVER start executing tasks without explicit user consent.** Always present the three-mode choice and wait.
