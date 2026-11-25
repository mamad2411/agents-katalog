---
name: gym-member-onboarding-flow
description: "Run trial booking, body metrics logging, and closing-meeting coordination for new gym members in Arbox"
---

# Gym Member Onboarding Flow

## Purpose

Guide **stage-3 studio onboarding**: trial class → weigh-in / body metrics → closing meeting → handoff to nutrition delivery.

## When to Use

- After a prospect agrees to a trial.
- At weigh-in or body-composition sessions.
- When scheduling the membership closing meeting.

## When NOT to Use

- Cold lead prioritization (use **gym-sales-daily-prioritization**).
- Nutrition menu build (use **gym-nutrition-menu-delivery**).

## Expected Outcome

- Trial booked in Arbox, metrics logged, closing meeting scheduled, status advanced per **gym-arbox-status-playbook**.

## Workflow

```
Trial class → Weigh-in / body fat → Closing meeting → Nutrition handoff
```

1. **Trial**: find slot with **`arbox_get_schedule`**; book with **`POST /v3/schedule/booking/trial`** `{ user_id, schedule_id }`.
2. **After trial**: move status toward the tenant’s “measurements / tracking” stage when appropriate.
3. **Measurements**: log via **`POST /v3/users/createNote`** (weight kg, body fat %). Prefer **`PATCH /v3/users`** customFields when the platform exposes patch support.
4. **Closing meeting**: create **Google Calendar** event when connected; set closing-meeting status with comment including date/time.
5. **Handoff**: dispatch or notify the nutrition-delivery role — do not build menus here unless asked.

## No-shows

- Reschedule trial before creating duplicate leads.
- Log no-show on workboard + Arbox note; use **member-retention-and-experience** for win-back framing.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| Arbox + Calendar | Full flow |
| Arbox only | Book trial, log notes, skip calendar holds |
| Read-only | Plan only |

### Related tool sets

- `arbox`
- `google-calendar`
