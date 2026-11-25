---
name: prioritize-assumptions
description: "使用"影响 × 风险"矩阵为假设排定优先级,并为每个假设建议实验。适用于分诊一批假设、决定先测试什么或应用假设优先级画布(assumption prioritization canvas)时。"
---

## 为假设排定优先级

使用"影响 × 风险"矩阵分诊假设,并建议有针对性的实验。

### 背景

你正在帮助为 **$ARGUMENTS** 的假设排定优先级。

如果用户提供了包含假设或研究数据的文件,先阅读它们。

### 领域背景

**ICE** 很适合用于假设优先级排序:Impact(机会分数 × 客户数)× Confidence(置信度,1–10)× Ease(容易度,1–10)。机会分数(Opportunity Score)= 重要性 ×(1 − 满意度),归一化到 0–1(Dan Olsen)。**RICE** 将 Impact 拆分为独立的 Reach × Impact:(R × I × C)/ E。完整公式和模板参见 `prioritization-frameworks` skill。

### 操作指引

用户会提供一组待排序的假设。应用以下框架:

1. **对每个假设**,评估两个维度:
   - **影响(Impact)**:验证该假设所创造的价值,乘以受影响的客户数量(在 ICE 中:Impact = 机会分数 × 客户数)
   - **风险(Risk)**:定义为(1 − 置信度)× 投入

2. **用"影响 × 风险"矩阵对每个假设分类**:
   - **低影响、低风险** → 推迟测试,先处理更高优先级的假设
   - **高影响、低风险** → 直接投入开发(低风险、高回报)
   - **低影响、高风险** → 否决该想法(不值得投入)
   - **高影响、高风险** → 设计实验来测试它

3. **对每个需要测试的假设**,建议一个满足以下条件的实验:
   - 以最小投入换取最大的验证性学习
   - 衡量真实行为,而非观点
   - 有明确的成功指标和阈值

4. **以优先级矩阵或表格呈现结果**。

逐步思考。内容较多时保存为 markdown。

---

### 延伸阅读

- [Assumption Prioritization Canvas: How to Identify And Test The Right Assumptions](https://www.productcompass.pm/p/assumption-prioritization-canvas)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm)(视频课程)
