---
name: coff0xc-detection-response
description: "Use when / 当用户请求 SOC、安全运营、detection engineering、threat hunting/intel、incident response/IR、forensics、malware、phishing：SIEM、Sigma、YARA、IOC、logs、alerts、EDR、timeline、alert tuning、误报和检测逻辑。手动触发：使用 coff0xc-detection-response。"
---

# coff0xc-detection-response

<!-- skill-id: cs-drs-6c1f90e4 -->

## 快速规则（日常任务先读这里）
> **[时间线先行]** 先定日志源、字段、时间范围、实体、告警上下文和已知 IOC。
> **[检测门禁]** Sigma/YARA/查询必须说明字段映射、样本、误报来源、ATT&CK 映射和测试方式。
> **[响应边界]** 默认给 triage、保全、遏制建议；真实隔离、封禁、删除、封号或生产处置先确认。
> **[交付标准]** 输出时间线、证据等级、规则、调优建议、缺失日志和复盘项。

普通检测/响应任务按本节先推进；只有事件指挥、真实 containment 或跨团队演练时再展开完整工作流。

## 能力定位
面向 SOC、检测工程、威胁狩猎、取证和应急响应的防御运营能力。它把日志、样本线索和告警问题转成可验证检测、时间线和响应建议。

## 能交付什么
- Sigma/YARA/查询规则草案和字段映射
- IOC、时间线、攻击阶段和 ATT&CK 映射
- 误报分析、测试样例和调优建议
- 应急处置、取证保全和复盘改进清单

## 可以接收什么输入
- EDR/SIEM/云日志、告警、IOC、样本摘要
- 取证笔记、邮件头、网络流量摘要、事件时间线
- 已有 Sigma/YARA/查询规则和误报反馈

## 放心使用的边界
- 只做防御检测、应急、取证和报告
- 不提供未授权攻击、持久化、规避检测或恶意样本投递步骤
- 处理真实日志时避免泄露个人信息和敏感资产细节
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 检测规则必须说明数据源、字段、测试样例和误报风险
- IR 输出区分已观测事实和推断
- 优先给可执行的处置和验证步骤

## 典型使用方式
```text
使用 coff0xc-detection-response 根据这些 EDR 日志写 Sigma 和 YARA 检测规则。
使用 coff0xc-detection-response 做一次威胁狩猎假设、日志查询和告警调优。
Use coff0xc-detection-response to build an incident timeline from these forensics notes.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
