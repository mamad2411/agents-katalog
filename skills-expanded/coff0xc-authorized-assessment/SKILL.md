---
name: coff0xc-authorized-assessment
description: "Use only for authorized security assessment / 当用户请求已授权评估、ROE、attack surface、recon/fingerprint、red team/adversary emulation、防御化攻击链规划、control validation、CDN/WAF 边界、phishing/social-engineering simulation planning 或报告。高风险动作先确认范围。手动触发：使用 coff0xc-authorized-assessment。"
---

# coff0xc-authorized-assessment

<!-- skill-id: cs-aas-f36c09a2 -->

## 快速规则（日常任务先读这里）
> **[授权先行]** 先确认资产范围、ROE、测试窗口、禁止动作和证据留存；没有授权只做防御化规划。
> **[防御转译]** 把攻击链语言转成控制验证、检测覆盖、风险复盘和修复优先级。
> **[执行门禁]** 主动扫描、社工演练、绕过验证、真实外传、生产动作和第三方目标必须先确认。
> **[交付标准]** 输出范围、阶段、观测点、停止条件、证据等级和报告结构。

普通授权评估任务按本节先推进；只有书面 ROE、演练执行或跨安全域编排时再展开完整工作流。

## 能力定位
面向授权安全评估和红队到防御映射的规划能力。它把评估范围、ROE、攻击面、控制验证和报告结构组织成可批准、可执行、可复盘的方案。

## 能交付什么
- 授权范围和 ROE 草案
- 攻击面清单、测试阶段和禁止动作
- 控制验证矩阵、检测覆盖和演练观测点
- 报告结构、风险登记和复盘改进计划

## 可以接收什么输入
- 授权说明、资产范围、测试窗口、禁止动作
- 攻击面线索、架构图、防护控制、日志能力
- 演练目标、合规要求、报告模板

## 放心使用的边界
- 没有明确授权时只输出准备清单和防御建议
- 不提供绕过、持久化、凭据窃取、外传或破坏性步骤
- 任何主动测试、社工演练、外部基础设施或远程动作必须先确认
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 先定义边界和停止条件，再设计验证
- 把红队行为转成可观测防御目标
- 报告以证据、影响、修复和检测改进为中心

## 典型使用方式
```text
使用 coff0xc-authorized-assessment 在书面授权范围内规划一次安全评估。
使用 coff0xc-authorized-assessment 把红队演练步骤转成防御验证和报告结构。
Use coff0xc-authorized-assessment to draft ROE and control validation for an internal assessment.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
