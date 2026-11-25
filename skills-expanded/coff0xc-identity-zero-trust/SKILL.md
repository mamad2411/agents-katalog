---
name: coff0xc-identity-zero-trust
description: "Use when / 当用户请求 identity、IAM、zero trust、AD/Active Directory、Kerberos、SSO/MFA、BloodHound、PAM、service accounts、权限/凭证风险、identity paths、lateral movement defense、access governance 或特权账号收敛。手动触发：使用 coff0xc-identity-zero-trust。"
---

# coff0xc-identity-zero-trust

<!-- skill-id: cs-izt-5b0a7d2e -->

## 快速规则（日常任务先读这里）
> **[身份图先行]** 先明确主体、组、角色、策略、会话、设备、服务账号和信任路径。
> **[证据门禁]** 结论绑定配置、日志、策略、BloodHound/图路径或代码调用点。
> **[修复优先]** 给最小权限、MFA/session、分段访问、审计和回滚建议。
> **[硬边界]** IAM/AD 写入、账号禁用、密钥轮换、生产权限调整和横向验证先确认。

普通身份/零信任评估按本节先推进；只有真实目录变更、演练或跨环境治理时再展开完整工作流。

## 能力定位
面向身份、访问控制、AD/Kerberos、IAM 和零信任治理的权限风险评估能力。它帮助回答“谁能访问什么、为什么、风险在哪里、如何收敛”。

## 能交付什么
- 身份/权限风险清单和路径说明
- MFA/SSO/session/device posture 评估
- AD/Kerberos/IAM 横向移动和特权账号防御建议
- 最小权限、PAM、条件访问和审计验证计划

## 可以接收什么输入
- IAM policy、AD/BloodHound 输出、SSO/MFA 配置
- 账号/角色/组/权限矩阵、登录日志、访问异常
- Zero Trust 策略、设备姿态、session policy

## 放心使用的边界
- 默认做授权环境的只读分析和防御建议
- 凭证获取、hash dump、未授权横向移动或提权步骤不提供
- 生产身份策略修改、账号禁用、密钥轮换必须先确认
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 把身份、设备、会话、资源和审计链路一起看
- 区分配置弱点和实际可达路径
- 输出收敛顺序和验证方法

## 典型使用方式
```text
使用 coff0xc-identity-zero-trust 评估这个 AD 域的 Kerberos、BloodHound 路径和服务账号风险。
使用 coff0xc-identity-zero-trust 梳理谁能访问什么，并给最小权限收敛方案。
Use coff0xc-identity-zero-trust to review IAM, SSO, MFA, and privileged account exposure.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
