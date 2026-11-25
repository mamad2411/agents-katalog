---
name: trellis-sync-prd
description: "Reconcile an out-of-date prd.md with code/requirement changes that landed without PRD update: gather diffs + user adjustments, confirm, update body, append change-log. Triggers: 「PRD 没同步」「同步 PRD」「事后回补 PRD」「sync PRD」. Not for initial PRD generation (trellis-brainstorm), source-fidelity audit (trellis-verify-prd), or re-running impl after PRD change (trellis-re-implement)."
---
# 同步 PRD - 代码/需求变更后回补 PRD

当你直接修改了任务相关的代码或需求，但没有同步更新任务的 `prd.md` 时，使用此技能将 PRD 与实际变更对齐。

**时机**：代码或需求已变更，但 PRD 未同步更新

---

## 使用场景

- 直接改了代码逻辑，但没更新 PRD 中的需求描述
- 用户口头调整了需求，代码已改但 PRD 仍是旧版本
- Code Review 后修改了实现方式，PRD 未反映
- 多次小修改累积后，PRD 与实际实现已出现偏差
- 任务完成前的最终检查，确认 PRD 是文档真实来源

---

## 执行步骤

### Step 1: 确认当前任务 `[AI]`

```bash
python3 ./.trellis/scripts/get_context.py
```

确认：
- 当前有激活的任务（`.trellis/.current-task` 已设置）
- 任务目录路径和 PRD 文件存在

如果没有激活的任务，询问用户要同步哪个任务的 PRD。

### Step 2: 读取现有 PRD `[AI]`

读取任务目录下的 `prd.md`，理解当前文档化的需求。

### Step 3: 收集实际变更 `[AI]`

从多个来源收集实际变更信息：

**3a. 代码变更**（如有）：

后端/前端的实际包目录因项目而异（如 `srm-boot` / `iqs` / `iqs-front-human` / `backend` 等），按当前项目实际包路径替换 `<pkg-dir>`。如任务仅改根仓库，可省略 `cd`。

```bash
# 查看当前未提交的变更
cd <pkg-dir> && git diff --name-only && git diff --cached --name-only
# 查看最近与任务相关的提交
cd <pkg-dir> && git log --oneline -20
```

**3b. 用户描述**：
- 询问用户："相比 PRD 中记录的内容，实际做了哪些不同的变更？"
- 提供多选引导：
  - 需求范围变了（增加/删减了功能点）
  - 实现方式变了（技术方案调整）
  - 接口/字段变了（API、数据库、DTO 等）
  - 业务规则变了（校验逻辑、流程等）
  - 其他

### Step 4: 对比分析 `[AI]`

将 PRD 内容与实际变更进行对比，识别差异：

```markdown
## PRD 偏差分析

### 新增（PRD 中没有，但实际已实现）
- <变更 1>

### 删除（PRD 中有，但实际未实现或已移除）
- <变更 2>

### 修改（PRD 描述与实际实现不一致）
- <变更 3>: PRD 说 X，实际是 Y
```

将分析结果展示给用户确认。

### Step 5: 更新 PRD `[AI]`

经用户确认后，更新 `prd.md`：

1. **更新主体内容**：修改 Goal、Requirements、Acceptance Criteria 等章节，使其反映实际状态
2. **追加变更记录**：在文末追加变更日志

**变更记录格式**：

```markdown
## 变更记录

### 变更 <N>: <简要描述> (YYYY-MM-DD)
- **变更类型**: 需求变更 / 实现调整 / 范围变更
- **变更内容**: <具体改了什么>
- **原因**: <为什么改>
- **PRD 同步方式**: 事后回补（代码先行）
```

### Step 6: 报告结果 `[AI]`

```markdown
## PRD 同步完成

### 偏差摘要
- 新增 <N> 项需求/实现
- 删除 <N> 项需求/实现
- 修改 <N> 项描述

### 更新的章节
- <章节 1>: <做了什么调整>
- <章节 2>: <做了什么调整>

### 下一步
- 确认 PRD 内容准确
- 如有后续开发，PRD 已可作为最新参考
- 如任务已完成，可运行 `trellis-finish-work`
```

---

## 与其他入口的区别

| 入口 | 形态 | 阶段 | 说明 |
|------|------|------|------|
| `trellis-brainstorm` | skill | 需求梳理 | PRD 从零创建，边讨论边完善 |
| `trellis-verify-prd` | skill | 开发前 | 对照原始需求文档校验 PRD（准确性 + 覆盖度） |
| `trellis-sync-prd` | skill（本技能） | 事后回补 | 代码已改，PRD 未同步，回补文档 |
| `trellis-re-implement` | skill | 需求变更 | 先更新 PRD，再调 Implement Agent |
| `trellis-finish-work` | 命令 | 完成检查 | 提交前整体检查清单 |

```
典型流程：
  PRD → 实现 → PRD 同步          # 理想流程（re-implement）
  PRD → 实现 → 偏差 → sync-prd   # 补救流程（本技能）
```

---

## 核心原则

| 原则 | 说明 |
|------|------|
| **PRD 是真实来源** | PRD 应始终反映任务的最新状态，而非初始计划 |
| **事后回补优于不补** | 即使是事后同步，也比让 PRD 过时不管要好 |
| **记录变更原因** | 追加变更记录，让后续开发者理解演变过程 |
| **用户确认为准** | 对比分析需经用户确认后再更新，避免错误同步 |
