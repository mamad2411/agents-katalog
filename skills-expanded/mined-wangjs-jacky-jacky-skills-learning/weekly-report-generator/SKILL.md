---
name: weekly-report-generator
description: 按公司模板生成结构化周报（Markdown）。在用户要求写周报、总结本周工作或生成状态汇报时使用。
---

# 周报生成器

使用公司模板生成规范的周报。

## 快速开始

向用户确认：
1. **周数/日期**：要汇报的是哪一周？
2. **工作项**：本周完成了什么？
3. **下周计划**：下周计划做什么？

然后按模板生成周报。

## 工作流

1. 向用户收集信息
2. 从 `assets/weekly-report-template.md` 复制模板
3. 填写模板各节：
   - 周数
   - 已完成工作项
   - 进行中工作
   - 下周计划
   - 阻塞/问题
4. 输出到 `output/weekly-report-week-XX.md`

## 模板结构

模板包含以下部分：
- **Overview（概述）**：周数与日期
- **Completed（已完成）**：本周完成的工作项
- **In Progress（进行中）**：当前进行中的工作
- **Next Week（下周计划）**：计划中的工作
- **Blockers（阻塞与问题）**：遇到的问题或阻塞

## 用户笔记 / 上下文

用户提供的日程或上下文（如「本周 3–4 点我在吃饭」）记录在 **`notes/weekly-context.md`**。生成周报时可参考该文件，用于补充或解释时间安排。

## 资源

- `assets/weekly-report-template.md`：公司周报模板
- `examples/`：已填写示例，供参考
- `notes/weekly-context.md`：本周上下文/笔记，生成周报时参考
