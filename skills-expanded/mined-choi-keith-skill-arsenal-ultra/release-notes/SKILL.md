---
name: release-notes
description: "根据工单、PRD 或变更日志生成面向用户的发布说明。产出按类别(新功能、改进、修复)组织的清晰、有吸引力的摘要。适用于撰写发布说明、创建变更日志、发布产品更新公告,或总结本期交付内容。"
---

## 发布说明生成器

把技术性工单、PRD 或内部变更日志转化为打磨过的、面向用户的发布说明。

### 背景

你正在为 **$ARGUMENTS** 撰写发布说明。

如果用户提供了文件(JIRA 导出、Linear 工单、PRD、Git 日志或内部变更日志),先阅读它们。如果他们提到产品 URL,用联网搜索了解产品和受众。

### 指令

1. **收集原始素材**:阅读所有提供的工单、变更日志或描述。提取:
   - 改变了什么(新功能、改进还是修复)
   - 影响谁(哪个用户群体)
   - 为什么重要(用户收益)

2. **对变更分类**:
   - **新功能**:全新的能力
   - **改进**:对现有功能的增强
   - **Bug 修复**:已解决的问题
   - **破坏性变更**:任何需要用户采取行动的变更(迁移、API 变更)
   - **弃用**:即将下线的功能

3. **按以下原则撰写每一条目**:
   - 以用户收益开头,而不是技术变更
   - 使用平实语言——避免行话、内部代号或工单编号
   - 每条目控制在 1-3 句
   - 如果用户提供了配图或截图,一并使用

   **改写示例**:
   - 技术表述:"Implemented Redis caching layer for dashboard API endpoints"
   - 面向用户:"仪表盘加载速度最高提升 3 倍,让你少等待、多分析。"

   - 技术表述:"Fixed race condition in concurrent checkout flow"
   - 面向用户:"修复了高流量时段部分订单可能失败的问题。"

4. **组织发布说明的结构**:

   ```
   # [Product Name] — [Version / Date]

   ## New Features
   - **[Feature name]**: [1-2 sentence description of what it does and why it matters]

   ## Improvements
   - **[Area]**: [What got better and how it helps]

   ## Bug Fixes
   - Fixed [issue description in user terms]

   ## Breaking Changes (if any)
   - **Action required**: [What users need to do]
   ```

5. **调整语气**以匹配产品的调性——B2B 产品用专业语气,消费级产品用亲切语气,API 产品面向开发者。

保存为 markdown 文档。如果用户想要 HTML 或其他格式,相应转换。
