---
name: excel-orchestrate
description: |
  **Default entry point — all Excel file operations should consider this skill first.**

  ## Auto-trigger Conditions (any one suffices) / 自动触发条件（满足任一即触发）

  ### Condition 1: User mentioned an Excel file / 条件一：用户提到了 Excel 文件
  As long as an Excel file (.xlsx / .xlsm / .csv / .xls / spreadsheet / workbook / worksheet) appears in context,
  AND the user is describing an operation to perform on it (modify/format/delete/merge/split/sort/dedup/filter/date/insert etc.),
  trigger this skill first — even if only one operation is described.

  ### Condition 2: Multi-step operations / 条件二：多步骤操作
  - Multiple operations in one sentence
  - Delimiter-separated requirements
  - Parallel phrasing: "first...then...finally..."
  - Connective words: "also" "additionally" "and" "meanwhile" "at the same time"

  ### Condition 3: Vague/summary commands / 条件三：模糊/总结性指令
  - "Process this file" "Handle this" "Take care of this" "Organize this"

  ## Non-trigger exceptions / 不触发的例外
  - Pure query/scout: just asking "how many rows" "are there nulls" → directly use excel-scout
  - User explicitly names a skill → directly use that skill

  Trigger keywords (not limited to): ".xlsx" ".csv" "spreadsheet" "Excel" "process" "batch" "full workflow" "all" "organize"
  触发词（不限于此）：".xlsx"".csv""表格""Excel""处理一下""批量""整个流程""全部""搞定""整理""先…再…""然后""还有""另外""并且""以及""同时""要求如下""以下几项"。

  Workflow: Confirm it's an Excel operation → Call excel-scout for reconnaissance → Output report → User confirms → Execute one by one.
  工作流程：确认是Excel操作 → 调 excel-scout 勘察 → 出报告 → 用户确认 → 逐个执行。
---

> This skill is a **meta-skill** — it does not directly operate on Excel, but orchestrates the existing 16 skills. Follows the "Decompose→Report→Confirm→Execute" four-step approach.
> 本技能是**元技能**——不直接操作 Excel，而是编排已有的 16 个技能。遵循"拆分→报告→确认→执行"四步。

# Excel Task Orchestration / Excel 任务编排

## Workflow / 工作流程

```
User Complex Requirements / 用户复杂需求
    │
    ▼
[0] Scout First / 勘察先行 → Call excel-scout to locate target columns, show current values
    │
    ▼
[1] Parse Requirements / 解析需求 → Match scout results, decompose into independent sub-tasks
    │
    ▼
[2] Match Skills / 匹配技能 → Each sub-task maps to an existing skill
    │
    ▼
[3] Output Report / 输出报告 → Table showing execution plan (order, skill, input, expected output)
    │
    ▼
[4] User Confirms / 用户确认 → After confirmation, call skills one by one
    │
    ▼
[5] Summarize Results / 汇总结果 → Report status after each step completes
```

## 已有技能速查 / Available Skills Quick Reference

| 分类 | 技能 | 能干什么 |
|------|------|------|
| 🔍 查 | `scout` | 操作前勘察——定位目标列、展示当前值 |
| | `find-duplicates` | 扫描重复行 |
| | `filter` | 按条件筛选行 |
| | `validate` | 数据质量检查 |
| 🗑️ 删 | `delete` | 删除行/列 |
| | `deduplicate` | 去重 |
| ✏️ 改 | `insert` | 插入行/列 |
| | `replace` | 查找替换 |
| | `mapping-replace` | 按映射表批量替换 |
| | `regex-clean` | 正则清理（提取/删除/替换） |
| | `date-to-text` | 日期转文本 |
| | `format` | 设置格式 |
| 📊 整 | `sort` | 排序 |
| | `split` | 按列拆分文件 |
| | `merge` | 合并多个文件 |
| | `freeze` | 冻结窗格 |
| 📋 基 | `safe-workflow` | 安全四步法 |

## 拆分原则 / Decomposition Principles

1. **依赖关系**：合并/筛选在前，改值/格式化在后
2. **文件来源**：先搞定输入（merge），再处理内容
3. **同类合并**：多个 mapping-replace 可以一次 XML 处理完成
4. **大文件优先 XML**：>10MB 的行操作自动走 XML 方案
5. **不可逆操作靠后**：删除类操作确认后再执行

## 报告格式 / Report Format

```
任务拆分报告 / Task Decomposition Report
═══════════════

原始需求: [用户原话]

执行计划:
| 序号 | 步骤 | 技能 | 输入 | 预期输出 |
|------|------|------|------|------|
| 1 | 合并28个文件 | excel-merge | 1000万-5000万/ | 单一xlsx |
| 2 | 日期列插文本 | excel-date-to-text | 合并结果 | 6个新列 |
| 3 | 类型→数字 | excel-mapping-replace | 合并结果 | 列值替换 |
| 4 | 国别→代码 | excel-mapping-replace | 合并结果 | 列值替换 |
| 5 | 新兴产业清理 | excel-regex-clean | 合并结果 | 列值清理 |

预计耗时: ~30分钟
风险点: 合并时需处理sharedStrings引用断裂

确认执行? (yes/no)
```

## 执行 / Execution

用户确认后，按顺序执行每步。每步完成后报告状态：

```
[1/5] excel-merge... done (451s, 333669行)
[2/5] excel-date-to-text... done (771s, 6列)
[3/5] excel-mapping-replace... done (697s)
[4/5] excel-mapping-replace... (已合并到第3步)
[5/5] excel-regex-clean... (已合并到第3步)

全部完成 / All Complete, 输出 / Output: 测试文件/终极合并.xlsx
```

## 注意事项

1. **先报告再执行**：拆分结果必须让用户看到并确认
2. **步骤间传递文件**：上一步的输出是下一步的输入，自动管理文件路径
3. **同类操作合并**：多个 mapping-replace 和 regex-clean 可一次 XML 处理，减少读盘次数
4. **失败处理**：某步失败时暂停，删除损坏产物，从备份恢复，询问用户是否继续或修改方案
5. **sharedStrings 警告**：如果涉及 merge + mapping-replace，提醒 sharedStrings 转换问题
6. **每步自动备份**：每个子任务执行前自动备份（时间戳命名），全部成功后仅保留最新3份
