---
name: opc-techstack
description: AI One-Person Company (OPC) technical toolkit for building AI agent teams, selecting tool stacks, and automating operations. Use when user needs to select AI tools, build AI agents, integrate MCP/A2A protocols, optimize AI API costs, or set up a no-code/low-code automation system. Triggers include "AI工具" "Agent搭建" "Dify" "Coze" "MCP" "自动化" "工具栈" "AI员工" "降本" "API成本" "n8n" "工作流".
---

# OPC TechStack: 工具 · Agent · 自动化

这个 skill 帮新手建立“够用、便宜、可升级”的 AI 工具栈。目标不是拥有最多工具，而是用最少工具跑通获客、交付、复盘。

## 快速诊断

| 用户状态 | 当前任务 | 推荐入口 | 合格产出 |
|----------|----------|----------|----------|
| 不知道买什么 | 按收入和阶段选最小工具栈 | [三层预算工具配置](references/tool-configuration.md) | 月预算和保留工具清单 |
| 想搭客服或内容Agent | 先选低门槛框架 | [Agent框架选型](references/agent-frameworks.md) | 一个客服/内容Agent原型 |
| API或订阅费太高 | 做成本审计和降级 | [成本优化六技](references/cost-optimization.md) | 成本追踪表和预算上限 |
| 重复工作太多 | 给任务做自动化评分 | [自动化工作流](references/automation-workflows.md) | 自动化优先级≥18的任务清单 |

## 新手工具栈原则

1. **收入未验证前，月工具预算不超过¥500**。
2. **每个工具必须服务一个业务动作**：获客、转化、交付、复盘或收款。
3. **先手工跑通流程，再自动化**：流程不稳定时，自动化只会放大混乱。
4. **每月做一次订阅审计**：使用少于5次或 ROI < 3 的工具取消。
5. **Agent 先做内部助手，再做对外自动回复**：降低幻觉和承诺风险。

## 三层配置

| 阶段 | 月收入 | 月预算 | 推荐配置 | 不建议 |
|------|--------|--------|----------|--------|
| 验证期 | <¥5000 | ¥0-500 | 免费模型、飞书/Notion、Canva、表格 | 自托管、复杂Agent、多平台付费 |
| 稳定期 | ¥5000-20000 | ¥500-2000 | Claude/ChatGPT、一个设计工具、一个自动化工具 | 同时买多套同类工具 |
| 增长期 | >¥20000 | ¥2000+ | 多模型API、Dify/n8n、监控、知识库 | 没有成本上限的API调用 |

## Agent 选型

| 创始人情况 | 先用 | 原因 |
|------------|------|------|
| 不会写代码，客户在微信/飞书 | Coze | 上手快，适合客服和内容助手 |
| 会一点技术，需要可控知识库 | Dify | 可视化工作流和 RAG 友好 |
| 需要连接多个SaaS | n8n | 自动化编排强 |
| 有工程能力，要深度定制 | LangGraph/LangChain | 灵活但维护成本高 |

MCP/A2A 属于进阶能力。新手只有在已经有稳定流程、明确工具调用需求、愿意维护配置时再引入。

## 成本控制底线

| 指标 | 健康值 |
|------|--------|
| AI工具和API成本占收入 | 15-25% |
| 单个客户AI成本/客户收入 | <30% |
| 缓存命中率 | >60% |
| 低价模型调用占比 | ≥70% |
| 僵尸订阅 | 每月清理 |

## 自动化优先级

优先自动化满足这些条件的任务：

- 每周重复至少3次。
- 输入输出稳定。
- 出错代价低。
- 能直接提升获客、转化、交付或复盘效率。
- 手工流程已经跑通至少2周。

不要优先自动化合同承诺、退款、投诉、复杂报价和高客单售前。

## 配套工具

| 工具 | 用途 | 位置 |
|------|------|------|
| AI成本追踪表 | 月度API支出监控 | [assets/toolkit-07-cost-tracker.md](assets/toolkit-07-cost-tracker.md) |
| Agent提示词模板 | 客服/内容/数据分析Agent | [assets/toolkit-08-agent-prompts.md](assets/toolkit-08-agent-prompts.md) |
| Dify Bot配置指南 | 进阶客服Bot搭建 | [assets/toolkit-12-dify-bot-config.md](assets/toolkit-12-dify-bot-config.md) |
| 全场景提示词库 | 进阶Prompt模板 | [assets/toolkit-11-prompt-library.md](assets/toolkit-11-prompt-library.md) |
