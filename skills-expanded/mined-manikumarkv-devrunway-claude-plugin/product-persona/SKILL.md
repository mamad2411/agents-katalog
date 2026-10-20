---
name: product-persona
description: Product persona and requirements standards — persona template, user story format, acceptance criteria, definition of done. Load when creating personas, writing stories, or defining requirements.
user-invocable: false
---

Full template in [persona.md](persona.md). Always-on summary:

**Persona fields:** Name, Role/Job title, Goals (3 bullets), Pain points (3 bullets), Tech comfort, Usage context (device, frequency, environment).

**User story format:**
```
As a <persona name>,
I want to <action>,
so that <outcome/value>.
```

**Acceptance criteria (Gherkin):**
```
Given <precondition>
When <action>
Then <expected result>
```

**Definition of done (every story):**
- [ ] AC met and demo-able
- [ ] Unit tests written, coverage ≥ 80%
- [ ] Accessibility: keyboard navigable, screen reader tested
- [ ] Mobile responsive
- [ ] No console errors
- [ ] PR approved and merged to develop


**Related skills — apply together:**
- `accessibility` — definition of done includes keyboard navigable and screen reader tested
- `testing-standards` — acceptance criteria map directly to test cases
- `playwright` — E2E specs validate the critical user journeys defined in stories