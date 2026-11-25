---
name: service-blueprint
description: Map how a service is delivered across five swim lanes — physical evidence, user actions, frontstage, backstage and support processes — with the line of interaction, line of visibility and line of internal interaction, then read the map for gaps, fragility and automation candidates. Use when staff or operations are part of the experience, or when a multi-channel service needs a coordination artifact.
license: MIT license
category: docs
metadata: {"version": "1.0", "skill-author": "MC Dean (designer-skills)"}
---

# Service Blueprint

Map the whole delivery system, not just the user-facing touchpoints, so teams see where a service
promises more than it can deliver. 中文触发：服务蓝图、前后台流程、多渠道服务设计、运营断点。

## What a blueprint shows

Five horizontal swim lanes:

1. **Physical evidence** — what the user sees, touches or receives at each step (screens, emails,
   receipts, packaging, physical space)
2. **User actions** — what the user does (adapt from journey-map research)
3. **Frontstage actions** — what employees or systems do that the user can see (support replies,
   onboarding calls, chat responses)
4. **Backstage actions** — what employees or systems do that the user cannot see (order processing,
   fraud checks, fulfilment)
5. **Support processes** — the infrastructure enabling the two lanes above (databases, third-party
   services, internal tools, policies)

Three separators:
- **Line of interaction** — between user actions and frontstage
- **Line of visibility** — between frontstage and backstage
- **Line of internal interaction** — between backstage and support processes

## When to use it
- Designing a new end-to-end service
- Diagnosing where a service fails (gaps between swim lanes)
- Coordinating a multi-team product spanning channels (web, app, email, phone, physical)
- Planning a major service redesign or migration
- Onboarding people to the full scope of a product

## Blueprint vs journey map

| | Journey map | Service blueprint |
|---|---|---|
| Focus | user experience | the whole delivery system |
| Actors | user | user + employees + systems |
| Purpose | understand the emotional journey | reveal operational gaps and dependencies |
| When | research and ideation | system design and coordination |

## Process

1. **Define scope** — one scenario ("first-time user completes onboarding"), never the whole product
2. **Gather inputs** — journey research, stakeholder interviews, process documentation, analytics
3. **Draft user actions** — adapted from the journey map
4. **Map frontstage** — for each user action, what does the team or system do visibly?
5. **Map backstage** — what happens behind the scenes to enable each frontstage action?
6. **Map support** — which infrastructure, tools or third parties enable the backstage actions?
7. **Add physical evidence** — which artefacts does the user receive or interact with?
8. **Identify failure points** — where do lanes disconnect; where do delays, errors or handoffs break?
9. **Validate** — review with operations, engineering and support; they spot missing backstage steps

## Reading the blueprint

- **Gaps between lanes** — frontstage promises something backstage cannot deliver
- **Dense backstage clusters** — complexity that is a candidate for automation or simplification
- **Several support dependencies for one frontstage action** — fragility, single points of failure
- **Long stretches with no user touchpoint** — the user is waiting; is that communicated?

## Working rules
- Blueprint the as-is state first, the future state second
- Co-create with operational teams, not design alone — they know the backstage
- Keep scope narrow: one focused scenario beats a sprawling map of everything
- Use it as a coordination artefact in cross-functional planning, not only as a research output
- Revisit it when the service changes; it goes stale faster than a journey map
