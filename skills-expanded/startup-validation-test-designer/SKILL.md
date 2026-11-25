---
name: startup-validation-test-designer
description: Design small credible demand tests, interviews, smoke tests, and kill criteria before building a startup v1, with optional formatted single-file HTML artifact output.
license: MIT
metadata:
  display_name: Startup Validation Test Designer
  hermes:
    tags: [startup, validation, customer-interviews, smoke-tests, demand-testing]
    category: business
    requires_toolsets: []
---

# Startup Validation Test Designer

## When to use

Use after a startup problem has been captured and grilled, especially when the next question is “how do I test this before building?”

This skill designs the smallest credible validation test. It should produce evidence from real people, not compliments about an idea.

## Core rule

Test the riskiest assumption first. Prefer interviews, targeted outreach, paid audits, manual services, landing pages, fake doors, demo videos, and concierge delivery before building full software.

## Inputs to request if missing

```markdown
Problem:
Target user:
Likely buyer:
Current workaround:
Riskiest assumption:
What the user can build or deliver manually:
Existing network or channels:
Founder advantage:
Recent enabling change:
Distribution route:
```

## Workflow

1. Identify the riskiest assumption.
2. Choose the fastest credible test type.
3. Define the exact behaviour that would count as evidence.
4. Write non-leading interview questions if interviews are part of the test.
5. Define the target list and outreach angle.
6. Tie the test to why the problem is urgent or newly solvable now.
7. Set success, failure, and kill criteria before the test runs.
8. Keep the test timeboxed. Default to 48 hours to 2 weeks.
9. End with a clear evidence gate for whether v1 scoping is justified after the test.

## Test types

Choose one or combine a small number:

- Customer interview: learn workflow, cost, workaround, urgency, budget, and objections.
- Direct outreach: test whether a narrow ICP responds to the pain statement.
- Landing page: test whether people understand and take a specific action.
- Fake door: measure clicks or requests for a specific capability.
- Demo video: test whether the promised workflow is compelling.
- Paid audit: sell a manual diagnostic or review before SaaS exists.
- Manual service: deliver the outcome by hand for a few users.
- Concierge/Wizard-of-Oz prototype: give a product-like experience with manual fulfilment.
- Prototype: build only when behaviour cannot be tested another way.

## Non-leading interview questions

Prefer questions about the past and current workflow:

1. Walk me through the last time this happened.
2. What triggered the issue?
3. Who was involved?
4. How long did it take?
5. What happened when it went wrong or took too long?
6. What tools or processes did you use?
7. Have you tried to fix this before?
8. Who owns this process?
9. Is there existing budget or spend around this?
10. What would make this urgent enough to change?

Block weak questions such as:

- Would you use this?
- Would you pay for this?
- Do you like my idea?
- Would this be useful?

## Outreach design

When designing outreach, include:

```markdown
First 10–20 targets:
Where to find them:
Message angle:
Specific ask:
Why they might care now:
Follow-up plan:
```

Keep outreach focused on the pain, not the imagined product.

## Ethics, privacy, and sensitive-domain guardrails

- Do not design deceptive tests. A fake door can test demand, but it must not claim a product, credential, endorsement, price, or delivery date that is not real.
- Collect the minimum data needed to answer the validation question. Avoid unnecessary personal, health, financial, legal, employment, child-related, or similarly sensitive data.
- Get permission before recording calls, using quotes, or sharing identifiable customer details.
- For paid audits, manual services, pilots, and concierge tests, make the scope, human involvement, limitations, and refund or cancellation terms clear.
- For regulated or high-risk domains, include a risk check and recommend domain/legal review before outreach, data collection, or paid testing.

## Optional HTML artifact

Default to the Markdown chat output below. If the user asks for an artifact, report, visual summary, printable version, or single-file HTML file, also create a standalone `.html` file when filesystem access is available.

For the HTML artifact:

- Use one self-contained file with inline CSS only; do not depend on external assets, fonts, scripts, CDNs, or network access.
- Preserve the same section order, evidence, scores or ratings when present, and recommendations as the Markdown output; do not add new claims for visual polish.
- Design for skimming: title, stage, decision/status badge when applicable, key scores or ratings, tables, callouts for risks, unknowns, and next steps, and a print-friendly layout.
- HTML-escape user-provided text and do not execute or embed user-provided HTML or script.
- Include the source skill name and generation date in small footer text.
- Name the file with the stage and date, such as `startup-validation-test-YYYY-MM-DD.html`.
- In chat, keep a short summary and link to the created HTML file. If file writing is not available, provide the complete HTML in a fenced `html` block.

## Output format

```markdown
## Riskiest assumption

...

## Recommended test

Test type: [interviews / direct outreach / landing page / fake door / demo video / paid audit / manual service / concierge prototype]

Why this test: ...

## Hypothesis

People will [do specific behaviour] because [pain/current cost].

Why now: ...

## Target users

- ...

## Test setup

Assets needed:
- ...

Timebox: ...

## Interview questions

Include this section only when interviews are part of the recommended test.

1. ...
2. ...
3. ...

## Test asset or script

Include this section only when the recommended test needs a landing-page message, fake-door copy, demo-video outline, audit offer, manual-service script, or concierge workflow.

...

## Outreach angle

...

Distribution route: ...

## Success criteria

Proceed if:
- ...

## Kill or rethink criteria

Kill/rethink if:
- ...

## What to record

- Exact quotes
- Current workaround
- Frequency
- Cost
- Buyer/budget signal
- Behavioural commitment
- Why-now signal
- Objections
- Follow-up commitment

## Evidence packet update

Stage: Validation test designed
Problem statement: ...
Target user: ...
Buyer / budget owner: ...
Current workaround: ...
Founder advantage: ...
Recent enabling change: ...
Distribution route: ...
Expansion path: ...
Evidence to collect: ...
Weakest assumptions: ...
Decision gate: [Ready to run test / Needs narrower test / Park]
V1 gate: Do not scope a build until the test produces the success criteria above.
Next step: ...
```

## Strong signals

- Repeated pain across 5+ conversations.
- Clear budget owner.
- Existing spend or ugly workaround.
- A buyer asks when they can try it.
- Someone accepts a paid audit, paid pilot, or manual service.
- The user can name and reach the next 10 prospects.

## Weak signals

- People say “that sounds useful” but will not take a next step.
- The pain is real but rare.
- The user is not the buyer and cannot introduce the buyer.
- Nobody has tried to solve it manually.
- The test only proves curiosity, not intent.

## Pitfalls

- Do not design tests that require a full build unless no cheaper test can answer the risk.
- Do not ask for compliments.
- Do not count friends being polite as validation.
- Do not use vanity metrics where a behavioural signal is possible.
- Do not proceed without explicit pass/fail criteria.
