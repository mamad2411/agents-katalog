---
name: jw-agenda-daily-todo
description: "Daily todo manager: generate today's plan, reschedule items, add ad-hoc tasks. Triggers: '生成今天的计划', 'today plan', '把X移到周三', '加一项', '明天要', '运行 daily-todo'. (Marking completion is handled by daily-log.)"
metadata:
  author: Jing Wu
  version: "0.2.0"
  updated: "2026-02-23"
---

# Daily Todo（处理当天）

管理今日 todo 的全生命周期：生成、调整。

**时间表**：今日时间表用来安排每天要做的事项。**优先**读取用户工作区 jw-agenda 根目录下的 `schedule-config.md`（即 `{agendaRoot}/schedule-config.md`）的「时段定义」表；若该文件不存在，则使用本 Skill 的 `assets/schedule-config.example.md`。固定活动（如出门、晚餐）不覆盖，仅「（填入当日任务）」的时段填入具体事项。

**汇报规则**：每次新增或更新 todo 后，**必须告诉用户修改了哪些文件的实际路径**。

**级联更新原则**：当调整任务（添加、移动、推迟、取消等）时，**必须从上往下逐层检查并同步更新**，确保各层规划一致：

1. **tasks/TODO.md**（总待办）→ 若任务需从总待办中移除或标记已规划，更新此文件
2. **月规划**（monthly/YYYY-MM-plan.md）→ 若任务涉及本月目标或跨周变动，更新月规划
3. **周规划**（weekly/Week{W}-plan.md）→ 若任务涉及当周，更新周规划对应日
4. **日计划**（daily/YYYY-MM-DD-todo.md）→ 最终落到具体日期的 todo 文件

每一层只在确实受影响时才修改，但**必须逐层检查**，不可跳过。

## 安装前提

本 Skill 仅依赖用户 workspace 下存在 **jw-agenda 根目录**（默认 `jw-agenda-data`，可经 workspace 根目录的 `.jw-agenda.json` 或 `jw-agenda.json` 配置）及子目录 monthly、weekly、daily、tasks；可选 jw-agenda 根目录下的 `schedule-config.md` 用于自定义作息。约定与脚本已随本 Skill 安装，无需用户另行复制。先按 conventions 解析 jw-agenda 根目录。

## 约定

开始前读取**本 Skill 的 `assets/conventions.md`** 获取文件命名、路径、日期规则和来源标记格式。

## 模式选择

根据用户意图自动选择：

| 触发场景 | 模式 |
|---------|------|
| 「生成今天的计划」「today plan」 | 模式 A：生成（见下方） |
| 「今天完成得怎么样」「还剩哪些」 | 模式 B1：查询进度（见下方） |
| 「Y 不做了」「取消」「推迟」等 | 模式 B2：更新状态（见下方） |
| 「把 X 移到周三」「推迟到下周」「加一项」「明天要」「本月要」等 | 模式：添加/移动任务 → 读取 `references/mode-add-or-move.md` |

---

## 模式 A：生成今日 Todo

### Step 1: 确定日期

计算今天日期（YYYY-MM-DD）、当月、年内周数（推荐使用本 Skill 的 `assets/scripts/date_utils.py`）。

### Step 2: 读取来源

按顺序读取（缺失则跳过）：

1. **当月规划**：`{agendaRoot}/monthly/YYYY-MM-plan.md`（当前年月，如 2026-02-plan.md，可用 date_utils 推算），提取本月目标与本周重点
2. **当周规划**：`{agendaRoot}/weekly/Week{W}-plan.md`，提取「今天」对应的建议任务
3. **昨天未完成**：从 `{agendaRoot}/daily/{昨天日期}-log.md` 或 `{昨天日期}-todo.md` 中未勾选项
4. **tasks 目录下以 todo 开头的文件**（可选）：如 `{agendaRoot}/tasks/TODO.md`、`todo-readinglist.md`、`todo-*.md`。读取其中未勾选项，酌情纳入今日计划（如 1–2 项低优先级或按清单性质分配），并标记 `*(来自 tasks 清单)*` 或 `*(来自阅读清单)*`（若来自 todo-readinglist.md）

### Step 3: 合并、去重、排优先级

**幂等性检查**：若今日 todo 已存在，读取现有条目，归一化比较（忽略勾选状态、来源标记、前后空格），已存在的条目不再追加。

**去重规则**：从上述来源（月规划、周规划、昨天未完成、tasks 清单）中内容相同或高度相似的事项只保留一条。若某条既在昨天未完成又在规划中，以 `*(从昨天转移)*` 标记。

**来源标记与优先级**：按 `conventions.md` 中的来源标记和优先级标识规则执行。

### Step 4: 写入文件

**路径**：`{agendaRoot}/daily/{今天日期}-todo.md`

使用 `assets/todo-template.md` 模板，**必须包含**：

1. **今日时间表**：优先从 `{agendaRoot}/schedule-config.md` 读取时段配置；若不存在则从本 Skill 的 `assets/schedule-config.example.md` 读取。把当日任务填入各时段「安排」列。优先从周规划中「今天」的时段提取；若无，则按优先级合理分配。每个时段写具体事项。
2. **高/中/低优先级**：任务列表，与时间表一致，带来源标记，供逐项勾选。

若文件已存在，仅追加不重复的新条目；时间表若已存在则保留不覆盖。

### Step 5: 汇报

**必须首先说明**：已写入/已更新的文件路径。再说明各优先级项数、来源分布。

---

## 模式 B：追踪当日完成

### B1：查询进度

读取今日 todo，统计已完成（`[x]`）/ 未完成（`[ ]`），按优先级汇总，不修改文件。

### B2：更新状态

识别目标条目和新状态，在今日 todo 中更新：已完成 → `[x]`；进行中 → `[ ]` 加 `（进行中）`；取消 → `[x]` 加 `（取消）`；推迟无目标日 → 加 `（推迟）`；推迟有目标日 → 转入「添加/移动任务」模式（见 `references/mode-add-or-move.md`）。确认并说明已更新的文件路径。

---

## Error Handling

| 情况 | 处理 |
|------|------|
| 月/周/昨天来源不存在 | 跳过，用已有数据生成 |
| 三个主来源都不存在 | 生成空框架 todo，标注"无数据来源，请手动补充" |
| 今日 todo 已存在（模式 A） | 幂等处理：仅追加不重复的新条目 |
| 目标日期歧义（添加/移动任务） | 推算后向用户确认具体日期 |
| 临时追加目标文件不存在（添加/移动任务） | 可创建最小框架再追加，或告知用户 |

## 与其他 Skill 的配合（可选）

- **若安装了 daily-log**：它可能已写入今日 todo 的「从昨天转移」项，本 Skill 合并时会识别并保留不重复。未安装时不影响本 Skill 正常工作。
- **若安装了 weekly-plan**：本 Skill 读取其产出的周规划作为当日计划来源之一。未安装时跳过该数据来源。
- **若安装了 planning-sync**：可在本 Skill 运行后检查日/周/月一致性。未安装时不影响本 Skill。

## Resources

- `assets/todo-template.md`：每日 todo 输出模板
- `assets/conventions.md`：约定
- `assets/schedule-config.example.md`：默认作息模板（用户可选 jw-agenda 根目录下的 `schedule-config.md` 覆盖）
- `assets/scripts/date_utils.py`：日期处理工具
- `assets/scripts/dedup_todos.py`：去重工具
- `references/mode-add-or-move.md`：添加/移动任务详细流程
