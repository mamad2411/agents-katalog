---
name: init-dev-harness-agents
description: Initializes code-dev multi-agent Harness (architect/orchestrator/executor/reviewer/devops), workflows, triage-routing, FAQ, progress-tracking, experience-summary, and collaboration-sync. Invoke on `/init-dev` or when setting up code-development agent collaboration.
---

# Init Dev Harness Agents — 代码开发多 Agent 协作框架初始化

## Overview

为代码开发项目搭建 AI Agent 协作框架（Harness Engineering），定义开发专用 Agent 角色、工作流、通信协议、治理规则，以及**协同进度跟踪、经验总结、工作状态可视化**等工程化管理基础设施。

**核心理念：软件是工程，不是代码**。Harness 不是单节点的文档集合，而是一个有机的协同系统——角色之间通过标准化的交接、同步、跟踪机制形成闭环，确保工作状态透明、经验可追溯、进度可量化。

**核心定位（重要区分）**:
- **本 Skill（Harness）= 定义角色 + 工作流程 + 协同机制**：每个工作流由若干"工作节点"组成，规定角色在什么阶段做什么、何时交接、如何同步状态
- **其他 Skills = 具体工作步骤**：角色在执行某个工作节点时，优先调用已有 skill 完成具体操作（怎么做）
- **关系**：Harness 是"骨架"（角色 + 流程 + 节点 + 协同），Skills 是"肌肉"（每个节点上的具体执行步骤）
- **原则**：角色不重复发明工作步骤，能调用 skill 就调用 skill；Harness 不复制 skill 内容，只引用与编排

**核心原则**:
- 每个 Agent 角色职责单一、输入输出契约明确、通信协议标准化
- 架构师把控全局，编排者按工作类型路由到对应角色
- 工作流先识别"这是什么工作"，再转发给匹配角色；无匹配则创建新角色/工作流后执行
- 每个角色配备 FAQ，避免重复犯错
- 每个工作节点必须标注"优先调用的 skill"，避免角色自行实现已有步骤
- **每次用户交互必走自我迭代流程**：collect → analyze → sink → iterate，每个角色都参与实践（非 orchestrator 独占）
- **已初始化不覆盖，合并增强**：检测到已有 Harness 配置时按合并策略增强，保留已有能力与历史沉淀
- **小步快跑，大周期沉淀**：交互级轻量迭代（小步快跑，每轮做最小改进）+ 周期级深度沉淀（大周期，定期回顾提炼最佳实践与模式）
- **每个角色积累最佳实践**：每个角色维护自身最佳实践库，区别于 FAQ（错误沉淀），最佳实践是正向经验沉淀
- **协同进度透明化**：通过进度跟踪文件、交接记录、同步日志实现多角色工作状态可视化
- **经验可追溯**：通过经验总结文件、跨角色 lessons learned 实现知识持续积累与复用

## When to Use

- 新代码项目需要多 Agent 开发协作框架
- 已有代码项目接入 Harness Engineering（开发模式）
- `/init-dev` 命令触发
- 需要定义开发 Agent 角色分工与协作流程

## Boot Agents 流程

收到 `/init-dev` 指令后，执行以下步骤：

### Step 1: 扫描项目

```
扫描内容：
├── package.json / pom.xml / Cargo.toml → 技术栈
├── src/ / app/ / lib/ → 目录结构
├── agents/ → 现有 agent 结构（如有）
├── .git/ → 是否 git 仓库
├── existing harness.yaml → 是否已有 Harness 配置
└── docs/ → 已有文档
```

### Step 2: 生成 Harness 配置

创建 `agents/harness.yaml`，定义开发专用 Agent 角色：

```yaml
name: {项目名}-harness
version: 1.0.0

agents:
  - id: architect
    role: architect.md
    capabilities: [architecture-design, module-split, interface-definition, tech-decision]
    protocol: direct

  - id: orchestrator
    role: orchestrator.md
    capabilities: [task-decomposition, work-triage, context-management, agent-routing]
    protocol: direct

  - id: executor
    role: executor.md
    capabilities: [code-generation, file-operation, command-execution]
    protocol: direct
    instances: 3

  - id: reviewer
    role: reviewer.md
    capabilities: [code-review, security-scan, quality-check]
    protocol: direct

  - id: devops
    role: devops.md
    capabilities: [start-stop-scripts, monitoring-setup, deployment, infra-automation]
    protocol: direct

workflows:
  - name: standard-dev
    steps:
      - agent: orchestrator
        action: triage          # 先识别工作类型
        skill: null             # 路由判断，无需 skill
      - agent: orchestrator
        action: route           # 路由到匹配角色；无匹配则创建
        skill: null
      - agent: executor
        action: implement
        skill: subagent-driven-development  # 逐任务实施
        parallel: true
      - agent: reviewer
        action: review
        skill: requesting-code-review       # 代码审查
      - agent: executor
        action: fix
        skill: receiving-code-review        # 接收审查反馈并修复
        condition: review.failed

  - name: architecture-first
    steps:
      - agent: architect
        action: design          # 应用/模块拆分、接口与类职责
        skill: codebase-design                # 深模块设计
      - agent: orchestrator
        action: decompose
        skill: writing-plans                  # 实施计划
      - agent: executor
        action: implement
        skill: subagent-driven-development
      - agent: reviewer
        action: review
        skill: requesting-code-review

  - name: devops-ops
    steps:
      - agent: devops
        action: create-scripts  # 启停脚本
        skill: null             # 按项目技术栈编写
      - agent: devops
        action: setup-monitoring
        skill: null

  - name: debug-flow
    steps:
      - agent: orchestrator
        action: triage
        skill: null
      - agent: executor
        action: diagnose
        skill: systematic-debugging          # 系统化调试
      - agent: executor
        action: fix
        skill: null
      - agent: reviewer
        action: review
        skill: requesting-code-review

  - name: prd-to-code
    steps:
      - agent: orchestrator
        action: clarify
        skill: brainstorming                  # 需求澄清
      - agent: orchestrator
        action: plan
        skill: writing-plans
      - agent: executor
        action: implement
        skill: subagent-driven-development
      - agent: reviewer
        action: review
        skill: requesting-code-review
      - agent: executor
        action: verify
        skill: verification-before-completion # 完成前验证

communication:
  format: json
  timeout_ms: 30000
  retry: 3
```

### Step 3: 生成 Agent 角色定义

创建 `agents/roles/` 目录，为每个角色生成提示词模板：

**architect.md** — 架构师（全局把控）:
- 职责：项目技术架构设计、应用与模块拆分、接口和类的职责把控
- 职责：确保项目符合性能、可扩展性、安全性要求
- 输入：用户需求 / 技术约束
- 输出：架构设计文档 / 模块拆分方案 / 接口契约
- 优先调用 skill：`codebase-design`（深模块设计）、`design-an-interface`（接口设计）

**orchestrator.md** — 编排者（路由中枢）:
- 职责：任务分解、上下文管理、**工作类型识别与 Agent 路由**
- 职责：收到工作后先判断"这是什么工作"，转发给匹配角色处理
- 职责：若无匹配角色或工作流，创建新的角色/工作流后执行
- 输入：用户需求 / 上游 Agent 输出
- 输出：任务分配指令 / 路由决策
- 优先调用 skill：`writing-plans`（实施计划）、`brainstorming`（需求澄清）

**executor.md** — 执行者:
- 职责：代码生成、文件操作、命令执行
- 输入：任务分配指令
- 输出：代码变更 / 执行结果
- 优先调用 skill：`subagent-driven-development`（逐任务实施）、`tdd`/`test-driven-development`（测试驱动）、`systematic-debugging`（调试）、`receiving-code-review`（修复审查反馈）

**reviewer.md** — 评审者:
- 职责：代码审查、安全扫描、质量检查
- 输入：代码变更
- 输出：审查报告
- 优先调用 skill：`requesting-code-review`、`TRAE-code-review`、`TRAE-security-review`、`review`

**devops.md** — DevOps:
- 职责：创建启停脚本、监控脚本、必要的监控配置
- 职责：部署自动化、基础设施管理
- 输入：部署需求 / 运维任务
- 输出：脚本 / 监控配置 / 部署产物
- 优先调用 skill：`setup-pre-commit`（提交钩子）、`git-guardrails-claude-code`（git 安全）、`verification-before-completion`（部署前验证）

### Step 4: 生成工作流定义

创建 `agents/workflows/` 目录，定义多 Agent 协作流程：

- `standard-dev.yaml` — 标准开发流程（triage → route → implement → review → fix）
- `architecture-first.yaml` — 架构优先流程（架构师先行 → 拆解 → 实施 → 评审）
- `code-review.yaml` — 代码审查流程
- `prd-to-code.yaml` — PRD → 代码流程
- `debug-workflow.yaml` — 调试协作流程
- `devops-ops.yaml` — 运维操作流程（启停脚本 / 监控）

**工作流 = 工作节点序列**：每个 step 是一个工作节点，节点上标注 `skill` 字段表示该节点优先调用的 skill。`skill: null` 表示该节点为角色内禀职责（如路由判断、脚本编写），无需调用外部 skill。

**工作流类型**：
- **顺序（sequential）**：Agent 按序执行
- **并行（parallel）**：多个 Agent 同时执行
- **辩论（debate）**：多 Agent 讨论达成共识
- **评审（review）**：执行 → 评审 → 修复循环
- **路由（triage-route）**：先识别工作类型，再转发给匹配角色

**节点-skill 映射原则**：
- 工作流只定义"做什么、谁来做、何时做"，不定义"怎么做"
- "怎么做"由该节点引用的 skill 提供；角色不重复实现 skill 已覆盖的步骤
- 若某节点找不到对应 skill，标注 `skill: null` 并在角色定义中说明执行方式
- 后续若新增覆盖该节点的 skill，回写更新工作流的 `skill` 字段

### Step 5: 生成角色 FAQ

创建 `agents/faq/` 目录，为每个角色生成 FAQ，记录常见错误与规避方式：

- `architect.faq.md` — 架构设计常见反模式、过度设计陷阱
- `orchestrator.faq.md` — 路由误判、任务遗漏、上下文丢失
- `executor.faq.md` — 代码生成常见错误、契约不一致
- `reviewer.faq.md` — 审查遗漏项、误报漏报
- `devops.faq.md` — 脚本兼容性、监控盲区

**FAQ 维护原则**：每次角色执行中发现的重复错误，必须回写到对应 FAQ，避免再次发生。

### Step 6: 生成 Harness AGENTS.md

按以下模板生成：

```markdown
# {项目名} — Harness 工程

## 项目定位
[一句话]

## Agent 架构拓扑
（引用 harness.yaml 中的角色关系）
- architect → 全局架构把控
- orchestrator → 工作类型识别与路由
- executor → 代码实施
- reviewer → 质量评审
- devops → 运维与监控

## 协作流程
（引用 agents/workflows/）
- 标准开发：triage → route → implement → review → fix
- 架构优先：architect → decompose → implement → review
- 运维操作：devops → scripts / monitoring

## 治理规则
### 角色边界
### 通信协议
### 错误处理
### 工作路由规则（先识别工作类型，再转发；无匹配则创建）

## FAQ 入口（负向错误沉淀）
（引用 agents/faq/，每个角色避免重复犯错）

## 最佳实践入口（正向经验沉淀）
（引用 agents/best-practices/，每个角色积累最佳实践）

## 自我迭代与沉淀（双节奏：小步快跑 + 大周期）
- 演进机制配置：`agents/evolution/evolution.yaml`
- 跨角色经验：`agents/evolution/lessons-learned.md`
- 可复用模式：`agents/evolution/patterns.md`（大周期提炼）
- 角色变更日志：`agents/evolution/role-changes.md`
- 工作流变更日志：`agents/evolution/workflow-changes.md`
- 小步快跑：每次用户交互必走，轻量迭代
- 大周期沉淀：每 N 轮交互（默认 10）或 `/harness-evolve` 触发深度回顾

## 协同进度与经验（工作状态可视化）
- 全局进度看板：`agents/sync/progress.yaml`（所有角色共享）
- 操作时间线：`agents/sync/sync-log.md`（所有角色操作记录）
- 交接记录：`agents/sync/handoffs/`（角色间任务传递）
- 经验总结：`agents/sync/experience-summary.md`（可迁移工程洞察）
- 协同指南：`agents/sync/README.md`（协同工作区使用说明）

## 交互记录
用户询问与变更记录存放于 `docs/interaction-changes/`，按日期归档。

## Skill 依赖
| Skill | 用途 |
|---|---|
| init-dev-harness-agents | Harness 框架初始化 |
| brainstorming | 需求澄清 |
| writing-plans | 实施计划 |
| subagent-driven-development | 逐任务实施 |
| systematic-debugging | 排查 bug |
| verification-before-completion | 完成前验证 |

## 启动命令
## 当前优先级
```

### Step 7: 生成通信配置

创建 `agents/communication.yaml`：

```yaml
format: json
routing:
  default: direct
  fallback: mcp

timeout:
  default_ms: 30000
  review_ms: 60000

retry:
  max_attempts: 3
  backoff: exponential

message:
  schema: |
    {
      "from": "agent_id",
      "to": "agent_id",
      "type": "task | review | response | route",
      "payload": {},
      "correlation_id": "uuid"
    }
```

### Step 8: 记录交互变更

- 必须记录用户的询问与本次初始化决策，存放于 `docs/interaction-changes/`
- 在 AGENTS.md 中说明该目录位置与归档方式
- 后续每次 Harness 配置调整，同步追加记录

### Step 9: 生成自我迭代与沉淀机制

创建 `agents/evolution/` 目录，建立 Harness 自我演进基础设施。

**核心约束**：每次用户交互都必须走 collect → analyze → sink → iterate 流程，且每个角色都要参与实践（不只是 orchestrator）。已初始化过的 Harness 不覆盖，而是合并增强。

```yaml
# agents/evolution/evolution.yaml
iteration:
  # 双节奏：小步快跑（交互级）+ 大周期沉淀（周期级）
  small_step:                    # 小步快跑 — 每次用户交互必走，轻量
    trigger: per-interaction
    cadence: every-user-turn
    scope: minimal-change        # 每轮只做最小改进，避免过度调整
    owner: all-roles             # 每个角色各自实践
  big_cycle:                     # 大周期沉淀 — 定期深度回顾，重量
    trigger: every-n-interactions  # 每 N 轮交互触发（N 默认 10，可调）
    manual: /harness-evolve        # 手动强制触发
    scope: pattern-extraction      # 提炼最佳实践、固化模式、升级角色定义
    owner: orchestrator-led        # orchestrator 牵头，所有角色参与

role_practice:                    # 每个角色在迭代流程中的职责
  architect:
    collect:  架构决策是否偏离、模块边界是否模糊、接口契约是否一致
    analyze:  回顾架构假设是否成立、是否过度设计或欠设计
    sink:     架构反模式 → architect.faq.md；架构经验 → lessons-learned.md；最佳实践 → architect.best-practices.md
    iterate:  调整 architect.md 提示词、更新模块拆分原则
  orchestrator:
    collect:  路由误判、工作类型识别错误、任务遗漏、上下文丢失
    analyze:  回顾 triage 准确率、工作流匹配度、新工作类型识别
    sink:     路由错误 → orchestrator.faq.md；新工作类型 → patterns.md；最佳实践 → orchestrator.best-practices.md
    iterate:  调整路由规则、新增工作流、更新节点-skill 映射
  executor:
    collect:  代码生成错误、契约不一致、skill 调用失败、重复实现已有步骤
    analyze:  回顾代码质量、skill 使用效率、是否绕过 skill 自行实现
    sink:     实施错误 → executor.faq.md；实施经验 → lessons-learned.md；最佳实践 → executor.best-practices.md
    iterate:  调整 executor.md、补充节点-skill 映射、推荐新 skill
  reviewer:
    collect:  审查遗漏项、误报漏报、审查标准不一致
    analyze:  回顾审查覆盖度、误报率、是否遗漏安全/性能维度
    sink:     审查问题 → reviewer.faq.md；审查模式 → patterns.md；最佳实践 → reviewer.best-practices.md
    iterate:  调整 reviewer.md、更新审查清单、引入新审查 skill
  devops:
    collect:  脚本兼容性问题、监控盲区、部署失败、环境差异
    analyze:  回顾脚本健壮性、监控覆盖度、部署可重复性
    sink:     运维问题 → devops.faq.md；运维经验 → lessons-learned.md；最佳实践 → devops.best-practices.md
    iterate:  调整 devops.md、补充监控项、优化脚本模板

sinks:                            # 沉淀去向（三类：错误/经验/最佳实践）
  - faq             → agents/faq/<role>.faq.md                  # 角色常见错误（负向）
  - best-practices  → agents/best-practices/<role>.best-practices.md  # 角色最佳实践（正向）
  - lessons         → agents/evolution/lessons-learned.md        # 跨角色经验
  - patterns        → agents/evolution/patterns.md               # 可复用工作模式
  - role-delta      → agents/evolution/role-changes.md           # 角色定义变更记录
  - workflow-delta  → agents/evolution/workflow-changes.md       # 工作流变更记录

feedback_loop:                    # 双节奏反馈闭环
  small_step:                     # 小步快跑（每次交互）
    - collect: 每个角色记录本轮交互中的问题（轻量，只记关键项）
    - analyze: 每个角色快速判断是否需要立即修正
    - sink:    每个角色写入自身 FAQ（错误）或 best-practices（经验）
    - iterate: 最小改动 — 仅调整节点-skill 映射或 FAQ 条目
  big_cycle:                      # 大周期沉淀（每 N 轮交互）
    - collect: 汇总小步快跑期间的所有沉淀
    - analyze: orchestrator 牵头深度回顾，识别模式与系统性问题
    - sink:    提炼最佳实践到 best-practices/；固化模式到 patterns.md
    - iterate: 重量级改动 — 升级角色定义、新增工作流、重构节点序列

merge_policy:                     # 已初始化时的合并策略
  existing_config: merge          # 不覆盖，合并增强
  roles: append-capabilities      # 角色能力追加，不删除已有
  workflows: append-or-update     # 新工作流追加，已有工作流按 diff 更新
  faq: append-entries             # FAQ 条目追加，不覆盖
  best-practices: append-entries  # 最佳实践条目追加，不覆盖
  sync: append-entries            # 协同文件条目追加，不覆盖已有进度/日志/经验
  evolution: append-history       # 演进历史追加，保留全部记录
```

**沉淀目录初始文件**：
- `agents/best-practices/architect.best-practices.md` — 架构师最佳实践（正向经验）
- `agents/best-practices/orchestrator.best-practices.md` — 编排者最佳实践
- `agents/best-practices/executor.best-practices.md` — 执行者最佳实践
- `agents/best-practices/reviewer.best-practices.md` — 评审者最佳实践
- `agents/best-practices/devops.best-practices.md` — DevOps 最佳实践
- `agents/sync/progress.yaml` — 全局进度看板（所有角色共享）
- `agents/sync/sync-log.md` — 操作时间线日志
- `agents/sync/experience-summary.md` — 跨角色经验总结
- `agents/sync/handoffs/handoff-template.yaml` — 交接记录模板
- `agents/sync/README.md` — 协同工作区说明
- `agents/evolution/lessons-learned.md` — 跨角色经验沉淀（执行中发现的最佳实践、踩坑、优化点）
- `agents/evolution/patterns.md` — 可复用工作模式（识别出的高频工作类型与推荐流程）
- `agents/evolution/role-changes.md` — 角色定义变更日志（每次角色提示词调整的 diff 与原因）
- `agents/evolution/workflow-changes.md` — 工作流变更日志（新增/调整工作流、节点-skill 映射更新）
- `agents/evolution/evolution.yaml` — 演进机制配置

**自我迭代触发条件**：
- **小步快跑（每次交互必走）**：per-interaction，轻量迭代，非可选
- **大周期沉淀（每 N 轮交互）**：默认 N=10，可调；深度回顾提炼最佳实践与模式
- 同类错误在 FAQ 中出现 ≥3 次（强制升级角色定义）
- 发现新工作类型无匹配工作流（创建并沉淀）
- 发现某节点 `skill: null` 但实际有 skill 可覆盖（回写映射）
- 用户主动触发 `/harness-evolve` 指令（强制大周期回顾）

**已初始化时的合并增强原则**：
- 检测到 `agents/harness.yaml` 已存在 → 不覆盖，diff 展示建议改动后合并
- 检测到 `agents/roles/*.md` 已存在 → 追加新能力，保留已有职责定义
- 检测到 `agents/workflows/*.yaml` 已存在 → 新工作流追加，已有工作流按节点 diff 更新
- 检测到 `agents/faq/*.md` 已存在 → 条目追加，不覆盖已有 FAQ
- 检测到 `agents/sync/` 已存在 → 条目追加，不覆盖已有进度/日志/经验/交接记录
- 检测到 `agents/evolution/` 已存在 → 历史记录保留，仅追加新沉淀
- 合并前必须向用户展示 diff，确认后写入

### Step 10: 生成协同进度跟踪与经验总结文件

创建 `agents/sync/` 目录，建立多角色协同工作的**进度可视化、交接同步、经验总结**基础设施。这是 Harness 作为"工程系统"而非"文档集合"的关键——角色之间通过标准化文件实现工作状态透明化。

#### 10.1 进度跟踪文件

创建 `agents/sync/progress.yaml` — 全局进度看板，所有角色共享：

```yaml
# agents/sync/progress.yaml — 多角色协同进度跟踪
# 每次角色完成工作节点后更新，实现工作状态可视化

project: {项目名}
last_updated: {时间戳}

# 当前活跃工作流
active_workflows:
  - id: wf-001
    name: standard-dev
    status: in_progress        # pending | in_progress | blocked | completed
    current_step: implement
    assigned_agent: executor
    started_at: {时间戳}
    estimated_remaining: {预估剩余节点数}

# 各角色工作队列
agent_queues:
  architect:
    status: idle               # idle | busy | blocked
    current_task: null
    pending_tasks: []
    completed_tasks: []
  orchestrator:
    status: busy
    current_task: "路由判断: 用户需求 → standard-dev"
    pending_tasks: []
    completed_tasks: ["wf-001:triage", "wf-001:route"]
  executor:
    status: busy
    current_task: "wf-001:implement — 实现用户管理模块"
    pending_tasks: []
    completed_tasks: []
  reviewer:
    status: idle
    current_task: null
    pending_tasks: ["wf-001:review"]
    completed_tasks: []
  devops:
    status: idle
    current_task: null
    pending_tasks: []
    completed_tasks: []

# 阻塞项跟踪
blockers:
  - id: blk-001
    description: "等待架构师确认接口契约"
    blocked_agent: executor
    blocking_agent: architect
    created_at: {时间戳}
    resolved: false

# 里程碑进度
milestones:
  - name: "核心模块架构设计完成"
    target: {日期}
    status: completed
    completed_at: {时间戳}
  - name: "用户管理模块 CRUD 完成"
    target: {日期}
    status: in_progress
    progress_pct: 60
  - name: "代码审查通过"
    target: {日期}
    status: pending
    progress_pct: 0

# 工作流执行统计
stats:
  total_workflows_completed: 0
  total_workflows_in_progress: 1
  total_workflows_blocked: 0
  avg_review_pass_rate: 0
  avg_cycle_time_minutes: 0
```

#### 10.2 交接记录文件

创建 `agents/sync/handoffs/` 目录 — 角色间任务交接的标准化记录：

`agents/sync/handoffs/handoff-template.yaml`:
```yaml
# 交接记录模板 — 角色 A → 角色 B 的任务传递
handoff_id: {uuid}
from_agent: {角色A}
to_agent: {角色B}
workflow_id: {工作流ID}
step: {当前节点名称}
timestamp: {时间戳}

# 传递内容
context:
  summary: "本轮完成的工作摘要"
  decisions: ["关键决策1", "关键决策2"]
  artifacts: ["产出文件路径1", "产出文件路径2"]
  open_questions: ["待解决问题1"]

# 接收确认
acknowledged: false
acknowledged_at: null
acknowledged_by: null
```

#### 10.3 角色同步日志

创建 `agents/sync/sync-log.md` — 所有角色的操作日志，按时间线记录：

```markdown
# 协同同步日志

## {日期}

| 时间 | 角色 | 操作 | 工作流 | 详情 |
|---|---|---|---|---|
| 10:00 | orchestrator | triage | wf-001 | 识别为用户管理模块开发需求 |
| 10:02 | orchestrator | route | wf-001 | 路由到 executor，工作类型: 代码实施 |
| 10:05 | executor | start | wf-001 | 开始实现用户管理 CRUD |
| 10:30 | executor | handoff | wf-001 | 交接给 reviewer 进行代码审查 |
| 10:32 | reviewer | start | wf-001 | 开始代码审查 |
| 10:45 | reviewer | complete | wf-001 | 审查通过，无阻塞问题 |
```

#### 10.4 经验总结文件

创建 `agents/sync/experience-summary.md` — 跨角色经验总结，区别于 FAQ（错误）和 best-practices（正向实践），经验总结聚焦于**可迁移的工程洞察**：

```markdown
# 经验总结

> 记录跨角色的工程洞察、方法论反思、协作优化点。
> 区别于 FAQ（具体错误规避）和 best-practices（角色内最佳实践），
> 经验总结聚焦于"如果重来一次，我们会怎么做"。

## 架构决策经验

### {日期} — {经验标题}
- **背景**：{什么场景下做的决策}
- **决策**：{做了什么选择}
- **结果**：{实际效果如何}
- **反思**：{如果重来，会怎么改进}
- **可迁移洞察**：{对后续项目的启示}

## 协作流程经验

### {日期} — {经验标题}
- **背景**：{协作中遇到的问题}
- **根因**：{问题本质是什么}
- **改进**：{流程做了什么调整}
- **效果**：{调整后的变化}
- **可迁移洞察**：{对后续协作的启示}

## 技术选型经验

### {日期} — {经验标题}
- **背景**：{技术选型场景}
- **对比方案**：{考虑过的方案及优劣}
- **最终选择**：{选了什么，为什么}
- **实际表现**：{上线后的表现}
- **可迁移洞察**：{对后续选型的启示}
```

#### 10.5 协同看板索引

创建 `agents/sync/README.md` — 协同文件目录说明与使用指南：

```markdown
# 协同工作区

本目录包含多 Agent 协同工作的进度跟踪、交接同步与经验总结文件。

## 文件说明

| 文件 | 用途 | 更新频率 | 更新角色 |
|---|---|---|---|
| `progress.yaml` | 全局进度看板，所有角色工作状态 | 每个工作节点完成后 | 当前执行角色 |
| `sync-log.md` | 操作时间线日志 | 每次角色操作后 | 操作角色 |
| `experience-summary.md` | 跨角色经验总结 | 大周期沉淀时 | orchestrator 牵头 |
| `handoffs/` | 角色间任务交接记录 | 每次交接时 | 交接双方 |

## 使用原则

1. **进度透明**：任何角色可随时查看 `progress.yaml` 了解全局状态
2. **交接有据**：角色间任务传递必须创建 handoff 记录，接收方确认后更新
3. **操作可追溯**：所有角色操作写入 `sync-log.md`，按时间线排列
4. **经验可复用**：大周期沉淀时将洞察写入 `experience-summary.md`
```

### Step 11: 确认并提交

- 展示生成的 Harness 配置给用户确认
- 用户确认后 git commit

## Harness 工程目录结构

```
agents/
├── harness.yaml           # Harness 主配置
├── communication.yaml     # Agent 间通信配置
├── roles/                 # Agent 角色定义
│   ├── architect.md
│   ├── orchestrator.md
│   ├── executor.md
│   ├── reviewer.md
│   └── devops.md
├── workflows/             # 多 Agent 协作流程
│   ├── standard-dev.yaml
│   ├── architecture-first.yaml
│   ├── code-review.yaml
│   ├── prd-to-code.yaml
│   ├── debug-workflow.yaml
│   └── devops-ops.yaml
├── faq/                   # 角色 FAQ（负向错误沉淀，避免重复犯错）
│   ├── architect.faq.md
│   ├── orchestrator.faq.md
│   ├── executor.faq.md
│   ├── reviewer.faq.md
│   └── devops.faq.md
├── best-practices/        # 角色最佳实践（正向经验沉淀，小步快跑积累）
│   ├── architect.best-practices.md
│   ├── orchestrator.best-practices.md
│   ├── executor.best-practices.md
│   ├── reviewer.best-practices.md
│   └── devops.best-practices.md
├── sync/                  # 协同进度跟踪与经验总结（工作状态可视化）
│   ├── README.md                 # 协同工作区说明与使用指南
│   ├── progress.yaml             # 全局进度看板（所有角色共享）
│   ├── sync-log.md               # 操作时间线日志（所有角色操作记录）
│   ├── experience-summary.md     # 跨角色经验总结（可迁移工程洞察）
│   └── handoffs/                 # 角色间任务交接记录
│       └── handoff-template.yaml # 交接记录模板
├── evolution/             # 自我迭代与沉淀（大周期沉淀）
│   ├── evolution.yaml            # 演进机制配置（双节奏：小步快跑 + 大周期）
│   ├── lessons-learned.md        # 跨角色经验沉淀
│   ├── patterns.md               # 可复用工作模式（大周期提炼）
│   ├── role-changes.md           # 角色定义变更日志
│   └── workflow-changes.md       # 工作流变更日志
└── AGENTS.md              # Harness 工程入口文档
docs/
└── interaction-changes/   # 用户询问与变更记录
```

## 工作路由机制（核心）

orchestrator 收到工作后，执行 triage-route 流程：

1. **识别工作类型**：判断属于架构设计 / 代码实施 / 质量评审 / 运维操作 / 调试 哪一类
2. **路由到匹配角色**：
   - 架构设计 → architect（调用 `codebase-design` / `design-an-interface`）
   - 代码实施 → executor（调用 `subagent-driven-development` / `tdd`）
   - 质量评审 → reviewer（调用 `requesting-code-review` / `TRAE-code-review`）
   - 运维操作 → devops（调用 `setup-pre-commit` / `verification-before-completion`）
   - 调试 → executor（调用 `systematic-debugging`）
3. **角色执行工作节点**：角色收到任务后，按工作流定义的节点序列推进，每个节点优先调用对应 skill 完成具体步骤
4. **无匹配时创建**：若现有角色/工作流无法覆盖，先创建新角色定义或新工作流（含节点-skill 映射），再执行
5. **记录到 FAQ**：路由误判或新工作类型，回写到 `agents/faq/orchestrator.faq.md`

## 自我迭代与沉淀机制（核心）

Harness 不是一次性产物，必须随执行持续演进。采用**双节奏机制**：小步快跑（交互级轻量迭代）+ 大周期沉淀（周期级深度提炼）。每个角色都要参与实践，积累自身最佳实践。已初始化过的 Harness 不覆盖，按合并策略增强。

### 双节奏总览

| 节奏 | 触发 | 范围 | 改动幅度 | 产出 |
|---|---|---|---|---|
| **小步快跑** | 每次用户交互 | 本轮交互问题 | 最小改动 | FAQ 条目、最佳实践条目、节点-skill 微调 |
| **大周期沉淀** | 每 N 轮交互（默认 10）或 `/harness-evolve` | 汇总小步快跑期间所有沉淀 | 重量级改动 | 模式固化、角色定义升级、工作流重构 |

### 小步快跑（交互级，每次必走）

每次用户交互（无论是否触发工作流）结束后，每个角色独立执行：

1. **collect（每个角色）**：回顾本轮交互中自身职责范围内的问题与亮点
2. **analyze（每个角色）**：快速判断 — 错误沉淀到 FAQ？亮点沉淀到 best-practices？是否需要立即微调？
3. **sink（每个角色）**：写入自身 FAQ（负向）或 best-practices（正向）
4. **iterate（最小改动）**：仅调整节点-skill 映射或 FAQ 条目，不升级角色定义

**小步快跑原则**：每轮只做最小改进，避免过度调整；重量级改动留到大周期。

### 大周期沉淀（周期级，定期深度回顾）

每 N 轮交互（默认 N=10，可调）或用户执行 `/harness-evolve` 时触发：

1. **collect（orchestrator 牵头）**：汇总小步快跑期间所有 FAQ、best-practices、lessons-learned
2. **analyze（所有角色参与）**：识别系统性问题、可复用模式、角色定义短板
3. **sink（深度提炼）**：提炼最佳实践到 `best-practices/`；固化模式到 `patterns.md`
4. **iterate（重量级改动）**：升级角色定义、新增工作流、重构节点序列

**大周期沉淀原则**：从零散经验提炼系统性模式；FAQ 反复出现的错误升级到角色定义；稳定的模式固化为标准工作流。

### 反馈收集（collect）— 每个角色各自实践

| 角色 | 负向收集（→ FAQ） | 正向收集（→ best-practices） |
|---|---|---|
| architect | 架构决策偏离、模块边界模糊、接口契约不一致、过度/欠设计 | 架构决策成功案例、模块拆分有效模式、接口设计经验 |
| orchestrator | 路由误判、工作类型识别错误、任务遗漏、上下文丢失 | 路由准确案例、新工作类型识别、跨角色协调经验 |
| executor | 代码生成错误、契约不一致、skill 调用失败、重复实现已有步骤 | 高效实施模式、skill 组合用法、代码质量提升经验 |
| reviewer | 审查遗漏项、误报漏报、审查标准不一致、安全/性能维度遗漏 | 审查覆盖全面案例、误报规避、高效审查流程 |
| devops | 脚本兼容性问题、监控盲区、部署失败、环境差异 | 健壮脚本模式、监控覆盖经验、部署自动化实践 |

通用收集项：耗时与阻塞点、skill 缺失、skill 不匹配、重复错误。

### 沉淀（sink）— 三类沉淀，每个角色写入

| 沉淀类型 | 性质 | 目标文件 | 写入角色 | 节奏 |
|---|---|---|---|---|
| 角色常见错误 | 负向 | `agents/faq/<role>.faq.md` | 对应角色 | 小步快跑 |
| 角色最佳实践 | 正向 | `agents/best-practices/<role>.best-practices.md` | 对应角色 | 小步快跑 + 大周期提炼 |
| 跨角色经验 | 混合 | `agents/evolution/lessons-learned.md` | 任意角色 | 小步快跑 |
| 可复用模式 | 正向 | `agents/evolution/patterns.md` | orchestrator | 大周期沉淀 |
| 角色定义变更 | 变更 | `agents/evolution/role-changes.md` | 对应角色 | 大周期沉淀 |
| 工作流变更 | 变更 | `agents/evolution/workflow-changes.md` | orchestrator | 大周期沉淀 |

### 迭代（iterate）— 触发工作流程自我更新

**小步快跑级迭代**（最小改动）：
- 节点-skill 映射微调：发现 `skill: null` 节点实际有 skill 可覆盖 → 回写工作流 `skill` 字段
- FAQ 条目追加：单次错误立即记录
- best-practices 条目追加：单次亮点立即记录

**大周期级迭代**（重量级改动）：
- **角色定义迭代**：同类错误在 FAQ 出现 ≥3 次 → 升级到角色提示词，记录到 `role-changes.md`
- **工作流迭代**：发现新工作类型 → 创建新工作流并标注节点-skill 映射，记录到 `workflow-changes.md`
- **模式固化**：高频工作类型稳定后（被引用 ≥3 次无调整）→ 提炼为模式写入 `patterns.md`，供 orchestrator 路由参考
- **最佳实践升华**：`best-practices/` 中多次验证有效的条目 → 固化到角色提示词或标准工作流节点

### 触发方式

- **小步快跑**：每次用户交互必走（per-interaction，强制，非可选）
- **大周期沉淀**：每 N 轮交互自动触发（默认 N=10，可在 `evolution.yaml` 调整）
- **阈值触发**：FAQ 同类错误累计 ≥3 次，强制升级角色定义（跨节奏触发）
- **手动深度回顾**：用户执行 `/harness-evolve` 指令，强制触发大周期沉淀

### 已初始化时的合并增强

检测到 Harness 配置已存在时，不覆盖，按以下策略合并：

| 资源 | 合并策略 |
|---|---|
| `harness.yaml` | diff 展示建议改动后合并，保留已有 agents/workflows |
| `roles/*.md` | 追加新能力，保留已有职责定义；冲突部分向用户展示 diff |
| `workflows/*.yaml` | 新工作流追加；已有工作流按节点 diff 更新 |
| `faq/*.md` | 条目追加，不覆盖已有 FAQ |
| `best-practices/*.md` | 条目追加，不覆盖已有最佳实践 |
| `sync/*` | 条目追加，不覆盖已有进度/日志/经验/交接记录 |
| `evolution/` | 历史记录全部保留，仅追加新沉淀 |
| `communication.yaml` | 按字段合并，保留已有配置 |

**合并前必须向用户展示 diff，确认后写入**。

### 沉淀文件维护原则

- 沉淀文件必须按日期 + 序号追加，不覆盖历史
- 每条沉淀记录包含：时间、来源交互/工作流、角色、问题、改进措施、影响范围
- 角色定义与工作流变更必须同步提交 git，便于回溯
- `patterns.md` 中的模式达到稳定（被引用 ≥3 次无调整）后，可考虑固化为标准工作流

## 依赖 Skill 声明

init-dev-harness-agents 本身不依赖其他 skill 执行，但生成的 AGENTS.md 中会声明 Harness 工程所需的 skill 链：

```
Harness 开发 skill 链:
  brainstorming → writing-plans → subagent-driven-development → verification-before-completion

多 Agent 协作:
  orchestrator (triage) → architect / executor / reviewer / devops

架构优先:
  architect → orchestrator (decompose) → executor → reviewer

调试:
  systematic-debugging

验证:
  verification-before-completion
```

## 模板变量

| 变量 | 来源 | 示例 |
|---|---|---|
| `{项目名}` | 目录名或 package.json name | stock-analysis |
| `{技术栈}` | 扫描依赖文件 | Java 17 + Spring Boot + Vue3 + Vite |
| `{Agent 数量}` | 根据项目复杂度 | 5（architect + orchestrator + executor + reviewer + devops） |
| `{工作流数量}` | 根据项目需求 | 6（dev / architecture / review / prd-to-code / debug / devops） |

## 与 init-harness-agents 的区别

| 维度 | init-harness-agents（通用） | init-dev-harness-agents（开发） |
|------|--------------------------|-------------------------------|
| 目标 | 通用多 Agent 协作 | 代码开发多 Agent 协作 |
| 角色 | coordinator / analyst / creator / evaluator | architect / orchestrator / executor / reviewer / devops |
| 适用 | 产品、设计、研究等非代码领域 | 前后端代码开发 |
| 工作流 | 协作、辩论、调研 | 开发、架构、审查、调试、运维 |
| 路由 | 任务分解后分配 | triage-route（先识别工作类型再路由） |
| 触发 | `/init` | `/init-dev` |

## 注意事项

- **Harness 与 Skills 分工**：本 skill 只定义角色 + 工作流（工作节点序列），不复制 skill 的具体步骤；角色执行节点时优先调用对应 skill，避免重复发明
- **自我迭代是硬性要求**：Harness 必须随执行演进，不能一次性生成后不再维护
- **双节奏迭代**：小步快跑（每次交互轻量迭代，最小改动）+ 大周期沉淀（每 N 轮深度回顾，重量级改动）；避免小步快跑做重量级改动，也避免大周期遗漏细节
- **每个角色都参与迭代**：collect/analyze/sink 由每个角色独立完成，非 orchestrator 独占；orchestrator 仅在大周期牵头汇总
- **每个角色积累最佳实践**：best-practices 是正向经验沉淀，区别于 FAQ（负向错误）；两者并行维护，不能只有 FAQ 没有 best-practices
- **沉淀先于迭代**：发现问题时先沉淀到 FAQ / best-practices / lessons-learned，达到阈值（≥3 次）再升级到角色定义或工作流变更
- **已初始化不覆盖，合并增强**：检测到已有 Harness 配置时按合并策略增强，保留已有能力与历史沉淀；合并前必须展示 diff
- 如果 Harness 配置已存在，不要覆盖，而是 diff 展示建议改动
- 角色定义保持单一职责，避免一个角色承担过多能力
- 架构师角色必须先行于大规模实施，把控应用、模块拆分、接口与类职责
- DevOps 角色必须产出启停脚本与必要监控，不能只停留在文档
- 工作流定义优先覆盖核心流程（dev / architecture / review / debug / devops），后续按需扩展
- 通信配置中的超时和重试策略根据实际 Agent 响应时间调整
- FAQ 与 best-practices 必须随执行过程持续更新，不能一次性生成后不再维护
- 交互记录必须存放于 `docs/interaction-changes/`，并在 AGENTS.md 中说明位置
- 沉淀文件按日期 + 序号追加，不覆盖历史；角色与工作流变更同步提交 git
