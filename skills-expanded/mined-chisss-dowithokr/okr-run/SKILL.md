---
name: okr-run
description: Run the full DoWithOKR workflow from client need to GM OKR, role tree, role OKR, delivery acts, status board, scoring, and final result.
---

# OKR Run

## 前置条件

- 需要：用户自然语言需求描述（全新执行时）。
- 缺失处理：
  - 全新执行但无需求 → 提示用户输入需求。
  - 断点续跑 → 无需额外输入，从上次进度继续。

## 前置读取

- 检查 `.okr/active.md` 是否存在。
  - 存在且包含 `current_act` → 断点续跑模式：
    - 读取 `current_act` 确定当前交付幕。
    - 扫描 `.okr/status.md` 统计各 KR 的实际状态（未开始 / 进行中 / 阻塞 / 已完成 / 放弃）。
    - 综合两者生成进度摘要，供用户决策。
  - 存在但用户要求重新开始 → 归档到 `.okr/archive/<YYYY-MM-DD>-active.md`，重新初始化。
  - 不存在 → 全新执行，从 M0 开始。
- 读取用户输入的自然语言需求（全新执行时必须）。
- 状态文件结构（含归档目录）：
  ```text
  .okr/
    active.md
    status.md
    evidence/
    reviews/
    archive/            # 历史快照归档
      <YYYY-MM-DD>-active.md
      <YYYY-MM-DD>-status.md
  ```

## 执行规则

- 用于全自动闭环执行。
- 固定主链路：甲方需求 → GM OKR → 角色树 → 角色 OKR → 交付幕计划 → 角色执行 → 状态看板 → 上级评分 → 最终 R。
- 写入状态文件、高风险操作、范围变化、证据不足标记完成前必须请求用户确认。
- 每个阶段必须更新状态：未开始、进行中、阻塞、已完成、放弃。
- 每个完成项必须有证据。

## 状态机

### 转换表

| 当前幕 | 退出门禁 | 验证方式 | 通过 → 下一幕 | 未通过处理 |
| --- | --- | --- | --- | --- |
| M0 | 用户确认 GM OKR | `active.md` 含 `## GM OKR` 且用户确认 | → M1 | 停留 M0，修改后重新确认 |
| M1 | 所有 GM KR 有负责人 | `active.md` 含 `## 角色树` + `## 层级 OKR`；`status.md` 已创建 | → M2 | 停留 M1，提示补充角色或 KR 映射 |
| M2 | 产品方案和技术方案明确 | PD 和 ArchD KR 状态 ≠ 未开始；`active.md` 含 `## 交付验证计划`；用户确认方案 | → M3 | 停留 M2，继续执行方案角色 |
| M3 | 关键 KR 有证据且自检达标 | `status.md` 中 M3 阶段 KR 均有证据或标记为放弃；角色自检结果达标 | → M4 | 停留 M3，列出缺失证据和未达标的 KR |
| M4 | 评分和复盘完整 | `reviews/` 下存在评分文件；用户确认最终 R | → 完成 | 停留 M4，补充评分 |

### 子技能调用序列

| 幕 | 调用序列 | 用户确认点 |
| --- | --- | --- |
| M0 | `okr-gm` | GM OKR 确认 |
| M1 | `okr-role-splitter` → `okr-planner` | 无（自动流转） |
| M2 | `okr-execution-plan` → `okr-role-run(PD)` → `okr-role-run(PM)` → `okr-role-run(UI)` → `okr-role-run(ArchD)` → `okr-status-tracker` | 方案确认 |
| M3 | `okr-role-run(BE)` → `okr-role-run(FE)` → `okr-role-run(QA)` → `okr-role-run(DevOps)` → `okr-role-run(SEC)` → `okr-role-run(TW)` → `okr-alignment-check` → `okr-status-tracker` | 无（门禁自动检查：证据 + 自检达标） |
| M4 | `okr-review-score` → `okr-next-cycle` | 最终 R 确认 |

## 执行步骤

### 启动判断

1. 检查 `.okr/active.md` 是否存在。
2. 如果存在，读取 `current_act` 并扫描 `status.md` 获取实际 KR 状态：
   - 统计各状态 KR 数量（未开始 / 进行中 / 阻塞 / 已完成 / 放弃）。
   - 展示进度摘要：
     - 当前交付幕：`current_act` 值（如 M2 方案成型幕）。
     - 已完成 KR：X / 总 KR 数。
     - 进行中 KR：列出 KR 编号和对应角色。
     - 阻塞项：列出阻塞的 KR 编号、阻塞原因和影响范围。
   - 给用户 3 个选项：
     1. **从断点继续**：从 `current_act` 对应的幕继续执行，跳过已完成的步骤。
     2. **重新开始**：将当前 `.okr/active.md` 归档到 `.okr/archive/<YYYY-MM-DD>-active.md`，同时归档 `status.md` 到 `.okr/archive/<YYYY-MM-DD>-status.md`，然后重新初始化，从 M0 开始。
     3. **取消**：不执行任何操作，退出。
3. 如果不存在，进入 M0 全新执行。
4. 如果用户选择"重新开始"：
   - 创建 `.okr/archive/` 目录（如不存在）。
   - 归档当前状态文件。
   - 清空 `.okr/active.md` 和 `.okr/status.md`，从 M0 开始。

### M0 需求转译幕

4. 调用 `okr-gm`：将甲方需求转成 GM OKR。
5. 验证：`.okr/active.md` 包含 `## GM OKR` 区块。
6. **用户确认点**：展示 GM OKR，等待用户确认后继续。

### M1 组织拆解幕

7. 调用 `okr-role-splitter`：生成角色树。
8. 验证：`.okr/active.md` 包含 `## 角色树` 区块。
9. 调用 `okr-planner`：生成层级 OKR 和交付幕计划。
10. 验证：`.okr/active.md` 包含 `## 层级 OKR` 和 `## 交付幕计划`；`.okr/status.md` 已创建。

### M2 方案成型幕

11. 调用 `okr-execution-plan`：生成交付验证计划（验收标准 + 验证方法 + 证据类型）。
12. 调用 `okr-role-run`：执行 PD 产品总监角色 OKR。
13. 调用 `okr-role-run`：执行 PM 产品经理和 UI 设计师角色 OKR。
14. 调用 `okr-role-run`：执行 ArchD 技术总监角色 OKR。
15. 调用 `okr-status-tracker`：展示当前看板。
16. **用户确认点**：展示方案摘要，等待用户确认后进入构建阶段。

### M3 构建验证幕

17. 按推荐顺序调用 `okr-role-run`：BE → FE → QA → DevOps → SEC → TW（按角色树裁剪结果跳过不参与的角色）。
17. 每个角色执行后调用 `okr-alignment-check`：检查交付结果是否满足 KR 标准。
18. 调用 `okr-status-tracker`：展示当前看板。
19. **门禁检查**：关键 KR 是否有证据且自检结果达标。未通过 → 停留 M3，提示缺失项和未达标项。

### M4 收敛复盘幕

20. 调用 `okr-review-score`：上级评分并汇总最终 R。
    - `okr-review-score` 完成评分后会执行周期归档与清理（归档 active.md、status.md、evidence/、reviews/ 到 `.okr/archive/<date>-cycle/`，清空工作区，保留 wisdom/ 和 archive/）。
    - 归档前需用户确认。
21. 调用 `okr-next-cycle`：生成下一轮建议。
    - 如果用户确认本轮结束且 `okr-review-score` 已完成归档，则 `okr-next-cycle` 跳过归档。
    - 如果用户在 `okr-review-score` 阶段拒绝了归档，`okr-next-cycle` 在用户确认结束时再次触发归档。
22. **用户确认点**：展示最终 R 和下一轮建议，等待用户决定。

### 失败回退

- 任一步骤的前置读取失败 → 停止并报告缺失的前置条件和建议操作。
- 门禁未通过 → 停留当前幕，列出未满足的退出条件。
- 用户拒绝确认 → 回退到当前幕起点，允许用户修改后重新执行。

## 输出格式

先输出全局摘要，再按交付幕展示 GM OKR、角色树、执行计划、OKR 状态看板、上级评分、最终 R。

必须包含：

- 当前交付幕
- 上级映射
- 证据
- 下一步

## 异常处理

- 用户中途要求跳过某个幕：允许跳过但提示风险（如跳过 M2 直接进入 M3 可能导致方案不明确）。
- 某个角色执行失败或阻塞：记录阻塞状态，继续执行其他角色，最后汇总阻塞项。
- 用户中途修改需求：暂停执行，回到 M0 重新生成 GM OKR，保留已有角色树和执行记录供参考。

## 产出写入

- 本技能通过调用子技能间接写入所有 `.okr/` 文件。
- 每个子技能调用后验证其产出文件已正确写入。
- 更新 `.okr/active.md` frontmatter 的 `current_act` 为当前执行到的交付幕。
- **Web 事件发射**：每个子技能调用完成后，追加一行 JSON 到 `.okr/web/events.jsonl`（目录不存在时自动创建）。事件格式：
  ```json
  {
    "time": "2026-05-01T10:00:00+08:00",
    "skill": "okr-role-run",
    "act": "M3",
    "role": "BE",
    "status": "completed",
    "changed": [".okr/status.md", ".okr/evidence/BE-KR1.md"],
    "summary": "BE-KR1 已完成接口实现"
  }
  ```
  `status` 取值：`completed`、`failed`、`skipped`。`.okr/` 文件仍是唯一状态源，事件仅用于通知 Web 控制台刷新。
