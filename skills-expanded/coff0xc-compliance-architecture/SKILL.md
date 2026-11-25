---
name: coff0xc-compliance-architecture
description: "Use when / 当用户请求 security architecture、threat modeling、compliance、data security/privacy/DLP、baseline：STRIDE、等保、PCI-DSS、GDPR、ISO27001、SOC2、CIS/NIST、control evidence、risk register、audit log、executive/compliance report、release evidence。手动触发：使用 coff0xc-compliance-architecture。"
---

# coff0xc-compliance-architecture

<!-- skill-id: cs-car-a64d8e31 -->

## 快速规则（日常任务先读这里）
> **[范围先行]** 先定系统边界、数据分类、信任边界、合规框架、控制目标和证据来源。
> **[架构门禁]** 风险要映射到资产、威胁、控制、负责人、验证证据和残余风险。
> **[输出可审计]** 交付威胁模型、控制矩阵、差距、优先级、例外和整改路线。
> **[硬边界]** 法律意见、客户承诺、正式认证声明、生产策略变更和公开发布先确认。

普通安全架构/合规评审按本节先推进；只有正式审计、客户交付或企业控制治理时再展开完整工作流。

## 能力定位
面向安全架构、威胁建模、合规映射、数据安全和成熟度评估的治理能力。它把系统设计、控制要求和审计证据整理成能落地的风险决策材料。

## 能交付什么
- 架构风险评审和信任边界图
- STRIDE/威胁建模、控制矩阵和差距分析
- 数据分类、隐私、DLP 和日志审计建议
- 合规证据清单、整改路线和上线门禁

## 可以接收什么输入
- 架构图、数据流、系统说明、上线方案
- 合规要求、控制项、审计证据、政策文档
- 数据分类、权限模型、日志和风险登记

## 放心使用的边界
- 可做设计评审、差距分析和证据整理
- 不替代法律意见、正式审计签字或监管结论
- 生产策略变更、权限收敛和数据处理动作必须先确认
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 把控制项映射到具体系统证据
- 区分必须修、可接受风险和后续改进
- 输出能被工程、审计和管理层共同理解

## 典型使用方式
```text
使用 coff0xc-compliance-architecture 做上线前安全架构评审和威胁建模。
使用 coff0xc-compliance-architecture 把这些控制项映射成审计证据清单。
Use coff0xc-compliance-architecture to build a risk model and remediation roadmap.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
