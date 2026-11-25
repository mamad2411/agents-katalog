---
name: trellis-re-implement
description: "Re-run Implement Agent and Check Agent after PRD change; updates PRD first, then rebuilds."
---
# 二次实现 - 需求变更后重新调用 Implement Agent

当任务实施过程中出现需求漂移或变动时，重新调用 Implement Agent 实现更新后的需求。

---

## 使用场景

- 任务已通过 `trellis-continue` 完成了首次实现
- 实施过程中需求发生了变更或补充
- PRD 已更新，需要 Implement Agent 根据新需求重新实现
- 用户在 check 或测试阶段发现需要调整方向

---

## 前置条件

- 当前任务已激活（`.trellis/.current-task` 已设置）
- 任务目录下存在 `prd.md`（已更新为最新需求）
- 任务目录下存在 `implement.jsonl`（code-spec context 配置）

---

## 执行步骤

### Step 1: 确认当前任务状态 `[AI]`

```bash
python3 ./.trellis/scripts/get_context.py
```

确认：
- 当前任务存在且已激活
- 任务目录路径

如果没有激活的任务，提示用户先通过 `trellis-continue` 开始任务。

### Step 2: 了解变更内容 `[AI]`

读取当前 PRD 和已有代码变更，理解上下文：

1. 读取 `prd.md` 了解当前需求
2. 运行 `git diff --name-only` 了解已有代码变更
3. 询问用户：需求哪里变了？

### Step 3: 更新 PRD `[AI]`

根据用户描述的变更，更新 `prd.md`：

- 在 `## Requirements` 中标注新增/修改/删除的需求
- 更新 `## Acceptance Criteria`
- 在 `## Technical Notes` 中记录变更原因

**格式建议**（在 PRD 中追加）：

```markdown
## 变更记录

### 变更 1: <变更标题> (YYYY-MM-DD)
- **原需求**: <原来是什么>
- **新需求**: <现在要什么>
- **原因**: <为什么要改>
- **影响范围**: <哪些已实现的代码需要调整>
```

### Step 4: 评估是否需要更新 Context 配置 `[AI]`

判断变更是否涉及新的模块或规范：

- 如果**不涉及新模块**：直接进入 Step 5
- 如果**涉及新模块**：先补充 context 配置

```bash
# 需要时追加 code-spec context
python3 ./.trellis/scripts/task.py add-context "$TASK_DIR" implement "<新路径>" "<原因>"
python3 ./.trellis/scripts/task.py add-context "$TASK_DIR" check "<新路径>" "<原因>"
```

### Step 5: 调用 Implement Agent `[AI]`

调用 Implement Agent 执行二次实现（code-spec context 由 hook 自动注入）：

```
Agent(
  subagent_type: "trellis-implement",
  prompt: "基于更新后的 prd.md 重新实现任务。

  注意：这是一次需求变更后的二次实现。
  - 阅读 prd.md 中的「变更记录」章节，理解哪些需求发生了变化
  - 保留已有的正确实现，只修改需要调整的部分
  - 如果变更涉及已实现的逻辑，确保修改后不破坏原有功能
  - 遵循所有已注入的 code-spec 规范
  - 完成后报告修改/新增的文件列表",
  model: "opus"
)
```

### Step 6: 调用 Check Agent `[AI]`

实现完成后，调用 Check Agent 验证（code-spec context 由 hook 自动注入）：

```
Agent(
  subagent_type: "trellis-check",
  prompt: "检查所有代码变更是否符合 code-spec 规范。

  重点关注：
  - 二次实现是否正确反映了 prd.md 中的变更需求
  - 新旧代码之间是否存在不一致
  - 修改是否引入了回归问题
  - 直接修复发现的问题
  - 确保 lint 和 typecheck 通过",
  model: "opus"
)
```

### Step 7: 报告结果 `[AI]`

输出二次实现的结果摘要：

```markdown
## 二次实现完成

### 需求变更
- <变更点 1>
- <变更点 2>

### 代码变更
- <修改的文件 1>: <做了什么>
- <修改的文件 2>: <做了什么>

### 验证状态
- [ ] Lint 通过
- [ ] Typecheck 通过
- [ ] Check Agent 验证通过

### 下一步
- 测试变更
- 确认无误后提交
- 运行 `trellis-finish-work` 检查清单
```

---

## 与其他入口的区别

| 入口 | 形态 | 阶段 | 说明 |
|------|------|------|------|
| `trellis-continue` | 命令 | 首次实现 | 完整流程：Research → Context → Implement → Check |
| `trellis-re-implement` | skill（本技能） | 二次实现 | 需求变更后：更新 PRD → Implement → Check |
| `trellis-finish-work` | 命令 | 完成 | 提交前检查清单 |

---

## 核心原则

| 原则 | 说明 |
|------|------|
| **增量修改** | 保留正确的已有实现，只改变需要调整的部分 |
| **PRD 先行** | 先更新 PRD 再调 Implement Agent，确保上下文准确 |
| **Context 自动注入** | implement.jsonl + prd.md 由 hook 自动注入，无需手动传递 |
| **记录变更原因** | 在 PRD 变更记录中说明为什么改、改了什么 |
