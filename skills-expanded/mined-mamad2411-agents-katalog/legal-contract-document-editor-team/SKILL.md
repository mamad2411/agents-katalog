---
name: legal-contract-document-editor-team
description: "合同与公文审稿。用于在 .docx 原文里加批注和追踪修订，不返刷新文档、不破坏原格式。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-contract-document-editor"
  workbuddy_card: "合同与公文审稿"
  workbuddy_category: "法务安全"
---

# 合同与公文审稿

Use this skill as the routing entry point for 合同与公文审稿 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-contract-document-editor-intake`
- `legal-contract-document-editor-strategy`
- `legal-contract-document-editor-execution`
- `legal-contract-document-editor-quality`
- `legal-contract-document-editor-measurement`
- `legal-contract-document-editor-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 合同与公文审稿 package, assemble the output set described in `references/workflow.md`.
