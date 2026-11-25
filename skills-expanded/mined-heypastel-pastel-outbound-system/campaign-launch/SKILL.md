---
name: campaign-launch
description: Launcher — turns approved drafts into Pastel sequences (profile visit, invitation, message once accepted, optional Lemlist push) and reports each run id. Use after the user approves drafts, for "send", "launch", "queue these", or autopilot runs above the minimum priority.
---

# Campaign launch — Launcher

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

What was approved, for whom it was approved — nothing more — and a run id for each.

## Before anything

- **Normal mode:** show who, which steps, and which text — then wait for a yes.
- **Autopilot:** only leads at or above the minimum priority, not off-limits, not already in a run.

## Steps

1. **Can we send?** `pastel_list_capabilities`: `create_sequence` needs `sequences:write` and `engage:write`. `pastel_list_connected_accounts`: at least one account that can send. If either fails, halt and name the missing permission or account.
2. **The right lead:** use the `lead_id` from the lead card. When the user names someone instead, follow *Finding a named lead* in the Pastel tools guide — never an id from a name search — and confirm it with `pastel_get_details`. A lead is unreachable only when a record that *was* found has no LinkedIn profile.
3. **Approved text only:** every invitation and message comes from `message-writer`, passed through `human-voice`. If the lead has no drafts yet, write them with those skills first and show them; never compose new copy inside the launch.
4. **Current action ids:** `pastel_list_sequence_actions` for valid `action_id`, `condition_id`, and branching syntax — never assume them.
5. **No doubles:** `pastel_list_sequence_runs(lead_id=…)`; skip anyone already running.
6. **Build the sequence:**

   | Route (from `reach-check`) | Steps |
   |---|---|
   | `linkedin` | `visit_profile` → next day `send_invitation` (invitation note) → on `accepted_linkedin_invite`, next day `send_message` (opening message) |
   | `linkedin-connected` | `send_message` (opening message) |
   | `lemlist` | the LinkedIn steps above, plus `push_to_lemlist` with the campaign from `outbound-brief.md` |

   No follow-up is written in advance: if there's no answer, `nudge` writes the next touch from the real conversation.
7. **Request** `create_sequence` through `pastel_request_action`, one `idempotency_key` per lead (lead id + today's date), and complete the confirmation step if Pastel asks for one.
8. **Check** each run with `pastel_get_sequence_run` and report its id. Status is _scheduled_ — Pastel spaces the steps within daily limits and working hours. `bypass_daily_limit` stays off.

## Output

```
# Launch — [date]
Normal | Autopilot · Scheduled: n · Already running: n · Held back: n

| Person | Route | Steps | run_id | Status |

Problems:
```

To pause or resume a run later: `pause_sequence` / `resume_sequence` with its run id.
