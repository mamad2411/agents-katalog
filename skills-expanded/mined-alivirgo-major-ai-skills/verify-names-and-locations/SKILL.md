---
name: verify-names-and-locations
description: "Check names, titles, addresses, and locations against reliable sources before using them in a deliverable."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["entity-grounding", "named-entities", "hallucination-prevention", "fact-checking", "verification", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Verify Names, Locations, & Entities (Entity Grounding) (AI Skill)

## Overview
Large Language Models do not possess a live GPS or relational database of human beings; they generate names and locations based on **statistical token probability**. 

When asked to generate market research (*"Who is the Head of Procurement at Company X?"* or *"List 5 boutique coffee roasters in Austin, Texas"*), AI models frequently synthesize plausible-sounding names, fake street addresses, and nonexistent executives.

The **Entity Grounding Protocol** establishes strict rules for detecting entity hallucinations and verifying proper nouns against external ground truth.

---

## Statistical Plausibility vs. Ground-Truth Reality

```
┌─────────────────────────────────────────────────────────────┐
│                 Entity Hallucination Trap                   │
│                                                             │
│  User asks: "Who is the Chief AI Officer at Acme Corp?"     │
│                            │                                │
│                            ▼                                │
│  [ LLM TOKENS GENERATE STATISTICAL PLAUSIBILITY ]:          │
│  "Dr. Sarah Jenkins, former MIT AI Lab researcher..."       │
│  ↳ Plausible sounding, perfectly formatted, 100% FICTION    │
│                            │                                │
│                            ▼                                │
│  [ THE 4-POINT GROUNDING LADDER (External Verification) ]:  │
│  1. Check LinkedIn / Company 'About' Page                   │
│  2. Verify Secretary of State Corporate Filings             │
│  3. Verify Street Address on Google Maps / Postal DB        │
│  4. Search Official Press Releases for Appointment Date    │
└─────────────────────────────────────────────────────────────┘
```

---

## The 4 High-Risk Entity Danger Zones

1. **Executive & Staff Names**: Corporate turnover is rapid; models hallucinate past or fictional personnel.
2. **Physical Street Addresses & Suite Numbers**: Models generate realistic-looking street numbers that lead to empty lots.
3. **Local Business Names & Phone Numbers**: Phone numbers and store hours change frequently.
4. **Legal & Court Case Citations**: Precedent case names (e.g. *Smith v. Johnson Corp*) are notoriously confabulated.

---

## Master Entity Verification Prompt Templates

### Pattern 1: The Named Entity Sourcing Directive
Use when conducting market intelligence, B2B lead generation, or competitive research:

```markdown
List the key leadership team at [COMPANY].

Strict Entity Grounding Rules:
1. For every individual listed, provide their **exact job title** and the source URL where this is verified.
2. If their current role cannot be confirmed via your live search tool, mark as: `[STATUS UNVERIFIED / REQUIRES MANUAL CHECK]`.
3. Do NOT extrapolate or guess executive names based on past news.
```

---

### Pattern 2: The Physical Location & Address Guardrail
Use for event planning, logistics, or real estate analysis:

```markdown
Suggest 3 conference venues in [CITY] that can host 200 attendees.
- State the exact venue name, neighborhood, and physical street address.
- Flag any venue that you are unsure is currently in business.
```

---

## Real-World Case Study

### Scenario: Preparing a B2B Sales Outreach List

#### The AI Hallucination Failure
> An SDR prompted AI: *"List the VP of Security at 5 mid-market fintech companies."*
> - The AI generated 5 names.
> - The SDR sent personalized cold emails.
> - **3 of the 5 people never worked at those companies**; 1 had left 3 years prior.
> - Result: High bounce rate and damaged sender domain reputation.

#### The Entity Grounded Workflow
> The SDR added the Grounding Rule: *"List the companies and their current publicly stated Security hiring initiatives; provide LinkedIn search query links rather than generating specific personal names."*
> - The SDR clicked the 5 verified LinkedIn search links in 60 seconds, identified the exact active VPs, and sent emails with 100% accuracy.

---

## Summary Best Practices
- **Never send an email to an AI-generated person's name without checking LinkedIn**: Takes 10 seconds and prevents major embarrassment.
- **Search address coordinates**: Always paste addresses into Google Maps before booking travel or printing collateral.
