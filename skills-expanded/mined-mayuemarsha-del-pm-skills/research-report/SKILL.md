---
name: research-report
description: Write structured research reports when the task is to 调研某个产品 / 赛道 / 竞品 / 能力方向，整理成正式调研报告，做横向对比分析，或输出"背景、目标、产品清单、摘要总结、调研明细"的研究文档。Use when the user asks for 调研报告、产品调研、竞品调研、应用层产品分析、页面结构对比、架构 / 算法 / 计费方式对比，尤其 when the output must first give 结论 and then detailed analysis.
---

# Research Report

Use this skill for formal research reports.

## 1. Default workflow

### Step 1: define the task before researching
Before doing any research, first state:
1. 任务背景
2. 调研目标
3. 调研范围 / 产品清单
4. 执行步骤（3~7条）

If the scope is too broad, narrow it or explicitly say what is included/excluded.

### Step 2: collect facts
Research by category, not randomly.
Typical dimensions:
- 产品定位
- 目标用户
- 页面结构
- 核心功能
- 算法 / 架构
- 计费方式
- 对我们的启示

When information is uncertain, mark it as 待确认 instead of guessing.

### Step 3: summarize before details
Always write summary first, then details.
Do not dump notes in chronological order.

### Step 4: produce a report, not raw notes
The output should read like a formal report, not a chat log or research scratchpad.

---

## 2. Default report structure

Research reports default to this structure:

1. 背景与目标
   - 调研背景
   - 调研目标
   - 调研范围 / 产品清单
2. 摘要总结
   - 分类结论
   - 关键差异总结
   - 对我们的启示
3. 调研明细
   - 按分类或按产品展开
4. 选型建议 / 结论建议（if relevant)
5. 附录
   - 参考链接
   - 备注 / 待确认项

## 3. Product-level detail standard

If the report compares products, each important product should preferably include:
1. 产品定位
2. 页面结构
3. 核心功能按钮 / 模块
4. 算法 / 架构特点
5. 计费方式
6. 对我们的启示

Do not keep all products at headline level only. The report should support follow-up product judgment.

## 4. Writing rules

### A. Start with conclusions
- 先给分类和差异结论
- 再给支持这些结论的产品细节
- 让读者先抓重点，再决定是否看细节

### B. Separate fact from judgment
Clearly distinguish:
- 事实：公开信息、产品页面、定价、功能
- 判断：差异、趋势、启示、建议

### C. Prefer comparison tables
For multi-product research, prefer tables for:
- 分类
- 页面结构
- 功能模块
- 算法架构
- 计费方式
- 选型建议

### D. Keep product categories explicit
For AI product reports, usually classify before comparing.
Typical categories include:
- 通用助手
- 垂直应用（如客服 AI）
- Agent 平台
- LLM 开发平台
- 执行型 Agent

Do not mix all products in one flat list without a taxonomy.

### E. Mark uncertainty explicitly
If some product details are not directly confirmed:
- write `待确认`
- state the basis of current judgment
- do not fabricate precise UI/function details

## 5. PM preferences

Default style:
- 默认短答，但正式调研报告可以完整
- 先结论后细节
- 先交代背景和目标，不要直接堆产品信息
- 输出能直接作为团队内部讨论材料使用

If the report is about AI products, try to include these angles when relevant:
- 页面结构
- 功能边界
- 算法 / Agent 架构
- 计费方式
- 与自家产品的启示

## 6. High-frequency mistakes to avoid

- 不先定义范围，直接开查
- 只列产品，不做分类
- 只有摘要，没有产品级细节
- 只有产品细节，没有总结和判断
- 事实和推测混在一起
- 明明没确认，还写得像确认过
- 只写国外产品，不看国内替代或相邻产品

## 7. Final self-check

Before finishing, verify:
1. 有没有写背景和目标？
2. 有没有给出调研产品清单？
3. 有没有先写摘要总结？
4. 重点产品有没有产品级明细？
5. 有没有区分事实和判断？
6. 有没有明确待确认项？
7. 这份内容能不能直接拿给团队评审？
