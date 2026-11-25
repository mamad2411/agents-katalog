---
name: prioritization-frameworks
description: "9 种优先级框架的参考指南,包含公式、适用场景指引和模板——RICE、ICE、Kano、MoSCoW、Opportunity Score 等。适用于选择优先级方法、比较 RICE 与 ICE 等框架,或了解不同优先级方法的原理。"
---

## 优先级框架参考

一份帮助你针对具体场景选择并应用合适优先级框架的参考指南。

### 核心原则

永远不要让客户来设计解决方案。给**问题(机会)**排优先级,而不是给功能排优先级。

### Opportunity Score(Dan Olsen,《The Lean Product Playbook》)

推荐的客户问题优先级框架。

就每项需求向客户调研**重要性(Importance)**和**满意度(Satisfaction)**(归一化到 0–1 区间)。

三个相关公式:
- **当前价值** = Importance × Satisfaction
- **Opportunity Score** = Importance × (1 − Satisfaction)
- **创造的客户价值** = Importance × (S2 − S1),其中 S1 = 之前的满意度,S2 = 之后的满意度

高重要性 + 低满意度 = 最高的 Opportunity Score = 最好的机会。画在"重要性 vs 满意度"图上——左上象限是甜区。它排的是客户问题的优先级,而不是解决方案的优先级。

### ICE 框架

适用于给各类举措和想法排优先级。不仅考虑价值,还考虑风险和经济因素。

- **I**(Impact)= Opportunity Score × 受影响客户数
- **C**(Confidence)= 我们有多大把握?(1-10)。体现风险。
- **E**(Ease)= 实现起来有多容易?(1-10)。体现经济因素。

**得分** = I × C × E。得分越高,越优先。

### RICE 框架

把 ICE 中的 Impact 拆成两个独立因子。适合需要更细粒度的大团队。

- **R**(Reach)= 受影响的客户数
- **I**(Impact)= Opportunity Score(每个客户的价值)
- **C**(Confidence)= 我们有多大把握?(0-100%)
- **E**(Effort)= 实现需要多少投入?(人月)

**得分** = (R × I × C) / E

### 9 种框架概览

| 框架 | 最适合 | 关键洞察 |
|-----------|----------|-------------|
| Eisenhower 矩阵 | 个人任务 | 紧急 vs 重要——用于 PM 个人的任务管理 |
| Impact vs Effort | 任务/举措 | 简单的 2×2——快速分诊,不适合严谨的战略决策 |
| Risk vs Reward | 举措 | 类似 Impact vs Effort,但考虑了不确定性 |
| **Opportunity Score** | 客户问题 | **推荐。** Importance × (1 − Satisfaction)。归一化到 0–1。 |
| Kano 模型 | 理解用户预期 | 必备型、期望型、魅力型、无差异型、反向型。用于理解,而非排序。 |
| 加权决策矩阵 | 多因素决策 | 给评估维度赋权重,给每个选项打分。有助于争取干系人认同。 |
| **ICE** | 想法/举措 | Impact × Confidence × Ease。推荐用于快速排优先级。 |
| **RICE** | 规模化场景的想法 | (Reach × Impact × Confidence) / Effort。在 ICE 基础上加入 Reach。 |
| MoSCoW | 需求 | Must/Should/Could/Won't。注意:源自项目管理领域。 |

### 模板

- [Opportunity Score intro (PDF)](https://drive.google.com/file/d/1ENbYPmk1i1AKO7UnfyTuULL5GucTVufW/view)
- [Importance vs Satisfaction Template — Dan Olsen (Google Slides)](https://docs.google.com/presentation/d/1jg-LuF_3QHsf6f1nE1f98i4C0aulnRNMOO1jftgti8M/edit#slide=id.g796641d975_0_3)
- [ICE Template (Google Sheets)](https://docs.google.com/spreadsheets/d/1LUfnsPolhZgm7X2oij-7EUe0CJT-Dwr-/edit?usp=share_link&ouid=111307342557889008106&rtpof=true&sd=true)
- [RICE Template (Google Sheets)](https://docs.google.com/spreadsheets/d/1S-6QpyOz5MCrV7B67LUWdZkAzn38Eahv/edit?usp=sharing&ouid=111307342557889008106&rtpof=true&sd=true)

---

### 延伸阅读

- [The Product Management Frameworks Compendium + Templates](https://www.productcompass.pm/p/the-product-frameworks-compendium)
- [Kano Model: How to Delight Your Customers Without Becoming a Feature Factory](https://www.productcompass.pm/p/kano-model-how-to-delight-your-customers)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm)(视频课程)
