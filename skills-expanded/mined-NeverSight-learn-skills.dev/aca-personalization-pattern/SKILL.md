---
name: aca-personalization-pattern
description: "Apply ACA prompt-mode personalization patterns to outbound campaigns. Use when the user wants scalable personalization, dynamic campaign prompts, first-line personalization, AI-written DMs, or QA samples before launch."
license: MIT
compatibility: Requires the ACA MCP server connected with a valid bearer token.
metadata:
  author: ACA
  version: "1.0"
  homepage: https://aca.so/product/campaigns
---

# ACA personalization pattern

Use ACA's campaign `analyze_contact` step and prompt-mode messages to personalize at scale.

## Rules

- Use `analyze_contact` before personalized copy when possible.
- Write prompt instructions that constrain length, tone, CTA, and prohibited claims.
- QA samples before activating.
- Do not rely on non-existent per-lead injection tools.

## Workflow

1. Inspect target campaign/list with `get_campaign`, `get_lead_list`, and sampled `get_contact` calls.
2. Identify fields available for personalization: role, company, industry, lead score, tags, LinkedIn URL, prior notes, and analysis data.
3. Draft prompt-mode instructions for each step:
   - Connection request
   - LinkedIn DM
   - Email
   - Follow-up
4. Generate 3-5 sample outputs manually from sampled contact data and review for hallucination risk.
5. If approved, update a draft/paused campaign with `update_campaign`.

## Output format

```text
Personalization pattern:
Data available: {fields}
Risk: {low/medium/high}

Step prompt:
{prompt}

Sample QA:
- {contact}: {sample}
```

## Skill chaining

This skill participates in the ACA chain. Preserve the selected ACA org, relevant IDs, user brief, approval state, and any generated artifacts when continuing into another ACA skill. If the user asked for execution and a downstream condition is met, continue into the next skill automatically; otherwise end with the handoff block.

**Upstream**
- Called by `aca-campaign-copywriting`, `aca-launch-outreach`, or `aca-experiment-design` when scalable personalization is needed.

**Auto-continue conditions**
- After prompt-mode instructions are drafted -> continue to `aca-copy-spam-checker`.
- If QA samples are acceptable and campaign is draft/paused -> continue to `aca-launch-outreach` or update through `aca-campaign-copywriting`.

**Stop before chaining when**
- Ask before updating a campaign.

**Downstream skills**
- `aca-copy-spam-checker` - check generated message risk.
- `aca-launch-outreach` - build or update the campaign.
- `aca-experiment-design` - test personalization against a control.

**Handoff block**

```text
Chain state: {continue|needs_approval|blocked|complete}
Next skill: {aca-skill-name|none}
Reason: {why this handoff is or is not needed}
Carry forward: {org_id/name, product_id, icp_id, lead_list_id, campaign_id, sequence_id, job_id, approvals, constraints}
```

## ACA tools used

- `get_campaign`, `update_campaign`
- `get_lead_list`, `get_contact`
- `create_strategy_document`
