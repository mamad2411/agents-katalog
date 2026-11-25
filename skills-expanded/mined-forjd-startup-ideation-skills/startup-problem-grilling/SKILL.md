---
name: startup-problem-grilling
description: Stress-test a captured startup problem with sharp questions before validation or product scoping, with optional formatted single-file HTML artifact output.
license: MIT
metadata:
  display_name: Startup Problem Grilling
  hermes:
    tags: [startup, ideation, validation, customer-discovery, critique, tarpit]
    category: business
    requires_toolsets: []
---

# Startup Problem Grilling

## When to use

Use after a startup problem has been captured in a problem ledger, or when the user asks whether a business idea is worth pursuing.

This skill is deliberately sceptical. The goal is not to kill ideas for sport; it is to find fragile assumptions before the user spends weeks building the wrong thing.

## Stance

Be direct, practical, and specific. Question the problem, buyer, urgency, reachability, distribution, willingness to pay, founder fit, tarpit risk, and build scope. Avoid generic startup theatre.

## Inputs to request if missing

Use the evidence packet or problem ledger if it is already in context. If it is missing, do not block useful critique when partial context is enough. Ask only the 3–5 missing questions that would most change the verdict.

Use this full ledger shape when the user wants a formal handoff from the problem ledger:

```markdown
Problem:
User/persona:
When it happens:
Current workaround:
Cost of doing nothing:
Frequency:
Potential buyer:
Existing tools/alternatives:
Why now:
Founder advantage:
Distribution route:
Expansion path:
Could I reach 10 users:
Could I build v1 in 2–4 weeks:
```

## Grilling workflow

1. Restate the problem in its strongest concrete form.
2. Identify the weakest 3–5 assumptions.
3. Map user, buyer, blocker, budget owner, and risk owner.
4. Check tarpit risk and whether distribution may be harder than product.
5. Challenge pricing and willingness-to-pay early.
6. Screen whether the problem is painful, specific, timely, underserved, founder-fit, and expandable.
7. Score founder-market fit against the user's actual advantages.
8. Suggest small validation moves that do not require building the full product.
9. End with a verdict: `Promising`, `Needs narrowing`, `Weak until proven`, or `Probably not worth building yet`.
10. Update the evidence packet with the verdict, weakest assumptions, and the next validation gate.

## Question bank

### Problem reality

- Is this painful enough that people already spend time, money, or political capital on it?
- What happens if they ignore it?
- Is it a frequent problem, a severe problem, or neither?
- Is the pain felt by the same person who would approve a fix?
- Is the current workaround hated, or merely untidy?

### Buyer mapper

Answer these explicitly:

```markdown
Who feels the pain:
Who signs off spend:
Who blocks adoption:
Who owns the risk:
Who benefits from the outcome:
Who loses power if this works:
Budget line or spend category:
```

Hard questions:

- Is the buyer the same person as the daily user?
- Who owns the budget?
- What budget line would this come from?
- Is the cost visible enough for someone to justify paying?
- Would this be bought by an individual, team lead, department, or company?

### Current workaround and alternatives

- What spreadsheet, Slack ritual, outsourced labour, internal tool, manual review, or agency already exists?
- Why have existing tools not solved it?
- What would they search for if they wanted to solve it today?
- Which boring incumbent is already close enough?
- Could an agency, Zapier workflow, VA, spreadsheet, or LLM prompt solve 80% of it?
- What would make switching worth the bother?

### Tarpit detector

Check whether the idea has structural traps:

```markdown
Marketplace or network effects required:
Vague buyer:
Consumer habit change required:
Distribution harder than product:
Many failed versions already:
Pain real but willingness to pay weak:
Feature rather than company:
Only compelling because AI is fashionable:
Trust/compliance burden too high for v1:
```

Rate tarpit risk as `Low`, `Medium`, or `High`, and say why.

### Distribution and reachability

- Can the user name 10 people or organisations to contact?
- Is there a community, marketplace, job title, search query, association, or LinkedIn filter that exposes these users?
- Would these people talk about the problem, or is it private/sensitive?
- Can outreach happen before anything is built?
- What is the first credible channel: direct outreach, LinkedIn content, niche community, partnership, marketplace, SEO, open-source wedge, audit/diagnostic, webinar?

### Timing

- Why now?
- What changed in regulation, technology, behaviour, cost pressure, AI capability, or market structure?
- Is this a new problem, or an old problem with a newly cheap solution?
- What would make the same solution impossible, too expensive, or poorly timed 3-5 years ago?

### Opportunity shape

Check whether the candidate has all six properties:

```markdown
Painful:
Specific:
Timely:
Underserved:
Founder-fit:
Expandable:
```

If one is weak, say how to narrow or retest. If several are unknown, the next step is discovery, not product scoping.

### Pricing and willingness to pay

- What is the current cost of the pain?
- Is there existing spend on staff time, consultants, tools, services, or risk reduction?
- What pricing model could match the value: per file, per user, per team, usage-based, paid audit, setup fee plus subscription, or service-led pilot?
- How could willingness to pay be tested before building a SaaS product?

### Founder-market fit

Score quickly from 0–3:

```markdown
Understands the user: /3
Can reach users: /3
Can build v1: /3
Pain is frequent: /3
Pain is expensive or risky: /3
Clear buyer: /3
Newly possible now: /3
Can test demand before building: /3
```

Use the score as a thinking aid, not false precision.

### Opportunity score

Use this 0-5 score only when comparing multiple candidates or when the user asks which idea deserves focus:

```markdown
Pain intensity:
Frequency:
Existing spend:
Reachable ICP:
Founder fit:
Timing:
Competition gap:
Wedge:
Expansion:
Validation speed:
Distribution:
```

Treat `45-55` as serious, `35-44` as worth deeper discovery, `25-34` as needing sharper narrowing, and below `25` as a park signal unless real buyer evidence says otherwise.

### V1 feasibility

- What is the smallest thing that proves value?
- Can the first version be concierge/manual behind the scenes?
- What can be faked, scripted, or done with off-the-shelf tools?
- What must be true for a 2–4 week build to be meaningful?

## Optional HTML artifact

Default to the Markdown chat output below. If the user asks for an artifact, report, visual summary, printable version, or single-file HTML file, also create a standalone `.html` file when filesystem access is available.

For the HTML artifact:

- Use one self-contained file with inline CSS only; do not depend on external assets, fonts, scripts, CDNs, or network access.
- Preserve the same section order, evidence, scores or ratings when present, and recommendations as the Markdown output; do not add new claims for visual polish.
- Design for skimming: title, stage, decision/status badge when applicable, key scores or ratings, tables, callouts for risks, unknowns, and next steps, and a print-friendly layout.
- HTML-escape user-provided text and do not execute or embed user-provided HTML or script.
- Include the source skill name and generation date in small footer text.
- Name the file with the stage and date, such as `startup-problem-grilling-YYYY-MM-DD.html`.
- In chat, keep a short summary and link to the created HTML file. If file writing is not available, provide the complete HTML in a fenced `html` block.

## Output format

```markdown
## Strongest version of the problem

...

## Weakest assumptions

1. ...
2. ...
3. ...

## Buyer map

Who feels the pain: ...
Who signs off spend: ...
Who blocks adoption: ...
Who owns risk: ...
Budget line: ...

## Tarpit risk

[Low / Medium / High]

Reasons:
- ...

## Founder-market fit

Score: .../24

Biggest gap: ...

## Opportunity shape

Painful: ...
Specific: ...
Timely: ...
Underserved: ...
Founder-fit: ...
Expandable: ...

Opportunity score: .../55

## Grilling questions

### Problem risk
1. ...

### Buyer / willingness-to-pay risk
1. ...

### Reach / distribution risk
1. ...

### Build risk
1. ...

## Fast validation moves

1. ...
2. ...
3. ...

## Verdict

[Promising / Needs narrowing / Weak until proven / Probably not worth building yet]

Because: ...

## Evidence packet update

Stage: Problem grilled
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
Decision gate: [Ready to design validation / Needs narrowing / Park / Kill]
Next step: ...
```

## Pitfalls

- Do not become a cheerleader. If it is vague, say it is vague.
- Do not require venture-scale potential. A small useful business can still pass.
- Do not over-index on TAM. Early evidence from real reachable users matters more.
- Do not suggest building as the default next step when interviews, landing pages, manual fulfilment, paid audits, or paid pilots would answer the bigger risk faster.
- Do not let “AI can do this now” substitute for a buyer, channel, or painful current workaround.
