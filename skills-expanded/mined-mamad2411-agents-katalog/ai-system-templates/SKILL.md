---
name: ai-system-templates
description: Use when a user is designing AI-native systems such as AI chat products, AI gateways, RAG knowledge bases, agent or workflow platforms, inference serving, or vector databases and wants architecture choices and trade-offs grounded in the awesome-architecture templates.
---

# AI System Templates

Use the `awesome-architecture` AI-native templates as architecture maps for LLM-era systems. These templates focus on system shape, bottlenecks, guardrails, and trade-offs rather than framework selection.

## Source Of Truth

- Local source repo: `~/.hermes/external-repos/awesome-architecture`
- Template map: `references/template-map.md`

## When To Use

- `AI 架构`, `AI 聊天架构`, `AI 网关`
- `RAG 架构`, `向量数据库架构`
- `AI Agent 平台架构`, `AI 工作流架构`
- `模型推理服务架构`, `inference serving`

For classic product architectures, route to `comm/arch/general-system-templates`. For method and trade-off framing, route to `comm/arch/architecture-thinking`.

## Workflow

1. Map the request to one or two AI-native templates from `references/template-map.md`.
2. Read the matching upstream template files before answering.
3. Structure the answer as:
   - problem shape
   - core runtime components
   - retrieval / memory / serving path
   - cost, latency, and reliability pressure points
   - guardrails and control points
   - evolution path
4. If the system combines agentic behavior with retrieval or gateway concerns, explicitly separate control plane from data plane.

## Guardrails

- Keep the answer architecture-first; avoid jumping straight to framework picks.
- Distinguish retrieval, orchestration, inference, and storage responsibilities.
- Make cost/latency/quality trade-offs explicit.

## References

- `references/template-map.md`

