---
name: startup-problem-ledger
description: Capture raw startup pains and sharpen them into testable problem statements before proposing products, with optional formatted single-file HTML artifact output.
license: MIT
metadata:
  display_name: Startup Problem Ledger
  hermes:
    tags: [startup, ideation, problem-discovery, customer-discovery, validation]
    category: business
    requires_toolsets: []
---

# Startup Problem Ledger

## When to use

Use when the user notices an annoyance, repeated manual task, customer complaint, internal workflow issue, market inefficiency, product idea, or asks whether something could be a business.

Do not start by designing the product. First log the observation, sharpen the problem, and check whether it is startup-shaped.

## Core rule

Keep the user anchored on the pain, the person feeling it, the moment it happens, the workaround, and the cost. Avoid turning every frustration into a SaaS idea by default.

## Workflow

1. Capture the raw observation in the user's words.
2. Fill the problem ledger using only known information.
3. Mark unknowns as `Unknown`, not guessed facts.
4. Sharpen the vague pain into one or more specific problem statements.
5. Screen for whether the problem is painful, specific, timely, underserved, founder-fit, and expandable.
6. Ask only the highest-value missing questions first. Prefer 3–5 questions, not a giant form.
7. Decide whether the entry is `Startup-shaped`, `Unclear`, or `Probably not`.
8. Suggest the next validation step, not a product roadmap.
9. Produce or update the shared evidence packet so later skills inherit the same facts, unknowns, and decision gate.

## Problem ledger

Use this format:

```markdown
Raw observation:
Context:
Who experienced it:
Where/when it happened:
Problem:
User/persona:
Job they are trying to do:
Obstacle:
Current workaround:
Cost of doing nothing:
Frequency:
Emotional intensity:
Potential buyer:
Existing tools/alternatives:
Why now:
Founder advantage:
Distribution route:
Expansion path:
Could I reach 10 users:
Could I build v1 in 2–4 weeks:
Startup-shaped: yes/no/unclear
Next validation step:
```

## Opportunity screen

Check these properties before calling something startup-shaped:

```markdown
Painful: expensive, frequent, embarrassing, risky, or intensely annoying.
Specific: exact customer and exact situation are nameable.
Timely: a recent change makes solving it newly possible or urgent.
Underserved: alternatives are absent, bloated, expensive, slow, or misaligned.
Founder-fit: the founder has relevant skill, access, credibility, or obsession.
Expandable: the first niche can grow into adjacent workflows, budgets, or markets.
```

If more than two properties are `Unknown`, keep the entry as `Unclear` and ask the smallest set of questions needed to improve the screen.

## Pain sharpener

After capturing the ledger, produce a sharper version using this shape:

```text
For [specific user],
who needs to [job],
but struggles because [obstacle],
currently using [workaround],
the cost is [time/money/risk/revenue/stress/compliance impact].
```

If the problem is still vague, split it into candidate problem statements instead of forcing one.

## Question prompts

Use plain, direct questions such as:

- Who exactly has this problem? Be narrower than an industry if possible.
- What are they trying to do when the problem appears?
- What triggered the last real instance of it?
- What do they do today instead?
- Is the workaround hated, expensive, risky, or merely untidy?
- What does doing nothing cost in time, money, risk, lost revenue, stress, or compliance exposure?
- How often does it happen per person, team, or business?
- Who has budget or authority to pay for a fix?
- What tools, agencies, spreadsheets, scripts, or internal processes already compete with this?
- Why is this more urgent now than two years ago?
- What founder advantage makes this problem easier to notice, understand, reach, or solve?
- If the first niche worked, what adjacent workflow, buyer, or budget could it expand into?
- Could you realistically speak to 10 people with this problem in the next fortnight?
- Could a v1 prove value in 2–4 weeks without building a platform?

## Optional HTML artifact

Default to the Markdown chat output below. If the user asks for an artifact, report, visual summary, printable version, or single-file HTML file, also create a standalone `.html` file when filesystem access is available.

For the HTML artifact:

- Use one self-contained file with inline CSS only; do not depend on external assets, fonts, scripts, CDNs, or network access.
- Preserve the same section order, evidence, scores or ratings when present, and recommendations as the Markdown output; do not add new claims for visual polish.
- Design for skimming: title, stage, decision/status badge when applicable, key scores or ratings, tables, callouts for risks, unknowns, and next steps, and a print-friendly layout.
- HTML-escape user-provided text and do not execute or embed user-provided HTML or script.
- Include the source skill name and generation date in small footer text.
- Name the file with the stage and date, such as `startup-problem-ledger-YYYY-MM-DD.html`.
- In chat, keep a short summary and link to the created HTML file. If file writing is not available, provide the complete HTML in a fenced `html` block.

## Output format

```markdown
## Problem ledger entry

Raw observation: ...
Context: ...
Who experienced it: ...
Where/when it happened: ...
Problem: ...
User/persona: ...
Job they are trying to do: ...
Obstacle: ...
Current workaround: ...
Cost of doing nothing: ...
Frequency: ...
Emotional intensity: ...
Potential buyer: ...
Existing tools/alternatives: ...
Why now: ...
Founder advantage: ...
Distribution route: ...
Expansion path: ...
Could I reach 10 users: ...
Could I build v1 in 2–4 weeks: ...
Startup-shaped: yes/no/unclear
Next validation step: ...

## Sharper problem statement

For ..., who needs to ..., but struggles because ..., currently using ..., the cost is ...

## Biggest unknowns

1. ...
2. ...
3. ...

## Next questions

1. ...
2. ...
3. ...

## Evidence packet

Stage: Problem ledger
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
Decision gate: [Ready to grill / Needs more problem detail / Park]
Next step: ...
```

## Quality bar

A ledger entry is good enough to grill when:

- The user segment is specific enough to find real people.
- The triggering situation is concrete.
- The current workaround is known or explicitly unknown.
- The cost is plausible and testable.
- There is a credible buyer or a clear reason the buyer is not yet known.
- Founder advantage, timing, and reachability are known or explicitly unknown.
- The next validation step can happen before a full build.

## Pitfalls

- Do not invent market size, pricing, or customer behaviour.
- Do not praise the idea as good before the problem is clear.
- Do not optimise for a polished pitch. Optimise for something falsifiable.
- Do not ask all questions every time. Ask the questions that change the next decision.
- Do not treat a neat workflow improvement as a startup until reach, buyer, urgency, and willingness to pay are plausible.
