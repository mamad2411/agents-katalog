---
name: multi-agent-research
description: >
  Run multi-agent research-to-planning pipeline using two sequential agents.
  Use when the user has campaign data and needs a structured plan without code.
  Agent 1 (Research) analyzes campaign data and returns structured JSON insights.
  Agent 2 (Strategy) takes those insights and produces a complete campaign plan.
  Input: campaign data, target, budget, timeline.
  Output: research findings as JSON → executable campaign plan.
metadata:
  author: thaolst
  version: "1.1"
  license: MIT
  related_skills:
    - campaign-planning
    - campaign-brief
    - growth-mcp-connect
---

# Multi-Agent Research & Planning Agent

Bạn hướng dẫn marketer chạy hai agent nối tiếp nhau — không cần code, chỉ cần hai cuộc trò chuyện riêng trong Claude.

> **Context check:** Reads `.agents/product-marketing-context.md` for market context.
> If growth-mcp connected, pulls market data before research phase.

## Workflow

### Agent 1: Research
Input: campaign data, target, budget.
Output: structured JSON insights về market, segments, past performance, recommendations.

### Agent 2: Strategy
Input: JSON từ Agent 1 + constraints.
Output: executable campaign plan với timeline, budget, mechanics, risks.

## Khi nào dùng

- Có nhiều dữ liệu campaign cần phân tích trước khi lập kế hoạch
- Muốn structured research notes (JSON) trước khi viết plan
- Campaign phức tạp, cần separation of concerns

## Related Skills

- [campaign-planning](../campaign-planning/) — tổng quan plan
- [campaign-brief](../campaign-brief/) — chi tiết từng campaign
- [growth-mcp-connect](../growth-mcp-connect/) — pull research data

---

# English

Guide the marketer through a two-agent sequential pipeline — no code required, just two separate conversations in Claude.

Agent 1 (Research) → Agent 2 (Strategy) = executable campaign plan.
