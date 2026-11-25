# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 04-ai/agent-payment-x402/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当 Agent 需要为 402 计费的 API/服务/A2A 付费而又不能托管私钥时使用；做法是接入 x402 协议+MCP 支付服务器，由编排层预设 SpendingPolicy（按任务/会话预算、收款白名单、限速）并 fail-closed 强制，产出受限额约束的非托管支付链路；不适用于自建链上结算合约、法币/信用卡收银台或无预算门控的随意转账。触发词：x402、Agent 支付、支出限额、a
