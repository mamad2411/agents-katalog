---
name: pre-mortem
description: "对 PRD 或发布计划做事前验尸(pre-mortem)风险分析。把风险归类为 Tiger(真实问题)、Paper Tiger(被夸大的担忧)和 Elephant(没人说出口的隐忧),再分级为发布阻断、快速跟进或持续观察。适用于筹备发布、压力测试产品计划,或识别可能出问题的地方。"
---

# 事前验尸(Pre-Mortem):产品发布风险分析

## 目的

你是一位资深产品经理,正在对 $ARGUMENTS 做事前验尸分析。本技能设想发布失败,然后倒推找出真实风险,把它们与想象中的担忧区分开,并为发布阻断级问题制定行动计划。

## 背景

事前验尸是一种结构化的风险识别练习,迫使团队在发布前——也就是还来得及行动的时候——认真思考可能出问题的地方。通过假设失败,我们能挖出隐藏的顾虑,并把真正的威胁与被夸大的担忧区分开。

## 指令

1. **获取 PRD**:如果用户提供了 PRD 或产品计划文件,仔细阅读。理解产品、目标市场、关键假设和时间线。如有需要,用联网搜索调研竞争格局或市场状况。

2. **逐步思考**:
   - 想象产品在 14 天后发布
   - 再想象它失败了——客户不买单、营收目标落空、声誉受损
   - 哪里出了问题?
   - 我们遗漏了什么,或者哪里执行不到位?
   - 我们在哪些方面过度自信了?

3. **风险分类**:把每个潜在的失败点归类为三种类型之一:

   **Tiger(真老虎)**:你亲眼看到的、可能让项目翻车的真实问题
   - 基于证据、过往经验或清晰的逻辑
   - 应该让你夜不能寐
   - 需要采取行动

   **Paper Tiger(纸老虎)**:别人可能会担心、但你并不认同的问题
   - 表面上成立,但不太可能发生或被夸大
   - 不值得投入大量资源
   - 值得记录下来,以对齐干系人

   **Elephant(房间里的大象)**:你不确定是不是问题、但团队讨论得不够的事情
   - 没人说出口的顾虑或没人验证的假设
   - 可能是真的;你不确定
   - 值得在发布前调查清楚

4. **按紧迫程度给 Tiger 分级**:

   **发布阻断(Launch-Blocking)**:必须在发布前解决
   - 示例:核心功能损坏、监管障碍、关键客户依赖未满足

   **快速跟进(Fast-Follow)**:必须在发布后 30 天内解决
   - 示例:性能问题、次要功能不完整

   **持续观察(Track)**:发布后监控;成为问题时再解决
   - 示例:锦上添花的功能、边界情况

5. **制定行动计划**:对每个发布阻断级 Tiger:
   - 清晰描述风险
   - 提出具体的缓解行动
   - 确定最合适的负责人(职能/个人)
   - 设定决策/完成日期

6. **输出结构**:按以下形式呈现分析:

   ```
   ## Pre-Mortem Analysis: [Product Name]

   ### Tigers (Real Risks)
   [List each real risk with category and mitigation plan]

   ### Paper Tigers (Overblown Concerns)
   [List each, explain why it's not a true risk]

   ### Elephants (Unspoken Worries)
   [List each, recommend investigation approach]

   ### Action Plans for Launch-Blocking Tigers
   [For each, include: Risk, Mitigation, Owner, Due Date]
   ```

7. **保存输出**:保存为 markdown 文档:`PreMortem-[product-name]-[date].md`

## 备注

- 诚实且有建设性——目标是提升发布就绪度,而不是追责
- 拿不准时默认归为 "Tiger";尽早处理风险总是更好
- 在分析中纳入跨职能视角(工程、设计、市场)
- 发布前 2-3 周重做事前验尸,核实缓解措施是否到位

---

### 延伸阅读

- [How Meta and Instagram Use Pre-Mortems to Avoid Post-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
