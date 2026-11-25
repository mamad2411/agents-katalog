---
name: base-workflow
description: Use when driving a full development workflow (task creation, IDL changes, coding, deployment, testing, wrap-up) or resuming a prior workflow session via status.json.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# 基础研发流程手册

> **核心原则**：整个研发流程由 `.gdpa/{session-id}/status.json` 驱动。每次执行前先读取状态文件，确认当前阶段；每步操作后更新状态文件。
> **Session-ID 约束（workflow 专用）**：`gdpa-cli run` 全局不再强制要求 `--session-id`，但本 workflow 必须在整条链路里显式复用同一个 `--session-id <session_id>`。CLI 不会自动把 Session-ID 注入到 Skill 输入；如果漏传或中途更换，会导致 `.gdpa/{session-id}/status.json`、阶段产物、恢复点以及部分基于 Session 的排障信息断链。

---

## 强制执行约束（必须遵守）

**以下规则优先级最高，违反任何一条都视为执行失败：**

1. **命令失败时如实报告，不可伪造成功** — 如果 `gdpa-cli` 命令执行失败，**必须如实向用户报告错误**并排查修复，不可跳过或伪造结果。
2. **调用 `gdpa-cli` 前必须先阅读对应 Skill** — 了解完整的参数格式、输入输出 Schema 和使用示例，确保命令参数正确。不要凭记忆或猜测拼写命令。

---

## 一、启动与恢复

**每次收到用户指令时，按以下顺序执行：**

### 0. 确定本次 workflow 使用的 session_id
- **当前对话或用户输入已提供 session_id**：直接复用这个值
- **未提供**：立即执行 `gdpa-cli create-session`，使用返回的 session_id
- **拿到后**：后续所有 `gdpa-cli run` 命令都必须显式追加同一个 `--session-id <session_id>`

### 1. 检查是否有进行中的会话

查找 `.gdpa/` 目录下是否有已存在的会话（`{session-id}/status.json`）：

- **存在 `status.json`**：读取文件，根据 `current_phase` 和 phase `status` 恢复到对应阶段继续执行
- **不存在**：使用当前 `session_id` 初始化新的 `.gdpa/{session-id}/status.json`

> 完整的 status.json 结构与初始化模板见 [status-schema.md](status-schema.md)

### 2. 恢复会话

读取 `status.json` 后，按 `current_phase` 定位到对应阶段：

| phase status | 行为 |
|-------------|------|
| `pending` | 开始该阶段 |
| `in_progress` | 从上次中断处继续（结合 `history` 判断进度） |
| `completed` | 跳到下一个阶段 |
| `skipped` | 跳到下一个阶段 |
| `failed` | 分析 `summary` 中的失败原因，尝试修复或询问用户 |

---

## 二、阶段定义与状态流转

### 流转总览

```
info_collection
  ↓ ◆ 执行计划确认
task_setup → idl_change（可跳过）
  ↓ ◆ 设计方案确认
coding → deploy
  ↓ ◆ 测试方案确认
testing → completion
  ↑         │
  └─────────┘（测试不通过时回退）
```

◆ = 确认检查点（必须等待用户确认后才能继续）

各阶段 `status` 值：`pending` → `in_progress` → `completed` / `skipped` / `failed`

---

### 确认检查点机制

工作流在三个关键节点设置了确认检查点。这些检查点的作用是让用户在投入实际工作之前审查方案、发现问题、调整方向——越早发现偏差，修正成本越低。

**检查点清单**：

| 检查点 | 触发时机 | 确认内容 | 目的 |
|--------|---------|---------|------|
| 执行计划确认 | info_collection 完成后 | 全流程计划、各阶段要做什么、预期风险 | 对齐全局预期，避免方向性错误 |
| 设计方案确认 | idl_change 完成/跳过后、coding 开始前 | 技术方案、修改范围、依赖分析、关键决策 | 确保实现思路正确，避免返工 |
| 测试方案确认 | deploy 完成后、testing 开始前 | 测试用例、覆盖范围、预期结果、验证标准 | 确保测试充分，不遗漏关键场景 |

**执行规则**：
- 每个检查点必须向用户展示结构化的方案文档，等待用户回复"确认"后才能继续
- 用户可以回复修改意见，模型需要调整方案后重新展示，直到用户确认
- 检查点确认记录写入 `status.json` 的 `checkpoints` 字段和 `history` 中
- 产出文件保存在对应阶段的目录下（如 `info/execution_plan.md`）

---

### Phase 0: info_collection (信息收集与确认)

> **目标**：在开始执行前，收集并确认所有必要参数，确保后续流程自动化执行的准确性。

**入口条件**：收到用户的研发需求

**操作步骤**：

1. **检查本地分支**：
   - 如果当前分支 **不是** `master` 或 `main`：默认使用当前分支作为开发分支。
   - 如果当前分支 **是** `master` 或 `main`：根据需求生成一个新的分支名称（如 `feature-xxx`），并在确认单中要求用户确认。
2. **分析需求**：从用户输入中提取关键信息（PSM、分支、业务线、是否变更 IDL 等）。
3. **交互确认**：**必须**向用户展示以下确认表单（Markdown 格式），并等待用户确认 "yes" 或提供修改意见。

**确认表单模板**：

```markdown
## 🚀 研发任务确认单

请确认以下信息是否正确：

| 配置项 | 当前值 | 说明 |
|--------|--------|------|
| **需求描述** | <提取的需求摘要> | 简要描述本次研发任务的目标 |
| **PSM** | `tiktok.xxx.xxx` | 目标服务 PSM |
| **业务线 (Biz)** | `Tiktok` | 仅以下可选: Tiktok/Aweme/Devflow/Tikcast |
| **开发分支** | `feature-xxx` | 将使用的 Git 分支（如本地为 master，此处为建议的新分支名） |
| **变更 IDL** | `是/否` | 是否涉及 IDL 修改 |
| **环境 (Env)** | `ppe` | 默认 ppe，可选 boe/ppe+boe |
| **区域 (Region)** | `i18n` | 默认 i18n，可选 cn |

> 回复 "确认" 或 "yes" 继续执行；回复具体修改项进行调整（如 "分支改为 fix-bug"）。
```

4. **修正参数**：根据用户反馈更新参数，直到用户确认。

#### ◆ 检查点：执行计划确认

用户确认基本参数后，分析需求并生成完整执行计划。向用户展示以下文档，等待确认后再进入 task_setup。

之所以在这里停下来，是因为后续操作（创建 DevFlow 任务、编辑 IDL、部署等）一旦启动就涉及外部系统变更，提前对齐计划可以避免方向性错误。

**执行计划模板**：

```markdown
## 📋 执行计划

基于需求分析，以下是本次研发的完整执行计划：

### 阶段概览

| # | 阶段 | 执行/跳过 | 具体内容 |
|---|------|----------|---------|
| 1 | 任务准备 | ✅ 执行 | 创建 DevFlow 任务，配置 {env} 环境 |
| 2 | 接口变更 | ✅/⏭️ | {需修改 xxx.thrift / 无需 IDL 变更} |
| 3 | 代码编写 | ✅ 执行 | {实现 xxx 功能的概要描述} |
| 4 | 提交部署 | ✅ 执行 | Push 到 {branch}，触发部署 |
| 5 | 测试验证 | ✅ 执行 | {测试 xxx 接口} |
| 6 | 完成收尾 | ✅ 执行 | 生成报告，按需发起 MR |

### 预期涉及的关键操作

1. {操作1: 如 "在 xxx.thrift 中新增 YYY 字段"}
2. {操作2: 如 "修改 handler.go 和 service.go 实现 YYY 逻辑"}
3. {操作3: 如 "调用 bam-api 查询下游 ZZZ 接口定义"}

### 潜在风险与注意事项

- {风险1: 如 "下游 ZZZ 服务的接口兼容性需确认"}
- {风险2: 如 "涉及写接口，测试时需谨慎"}

> 回复 "确认" 开始执行；回复修改意见调整计划。
```

将确认后的执行计划保存为 `info/execution_plan.md`。

**退出条件**：用户明确确认参数 + 执行计划（"yes"/"确认"）

**产出文件**：
- `info/task_config.json`（确认后的参数配置）
- `info/execution_plan.md`（确认后的执行计划）

> 完成检查：`task_config.json` + `execution_plan.md` 都存在 → 标记 completed

---

### Phase 1: task_setup（任务准备）

> 使用 `devflow` Skill 完成。**调用前必读该 Skill。**

**入口条件**：用户提供了需求描述

**操作步骤**（必须在终端实际执行，禁止跳过或模拟）：

1. **切换分支**：如果当前本地分支是 `master` 或 `main`，且 Phase 0 确认了新的开发分支，**必须先执行 `git checkout -b <new_branch>` 切换到新分支**，再进行后续操作。
2. **检查已有任务**：如用户已提供 task_id 或 PSM+分支，检查是否有可复用的 `OPEN` / `DEV_IN_PROCESS` 任务
3. **创建新任务**（无可复用任务时）：与用户确认 PSM、分支名、环境（默认 PPE）
4. **启动开发调试**

**退出条件**：获得 task_id、branch、PSM、env、vregion、vdc、lanes（必须来自 `gdpa-cli run devflow` 的实际返回值）

> **重要**：创建任务后必须执行 `devflow develop-detail <task_id>` 获取完整的部署信息。从返回结果中提取：
> - **Env** → `context.env`（完整环境名，如 `ppe_20260211`，**不是** `ppe`）
> - **VRegion** → `context.vregion`（标准 VRegion 数组，如 `["Singapore-Central", "US-East"]`）
> - **VDC** → `context.vdc`（VDC 数组，如 `["sg1", "maliva"]`）

**产出文件**：`devflow/task_info.json`（task_id、PSM、分支、env、vregion、vdc、泳道、流水线链接）

> 完成检查：`task_info.json` 存在且 task_id 有效 → 标记 completed

---

### Phase 2: idl_change（接口变更）

> **调用前必读 `edit-idl` Skill。** 按 `edit-idl` 编排指南，依次调用：`idl-pull` → 本地编辑 → `idl-commit` → `idl-codegen`。

**入口条件**：`task_setup` 已完成

**跳过判断**：需求不涉及 IDL/接口变更 → 标记为 `skipped`，直接进入 coding
> **注意**：如果需求涉及**新增 Endpoint**，必须走 IDL 编辑流程。该流程不仅会编辑 IDL，还会触发代码生成，生成新 Endpoint 的相关代码。

**重要约束**：
- **`base.thrift` 不可修改**，修改可能导致下游代码生成失败。
- **分支对齐**：三个 Agent 的 branch 参数必须与业务代码分支一致 — `idl-pull.branch == idl-commit.branch == idl-codegen.branch == context.branch`。
- **禁止提交到 `master`**：`idl-commit.branch` 必须使用 `context.branch`（feature 分支），不得改为 `master`。
- **fallback 不改变提交分支**：即使 `idl-pull` 因分支不存在 fallback 到 `master` 拉取，也仍然要向 `context.branch` 提交；若该分支不存在，`idl-commit` 会自动创建。

**操作步骤**：

1. **拉取 IDL 文件**（`idl-pull`）：
   - 使用临时目录存放 IDL（如 `/tmp/gdpa-idl/<task-id>` 或 `.tmp/gdpa-idl/<task-id>`）
   - `branch` 从 `context.branch` 读取；若请求分支在 IDL 仓库不存在，`idl-pull` 会自动 fallback 到 `master` 并报告
   - 输出的 `meta_path`（`.gdpa_idl_meta.json`）在后续 commit 阶段需要使用
2. **本地编辑 IDL 文件**：在拉取的临时目录中修改 `.thrift` / `.proto` 文件（跳过 `base.thrift`）
3. **提交 IDL 变更**（`idl-commit`）：
   - 传入 `meta_path`（来自 idl-pull 输出）和 `branch=context.branch`（feature 分支）
   - 不要把 `idl-pull` 返回的 `branch_used=master` 误用于 commit 分支
   - 若分支不存在会自动创建
   - 提交完成后自动创建 BAM 版本
4. **触发代码生成**（`idl-codegen`）：
   - 传入 `psm`、`branch`、`mode`（推荐 `auto`，也可指定 `overpass` / `gdp_remote`）
   - 若使用 `gdp_remote` 需额外传入 `prod`（默认 `tiktok`）和 `service_type`（`rpc` 或 `api`）
   - 等待代码生成完成，获取 `go_get_cmds` 更新本地依赖
   - 如果返回 `status: running`，使用 `action: query_status` 轮询直到完成
5. **清理临时目录**：代码生成验证通过后，清理临时 IDL 目录

**退出条件**：IDL 提交成功 + 代码生成状态为 `success`

**产出文件**：`edit-idl/diff_result.json`（IDL 路径、变更摘要、commit 信息、codegen 结果、go_get_cmds）

> 完成检查：`diff_result.json` 存在且 codegen `status` 为 `success` → 标记 completed

---

### Phase 3: coding（代码编写）

**入口条件**：`idl_change` 完成或跳过

#### ◆ 检查点：设计方案确认

在写任何代码之前，先分析需求并展示技术设计方案。这一步的价值在于：代码一旦写出来，修改方向的成本远高于在纸面上调整——特别是当涉及多个文件、依赖下游服务、或有多种实现方式可选时。

结合 IDL 变更结果（如有）、需求描述、以及通过 Skill（如 `bam-api`、`repotalk`、`tcc-query`）获取的上下文信息，生成设计方案并展示给用户。

**设计方案模板**：

```markdown
## 🔧 设计方案

### 实现思路
{对需求的技术分析，说明整体实现方案}

### 修改范围

| 文件 | 修改内容 | 说明 |
|------|---------|------|
| handler.go | 新增 XXX Handler | 处理新接口请求 |
| service.go | 添加 XXX 业务逻辑 | 实现核心功能 |
| model.go | 新增/修改结构体 | 数据模型适配 |

### 依赖分析
- **下游服务**: {需要调用的下游服务及接口}
- **配置依赖**: {需要读取的 TCC 配置项}
- **数据依赖**: {需要访问的数据库表}

### 关键设计决策

| 决策点 | 选择方案 | 理由 |
|--------|---------|------|
| {决策1} | {方案A} | {选择原因} |
| {决策2} | {方案B} | {选择原因} |

> 回复 "确认" 开始编码；回复修改意见调整方案。
```

将确认后的设计方案保存为 `coding/design_proposal.md`。用户确认后，开始实际编码。

**操作步骤**：
1. 按需调用对应 Skill 获取 context 来实现需求，编写代码。
2. **本地编译验证**（必须执行）：在提交代码前，必须确保本地编译通过（如执行 `go build ./...` 或 `./build.sh`）。如果编译失败，必须修复错误直到编译成功，**禁止提交无法编译的代码**。
3. 完成基本本地验证（如运行关键单测）。

> 可用 Skill 及选择指南见 [skills-reference.md](skills-reference.md)

**Repotalk 查询策略**：按 `get_repos_detail` → `get_packages_detail` → `get_files_detail` → `get_nodes_detail` 逐级深入，鼓励递归调用 `get_nodes_detail` 追踪间接依赖。

**退出条件**：代码编写完成 + **本地编译通过** + 本地验证通过

**产出文件**：
- `coding/design_proposal.md`（确认后的设计方案）
- `coding/changes.json`（变更摘要、修改文件列表、使用的 Skill 列表）

> 完成检查：`design_proposal.md` + `changes.json` 存在且 `files_modified` 非空 → 标记 completed

---

### Phase 4: deploy（提交部署）

**入口条件**：`coding` 已完成

**操作步骤**（部署状态必须通过 `devflow` Skill 确认，禁止假设部署成功）：

1. 提交代码并 Push 到远程分支（分支名从 `context.branch` 读取）
2. Push 后自动触发 BOE/PPE 部署
3. 通过 `devflow` Skill 确认部署状态（检查泳道流水线，`task_id` 从 `context.task_id` 读取）

**退出条件**：代码已 Push + 部署状态已确认

**产出文件**：`deploy/deploy_info.json`（分支、commit hash、push 状态、部署环境、DevFlow 检查结果）

> 完成检查：`deploy_info.json` 存在且 `push_success` 为 true → 标记 completed

---

### Phase 5: testing（测试验证）

> **调用前必读对应 Skill**：`bam-query`、`argos-query`、`devflow`

**入口条件**：`deploy` 已完成

**跳过判断**：用户明确表示不需要测试 → 标记为 `skipped`

#### ◆ 检查点：测试方案确认

在执行任何测试之前，先生成结构化的测试方案供用户审查。这一步能避免两类问题：遗漏关键测试场景（比如只测了一个 Region 而忘了另一个），以及误操作写接口导致脏数据。

结合 `coding/changes.json` 的变更内容和 `context` 中的环境信息，生成测试方案。

**测试方案模板**：

```markdown
## 🧪 测试方案

### 测试环境
- **Env**: {context.env}
- **VRegion**: {context.vregion 列表}
- **VDC**: {context.vdc 列表}

### 测试用例

| # | 接口/方法 | 类型 | VRegion | 测试输入 | 预期结果 |
|---|----------|------|---------|---------|---------|
| 1 | GetUserInfo | 读 | Singapore-Central | {"user_id": 123} | 返回包含新增字段 |
| 2 | GetUserInfo | 读 | US-East | {"user_id": 123} | 同上（跨 Region 验证） |
| 3 | ... | ... | ... | ... | ... |

### 日志验证计划
- **搜索关键字**: error, {相关方法名}
- **预期结果**: 无异常错误日志
- **时间范围**: 测试请求前后 5 分钟

### 注意事项
- {如有写接口: "用例 X 为写接口，需要用户明确授权才执行"}
- {其他注意事项}

> 回复 "确认" 开始测试；回复 "跳过" 跳过测试；回复修改意见调整方案。
```

将确认后的测试方案保存为 `bam-query/test_plan.md`。用户确认后，开始实际测试。

**操作步骤**（必须在终端实际执行，禁止用本地单测或 Grep 替代）：

1. **确认部署完成**：版本、实例状态符合预期
2. **发起接口测试**（使用 `bam-query` Skill）：按测试方案中的用例逐一执行，记录 request 和 response
   - **VRegion 和 env 参数必须从 `context.vregion` 和 `context.env` 读取**，使用标准 VRegion 值（如 `Singapore-Central`），不要传别名（如 `sg`、`boe`）
   - 如有多个 VRegion/VDC，需分别测试每个组合
   - 读接口可直接测试；**写接口必须用户明确授权**
3. **分析日志**（使用 `argos-query` Skill）：查看真实服务日志
   - **注意**：Argos 日志可能有 1-5 分钟延迟。如果首次查询未找到预期日志，**必须**提示用户日志可能有延迟，建议稍作等待（如 30-60 秒）后再次查询，而不是直接报告失败。
4. **结果判断**：通过 → 进入 completion；不通过 → 记录失败原因，回退到 coding

**产出文件**：

- `bam-query/test_result.json`（测试用例及结果）
- `argos-query/logs_summary.md`（日志分析摘要）
- `argos-query/logs_raw.log`（原始日志，大量日志时写入）

> 完成检查：`test_result.json` + `logs_summary.md` 都存在 → 标记 completed
>
> 测试不通过时：`current_phase` 回退到 coding，testing 标记 `failed`，coding 标记 `in_progress`

---

### Phase 6: completion（完成收尾）

**入口条件**：`testing` 完成或跳过

**操作步骤**：

1. **研发总结**：整理变更内容、影响范围、关键决策
2. **发起 MR**（按需）：关联 Meego 任务，MR 描述引用自测报告
3. **关闭 DevFlow 任务**（按需，详见 `devflow` Skill）

**产出文件**：`summary/report.md`（研发总结，汇总所有阶段产出）

> 完成检查：`report.md` 存在 → 标记 completed

---

## 三、状态文件规范

> 完整 status.json 结构见 [status-schema.md](status-schema.md)

### 3.1 状态更新规则

**必须在以下时机更新 status.json**：

| 时机 | 更新内容 |
|------|---------|
| 进入新阶段 | `current_phase`、该阶段 `status` → `in_progress`、`started_at` |
| 完成当前阶段 | 该阶段 `status` → `completed`、`completed_at`、`summary`；`current_phase` → 下一阶段 |
| 跳过阶段 | 该阶段 `status` → `skipped`、`summary` 注明跳过原因 |
| 阶段失败 | 该阶段 `status` → `failed`、`summary` 注明失败原因 |
| 回退阶段 | `current_phase` 回退、目标阶段 `status` → `in_progress` |
| 关键操作完成 | 追加 `history` 条目 |
| context 信息变更 | 更新 `context` 对应字段 |

### 3.2 各阶段产出文件

每个阶段完成时**必须**写入对应的产出文件。`summary` 字段必须包含产出文件路径（格式：`→ 文件路径`）。

| 阶段 | 产出文件 | 完成检查条件 |
|------|---------|-------------|
| `info_collection` | `info/task_config.json` + `info/execution_plan.md` | 两个文件都存在 |
| `task_setup` | `devflow/task_info.json` | 文件存在且 task_id 有效 |
| `idl_change` | `edit-idl/diff_result.json` | 文件存在且 idl_codegen.status=success（skipped 时无需产出） |
| `coding` | `coding/design_proposal.md` + `coding/changes.json` | 两个文件都存在且 files_modified 非空 |
| `deploy` | `deploy/deploy_info.json` | 文件存在且 push_success=true |
| `testing` | `bam-query/test_plan.md` + `bam-query/test_result.json` + `argos-query/logs_summary.md` | 三个文件都存在（skipped 时无需产出） |
| `completion` | `summary/report.md` | 文件存在 |

完整目录结构：

```
.gdpa/{session-id}/
├── status.json                    # 流程状态（核心，每步更新）
├── info/
│   ├── task_config.json           # info_collection 产出
│   └── execution_plan.md          # ◆ 执行计划确认产出
├── devflow/
│   └── task_info.json             # task_setup 产出
├── edit-idl/
│   └── diff_result.json           # idl_change 产出（skipped 时不存在）
├── coding/
│   ├── design_proposal.md         # ◆ 设计方案确认产出
│   └── changes.json               # coding 产出
├── deploy/
│   └── deploy_info.json           # deploy 产出
├── bam-query/
│   ├── test_plan.md               # ◆ 测试方案确认产出（skipped 时不存在）
│   └── test_result.json           # testing 产出（skipped 时不存在）
├── argos-query/
│   ├── logs_raw.log               # testing 产出（大体量日志）
│   └── logs_summary.md            # testing 产出（skipped 时不存在）
└── summary/
    └── report.md                  # completion 产出
```

### 3.3 使用规则

1. **每步四拍节奏**：读 status → 执行操作 → 写产出文件 → 更新 status（缺一不可）
2. **产出文件是硬约束**：标记 `completed` 前必须先写入对应产出文件
3. **history 记录 wrote_file**：每次写入产出文件后，在 `history` 中追加 `{"action": "wrote_file", "detail": "文件路径"}`
4. **大输出走文件**：大体量输出（如 argos 日志）写入文件，对话 context 仅传摘要 + 文件路径
5. **Session 隔离**：每次研发流程使用独立 `session-id`，互不干扰
6. **Git 忽略**：`.gdpa/` 目录应加入 `.gitignore`
7. **Context 优先读 status**：PSM、分支、env、vregion、vdc 等信息统一从 `context` 读取，不重复询问用户
8. **Skipped 阶段无需产出**：被标记为 `skipped` 的阶段不需要写产出文件
9. **产出必须基于真实数据**：产出文件数据必须来自 `gdpa-cli` 命令的真实返回，禁止编造
10. **默认环境**：默认部署 i18n PPE 环境。env、vregion、vdc 均以 `devflow develop-detail` 的返回为准
11. **使用标准 VRegion**：调用 `bam-query`、`argos-query` 等 Skill 时，vregion 参数必须使用标准值（`Singapore-Central`、`US-East`、`China-North`、`China-BOE`、`US-BOE`），不要传别名

---

## 四、附加资源

- 完整 status.json 结构与初始化模板 → [status-schema.md](status-schema.md)
- 各阶段产出文件与状态更新 JSON 示例 → [phase-examples.md](phase-examples.md)
- 可用 Skill 速查与选择决策指南 → [skills-reference.md](skills-reference.md)
