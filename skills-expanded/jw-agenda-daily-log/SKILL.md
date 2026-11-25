---
name: jw-agenda-daily-log
description: "Daily log generator: summarize yesterday or accept today's progress (casual or single-sentence), generate dated log file, update today's todo checkboxes, transfer incomplete to today. Triggers: '整理昨天的日志', '总结昨天', '汇报今天', '记录一下今天', '我完成了 X', '作业做完了', 'daily log', '运行 daily-log'."
metadata:
  author: Jing Wu
  version: "0.2.0"
  updated: "2026-02-23"
---

# Daily Log（日志与汇报）

总结昨天的工作并生成日志，或将当天口语化汇报整理成日志；未完成事项转移到今日 todo。
记录已经完成的或正在进行的事项的进度。

**与 daily-todo 的分工**：若是未完成、未开始事件的调整，由daily-todo来完成。

**口语化汇报**：用户汇报进度时可能很口语、带想法。从汇报中解析出：完成的事、未完成的、时间分配；想法、感受、随口说的内容单独放进日志的「今日想法/随口记」区块，原意保留、不丢弃。汇报后必须告诉用户日志写入路径。

**级联状态同步原则**：记录日志后，**必须从下往上逐层检查并同步完成状态**，确保各层规划反映实际进度：

1. **日计划**（daily/YYYY-MM-DD-todo.md）→ 勾选已完成项 `[x]`，标记进行中 `（进行中）`
2. **周规划**（weekly/Week{W}-plan.md）→ 在对应日的任务旁标记完成 `[x]` 或进行中状态
3. **月规划**（monthly/YYYY-MM-plan.md）→ 若完成的事项属于月目标/重点任务，标记其完成状态
4. **年规划**（若存在）→ 若完成的事项属于年度目标，标记其进展

**注意**：对上层规划文件（周/月/年）只做**轻量标记**（完成 `[x]`、进行中等），不改动原有规划内容。详细记录仍保留在日志文件中。每一层只在确实受影响时才修改，但必须逐层检查，不可跳过。

## 安装前提

本 Skill 仅依赖用户 workspace 下存在 **jw-agenda 根目录**（默认 `jw-agenda-data`，可经 workspace 根目录的 `.jw-agenda.json` 或 `jw-agenda.json` 配置）及子目录 monthly、weekly、daily、tasks；可选 jw-agenda 根目录下的 `schedule-config.md` 用于自定义作息。
先按 conventions 解析 jw-agenda 根目录。

## 约定

开始前读取**本 Skill 的 `assets/conventions.md`** 获取文件命名、路径和日期规则。

## 两种用法

| 用户意图 | 处理方式 |
|----------|----------|
| 总结昨天 / 整理昨天的日志 | 读昨天 todo 与已有数据 → 生成昨天日志 → 未完成转移今天 |
| 汇报今天 / 记录一下今天（含口语、想法） | 解析用户当天的口语化汇报 → 生成今天日志 → 同步更新今天 todo 勾选 → 未完成保留或转移 |

---

## Workflow

### Step 1: 确定日期与数据来源

- **若用户要「总结昨天」**：计算昨天日期（推荐使用本 Skill 的 `assets/scripts/date_utils.py`）；读取 `{昨天日期}-todo.md`、`{昨天日期}-log.md`（若有）；从数据中识别已完成 / 未完成 / 时间分配 / 学习产出。
- **若用户「汇报今天」（口语化）**：计算今天日期；从用户输入中解析完成的事、未完成、时间或顺序、想法/感受/碎碎念。

### Step 2: 生成日志文件

使用 `assets/log-template.md` 模板，填充变量后写入：

**路径**：jw-agenda 根目录下的 `daily/{目标日期}-log.md`（即 `{agendaRoot}/daily/{目标日期}-log.md`）

**模板变量**：`{{DATE}}`、`{{COMPLETED_TASKS}}`、`{{TIME_ALLOCATION}}`、`{{ACTUAL_WORK_TIME}}`（实际工作/学习时长汇总，如「约 6h50（德语约 50min + jw-agenda skills 约 6h）」）、`{{LEARNING_OUTPUT}}`、`{{INCOMPLETE_TASKS}}`、`{{SUMMARY}}`、`{{NOTES_AND_THOUGHTS}}`（想法/随口记，无则写「无」）、`{{TIMESTAMP}}`。

若 jw-agenda 根目录下的 `daily/` 不存在则创建。

### Step 3: 从下往上级联同步状态

按以下顺序逐层检查并更新：

#### 3a: 日计划（daily/YYYY-MM-DD-todo.md）

- **若本次是「汇报今天」**：在 `{今天日期}-todo.md` 中根据完成项勾选 `[x]`，进行中的标记 `（进行中）`；若今日 todo 不存在则只写日志。
- **若本次是「总结昨天」**：在 `{昨天日期}-todo.md` 中勾选已完成项；有未完成项则在 `{今天日期}-todo.md` 追加，标记 `*(从昨天转移)*`，跳过已存在条目。

#### 3b: 周规划（weekly/Week{W}-plan.md）

- 检查本次完成/进行中的任务是否出现在当周规划中
- 若出现，在周规划对应日/条目旁标记完成 `[x]` 或 `（进行中）`
- **只做标记，不改动规划内容本身**

#### 3c: 月规划（monthly/YYYY-MM-plan.md）

- 检查本次完成的任务是否属于月目标或月重点任务
- 若属于，在月规划对应条目旁标记完成状态
- **只做轻量标记，不改动规划结构**

#### 3d: 年规划（若存在）

- 检查本次完成的任务是否与年度目标相关
- 若相关，在年规划对应条目旁标记进展
- **只做轻量标记**

**注意**：每一层只在确实受影响时才修改，但必须逐层检查，不可跳过。对上层文件的修改仅限于状态标记，详细内容保留在日志文件中。

### Step 4: 汇报

向用户说明：已写入日志路径、完成概况、转移数量、**已同步状态的所有文件路径**。

## Error Handling

| 情况 | 处理 |
|------|------|
| 昨天 todo 不存在 | 仅从已有文件推断活动，若也无内容则生成空模板日志 |
| 昨天日志已存在 | 向用户确认是否覆盖或追加，默认不覆盖 |
| 目录不存在 | 自动创建 |
| 今日 todo 已存在且含相同条目 | 跳过重复条目 |

## 与其他 Skill 的配合（可选）

- 若安装了 **daily-todo**：它会读取本 Skill 写入的「从昨天转移」项，合并时保留不重复。未安装时不影响本 Skill。
- 若安装了 **weekly-review**：它会汇总本 Skill 产出的每日日志。未安装时不影响本 Skill。

## Resources

- `assets/log-template.md`：日志输出模板
- `assets/conventions.md`：约定
- `assets/scripts/date_utils.py`：日期计算脚本
