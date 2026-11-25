---
name: coff0xc-secure-code-appsec
description: "Use when / 当用户请求 code/AppSec audit：source/sink、taint、Web/API/GraphQL/OAuth、CSP/CORS/Cookie、LLM prompt injection、access control/authorization bypass、SSRF/XSS/SQLi、backdoor/Webshell、security regression。仅限授权范围。手动触发：使用 coff0xc-secure-code-appsec。"
---

# coff0xc-secure-code-appsec

<!-- skill-id: cs-sca-3d9e7a54 -->

## 快速规则（日常任务先读这里）
> **[入口优先]** 先找入口、鉴权/授权边界、source/sink、信任边界和危险函数。
> **[证据门禁]** 每个发现必须有文件/行号、调用链、影响、触发条件和修复建议。
> **[修复闭环]** 优先最小补丁和回归测试；不把未复现猜测写成确认漏洞。
> **[硬边界]** 未授权目标、真实攻击链、凭据滥用、持久化、数据外传和生产验证先确认。

普通代码安全审计按本节先推进；只有大范围 variant analysis、补丁验证或上线安全门禁时再展开完整工作流。

## 能力定位
面向代码和应用安全的证据化审计能力。它把源码、路由、配置、扫描结果和日志转成可验证发现、修复建议和回归检查。

## 能交付什么
- 安全发现列表：位置、影响、证据、复现条件
- source/sink 或权限链路说明
- 修复建议、测试用例、检测/日志建议
- 误报判断和剩余风险

## 可以接收什么输入
- 源码仓库、routes/controllers/resolvers、auth middleware
- Burp 项目、SARIF、扫描结果、日志、配置
- 漏洞线索、越权现象、Prompt 注入或后门疑点

## 放心使用的边界
- 只处理自有或明确授权资产、本地代码和防御建设
- 不提供未授权利用、凭据获取、持久化、规避检测或外传步骤
- 主动扫描、认证绕过测试和外部回连必须先确认授权范围
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 每个发现必须有代码/配置/日志证据
- 区分已验证、高可信、推断和未知
- 安全输出默认包含修复、检测和验证闭环

## 典型使用方式
```text
使用 coff0xc-secure-code-appsec 审计这个 Web/API 项目的认证和越权风险。
使用 coff0xc-secure-code-appsec 看 source/sink、SSRF、XSS、SQLi 和后门迹象。
Use coff0xc-secure-code-appsec to triage this SARIF report and remove false positives.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
