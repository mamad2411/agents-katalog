---
name: java-security-audit
description: Java 代码安全审计技能（中文）。用于 Java/Spring/MyBatis/Shiro 等项目的漏洞审计、证据链确认与修复建议输出，覆盖 SQL 注入、命令执行、反序列化、XXE、SSRF、越权、上传下载与业务逻辑缺陷。触发场景：审计 Java 项目、定位漏洞、输出整改与复测计划。
---

# Java Security Audit

## 审计目标

输出可落地结果，而不是“命中关键词列表”。每个结论都要有证据链：

- 外部输入点
- 污点传播路径
- 危险调用点（sink）
- 安全控制是否缺失或可绕过
- 可利用条件与影响范围

## 标准流程（严格按顺序）

1. 识别项目边界与技术栈（框架、中间件、构建工具、鉴权方案）。
2. 建立攻击面清单（HTTP、RPC、MQ、定时任务、文件导入导出）。
3. 建立“源-汇”映射（source -> sanitizer -> sink）。
4. 先做高危链路审计（RCE/注入/越权/反序列化/上传）。
5. 再做中低危与业务逻辑审计（信息泄露、弱校验、风控绕过）。
6. 给出漏洞确认、风险分级、修复方案与复测要点。

## 输入点与汇点

优先读取：`references/source-sink-matrix.md`

审计时必须回答：

- 输入是否可信？（请求参数、Header、Cookie、文件、消息体）
- 是否有白名单校验？（格式/长度/范围/语义）
- 是否有编码/参数化/策略化控制？
- 危险调用是否被包裹并受控？

## 框架专项检查

优先读取：`references/framework-checklist.md`

按框架做差异化审计：

- Spring MVC / Boot：`@RequestBody` 绑定对象、SpEL、Actuator 暴露、`RestTemplate/WebClient` 出网。
- MyBatis / JPA：动态 SQL 拼接、`ORDER BY`/`LIMIT` 参数拼接、原生 SQL。
- Shiro / Spring Security：URL 鉴权规则、方法鉴权、权限注解缺失、鉴权前置顺序。
- Jackson / Fastjson：AutoType、多态反序列化、黑白名单配置。
- 模板引擎（Thymeleaf/Freemarker/Velocity）：模板表达式注入与沙箱绕过。

## 漏洞判定规则

优先读取：`references/vuln-verification-standard.md`

- 若链路可达但条件不充分：标记“可疑点（需验证）”。
- 若可构造稳定触发：标记“已确认漏洞”。
- 若仅理论存在且落地受限：标记“风险设计缺陷”。

## 风险分级（默认）

- 高危：可直接导致 RCE、未授权数据泄露、批量越权、核心资产泄露。
- 中危：需要较多前置条件但可造成敏感影响。
- 低危：影响有限或需复杂链路。
- 建议项：尚未形成漏洞，但存在明显攻击面。

## 输出要求

优先使用：`templates/report-template.md`

每条问题必须包含：

- 位置（文件/类/方法）
- 漏洞类型与成因
- 触发路径（source -> sink）
- 利用前提
- 影响范围
- 修复建议（最小改动优先）
- 复测步骤

## 语义护栏（抗幻觉）

先读取 `references/semantic-guardrails.md`。

执行时强制：

- 结论使用 `CONFIRMED` / `SUSPECTED` / `INFO`。
- 每条高危结论必须附完整证据链（source -> sink）。
- 输出必须满足 8 字段结构，缺字段重做。
- 避免宽语义词扩边，超范围内容不纳入漏洞结论。

## 快速模式（时间紧）

1. 读取 `references/quick-grep-rules.md` 做初筛。
2. 读取 `references/source-sink-matrix.md` 对命中点分组。
3. 仅输出 Top 10 风险（按可利用性排序）。
4. 明确“立即修复”与“后续优化”两类任务。

## 修复建议原则

- 优先最小改动，先止血再优化。
- 参数化优先于转义；白名单优先于黑名单。
- 鉴权与租户隔离在服务端强制执行。
- 上传下载必须做路径规范化与存储隔离。
- 对外请求必须限制协议、域名、IP 段与重定向。

## 禁止行为

- 不输出攻击脚本用于未授权目标。
- 不将“关键词命中”直接当作漏洞结论。
- 不忽略业务上下文就给高危定级。
