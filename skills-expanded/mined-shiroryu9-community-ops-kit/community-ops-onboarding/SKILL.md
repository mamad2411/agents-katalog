---
name: community-ops-onboarding
description: Use when designing, auditing, or improving community newcomer journeys, onboarding questions, welcome flows, first-action prompts, start-here pages, role/access routing, activation checklists, or early retention paths across Discord, forums, Slack, product/customer communities, creator communities, or private groups.
---

# Community Ops Onboarding

Use this skill when the problem is entry, activation, first action, role/access routing, or early retention.

## Project Inputs

Get the relevant community-specific context from the user or an approved source: target newcomer segment, entry source, current welcome/rules/start surfaces, intended first action, roles and access rules, known friction and evidence, and support or safety boundaries. Unknown fields may remain data gaps during diagnosis.

The skill supplies the path-design method. It does not supply channel names, role names, permission rules, age/content policies, product steps, or activation data. Do not inherit those values from examples or another community. Ask only for missing context that changes the diagnosis, access safety, or proposed first action.

## First Move

Map the newcomer path:

```text
discovery -> entry -> identity/intent -> first action -> feedback/help -> second action
```

Do not start by rewriting welcome copy. First find where the path breaks.

## Surface Jobs

Assign one job to each surface:

- invite / landing page: set expectation;
- onboarding questions: segment and route safely;
- rules: define boundaries;
- welcome / start-here: give one first action;
- guide / pinned post: explain details;
- first activity or checklist: create participation;
- support path: handle confusion or access problems.

Avoid making every surface repeat every CTA.

## Output Pattern

```md
**Diagnosis**
[Where newcomers currently get stuck.]

**Newcomer Segments**
| Segment | Need | First action | Risk |
|---|---|---|---|

**Path**
1. Entry: ...
2. Intent/role routing: ...
3. First action: ...
4. Feedback/help: ...
5. Second action: ...

**Surface Changes**
| Surface | Current issue | Change | Owner gate |
|---|---|---|---|

**Activation Evidence**
- onboarding completion;
- first post/comment/submission;
- first product/account action;
- support questions reduced;
- day 1 / day 7 return signal if available.
```

## Guardrails

Preserve access, roles, age/content boundaries, paid permissions, and safety gates. Require explicit confirmation before changing public onboarding surfaces, roles, access, channels, or permissions. Do not copy one community's role names or adult-content rules into another. If exact permissions are unknown, mark them as data gaps.

Keep welcome copy short and give newcomers one clear first action before optional detail.
