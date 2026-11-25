---
name: specify-the-audience
description: "Describe the audience's expertise and needs so vocabulary, detail, and framing fit the intended reader."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["audience-calibration", "stakeholder-management", "communication", "framing", "readability", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Specify the Target Audience (Audience Calibration) (AI Skill)

## Overview
When you prompt an AI without naming a specific reader, the model writes for an imaginary "average internet user." The result is almost always misaligned: too technical for executive leadership, too simplistic for senior engineers, or too stiff for customers.

The **Audience Calibration Protocol** anchors the AI to a concrete **Reader Profile** - instantly tailoring vocabulary, technical density, and emotional framing to match the exact priorities of that stakeholder.

---

## The 4 Core Stakeholder Archetypes

```
┌─────────────────────────────────────────────────────────────┐
│                 The 4 Stakeholder Profiles                  │
│                                                             │
│  1. THE NON-TECHNICAL EXECUTIVE (CEO / CFO)                 │
│  • Focus: Revenue, margin, operational risk, timeline       │
│  • Banned: Raw technical jargon, code snippets, acronyms    │
│                                                             │
│  2. THE SENIOR DOMAIN PEER (Staff Engineer / Legal Counsel) │
│  • Focus: Architecture, edge cases, exact specs, trade-offs │
│  • Tone: Direct, high density, no introductory fluff        │
│                                                             │
│  3. THE EVERYDAY CUSTOMER / END-USER                        │
│  • Focus: "What's in it for me?", ease of use, clear steps │
│  • Tone: Warm, empathetic, 5th-to-8th grade reading level   │
│                                                             │
│  4. THE SKEPTICAL INVESTOR / BOARD MEMBER                   │
│  • Focus: Defensibility, unit economics, risk mitigation    │
│  • Tone: Metrics-driven, objective, zero vanity buzzwords   │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Audience-Anchored Prompt Templates

### Pattern 1: The Multi-Audience Translation Engine
Use when you have a single technical update that needs to be communicated to different teams:

```markdown
Here is the core project update / technical RFC: [PASTE TEXT].

Generate 2 distinct tailored summaries:

### Version A: For the Non-Technical Executive (CFO / CEO)
- Frame strictly around cost, business risk, and delivery date.
- Under 100 words. Zero technical jargon.

### Version B: For the Engineering Team (Slack Announcement)
- Focus on technical migration steps, breaking API changes, and branch PR links.
- Direct, bulleted technical breakdown.
```

---

## Real-World Case Study

### Scenario: Upgrading Infrastructure from Static EC2 to EKS Kubernetes

#### Version A: Tailored for the Non-Technical CFO
> **Subject**: Infrastructure Cost Optimization Update
> 
> *Our engineering team completed our cloud server modernization this morning. By switching from fixed monthly servers to automated autoscaling, we cut our idle cloud compute costs by **$4,500/month (32% savings)** and eliminated the traffic slowdowns we experienced during last month's sale.*
> 
> ✅ *(Focuses 100% on cost savings and business stability).*

#### Version B: Tailored for Senior Engineering Peers
> **Subject**: EKS Cluster Migration Complete (Karpenter Autoscaling Live)
> 
> *We have completed cutover from static `m5.large` EC2 instances to AWS EKS managed node groups using Karpenter. Pod disruption budgets are set to `minAvailable: 1`, and nodes automatically spin down during off-peak hours. Please ensure all new service Helm charts define CPU/memory requests to prevent OOM kills.*
> 
> ✅ *(Focuses 100% on tooling, configurations, and developer action items).*

---

## Summary Best Practices
- **Name the job title**: *"Write this for a Chief Security Officer (CSO)"* activates entirely different vocabulary than *"Write this for a marketer"*.
- **Specify the reading level**: Use *"Write at an 8th-grade reading level"* for consumer-facing onboarding text.
- **State what the reader cares about**: Add *"The reader's primary concern is avoiding downtime"* to guide the narrative emphasis.
