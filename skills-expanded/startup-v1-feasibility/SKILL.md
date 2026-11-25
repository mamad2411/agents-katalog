---
name: startup-v1-feasibility
description: Scope a startup idea into a narrow wedge and 2–4 week v1 that tests the riskiest assumption, with optional formatted single-file HTML artifact output.
license: MIT
metadata:
  display_name: Startup V1 Feasibility
  hermes:
    tags: [startup, v1, mvp, feasibility, validation, product-scope, wedge]
    category: business
    requires_toolsets: []
---

# Startup V1 Feasibility

## When to use

Use when a captured, grilled, and validated startup problem has enough evidence to justify deciding what to build first.

This skill prevents v1 scope creep. The first version should test the riskiest useful assumption, not become a miniature version of the imagined company.

If the user has not run a validation test or cannot provide credible evidence from real prospects, do not produce a build plan by default. Return a `Not build-ready` verdict, list the missing evidence, and route them back to validation. Only produce a planning-only sketch when the user explicitly asks for a hypothetical plan and label it as unvalidated.

## Core principle

A good v1 is small enough to build in 2–4 weeks and sharp enough that real user behaviour teaches something commercially useful.

## Workflow

1. Start from the evidence packet, problem ledger, grilling notes, and validation results.
2. Check the v1 evidence gate before scoping:
   - Specific target user and buyer are known.
   - Current workaround and cost are grounded in real examples.
   - Founder advantage, recent enabling change, and first distribution route are plausible.
   - There is at least a rough expansion path beyond the first wedge.
   - At least one validation test produced behavioural signal, not compliments.
   - The strongest remaining assumption is one a v1 can test.
3. If the gate fails, stop and return the missing evidence plus the next validation move.
4. Identify the narrow wedge: the painful sliver where a first product can deliver value.
5. Identify the riskiest assumption that building can test.
6. Choose a v1 mode: manual concierge, Wizard-of-Oz, internal tool, workflow wrapper, integration, report, landing page plus manual fulfilment, narrow automation, or paid pilot.
7. Define the smallest user journey that proves value.
8. Cut scope until it is almost uncomfortable.
9. List what is explicitly out of scope.
10. Define success and kill criteria before implementation.
11. Produce a 2–4 week build plan only if the evidence gate and scope are credible.

## Wedge generator

Convert broad areas into narrow entry points:

```markdown
Broad area:
Target market:
Known pain:
Founder advantage:
Recent enabling change:
Distribution route:
Expansion path:

Potential wedges:
1. [Wedge] — [user] — [first value delivered] — [build complexity] — [sales difficulty]
2. ...
3. ...
```

Pick the wedge where pain, reachability, and build speed overlap.

## V1 modes

Prefer boring, fast modes:

- Concierge: user submits input, founder manually produces the outcome.
- Wizard-of-Oz: product interface exists, but fulfilment is manual or semi-manual.
- Report: turn messy inputs into a high-value one-off output.
- Workflow wrapper: connect existing tools and reduce one painful step.
- Narrow automation: automate one repeated task, not the whole job.
- Paid pilot: deliver value for a small number of users before scalable software.
- Diagnostic/audit: reveal a costly problem and sell the next step.

## Scope cutter

Force the v1 through this cut:

```markdown
Core job:
Must have:
Should not have:
Manual steps allowed:
Fake doors allowed:
Human-in-loop required:
Data, trust, or compliance risks:
First demo flow:
Build estimate:
Risks:
```

Default exclusions unless essential to the test:

- Dashboards
- Team management
- Billing
- Permissions systems
- Complex onboarding
- Full integrations
- Polished admin tools
- Multi-tenant platform architecture
- “AI agent” autonomy where a script, form, or checklist would test the value faster

## Feasibility questions

- What single user action starts the workflow?
- What output would make the user say “yes, this helped”?
- Can the user experience be useful with manual work behind the scenes?
- What data, permissions, integrations, or domain expertise are required?
- What is the biggest engineering unknown?
- What can be replaced with a spreadsheet, script, form, email, or admin panel?
- What would make this impossible in 2–4 weeks?
- What would count as a strong signal after 10 users?

## Manual and fake-door guardrails

- Do not hide material manual fulfilment when it affects trust, price, delivery expectations, safety, or regulated outcomes.
- Do not collect unnecessary sensitive data. Minimize and protect personal, health, financial, legal, employment, child-related, and similarly sensitive information.
- Do not fake endorsements, security claims, compliance status, model accuracy, customer logos, or delivery guarantees.
- For paid pilots or diagnostics, define scope, limitations, cancellation, and what the user receives before money changes hands.
- If the v1 touches regulated or high-risk decisions, include a legal/domain review step before launch.

## Optional HTML artifact

Default to the Markdown chat output below. If the user asks for an artifact, report, visual summary, printable version, or single-file HTML file, also create a standalone `.html` file when filesystem access is available.

For the HTML artifact:

- Use one self-contained file with inline CSS only; do not depend on external assets, fonts, scripts, CDNs, or network access.
- Preserve the same section order, evidence, scores or ratings when present, and recommendations as the Markdown output; do not add new claims for visual polish.
- Design for skimming: title, stage, decision/status badge when applicable, key scores or ratings, tables, callouts for risks, unknowns, and next steps, and a print-friendly layout.
- HTML-escape user-provided text and do not execute or embed user-provided HTML or script.
- Include the source skill name and generation date in small footer text.
- Name the file with the stage and date, such as `startup-v1-feasibility-YYYY-MM-DD.html`.
- In chat, keep a short summary and link to the created HTML file. If file writing is not available, provide the complete HTML in a fenced `html` block.

## Output format

```markdown
## V1 thesis

If we build [small thing] for [specific user] in [specific moment], we will learn whether [riskiest assumption].

## Recommended wedge

Wedge: ...
User: ...
First value delivered: ...
Why this wedge: ...
Founder advantage: ...
Recent enabling change: ...
Distribution route: ...
Expansion path: ...

## Recommended v1 mode

[Concierge / Wizard-of-Oz / Report / Workflow wrapper / Narrow automation / Paid pilot / Diagnostic]

Why: ...

## Smallest useful user journey

1. ...
2. ...
3. ...

## Scope cut

Core job: ...
Must have: ...
Should not have: ...
Manual steps allowed: ...
Fake doors allowed: ...
Human-in-loop required: ...
Data, trust, or compliance risks: ...
First demo flow: ...
Build estimate: ...
Risks: ...

## In scope

- ...

## Out of scope

- ...

## 2–4 week build plan

Include this section only when the v1 evidence gate is credible. If the gate fails, replace this section with `## Not build-ready`.

### Week 1
- ...

### Week 2
- ...

### Optional weeks 3–4
- ...

## Success criteria

- ...

## Kill or rethink criteria

- ...

## Open risks

1. ...
2. ...
3. ...

## Evidence packet update

Stage: V1 scoped
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
Decision gate: [Build v1 / Run more validation / Park / Kill]
Next step: ...
```

When the evidence gate fails, use this shorter output instead:

```markdown
## Not build-ready

Missing evidence:
1. ...
2. ...
3. ...

Next validation move: ...

## Evidence packet update

Stage: V1 blocked
Decision gate: Run more validation
Next step: ...
```

## Pitfalls

- Do not turn v1 into a platform.
- Do not include authentication, billing, teams, dashboards, integrations, or admin tooling unless they are essential to the riskiest test.
- Do not treat “can I build it?” as the only question. The better question is whether the build teaches something commercially useful.
- Do not hide manual fulfilment. Manual is often the fastest way to learn.
- Do not let the v1 absorb every good idea from the grilling step. A wedge wins by being narrow.
