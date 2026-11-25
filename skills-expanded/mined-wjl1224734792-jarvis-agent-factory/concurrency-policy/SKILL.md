---
name: concurrency-policy
description: "并发调用与 Team/Subagent 分配规范——无依赖并行、同层并行跨层串行、Team 按规模选择、Gate 级并发规则"
version: "4.7.89"
updated: "2026-05-22"
---

# Concurrency Policy — 并发调用与 Team/Subagent 分配规范

## 核心原则

1. **无依赖 = 并行**：互不依赖的任务在同一条消息中同时发出，不等不串行
2. **同层并行、跨层串行**：同级目录/模块并行处理，父子依赖的层级串行
3. **Team 按规模**：>10 文件或跨模块变更 → Team 模式；≤10 文件 → Subagent 模式
4. **批量同发**：同一 Gate 内的独立 Agent 调用一次发出，不做无意义的逐个等待

## 执行模式选择

| 条件 | 模式 | 说明 |
|------|------|------|
| 文件数 ≤5，单模块 | Subagent（直接 spawn） | 轻量，一个 Agent 完成 |
| 文件数 5-10，单模块 | Subagent × 2-3（并行） | 拆分到无冲突文件组 |
| 文件数 >10，跨模块 | Team 模式 | TeamCreate → 按模块分配成员 |
| 只读探索（多目录） | Subagent × N（并行） | 每个目录一个 explore agent |
| 审查（多领域） | Subagent × N（并行） | 前端/后端/安全/性能审查同发 |

## Team 模式规范

### 何时用 Team

满足任一条件即触发 Team 模式：
- 变更文件 >10 个
- 跨 ≥3 个源码目录
- 需要前端+后端同时实现
- 需要多种测试（单元+集成+E2E）同时进行

### Team 创建与销毁

```
1. TeamCreate({ team_name: "{task}-{gate}" })
2. spawn Agent（指定 team_name, name, subagent_type）
3. 全部完成后 → SendMessage 发送 shutdown_request
4. TeamDelete() 清理
```

### Team 成员分配

| 场景 | 成员配置 |
|------|---------|
| 前端+后端 | frontend-dev-expert + backend-dev-expert |
| 全栈审查 | frontend-review + backend-review + security-review + perf-review |
| 并行测试 | frontend-test + backend-test + e2e-test |
| 多模块实现 | 每个模块一个 dev-expert，无文件重叠 |

### 降级策略

- 不支持 TeamCreate → 回退到并行 Subagent 模式
- <5 文件的小任务 → 直接用 Subagent，不创建 Team

## 并行 Subagent 规范

### 何时并行

- 探索多个目录（code-explore-expert × N）
- 多领域审查（frontend-review + backend-review + security-review + perf-review）
- 多类型测试（单元 + 集成 + E2E）
- 多模块实现（无共享文件冲突）
- **同类型 Agent 多实例**（不同模块、无文件冲突 → 同类型 Agent 可并行 N 个实例）

### 何时串行

- 子任务依赖父任务输出（如 planner 产出后才能 spawn 实现 Agent）
- 共享文件有写入冲突
- 测试依赖实现完成（先实现 → 后测试）
- 审查依赖测试报告（先测试 → 后审查）
- 同一模块/同一共享 Schema 的多个任务（共享上下文，并行会导致冲突）

## 同类型 Agent 多实例并行（Same-Type Agent Fan-Out）

### 核心规则

**Agent 类型的约束是文件冲突，不是类型本身。** 同类型 Agent 可以为不同模块创建多个并行实例，只要各自操作的 `allowed_paths` 互不重叠。

| 规则 | 说明 |
|------|------|
| 并行条件 | 同类型 Agent × N，各自 allowed_paths 无重叠 → 可并行 |
| 串行条件 | 同类型 Agent 共享同一模块/Schema/中间件 → 必须串行 |
| 数量上限 | 由任务数决定，不设硬上限（受 file_claim 协议保护） |
| 模型覆盖 | 每个实例独立调用 `agent_config` 查询模型偏好 |

### 判据：何时 fan-out 同类型 Agent

| 场景 | 策略 | 示例 |
|------|------|------|
| 3 个独立 API 模块（user/order/product） | **3 个 backend-api-expert 并行** | 各自操作 `src/api/user/`、`src/api/order/`、`src/api/product/` |
| 5 个独立前端页面/组件 | **5 个 frontend-ui-expert 并行** | 各自操作独立组件目录 |
| 2 个独立微服务 | **2 个 backend-dev-expert 并行** | 各自操作独立服务目录 |
| 同一模块内多个 API 端点（共享 Schema/中间件） | **1 个 backend-api-expert 串行处理** | 共享文件 → 并行会冲突 |
| 多个数据模型分属不同业务域 | **N 个 backend-data-expert 并行** | 各自操作独立 Schema 文件 |
| 多个独立业务逻辑模块 | **N 个 backend-logic-expert 并行** | 各自操作独立 service 文件 |

### 同一消息批量发出

```
# 3 个独立 API 模块 — 同一消息同时 spawn 3 个 backend-api-expert
Agent(backend-api-expert, "实现用户 API 模块", allowed_paths=["src/api/user/"])
Agent(backend-api-expert, "实现订单 API 模块", allowed_paths=["src/api/order/"])
Agent(backend-api-expert, "实现商品 API 模块", allowed_paths=["src/api/product/"])
# 全部在同一消息发出，并行执行
```

### 反模式

- ❌ 有 3 个独立 API 模块，却只 spawn 1 个 backend-api-expert 一个一个串行处理
- ❌ 盲目为每个文件 spawn 一个 agent（文件粒度 < 模块粒度时合并）
- ❌ 同类型 Agent 操作重叠路径（违反 file_claim 协议）
- ❌ 把同一模块拆给多个同类型 Agent（共享 Schema/中间件必然冲突）

## Gate 级并发规则

| Gate | 并发策略 | 说明 |
|------|---------|------|
| Gate A | 需求澄清 → 并行探索（explore × N） | 探索可并行 |
| Gate B-DDD/B-BDD/B-TDD | 串行 | DDD → BDD → TDD 依赖链 |
| Gate B1 | 并行架构评审 | frontend-architect + backend-architect + database-architect |
| Gate C | planner + skill-assignment 并行 | planner 和 skill-assignment-expert 同发 |
| Gate C-impl | 按 batch 内并行 | 同 batch 无冲突 → 同发；batch 间串行 |
| Gate C1 | 并行质量检查 | lint + typecheck + build + audit 同发 |
| Gate C2 | 并行测试 | unit + integration + e2e 同发 |
| Gate D | 并行审查 | 前端/后端/安全/性能审查同发 → qa-review 串行等待 |
| Gate E | 串行发布 | 质量重检 → 版本递增 → changelog → commit+tag+push |

## Agent 专用并发规则

每个 Agent 的 frontmatter 中可声明 `concurrency` 字段：

```yaml
concurrency:
  max_parallel_spawns: 4      # 此 Agent 最多并行 spawn 数
  team_preferred: false        # 是否优先使用 Team 模式
  safe_to_parallelize: true    # 此 Agent 的输出是否可被下游并行消费
```

未声明时使用默认值：max_parallel_spawns=4, team_preferred=false, safe_to_parallelize=true。

## 文件冲突防护协议

每次 spawn 实现类 Agent 必须遵循三步骤：

```
# Step 1: 预检查
file_claim_check({ run_id, paths: ["src/components/Login/", "src/hooks/useAuth.ts"] })
# → conflict_free: true → 继续
# → conflict_free: false → 调整 paths 或延后到下一 Batch

# Step 2: 注册
file_claim_register({ run_id, agent_name: "T1-frontend-login", paths: [...] })

# Step 3: 释放（Agent 完成后）
file_claim_release({ run_id, agent_name: "T1-frontend-login" })
```

- 同 Batch 内所有 Agent 的路径互不重叠（含子目录）
- 冲突检测基于路径前缀匹配：`src/a/b.ts` 与 `src/a/` 冲突
- pipeline_guide 返回当前 run 的 `file_claims`，编排者可据此调度

## Worktree 隔离规范

对于大任务（>10文件或跨≥3目录），spawn Agent 时使用 Claude Code 原生 worktree 隔离：

```

Agent({
  subagent_type: "backend-api-expert",
  isolation: "worktree",
  ...
})
```

- **何时用 worktree 隔离**：变更>10文件 或 跨≥3目录 或 Team 模式并行
- **何时用 file_claim**：≤10文件 且 单模块（worktree 有创建开销）
- **worktree vs file_claim**：worktree 是操作系统级隔离（强制），file_claim 是行为协议（协商）
- pipeline_guide 的 `isolation_guide` 字段会返回当前 Gate 的推荐隔离策略

## Agent 模型覆盖规范

用户可通过 `agent_config` MCP 工具为每个 Agent 配置专属 model。编排者 spawn Agent 时需遵守：

1. spawn 前调用 `agent_config` 查询该 agent_type 的模型偏好
2. 将查询到的 `model` 值作为 `Agent()` 的 `model` 参数传入
3. 若未配置（`is_custom: false`），使用默认模型（不传 model 参数）

```

Agent({
  subagent_type: "backend-api-expert",
  model: "opus",
  ...
})
```

> pipeline_guide 的 `model_guide` 字段会提示此流程。不传 model 参数会导致所有 Agent 使用当前会话模型，用户配置的模型偏好将被忽略。

## 代码智能工具选择指南

Claude Code 内置 LSP 工具与 Jarvis MCP LSP 工具各有侧重，Agent 实现时按场景选择：

| 场景 | 优先使用 | 说明 |
|------|---------|------|
| 跳转到定义 | 内置 LSP(goToDefinition) | 原生支持，无需 MCP 往返 |
| 查找所有引用 | 内置 LSP(findReferences) | 原生支持 |
| 类型/文档悬停 | 内置 LSP(hover) | 原生支持 |
| 文件内符号 | 内置 LSP(documentSymbol) | 原生支持 |
| 项目级符号搜索 | 内置 LSP(workspaceSymbol) | 原生支持 |
| 查找实现 | 内置 LSP(goToImplementation) | 原生支持 |
| 调用层级 | 内置 LSP(prepareCallHierarchy) | 原生支持 |
| AST 结构化搜索 | jarvis_ast_search | 语法树匹配，比文本 Grep 精确 |
| AST 安全替换 | jarvis_ast_replace | dryRun 预览后再应用 |
| 秒级诊断 | jarvis_lsp_diagnostics | 无需编译，快速反馈 |
| 重命名符号 | jarvis_lsp_prepare_rename/rename | 全仓同步 |
| 代码操作 | jarvis_lsp_code_actions | 自动修复/重构 |

> 内置 LSP 用于**导航和理解**，Jarvis MCP LSP 用于**诊断和重构**。两者互补，不可互相替代。

## 文档产出与确认

1. Gate A（需求澄清）：与用户对话确认需求后，直接产出需求文档到 `.jarvis/YYYY-MM-DD/requirements/`，然后 `advance_gate` 推进
2. Gate C（执行规划）：planner 读取 Gate B 的任务文档，自动生成执行计划（含 parallel_batches + required_skills）到 `.jarvis/YYYY-MM-DD/plans/`，产出后自动 `advance_gate` 推进，无需用户确认
3. 其他文档产出 Gate：产出对应文档后立即 `advance_gate`，不在中间插入交互阻断

## 反模式（禁止）

- ❌ 串行 spawn 无依赖的 Agent（浪费轮次）
- ❌ 小任务（<5 文件）创建 Team（过度开销）
- ❌ 共享文件的并发写入（必然冲突）
- ❌ 等待 agent 结果时不发其他独立任务
- ❌ 测试和审查并发执行（审查依赖测试报告）
- ❌ 跳过 file_claim_check 直接 spawn（文件冲突不可追溯）
- ❌ **同类型 Agent 串行化**：有 3 个独立 API 模块却只 spawn 1 个 backend-api-expert 逐个处理（应按模块并行 spawn 3 个）
- ❌ **把同一模块拆给多个同类型 Agent**（共享 Schema/中间件必然冲突→应合并为 1 个）
