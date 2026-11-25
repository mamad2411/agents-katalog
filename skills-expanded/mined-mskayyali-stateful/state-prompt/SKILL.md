---
name: state-prompt
description: Rewrite a generic product-design prompt into a paste-ready prompt for one specific Stateful condition or one explicit high-risk composition of lifecycle state, interruption context, surface, and changed-data or dependency condition. Use when generating a screen, component, email, notification, or prototype from an existing map. Do not paste the whole map into a generator or use for non-stateful brand and marketing imagery.
---

# State Prompt

Produce one bounded design-generation prompt from confirmed condition-map content.

## Procedure

1. Read `STATEFUL.md` and `state-map.json` when present.
2. Identify:
   - target lifecycle or failure condition;
   - interruption/re-entry context, if any;
   - target surface;
   - data, time, actor, permission, and dependency facts;
   - acceptance criteria and constraints.
3. If the user has no target, offer three risk-relevant candidates from the map. Do not invent a substitute map.
4. For failures, use cause to frame the response:
   - `user-input`: coaching and correction;
   - `system`: ownership, safe retry, and correlation when useful;
   - `external`: dependency status and alternatives;
   - `policy`: clear rule and permitted next action.
5. Include surface-specific accessibility, freshness, authentication, privacy, and action constraints.
6. Produce one prompt for one condition or explicit composition. Name assumptions separately.
7. Suggest adjacent conditions only after the paste-ready block.

## Output

```text
Condition being generated:
<lifecycle/failure × interruption × surface>

Prompt:
---
<surface and viewport>

Condition:
<what happened and what is true now>

Render and behavior:
- <observable requirement>
- <supported actions and recovery>
- <accessibility, freshness, privacy, and platform constraints>

Acceptance criteria:
- <criterion>

Output:
<single artifact and format>
---

Assumptions:
- <assumption>

Adjacent conditions worth generating:
- <condition>
```

## Failure modes

- A generic prompt with a condition name pasted on.
- Omitting what happened and what is true.
- Including the whole map.
- Losing the target surface.
- Ignoring failure cause or recovery.
- Generating unsupported product decisions.
