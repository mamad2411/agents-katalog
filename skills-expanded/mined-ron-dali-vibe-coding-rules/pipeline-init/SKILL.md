---
name: pipeline-init
version: 2.9.0
---

# pipeline-init — Project Initialization Wizard V2.9

> Conversational project info collection → dependency detection → scaffold creation → pipeline template fork → ready in one go.
> V2.6 adds Step -1: Platform Detection → Memory Self-Heal → Project State Detection with three-path handling.
> V2.7 softens Memory seeding: discover + suggest, not force-write. Cross-platform compatibility first.
> V2.8 fixes Path C: adds user confirmation + language selection.
> V2.9 **去模板化**：Path C 从固定模板创建改为项目扫描→智能提案→用户确认，只创建项目真正需要的目录。

## Trigger Conditions

Activate when any of the following occurs:
- User says "I want to build X project", "Help me init the pipeline", "New project"
- Memory trigger hits new-project intent
- User mentions starting a new project
- **V2.6**: Skill first loaded in ANY project (runs Step -1 for memory self-heal)

## Workflow

### Step -1: Pre-Initialization Detection（V2.6 NEW — Run first on every skill load）

This step runs BEFORE any other workflow. It is **idempotent** — safe to run repeatedly.

#### Step -1.0: Platform Detection（确定 Memory 文件路径）

Detect which AI coding tool the user is using, and map to its memory/rules file:

| Detection Condition | Tool | Memory File |
|:--|:--|:--|
| `~/.codebuddy/skills/` directory exists | CodeBuddy | `.codebuddy/memory/MEMORY.md` |
| `.cursor/rules/` directory exists | Cursor | `.cursor/rules/vibe-coding-rules.mdc` |
| `.windsurfrules` file exists | Windsurf | `.windsurfrules` |
| `CLAUDE.md` file exists | Claude Code | `CLAUDE.md` |
| `.github/copilot-instructions.md` exists | GitHub Copilot | `.github/copilot-instructions.md` |
| None of the above | Generic fallback | `.ai-pipeline/MEMORY.md` |

Store detected `memoryPath` for use in Step -1.a and Step 6.

#### Step -1.a: Memory Integrity Check & Self-Heal（每次加载必执行，幂等）

1. Read the file at `memoryPath` (from Step -1.0)
2. Check for 5 critical sections (using fuzzy markdown heading match):
   - `"Skill依赖链"` or `"Skill 编排"` or `"Skill Orchestration"`
   - `"强制自检硬规则"` or `"步骤6（测试）不可跳过"` or `"Step 6 mandatory"`
   - `"开发文档标准路径"` or `"Dev doc standard paths"`
   - `"面包屑规则"` or `"breadcrumb"`
   - `"项目初始化状态"` or `"已初始化"` or `"initialization status"`
3. If ANY section is missing → **detect and report** (V2.7: do NOT auto-write without confirmation)
4. Report missing sections to user: "发现 Memory 文件缺少 [N] 个关键段落：[list]。是否自动补全？(是 / 跳过)"
5. Only write to `memoryPath` after explicit user confirmation
6. If file does not exist → ask: "没有检测到 Memory 文件，要创建吗？(是 / 先不要)"
7. Record in log: `self-healed: [list]` or `self-heal-skipped: [list]`

**Why V2.7 changed from auto-write to confirm / 为什么改为确认而非自动写入**: Different platforms have different memory file formats (`.mdc` for Cursor, `.codebuddy/memory/` for CodeBuddy, `CLAUDE.md` for Claude Code). Blind auto-writing can break platform-specific syntax or interfere with user's existing configuration. Discovery is universal; writing requires consent.

**File format adaptation**:
- `.mdc` files (Cursor): add YAML frontmatter (`---\ndescription: Vibe Coding Rules\nalwaysApply: true\n---`) before markdown
- `.md` / `.windsurfrules` / `CLAUDE.md`: plain markdown

**This step runs on EVERY skill activation** — not just first time. It ensures the pipeline's critical rules are always present in memory, preventing AI from skipping mandatory steps.

#### Step -1.b: Project State Detection

After memory self-heal, detect project state:

1. Check if project root has code files (`.js`, `.html`, `.py`, `.ts`, etc.)
   → NO → **Path A: New Project**
2. Check if `开发文档/` directory exists (or configured `devDocs` path)
   → NO → **Path C: Existing Project Without Docs**
3. Check if `开发文档/00-必读/开发文档管理.md` exists
   → YES → **Path B: Existing Project With Docs**
   → NO → **Path C: Existing Project Without Docs**

#### Path A: New Project

Proceed with standard pipeline-init workflow (Step 0 through Step 7 below).

#### Path B: Existing Project With Docs — Compliance Scan

1. Run DOC_SPEC compliance scan:
   - Check all docs in `开发文档/` have `📋 管理规范见` reference in header
   - Check no orphan files in wrong directories
   - Check file size limits (≤500 lines)
   - Verify `📖` references point to existing docs
   - Verify management doc index is up to date
2. Output a report: `[N] missing 📋 references | [N] files over limit | [N] broken 📖 links`
3. Ask user: "Found some documentation issues. Fix them now or later?"
4. If user says "fix now" → repair issues (add 📋, split large files, fix broken links)

#### Path C: Existing Project Without Docs — Bootstrap

> **V2.9 核心哲学：去模板化。** 不同项目需要不同的开发文档结构，Skill 不应该拿着一套固定模板往任何项目里硬塞。正确的做法是：扫描项目 → 检测特征 → 智能提案 → 用户确认。

0. **Ask user confirmation before creating**: "检测到项目缺少开发文档目录。是否自动创建？
   （将先扫描项目结构，根据实际技术栈和特征给出定制化建议）
   ① 是，帮我创建  ② 跳过（后续可手动执行「初始化开发文档」）"
   → If skip → exit with message: "已跳过。需要时可以说'初始化开发文档'来手动触发。"
   → If proceed → continue to Step 1.

1. **Language selection first**: Run Phase 0 of `references/init-dialog.md` to ask user's preferred language (中文 / English / 日本語 / 其他).

2. **Project Scan（扫描项目特征）**：

   a. **文件类型分布**：统计项目代码文件类型（`.js`/`.py`/`.ts`/`.html`/`.css` 等），了解项目主要语言。

   b. **技术栈检测**（按优先级搜索）：
      - 读 `package.json` → 检测 Web 框架（Express/Koa/Fastify）、前端框架（React/Vue/Svelte）、Electron、CLI 工具等
      - 读 `requirements.txt` / `pyproject.toml` → 检测 Python 框架（FastAPI/Django/Flask）
      - 读 `Cargo.toml` / `go.mod` / `Gemfile` → 检测 Rust/Go/Ruby 项目类型
      - 读 `Dockerfile` / `docker-compose.yml` / `ecosystem.config.js` → 部署相关
      - 读 `.github/workflows/` / `.gitlab-ci.yml` → CI/CD 相关

   c. **关键特征检测**（决定建议哪些目录）：
      | 检测到 | 建议目录 | 理由 |
      |:--|:--|:--|
      | HTTP 路由文件（`routes/`、`server.js`、`app.js` 等） | 接口文档 | 有 API 需要文档化 |
      | Agent/AI prompt 相关文件（`prompts/`、`agent/`、`metacraft/` 等） | Agent模板 | 有 AI Agent 需要模板管理 |
      | 项目模块数 ≥ 3 且结构复杂 | 架构设计 | 复杂项目需架构文档 |
      | 多方案设计痕迹（`proposal/`、`design/`、方案对比文档） | 方案设计 | 有方案决策需要记录 |
      | 部署配置文件（Dockerfile、k8s、PM2、Nginx 等） | 部署运维 | 有部署流程需要文档 |
      | PRD/合规/软著/法律相关文件 | 产品与合规 | 有合规需求 |
      | 工具/脚本集合（`scripts/`、`tools/` 目录非空） | 项目参考 | 自定义工具需要说明 |

   d. **不确定项标记**：对于无法确定是否需要但可能相关的目录，标记为 `❓不确定`，在提案中单独列出询问用户。

3. **Propose Tailored Structure（展示定制化提案）**：

   根据扫描结果，向用户展示提案，格式如下：

   ```
   根据项目扫描结果，建议创建以下开发文档目录：

   ✅ 强制（任何项目都需要）：
      00-必读/          — 开发文档管理规范+项目概览
      01-变更日志/      — 每次改动的变更记录
      归档/             — 过期文档季度归档

   ✅ 建议创建（基于项目特征）：
      04-接口文档/      — 检测到 HTTP 路由（routes/ 目录，Express 框架）
      [其他建议...]

   ❓ 不确定是否需要：
      06-Agent模板/     — 未检测到 AI Agent 相关代码，是否需要？
      [其他不确定...]

   ❌ 不建议（与项目无关）：
      05-部署运维/      — 未检测到部署配置文件
      [其他不建议...]

   你可以：
   ① 确认全部建议（默认）
   ② 调整：添加/删除/重命名目录
   ③ 自定义：告诉我你想要的目录结构
   ```

   **关键原则**：
   - 永远不要让用户看到与项目无关的空目录
   - `00-必读/`、`01-变更日志/`、`归档/` 是唯一三项强制创建
   - 其他目录全部基于扫描结果建议，由用户最终决定
   - 如果用户说"我不知道需要什么"→ 展示完整可选列表，逐一询问

4. **User Confirms → Create Structure**：

   用户确认后：
   - 创建用户选定的目录结构
   - 为每个目录创建 `.gitkeep` 或初始索引文件
   - 在 `00-必读/` 中创建 `开发文档管理.md`，其「目录结构」节由实际创建的结构填充（不是固定模板）

5. **Auto-Populate from Scan**（根据扫描结果智能填充初始内容）：

   - 如果创建了 `接口文档/` → 扫描路由文件，生成路由清单骨架
   - 如果创建了 `Agent模板/` → 扫描 prompt 文件，列出已有模板
   - 如果创建了 `架构设计/` → 生成项目文件结构概览
   - 如果创建了 `项目参考/` → 列出工具脚本和配置说明
   - 所有未填充的标记为 `<!-- TODO: 待补充 -->`

6. **Run baseline self-check**（如果项目有可执行代码）：
   - 执行 self-check 周期
   - 将基线发现写入 `01-变更日志/变更日志-YYYY-MM-DD.md`
   - 标记为 "baseline finding — not a regression"

7. **Report**: "已创建 [N] 个目录的开发文档结构。以下是初始填充内容摘要..."

### Step 0: Language Selection

Follow `references/init-dialog.md` Phase 0 to ask the user's preferred language. All subsequent generated docs, memory files, and changelogs MUST use the selected language.

### Step 1: Conversational Collection

Follow `references/init-dialog.md` template to progressively collect:
1. **Project name**, 2. **Tech stack**, 3. **Project type**, 4. **Auto-testing needed?** (default yes)

### Step 2: Dependency Detection

Check environment: Node.js version, npm, Git, additional deps per tech stack.
On failure: provide plain-language guides. Mark missing items for later.

### Step 3-5: Create Structure + Fork Template + Populate pipeline.json

Create `.ai-pipeline/` with `pipeline.json`, `VERSION` (2.9.0), and self-check references.
Fork `self-check` and `changelog` Skill templates. Populate project config.
Write `README.md` with proper language and no hardcoded versions.

### Step 6: Write Project Memory

Using the Step -1.0 detected platform, append V2.6 pipeline enforcement rules to the memory file, including:
- Skill dependency chain (mandatory order)
- Force self-check hard rules (Step 6 mandatory, Step 5.5 integrity gate)
- Dev doc standard paths
- Breadcrumb rules
- Initialization status marker

### Step 7: Confirm Completion

Report created structure, config items, and pipeline readiness.
If memory was self-healed in Step -1.a, mention which sections were repaired.
