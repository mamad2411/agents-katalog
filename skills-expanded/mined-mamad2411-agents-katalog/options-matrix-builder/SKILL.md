---
name: Options Matrix Builder
description: Synthesizes disagreements into 2-3 viable options with pros/cons, risk, reversibility, confidence, cost, time-to-impact. Use when specialists disagree.
version: 1.0.0
dependencies: none
---

# Options Matrix Builder

## Overview

When research specialists or domain experts disagree on recommendations, this skill synthesizes their positions into a clear, decision-ready options matrix. It surfaces the trade-offs without forcing premature consensus.

**When to use this skill:**
- After collecting position memos from specialists
- When there are 2+ viable paths forward
- Before presenting final recommendation to decision-maker

## Core Philosophy: Dissent as Signal

Disagreement is not a bug—it's a feature. When smart people with access to the same data reach different conclusions, it means:
1. **The decision is non-trivial** (otherwise consensus would be easy)
2. **Trade-offs exist** (no obviously dominant option)
3. **Multiple perspectives matter** (each specialist sees different dimensions)

The goal is **not** to eliminate dissent through debate. The goal is to **structure it** so the decision-maker can make an informed choice.

## The Options Matrix Format

### Template

```json
{
  "decision": "How should we position our AI coding agent for solo developers?",
  "date": "2025-10-18",
  "specialists_consulted": ["pm", "strategic-advisor", "ux-designer", "finance-consultant"],
  "options": [
    {
      "id": "option_a",
      "name": "Enterprise-First Positioning",
      "summary": "Target engineering teams at Series B+ startups (50-200 employees)",
      "champion": "strategic-advisor",
      "supporters": ["finance-consultant"],
      "pros": [
        "Higher willingness-to-pay ($50/seat/month vs $20 for individuals)",
        "Stickier (once integrated into workflows, high switching cost)",
        "Clearer path to $10M ARR (200 companies * 50 seats * $50 = $500K MRR)"
      ],
      "cons": [
        "Longer sales cycles (3-6 months)",
        "Requires dedicated sales team (not solo-founder friendly)",
        "Product must support SSO, audit logs, team management (scope creep)",
        "Crowded market (competing with GitHub Copilot Enterprise, Cursor Business)"
      ],
      "risk": "high",
      "risk_rationale": "Execution risk: Solo founder may lack enterprise sales experience. Market risk: Established competitors with deep pockets.",
      "reversibility": "low",
      "reversibility_rationale": "Enterprise features (SSO, RBAC) add complexity that's hard to remove. Brand perception ('enterprise tool') hard to undo.",
      "confidence": "medium",
      "confidence_rationale": "PM has enterprise experience but acknowledges solo founder constraint. Strategic-advisor confident in market size but unsure about competitive moat.",
      "cost": "high",
      "cost_details": {
        "development": "$80K (SSO, team mgmt, compliance features)",
        "sales_marketing": "$50K/year (enterprise sales playbook, partnerships)",
        "opportunity_cost": "6 months to build features vs shipping MVP in 2 months"
      },
      "time_to_impact": "9-12 months",
      "time_rationale": "3 months to build enterprise features + 6 months for first enterprise deal to close",
      "key_assumptions": [
        "Can hire enterprise sales consultant within budget",
        "Series B+ startups will switch from incumbents",
        "Solo founder can manage enterprise customer expectations"
      ],
      "major_unknowns": [
        "Will enterprises trust a solo-founder product for mission-critical tooling?",
        "Can we match GitHub/Cursor on features with 10x less budget?"
      ]
    },
    {
      "id": "option_b",
      "name": "Indie Developer Positioning",
      "summary": "Target solo developers and small teams (1-5 people) building side projects or bootstrapped startups",
      "champion": "pm",
      "supporters": ["ux-designer"],
      "pros": [
        "Fast iteration: Ship MVP in 2 months, learn quickly",
        "Low customer acquisition cost (Product Hunt, Reddit, HN = $0)",
        "Founder can do all customer development (no sales team needed)",
        "Niche focus = less direct competition (most tools target enterprises)",
        "Product simplicity (no SSO, RBAC, compliance overhead)"
      ],
      "cons": [
        "Lower WTP ($10-20/month individual)",
        "Harder path to $10M ARR (need 50K users at $20/month)",
        "Churn risk (indie devs more price-sensitive)",
        "Market size uncertainty (TAM for indie dev tools unclear)"
      ],
      "risk": "medium",
      "risk_rationale": "Market risk: Indie dev TAM may be smaller than projected. Monetization risk: Converting free users to paid is hard.",
      "reversibility": "high",
      "reversibility_rationale": "Can pivot to enterprise later (easier to add complexity than remove it). Indie positioning doesn't burn bridges.",
      "confidence": "high",
      "confidence_rationale": "PM and UX-designer have both built successful indie dev tools. Know the playbook. Understand the customer.",
      "cost": "low",
      "cost_details": {
        "development": "$20K (MVP features only)",
        "sales_marketing": "$5K/year (content marketing, community building)",
        "opportunity_cost": "2 months to MVP vs 6 months for enterprise"
      },
      "time_to_impact": "3-4 months",
      "time_rationale": "2 months to build MVP + 1-2 months to get first 100 users and validate monetization",
      "key_assumptions": [
        "Indie devs are underserved by current AI coding tools",
        "$20/month is within budget for side project builders",
        "Word-of-mouth growth is viable (community-driven adoption)"
      ],
      "major_unknowns": [
        "Is the indie dev market large enough to build a sustainable business?",
        "Will we hit a ceiling at $1M ARR and need to pivot to enterprise anyway?"
      ]
    },
    {
      "id": "option_c",
      "name": "Hybrid: Start Indie, Expand Enterprise",
      "summary": "Launch as indie tool, build enterprise features based on demand signals",
      "champion": "none",
      "supporters": [],
      "pros": [
        "Combines speed of indie launch with optionality for enterprise",
        "Learn about enterprise needs from indie customers who grow",
        "De-risks both paths (doesn't bet everything on one)"
      ],
      "cons": [
        "Risks doing both poorly (split focus)",
        "May build indie features that enterprise doesn't need",
        "Unclear positioning in market (are we indie or enterprise?)"
      ],
      "risk": "medium-high",
      "risk_rationale": "Execution risk: Solo founder spreading too thin. Positioning risk: Confusing market message.",
      "reversibility": "medium",
      "reversibility_rationale": "Can commit to one path later, but time spent on hybrid is partially wasted",
      "confidence": "low",
      "confidence_rationale": "No specialist championed this. Emerged as compromise but lacks conviction.",
      "cost": "medium",
      "cost_details": {
        "development": "$40K (indie MVP + some enterprise features)",
        "sales_marketing": "$20K/year (split between indie and enterprise)",
        "opportunity_cost": "4 months (slower than indie, faster than pure enterprise)"
      },
      "time_to_impact": "6 months",
      "time_rationale": "Longer than indie (diluted focus), shorter than enterprise (less scope)",
      "key_assumptions": [
        "Can execute both paths with limited resources",
        "Market won't punish unclear positioning"
      ],
      "major_unknowns": [
        "Which customer segment will we prioritize when trade-offs arise?"
      ]
    }
  ],
  "recommended_shortlist": ["option_b", "option_a"],
  "shortlist_rationale": "Option B (indie) has highest confidence from specialists and best reversibility. Option A (enterprise) is higher-risk but higher-reward if founder wants to bet big. Option C lacks conviction—no specialist championed it.",
  "decision_framework": "If optimizing for learning velocity and capital efficiency → Option B. If optimizing for TAM and willing to accept execution risk → Option A.",
  "next_steps": {
    "if_option_a": "1. Hire enterprise sales consultant. 2. Build SSO/RBAC. 3. Create enterprise sales deck.",
    "if_option_b": "1. Ship indie MVP. 2. Launch on Product Hunt. 3. Collect customer feedback.",
    "if_option_c": "Not recommended unless founder can articulate clear triggers for pivoting to full enterprise or full indie."
  }
}
```

## Building the Matrix: Step-by-Step

### Step 1: Collect Position Memos

Each specialist submits a memo:

**Template:**
```markdown
## Specialist: [name]
## Position: [Option A / Option B / Other]
## Confidence: [High / Medium / Low]

### Recommendation
[1-2 paragraphs: What do you recommend and why?]

### Key Trade-Offs
[What are you optimizing for? What are you willing to sacrifice?]

### Biggest Risk
[What keeps you up at night about this option?]

### Deal-Breaker Scenarios
[Under what conditions would you change your position?]
```

### Step 2: Identify Distinct Options

Cluster similar positions:
- If 3 specialists recommend "enterprise" with slight variations → 1 option with 3 supporters
- If 2 specialists recommend fundamentally different approaches → 2 distinct options

**Aim for 2-3 options max.** More than 3 = analysis paralysis.

### Step 3: Populate Pros/Cons

For each option:
- **Pros:** Extract from supporting specialists' memos (direct quotes when possible)
- **Cons:** Extract from dissenting specialists' critiques + champion's honest assessment

### Step 4: Assess Risk & Reversibility

**Risk (High/Medium/Low):**
- **High:** Multiple unknowns, high $ cost, founder inexperienced in domain
- **Medium:** Some unknowns, moderate cost, founder has adjacent experience
- **Low:** Well-understood, low cost, founder has done this before

**Reversibility (High/Medium/Low):**
- **High:** Decision can be undone in <3 months with minimal sunk cost
- **Medium:** Can pivot but will lose 3-6 months of effort
- **Low:** One-way door (Amazon concept); very hard to undo

### Step 5: Estimate Cost & Time-to-Impact

**Cost buckets:**
- Development (eng time * rate)
- Marketing/Sales
- Opportunity cost (what could you build instead?)

**Time-to-Impact:**
- When will you see first results? (revenue, users, validation signal)

### Step 6: Surface Key Assumptions & Unknowns

**Key Assumptions:** What must be true for this to work?
**Major Unknowns:** What don't we know that could invalidate the plan?

### Step 7: Recommend Shortlist

Narrow to 2 options (rarely 3) based on:
- Specialist confidence
- Reversibility (favor high-reversibility when uncertain)
- Strategic fit (does it align with founder's strengths/goals?)

## Dissent Documentation

In the appendix, preserve the **full debate**:

```markdown
## Appendix: Specialist Debate Transcript

### Round 1: Initial Positions

**strategic-advisor (Option A - Enterprise):**
> The TAM for enterprise is clear: $5.2B. Indie dev market is speculative at best. We should go where the money is proven.

**pm (Option B - Indie):**
> I disagree. As a solo founder, you'll burn 6 months and $80K on enterprise features before you get a single customer. Indie lets you learn in weeks, not months.

**ux-designer (Option B - Indie):**
> +1 to PM. Enterprise tools require enterprise UX (SSO, admin dashboards, audit logs). That's not your competitive advantage. Your advantage is speed and focus.

**finance-consultant (Option A - Enterprise):**
> From a unit economics standpoint, enterprise makes sense. $50/seat/month vs $20 for indie = 2.5x revenue per user. Churn is also lower.

### Round 2: Addressing Concerns

**strategic-advisor responding to PM:**
> Fair point on time-to-market. But indie's path to $10M ARR requires 50K paying users. That's brutal customer acquisition at scale.

**pm responding to strategic-advisor:**
> True, but we can always go upmarket later. Can't easily go downmarket from enterprise. Reversibility matters.

### Round 3: Convergence / Final Positions

**strategic-advisor:**
> I maintain Option A is higher upside, but I acknowledge the execution risk for a solo founder is real. If founder has limited runway, Option B is defensible.

**pm:**
> Option B is my strong recommendation. Option A is viable if founder is willing to bet big and has 12+ months runway.

*[Full transcript preserved for audit trail]*
```

## Decision-Making Framework

Present a simple heuristic:

```
IF [condition] THEN [option]

Examples:
- IF founder has <12 months runway → Option B (indie)
- IF founder has enterprise sales experience → Option A (enterprise)
- IF optimizing for learning → Option B
- IF optimizing for TAM → Option A
```

## Output Files

1. **Primary:** `research/options_matrix.json` (machine-readable)
2. **Summary:** `research/proposal.md` (includes executive summary of options)
3. **Appendix:** `research/appendix-C-debate-transcript.md` (full specialist positions)

## Quality Checklist

Before finalizing:

- [ ] Each option has named champion (or explicitly "none")
- [ ] Pros/cons are specific (not generic)
- [ ] Risk & reversibility assessed with rationale
- [ ] Cost estimates include $ and opportunity cost
- [ ] Key assumptions and unknowns identified
- [ ] Recommended shortlist (2-3 max) with clear reasoning
- [ ] Decision framework provided (helps decision-maker choose)

## Anti-Patterns

❌ **False Consensus:** Forcing all specialists to agree on one option
✅ **Structured Dissent:** Preserve different positions, let decision-maker choose

❌ **Too Many Options:** Presenting 5+ options
✅ **Curated Shortlist:** Narrow to 2-3 viable paths

❌ **Generic Pros/Cons:** "This is good because it's strategic"
✅ **Specific Trade-Offs:** "This requires $80K and 6 months but targets proven $5B TAM"

❌ **Hiding Dissent:** Only showing majority position
✅ **Surfacing Disagreement:** Full debate in appendix, options matrix in summary

## References

See `templates/options-matrix.json` for full JSON schema
See Amazon's "Disagree and Commit" principle for cultural context
