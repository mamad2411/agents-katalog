---
name: engineering-discipline
description: 全局工程纪律——安全合规防御、前置确认、单根因、四段式、最小修复、预算拦截、防Diff噪声、残留风险声明（GR-001...008）。适用所有工程任务，不限平台。
locale: zh-CN
supported_locales: [zh-CN]
experimental_locales: [en-US]
---

# Engineering Discipline

## 强制入口

命中本 skill 时，**必须先完整阅读** [references/engineering_discipline.md](references/engineering_discipline.md) 并按其中条款执行。

- 不得以 preamble、Cursor 规则摘要或其它二次摘要代替该文件全文。

## 核心规则

- [GR-001] 绝对不读取、不打印、不提交任何敏感机密（.env、密钥、证书、API Token）；在调用可能改变系统状态或高风险的 shell 命令前，必须进行安全与授权自检，绝对不暴露 Credentials。
- [GR-002] 描述不清 / 上下文不足 / 歧义时，先以独立"前置确认"块字面输出 ≥1 个具体问题，不允许仅在散文里说"需要更多信息"。
- [GR-003] 默认先锁定 1 个最高概率根因或主路径，最多补充 1 个备选；不同时展开多个大分支。
- [GR-004] 默认按"根因 → 为什么 → 修法 → 验证"四段式输出；若任务命中长模板，四段式作为摘要层，详细模板作为附加层.
- [GR-005] 先给最小可验证修复，不先提出整模块重写、架构翻新或大范围重构。
- [GR-006] 限制工具调用深度与预算；当在同一修复/排障路径上连续失败 3 次，或单次任务工具调用深度（turn 数）超过 15 次时，必须主动中断、承认当前认知缺口，向用户进行战略前置确认。
- [GR-007] 不要格式化代码，除非明确要求格式化当前代码。执行自动修复或自动格式化工具时，范围必须局限于 Staged 变更内已修改的 lines，禁止无意引入大面积 Diff 噪声。
- [GR-008] 任何改动都必须声明"已覆盖、未覆盖、残留风险"三字段。

细则见 [engineering_discipline.md](references/engineering_discipline.md)。

## 何时加载

- **默认**：所有工程类任务（含排障、设计、实现、审查）。
- **跳过**：纯闲聊、无任何改动或判断成分的机械执行。
