---
name: legal-intelligent-invoice-team
description: "智能发票专家团。用于五位 AI 专家接力协作，通过上传文件、表格或文件夹，完成识别、税局验真、信用核查与归档。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-intelligent-invoice"
  workbuddy_card: "智能发票专家团"
  workbuddy_category: "法务安全"
---

# 智能发票专家团

Use this skill as the routing entry point for 智能发票专家团 work. It packages the WorkBuddy 法务安全 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `file-ingestion`
- `invoice-ocr`
- `tax-verification`
- `business-credit`
- `smart-archive`
- `audit-trail`

## Output

Produce only the deliverables relevant to the request. For a full 智能发票 package, assemble the output set described in `references/workflow.md`.
