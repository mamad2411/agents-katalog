---
name: agent-workflow-kit-zh-cn
description: 评估是否以及如何为新项目或已有代码库接入 AI 辅助开发工作流。用于用户要求接入 AI agent、创建或更新 AGENTS.md、选择工作流级别、判断是否使用 OpenSpec 或 Spec Kit 等规格层、判断是否使用 Superpowers 等执行纪律、判断是否添加 gstack 等专家审查、判断是否添加 ECC 等工具底座，或需要为维护者输出 Agent 工作流套件决策时。
---

# Agent 工作流套件

先评估仓库，再推荐能降低真实项目风险的最小 AI 工作流。除非维护者已经批准，不要安装工具、启用 hooks、添加 MCP server，或修改项目规则文件。

## 核心规则

按这个顺序执行：

```text
检查仓库 -> 风险评分 -> 选择工作流级别 -> 推荐文件/规则 -> 请求批准 -> 批准后再编辑
```

不要默认假设项目必须使用 OpenSpec、Spec Kit、Superpowers、gstack、ECC 或任何其他工具。它们只是示例，不是默认要求。

## 先检查项目

在提出接入建议前，先检查可用的项目上下文：

- `README.md`
- 现有 AI 规则：`AGENTS.md`、`CLAUDE.md`、`.cursor/rules`、`.github/copilot-instructions.md`
- 技术栈文件：`package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod`、`pom.xml` 等
- 源码结构：`src/`、`app/`、`pages/`、`components/`、`lib/`
- 测试和 E2E 配置：`tests/`、`spec/`、`e2e/`、Playwright/Cypress 配置
- CI/部署配置：`.github/workflows/`、`.gitlab-ci.yml`、`vercel.json`、`Dockerfile`、基础设施文件
- 风险面：auth、权限、token、cookie、支付、用户数据、抓取、发布、浏览器自动化、生产数据

如果没有仓库上下文，先向用户索要项目资料，或只输出通用评估清单。

## 风险评分

每个维度打 0-2 分：

| 维度 | 0 | 1 | 2 |
|---|---|---|---|
| 生命周期 | 一次性 | 偶尔维护 | 长期产品 |
| 用户 | 仅作者 | 内部用户 | 公开用户/客户 |
| UI/体验 | 无 | 简单 UI | 复杂 UI/编辑器/仪表盘 |
| 发布风险 | 不发布 | 手动发布 | staging/production/CI 发布 |
| 安全/账号 | 无 | API key/有限权限 | auth/cookie/token/用户数据/支付 |
| 外部平台 | 无 | 第三方 API | 抓取/发布/浏览器自动化 |
| 测试难度 | 单测足够 | 需要集成测试 | E2E/截图/可访问性/性能 |
| 协作 | 单人短期 | 单人长期 | 团队或多 agent |

工作流级别：

- `0-4`：Level 1 最小工作流；如果 AI 不改代码，可以 Level 0。
- `5-9`：Level 2 标准工作流。
- `10+`：Level 3 完整工作流。

覆盖规则：

- 安全/账号或外部平台为 `2`：加入安全/外部操作规则。
- UI/体验或测试难度为 `2`：加入浏览器/E2E 验证规则。
- 协作为 `2`：加入明确的项目级 AI 规则。

## 选择层级

只选择风险真正需要的层。

| 层级 | 何时加入 | 示例 |
|---|---|---|
| 规格层 | 非平凡行为/架构/数据/自动化变更需要长期记忆 | OpenSpec、Spec Kit、ADR/RFC、GitHub issues、`docs/changes/` |
| 执行纪律层 | AI 会写或改代码 | Superpowers、自定义 AGENTS 规则、团队 checklist |
| 专家审查层 | 存在产品/设计/QA/安全/发布风险 | gstack、人类 review checklist、QA/安全门 |
| 工具底座层 | 团队需要跨 agent 的 rules/hooks/MCP/记忆/语言规则 | ECC、自定义 rules/hooks |

规格层选择：

- 一般已有项目和小团队：优先 OpenSpec 或轻量 `docs/changes/`。
- 正式团队/企业级 SDD：优先 Spec Kit，尤其是需要 constitution/spec/plan/tasks 阶段时。
- 架构决策：优先 ADR/RFC/design docs。
- 小型开源项目：优先 GitHub issues/project docs。
- 不要同时使用两套规格工具作为事实来源。

## 先输出决策

除非用户已授权直接修改，否则先输出以下决策并请求批准：

```markdown
## Agent Workflow Kit Decision

Project: <project-name>

### Summary

- Project type: <library / CLI / web app / automation / data pipeline / editor / internal tool / etc.>
- Lifecycle: <one-off / maintained / long-lived>
- Users: <author / internal / public / customers>
- Risk level: <low / medium / high>
- Score: <0-16>

### Decision

- Workflow level: <0 / 1 / 2 / 3>
- Spec layer: <none / light / required>
- Agent discipline: <none / recommended / required>
- Specialist review: <none / light / full>
- Harness/tooling pack: <none / optional / recommended>

### Reasoning

- <reason 1>
- <reason 2>
- <reason 3>

### Proposed Files

- <file to create/update, or "none">

### Verification Commands Found

- Install: `<command or unknown>`
- Test: `<command or unknown>`
- Lint/typecheck: `<command or unknown>`
- Build: `<command or unknown>`
- E2E/browser: `<command or unknown>`
```

## 批准后编辑

创建或更新最小可用的项目规则。

推荐映射：

- Level 1：只用基础 `AGENTS.md` 块。
- Level 2：基础块 + 规格层块 + 执行纪律块 + 外部操作安全块。
- Level 3：Level 2 + 专家审查块；只有团队实际使用工具底座时才加入工具底座块。

使用 `references/agents-templates.zh-CN.md` 获取可复制模板。模板默认使用英文，通常更利于 agent 稳定执行；如果团队明确要求中文，可以翻译。

编辑已有规则时：

- 保留现有项目指令。
- 补充缺失规则，不要整文件覆盖。
- 保持规则足够短，让 agent 能真正遵守。
- 能发现验证命令时，填入真实命令。
- 只有无法判断命令时才保留 `<fill in>`，并在最终回复中说明。

## 安全规则

- 除非用户明确授权，外部/网络操作都需要批准。
- push、开/合 PR、部署、修改生产数据、发布内容、发送消息、改凭据、运行付费任务、操作真实第三方账号前必须询问。
- 不要把私有代码、客户数据、密钥、生产日志、数据库导出或凭据发送给不可信 agent、MCP server、浏览器自动化或外部服务。
- 高风险流程先输出本地计划或报告。

## 可选参考

仅在需要时加载：

- `references/agents-templates.zh-CN.md`：可复制的 `AGENTS.md` 模板块和完整标准示例。
- `references/engineering-references.zh-CN.md`：可选工程规约目录和使用时机。

