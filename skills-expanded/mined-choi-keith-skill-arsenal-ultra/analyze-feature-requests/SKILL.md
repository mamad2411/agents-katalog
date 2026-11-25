---
name: analyze-feature-requests
description: "按主题、战略契合度、影响、投入和风险分析客户功能请求并排定优先级。适用于评审客户功能请求、分诊 backlog 或做优先级决策时。"
---

## 分析功能请求

对照产品目标,对客户功能请求进行分类、评估和优先级排序。

### 背景

你正在分析 **$ARGUMENTS** 的功能请求。

如果用户提供了文件(包含功能请求的电子表格、CSV 或文档),直接阅读并分析。如果数据是结构化格式,可考虑创建汇总表。

### 领域背景

永远不要让客户来设计解决方案。优先处理**机会(问题)**,而不是功能。使用**机会分数(Opportunity Score)**(Dan Olsen)评估客户上报的问题:机会分数 = 重要性 ×(1 − 满意度),归一化到 0–1。完整细节和模板参见 `prioritization-frameworks` skill。

### 操作指引

用户会描述他们的产品目标并提供功能请求。按以下步骤进行:

1. **明确目标**:确认将用于指导优先级排序的产品目标和期望成果。

2. **将请求归类为主题**:把相关请求归组,并为每个主题命名。

3. **评估战略契合度**:评估每个主题与既定目标的匹配程度。

4. **基于以下维度选出前 3 个功能**:
   - **影响(Impact)**:客户价值和受影响的用户数量
   - **投入(Effort)**:所需的开发和设计资源
   - **风险(Risk)**:技术和市场不确定性
   - **战略契合度**:与产品愿景和目标的匹配程度

5. **对每个头部功能**,提供:
   - 理由(客户需求、战略契合度)
   - 值得考虑的替代方案
   - 高风险假设
   - 如何以最小投入验证这些假设

逐步思考。保存为 markdown 或创建结构化的输出文档。

---

### 延伸阅读

- [Kano Model: How to Delight Your Customers Without Becoming a Feature Factory](https://www.productcompass.pm/p/kano-model-how-to-delight-your-customers)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm)(视频课程)
