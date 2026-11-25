---
name: coff0xc-skill-router
description: "Coff0xc lightweight skill router/composer. Use only when the user asks AI to decide which coff0xc skills to use, chain skills, build a task/workflow graph, orchestrate vibe coding, handle cross-domain/multi-domain work, or recover an uncertain trigger. Also for broad plan work spanning dev API UI or security cloud identity detection compliance Office. 中文触发：自主编排、多 skill、AI 自己判断、跨领域、工作流图。窄任务不用 router。"
---

# coff0xc-skill-router

<!-- skill-id: cs-srt-b7a20c6d -->

## 快速规则（日常任务先读这里）
> **[单域直达]** 能用一个专业 skill 做完就直接用它，不输出长 skill graph。
> **[跨域编排]** 只有任务确实跨多个领域或用户要求 AI 自己串联 skill，才给主 skill、辅助 skill、阶段和门禁。
> **[轻量执行]** 复杂任务只给 3-5 行可执行工作流，然后马上进入第一阶段。
> **[复杂升级]** 多文件、多阶段、架构/API/schema/auth 或多 worker 任务才读取 `references/complex-workflow.md`。
> **[发版边界]** trigger eval、quality eval、workflow trace、golden responses 只在 review/eval/发版/CI/推送时使用。

普通任务按本节分流；只有路由调试、skill 质量验证或复杂跨域工作流才读取 references。

## 能力定位
面向不确定任务和跨领域任务的轻量 autonomous skill composer。它不是把所有能力揉成一个大 skill，也不是普通任务的必经步骤；它只在任务确实需要选择、分流或跨域编排时介入。

单一任务只选一个最具体 skill；复杂任务输出主 skill、辅助 skill、执行顺序、门禁和重路由条件。

## 能交付什么
- 轻量分流结果：当前主 skill、必要辅助 skill、暂不使用的 skill
- 分阶段执行顺序：每阶段调用哪个 skill、输入、输出、完成门禁
- 候选 skill 对比、取舍理由和适用边界
- 需要澄清的最少问题
- 执行中新增、移除或切换 skill 的条件
- 后续手动触发或自然语言触发句式

## 可以接收什么输入
- 模糊任务描述、多个领域混合需求、vibe coding 需求
- 用户说不确定用哪个 skill、自动触发失败
- 仓库、截图、日志、论文、配置等混合材料
- 用户要求 AI 自己判断、自己串联 skill、按工作流完成

## 放心使用的边界
- 负责规划和编排，不替代专业 skill 的深层执行规则
- 遇到安全、生产、凭据、删除、远程写入或付费动作时沿用目标 skill 的门禁
- 无法确定时给 2-3 个候选组合并问最小澄清问题
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 保持 skill 模块化，只在需要时加载对应专业流程
- 每个 skill 都必须有明确职责、输入、输出和退出门禁
- 执行中根据真实证据重路由，而不是死守初始判断
- 保留手动触发写法，用户仍可强制指定某个 skill

## 典型使用方式
```text
使用 coff0xc-skill-router 帮我判断这个任务该用哪个 skill。
使用 coff0xc-skill-router 这个需求同时涉及 API、UI 和安全，帮我分流。
你自己判断要用哪些 coff0xc skills，并把它们串成工作流完成这个功能。
这个 vibe coding 任务可能涉及前后端、数据库、安全和文档，你来编排 skill。
Use coff0xc-skill-router when a Coff0xc skill did not auto-trigger.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
