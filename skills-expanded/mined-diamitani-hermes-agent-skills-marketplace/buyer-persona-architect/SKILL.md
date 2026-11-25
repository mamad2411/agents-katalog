---
name: buyer-persona-architect
description: "Use when generating detailed user and buyer personas from documents, research, or prompts. Includes ICP definition and segmentation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [personas, icp, buyer-persona, segmentation, customer-research, target-audience]
    related_skills: [value-proposition-architect, gtm-architect, jobs-to-be-done, strategic-business-architect]
---

# Buyer Persona Architect

## Overview

Generates detailed, actionable buyer and user personas from any input: rough notes, interview transcripts, market research, survey data, competitor analysis, or even just a product description. Each persona includes demographics, psychographics, goals, pain points, buying triggers, objections, decision-making process, and preferred channels. Also produces Ideal Customer Profile (ICP) definitions for account-based targeting and segmentation strategies.

## When to Use

- Building personas for a new product, campaign, or market entry.
- Existing personas are outdated, too generic, or not used by sales/marketing.
- Defining ICP criteria for outbound prospecting or ABM campaigns.
- Onboarding new sales/marketing hires who need to understand the target audience fast.
- Prepping for a messaging workshop or GTM strategy session.
- Don't use for: deep ethnographic research (this synthesizes, it doesn't conduct original research), or psychographic segmentation for consumer brands (B2C personas need different depth).

## How It Works

1. **Input digestion** — Accepts structured or unstructured input: interview notes, survey results, product specs, competitor personas, or simple prompts.
2. **Persona generation** — Produces 3-5 distinct personas per audience with a standardized template.
3. **ICP extraction** — Derives firmographic and behavioral ICP criteria from the persona set.
4. **Segmentation map** — Shows how personas relate to each other, who influences whom, and where they sit in the buying committee.

## Steps

1. **Gather source material:** Ask the user for any of: customer interview notes, survey data, product description, target market description, competitor analysis, or rough persona notes. If none exists, use a guided questionnaire: industry, company size, role/title, key pain point, what triggers a purchase.
2. **Generate personas:** For each persona, produce:
   - **Name + Role:** A memorable archetype label (e.g., "Scaling Sarah — VP of Engineering at 50-200 person SaaS")
   - **Demographics:** Title, company size, industry, location, experience level
   - **Goals & Motivations:** What does success look like in their role?
   - **Pain Points:** What frustrates them daily? What's the cost of inaction?
   - **Buying Triggers:** What event makes them start looking for a solution?
   - **Objections:** What would stop them from buying?
   - **Decision Process:** Who else is involved? What's their approval chain?
   - **Preferred Channels:** Where do they learn about new tools? (LinkedIn, peers, review sites, events)
   - **Messaging Hooks:** What language resonates with them?
3. **Define ICP:** Extract firmographic criteria:
   - Company size (employees/revenue)
   - Industry/vertical
   - Geography
   - Tech stack / tooling maturity
   - Budget range
   - Key behavioral signals (hiring in relevant roles, using complementary tools)
4. **Segmentation map:** Show the buying committee structure — who's the champion, the decision-maker, the blocker, the end user. Map how they influence each other.
5. **Validation prompts:** Provide 5-10 interview questions the user can use to validate or refine each persona with real customers.

## Common Pitfalls

1. **Fictional fluff:** Personas with made-up backstories ("Janet has two kids and loves hiking") add noise without insight. Stick to job-relevant attributes.
2. **Too many personas:** 8+ personas means the segmentation is too granular (or the product is too broad). Aim for 3-5 B2B personas max.
3. **No differentiation between buyer and user:** In B2B SaaS, the buyer (VP/C-suite) and the user (individual contributor) have different pain points. Build both.
4. **Static personas:** Personas should be living documents. Include a "last updated" date and suggested review cadence (quarterly for early-stage, annually for mature).
5. **No activation path:** A persona doc that sits in a folder is useless. Connect each persona to a sales play, an email sequence, or a campaign.

## Verification Checklist

- [ ] Each persona covers all template sections (role, goals, pains, triggers, objections, channels)
- [ ] ICP criteria are specific and measurable (not "mid-market" but "50-500 employees, $5M-$50M revenue")
- [ ] Buying committee structure is mapped
- [ ] Personas are differentiated (not slight variations of the same person)
- [ ] Validation interview questions are included
- [ ] Activation path: which team uses this persona for what?

## Source

Originally a custom GPT: [Buyer Persona Architect](https://chatgpt.com/g/g-68ae33816490819185f5116a20f0f1d2-buyer-persona-gpt)
