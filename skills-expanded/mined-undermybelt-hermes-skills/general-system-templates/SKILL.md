---
name: general-system-templates
description: Use when a user wants architecture starting points for common non-AI systems such as ecommerce, chat, payment, search, ticketing, storage, mobile apps, or social feeds, and needs components, data flow, trade-offs, bottlenecks, and evolution hints from the awesome-architecture template library.
---

# General System Templates

Use the `awesome-architecture` general system templates as architecture maps for common product classes. Treat each template as a starting point, not a drop-in answer.

## Source Of Truth

- Local source repo: `~/.hermes/external-repos/awesome-architecture`
- Template map: `references/template-map.md`

## When To Use

- `架构模板`, `系统设计模板`, `系统架构模板`
- `电商架构`, `支付系统架构`, `搜索引擎架构`
- `实时聊天架构`, `社交 feed 架构`, `视频流媒体架构`
- `云存储架构`, `通知系统架构`, `在线票务架构`
- `系统设计面试`, `system design interview`

For AI-native systems, route to `comm/arch/ai-system-templates`. For higher-level framing, route to `comm/arch/architecture-thinking`.

## Workflow

1. Match the user's scenario to one or two templates from `references/template-map.md`.
2. Read the matching upstream template files before answering.
3. Structure the answer as:
   - problem shape
   - core components
   - data flow and state hotspots
   - failure and scale bottlenecks
   - key trade-offs
   - evolution path
4. If the user's system blends multiple classes, compare the closest templates and state what transfers cleanly vs what does not.

## Guardrails

- Stay at the architecture level unless the user asks for implementation.
- Do not imply the template is the only valid shape.
- Call out where scale, consistency, latency, or compliance changes the answer.

## References

- `references/template-map.md`

