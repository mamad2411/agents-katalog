---
name: juanjuan-team
description: 多 Agent 对抗式协作工作流（juanjuan team）。当用户描述任务（含「做」「修」「写」「实现」「帮我」等动词 + 任务对象 + 复杂度信号）时自动触发，或显式说「juanjuan skill」「用卷卷 skill」「team up」「multi-agent」。先调 superpowers:brainstorming 头脑风暴澄清需求，再选模式（Safe/Manual/Auto/YOLO），然后建项目目录、跑 7 人 Agent 团队（leader/convener/architect/frontend/coder/reviewer/docs-researcher）、智能备份、存档记忆。核心价值是对抗式协作——多个 Agent 同步独立审核同一产出，互相挑错，避免单 Agent 认知连续性错误。**v1.6 新增：主+sub 双层对抗——每个主 Agent 必须自己独立审 + 同时派 sub-agent 平行审，最后做共识/分歧/盲点三方综合，见 references/sub-agent-review.md。7 Agent 只是默认配置，可改 prompt/数量/理论框架，见 references/customization.md。单文件任务可走 Lite 模式（6 Phase），见 references/lite-mode.md**。**v1.8 新增：真 spawn 落地——3 个独立 Agent（convener+architect+reviewer）跑 MVP 流程，验证对抗式协作真的发生了，见 §十六**。
---

# Juanjuan Team Skill

> **Juanjuan Team** — Claude Code 首个对抗式协作多 Agent Skill。
> 7 个 Agent + 11 Phase + 4 模式 + 主+sub 双层对抗审核（v1.6）。
> **v1.8 MVP：3 个独立 Agent 真 spawn 落地**（convener + architect + reviewer），验证对抗式协作真的发生了。
> 让"对抗式协作"从口头规则变成可验证的工程化机制。

## 一、触发方式

### 1.1 自动触发（推荐）

卷卷描述任务时自动触发，**三要素同时满足**：
1. **动词**：做 / 修 / 写 / 实现 / 帮我 / 搞 / 弄 / 完成 / 改
2. **+ 任务对象**：项目 / bug / 功能 / 页面 / 模块 / 脚本 / 文档
3. **+ 复杂度信号**：多文件 / 跨模块 / 架构影响 / 新功能 / 不确定（单文件单行修改不算）

例：
- "帮我修 React 项目缺失页面" → 自动触发（多文件）
- "做一个 AI 论文管理系统" → 自动触发（新功能）
- "写一个爬虫脚本" → 自动触发（新功能）
- "把 foo 改成 bar" → **不触发**（单行无复杂度）

### 1.2 显式触发

听到以下关键词时也触发：
- `juanjuan skill`（拼音带声调或兜底）
- `用卷卷 skill`
- `用自己的 skills`
- `用 juanjuan team`
- `上 ruflo team`
- `team up`（通用）
- `multi-agent`（通用）

### 1.3 不触发的场景

- 纯问答（"什么是 React"）→ 不触发
- 单文件单行修改（"把 foo 改成 bar"）→ 不触发
- 卷卷明确说"不用 juanjuan team"→ 不触发

## 二、团队配置（7 人，可改）

| # | Agent | 角色 | 跟卷卷对话 |
|---|-------|------|-----------|
| 1 | leader | 调控者 | 间接（通过 convener） |
| 2 | convener | 主对接 + 总审核 | **是**（唯一） |
| 3 | architect | 架构师（类 PM） | 否 |
| 4 | frontend | 前端工程师 | 否 |
| 5 | coder | 后端工程师 | 否 |
| 6 | reviewer | 安全审查 | 否 |
| 7 | docs-researcher | 文稿 + 浏览器调试 | 否 |

**角色详细 prompt 见 `references/role-*.md`，所有角色共享 `references/global-rules.md`。**

## 三、4 种工作模式

| 模式 | 行为 | 何时用 |
|------|------|--------|
| **Safe** | 默认全选最谨慎方案；每阶段都审核 + 卷卷确认 | 重要项目、不确定时 |
| **Manual**（原 Normal） | 团队只做头脑风暴式辅助，**完全由卷卷审核**，reviewer 否决权降级为建议 | 卷卷完全掌控时（原 Normal 改名，避免「Normal=团队正常审」的语义歧义） |
| **Auto** | 团队帮卷卷审核，遇到难抉择的转卷卷定夺 | 日常推荐 |
| **YOLO** | 全权限放给团队，hive-mind 投票决策，投票即审核，最后给卷卷结果 | 信任团队、要快速出结果 |

> ⚠️ Normal 已改名 Manual（卷卷全审），避免命名歧义。原 Normal 触发词仍兼容。

**模式选择时机（关键）**：必须在头脑风暴完成之后。流程顺序严格按 Phase 0 → Phase 1，不可颠倒。

## 四、完整工作流（11 个 Phase + Phase 0.5）

```
[Phase 0: 头脑风暴]  ← Convener 调 superpowers:brainstorming skill
  Convener 调 Skill({ skill: "superpowers:brainstorming" })
  按 SuperPower 流程：探索项目上下文 → 逐个澄清问题
  卷卷确认需求清晰后，进入 Phase 0.5
  ⚠️ 不在 Phase 0 出方案！只澄清需求
  ⚠️ brainstorming 完成后必须回到 juanjuan-team 流程进入 Phase 0.5/1
     （用 AskUserQuestion 选模式），不要继续走 brainstorming 的 design doc 流程
  ↓
[Phase 0.5: 资料查询]  ← docs-researcher 主导，预取式并行（不是真并行）
  docs-researcher 调 memory_search（threshold=0.3, limit=5）+ kimi-webbridge
  结果暂存 <项目>/.phase0.5-findings.json
  Phase 0 brainstorming 完成后，convener 读暂存结果作为 Phase 1 输入
  ⚠️ 预取式并行：Phase 0 开始时 docs-researcher 同步启动（只查不消费），结果暂存；Phase 0 完成后汇合
  ⚠️ DAG 标注：async prefetch, barrier at Phase 1 entry
  ↓
[Phase 1: 模式选择]  ← 必须在出方案之前！用 AskUserQuestion 卡片式选择
  Convener 基于 Phase 0.5 docs-researcher 的查询结果给建议
  用 AskUserQuestion 工具弹卡片：
    - Safe / Manual / Auto / YOLO
    - 每个选项带 description + preview
  卷卷点选 → 进入对应模式
  ⚠️ 为什么先选模式：模式决定「谁来出方案 + 谁来审方案 + 卷卷是否要看」
     - Safe: 卷卷审每个方案
     - Manual: 卷卷完全审（reviewer 否决权降级为建议）
     - Auto: 团队审，难抉择转卷卷
     - YOLO: 团队投票即审核，放宽阈值
  ↓
[Phase 2: 建项目目录]
  ~/项目/YYYY-MM-DD-HHmm-<任务简述>/
  git init
  ↓
[Phase 3: 方案生成]  ← 按模式出方案
  Convener + Architect 出方案 A/B/C
  ⚠️ 不管什么模式，方案必须让卷卷看到（Safe/Manual 详细看，Auto/YOLO 看摘要）
  ⚠️ 卷卷可随时打断，决定是否修改方案
  ↓
[Phase 4: 方案审核]（按模式，对抗式辩论协议）
  Safe/Manual: Architect + Reviewer + Docs-Researcher 三方独立审（卷卷可看每方意见）
  Auto: 同上 + Leader 自检介入（卷卷看汇总摘要）
  YOLO: 全权交团队投票（投票即审核，放宽阈值；卷卷看最终胜出方案）
  Convener 用加权评分公式汇总（详见 references/decision-engine.md）
  ⚠️ 加权评分先跑 LEVEL，再触发辩论（LEVEL C/D 才辩论，详见 global-rules §3.4）
  ⚠️ Convener 不做 Optimizer，Optimizer 由 architect 担任（详见 global-rules §3.5）
  ⚠️ 不管什么模式，最终选定的方案必须让卷卷看到，可打断修改
  ⚠️ Phase 4→3 回退时不重走 Phase 0/1，仅 architect 修订方案；若方案问题源于需求歧义则强制回退到 Phase 0
  ↓
[Phase 5: 设计文档]
  Docs-Researcher 写 spec
  Convener 可调 superpowers:writing-plans 辅助
  ↓
[Phase 6: 文档审核]（按模式）
  Safe/Auto/YOLO: Reviewer 单向审 docs-researcher 的文档（不是互审，docs-researcher 不审自己写的）
  Manual: 跳过，卷卷直接审
  ⚠️ Phase 6 改为 Reviewer 单向审（之前写「互审」有歧义）
  ↓
[Phase 7: 实施]
  Frontend + Coder 并行
  Coder 调 superpowers:test-driven-development 做 TDD
  出 build 错误调 /build-fix 或 build-error-resolver 子 Agent
  ⚠️ frontend + coder 依赖 architect 的接口契约，契约先定义才能并行
  ↓
[Phase 8: 代码审查]
  Reviewer 主动调 /review + /security-review（或 spawn code-reviewer subagent 作为 fallback）
  + 开语言专项子 Agent（typescript-reviewer / python-reviewer 等）并行
  Reviewer 自己做最终 verdict（不甩给子 Agent；子 Agent 只产 issue list，reviewer 合成 verdict 文本）
  ↓
[Phase 9: 智能备份]  ← 事件驱动，不在 Phase 9 单次执行
  tar.gz + git bundle
  命名: YYYY-MM-DD-HHmm-<任务简述>.tar.gz
  位置: 项目目录内 .backups/
  每日上限 3 次（YOLO 模式 6 次）
  详见 references/backup-script.sh
  ⚠️ 备份改为事件驱动：Reviewer verdict=pass 事件触发（不在 Phase 9 单次执行）
  ⚠️ Phase 9 位置改为「最终归档备份」（项目完成时的一次性完整备份）
  ⚠️ 计数器存 <项目>/.backups/.daily-counter.json，强制备份需卷卷二次确认 + force=true
  ⚠️ git bundle 前用 git filter-repo 扫 history 排除 secrets（避免泄露 .env/*.pem 等已 commit 的文件）
  ↓
[Phase 10: 存记忆]
  Docs-Researcher 把项目经验存入 ruflo memory
  内容: 任务简述 + 最终方案 + 踩坑 + 团队配置 + 模式选择
  ⚠️ memory_store 失败时不阻塞流程，convener 提示卷卷「记忆未存档」
  ↓
[Phase 11: 汇报归档]
  Convener 给卷卷最终结果
```

## 五、Phase 依赖图（DAG）

```
                    ┌──→ Phase 0 (头脑风暴，Convener)
                    │     ↓
   (并行启动) ───────┤   [需求清晰]
                    │     ↓
                    └──→ Phase 0.5 (资料查询，docs-researcher) ──┐
                          ↓                                       │
                       [两者汇合]                                 │
                          ↓                                       │
                       Phase 1 (模式选择) ←──────────────────────┘
                          ↓
                       Phase 2 (建目录)
                          ↓
                       Phase 3 (方案生成) ←─────┐
                          ↓                    │
                       Phase 4 (方案审核) ─────┤ (回退：reviewer 发现方案问题)
                          ↓                    │
                       Phase 5 (设计文档) ←───┘
                          ↓
                       Phase 6 (文档审核) ←─────┐
                          ↓                    │ (回退：reviewer 发现文档问题)
                       Phase 7 (实施: frontend + coder 并行) ──┤
                          ↓                    │
                       Phase 8 (代码审查) ─────┘ (回退：reviewer 发现代码问题)
                          ↓
                       Phase 9 (事件驱动备份 + 最终归档)
                          ↓
                       Phase 10 (存记忆)
                          ↓
                       Phase 11 (汇报归档)
```

**Phase 0 + 0.5 预取式并行**：Convener 跑 brainstorming 的同时，docs-researcher 后台预取 memory（结果暂存 .phase0.5-findings.json，Phase 0 完成后汇合，不是真并行）
**Phase 7 内并行**：frontend + coder（依赖 architect 接口契约先定义）
**Phase 4/6/8 三方并行审核**：architect + reviewer + docs-researcher 独立审（global-rules §4.1）
**不可跳过**：Phase 0（头脑风暴）、Phase 4（审核）、Phase 8（代码审查）

## 六、项目目录强制要求

**禁止**在根目录直接操作。必须建在：

```
~/项目/YYYY-MM-DD-HHmm-<任务简述>/
```

例：
```
~/项目/2026-08-03-1430-kaoyan-english-fix-login-bug/
```

git 仓库位置（默认选项 A）：
- **A**：项目目录内（`~/项目/2026-08-03-1430-.../.git/`）
- **B**：项目目录的上一级（`~/项目/.git/`）

## 七、智能备份机制

### 触发条件（满足任一即备份）
1. 单次任务内 git diff 累计 > 200 行
2. 单次任务内文件改动数 > 5 个（git tracked，含新增/修改/删除）
3. convener 跟卷卷确认「阶段性完成」时
4. reviewer 完成审查时（Reviewer verdict=pass 事件触发）
5. 卷卷显式说「备份一下」/「存档」

### 备份内容
- **tar.gz**：整个项目目录（默认排除 dist/build/node_modules/.git/secrets）
  - secrets 黑名单：`.env`、`.env.*`、`*.pem`、`*.key`、`*.crt`、`id_rsa`、`id_ed25519`、`.ssh/`、`.npmrc`、`.pypirc`、`.aws/credentials`、`.gnupg/`、`*.keystore`、`*.jks`、`*.kdbx`、`*.p12`、`*.pfx`、`credentials.json`、`.htpasswd`、`.netrc`、`.docker/config.json`、`.kube/config`、`*token*.json`、`*secret*.json`
  - 兜底：任何文件名含 `token` / `secret` / `credential` / `key` 的文件默认排除
  - 构建产物默认排除，仅在显式 `--full` 时包含
- **git bundle**：完整 git 历史（**必须先扫 history 排除 secrets**）
  - 命令：`git bundle create .backups/YYYY-MM-DD-HHmm-<任务>-git-bundle.bundle --all`
  - ⚠️ bundle 前用 `git filter-repo` 或扫描 `git rev-list --all -- '**/.env' '**/*.pem' '**/*.key'`，确认 history 无 secrets 再 bundle
  - 若 history 含 secrets：禁止 bundle，先清理 history 或改用 `git bundle --not $(git rev-list --all -- secrets_files)`

### 备份命名格式
```
YYYY-MM-DD-HHmm-<任务简述>.tar.gz
YYYY-MM-DD-HHmm-<任务简述>-git-bundle.bundle
```

### 备份位置
- 默认：`<项目目录>/.backups/`
- 可选：`~/项目/.backups/`（上一级统一备份库）

### 频率控制
同一项目内同一日最多备份 3 次（本地时区）。超出时 convener 提示：「今日备份已达 3 次上限，是否强制再备份？」

## 八、记忆机制

### 任务启动时自动读取（Phase 0）
docs-researcher 自动调 `memory_search`：
```
query: <任务关键词>
threshold: 0.3
limit: 5
```
匹配到的历史项目经验注入 convener 对话上下文。

### 任务完成时存档（Phase 10）
docs-researcher 存入 ruflo memory：
```yaml
key: <项目目录名>
namespace: project
value: |
  任务简述: <一句话描述>
  最终方案: <选定的方案 + 关键决策>
  踩坑: <实施过程中遇到的问题 + 解决方法>
  团队配置: <本次实际用的 Agent 角色组合>
  模式选择: <Safe/Manual/Auto/YOLO + 是否阶段性切换>
  项目路径: ~/项目/YYYY-MM-DD-HHmm-.../
tags: [skill, juanjuan-team, <技术栈标签>]
provenance_type: agent_output
```

## 九、Skill 文件结构

```
~/.claude/skills/juanjuan-team/
├── SKILL.md                          # 本文件（主入口）
├── references/
│   ├── global-rules.md               # 全局共享规则（10 条硬约束 + 模式冲突处理）
│   ├── role-leader.md                # 7 个角色完整 prompt
│   ├── role-convener.md
│   ├── role-architect.md
│   ├── role-frontend.md
│   ├── role-coder.md
│   ├── role-reviewer.md
│   ├── role-docs-researcher.md
│   ├── decision-engine.md            # 决策引擎（对抗式辩论 + 加权评分）
│   ├── state-machine.md               # 任务状态机
│   ├── skill-allocation.md           # 角色技能分配矩阵
│   ├── agent-commands.md             # Agent 命令规范（跨平台兼容）
│   ├── customization.md              # 灵活配置指南（改 prompt/数量/理论）
│   ├── message-protocol.md           # ★ Agent 间通信协议（文件消息 + MCP + SendMessage）
│   ├── fault-tolerance.md            # ★ 容错机制（convener 单点 + 失联 + 模式切换 + 并发隔离）
│   ├── lite-mode.md                  # ★ Lite 模式（单文件任务走 6 Phase 精简流程）
│   ├── domain-checklists.md          # ★ 9 信号组 + 领域 checklist + 反群体思维 + HTML 报告（可选）
│   └── backup-script.sh               # 备份脚本
└── scripts/
    ├── install.sh                    # ★ 一键安装（clone + symlink 到 ~/.claude/skills/）
    ├── swarm-spawn.sh                 # 7 人 agent spawn 脚本
    └── backup-check.sh                # 备份触发条件检查
```

★ = v1.3 新增

## 十、MCP 工具调用路径

本 skill 通过 Claude Code 的 MCP 工具调用 Ruflo（已连接，验证可用）：

| 工具 | 用途 | 调用时机 |
|------|------|---------|
| `mcp__claude-flow__swarm_init` | 初始化 7 人 swarm | Phase 2 建目录后 |
| `mcp__claude-flow__agent_spawn` | spawn 单个 Agent | Phase 2 后，并行 spawn 7 人 |
| `mcp__claude-flow__agent_execute` | 给 Agent 派任务 | Phase 3-11 各 Phase |
| `mcp__claude-flow__memory_search` | 查历史经验 | Phase 0 头脑风暴 |
| `mcp__claude-flow__memory_store` | 存项目经验 | Phase 10 存记忆 |
| `mcp__claude-flow__swarm_status` | 查 swarm 状态 | 任意 Phase 监控 |
| `mcp__claude-flow__hive-mind_consensus` | YOLO 模式投票 | Phase 4 冲突处理 |

## 十一、错误处理

| 场景 | 处理 |
|------|------|
| ruflo MCP 不可用 | convener 提示「MCP 不可用，降级为本地 JSON 模式」（见 fault-tolerance.md §五），**流程继续不阻塞** |
| 记忆库查询失败 | docs-researcher 报告「无历史经验」，继续流程 |
| 备份失败（磁盘满） | convener 提示并询问是否清理旧备份或换位置 |
| Agent 间无法达成共识 | Leader 自检 → 明显情况定夺，技术性选择转卷卷 |
| 项目目录已存在 | convener 询问「追加到现有项目还是新建带后缀的目录」 |
| git 仓库已存在 | convener 询问「复用现有 git 历史 还是 重新 init」 |
| 模式切换冲突 | 以最新一次模式选择为准，convener 通知团队 |
| 记忆库写入失败 | convener 提示卷卷「记忆未存档，请检查 ruflo MCP」，流程继续不阻塞 |

## 十二、与 SuperPower brainstorming 的衔接

- brainstorming skill 完成需求澄清后，convener 主动询问「这次要不要上 juanjuan team？」
- 或者卷卷主动说「上 juanjuan team」/「用 ruflo 跑这个」
- 衔接点：brainstorming 输出的需求 spec → juanjuan-team 的 Phase 0 输入

## 十三、Claude Code 内置命令的使用口径

> ⚠️ 之前的表述「禁用」有歧义。明确口径：

**最新版 Claude Code 把 `/review`、`/security-review`、`deep search` 等内置命令改成「必须手动 `/` 调用才生效」（不是禁用，是不再自动触发）**。本 skill 的 Agent 在对应场景必须**主动用 `/` 前缀调用**，否则不生效。

| 命令 | 状态 | 本 skill 使用方式（按优先级） |
|------|------|------------------------------|
| `/review` | 需手动 `/` 调用 | ① Reviewer 主动调 `/review`；② 失败则 spawn `code-reviewer` subagent |
| `/security-review` | 需手动调用 | ① Reviewer 主动调 `/security-review`；② 失败则 spawn `security-reviewer` subagent |
| `deep search` | 需手动调用 | docs-researcher 用 `memory_search` + `kimi-webbridge` skill |

> ⚠️ 优先级：先试 `/` 命令，失败才 spawn subagent fallback，不要并列调用

调用方式（convener 在 Phase 4/6/8 用）：
```
Reviewer 主动调: /review + /security-review
或 spawn subagent 作为 fallback:
Agent({ description: "reviewer 审 <目标>", prompt: "<reviewer 角色 prompt + 被审目标>", subagent_type: "code-reviewer" })
```

## 十四、未来扩展（YAGNI，本次不做）

- 全局自动读取记忆：配 PreToolUse hook
- 跨项目记忆聚合分析
- Web UI 可视化聊天日志
- 支持 GitLab / Bitbucket 等非 GitHub 仓库
- 团队配置热加载（运行中调整角色）
- JAAOS 三引擎融合架构（Ruflo + Hermes Kanban + AgentTeams）

## 十五、自检与进化（v1.5 新增，v1.6 扩展）

### 15.1 何时自检

- 每次大改 skill 后（v1.x → v1.(x+1)）
- 每月一次定期自检
- 怀疑对抗式协作失效时

### 15.2 怎么自检

跑 `scripts/meta-verify.sh <项目目录>` 验证 6 项（v1.6 新增 MV-6）：

| 检查项 | 验证目标 |
|--------|---------|
| MV-1 独立审核证据 | Phase 4/6/8 三方真的独立产出意见 |
| MV-2 并行调用证据 | convener 真的并行（不是串行）调用三方 |
| MV-3 模式切换日志 | 模式切换真的 Phase 边界原子化 |
| MV-4 记忆闭环 | Phase 10 存的 memory Phase 0.5 能查到 |
| MV-5 备份触发 | reviewer pass 事件真的触发备份 |
| MV-6 主+sub 双层对抗（v1.6） | 主 Agent 自己审 + sub-agent 平行审 + 综合分类（共识/分歧/盲点）|

任何一项失败 → 回到 `docs/superpowers/specs/YYYY-MM-DD-juanjuan-team-self-audit-design.md` 修订 → 重跑。

### 15.3 进化原则

1. **系统性问题 > 具体缺陷**：修缺陷不修系统 = 下次还会冒出来
2. **可观测 > 自觉**：规则要变成脚本能验证的
3. **闭环 > 单向**：存的记忆要能查出来才算闭环
4. **借鉴 > 自创**：先看 hermes-studio / agent-review-panel / ChatGPT JAIT 有没有现成方案
5. **YAGNI**：不在 evolution-roadmap 上的功能不做
6. **反模式驱动**：每次发现的缺陷归纳成反模式（`references/anti-patterns.md`），避免重蹈覆辙
7. **主+sub 平行对抗**（v1.6 新增）：主 Agent 不能只做汇总员，必须自己独立审，与 sub-agent 平行产出，盲点必须披露

### 15.4 可观测性（v1.5 新增）

- **run_id**：每个 Phase 产生一个 `run-<phase>-<timestamp>-<rand4>`，绑定该 Phase 所有消息和产出物（详见 `references/observability.md`）
- **.phase-trace.json**：记录所有 Phase 执行轨迹
- **.phase-summary.md**：rolling summary，每 Phase 结束 docs-researcher 更新，下次 Phase 0.5 优先读此文件
- **message-protocol.md 加 run_id 字段**：所有 `.msg/*.json` 必须含 `run_id`

### 15.5 主+sub 双层对抗（v1.6 新增）

每个主 Agent 在 Phase 4/6/8 审核时：
1. **主 Agent 自己独立审**：产 self_findings（不能只做汇总员）
2. **同时派 sub-agent 平行审**：时间差 ≤ 1s（避免锚定效应）
3. **综合分类**：verdict 必须含 `consensus / divergence / blind_spots` 三类
4. **盲点披露**：主 Agent 采纳 sub-agent 补的 issue 时，必须明示"我漏了 X"

详见 `references/sub-agent-review.md`。元验证 MV-6 检查此机制。

### 15.6 v1.6 文件结构更新

```
~/.claude/skills/juanjuan-team/
├── SKILL.md                          # v1.6 加 §15.5 主+sub 双层对抗
├── docs/                              # v1.6 新增
│   ├── getting-started.md             # ★ 5 分钟上手
│   └── for-non-developers.md          # ★ 非技术用户指南
├── references/
│   ├── global-rules.md               # v1.5 加第 11 条 run_id 必填
│   ├── role-*.md                     # 7 个角色
│   ├── decision-engine.md            # v1.5 修 D-11/D-12
│   ├── state-machine.md
│   ├── skill-allocation.md
│   ├── agent-commands.md             # v1.5 修 D-3/D-4
│   ├── customization.md
│   ├── message-protocol.md           # v1.5 加 run_id 字段
│   ├── fault-tolerance.md            # v1.5 修 D-9
│   ├── lite-mode.md
│   ├── domain-checklists.md
│   ├── backup-script.sh              # v1.5 修 D-5/D-6
│   ├── meta-verification.md          # v1.5 新增，v1.6 加 MV-6
│   ├── observability.md              # v1.5 新增
│   ├── anti-patterns.md              # v1.5 新增（v1.6 加 AP-13~17）
│   ├── evolution-roadmap.md          # v1.5 新增
│   └── sub-agent-review.md           # ★ v1.6 新增：主+sub 双层对抗规范
└── scripts/
    ├── install.sh
    ├── swarm-spawn.sh                # v1.5 修 D-1/D-2
    ├── backup-check.sh
    ├── create-project.sh
    ├── heartbeat-check.sh
    ├── hook-enforce.sh               # v1.5 修 D-7/D-8
    ├── lite-check.sh
    ├── send-msg.sh
    ├── meta-verify.sh                # v1.5 新增，v1.6 加 MV-6 检查
    ├── e2e-dry-run.sh                # v1.5 新增
    └── memory-roundtrip-test.sh      # v1.5 新增
```

### 15.7 v1.6 自检结果

- 新增 sub-agent-review.md（主+sub 平行对抗 + 三方综合规范）
- 新增 MV-6 元验证（主 Agent self + sub 平行 + 盲点披露）
- 新增 5 条反模式（AP-13~17：形式主义 / 串行 / 汇总员 / 悄悄采纳 / 锚定）
- 新增 docs/ 目录（小白指南 + 非技术用户指南）
- README 顶部加快速入门链接

### 15.8 v1.7 自审查与修复

对 v1.6 自审发现 12 个缺陷（V16-1 ~ V16-12），全部修复：

**critical/major**:
- V16-1 sub-agent 数量爆炸未设上限 → 加 §11 复杂度感知配置（Lite/Medium/Complex 三档）
- V16-2 MV-6 时间戳逻辑 bug → 修正为 `sub_started_at - self_started_at >= -1`，并加 anchor_risk 检查
- V16-3 sub-agent 失败 fallback 路径不明 → §8 三层失败场景（sub 失败 / 主失败 / 都失败）
- V16-4 盲点披露无强制字段 → §2 第 4 条规范 acknowledgement 必须含"我漏了"等关键词，MV-6 检查
- V16-5 共识/分歧判定标准模糊 → §2.1 issue 粒度规范（文件+函数+类别三要素对齐）
- V16-6 sub-agent 能否 spawn 子 sub-agent → §2 第 9 条硬规则禁止，AP-18 反模式

**minor**:
- V16-7 leader 的 sub-agent 形同虚设 → 移除，改为 architect peer review，AP-19 反模式
- V16-8 getting-started.md 13 步与 SKILL.md 11 Phase 不一致 → 重写对齐到 11+0.5
- V16-9 AP-17 时间戳描述过严 → 修正语义为发起时间差
- V16-10 sub-agent token 无监控 → §4 sub-call 加 token_used 字段
- V16-11 for-non-developers.md 没提 sub-agent → 加"v1.6 新增：双层对抗"章节
- V16-12 hermes-studio run_id 启发未完整 → §5 加 tool_call_id 字段（借鉴 hermes-studio 配对机制）

**v1.7 反模式新增**: AP-18（sub-agent 无限生长）+ AP-19（leader sub-agent 形同虚设）

**v1.7 元验证增强**: MV-6 检查 acknowledgement 字段内容规范性 + anchor_risk 修正

## 十六、v1.8 MVP：真 spawn 落地

### 16.1 背景

v1.0~v1.7 全是"剧本版"——Claude 一个人扮演 7 个角色，没有真 spawn 过独立 Agent。v1.8 做 MVP：真 spawn 3 个独立 Agent（convener + architect + reviewer），跑一个小任务，验证对抗式协作真的发生了。

### 16.2 关键认知（Claude 纠偏）

**Skill 是 markdown 指令文件，不是代码项目。** 没有 spawn 的 JS/bash API 给你调用。Skill 能做的是：
1. 在 `~/.claude/agents/juanjuan-*.md` 定义角色文件（带 YAML frontmatter）
2. 在 SKILL.md / role-convener.md 里写自然语言指令："Phase 2 时，convener 调用 Agent 工具，subagent_type 填 juanjuan-architect，prompt 参数填入..."
3. Claude 扮演 convener 时，读到这条指令，自己会去调用 Agent 工具——调用发生在 Claude Code 运行时内部

### 16.3 v1.8 Agent 定义文件（不是字符串拼接）

3 个独立文件（v1.9 扩到 7 个）：

| 文件 | 角色 | 由谁 spawn |
|------|------|-----------|
| `~/.claude/agents/juanjuan-convener.md` | convener（主会话） | 卷卷启动 skill 时自动 |
| `~/.claude/agents/juanjuan-architect.md` | architect | convener 在 Phase 2 spawn |
| `~/.claude/agents/juanjuan-reviewer.md` | reviewer | convener 在 Phase 3 spawn |

每个文件 YAML frontmatter（name/description/tools/model）+ 正文（role 完整定义）。

### 16.4 v1.8 MVP 6 Phase 流程（不是 11 Phase）

```
[Phase 0] 需求 — convener 跟卷卷对话，整理到 .shared/requirements.md
  ↓
[Phase 1] 建上下文目录 — 见 §16.5 目录协议
  ↓
[Phase 2] spawn architect — convener 调 Agent 工具，architect 产 design.md + reasoning.md
  ↓
[Phase 3] spawn reviewer 盲审 — convener 调 Agent 工具，reviewer 只读 design.md，产 review.json
  ↓
[Phase 4] 综合决策 — convener 读 design.md + review.json，写 decision.md
  ↓
[Phase 5] audit — convener 调 Agent 工具 spawn audit-agent，产 audit-report.md
```

### 16.5 目录协议

每个 v1.8 任务在 `~/项目/YYYY-MM-DD-HHmm-<任务简述>-<rand4>/` 下建：

```
.shared/
  requirements.md              # convener 整理卷卷需求
.architect/
  public/
    design.md                  # architect 公开决策 + 一句话技术理由
  private/
    reasoning.md               # architect 私有推理（reviewer 绝对不能读）
.reviewer/
  reviews/
    design-review.json         # reviewer 盲审产出
.convener/
  decision.md                  # convener 综合决策
.audit/
  events.jsonl                 # 每次 spawn 都追加一行（schema 见 references/audit-event-schema.md）
  audit-report.md              # Phase 5 audit-agent 产出
```

### 16.6 盲审硬约束（最核心）

spawn reviewer 时，convener 必须：
- ✅ allowed_files: `.shared/requirements.md` + `.architect/public/design.md`
- ❌ forbidden_files: `.architect/private/reasoning.md`

reviewer 的 prompt 里**绝对不能**出现 reasoning.md 的任何原文片段。事后审计通过 `.audit/events.jsonl` 的 `prompt_full` 字段检查（schema 见 `references/audit-event-schema.md`）。

### 16.7 design.md 内容规范

允许「结论 + 一句话技术理由」：
- ✅ 「采用 PostgreSQL，因为事务一致性保证任务状态更新」
- ✅ 「API 用 RESTful 风格，符合卷卷现有技术栈」

禁止策略性语言：
- ❌ 「一开始考虑 MongoDB，但怕 reviewer 攻击，所以选 PostgreSQL」
- ❌ 「对比过 X 方案，放弃了，因为……」
- ❌ 「担心 reviewer 会……」

**判断标准**：只允许陈述"选了什么 + 为什么这个技术特性匹配需求"，禁止提及"还考虑过什么别的选项、为什么没选、对 reviewer 的预测"。

检测到策略性语言：**打回给 architect 重写**（不是 convener 清洗，避免污染链前移），最多 2 次。

### 16.8 Spawn 顺序（不并行）

```
Step 1: convener 存在（主会话）
Step 2: spawn architect → 产 design.md + reasoning.md
Step 3: spawn reviewer → 读 design.md 产 review.json
Step 4: convener 综合 → decision.md
Step 5: spawn audit-agent → audit-report.md
```

v1.8 验证的是**隔离**，不是并行。并行留给 v1.9。

### 16.9 v1.8 不做（YAGNI）

- 不做 7 Agent（v1.9）
- 不做 sub-agent（v1.9）
- 不做对话模式辩论（v1.9）
- 不做 leader 独立角色（convener 兼任）
- 不做跨平台抽象（v1.9）
- 不做 11 Phase（v1.8 用 6 Phase MVP）
- 不做成本统计（v1.9）

### 16.10 验收标准

v1.8 跑成功的标志（4 条都要满足）：

1. **独立 Agent 真被调用**：`.audit/events.jsonl` 有 architect 和 reviewer 各 1 条 spawn 事件 + 各 1 条 complete 事件
2. **信息隔离成立**：reviewer 的 spawn prompt_full 里不含 reasoning.md 的任何 50+ 字符原文片段
3. **reviewer 发现真问题**：review.json 里至少 1 个 issue 是 architect 漏掉的真实问题（不是凑数）
4. **convener 综合决策**：decision.md 明示采纳了哪些 reviewer 意见、不采纳哪些、理由

### 16.11 v1.8 Commit 路线

- **Commit 0**（本次）：目录协议 + 3 个 agent 定义文件 + audit-event schema ✓
- **Commit 1**：真 spawn 跑 TODO list 数据结构设计任务
- **Commit 2**：生成 audit-report.md，验收 4 条标准

### 16.12 v1.9 优先级（v1.8 跑通后再做）

1. 扩到 7 Agent（加 leader/coder/frontend/docs-researcher）
2. 加 sub-agent（每个主 Agent 派 sub）
3. token 调度（模型分层）
4. 跨平台抽象层（最后做）

### 16.13 最终成功标准（v1.9+）

**不**追求"7 人团队"，**只**追求："3 个 Agent 真的比 1 个 Agent 可靠"。

v1.8 先证明机制能跑通、隔离是真的。统计对比（跑 10 个任务看错误率差异）留到 v1.9 有了稳定 3-Agent 版本之后再做。
