---
name: executive-summary
description: Synthesize complex projects into Amazon Working Backwards PR-FAQs, 6-page memos, and McKinsey MECE Pyramid structures.
category: productivity
aliases:
- working-backwards
- pr-faq
- pyramid-principle
- mece
- 6-page-memo
triggers:
- write an executive summary
- Amazon working backwards
- create a PR-FAQ
- McKinsey pyramid principle
- format as an executive memo
keywords:
- executive
- summary
- working-backwards
- pr-faq
- mece
- pyramid
- memo
- leadership
dependencies: []
risk: low
version: 1.0.0
source: custom
enabled: true
lifecycle: enabled
capabilities:
- executive-summarization
- working-backwards-framework
- mece-structuring
inputs:
- project_details
- proposal
- target_audience
outputs:
- executive_memo
- pr_faq_document
- leadership_decision_brief
permissions:
  filesystem: none
  network: none
  shell: none
  secrets: none
author: Mr-Nobody-Anonymous
tags:
- executive
- pr-faq
- productivity
- summary
- working-backwards
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Executive Summary

## Purpose
Synthesizes extensive technical, operational, or strategic initiatives into rigorous executive communication frameworks, specifically Amazon's Working Backwards (PR-FAQ / 6-page memo) and McKinsey's MECE Pyramid Principle.

## When to Use
- Preparing proposals or strategic recommendations for executive leadership or stakeholders.
- Defining a new product or technical initiative before writing code (Working Backwards).
- Structuring complex, multi-faceted arguments with Mutually Exclusive, Collectively Exhaustive (MECE) clarity.
- Condensing large technical project reports into decision-oriented executive briefs.

## When NOT to Use
- Day-to-day granular code commits or inline PR comments.
- Raw developer setup instructions or internal technical task logs.

## Capabilities
- **Working Backwards (PR-FAQ)**: Draft customer-facing press releases and internal FAQs before building.
- **Pyramid Principle**: Lead with the governing conclusion, supported by MECE argument groups.
- **6-Page Narrative Memo**: Structure context, goals, tenet trade-offs, and data-driven recommendations.
- **Decision-Centric Framing**: Clearly present options, trade-offs, required investments, and risks.

## Inputs
- `project_details` (required) — Project scope, findings, data, or proposed change.
- `framework` (optional) — `working-backwards`, `pyramid-principle`, or `6-page-memo`.
- `target_audience` (optional) — C-suite, engineering leadership, or external partners.

## Workflow
1. Identify the core decision, proposal, or customer impact statement.
2. Select the appropriate executive framework (PR-FAQ, Pyramid Principle, or Memo).
3. Draft the lead conclusion / Press Release headline and key paragraph.
4. Organize supporting arguments into mutually exclusive, collectively exhaustive buckets.
5. Compile the FAQ covering internal risks, resource requirements, and customer value.
6. Review for clear, quantified data and eliminate ambiguous adjectives.

## Tools
- Analytical and executive communication frameworks.

## Examples
- "Create an Amazon-style PR-FAQ for our new API caching feature."
- "Structure an executive summary of our Q3 reliability metrics using the Pyramid Principle."
- "Write a 1-page executive memo proposing our cloud migration strategy."

## Safety
- Ensure all business metrics, timelines, and financial numbers are accurate and verified.
- Explicitly surface known failure modes, downsides, and trade-offs.

## Source
Custom skill maintained in this library based on executive leadership communication playbooks.

## Notes
Composes with `documents.markdown` and `productivity.planning` to provide end-to-end strategy-to-execution alignment.
