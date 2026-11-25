---
name: vibe-autopilot
description: Use this skill when the user requests fully autonomous, 24/7 hands-free development without human intervention.
---

# 自动驾驶工作流 (Autopilot 24/7)

## 1. 文档目的
赋予 AI “全自动、不间断”的执行能力。在需求沟通阶段充分提问与确认，但一旦进入正式开发阶段，自动串联所有 VIBE 工作流（编码 -> 测试 -> 审查 -> 迭代），**期间禁止停顿等待用户确认，自动采用最优解执行**，直到最终交付。

## 2. 自动驾驶核心法则 (Smart Autopilot)
- **需求期充分沟通**：在需求分析和架构设计阶段，必须主动向用户提问，澄清模糊点，确保方向完全正确。
- **开发期绝对静默 (NO HUMAN PAUSES)**：一旦需求确认并进入正式编码阶段（阶段二），**禁止提问**。除非遇到严重且无法自行解决的环境死锁，否则禁止使用“您看这样可以吗？”、“需要我继续吗？”等话术，遇到分支选择时**直接采用最优解**。
- **状态机依赖 (Document as State)**：禁止依赖大脑记忆！所有的进度、状态必须实时更新到 `tasks.md` 中。如果感觉上下文变慢或混乱，主动提示用户使用 `/clear` 清理上下文，随后读取 `tasks.md` 即可满血复活。
- **事不过三熔断机制 (Circuit Breaker)**：在处理报错、跑测试或解决依赖冲突时，如果**同一个问题连续尝试修复超过 3 次均失败**，必须立即停止死磕！将该任务在 `tasks.md` 中标记为 `[Blocked]`，记录原因，然后**强制跳过，去执行下一个未完成的任务**。

## 3. 24小时全链路循环引擎
当用户触发此工作流时，严格按照以下顺序执行：

### 阶段一：需求沟通与架构规划（允许且鼓励提问）
1. **自动执行 `vibe-analyze-req`**：当用户是从头开始一个全新项目时，触发此技能。与用户进行多轮对话，澄清项目背景、核心功能、UI 风格（如深色工业风）等细节。
2. （如果是已有项目的新需求，则触发 `vibe-analyze-new`）。
3. **生成核心文档**：确认需求后，生成 PRD（需求文档），并自动执行 `vibe-architecture` 和 `vibe-database` 生成架构与数据库文档。
4. 自动执行 `vibe-plan` 生成 `tasks.md`（任务拆解清单）。
5. **最后一次确认**：向用户展示 `tasks.md` 并询问“是否可以开始全自动开发？”。一旦用户同意，进入阶段二。

### 阶段二：无人值守编码循环 (Subagent-Driven Loop - 开发期绝对静默)
由于 AI 上下文窗口有限，对于 `tasks.md` 中的复杂任务，必须采用**子智能体分发（Subagent Delegation）**策略。
读取 `tasks.md` 中的任务，针对每一个未完成的最小模块任务执行以下死循环（**全自动，零打断，遇问题按最优解自动处理**）：
1. **工作树隔离 (Git Worktree / Branching)**：在开始新任务前，建议在一个新的 Git 分支上进行开发，确保主分支的安全。
2. **API契约校验**：确认该模块对应的 API 文档已存在，严格按照 API 文档的入参/出参约束进行开发。
3. **最小模块编码 (企业级分层)**：
   - 隔离上下文，仅针对当前**最小模块**生成代码。
   - 严格遵循企业级规范（前端：Components/Hooks/API Clients；后端：Controller/Service/Repository）。
   - 自动触发 `vibe-frontend` 或 `vibe-backend`。
4. **测试与组装**：编码完毕后，立即触发 `vibe-test` 运行单元测试（RED-GREEN-REFACTOR），将通过测试的模块与其他模块进行组装。
   - 如果测试失败：自动修复代码，重新运行。
   - 如果测试成功：进入下一步。
5. **安全与质量**：触发 `vibe-security` 与 `vibe-review` 检查当前代码块。
6. **美化**（如果是前端任务）：触发 `vibe-ui-beautify` 注入工业风和“果汁感”动画。
7. **打勾**：在 `tasks.md` 中将该任务标记为已完成 `[x]`，并提交代码 (Git Commit)。
8. **继续**：自动读取下一个 `[ ]` 任务，重复阶段二，直至系统拼装完毕。

### 阶段三：自动交付与文档更新
1. **端到端真机验证**：所有任务完成后，触发 `vibe-e2e` 启动项目、打开浏览器、逐页验证功能可用性。P0/P1 问题必须修复后才能继续交付。
2. 自动触发 `vibe-api-docs` 更新接口文档。
3. 自动更新 `AI_DEVELOPMENT_DOC.md` 记录本次无人值守开发过程中的踩坑和经验。
4. 向用户输出最终的**交付总结报告**。

## 4. 异常跳出条件
只有在以下情况发生时，才允许中断 24 小时工作流并向用户求助：
1. 缺少必要的 API 密钥（如第三方服务必须用户手动注册）。
2. 服务器端口被彻底占死，且 AI 尝试了 3 种杀进程方案均失败。
3. 用户的需求描述中存在致命的逻辑悖论（例如要求“不用数据库，但要持久化存储TB级关联数据”），且 AI 无法做出合理假设。

## 5. 启动指令示例
当接收到类似 `开启全自动开发`、`autopilot`、`24小时不间断` 的指令时，立即进入此状态。

## 6. 子智能体并行调度 (Parallel Subagent Orchestration)
**核心原则：能并行就并行，不能并行才串行。** 使用 Claude Code 的 Task 工具启动子智能体，每个子智能体拥有独立上下文窗口，避免记忆污染。

### 6.1 并行调度决策树
```
读取 tasks.md 当前阶段的任务清单
    ↓
分析任务间的依赖关系
    ├─ 无依赖 → 全部并行启动
    ├─ 部分依赖 → 分批并行（先并行执行无依赖的，再执行依赖项）
    └─ 全串行依赖 → 顺序执行
```

### 6.2 并行调度模板
**场景**：阶段二有 5 个任务，其中前端任务 A/B/C 互相独立，后端任务 X/Y 互相独立。

**错误做法（串行）**：
```
任务A → 任务B → 任务C → 任务X → 任务Y（耗时长，上下文累积）
```

**正确做法（并行）**：
```
同一消息内启动多个 Task 工具调用：
  ├── Task(subagent_type="general_purpose_task"): 前端任务A
  ├── Task(subagent_type="general_purpose_task"): 前端任务B
  ├── Task(subagent_type="general_purpose_task"): 前端任务C
  ├── Task(subagent_type="general_purpose_task"): 后端任务X
  └── Task(subagent_type="general_purpose_task"): 后端任务Y
所有子智能体完成后：
  → 合并代码
  → 运行集成测试
  → vibe-review 审查
  → vibe-security 扫描
```

### 6.3 子智能体任务模板
每个并行子智能体的任务描述必须包含：
1. **身份声明**：你是 VIBE 流水线的前端/后端工程师
2. **任务范围**：只实现 xxx 模块，不触碰其他模块
3. **API 契约**：引用对应的 API 文档路径
4. **设计令牌**：引用 vibe-ui-design 的 token 文件（前端任务）
5. **完成后**：写代码 + 跑测试 + 报告结果

### 6.4 并行安全规则
- **文件隔离**：每个子智能体只能修改自己模块的文件，禁止跨模块修改
- **共享文件只读**：API 文档、设计令牌、tasks.md 对子智能体是只读的
- **合并冲突预防**：vibe-plan 在拆解任务时必须确保模块间文件不重叠
- **并行上限**：同时并行的子智能体不超过 5 个（Claude Code 限制）

## 7. 进度可视化面板 (Progress Dashboard)
**原则：用户随时能看到进度，不用盯终端。**

### 7.1 进度文件生成
每完成一个任务后，更新 `.vibe/progress.html`：

```html
<!DOCTYPE html>
<html>
<head><title>VIBE Progress</title></head>
<body>
  <h1>VIBE 自动驾驶进度</h1>
  <div class="summary">
    <div class="stat">总任务: 15</div>
    <div class="stat done">已完成: 8</div>
    <div class="stat active">进行中: 2</div>
    <div class="stat blocked">阻塞: 1</div>
    <div class="stat pending">待执行: 4</div>
    <div class="progress-bar"><div class="fill" style="width: 53%"></div></div>
  </div>
  <table>
    <tr><th>任务</th><th>类型</th><th>状态</th><th>耗时</th></tr>
    <tr><td>用户接口-注册</td><td>后端</td><td>✅</td><td>2m</td></tr>
    <tr><td>登录页面</td><td>前端</td><td>🔄</td><td>1m</td></tr>
    <tr><td>JWT 鉴权</td><td>后端</td><td>⛔ Blocked</td><td>5m</td></tr>
  </table>
</body>
</html>
```

### 7.2 更新规则
- 每完成一个任务 → 更新 `progress.html`
- 每开始一个任务 → 状态改为 🔄
- 每标记 Blocked → 状态改为 ⛔ + 原因
- 用户可随时在浏览器打开 `.vibe/progress.html` 查看进度

## 8. 错误自动恢复 (Auto-Recovery)
**原则：Blocked 不是终点，是暂停。**

### 8.1 二次尝试机制
当所有其他任务完成后，对 `[Blocked]` 任务进行二次尝试：

1. **换思路**：不复用之前的代码，从零开始换一种实现方案
2. **搜索参考**：用 WebSearch 搜索类似问题的解决方案
3. **简化需求**：如果原需求过于复杂，降级为最小可行版本
4. **二次失败**：标记为 `[Needs Human]`，在交付报告中详细说明

### 8.2 恢复流程
```
所有非 Blocked 任务完成
    ↓
扫描 tasks.md 中的 [Blocked] 任务
    ↓
对每个 Blocked 任务：
  ├─ 分析失败原因（读取 tasks.md 中的记录）
  ├─ WebSearch 搜索解决方案
  ├─ 换一种实现思路重写
  ├─ 跑测试验证
  ├─ 通过 → 标记 [x]，继续下一个
  └─ 仍失败 → 标记 [Needs Human]
    ↓
所有任务处理完毕 → 进入阶段三交付
```

### 8.3 交付报告中的 Blocked 说明
对于最终仍标记为 `[Needs Human]` 的任务，交付报告必须包含：
- 任务名称
- 失败原因（技术细节）
- 已尝试的方案列表
- 建议的人工解决方向
- 相关文件路径
