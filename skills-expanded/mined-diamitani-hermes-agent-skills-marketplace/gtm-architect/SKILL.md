---
name: gtm-architect
description: "Use when designing go-to-market strategies, playbooks, BDR/AE bibles, sales playbooks, or GTM automations with Make/n8n blueprints. Consolidates GTM Engineer, GTM Playbook Architect, and Go To Market Architect."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [gtm, sales-enablement, playbooks, automation, bdr, ae, make, n8n]
    related_skills: [buyer-persona-architect, value-proposition-architect, kpi-architect, use-case-architect]
---

# GTM Architect

## Overview

Consolidates three GTM disciplines into one skill: **GTM strategy design**, **sales playbook creation** (BDR/AE bibles, battlecards, call scripts), and **GTM automation** (Make.com / n8n blueprint generation). Takes a product, audience, or channel hypothesis and produces an actionable launch plan — from high-level strategy down to the automation workflows that execute it.

## When to Use

- Launching a new product, feature, or entering a new market.
- Building or refreshing BDR outbound sequences, AE battlecards, or objection-handling guides.
- Designing automated GTM workflows (lead routing, enrichment, outreach sequences) in Make or n8n.
- A founder or PM says "we need a GTM plan" and needs something tactical, not just a deck.
- Don't use for: brand-only campaigns with no sales motion, or pure content marketing plans.

## How It Works

The skill operates in three modes that flow into each other:

1. **GTM Strategy** — Defines target segments, messaging, channels, and launch sequence.
2. **Sales Playbooks** — Produces BDR/AE bibles with talk tracks, qualification frameworks, objection responses, and battlecards.
3. **Automation Blueprints** — Generates step-by-step Make/n8n scenario designs: lead capture → enrichment → scoring → routing → outreach.

## Steps

1. **Discovery:** Ask the user for product, target audience, competitive context, and current GTM motion (if any). Clarify: are we building strategy, playbooks, automations, or all three?
2. **Strategy output (if needed):** Produce a one-page GTM strategy with: target ICP segments, core messaging by segment, channel mix (outbound, inbound, partner, PLG), launch sequence timeline, and success metrics.
3. **Playbook output (if needed):** By persona/segment, generate:
   - BDR talk track (opener, value prop, qualification questions, objection responses)
   - AE battlecard (discovery framework, demo flow, competitive positioning, pricing talk track)
   - Email/LinkedIn sequences (subject lines, body templates, follow-up cadence)
4. **Automation output (if needed):** For each workflow, produce:
   - Trigger event and data source
   - Enrichment and scoring logic (step-by-step)
   - Routing rules (assignment, SLAs)
   - Make.com or n8n module blueprint (which modules, how connected)
5. **Integration check:** Validate that strategy, playbook, and automations are consistent — the automations should execute the playbook, and the playbook should drive the strategy.

## Common Pitfalls

1. **Strategy without execution:** A GTM plan that stops at slides is worthless. Always push to at least a BDR sequence or automation blueprint.
2. **Generic playbooks:** A BDR script that works for enterprise won't work for SMB. Tailor by segment and persona — use `buyer-persona-architect` if needed.
3. **Automation without exception handling:** Lead routing always needs fallback rules. What happens when enrichment fails? When a lead doesn't match any segment?
4. **No feedback loops:** GTM motions must improve. Include data capture points in every automation so you can measure and iterate.
5. **Over-automating personal touchpoints:** Some sequences (enterprise, strategic accounts) should remain manual or semi-automated. Flag these explicitly.

## Verification Checklist

- [ ] Target segments are clearly defined with ICP criteria
- [ ] Core messaging is differentiated per segment
- [ ] BDR/AE playbook covers discovery, qualification, objection handling, and close
- [ ] Automation blueprints include trigger, enrichment, routing, and fallback paths
- [ ] Success metrics are defined and measurable (not vanity)
- [ ] Strategy, playbook, and automations are internally consistent

## Source

Consolidates three original custom GPTs:
- [GTM Engineer & Automation Architect](https://chatgpt.com/g/g-68ae5687c9b881919c923a432f1fd086-gtm-engineer-automation-architect-gpt)
- [GTM Playbook Architect](https://chatgpt.com/g/g-68ae50b86e748191b3b17da1c50e5c68-gtm-playbook-architect)
- [Go To Market Architect](https://chatgpt.com/g/g-683f2ca476248191b9bdfc97bc4ad641-go-to-market-architect)
