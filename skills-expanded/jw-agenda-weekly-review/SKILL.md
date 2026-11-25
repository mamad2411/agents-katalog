---
name: jw-agenda-weekly-review
description: "Weekly review: aggregate daily logs, compute completion rate and time allocation, generate summary, list carry-over items; archive daily files older than 2 weeks into YYYYMM subdirs. Triggers: '周总结', '本周回顾', 'weekly review', '运行 weekly-review'."
metadata:
  author: Jing Wu
  version: "0.2.0"
  updated: "2026-02-23"
---

# Weekly Review（周回顾）

汇总本周日志与 todo，统计完成率和时间分配，生成周总结报告，识别转入下周的事项。

**级联状态同步原则**：生成周回顾后，**必须从下往上逐层检查并同步完成状态**，确保各层规划反映实际进度。数据来源是本周的每日日志（daily log）和每日 todo，以此为依据逐层向上同步：

1. **每日日志/日计划**（daily/{日期}-log.md、{日期}-todo.md）→ 这是事实来源，汇总本周各天的完成情况
2. **周规划**（weekly/Week{W}-plan.md）→ 根据日志汇总的实际完成情况，标记各任务的完成 `[x]` 或未完成状态
3. **月规划**（monthly/YYYY-MM-plan.md）→ 若本周完成的事项属于月目标/重点任务，在月规划对应条目旁标记完成状态
4. **年规划**（若存在）→ 若本周完成的事项与年度目标相关，标记进展

**注意**：对上层规划文件（周/月/年）只做**轻量标记**（完成 `[x]`、进行中等），不改动原有规划内容。详细分析保留在周回顾文件中。每一层只在确实受影响时才修改，但必须逐层检查，不可跳过。

## 安装前提

本 Skill 仅依赖用户 workspace 下存在 **jw-agenda 根目录**（默认 `jw-agenda-data`，可经 workspace 根目录的 `.jw-agenda.json` 或 `jw-agenda.json` 配置）及子目录 monthly、weekly、daily、tasks。约定与脚本已随本 Skill 安装，无需用户另行复制。先按 conventions 解析 jw-agenda 根目录。

## 约定

开始前读取**本 Skill 的 `assets/conventions.md`** 获取文件命名、路径和周数规则。

## Workflow

### Step 1: 确定回顾范围

使用本 Skill 的 `assets/scripts/date_utils.py` 计算本周/上周的日期范围和年内周数（1–52）。

- **默认**：本周（周一至周日）
- 若用户说「上周回顾」，则使用上周日期范围

### Step 2: 汇总数据

读取本周范围内的所有文件：

**主要来源**：
- `{agendaRoot}/daily/{日期}-log.md`：逐日读取，提取已完成、未完成、时间分配、学习/产出
- `{agendaRoot}/daily/{日期}-todo.md`：逐日读取勾选状态，交叉验证日志

**可选来源**：
- `{agendaRoot}/weekly/Week{W}-plan.md`：对比计划 vs 实际

记录哪些天有数据、哪些天缺失。

### Step 3: 统计分析

**完成率**：`已勾选项总数 / 总项数 × 100%`，某天无 todo 文件则不纳入。分别统计高/中/低优先级。

**时间分配**：从每日日志的「时间分配」部分提取，按类别汇总。

**产出汇总**：从每日日志的「学习/产出」部分汇总为列表。

### Step 4: 生成周总结

使用 `assets/review-template.md` 模板，填充后写入：

**路径**：`{agendaRoot}/weekly/Week{W}-review.md`（W = 年内周数，1–52，与周规划命名一致）

**内容**：整体概览（完成率、主要成就）、分类统计、未完成/待处理、**转入下周**清单。

### Step 5: 从下往上级联同步状态

基于 Step 2-3 从每日日志和每日 todo 中汇总的实际完成情况，逐层向上同步：

#### 5a: 周规划（weekly/Week{W}-plan.md）

- 根据每日日志汇总的实际完成情况，在周规划中标记各任务状态：完成 `[x]`、未完成保持 `[ ]`、进行中标记 `（进行中）`
- **只更新状态标记，不改动规划内容本身**

#### 5b: 月规划（monthly/YYYY-MM-plan.md）

- 检查本周完成的任务是否属于月目标或月重点任务
- 若属于，在月规划对应条目旁标记完成状态或进展
- **只做轻量标记，不改动规划结构**

#### 5c: 年规划（若存在）

- 检查本周完成的任务是否与年度目标相关
- 若相关，在年规划对应条目旁标记进展
- **只做轻量标记**

**注意**：每一层只在确实受影响时才修改，但必须逐层检查，不可跳过。

### Step 6: 归档 daily 目录（二周以前）

按 `conventions.md` 中的 **daily 目录归档规则** 执行：

- 扫描 `{agendaRoot}/daily/` 根下的 `YYYY-MM-DD-todo.md`、`YYYY-MM-DD-log.md` 文件
- 若文件日期早于「今天 − 14 天」，则移入 `{agendaRoot}/daily/YYYYMM/` 子目录（如 `202601/`、`202602/`）
- 若子目录不存在则创建；同一月的文件归入同一子目录
- 归档后向用户说明移入了多少文件、目标子目录

### Step 7: 汇报

说明：周总结文件路径、完成率、时间分配要点、转入下周事项数量、归档文件数（若有）、**已同步状态的所有文件路径**。

## Error Handling

| 情况 | 处理 |
|------|------|
| 部分日期缺少日志 | 用已有日志统计，在报告中标注缺失日期 |
| 全部日期无日志 | 询问用户是否仍需生成空框架 |
| 日志中无时间分配信息 | 跳过时间统计，在报告中标注 |
| 周总结已存在 | 向用户确认是否覆盖，默认不覆盖 |
| 无 todo 文件 | 仅统计日志中的完成/未完成项 |

## 与其他 Skill 的配合（可选）

- 若安装了 **daily-log**：本 Skill 汇总其产出的每日日志。未安装时从 daily todo 文件推断完成情况。
- 若安装了 **daily-todo**：每日 todo 的完成状态用于计算完成率。未安装时从日志推断。
- 若安装了 **weekly-plan**：下周生成周规划时，可读取本 Skill 的「转入下周」部分。未安装时不影响本 Skill。

## Resources

- `assets/review-template.md`：周总结输出模板
- `assets/conventions.md`：约定
- `assets/scripts/date_utils.py`：日期计算脚本
