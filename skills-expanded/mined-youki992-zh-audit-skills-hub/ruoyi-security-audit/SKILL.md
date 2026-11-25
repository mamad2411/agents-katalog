---
name: ruoyi-security-audit
description: 若依（RuoYi）框架代码审计技能（中文）。用于 RuoYi-Vue / RuoYi-Cloud 项目的漏洞排查、证据链确认与修复建议输出，覆盖 SQL 注入、未授权访问、越权、文件上传、代码执行链、鉴权绕过、定时任务滥用与配置泄露等常见风险。触发场景：若依漏洞审计、Nday 复盘、整改复测报告输出。
---

# RuoYi Security Audit

## 审计目标

以“业务代码 + 框架配置”双线审计为核心，输出可复测的结论，而不是漏洞关键词罗列。

## 标准流程

1. 识别项目形态（RuoYi-Vue / RuoYi-Cloud）与版本。
2. 梳理攻击面（登录、权限、代码生成、文件、定时任务、系统配置）。
3. 追踪 source -> sink 证据链，确认可控参数与防护状态。
4. 分级输出 `CONFIRMED / SUSPECTED / INFO`。
5. 给出最小改动修复与复测步骤。

## 高危优先检查

先读取 `references/ruoyi-checklist.md`。

重点审计：

- SQL 注入：动态查询条件、排序字段、拼接 SQL。
- 权限问题：菜单权限、接口鉴权、数据权限与对象级授权。
- 未授权访问：后台管理接口、配置接口、历史兼容接口。
- 文件能力：上传落地路径、文件下载路径、文件类型校验。
- 定时任务：任务配置可控、执行类/表达式滥用。
- 配置泄露：默认口令、敏感配置、错误堆栈暴露。

## Nday 复盘模式

先读取 `references/ruoyi-nday-review.md`。
再读取 `references/ruoyi-nday-patterns.md`。

- 将历史漏洞拆为“根因模板”（鉴权缺失、参数拼接、路径控制等）。
- 在当前代码中寻找同根因变体，而不是只复现旧 PoC。
- 对弱口令、Druid、Swagger、Shiro、敏感接口族做专项核查。
- 结论必须包含版本与补丁状态说明。

## 语义护栏（抗幻觉）

先读取 `references/semantic-guardrails.md`。

执行时强制：

- 每条结论必须附 `source -> sink` 证据链。
- 只评估本 skill 范围内漏洞族，范围外内容归 `INFO`。
- 输出字段不完整则重做。

## 输出要求

优先使用 `templates/ruoyi-audit-report.md`。

每条问题必须包含：

- 位置（文件/类/方法）
- 参数（可控输入）
- 漏洞类型
- 证据链（source -> sink）
- 防护状态（缺失/可绕过/有效）
- 结论分级（CONFIRMED/SUSPECTED/INFO）
- 修复建议
- 复测步骤

## 禁止行为

- 不输出未授权攻击脚本。
- 不以历史文章结论直接替代当前版本结论。
- 不把“可疑现象”直接判定为确认漏洞。
