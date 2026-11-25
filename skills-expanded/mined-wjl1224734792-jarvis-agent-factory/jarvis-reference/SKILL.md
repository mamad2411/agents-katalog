---
name: jarvis-reference
description: "Jarvis 统一参考 — Agent 目录、命令入口、技能注册表、流水线体系、MCP 工具参考、发布协议。Agent/编排者启动时自动加载获取全量能力索引。"
version: "4.3.8"
updated: "2026-05-20"
user-invocable: false
---

# Jarvis Reference — 统一能力参考

Jarvis Agent Factory 完整能力索引。Agent 和编排者启动时加载此技能即可获得全量参考，无需查多个文件。

## Agent 目录

共 **88 个 Agent**，仅 Claude Code 平台。前缀 `oh-my-claudecode:`。详见 `AGENTS.md` L5。

### 实现类（34）

| Agent | 专长 |
|-------|------|
| `frontend-dev-expert` | Web 前端全栈开发 |
| `frontend-ui-expert` | Web 前端 UI 组件实现 |
| `frontend-state-expert` | Web 前端状态管理 |
| `backend-dev-expert` | 后端全栈开发 |
| `backend-api-expert` | RESTful/GraphQL API 设计实现 |
| `backend-logic-expert` | 业务逻辑层实现 |
| `backend-data-expert` | 数据访问层/ORM 实现 |
| `taro-dev-expert` | Taro 跨端全栈开发 |
| `taro-ui-expert` | Taro UI 组件实现 |
| `taro-state-expert` | Taro 状态管理 |
| `expo-dev-expert` | Expo 全栈开发 |
| `expo-ui-expert` | Expo UI 组件实现 |
| `expo-state-expert` | Expo 状态管理 |
| `flutter-dev-expert` | Flutter 全栈开发 |
| `flutter-ui-expert` | Flutter UI 组件实现 |
| `flutter-state-expert` | Flutter 状态管理 |
| `swift-dev-expert` | Swift/SwiftUI 开发 |
| `swift-ui-expert` | SwiftUI 实现 |
| `swift-state-expert` | Swift 状态管理 |
| `kotlin-dev-expert` | Kotlin/Compose 开发 |
| `kotlin-ui-expert` | Kotlin UI 实现 |
| `kotlin-state-expert` | Kotlin 状态管理 |
| `miniprogram-dev-expert` | 微信小程序开发 |
| `miniprogram-ui-expert` | 小程序 UI 实现 |
| `miniprogram-state-expert` | 小程序状态管理 |
| `uni-app-dev-expert` | uni-app 开发 |
| `uni-app-ui-expert` | uni-app UI 实现 |
| `uni-app-state-expert` | uni-app 状态管理 |
| `react-dev-expert` | React Web 开发 |
| `react-ui-expert` | React UI 实现 |
| `react-state-expert` | React 状态管理 |
| `vue-dev-expert` | Vue Web 开发 |
| `vue-ui-expert` | Vue UI 实现 |
| `vue-state-expert` | Vue 状态管理 |

### 测试类（18）

| Agent | 专长 |
|-------|------|
| `frontend-test-expert` | 前端单元/组件测试 |
| `backend-test-expert` | 后端单元/集成测试 |
| `flutter-test-expert` | Flutter 测试 |
| `taro-test-expert` | Taro 测试 |
| `expo-test-expert` | Expo 测试 |
| `swift-test-expert` | Swift 测试 |
| `kotlin-test-expert` | Kotlin 测试 |
| `miniprogram-test-expert` | 小程序测试 |
| `uni-app-test-expert` | uni-app 测试 |
| `react-test-expert` | React 测试 |
| `vue-test-expert` | Vue 测试 |
| `browser-test-expert` | 浏览器 E2E 测试 |
| `frontend-debug-expert` | 前端实时调试（Chrome DevTools MCP，性能追踪/渲染分析/网络诊断） |
| `e2e-test-expert` | 端到端集成测试 |
| `perf-test-expert` | 性能测试/分析 |
| `api-test-expert` | API 契约测试 |
| `test-doc-writer` | 测试用例文档编写 |
| `test-executor` | 测试用例执行 |

### 审查类（19）

| Agent | 专长 |
|-------|------|
| `frontend-review-expert` | 前端代码审查 |
| `backend-review-expert` | 后端代码审查 |
| `flutter-review-expert` | Flutter 代码审查 |
| `taro-review-expert` | Taro 代码审查 |
| `expo-review-expert` | Expo 代码审查 |
| `swift-review-expert` | Swift 代码审查 |
| `kotlin-review-expert` | Kotlin 代码审查 |
| `miniprogram-review-expert` | 小程序代码审查 |
| `uni-app-review-expert` | uni-app 代码审查 |
| `react-review-expert` | React 代码审查 |
| `vue-review-expert` | Vue 代码审查 |
| `diff-review-expert` | Diff 变更审查 |
| `project-review-expert` | 项目级全面审查 |
| `perf-review-expert` | 性能审查 |
| `security-review-expert` | 安全漏洞审查 |
| `qa-review-expert` | QA 综合质量审查 |
| `change-review-expert` | 变更影响审查 |
| `review-only` | 纯审查（不含修复） |
| `review-fix-optimize` | 审查+修复+优化一体化 |

### 规划/任务（4）

| Agent | 专长 |
|-------|------|
| `planner` | 执行计划编排 |
| `task-design` | 任务分解与设计 |
| `skill-assignment-expert` | 技能分配推荐 |
| `remediation-planner` | 修复方案规划 |

### 架构/专家（5）

| Agent | 专长 |
|-------|------|
| `frontend-architect` | 前端架构设计（仅方案讨论） |
| `backend-architect` | 后端架构设计（仅方案讨论） |
| `algorithm-expert` | 算法设计评审（仅方案讨论） |
| `database-architect` | 数据库架构设计 |
| `mobile-architect` | 移动端架构师 |

### 探索/支撑（7）

| Agent | 专长 |
|-------|------|
| `code-explore-expert` | 代码库搜索探索 |
| `external-resource-expert` | 外部文档/资源查询 |
| `api-contract-expert` | API 契约定义 |
| `docs-engineer` | 文档工程 |
| `infra-deploy-expert` | 基础设施/部署 |
| `remediation-expert` | 修复执行 |
| `docs-research-expert` | 文档调研 |

### 模型路由

- `haiku` — 快速查找、轻量检查、简单文档
- `sonnet` — 标准实现、调试、审查
- `opus` — 架构设计、深度分析、规划共识、高风险审查

---

## 命令目录

共 **44 条命令**，仅 Claude Code 平台。详见 `AGENTS.md` L4。

### 编排入口（2）

| 命令 | 流水线 | 说明 |
|------|--------|------|
| `/jarvis` | full（12 Gate） | 全流程严格模式，适合中大型功能开发 |
| `/auto` | 智能路由 | 自动检测→选最优流水线→跳过无关Gate。**日常默认入口** |

### 平台开发（2）

| 命令 | 平台 |
|------|------|
| `/frontend` `/backend` | Web 全栈 |

### 需求与设计（3）

| 命令 | 说明 |
|------|------|
| `/ask` | 需求探询（Interview/Direct/Consensus/Review 4模式） |
| `/task-design --mode=ddd\|bdd\|tdd` | 任务分解（领域/行为/测试驱动，三合一） |
| `/research` | 深度研究（RS0-RS4） |

### 工程操作（7）

| 命令 | 说明 |
|------|------|
| `/refactor` | 代码重构（R1-R5） |
| `/hotfix` | 紧急修复（H0-H3） |
| `/migrate` | 框架升级/依赖迁移（M1-M4） |
| `/evaluate` | 技术选型/方案对比（E0-E3） |
| `/debug` | 异常排查（D0-D4） |
| `/trace` | 假设驱动因果追踪（T0-T4） |
| `/improve` | 度量驱动迭代改进（IM0-IM4） |

### 质量（2）

| 命令 | 说明 |
|------|------|
| `/simplify` | 代码质量清理（S0-S3） |
| `/release` | 快速发布（RL0-RL4） |

### 审查与测试（7）

| 命令 | 说明 |
|------|------|
| `/review-only` `/review-fix` | 代码审查/审查+修复 |
| `/test-unit` `/test-integration` `/test-e2e` `/test-perf` `/test-security` | 专项测试 |

### 专用工具（3）

| 命令 | 说明 |
|------|------|

### 发布与同步（2）

| 命令 | 说明 |
|------|------|
| `/publish` | 发布上线 |
| `/sync` | 配置同步 |

### 框架开发（9）

| 命令 | 框架 |
|------|------|
| `/flutter` | Flutter/Dart 跨端移动端开发 |
| `/expo` | Expo/React Native 跨平台开发 |
| `/swift` | Swift/SwiftUI iOS 开发 |
| `/kotlin` | Kotlin/Jetpack Compose Android 开发 |
| `/taro` | Taro 小程序/H5 跨端开发 |
| `/miniprogram` | 微信小程序原生开发 |
| `/uni-app` | uni-app 跨端开发 |
| `/react` | React Web 开发 |
| `/vue` | Vue Web 开发 |

### 专用工具（5）

| 命令 | 说明 |
|------|------|
| `/cleanup` | 代码清理与格式化 |
| `/deepinit` | AI驱动分层架构文档初始化 |
| `/verify` | 证据驱动验证 |
| `/repowiki` | 知识库管理 |
| `/skill-flow` | 会话流程导出为 Skill 模板 |

### 流程管理（2）

| 命令 | 说明 |
|------|------|
| `/skill-flow` | 会话流程导出为 Skill 模板（export/save/list/apply） |
| `/cancel [--leave \| --force]` | 取消流水线运行（--leave 离开会话 / --force 紧急清除） |

---

## 技能注册表

共 **34 个 Skill**，按 14 类分组。详见 `AGENTS.md` L6。加载方式：`Skill("<skill-name>")`。

### 基础（5）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `behavioral-guidelines` | 四项核心行为准则 | 所有 Agent |
| `context-engineering` | 选择性上下文管理 | 编排者 |
| `using-agent-skills` | 技能系统使用指南 | 编排者/新 Agent |
| `concurrency-policy` | 并发调用与Team/Subagent分配规范 | 编排者/所有 Agent |
| `session-memory` | 跨会话记忆与上下文注入 | 所有 Agent |

### 需求（2）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `spec-driven-development` | 结构化需求规格编写 | 编排者 |
| `idea-refine` | 模糊想法→结构化问题清单 | 编排者 |

### 规划（1）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `planning-and-task-breakdown` | 垂直切片、风险标注、并行识别 | task-design Agent |

### 实现（7）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `source-driven-development` | 先读代码再写代码 | 所有实现 Agent |
| `incremental-implementation` | 小步增量交付、每步可验证 | 所有实现 Agent |
| `test-driven-development` | Red→Green→Refactor 方法论 | TDD 任务 Agent |
| `code-standards` | 通用编程规范（注释/嵌套/不可变/DDD） | 所有实现 Agent |
| `code-simplification` | 降低复杂度、消除重复 | 实现 Agent（Refactor 阶段） |
| `frontend-design` | 前端 UI/UX 设计方法论 | 前端实现 Agent |
| `refactoring` | 安全重构流程与模式 | 所有实现 Agent |

### 质量（3）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `code-quality-gate` | Gate C1 四项检查（Lint/Type-check/Build/Deps） | 编排者（Gate C1） |
| `code-review-and-quality` | 五轴审查框架、严重度分级 | qa-review-expert |
| `verification-before-completion` | 交付前 5 层验证清单 | 所有实现 Agent |

### 测试（2）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `perf-testing` | 性能测试方法论（基准/负载/剖析） | perf-test-expert |
| `test-data-factory` | 测试数据工厂（fixture/builder/mock） | 测试 Agent |

### 调试（2）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `debugging-and-error-recovery` | 系统化调试流程与根因追踪 | 所有 Agent（遇 Bug 时） |
| `debugging-deep` | 深度调试：内存/并发/竞态/死锁 | 复杂 Bug 排查 Agent |

### 浏览器/调试（1）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `browser-testing` | 浏览器测试方法论（混合模式：agent-browser 看清 + Playwright MCP 操作） | browser-test-expert |

### 安全（2）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `security-and-hardening` | 安全漏洞修复与加固 | 安全任务 Agent |
| `security-testing` | 安全测试方法论（OWASP/渗透/审计） | security-review-expert |

### 流程（3）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `shipping-and-launch` | 上线检查清单与灰度策略 | 编排者 |
| `git-workflow-and-versioning` | 分支管理、提交规范、版本管理 | 编排者 |
| `finishing-a-development-branch` | 分支合并、清理、部署验证 | 编排者 |

### 文档（3）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `chinese-documentation` | 中文文档排版与术语规范 | 编排者（写文档时） |
| `documentation-and-adrs` | 架构决策记录（ADR） | 编排者/planner |
| `writing-skills` | 技能文件编写与验证规范 | 创建/编辑技能文件的 Agent |

### 探索（1）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `find-docs` | 外部库/框架文档查询（WebSearch/WebFetch） | external-resource-expert |

### 工具（1）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `mcp-builder` | MCP 服务器构建方法论 | 构建 MCP 工具的 Agent |

### 参考（1）

| Skill | 用途 | 加载者 |
|-------|------|--------|
| `jarvis-reference` | 本技能——统一能力索引 | 所有 Agent（启动时） |

---

## 流水线体系

共 **17 条流水线**。Gate 序列由引擎 `GATE_CHECKS` 强制执行，不可跳过。

### 标准流水线

```
Gate A → Gate B-DDD → Gate B-BDD → Gate B-TDD → Gate B1
  → Gate C → Gate C-impl → Gate C1 → Gate C1.5 → Gate C2
  → Gate D → Gate E
```

| Gate | 说明 | 允许操作 | 禁止操作 |
|------|------|---------|---------|
| A | 需求澄清 | read, write_doc | write_code, spawn_test, build, deploy |
| B-DDD | 领域驱动分析 | read, write_doc | write_code, spawn_test, build, deploy |
| B-BDD | 行为驱动场景 | read, write_doc | write_code, spawn_test, build, deploy |
| B-TDD | 测试驱动分解 | read, write_doc | write_code, spawn_test, build, deploy |
| B1 | 架构评审（条件性） | read, write_doc, sweep_arch | write_code, spawn_impl, build, deploy |
| C | 执行规划 | read, write_doc, spawn_impl | spawn_test, build, deploy |
| C-impl | 并行实现 | read, write_code, spawn_impl | spawn_test, build, deploy |
| C1 | 代码质量门 | read, lint, build, fix | spawn_impl, spawn_test, deploy, write_code |
| C1.5 | 视觉验证（条件性） | read, preview, fix, spawn_test | spawn_impl, build, deploy, write_code |
| C2 | 测试验证 | read, spawn_test, fix | spawn_impl, deploy, write_code |
| D | 评审 | read, review, audit, fix, spawn_impl | spawn_test, build, deploy, write_code |
| E | 发布上线 | read, deploy, write_doc, lint, build, spawn_impl | write_code, spawn_test |

### 专业流水线（13）

| 命令 | 流水线 | Gate 序列 | 门数 |
|------|--------|----------|:----:|
| `/refactor` | refactor | R1→R2→R3→R4→R5 | 5 |
| `/hotfix` | hotfix | H0→H1→H2→H3 | 4 |
| `/migrate` | migrate | M1→M2→M3→M4 | 4 |
| `/evaluate` | evaluate | E0→E1→E2→E3 | 4 |
| `/debug` | debug | D0→D1→D2→D3→D4 | 5 |
| `/research` | research | RS0→RS1→RS2→RS3→RS4 | 5 |
| `/release` | release | RL0→RL1→RL2→RL3→RL4 | 5 |
| `/ask` | ask | K0→K1→K2→K3 | 4 |
| `/simplify` | simplify | S0→S1→S2→S3 | 4 |
| `/trace` | trace | T0→T1→T2→T3→T4 | 5 |
| `/improve` | improve | IM0→IM1→IM2→IM3→IM4 | 5 |
| `/frontend` | frontend | A→B-DDD→B-BDD→B-TDD→B1→C→C-impl→C1→C1.5→C2→D→E | 12 |
| `/backend` | backend | A→B-DDD→B-BDD→B-TDD→B1→C→C-impl→C1→C2→D→E | 11 |
| `/auto` | auto | A→B-DDD→B-BDD→B-TDD→B1→C→C-impl→C1→C1.5→C2→D→E (allow_jump) | 12 |
| `/deepinit` | deepinit | DI0→DI1→DI2→DI3 | 4 |
| `/consult` | consult | C0 | 1 |

### Agent 编排策略

| Gate | 策略 | 方式 |
|------|------|------|
| A / B-DDD / B-BDD / B-TDD | subagent_only | Agent 工具直接 spawn |
| B1 | subagent_only | Agent 工具直接 spawn 架构师 |
| C | subagent_only | Agent 工具 spawn planner |
| C-impl | prefer_team | TeamCreate + Agent(team_name) |
| C1.5 | subagent_only | Agent 工具 spawn browser-test-expert（视觉截图+多视口+样式验证） |
| C2 | prefer_team | TeamCreate + Agent(team_name) |
| D | prefer_team | TeamCreate + Agent(team_name) |
| E | subagent_only | Agent 工具直接 spawn |

---

## MCP 工具参考

引擎通过 MCP stdio 提供以下工具，由 `jarvis` CLI 自动注册到 Claude Code。

### 会话管理

| 工具 | 说明 |
|------|------|
| `session_join` | 加入/创建会话，注册平台和流水线类型 |
| `session_set_name` | 设置会话显示名称 |
| `session_list` | 列出所有会话（支持筛选/排序/置顶） |
| `session_heartbeat` | 心跳保活——活动追踪模式下标记当前会话活跃 |
| `session_leave` | 离开当前会话 |

### 流水线控制

| 工具 | 说明 |
|------|------|
| `pipeline_init` | 初始化流水线运行 |
| `pipeline_status` | 当前会话流水线状态查询 |
| `pipeline_guide` | 获取当前 Gate 的调度建议（Agent/Team策略） |
| `gate_check` | 检查当前 Gate 状态和通过条件 |
| `gate_enforce` | 强制 Gate 权限约束 |
| `advance_gate` | 推进到下一个 Gate |
| `gate_jump` | 跳转到指定 Gate（仅限 allow_jump 流水线：auto/ask/improve） |
| `report_status` | 报告当前流水线完整状态 |

### 文件冲突防护

| 工具 | 说明 |
|------|------|
| `file_claim_check` | 预检查：检测拟分配的路径是否与已有 Agent 的独占路径冲突 |
| `file_claim_register` | 注册 Agent 的独占文件路径（spawn 后立即调用） |
| `file_claim_release` | 释放 Agent 的文件独占声明（Agent 完成后调用） |

> **协议**：spawn 前 `file_claim_check` → spawn 后 `file_claim_register` → Agent 完成 `file_claim_release`。同 Batch 内路径不可重叠。

### 流程 Skill

| 工具 | 说明 |
|------|------|
| `session_export` | 导出当前会话的流水线流程数据 |
| `flow_skill_save` | 保存导出流程为可复用 Skill 模板 |
| `flow_skill_list` | 列出所有已保存的流程 Skill |

### Agent 管理

| 工具 | 说明 |
|------|------|
| `agent_config` | Agent 模型/思考等级配置（读写合一：无参数=读取，传 agent_id+model=写入） |

### 平台

| 工具 | 说明 |
|------|------|
| `platform_info` | 获取当前平台信息和功能矩阵 |

---

## 发布协议

详见 `AGENTS.md` L8。

### 流程

```
版本递增 → 文档同步 → 提交 → Tag → Push → CI 自动发布
```

### 版本规则

| 类型 | 场景 |
|------|------|
| patch (z) | Bug 修复 |
| minor (y) | 新功能、新指令、新 Agent/Skill |
| major (x) | 破坏性变更 |

### 提交格式

```
<type>: <中文描述>
```

### CI 自动发布

| 触发 | 工作流 | 职责 |
|------|--------|------|
| push/PR to main | `ci.yml` | Lint + Type-check + Test + Build |
| Tag `v*` | `ci.yml` | 质量检查 → Changelog → GitHub Release → npm publish |

### 文档同步约束

每次提交必须同步更新：
- `AGENTS.md` — Agent 列表、技能列表、统计数字
- `README.md` — 版本号、特性列表、统计数据
- `.jarvis/README.md` — 流水线产物目录结构

---

## 核心约束（24 条红线）

详见 `AGENTS.md` L2。关键规则：

1. **禁止凭记忆编码** — 修改前必须读取相关源码
2. **闸门不可绕过** — Gate 序列不可跳跃
3. **同 Batch 并行** — 无依赖任务批量发起
4. **修改完必须测试** — lint + typecheck + test + build
5. **修改完必须发布** — 测试通过后推送 GitHub
6. **提交必须同步文档** — AGENTS.md / README.md / .jarvis/README.md
7. **临时文件统一存放** — `.jarvis/tmp/`，禁止散落根目录
8. **产物目录规范** — `.jarvis/YYYY-MM-DD/{subdir}/`
9. **Agent Team + SubAgent 混合编排** — 根据 Gate team_strategy 选择
10. **Agent Team 模块隔离** — 每个成员独占模块/文件区域
