---
name: jinhoa-security-audit
description: 金和 OA（C6/相关版本）代码审计技能（中文）。用于 WebForms/ASMX 场景下的 SQL 注入、未授权访问、文件上传/下载、XXE、路径穿越、反序列化与鉴权绕过审计，输出结构化证据链、修复建议与复测步骤。触发场景：金和 OA 审计与漏洞复盘。
---

# CSharp Security Audit

## 审计目标

从“漏洞线索”走到“可交付结论”：

- 明确入口与可控参数
- 建立 source-sink 证据链
- 区分确认漏洞/可疑点/历史线索
- 输出最小改动修复与复测步骤

## 执行流程

1. 确认框架与入口（WebForms/MVC/Core/asmx）。
2. 建立接口资产清单（aspx/asmx/ashx/api 路由）。
3. 追踪外部输入到危险函数（source -> sink）。
4. 优先审计高危漏洞族（注入、上传、鉴权、XXE）。
5. 输出风险分级、修复建议与复测闭环。

## 高危优先检查

先读取 `references/dotnet-checklist.md`。

重点关注：

- SQL 注入：字符串拼接 SQL、`string.Format` 拼接查询、动态排序条件。
- 未授权访问：接口无会话/令牌校验、仅前端鉴权。
- 任意文件上传/下载：路径可控、扩展名校验弱、可执行目录落地。
- XXE：`XmlDocument/XmlTextReader/XDocument` 解析不可信 XML。
- 路径穿越：下载/读取接口参数可控且缺规范化校验。
- 反序列化：`BinaryFormatter/LosFormatter/NetDataContractSerializer` 不可信输入。

## 金和 OA 参考专项

先读取 `references/jinhoa-case-notes.md`。

将其作为“审计思路样例”：

- 先定位 asmx/aspx 入口与参数
- 再追踪到具体 SQL/文件/XML 处理点
- 最后判定是否可利用与影响范围

## AI 辅助审计流程

先读取 `references/ai-audit-workflow.md`。

执行时强制遵守：

- 初筛只给“候选点”，不直接判漏洞。
- 结论必须分级：`CONFIRMED` / `SUSPECTED` / `INFO`。
- 每个高危结论必须附完整证据链（source -> sink）。
- 对历史漏洞仅做“版本与补丁状态核查”，不直接下结论。

## 语义护栏（抗幻觉）

先读取 `references/semantic-guardrails.md`。

执行时额外强制：

- 统一使用窄语义词，避免“问题/风险/异常”等宽语义词扩边。
- 输出必须满足 8 字段结构，否则判定无效并重做。
- 若出现范围外结论，先做排除测试再继续。

## 输出要求

优先使用 `templates/csharp-audit-report.md`。

每条问题必须包含：

- 位置（文件/类/方法）
- 可控参数
- 漏洞链路（source -> sink）
- 利用前提
- 影响范围
- 修复建议（最小改动）
- 复测步骤

## 风险分级

- 高危：可直接导致 RCE、未授权敏感操作、批量数据泄露。
- 中危：需要条件但可造成明显安全影响。
- 低危：影响有限或利用复杂。
- 建议项：安全设计风险，尚未形成直接漏洞。

## 修复原则

- 参数化查询优先，禁止拼接 SQL。
- 服务端强制鉴权与资源归属检查。
- 上传下载统一走安全组件（白名单+路径规范化+隔离存储）。
- XML 解析关闭外部实体与危险特性。
- 历史接口（asmx/aspx）增加统一安全中间层或网关限制。

## 禁止行为

- 不输出未授权攻击脚本。
- 不把“延时现象”直接当漏洞最终结论。
- 不脱离版本和业务上下文做绝对判断。
