---
name: qa-management
description: >
  Diligence Q&A process acceleration. Synthesizes approved VDR documents,
  disclosure schedules, and prior responses to draft source-cited answers
  to buyer diligence questions. Routes drafts for expert approval while
  maintaining consistency across a multi-bidder auction process.
  Use when user asks to "manage Q&A process", "organize buyer questions", "data room Q&A", or mentions Q&A tracking, management presentations, or buyer inquiries.
---

# Q&A Management

Use only materials approved for the specific bidder, diligence phase, and clean-team boundary. Cite every draft answer, preserve prior approved language, flag conflicts, and never send or publish a response without the designated expert and disclosure approval.

As transactions enter confirmatory diligence, the Q&A process can devolve into a logistical nightmare. Multiple bidders submit hundreds of granular questions about tax liabilities, employee benefits, and IT infrastructure. Junior deal team members become administrative traffic cops, routing questions, chasing answers, and formatting responses.

## The /draft-qna Protocol

### How It Works

1. **Connect** to approved VDR documents, existing disclosure schedules, and prior Q&A
2. **Analyze** each buyer question to identify the relevant data source
3. **Draft** a preliminary response synthesizing approved materials
4. **Cross-reference** against previously answered questions for consistency
5. **Flag** for expert approval with routing recommendations
6. **Track** response status across all bidders

### Output Format

```
## Q&A Response Draft

### Question [#]
**From**: [Bidder name]
**Category**: [Financial / Legal / HR / Operations / IT / Tax]
**Question**: [Full question text]

**Draft Response**:
[Response synthesized from approved materials]

**Sources Used**:
- [VDR document reference and folder path]
- [Prior Q&A reference if applicable]

**Routing**: → [CFO / General Counsel / CTO] for approval
**Sensitivity**: [Standard / Restricted / Highly Confidential]
**Consistency Check**: [Aligned with prior responses / POTENTIAL CONFLICT with Q#X]
```

### Multi-Bidder Consistency Tracking

```
## Q&A Consistency Matrix

| Topic | Bidder A Response | Bidder B Response | Consistent? |
|-------|------------------|------------------|-------------|
| EBITDA adjustments | Referenced QoE §3.2 | Referenced QoE §3.2 | ✅ |
| Customer concentration | Disclosed top 10 = 45% | Disclosed top 5 = 38% | ⚠️ REVIEW |
| Pending litigation | Full disclosure | Full disclosure | ✅ |
```

## Operating Guidelines

- Never disclose information beyond what's been approved for the current diligence phase
- Maintain strict information barriers between bidders in a competitive auction
- Flag any question that could require disclosure of material non-public information
- Cross-reference every response against prior answers to prevent contradictions
- Route tax questions to tax counsel, employment questions to labor counsel
- Track response turnaround time — delays signal deal fatigue to bidders
- Preserve the Q&A log as it becomes part of the deal's legal record

Track actual handling time, approval latency, and rework. Never send a draft or disclose a document without the designated expert and disclosure approval.


## Examples

**Input**: "Draft a response to buyer question: 'Explain the $3.2M revenue reclassification in Q3 2023.'"  

**Auto-drafted response**:
> The Q3 2023 reclassification reflects adoption of ASC 606 effective July 1, 2023. Previously, installation revenue was recognized at contract signing; under the new standard, it is deferred and recognized over the implementation period (typically 60–90 days). The change had no cash impact. Supporting documentation is available in the VDR at [4.3.2 — Revenue Recognition Policy Memo].

*Routed to: CFO for approval. SLA: 24 hours.*


## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Q&A responses are inconsistent across bidders | No central response register | Maintain a master Q&A log; all answers distributed to all bidders |
| Expert approval is a bottleneck | Routing to wrong reviewer | Build a topic taxonomy; auto-route by category (legal → counsel, financial → CFO) |
| Sensitive information leaked in response | Draft not reviewed | Never send auto-draft directly; stage → review → approve → distribute |
| Response tracker gets out of sync | Manual updates | Use a shared spreadsheet with auto-timestamp on status change |
