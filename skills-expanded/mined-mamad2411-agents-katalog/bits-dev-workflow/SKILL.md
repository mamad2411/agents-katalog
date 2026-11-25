---
name: bits-dev-workflow
description: Use when driving a BITS DevOps workflow (task creation, deployment, testing, code review, stage pass, wrap-up) or resuming a prior workflow session via status.json. Also trigger when the user mentions BITS development workflow, BITS DevOps workflow, or wants to create a BITS dev task and run the deployment + testing cycle. This is for BITS DevOps based workflows — for DevFlow based workflows use base-workflow instead.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# BITS DevOps 研发流程手册

> **核心原则**：整个研发流程由 `.gdpa/{session-id}/status.json` 驱动。每次执行前先读取状态文件，确认当前阶段；每步操作后更新状态文件。
> **Session-ID 约束（workflow 专用）**：`gdpa-cli run` 全局不再强制要求 `--session-id`，但本 workflow 仍然必须在整条链路里显式复用同一个 `--session-id <session_id>`。CLI 不会自动把 Session-ID 注入到 Skill 输入；如果漏传或中途更换，`.gdpa/{session-id}/status.json`、阶段产物和恢复链路都会断开。

---

## 强制执行约束（必须遵守）

**以下规则优先级最高，违反任何一条都视为执行失败：**

1. **命令失败时如实报告，不可伪造成功** — 如果 `gdpa-cli` 命令执行失败，**必须如实向用户报告错误**并排查修复，不可跳过或伪造结果。
2. **调用 `gdpa-cli` 前必须先阅读对应 Skill** — 了解完整的参数格式、输入输出 Schema 和使用示例，确保命令参数正确。不要凭记忆或猜测拼写命令。
3. **关键信息须用户感知和确认** — 每个阶段在执行前，将所有需要用户输入或确认的信息汇总展示，让用户统一确认。如能提前通过 API 获取选项列表，优先展示选项让用户选择。
4. **必须创建 session 目录并维护 status.json** — 无论是创建新任务还是复用已有任务，都**必须**在 `.gdpa/{session-id}/` 下创建目录、初始化 `status.json`，并在每一步操作后写入产出文件和更新状态。不可跳过状态文件的创建和维护。

---

## 一、启动与恢复

**每次新对话的第一个操作，必须严格按以下顺序执行。不可跳步、不可调换顺序。**

### Step 0：创建 session（第一个动作，无条件执行）

> **这是整个流程的第一个动作，必须在做任何其他事情之前执行。**
> **不要先去查看 .gdpa/ 目录、不要先 ls、不要先检查是否有旧 session。**

**执行**：`gdpa-cli create-session`

- 记住返回的 `session_id`（例如 `sess_20260305_180000_abcd1234`）
- 后续所有 `gdpa-cli run` 命令都通过 `--session-id <session_id>` 传递

**唯一例外**：本次对话中已经执行过 `create-session` 并获得了 `session_id`，则直接使用，不重复创建。

### Step 1：初始化 session 目录和 status.json

拿到 `session_id` 后，**立即**执行：

```bash
mkdir -p .gdpa/{session-id}
```

然后在 `.gdpa/{session-id}/status.json` **写入**初始化内容（使用 [status-schema.md](status-schema.md) 中的初始化模板）。

> 完整的 status.json 结构与初始化模板见 [status-schema.md](status-schema.md)
>
> **关键**：后续每个阶段的产出文件也必须实际写入 `.gdpa/{session-id}/` 对应子目录，不可省略。

### Step 2：恢复已有流程（仅限用户主动提供 session_id 时）

> **此步骤仅在用户明确说"恢复 session XXX"或提供了一个已有的 session_id 时才执行。**
> 如果用户没有提供旧 session_id，则跳过此步骤，直接从 Phase 0 开始。

读取用户指定的 `.gdpa/{用户提供的session-id}/status.json`，按 `current_phase` 定位到对应阶段：

| phase status | 行为 |
|-------------|------|
| `pending` | 开始该阶段 |
| `in_progress` | 从上次中断处继续（结合 `history` 判断进度） |
| `completed` | 跳到下一个阶段 |
| `skipped` | 跳到下一个阶段 |
| `failed` | 分析 `summary` 中的失败原因，尝试修复或询问用户 |

---

## 二、Space ID 管理

BITS DevOps 操作依赖 `space_id`（BITS 空间 ID）。采用以下规范管理：

### 读取规则

1. **首先检查 `.gdpa/bits-devops.yaml`**：

```yaml
# BITS DevOps 空间配置（自动生成，请勿手动删除）
space_id: 94017024770
```

2. **如果文件不存在**：调用 `bits-devops` 的 `get_recent_spaces` 获取用户最近访问的空间列表，展示给用户选择：

```markdown
### 请选择 BITS 空间

以下是你最近访问的 BITS 空间：

| # | 空间 ID | 名称 | 标识 | 说明 |
|---|---------|------|------|------|
| 1 | 94017024770 | gdp_workplace | gdp_workplace | |
| 2 | 1058659382530 | gdpa_verifier | gdpa_verifier | GDPA 代码推改自动化测试 |

> 回复序号选择，或直接输入 space_id。
```

3. **用户选择后**：将 `space_id` 保存到 `.gdpa/bits-devops.yaml`（需先 `mkdir -p .gdpa/`），后续直接从文件读取，不再重复询问

> `.gdpa/bits-devops.yaml` 存放在 `.gdpa/` 目录下用于长期存放，跨 session 共享。

---

## 三、阶段定义与状态流转

### 流转总览

```
info_collection (◆ 参数确认 + 执行计划确认)
  ↓
task_setup (◆ 创建参数确认)
  ↓
deploy (自动触发流水线)
  ↓ ◆ 测试方案确认
testing → dev_stage_pass (◆ 用户确认推进)
  ↓
code_review → access_stage_pass (◆ 用户确认推进)
  ↓
completion
```

◆ = 确认检查点（必须等待用户确认后才能继续）

各阶段 `status` 值：`pending` → `in_progress` → `completed` / `skipped` / `failed`

---

### Phase 0: info_collection（信息收集与确认）

> **目标**：尽可能自动获取所有参数，汇总展示给用户确认。**所有参数无论来源（自动检测/历史推导/用户输入），都必须在确认单中展示并获得用户确认后才能使用。**

**入口条件**：收到用户的研发需求

**操作步骤**：

1. **自动检测 PSM**（使用 `repo2psm` 策略）：
   - 按优先级在仓库根目录中查找 PSM 定义：
     1. `script/bootstrap.sh` → `PSM` 变量
     2. `script/settings.py` → `PRODUCT.SUBSYSTEM.MODULE`
     3. `build.sh` → `RUN_NAME` 变量
     4. `atum.yaml` → `PSM` 字段
   - 找到后填入确认单；未找到则留空让用户填写

2. **读取 Space ID**：
   - 从 `.gdpa/bits-devops.yaml` 读取 `space_id`
   - 不存在则调用 `get_recent_spaces` 获取用户最近空间列表，展示选项供用户选择，确认后保存到 `.gdpa/bits-devops.yaml`

3. **检查本地分支**：
   - 当前分支 **不是** `master` 或 `main`：默认使用当前分支
   - 当前分支 **是** `master` 或 `main`：建议新分支名，在确认单中让用户确认

4. **预获取 BITS 配置**（proactive fetch，并行执行以提高效率）：
   - 调用 `bits-devops` 的 `get_dev_templates` 获取空间可用模板列表
   - 调用 `bits-devops` 的 `check_template_meego` 检查默认模板是否要求关联 Meego

5. **解析 env / 环境名 / 泳道名 / lane**（如用户指定）：任务创建后完整环境名如 `boe_<lane_id>` / `ppe_<lane_id>`；用户输入若带 `boe_` / `ppe_` 前缀，**去掉前缀**后写入 `context.lane_id`，原始值留在 `context.user_lane_name` 用于后续对账。

6. **预搜索 Meego 需求**（如模板要求关联 Meego）：
   - 调用 `meego-manage` 搜索当前用户近期 story：
     ```bash
     gdpa-cli run meego-manage --session-id <sid> --input '{"work_item_type_key":"story","page_size":10,"updated_at_start":"4380h"}'
     ```
   - 如用户提供了需求关键字，可追加 `work_item_name` 过滤
   - 将搜索结果以选项列表形式展示在确认单中，用户可直接选择或输入其他链接

7. **展示确认单**（所有参数汇总，无论来源都需用户确认）：

```markdown
## 🚀 研发任务确认单

以下参数已自动检测，请逐项确认是否正确：

| 配置项 | 当前值 | 来源 | 说明 |
|--------|--------|------|------|
| **需求描述** | <提取的需求摘要> | 用户输入 | 本次研发目标 |
| **PSM** | `tiktok.xxx.xxx` | 🤖 仓库自动检测 | ⚠️ 请确认是否正确 |
| **BITS 空间** | <space_name> (ID: <space_id>) | 📄 配置文件 / 🤖 get_recent_spaces | |
| **开发分支** | `feat/xxx` | 🤖 当前分支 / 自动建议 | |
| **开发模板** | <template_name> (ID: <id>) | 🤖 默认模板 | ⬇️ 可选列表见下方 |
| **关联 Meego** | <meego_url> | 🤖 自动搜索 / 待选择 | ⬇️ 最近 Story 见下方 |
| **控制面** | CONTROL_PLANE_I18N | 🤖 推断 | 决定流水线区域和泳道部署 |
| **测试 VRegion** | Singapore-Central | 🤖 根据控制面推导 | ⬇️ 推导规则见下方 |
| **测试 VDC** | sg1 | 🤖 根据 VRegion 推导 | ⚠️ 取决于实际部署，请确认 |
| **env / `lane_id`** | `<去前缀后 lane_id>` 或 _留空（默认 `feature_${dev_task_id}`）_ | ✏️ 用户输入 | 用户输入若带 `boe_` / `ppe_` 前缀已自动去掉 |

### 你最近的 Meego Story（选一个关联，或输入其他链接）

| # | ID | 名称 | 项目 | 更新时间 |
|---|-----|------|------|---------|
| 1 | 6788756641 | {story_name_1} | ttarch | 2026-03-10 |
| 2 | 6874274119 | {story_name_2} | ttarch | 2026-03-08 |
| ... | ... | ... | ... | ... |

> 回复数字选择，或直接粘贴 Meego 链接。

### VRegion / VDC 推导规则（根据控制面自动推导默认值）

| 控制面 | 默认 VRegion | 默认 VDC | 说明 |
|--------|-------------|---------|------|
| `CONTROL_PLANE_CN` | `China-North` | `lf` | 国内区域 |
| `CONTROL_PLANE_I18N` | `Singapore-Central` | `sg1` | 海外区域（SG vs US 请确认） |

> ⚠️ VDC 取决于服务实际部署的集群。I18N 控制面内 SG 和 US 需要用户确认。

### env / lane_id 规则

任务创建后完整环境名如 `boe_<lane_id>` / `ppe_<lane_id>`；用户口中的「env / 环境名 / 泳道名 / lane」均指 `lane_id`，输入若带 `boe_` / `ppe_` 前缀需去掉后再使用：

| 用户输入 | `lane_id` |
|---------|-----------|
| `ppe_gdpa_test_event` | `gdpa_test_event` |
| `boe_my_feature` | `my_feature` |
| `gdpa_test_event` | `gdpa_test_event` |
| _未指定_ | _留空，走默认 `feature_${dev_task_id}`_ |

### 可选模板列表（来自 BITS 空间）

| 模板 ID | 名称 | 是否默认 |
|---------|------|---------|
| 26037 | 需求研发 | ✅ |
| ... | ... | |

> 回复 "确认" 或 "yes" 继续；回复具体修改项进行调整。
```

8. **修正参数**：根据用户反馈更新，直到用户确认
   - 用户可以修改任何一项参数
   - 修改后重新展示确认单

#### ◆ 检查点：执行计划确认

用户确认基本参数后，分析需求生成完整执行计划，展示给用户确认。

**执行计划模板**：

```markdown
## 📋 执行计划

基于需求分析，以下是本次研发的完整执行计划：

### 阶段概览

| # | 阶段 | 执行/跳过 | 具体内容 |
|---|------|----------|---------|
| 0 | 信息收集 | ✅ 完成 | 参数已确认 |
| 1 | 任务准备 | ✅ 执行 | 创建 BITS 开发任务，配置泳道 |
| 2 | 提交部署 | ✅ 执行 | Push 到 {branch}，自动触发流水线 |
| 3 | 测试验证 | ✅ 执行 | 接口测试 + 日志分析 |
| 4 | 开发阶段通过 | ✅ 执行 | 确认后通过 BITS 开发阶段 |
| 5 | 代码审查 | ✅ 执行 | 发起 MR + 代码审查 |
| 6 | 准入阶段通过 | ✅ 执行 | 确认后通过 BITS 准入阶段 |
| 7 | 完成收尾 | ✅ 执行 | 生成报告，提供 BITS 链接 |

### 预期涉及的关键操作

1. {操作1}
2. {操作2}

### 潜在风险与注意事项

- {风险1}

> 回复 "确认" 开始执行；回复修改意见调整计划。
```

将确认后的执行计划保存为 `info/execution_plan.md`。

**退出条件**：用户明确确认参数 + 执行计划

**产出文件**：
- `info/task_config.json`（确认后的参数配置）
- `info/execution_plan.md`（确认后的执行计划）

> 完成检查：两个文件都存在 → 标记 completed

---

### Phase 1: task_setup（BITS 开发任务创建）

> 使用 `bits-devops` Skill 完成。**调用前必读该 Skill。**

**入口条件**：`info_collection` 已完成

**操作步骤**：

1. **切换分支**：如果当前分支是 `master` 或 `main`，且 Phase 0 确认了新分支，**必须先 `git checkout -b <new_branch>`**

2. **查找已有开发任务**（三种来源，任一命中即可复用）：

   **a. 按分支匹配**：调用 `get_opened_dev_task_list`（传入 space_id），从返回列表中筛选与 `context.branch` 相同分支的任务
   - 遍历返回的 `dev_tasks` 列表，检查每个任务的分支是否与当前分支一致
   - 如有多个匹配，优先推荐最近创建的

   **b. 用户直接提供**：询问用户是否已有关联的 BITS 开发任务
   - 用户可以提供：BITS 任务链接（如 `https://bits.bytedance.net/devops/.../detail/2147497`）或 `dev_task_id`
   - 从链接中解析出 `dev_task_id`（`/detail/` 后面的数字段）
   - 调用 `get_dev_task_basic_info` 验证任务存在且状态为 OPEN
   - **校验分支一致性**：比较任务绑定的分支与 `context.branch`，不一致时需特殊处理（见步骤 3）

   **c. 均无匹配**：进入创建新任务流程

3. **◆ 确认：复用已有任务 或 创建新任务**

   **⚠️ 分支冲突处理**：当复用的任务绑定分支与当前本地分支不一致时，必须展示冲突并让用户选择处理方式：

```markdown
## ⚠️ 分支不一致

复用的 BITS 任务绑定的分支与当前本地分支不同：

| 项目 | 值 |
|------|-----|
| **BITS 任务分支** | `{task_branch}` |
| **当前本地分支** | `{context.branch}` |

请选择处理方式：

1. **在 BITS 上切换分支** — 将 BITS 任务的开发分支更新为当前本地分支 `{context.branch}`
   - 适用于：BITS 任务的旧分支已废弃，实际开发在当前分支
2. **切换本地分支** — 将本地分支切换到 BITS 任务绑定的 `{task_branch}`，已有改动需 rebase
   - 适用于：BITS 任务的分支才是正确的开发分支
3. **放弃复用** — 不使用这个任务，改为创建新任务

> 回复 1/2/3 选择处理方式。
```

   处理逻辑：
   - **选 1**：后续 deploy 阶段使用 `context.branch` push，BITS 任务分支以实际 push 为准
   - **选 2**：执行 `git checkout {task_branch}`，如有未提交改动提示用户先 stash 或 commit；更新 `context.branch` 为 `{task_branch}`
   - **选 3**：回到创建新任务流程

   **分支一致时**：跳过冲突处理，直接展示正常的复用确认：

```markdown
## 🔧 BITS 开发任务确认

### 已找到的 OPEN 任务（按分支 `{branch}` 匹配）

| 任务 ID | 标题 | 分支 | 创建时间 | 状态 | 操作建议 |
|---------|------|------|---------|------|---------|
| 2147490 | feat: xxx | feat/xxx | 2026-03-09 | OPEN | ✅ 推荐复用（同分支） |

> **复用已有任务**：回复 "复用 {task_id}" 或 "复用 1"（序号）
> **提供其他任务**：回复 BITS 链接或 dev_task_id
> **创建新任务**：回复 "创建" 继续确认以下参数

### 创建新任务参数（仅在创建新任务时使用）

| 参数 | 值 | 来源 | 说明 |
|------|-----|------|------|
| space_id | <space_id> | 📄 .gdpa/bits-devops.yaml | |
| branch | <branch> | ✅ Phase 0 用户确认 | |
| psm_list | [<psm>] | ✅ Phase 0 用户确认 | |
| control_planes | [<cp>] | ✅ Phase 0 用户确认 | 决定泳道部署环境 |
| 模板 ID | <template_id> | ✅ Phase 0 用户选择 | |
| 关联 Meego | <meego_url> | ✅ Phase 0 用户选择 | |
| `lane_id` | <context.lane_id 或 _留空_> | ✅ Phase 0 已去前缀 | 留空时走默认 `feature_${dev_task_id}` |

> 确认后调用 `create_dev_task`；`context.lane_id` 不为空时必须作为 `lane_id` 入参传入。
```

4. **创建或复用开发任务**：
   - **复用**：直接使用已有 `dev_task_id`，跳过创建步骤
   - **创建**：调用 `create_dev_task`；`context.lane_id` 不为空时必须作为 `lane_id` 入参传入（已在 Phase 0 去除 `boe_` / `ppe_` 前缀），为空则不传走默认值

5. **获取任务详情**：创建/复用成功后依次调用：
   - `get_dev_task_stages`：获取工作流阶段信息（记录各 stage 的 fixed_name）
   - `get_dev_task_lane_info`：获取泳道配置信息

6. **推导测试环境参数**：从 `lane_info` 自动推导 `test_env`（完整泳道名）和 `test_env_type`，写入 `context`：
   - **泳道名拼接规则**：`overwrite_prefix` 不为空时用 `overwrite_prefix + lane_id`，否则用 `lane_type + lane_id`
   - **env_type 推断**：`lane_type` 或 `overwrite_prefix` 含 `ppe` → `ppe`；含 `boe` → `boe`；否则 → `prod`
   - 示例：`lane_type=ppe_i18n_env_`, `lane_id=feature_2147497` → `test_env=ppe_i18n_env_feature_2147497`, `test_env_type=ppe`
   - **校验**：若 `context.user_lane_name` 不为空，把推导出的 `test_env` 与之对比，不一致时报告用户

**退出条件**：获得 dev_task_id、BITS 链接、泳道信息、阶段信息、测试环境参数

**产出文件**：`bits-devops/task_info.json`（格式见 [phase-examples.md](phase-examples.md#phase-1-task_setup)）

> 完成检查：`task_info.json` 存在且 `dev_task_id` 有效 → 标记 completed

---

### Phase 2: deploy（提交部署）

> 使用 `bits-devops` Skill 完成流水线操作。**调用前必读该 Skill。**

**入口条件**：`task_setup` 已完成

**操作步骤**：

1. **提交代码**：`git add` → `git commit` → `git push`（分支名从 `context.branch` 读取）
2. **自动触发自测流水线**：调用 `run_pipeline`
   - `dev_task_id`: 从 `context.dev_task_id` 读取
   - `space_id`: 从 `context.space_id` 读取
   - `task_name`: `DevDevelopStageSelfTestTask`
   - `control_planes`: 从 `context.control_planes` 读取
3. **监控流水线状态**：调用 `get_dev_task_pipelines` 查看运行状态
   - 轮询直到流水线完成（成功/失败）
   - 流水线详情可通过 BITS 页面查看：`context.bits_link`
4. **查看部署详情**：流水线完成后，调用 `get_pipeline_run`（传入 `pipeline_run_id`）获取详细运行信息
   - `pipeline_run_id` 从 `get_dev_task_pipelines` 返回结果中获取
   - 返回每个 Job 的执行状态、耗时、失败原因等
   - **向用户展示部署结果汇总**（各 Job 状态、总耗时、流水线链接）
5. **流水线失败排查**：如果流水线失败，按以下流程排查：
   - 调用 `get_pipeline_run` 查看各 Job 状态，定位失败的 Job 及 `fail_reason`
   - 如果主流水线因子流水线失败，从 `fail_reason` 中提取 `driven_pipeline_run_id`，再次调用 `get_pipeline_run` 追踪子流水线
   - **向用户展示失败原因和修复建议**，由用户决定是修复代码后重新部署还是重试

**退出条件**：代码已 Push + 流水线运行完成（成功或失败均记录，含部署详情）

**产出文件**：`deploy/deploy_info.json`（格式见 [phase-examples.md](phase-examples.md#phase-4-deploy)）

> 完成检查：`deploy_info.json` 存在且 `push_success` 为 true → 标记 completed
>
> 流水线失败时：记录失败详情（含 `fail_reason` 和失败 Job 信息），展示给用户决策是否修复后重新部署

---

### Phase 3: testing（测试验证）

> **调用前必读对应 Skill**：`bam-query`、`argos-query`

**入口条件**：`deploy` 已完成

**跳过判断**：用户明确表示不需要测试 → 标记为 `skipped`

#### ◆ 检查点：测试方案确认

生成结构化的测试方案供用户审查。测试环境参数（VRegion、VDC、Env）已在 Phase 0/1 确认并存储在 `context` 中，直接使用：

- **VRegion / VDC**：从 `context.test_vregion` / `context.test_vdc` 读取（Phase 0 用户已确认）
- **Env（泳道名）**：从 `context.test_env` 读取（Phase 1 从 lane_info 自动推导）
- **Env Type**：从 `context.test_env_type` 读取（Phase 1 自动推导）

**测试方案模板**：

```markdown
## 🧪 测试方案

### 测试环境（Phase 0 已确认）

| 配置项 | 值 | 来源 |
|--------|-----|------|
| **VRegion** | {context.test_vregion} | Phase 0 用户确认 |
| **VDC** | {context.test_vdc} | Phase 0 用户确认 |
| **Env（泳道名）** | {context.test_env} | Phase 1 从 lane_info 推导 |
| **Env Type** | {context.test_env_type} | Phase 1 自动推导 |
| **控制面** | {context.control_planes} | Phase 0 用户确认 |

### 测试用例

| # | 接口/方法 | 类型 | VRegion | Env | 测试输入 | 预期结果 |
|---|----------|------|---------|-----|---------|---------|
| 1 | GetXxx | 读 | {context.test_vregion} | {context.test_env} | {...} | 返回预期数据 |

### 日志验证计划
- **查询模式**: Local File（PPE 测试优先使用）
- **Env**: {context.test_env}
- **搜索关键字**: error, {相关方法名}
- **预期结果**: 无异常错误日志

> 回复 "确认" 开始测试；回复 "跳过" 跳过测试。
```

**操作步骤**：

1. **确认部署完成**：查看流水线状态
2. **发起接口测试**（使用 `bam-query` Skill）：
   - 使用 `context` 中已确认的 VRegion、VDC、Env 参数
   - 读接口可直接测试；**写接口必须用户明确授权**
3. **分析日志**（使用 `argos-query` Skill）：
   - **优先使用 Local File 模式**：传入 `env`（泳道名）和 `env_type`（从 context 读取），精确查看泳道内日志
   - Argos 日志可能有 1-5 分钟延迟，首次未找到需提示用户等待后重试
4. **结果判断**：通过 → 进入 dev_stage_pass；不通过 → 回退到 deploy（用户修复代码后重新部署）

**产出文件**：
- `bam-query/test_plan.md`（确认后的测试方案）
- `bam-query/test_result.json`（测试用例及结果）
- `argos-query/logs_summary.md`（日志分析摘要）

> 完成检查：三个文件都存在 → 标记 completed
>
> 测试不通过时：`current_phase` 回退到 deploy，testing 标记 `failed`，deploy 标记 `in_progress`

---

### Phase 4: dev_stage_pass（通过开发阶段）

> 使用 `bits-devops` Skill 完成。**调用前必读该 Skill。**

**入口条件**：`testing` 完成

**操作步骤**：

1. **获取当前阶段状态**：调用 `get_dev_task_stages` 展示 BITS 工作流各阶段状态
   - 注意 `pipelines_by_task` 字段，展示各控制面的真实流水线状态
   - 判断是否全部通过时应以 `pipelines_by_task` 为准（BITS 聚合状态可能只要部分控制面通过就显示 `succeeded`）
2. **查看关键流水线详情**：对自测流水线调用 `get_pipeline_run` 获取详细运行结果
   - 展示各 Job 状态、耗时、流水线链接
   - 如有失败：展示 `fail_reason`，帮助用户判断是否需要修复
3. **自动触发提测流水线**：调用 `run_pipeline`（`DevDevelopStageRDTestTask`）
4. **监控提测流水线**：调用 `get_dev_task_pipelines` + `get_pipeline_run` 查看提测流水线运行结果
5. **◆ 汇总展示，等待用户确认**：

```markdown
## ✅ 开发阶段通过确认

### 当前状态汇总

| 项目 | 状态 | 详情 |
|------|------|------|
| 自测流水线 | ✅/❌ {status} | 耗时 {time_cost_sec}s [查看详情]({pipeline_run_url}) |
| 提测流水线 | ✅/❌ {status} | 耗时 {time_cost_sec}s [查看详情]({pipeline_run_url}) |
| 接口测试 | ✅ 全部通过 ({passed}/{total}) | |
| 日志检查 | ✅ 无异常 | |
| BITS 任务 | [查看详情]({bits_link}) | |

### 各控制面流水线状态（来自 pipelines_by_task）

| 阶段/任务 | 控制面 | 状态 |
|-----------|--------|------|
| {stage/task} | {control_plane} | {status} |

### BITS 工作流阶段

{从 get_dev_task_stages 获取的阶段状态表}

> 确认通过开发阶段？回复 "确认" 将调用 `pass_development_stage`。
```

6. **用户确认后**：调用 `pass_dev_task_stage`（`stage_action: pass_development_stage`）

**退出条件**：`pass_development_stage` 成功

**产出文件**：`bits-devops/dev_stage_pass.json`（格式见 [phase-examples.md](phase-examples.md#phase-4-dev_stage_pass)）

> 完成检查：`dev_stage_pass.json` 存在且 stage_action 执行成功 → 标记 completed

---

### Phase 5: code_review（代码审查）

> 使用 `bits-devops`、`codebase` Skill。**调用前必读对应 Skill。**

**入口条件**：`dev_stage_pass` 完成

**操作步骤**：

1. **发起 MR**：在 Codebase 上创建 Merge Request
   - 关联 BITS 任务（在 MR 描述中附上 BITS 链接）
   - MR 描述引用测试报告
2. **触发代码审查流水线**：调用 `run_pipeline`（`DevGatekeeperStageCodeReviewTask`）
3. **监控 CR 流水线**：调用 `get_dev_task_pipelines` 获取流水线列表，再调用 `get_pipeline_run` 查看详细运行结果
   - 展示各 Job 状态、耗时
   - 流水线失败时展示 `fail_reason`，帮助用户诊断
4. **查看代码审查状态**：调用 `get_dev_task_code_review_info` 查看审查进展
5. **向用户报告状态**：展示流水线详情、Reviewer 列表、审查结论等，提示用户等待或跟进

**退出条件**：Code Review 流水线完成（审查结果记录，用户自行决定是否继续）

**产出文件**：`code-review/review_info.json`（格式见 [phase-examples.md](phase-examples.md#phase-5-code_review)）

> 完成检查：`review_info.json` 存在 → 标记 completed

---

### Phase 6: access_stage_pass（通过准入阶段）

> 使用 `bits-devops` Skill 完成。**调用前必读该 Skill。**

**入口条件**：`code_review` 完成

**操作步骤**：

1. **获取最新阶段状态**：调用 `get_dev_task_stages` 展示各阶段最新状态
2. **◆ 汇总展示，等待用户确认**：

```markdown
## ✅ 准入阶段通过确认

### 全流程状态汇总

| 阶段 | 状态 |
|------|------|
| 开发阶段 | ✅ 已通过 |
| 自测 | ✅ 通过 |
| 提测 | ✅ 通过 |
| 代码审查 | ✅ 完成 |
| BITS 任务 | [查看详情]({bits_link}) |

### BITS 工作流阶段

{从 get_dev_task_stages 获取的最新阶段状态表}

> 确认通过准入阶段？回复 "确认" 将调用 `pass_access_stage`。
```

3. **用户确认后**：调用 `pass_dev_task_stage`（`stage_action: pass_access_stage`）

**退出条件**：`pass_access_stage` 成功

**产出文件**：`bits-devops/access_stage_pass.json`（格式见 [phase-examples.md](phase-examples.md#phase-6-access_stage_pass)）

> 完成检查：`access_stage_pass.json` 存在 → 标记 completed

---

### Phase 7: completion（完成收尾）

**入口条件**：`access_stage_pass` 完成

**操作步骤**：

1. **研发总结**：整理变更内容、影响范围、关键决策
2. **提供后续操作链接**：
   - BITS 任务链接（用户可在平台上继续驱动发布单流程）
   - MR 链接
   - 代码审查结果

**产出文件**：`summary/report.md`（研发总结，汇总所有阶段产出）

> 完成检查：`report.md` 存在 → 标记 completed

---

## 四、状态文件规范

> 完整 status.json 结构见 [status-schema.md](status-schema.md)

### 4.1 状态更新规则

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

### 4.2 各阶段产出文件

| 阶段 | 产出文件 | 完成检查条件 |
|------|---------|-------------|
| `info_collection` | `info/task_config.json` + `info/execution_plan.md` | 两个文件都存在 |
| `task_setup` | `bits-devops/task_info.json` | 文件存在且 dev_task_id 有效 |
| `deploy` | `deploy/deploy_info.json` | 文件存在且 push_success=true |
| `testing` | `bam-query/test_plan.md` + `bam-query/test_result.json` + `argos-query/logs_summary.md` | 三个文件都存在（skipped 时无需产出） |
| `dev_stage_pass` | `bits-devops/dev_stage_pass.json` | 文件存在且 stage_action 成功 |
| `code_review` | `code-review/review_info.json` | 文件存在 |
| `access_stage_pass` | `bits-devops/access_stage_pass.json` | 文件存在且 stage_action 成功 |
| `completion` | `summary/report.md` | 文件存在 |

完整目录结构：

```
.gdpa/{session-id}/
├── status.json                      # 流程状态（核心，每步更新）
├── info/
│   ├── task_config.json             # info_collection 产出
│   └── execution_plan.md            # ◆ 执行计划确认产出
├── bits-devops/
│   ├── task_info.json               # task_setup 产出
│   ├── dev_stage_pass.json          # dev_stage_pass 产出
│   └── access_stage_pass.json       # access_stage_pass 产出
├── deploy/
│   └── deploy_info.json             # deploy 产出
├── bam-query/
│   ├── test_plan.md                 # ◆ 测试方案确认产出
│   └── test_result.json             # testing 产出
├── argos-query/
│   ├── logs_raw.log                 # testing 产出（大体量日志）
│   └── logs_summary.md              # testing 产出
├── code-review/
│   └── review_info.json             # code_review 产出
└── summary/
    └── report.md                    # completion 产出
```

### 4.3 使用规则

1. **每步四拍节奏**：读 status → 执行操作 → 写产出文件 → 更新 status（缺一不可）
2. **产出文件是硬约束**：标记 `completed` 前必须先写入对应产出文件
3. **history 记录 wrote_file**：每次写入产出文件后，在 `history` 中追加 `{"action": "wrote_file", "detail": "文件路径"}`
4. **大输出走文件**：大体量输出（如 argos 日志）写入文件，对话 context 仅传摘要 + 文件路径
5. **Session 隔离**：每次研发流程使用独立 `session-id`，互不干扰
6. **Git 忽略**：`.gdpa/` 目录应加入 `.gitignore`
7. **Context 优先读 status**：PSM、分支、space_id、dev_task_id 等信息统一从 `context` 读取，不重复询问用户
8. **Skipped 阶段无需产出**：被标记为 `skipped` 的阶段不需要写产出文件
9. **产出必须基于真实数据**：产出文件数据必须来自 `gdpa-cli` 命令的真实返回，禁止编造
10. **测试环境 Phase 0 确认**：VRegion、VDC 在 Phase 0 确认单中由用户确认，Env（泳道名）在 Phase 1 从 lane_info 自动推导，后续阶段直接从 `context` 读取
11. **所有参数必须用户确认**：无论参数来源是自动检测（repo2psm）、历史推导、配置文件读取还是 API 预获取，都必须在确认单中展示来源并让用户确认后才能使用。不可假设自动检测的值一定正确
12. **主动预获取选项**：对需要用户选择的参数（如 Meego 链接、开发模板），优先通过 API 搜索候选列表展示给用户选择，减少用户手动输入的负担

---

## 五、附加资源

- 完整 status.json 结构与初始化模板 → [status-schema.md](status-schema.md)
- 各阶段产出文件与状态更新 JSON 示例 → [phase-examples.md](phase-examples.md)
- 可用 Skill 速查与选择决策指南 → [skills-reference.md](skills-reference.md)
