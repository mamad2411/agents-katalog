---
name: startup-problem-inventory
description: Generate a raw inventory of startup problem candidates from founder unfair access, domain observations, workflows, complaints, and recent enabling changes before logging or validating any one idea, with optional formatted single-file HTML artifact output.
license: MIT
metadata:
  display_name: Startup Problem Inventory
  hermes:
    tags: [startup, ideation, problem-discovery, opportunity-discovery, founder-fit]
    category: business
    requires_toolsets: []
---

# Startup Problem Inventory

## When to use

Use when the user asks for startup ideas, wants to run an ideation sprint, has several domains to explore, or needs to turn founder experience into a list of problem candidates.

Do not produce a list of polished product ideas by default. First identify arenas where the founder has access, then collect raw problems and choose candidates worth putting into `startup-problem-ledger`.

## Core rule

Treat a strong startup idea as a painful problem noticed from an unfair vantage point, made newly solvable by a change in technology, regulation, behaviour, cost, or distribution.

Use this mental model:

```text
Strong candidate = painful problem + specific customer + founder insight + recent enabling change + cheap validation path + expansion option
```

## Inputs to request if missing

Ask only the 3-5 questions that most affect the inventory:

```markdown
Founder background:
Domains worked in:
Communities or customer groups reachable:
Tools, workflows, or industries personally suffered through:
Recent technology, regulation, or market changes noticed:
Ability to build or manually deliver a first solution:
```

If the user provides little context, still produce an inventory from stated experience and mark assumptions as `Unknown`.

## Workflow

1. Identify 3-5 idea arenas where the founder has unfair access.
2. For each arena, list concrete workflows, recurring manual work, hated tools, compliance burdens, messy handoffs, spreadsheets, support complaints, or expensive services.
3. Capture raw problem candidates without designing products.
4. Screen each candidate for whether it is painful, specific, timely, underserved, founder-fit, and expandable.
5. Prefer boring, specific, reachable problems over broad market narratives.
6. Pick the best 3-5 candidates for `startup-problem-ledger`.
7. Create an evidence packet seed for the top candidate.

## Opportunity properties

Use these properties as a fast screen, not as false precision:

```markdown
Painful: expensive, frequent, embarrassing, risky, or intensely annoying.
Specific: exact customer and exact situation are nameable.
Timely: a recent change makes solving it newly possible or urgent.
Underserved: alternatives are absent, bloated, expensive, slow, or misaligned.
Founder-fit: the founder has relevant skill, access, credibility, or obsession.
Expandable: the first niche can grow into adjacent workflows, budgets, or markets.
```

## Problem sources

Mine from sources the user can realistically access:

- Own work frustrations and repeated manual tasks.
- Customer or client complaints.
- Support forums, GitHub issues, reviews, Slack, Discord, Reddit, and niche communities.
- Job postings that reveal repeated manual work.
- Expensive consultants, agencies, audits, and professional services.
- Spreadsheets, email threads, PDFs, portals, WhatsApp, and Slack rituals.
- Compliance checklists and reporting burdens.
- New APIs, AI capabilities, rules, platform shifts, cost curves, or buyer behaviour changes.

If browsing is available and the user explicitly asks for external research, collect raw signals from source material and communities before suggesting product concepts.

## Inventory format

For each candidate, capture:

```markdown
Problem candidate:
Arena:
Customer:
Situation:
Current workaround:
Likely cost:
Frequency:
Budget owner:
Founder advantage:
Recent enabling change:
Underserved alternative:
Expansion path:
Reachability:
Fastest validation move:
Unknowns:
```

## Fast score

When comparing many candidates, score each 0-5:

```markdown
Pain intensity:
Frequency:
Existing spend:
Reachable ICP:
Founder fit:
Timing:
Competition gap:
Narrow wedge:
Expansion:
Validation speed:
Distribution:
```

Interpret scores cautiously:

- `45-55`: serious candidate.
- `35-44`: worth ledger and customer discovery.
- `25-34`: needs a sharper customer, wedge, or why-now.
- `Below 25`: park unless stronger evidence appears.

Do not let scoring override concrete evidence from real buyers.

## Optional HTML artifact

Default to the Markdown chat output below. If the user asks for an artifact, report, visual summary, printable version, or single-file HTML file, also create a standalone `.html` file when filesystem access is available.

For the HTML artifact:

- Use one self-contained file with inline CSS only; do not depend on external assets, fonts, scripts, CDNs, or network access.
- Preserve the same section order, evidence, scores or ratings when present, and recommendations as the Markdown output; do not add new claims for visual polish.
- Design for skimming: title, stage, decision/status badge when applicable, key scores or ratings, tables, callouts for risks, unknowns, and next steps, and a print-friendly layout.
- HTML-escape user-provided text and do not execute or embed user-provided HTML or script.
- Include the source skill name and generation date in small footer text.
- Name the file with the stage and date, such as `startup-problem-inventory-YYYY-MM-DD.html`.
- In chat, keep a short summary and link to the created HTML file. If file writing is not available, provide the complete HTML in a fenced `html` block.

## Output format

```markdown
## Idea arenas

1. ...
2. ...
3. ...

## Problem inventory

| Candidate | Customer | Situation | Workaround | Why now | Founder advantage | First validation |
| --- | --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... | ... |

## Best ledger candidates

1. ...
2. ...
3. ...

## Why these candidates

- Painful: ...
- Specific: ...
- Timely: ...
- Underserved: ...
- Founder-fit: ...
- Expandable: ...

## Biggest unknowns

1. ...
2. ...
3. ...

## Evidence packet seed

Stage: Problem inventory
Problem statement: ...
Target user: ...
Buyer / budget owner: ...
Current workaround: ...
Founder advantage: ...
Recent enabling change: ...
Distribution route: ...
Expansion path: ...
Evidence collected: ...
Weakest assumptions: ...
Decision gate: [Ready for problem ledger / Needs founder context / Park]
Next step: ...
```

## Pitfalls

- Do not brainstorm generic SaaS categories when the user needs problem discovery.
- Do not turn every problem into an AI product.
- Do not invent the founder's access, credibility, or buyer network.
- Do not rank ideas only by market size. Reachable pain beats abstract TAM early.
- Do not discard a candidate merely because it sounds boring, niche, operationally messy, or unglamorous.
