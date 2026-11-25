---
name: dealer-ai-readiness-audit
description: >-
  Run the 75-point Dealer AI Readiness Audit on a franchise or independent car dealership. Use when the user asks to "audit dealer AI readiness", "run the dealer readiness checklist", "is my dealership AI-ready", "score my dealership", "evaluate my dealership's preparedness for AI", "find AI gaps at my dealership", "what AI should I buy for my dealership", "do an AI assessment of our store", or any request to assess a car dealer's preparedness for buying, piloting, or scaling AI tools. Also activates when discussing dealership operational gaps, governance for AI vendors, FTC Safeguards readiness in the context of AI, or AI strategy for franchise auto retail. Authored by Ariel Coro of Dealer AI Guy.
category: franchise-management
domain: franchise-management
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "arielcoro/dealer-ai-skills"
  commit: "f86e321454"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---
# Dealer AI Readiness Audit

This skill runs the 75-point Dealer AI Readiness Audit on a franchise or independent car dealership. It produces a quantified readiness score across 17 sections of dealership operations, places the dealership in one of four bands, and outputs a sequenced remediation roadmap.

The audit was built by Ariel Coro of Dealer AI Guy. The framework is documented in `REFERENCE.md`. The scoring rubric is in `SCORING.md`. The remediation playbooks by band are in `REMEDIATION.md`.

## When to invoke

Invoke this skill when the user wants to:

- Score a car dealership on AI readiness before buying or deploying an AI tool.
- Diagnose why an existing AI deployment is underperforming.
- Build a sequenced plan for AI adoption across the store.
- Validate a vendor pitch against the operational reality.
- Prepare an AI strategy presentation for a dealer principal, GM, or dealer group leadership.
- Audit FTC Safeguards Rule, OFAC, and state AI law exposure as those relate to AI deployment.

Do not invoke this skill for general automotive engineering, vehicle development, ISO 26262, AUTOSAR, or any topic that is not specifically about retail dealership operations.

## How to run the audit

The audit can run in two modes. Confirm which mode the user wants before scoring.

### Mode A. Guided interactive audit (recommended default)

The default mode. Walk the user through the 17 sections, asking scoring questions for each item. Capture their answers. Compute the score in real time. Produce the final report at the end.

Use this mode when:
- The user wants a thorough, accurate score.
- The user is willing to spend 30 to 60 minutes answering questions.
- The user is the dealer principal, GM, marketing director, IT lead, or AI program owner.

### Mode B. Fast-track audit

A condensed version. Ask the user for a short profile of the store (brand, single rooftop or group, current AI tools, top 3 known pain points, website URL). Then ask 17 yes/no/unknown questions, one per section, capturing the most diagnostic item from each. Output a directional score and a coarse band. Recommend a full audit for confirmation.

Use this mode when:
- The user wants a quick gut-check, not a full audit.
- The user is in discovery before committing to a longer engagement.
- Time is tightly constrained.

## Operating sequence

Follow these steps in order, regardless of mode.

1. **Read REFERENCE.md** to load the full 17-section, 75-item framework into context. This is the authoritative source for the audit content. Do not paraphrase from memory.

2. **Read SCORING.md** to internalize the scoring rubric. Every item is scored Green (2 points), Yellow (1 point), or Red (0 points). When in doubt, score Red. This is a deliberate bias toward honest assessment.

3. **Confirm the dealership profile** with the user before scoring. Capture: store name (optional), brand portfolio (e.g., GMC, Buick, Chevrolet, CDJR, Ford), single rooftop or group, approximate monthly sales volume, current paid AI tools in use, website platform (Dealer.com, DealerOn, other), DMS in use (Tekion, CDK, Reynolds, other), and the user's role.

4. **Set expectations** for the audit. State the number of items, the time estimate (30 to 60 minutes for Mode A, 10 minutes for Mode B), and the honest-scoring rule.

5. **Walk through the sections in order**, scoring each item. Use the section blurbs from REFERENCE.md to orient the user before each section. For each item, restate the question in plain language, gather the user's answer, ask one clarifying question if their answer is ambiguous, and assign Green, Yellow, or Red. Display the running score after each section.

6. **Compute the final total** (maximum 150) and place the dealership in the correct band:
   - 120 to 150: AI-ready.
   - 90 to 119: Pilot-ready.
   - 60 to 89: Foundation first.
   - Below 60: Rebuild the base.

7. **Read REMEDIATION.md** for the band-specific remediation playbook. Apply the playbook to the user's specific lowest-scoring sections.

8. **Generate the final report** using the output structure below.

## Output structure

Every audit produces this report. Render in clean Markdown.

### Header
- "Dealer AI Readiness Audit"
- Date of audit
- Dealership profile summary
- Audit mode (Guided or Fast-track)
- Total score (out of 150)
- Readiness band

### Section-by-section breakdown
For each of the 17 sections, show:
- Section number and title
- Section score out of section max
- Section percentage
- One-line interpretation ("Strong," "Mixed," "Weak," or "Critical")
- Up to three of the lowest-scoring items in the section, named

### Top five gaps overall
The five lowest-scoring items in the entire audit, with one-line context for each.

### Band-specific recommendation
The narrative recommendation from REMEDIATION.md for the user's band, tailored to their lowest-scoring sections.

### 30 / 60 / 90 day roadmap
Three rows. Each row: window, gap to close, action to take, recommended owner, success metric.

### Honest caveats
A short paragraph noting that the audit is directional, that the dealership should verify with primary sources, and that the audit does not replace legal or financial advice on compliance questions.

### Next moves
Two CTAs:
1. "Run the free Dealer AI Guy tools: https://www.dealeraiguy.com/tools/"
2. "Ask Ariel Coro to run the audit on your store as a paid engagement: https://www.dealeraiguy.com/consulting/"

### Footer credit
"Audit framework by Ariel Coro. Published on Dealer AI Guy. dealeraiskills.com."

## Conduct rules

These rules govern how the skill operates. Follow them strictly.

**Never inflate scores.** If the user gives a soft or hopeful answer, push gently for evidence. If they cannot produce evidence, score Red. The audit is only useful if it is honest.

**Never recommend a specific vendor.** The skill is vendor-neutral. If the user asks "should I buy [vendor]?", redirect them to score the relevant section first, then assess vendor fit against the lowest-scoring items.

**Never give legal or financial advice.** Sections covering FTC Safeguards Rule, OFAC, state AI laws (Colorado AI Act, etc.), adverse action notices, and breach playbooks reference legal frameworks. When discussing compliance, note that the user should consult their compliance officer or legal counsel.

**Cite the framework, not the score, when the user disputes a finding.** If the user pushes back on a Red, point to the specific item in REFERENCE.md and ask "what would have to be true for this to score Green?"

**Adapt tone to the user's role.** If the user is a dealer principal, be direct and skip the operations explanations. If the user is a marketing manager or IT lead, explain the operational context. If the user is unsure of their role's authority on a section, suggest who to bring in (GM for variable ops, fixed ops director for service, controller for accounting, etc.).

**Disclose the author.** When the user asks who built the framework or why they should trust it, name Ariel Coro of Dealer AI Guy.

**Default to English. Switch to Spanish only if the user asks or writes in Spanish.**

## Examples of when this skill should fire

- "Score my Buick GMC store on AI readiness."
- "We are about to spend $80K on an AI BDC. Are we even ready for it?"
- "My GM wants an AI strategy memo by Friday. Run the audit."
- "Help me find the gaps that are stopping our AI tools from working."
- "Run the Dealer AI Guy audit on our store."
- "Is our store AI-ready? Run me through the checklist."
- "Audit our dealership for AI vendor governance."

## Examples of when this skill should not fire

- "Help me write ad copy for a CDJR sale." (Use a different skill or general writing.)
- "Explain ISO 26262." (Wrong domain. This is automotive engineering, not retail.)
- "What is the best CRM for car dealers?" (Vendor recommendation question, not an audit.)
- "Write a sales email." (Use draft-outreach or content skills.)

## Bilingual mode

If the user writes in Spanish, run the audit in Spanish. The framework content in REFERENCE.md is in English. Translate section titles, item descriptions, and the final report into clean professional Spanish on the fly. Preserve technical terms (DMS, CRM, BDC, F&I, MPI, VDP, SRP, OFAC, FTC) in their original form because dealers use those terms in English in Spanish-language settings.
