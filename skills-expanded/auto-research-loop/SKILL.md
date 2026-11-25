---
name: auto-research-loop
description: 自动调研循环执行清单：plan → search → read → synthesize 的有界迭代，每步用 research_log 落盘（可跨压缩恢复），带明确的停止条件与来源纪律。适用于"帮我调研 X / 综述一下 X / 对比几个方案"类多步信息收集任务。
metadata:
  version: "0.1.0"
  reference: "https://github.com/Dominic789654/awesome-deepseek-harness"
---

# Auto-Research Loop

执行清单，不是教材。核心：**有界循环 + 每步落盘 + 来源可溯**。

## 0. 恢复

开始前先 `research_log(action: read, topic: <主题>)`。已有记录 → 从上次 phase 接着做，不重跑已完成的搜索。

## 1. Plan

1. 把任务拆成 3-6 个可回答的子问题；定义"做完"的标准（要回答什么、给谁看、多长）。
2. `research_log(append, phase: plan)` 记下子问题清单和停止条件。

## 2. Search（每轮 ≤3 个查询）

1. 每个子问题设计一个具体查询（关键词 + 限定词），用可用的搜索/抓取工具执行。
2. 只挑权威或一手来源进入 read 列表：官方文档 > 原始仓库/论文 > 高质量二手。
3. `research_log(append, phase: search, sources: [...])` 记录查询词、命中和弃选原因。

## 3. Read

1. 逐个读取入选来源，抽取与子问题直接相关的事实（数字、日期、结论），标注出处 URL。
2. 事实间冲突 → 两个说法都记，标注各自来源与日期，不要静默择一。
3. `research_log(append, phase: read, sources: [url])`，每个来源一条，note 写抽取到的事实而非"读了这篇"。

## 4. Synthesize & 循环判定

1. 对照 plan 里的子问题：哪些已有足够证据，哪些还缺。
2. `research_log(append, phase: synthesize)` 记录当前结论草稿和缺口。
3. **停止条件**（任一满足即进入 conclude）：
   - 所有子问题有 ≥2 个独立来源支撑；
   - 连续一轮搜索没有产生新信息（收益递减）；
   - 达到迭代上限（默认 3 轮 search→read→synthesize）。
4. 未满足 → 带着缺口回到步骤 2，只搜缺口，不重搜已覆盖的问题。

## 5. Conclude

1. 输出最终综述：按子问题组织，每个结论后附来源；冲突信息并列呈现。
2. 明确列出"未能确认"的项，不要用推测填补。
3. `research_log(append, phase: conclude)` 记录最终结论摘要。

## 红线

- 无来源的断言不进结论；引用只用自己真的打开过的 URL。
- 循环必须有界：到达上限就收敛汇报，不"再搜一轮"。
- 长任务中途压缩后，以 research_log 为准恢复状态，不凭记忆续写。
