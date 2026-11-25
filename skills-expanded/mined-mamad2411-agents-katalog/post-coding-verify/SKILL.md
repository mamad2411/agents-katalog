---
name: post-coding-verify
description: Automate post-coding verification workflow including PPE deployment, API testing, and log verification. Use when code implementation is done and the user wants to deploy to PPE, test interfaces, and verify logs, or mentions "post-coding verify" / "deploy and test" / "PPE verification".
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# 编码后验证流程

> **核心原则**：整个流程由 `.gdpa/{session-id}/status.json` 驱动。每次执行前先读取状态文件，确认当前阶段；每步操作后更新状态文件。
> **Session-ID 约束（workflow 专用）**：`gdpa-cli run` 全局不再强制要求 `--session-id`，但本 workflow 仍然必须在整条链路里显式复用同一个 `--session-id <session_id>`。CLI 不会自动把 Session-ID 注入到 Skill 输入；如果漏传或中途更换，`.gdpa/{session-id}/status.json`、阶段产物和恢复链路都会断开。

---

## 强制执行约束（必须遵守）

**以下规则优先级最高，违反任何一条都视为执行失败：**

1. **命令失败时如实报告，不可伪造成功** — 如果 `gdpa-cli` 命令执行失败，**必须如实向用户报告错误**并排查修复，不可跳过或伪造结果。
2. **调用 `gdpa-cli` 前必须先阅读对应 Skill** — 了解完整的参数格式、输入输出 Schema 和使用示例，确保命令参数正确。不要凭记忆或猜测拼写命令。
3. **环境参数一致性** — `env`、`vregion`、`vdc` 等参数必须从 `status.json` 的 `context` 中读取，全流程保持一致。
4. **必须创建 session 目录并维护 status.json** — **必须**在 `.gdpa/{session-id}/` 下创建目录、初始化 `status.json`，并在每一步操作后写入产出文件和更新状态。不可跳过状态文件的创建和维护。
---

## 一、启动与恢复

**每次新对话的第一个操作，必须严格按以下顺序执行。不可跳步、不可调换顺序。**

### Step 0：创建 session（第一个动作，无条件执行）

> **这是整个流程的第一个动作，必须在做任何其他事情之前执行。**
> **不要先去查看 .gdpa/ 目录、不要先 ls、不要先检查是否有旧 session。**

**执行**：`gdpa-cli create-session`

- 记住返回的 `session_id`（例如 `sess_20260213_143052_abcd1234`）
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

## 二、阶段定义与状态流转

### 流转总览

```
info_collection → deploy → api_testing → log_verify → completion
                                ↑              │
                                └──────────────┘
                                (用户选择重测时回退)
```

各阶段 `status` 值：`pending` → `in_progress` → `completed` / `skipped` / `failed`

**流转规则**：

| 从 | 到 | 条件 | 类型 |
|----|----|------|------|
| info_collection | deploy | 用户确认信息 | 线性 |
| deploy | api_testing | 部署成功 | 线性 |
| api_testing | log_verify | 测试完成 | 线性 |
| log_verify | completion | 日志验证通过 | 线性 |
| log_verify | api_testing | 发现问题 + 用户选择重测 | 用户决策回退 |
| log_verify | completion | 发现问题 + 用户选择结束 | 用户决策继续 |

---

### Phase 0: info_collection（信息收集与确认）

> **目标**：收集服务信息、检查分支状态、自动分析代码变更检测受影响的接口。
>
> 使用 `repotalk` 和 `bam-api` Skill。**调用前必读对应 Skill。**

**入口条件**：收到用户的验证请求

**操作步骤**：

1. **检查本地分支**：
   - 如果当前分支**是** `master` 或 `main`：根据最近的 commit 信息生成一个新分支名（如 `verify/xxx`），**必须先执行 `git checkout -b <new_branch>` 切换到新分支**。
   - 如果当前分支**不是** `master`/`main`：使用当前分支。
2. **收集基本信息**：PSM、业务线（Biz）等。从用户输入或项目配置中提取。
3. **分析代码变更**：
   - 执行 `git diff --name-only HEAD~1..HEAD`（或对比 master）获取变更文件列表
   - 使用 `repotalk` 语义搜索分析变更涉及的接口
   - 使用 `bam-api` 获取这些接口的完整定义（方法名、请求/响应 Schema）
4. **交互确认**：向用户展示确认表单：

```markdown
## 验证任务确认单

| 配置项 | 当前值 | 说明 |
|--------|--------|------|
| **PSM** | `tiktok.xxx.xxx` | 目标服务 |
| **开发分支** | `feature-xxx` | 当前 Git 分支 |
| **业务线 (Biz)** | `Tiktok` | Tiktok/Aweme/Devflow/Tikcast |
| **区域 (Region)** | `i18n` | i18n/cn |
| **检测到的变更接口** | `GetXxx`, `UpdateYyy` | 将自动测试的接口 |

> 回复 "确认" 继续；回复具体修改项进行调整。
```

5. **修正参数**：根据用户反馈更新，直到用户确认。

**退出条件**：用户明确确认

**产出文件**：`info/task_config.json`（PSM、分支、区域、检测到的接口列表）

> 完成检查：`task_config.json` 存在且 `psm` 非空 → 标记 completed

---

### Phase 1: deploy（提交部署）

> **目标**：自动 commit + push 代码，创建 DevFlow 任务，触发 PPE 部署并确认部署成功。
>
> 使用 `devflow` Skill。**调用前必读该 Skill。**

**入口条件**：`info_collection` 已完成

**操作步骤**（必须在终端实际执行，禁止跳过或模拟）：

1. **提交代码**：
   - `git add .` + `git commit`（提交信息参考变更内容自动生成）
   - `git push -u origin <branch>`（分支名从 `context.branch` 读取）
2. **创建 DevFlow 任务**：
   - 使用 `devflow` Skill 创建新任务（PSM、分支、环境等从 context 读取）
   - 记录返回的 `task_id`
3. **启动开发调试**：
   - 通过 `devflow` 启动调试，触发 PPE 部署流水线
4. **轮询等待部署完成**（关键步骤）：
   - 执行 `gdpa-cli run devflow develop-detail <task_id>` 查询部署状态
   - 检查返回结果中每个 Lane 的 **Status** 字段：
     - `READY` → 部署成功，**立即继续下一步**
     - `RUNNING` / `PENDING` → 部署进行中，**等待 30 秒后重新查询**
     - `FAILED` → 部署失败，记录错误信息，标记 phase 为 failed，向用户报告
   - **循环策略**：每 60 秒轮询一次，最多轮询 20 次（约 20 分钟）
   - **每次轮询时**向用户简要报告当前状态（如「部署中... 第 3 次检查，状态: RUNNING」）
   - 超时仍未 READY → 向用户报告超时，提供 PipelineURL 让用户手动检查
5. **提取部署信息**（Status 为 READY 后执行）：
   - 从 `develop-detail` 返回结果中提取：
     - **env**：泳道名（Lane 字段，如 `ppe_20260213`），这就是完整环境名
     - **vregion**：Region 字段对应的标准 VRegion（`i18n` → `["Singapore-Central", "US-East"]`，`cn` → `["China-North"]`）
     - **vdc**：DC 字段（如 `LF, SG` → `["lf", "sg1"]`）
   - 将上述信息写入 `context`

**自动推进规则**：当所有 Lane 状态变为 `READY` 后，**无需询问用户，立即写入产出文件、更新 status.json、自动进入 `api_testing` 阶段**。

**退出条件**：代码已 Push + DevFlow 任务已创建 + 所有 Lane 状态为 READY

**产出文件**：`deploy/deploy_info.json`（分支、commit hash、task_id、env、vregion、vdc、流水线链接）

> 完成检查：`deploy_info.json` 存在且 `push_success` 为 true → 标记 completed
>
> **重要**：`env` 使用完整泳道名（如 `ppe_20260213`），不是 `ppe`。`vregion` 使用标准值（如 `Singapore-Central`）。

---

### Phase 2: api_testing（接口测试）

> **目标**：对变更涉及的接口发起 RPC/HTTP 测试请求，验证功能正确性。
>
> 使用 `bam-query` Skill。**调用前必读该 Skill。**

**入口条件**：`deploy` 已完成

**操作步骤**（必须在终端实际执行，禁止用本地单测或 Grep 替代）：

1. **读取接口列表**：从 `context.affected_interfaces` 获取要测试的接口
2. **构造测试请求**：
   - 根据 `info_collection` 阶段获取的接口定义（Schema），构造合理的测试请求体
   - 读接口可直接测试；**写接口必须先征求用户确认**
3. **发起测试**：
   - 使用 `bam-query` 对每个接口发起请求
   - **vregion** 和 **env** 参数**必须从 `context.vregion` 和 `context.env` 读取**
   - 使用标准 VRegion 值（如 `Singapore-Central`），不要传别名（如 `sg`）
   - 如有多个 VRegion/VDC，需分别测试每个组合
4. **记录结果**：每个测试用例记录请求、响应、是否通过

**退出条件**：所有接口测试完成（不要求全部通过，但需记录结果）

**产出文件**：`testing/test_result.json`（测试用例列表、每个用例的请求/响应/结果）

> 完成检查：`test_result.json` 存在且 `test_cases` 非空 → 标记 completed

---

### Phase 3: log_verify（日志验证）

> **目标**：通过 Argos 查询服务日志，确认测试请求被正确处理、无异常错误。
>
> 使用 `argos-query` Skill。**调用前必读该 Skill。**

**入口条件**：`api_testing` 已完成

**操作步骤**：

1. **查询服务日志**：
   - 使用 `argos-query` 按 PSM + 时间范围（测试期间）+ 关键字查询日志
   - **vregion 参数必须使用标准值**（如 `Singapore-Central`），不要传别名
2. **分析日志**：
   - 检查是否有 ERROR/PANIC 级别日志
   - 确认测试请求在日志中有对应记录
   - 检查是否有非预期的异常
3. **注意日志延迟**：
   - Argos 日志可能有 1-5 分钟延迟
   - 如果首次查询未找到预期日志，**必须提示用户日志可能有延迟**，建议等待 30-60 秒后重试，不要直接报告失败
4. **结果判断**：
   - **通过**：无异常日志，请求链路正常 → 进入 completion
   - **发现问题**：暂停并**询问用户下一步操作**：
     - 选项 A：回退到 `api_testing` 重新测试
     - 选项 B：标记问题并继续到 completion

**退出条件**：日志分析完成 + 用户确认结果

**产出文件**：
- `logs/verify_result.json`（验证结论、发现的问题）
- `logs/logs_summary.md`（日志分析摘要）
- `logs/logs_raw.log`（原始日志，大量日志时写入）

> 完成检查：`verify_result.json` + `logs_summary.md` 都存在 → 标记 completed
>
> 发现问题且用户选择重测时：`current_phase` 回退到 `api_testing`，`log_verify` 标记 `failed`，`api_testing` 标记 `in_progress`

---

### Phase 4: completion（完成收尾）

> **目标**：汇总所有阶段结果，生成验证报告。

**入口条件**：`log_verify` 完成（通过或用户选择结束）

**操作步骤**：

1. **汇总验证结果**：
   - 读取各阶段产出文件，整理变更内容、部署信息、测试结果、日志分析
2. **生成报告**：使用以下模板生成 `summary/report.md`

```markdown
# 编码后验证报告

## 需求描述
{从 status.json 的 requirement 读取}

## 部署信息
- 分支: {context.branch}
- Commit: {context.commit_hash}
- 环境: {context.env}
- VRegion: {context.vregion}
- DevFlow: {context.task_link}

## 接口测试结果
{从 testing/test_result.json 读取，列出每个接口的测试结果}

| 接口 | VRegion | 状态 | 响应码 | 备注 |
|------|---------|------|--------|------|
| ... | ... | ... | ... | ... |

## 日志验证
{从 logs/logs_summary.md 读取}

## 结论
{整体通过/存在问题}
```

3. **展示报告摘要**：向用户展示关键结果

**退出条件**：报告生成完成

**产出文件**：`summary/report.md`

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

| 阶段 | 产出文件 | 完成检查条件 |
|------|---------|-------------|
| `info_collection` | `info/task_config.json` | 文件存在且 psm 非空 |
| `deploy` | `deploy/deploy_info.json` | 文件存在且 push_success=true |
| `api_testing` | `testing/test_result.json` | 文件存在且 test_cases 非空 |
| `log_verify` | `logs/verify_result.json` + `logs/logs_summary.md` | 两个文件都存在 |
| `completion` | `summary/report.md` | 文件存在 |

完整目录结构：

```
.gdpa/{session-id}/
├── status.json                    # 流程状态（核心，每步更新）
├── info/
│   └── task_config.json           # info_collection 产出
├── deploy/
│   └── deploy_info.json           # deploy 产出
├── testing/
│   └── test_result.json           # api_testing 产出
├── logs/
│   ├── verify_result.json         # log_verify 产出
│   ├── logs_summary.md            # log_verify 产出
│   └── logs_raw.log               # log_verify 产出（大量日志）
└── summary/
    └── report.md                  # completion 产出
```

### 3.3 使用规则

1. **每步四拍节奏**：读 status → 执行操作 → 写产出文件 → 更新 status（缺一不可）
2. **产出文件是硬约束**：标记 `completed` 前必须先写入对应产出文件
3. **history 记录 wrote_file**：每次写入产出文件后，在 `history` 中追加 `{"action": "wrote_file", "detail": "文件路径"}`
4. **大输出走文件**：大体量输出（如 argos 日志）写入文件，对话 context 仅传摘要 + 文件路径
5. **Session 隔离**：每次验证流程使用独立 `session-id`，互不干扰
6. **Git 忽略**：`.gdpa/` 目录应加入 `.gitignore`
7. **Context 优先读 status**：PSM、分支、env、vregion、vdc 等信息统一从 `context` 读取，不重复询问用户
8. **产出必须基于真实数据**：产出文件数据必须来自 `gdpa-cli` 命令的真实返回，禁止编造
9. **使用标准 VRegion**：调用 `bam-query`、`argos-query` 等 Skill 时，vregion 参数必须使用标准值（`Singapore-Central`、`US-East`、`China-North`、`China-BOE`、`US-BOE`），不要传别名

---

## 四、附加资源

- 完整 status.json 结构与初始化模板 → [status-schema.md](status-schema.md)
- 各阶段产出文件与状态更新 JSON 示例 → [phase-examples.md](phase-examples.md)
- 可用 Skill 速查与选择指南 → [skills-reference.md](skills-reference.md)
