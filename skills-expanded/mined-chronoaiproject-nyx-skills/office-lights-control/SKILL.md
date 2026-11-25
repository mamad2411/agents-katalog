---
name: office-lights-control
description: Turn the office wall lights on or off via two pre-registered aevatar scope workflows (office_lights_on / office_lights_off). Each asserts the on/off state of the 10 office wall-switch lights (Corridor, Front/Mid Reception, Coworking ceiling; Dubai Room excluded) through the NyxID-brokered home-assistant service. Use whenever the user wants to switch the office lights on or off.
version: "1.0"
metadata:
  category: tool-based
  tool-list:
    - aevatar_start_workflow
  tags:
    - home-assistant
    - office
    - lights
    - switch
    - workflow
---

# Office Lights Control

Turn the office wall lights on or off by starting one of two **pre-registered scope workflows**. Each workflow is idempotent (it asserts the desired state rather than toggling) and drives exactly 10 `switch.*` wall-light entities; it never touches camera / motion / recording switches.

> The two workflows are registered as **persistent scope workflow definitions**, so they resolve immediately. This skill does NOT bundle or mount workflows on each call — that avoids the mount→catalog propagation race that previously made the first call fail with `workflownotfound`.

## When to use → which workflow

- Turn lights **ON** ("开灯" / "开办公室的灯" / "把灯打开") → `aevatar_start_workflow { "workflow_id": "office_lights_on" }`
- Turn lights **OFF** ("关灯" / "关办公室的灯" / "把灯关掉") → `aevatar_start_workflow { "workflow_id": "office_lights_off" }`

No inputs are required; the entity list is fixed inside each workflow. The run returns the Home Assistant response describing which switches changed.

## Rules (important — follow exactly)

1. Start **exactly one** workflow that matches the user's intent.
2. **Never substitute the opposite action.** If the user asks to turn the lights ON, only ever start `office_lights_on` — never start `office_lights_off` as a fallback, and vice-versa. Turning the lights the wrong way is worse than doing nothing.
3. If `aevatar_start_workflow` returns `workflownotfound` (or any error), do **not** switch to the other workflow and do **not** claim success. Report that the workflow could not be started and suggest retrying shortly.
4. Report the actual outcome truthfully. Only say the lights were turned on/off if the start succeeded.

## What it controls (10 wall-switch lights)

- Corridor: back / front / world-map-bottom
- Front Reception: front / seat / world-map-center
- Mid Reception: mid / window / world-map-top
- Coworking Table: ceiling light

(Dubai Room lights are intentionally excluded.)

## Notes

- Daily schedules (on at 09:00, off at 18:30 Asia/Shanghai) run against the same two workflows and are configured separately; this skill is the on-demand control surface.
