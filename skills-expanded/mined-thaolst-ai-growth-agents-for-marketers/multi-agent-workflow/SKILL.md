---
name: multi-agent-workflow
description: >
  Run a two-stage research then planning workflow for growth campaigns.
  Use when the user wants to analyze past campaign data AND create a new plan
  based on that analysis in one connected workflow.
  Stage 1: analyze data and extract structured insights.
  Stage 2: use insights to build a campaign plan.
  Input: past campaign data, target, budget, timeline.
  Output: structured analysis followed by a specific campaign plan.
metadata:
  author: thaolst
  version: "1.0"
  license: MIT
---

# Multi-Agent Workflow: Research + Plan

Hai giai đoạn nối tiếp nhau. Output của giai đoạn 1 là input của giai đoạn 2.

## Giai đoạn 1 — Research Agent

Đọc data campaign và xuất ra JSON có cấu trúc:

```json
{
  "top_performing_mechanics": [],
  "underperforming_areas": [],
  "segment_insights": {},
  "recommended_focus": [],
  "data_gaps": []
}
```

Chỉ trả về JSON, không giải thích thêm.

## Giai đoạn 2 — Strategy Agent

Nhận JSON từ giai đoạn 1. Dựa trên analysis, viết campaign plan với:
- Strategy tổng thể và lý do
- Campaign cụ thể với mechanic, budget, timeline
- Giải thích tại sao mỗi quyết định dựa trên insight từ giai đoạn 1

## Nguyên tắc

Không bỏ qua data gaps từ giai đoạn 1. Mọi quyết định trong plan phải có dẫn chứng từ analysis.

---

# English

Two stages in sequence. Output of stage 1 is input of stage 2.

Stage 1: Analyze campaign data, return structured JSON with top performing mechanics, underperforming areas, segment insights, recommended focus, and data gaps.

Stage 2: Use the JSON analysis to build a specific campaign plan. Every decision must reference insights from stage 1.
