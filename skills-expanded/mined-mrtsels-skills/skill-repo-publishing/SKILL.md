---
name: skill-repo-publishing
description: Use when publishing a Hermes skill as its own git repo.
license: MIT
metadata:
  hermes:
    tags:
    - skill-authoring
    - git
    - github
    - publishing
    - sync
    related_skills:
    - subagent-driven-development
    - repo-documentation
    - knowledge-organization
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
    platforms:
    - macos
    - linux
  imported_from: hermes
---

# Skill Repo Publishing

把 Hermes 技能发布为独立公开 git 仓库，并维护"双克隆同步"。已验证实例：`mrtsels/rail-cli`、`mrtsels/trading-agents`（2026-08 全流程实测）。

## When to Use

- 用户要求技能拥有自己的公开仓库（本用户的既定模式）
- 现有技能超过单文件规模，需要仓库化
- 需要为已仓库化的技能做双克隆同步（push → 技能侧 pull）

## 布局（双克隆）

- **开发根**：`~/<name>-skill`（或 `~/<name>` 若名称空闲）——日常开发的仓库克隆
- **技能侧**：`~/.agents/skills/coding/<name>`——同一仓库的 git 克隆，Hermes 从这里加载技能
- 改动流转：开发根 commit+push → 技能侧 `git pull origin main`

## Steps（2026-08 trading-agents 实测验证）

1. `gh repo create mrtsels/<name> --public --description "..."`（先 `ls ~` 查名称冲突）
2. clone 到开发根：`~/<name>-skill`（若 `~/<name>` 已被占用——如上游 fork——用 `-skill` 后缀）
3. 把草稿技能内容（SKILL.md、references/）移入克隆；**删除旧草稿目录**（`~/.hermes/skills/...`），避免双份加载
4. 写 README.md（人类指南）、.gitignore（`__pycache__/`、`.DS_Store`、`*.pyc`、`.venv/`）、AGENTS.md（规则，见 `templates/AGENTS.md`）
5. 开发：SKILL.md + `scripts/`；**真实运行验证**后再 commit（零编造纪律：数据/行号引用必须实测）
6. 最终闸门：派 fresh-eyes 审校子代理（配方见本技能 `references/spec-compliance-review.md`；派发机制参考 `subagent-driven-development`，其为 external-dir 技能只读）→ 应用修正 → 回归测试 → commit
7. clone 到技能侧：`git clone https://github.com/mrtsels/<name>.git ~/.agents/skills/coding/<name>`
8. 每次 push 后：`cd ~/.agents/skills/coding/<name> && git pull origin main`
9. 可选：在 `mrtsels/skills` 里登记为 submodule（rail-cli 先例）——**先问用户**，会改动其 skills 仓库

## AGENTS.md 老规矩（本用户公开仓约定）

- **Git**：禁 `git add .`/`-A`，只 add 具体路径；逐任务 commit；Conventional Commits；commit 后立即 push
- **行为**：零编造（数据必须可溯源）；研究类内容声明"非投资建议"；公开仓禁个人敏感信息
- **同步章节**：写明双克隆流转，让未来 agent 知道技能侧要 pull
- **相关技能**：列出相关 skills（repo-documentation、subagent-driven-development 等）
- 语言：中文（用户仓库 AGENTS.md 均为中文）

## 包装既有应用的 CLI+skill 项目：仓库边界（cupedia-cli 先例，2026-08）

当目标是"把现有线上应用（如 CUpedia）打包成 CLI + agent skill"时，三份产物分属三个仓库，不要混放：

- **应用仓库**：只容纳后端 API 改造（薄包装路由，**用通用路径 `/api/*`，不要建 CLI 专用命名空间 `/api/cli/*`**——前端与 CLI 同源共用一个契约，CLI 专用命名空间会成为第二套契约而漂移；cupedia-cli 先例：用户明确否掉 `/api/cli/*` 方案），走 PR 合入。PR 必含 `Issue Number:` 行并关联 issue（先 `gh issue create` 建锚点）。push 403 = 无写权限：**先让用户去要权限，不要擅自 fork**；用户批准 fork 时才 `gh repo fork --clone=false` + `git remote add fork`（origin=上游 fetch、fork=个人 push）。
- **CLI 工具仓库**（`mrtsels/<app>-cli`）：Python CLI + install.sh + README/AGENTS，与应用仓库解耦，通过 API 通信。
- **SKILL.md**：不进应用仓库，另行编写发布（可放 CLI 仓库或技能库）。
- **共享仓库内开发计划 gitignore**：PLAN.md、references/（skill 拷贝）在共享仓中 `git rm --cached` + 加入 .gitignore，只留本地；独立 CLI 仓库才把 PLAN 入库（rail-cli 先例）。

## 派发实现子代理：工具上限是常态，父代负责收尾+验证（cupedia-cli 实测 2026-08）

Phase 拆分子代理做实现时，**子代理撞上 tool-iteration 上限是常态而非意外**（cupedia-cli 的 4 个批次中 3 次未完成收尾：1A 两次、1C 一次）。模式：

- 子代理的报告可能写着"已完成"但 git 里没有对应 commit——**永远不要信子代理的 push 自报**，收尾时父代亲自验证：`git fetch origin <branch> && git log origin/<branch> --oneline -3`，确认目标 commit 真的在远端。
- 子代理常止步于"文件写完、测试跑过"就耗尽工具预算——父代要预期自己跑收尾：`pnpm test`/`tsc --noEmit`/`lint` + `git add 具体路径` + commit + push。
- 给子代理的 context 里**直接给绝对工具路径**（如 `export PATH="$HOME/Library/pnpm:$PATH"`，pnpm 在 macOS 上 corepack 装在 `~/Library/pnpm/` 不在默认 PATH），否则子代理在非交互 shell 里找不到工具白白消耗预算。
- 子代理按 PLAN 机械实现会产生**死代码**：cupedia-cli 的 schemas.ts 6 个 parse 函数只用了 2 个、rate-limit.ts 写了但没路由调用。父代 review 时必须 grep 实际调用点（`grep -rn "checkRateLimit" src/`），按 YAGNI 删死代码——用户对 over-engineering 零容忍。
- 并行派发后子代理会互相看到对方的 untracked 文件——context 里明确"只 add 你自己的路径"（cupedia-cli 的 1D 正确只 add college-picker/wiki，没碰 1C 的 courses）。

## 薄包装侦察策略（建 API 前必做）
给已有应用加 API 层前，先 grep 现有 lib 导出与已存在路由——**大多数"新 API"只是薄包装**：

1. `search_files` 现有 lib：`^export (async )?function` 列出所有可用函数（如 `getCourses`/`getCourseReviews`/`submitCourseReview` 全套已存在 → 路由只做参数转换+错误码映射）
2. `search_files` 已有 `/api/*` 路由清单——能复用的直接转发，不重复造（如 `/api/canteens`、`/api/canteens/[id]/menu`、`/api/danmaku` 已存在）
3. **复用现有 auth，不新建 JWT**：better-auth 项目已有 session 机制与 API 守卫（`getAdminUserForApi` 等），CLI 认证走 `Authorization: Bearer <sessionToken>` 或 cookie，别自造 token 体系
4. 确认测试框架与依赖（vitest vs jest、有无 zod）——按项目现状手写校验，勿假定技术栈
5. 业务逻辑若已是纯函数（如 college-picker 的 `recommend.ts`），直接 import 调用，零 DB 依赖

> 完整实测记录（技术栈、已有路由清单、lib 函数签名、规划纪律）：`references/cupedia-cli-recon.md`

## Pitfalls

- **名称冲突**：`~/trading-agents` 是上游 fork → 开发根必须用 `~/trading-agents-skill`；先查 `ls ~`
- **双份加载**：clone 到技能侧后必须删 `~/.hermes/skills/coding/<name>` 草稿，否则 Hermes 加载两份
- **嵌套仓库**：技能侧在 `~/.agents/skills`（本身是 mrtsels/skills 的 git 仓库）内部，嵌套 clone 显示为 untracked；rail-cli 是 gitlink（submodule）——明确决定是否登记
- **description**：frontmatter ≤60 字符、触发词开头、句号结尾
- **语义改动需对源验证**：重写工作流语义（如辩论轮次）后，对照源仓库逻辑核对再 commit——fresh-eyes 审校能抓这类错误
- **计划文档入库**：别只放 `~/.hermes/plans/`，拷一份进仓库 `docs/`（rail-cli 先例：docs/PLAN.md）
- **脚本回退路径**：SKILL.md 里写的脚本路径/克隆地址要真实存在，审校子代理专门查这类"看似合理实则不存在"的路径

## Verify

- `skill_view` 显示技能来自技能侧路径且 linked files 齐全
- 两个克隆 `git status` 均干净
- `gh repo view mrtsels/<name> --json visibility,url` 确认 PUBLIC
