---
name: jw-agenda-planning-sync
description: "Planning sync: check consistency across all planning levels (tasks/TODO, yearly, monthly, weekly, daily), list discrepancies, batch update after user confirmation. Triggers: '同步规划', '检查一致性', 'planning sync', '运行 planning-sync'."
metadata:
  author: Jing Wu
  version: "0.2.0"
  updated: "2026-02-23"
---

# Planning Sync（规划同步助手）

检查 tasks 总待办、年规划、月规划、周规划、日计划之间的一致性，发现偏差后生成同步建议，**仅在用户确认后**批量更新。

**全层级检查原则**：本 Skill 覆盖规划体系的所有层级（tasks/TODO → 年 → 月 → 周 → 日），确保各层之间的任务内容对齐和完成状态同步。其他 Skill 在运行时会做各自方向的级联更新（daily-todo/weekly-plan 从上往下，daily-log/weekly-review 从下往上），本 Skill 作为**事后全局一致性检查**，捕捉遗漏的偏差。

建议运行时机见**本 Skill 的 `assets/conventions.md`** 的「Planning Sync 建议时机」。

## 安装前提

本 Skill 仅依赖用户 workspace 下存在 **jw-agenda 根目录**（默认 `jw-agenda-data`，可经 workspace 根目录的 `.jw-agenda.json` 或 `jw-agenda.json` 配置）及子目录 monthly、weekly、daily、tasks。约定与脚本已随本 Skill 安装，无需用户另行复制。先按 conventions 解析 jw-agenda 根目录。

## 约定

开始前读取**本 Skill 的 `assets/conventions.md`** 获取文件命名、路径和日期规则。

## 核心原则

1. **只读分析**：Step 1–4 仅读取和比较，不修改任何文件
2. **用户确认**：Step 5 必须获得用户明确同意后才执行更新
3. **最小变更**：只修改有偏差的部分，不做不必要的改动

## Workflow

### Step 1: 确定检查范围

使用本 Skill 的 `assets/scripts/date_utils.py` 计算日期和周数，然后按层级从上到下读取：

- **tasks 总待办**：`{agendaRoot}/tasks/TODO.md` 及其他 `todo-*.md`
- **年规划**（若存在）：`{agendaRoot}/yearly/YYYY-plan.md` 或类似路径
- **月**：`{agendaRoot}/monthly/YYYY-MM-plan.md`（当前月，如 2026-02-plan.md）
- **周**：`{agendaRoot}/weekly/Week{W}-plan.md`
- **日**：`{agendaRoot}/daily/{今天日期}-todo.md`（可选：最近 3–7 天的 todo 和 log）

缺失的层级跳过，向用户说明（见 Error Handling）。

### Step 2: 对比分析

从三个维度、跨所有可用层级检查一致性：

**维度 1 — 任务内容对齐（从上到下）**：
- tasks/TODO 中已标记「已规划」的任务，是否确实出现在月/周/日规划中？
- 月规划中本周/本日的任务，是否出现在周规划和日 todo 中？
- 周规划中今日的任务，是否出现在日 todo 中？
- 反向：日 todo / 周规划中的任务，是否在上层规划中有来源或已补入？

**维度 2 — 完成状态同步（从下到上）**：
- 日 todo / 日志中已完成（`[x]`）的任务，周规划中是否也已标记完成？
- 周规划中已完成的任务，月规划中对应条目是否已标记？
- 月规划中已完成的目标，年规划（若有）中是否已标记进展？
- 以**日执行为准**向上同步（见 conventions 中的冲突裁决策略）

**维度 3 — 新增/变更追踪**：日执行中新增的任务是否需补入周/月规划？取消/推迟的任务是否在各层级都已同步修正？

**内容对齐的比对策略**（维度 1 与 2 的判定方式）：
- **任务内容对齐**：采用**归一化后关键词匹配**。提取条目正文（去掉 `- [ ]` / `- [x]`、来源标记如 `*(来自规划)*` 等）后，对前后空格与换行做规范化；若两条目的核心描述一致（去掉标记后文本相同或一方包含另一方关键词子串），则视为「同一任务」。不要求精确逐字匹配，以便容忍用户微调措辞。
- **完成状态同步**：以**同一任务**为前提，比较日 todo 与周/月规划中的勾选状态（`[x]` vs `[ ]`）。若日已勾选而周未勾选，或周已勾选而日未勾选，则记为偏差；建议以**日执行为准**（见 conventions 中的冲突裁决策略）同步到周/月。

### Step 3: 偏差分类

| 级别 | 含义 | 示例 |
|------|------|------|
| ⚠️ 需行动 | 影响计划执行，建议立即同步 | 日已完成但周未勾选、周有今日任务但日 todo 未包含 |
| ℹ️ 信息性 | 不影响执行，供参考 | 日 todo 有额外临时任务未在规划中、日/周中的项来自 tasks 目录下 todo 开头清单（属合理来源） |

每条偏差附带：涉及的文件路径、具体位置、建议操作。

### Step 4: 生成同步建议

输出结构化的建议清单（使用 `assets/sync-report-template.md` 格式）。

### Step 5: 用户确认与执行

1. 向用户展示建议清单
2. 询问「是否按以上建议更新？可选择全部执行或指定编号」
3. **仅对用户同意的条目**执行文件修改
4. 汇报：更新了哪些文件、改动了哪些内容

## Error Handling

| 情况 | 处理 |
|------|------|
| 某层级文件不存在 | 跳过该层级，仅检查可用的层级 |
| tasks/TODO.md 不存在 | 跳过总待办检查 |
| 年规划不存在 | 跳过年规划检查（年规划为可选） |
| 仅有一个层级存在 | 无法做跨层对比，告知用户并建议先生成缺失的规划 |
| 无偏差 | 汇报「各层规划一致，无需同步」 |
| 用户不确认任何建议 | 汇报「未做任何修改」，不执行任何写操作 |

## 与其他 Skill 的配合（可选）

- 检查范围取决于用户数据目录中已有的文件。本 Skill 不依赖其他 Skill，但其他 Skill 产出的文件越多，检查越全面。
- 若安装了 **daily-todo / weekly-plan**：它们在调整任务时会从上往下级联更新（tasks/TODO → 月 → 周 → 日）；本 Skill 做的是事后全局一致性检查，捕捉遗漏的偏差。
- 若安装了 **daily-log / weekly-review**：它们在记录日志/回顾时会从下往上级联同步完成状态（日 → 周 → 月 → 年）；本 Skill 验证这些同步是否完整。

## Resources

- `assets/sync-report-template.md`：同步报告输出模板
- `assets/conventions.md`：约定
- `assets/scripts/date_utils.py`：日期计算脚本
