---
name: habit-loop
description: >-
  Design the return loop for a product: trigger, action, variable reward and
  investment, mapped to the product's real calendar (for a sports product:
  race weekends, qualifying, results, off weeks). Produces the notification
  plan with frequency caps and quiet hours, streak rules, and the analytics
  events for every step (entry, success, failure, drop-out). Trigger on
  "retention", "why don't people come back", "habit loop", "notification
  plan", "design streaks", "engagement loop", "make it sticky", or when
  planning push notifications or email cadence.
---

# Habit loop

**Product name.** `{{app}}` here and in the references stands for the user's product. Take its name from the project (README title, package.json, app.json, Info.plist) or ask once, then write every example with that name and the product's own screens.

People come back when something they care about is about to happen or just
happened, and the product is the fastest way to see it. The loop is built on
the product's real calendar, not on an arbitrary daily cadence. A daily
streak on a product with a weekly event teaches users to fail six days a
week.

## Step 1: the calendar

List the moments that exist whether or not the product does, with their
typical local time for the user and how often they occur.

{{app}} example (per race weekend, about 24 a season, some double-header
weekends back to back, gaps of 1 to 4 weeks between):

| Moment | When | Why users care |
|--------|------|----------------|
| Weekend preview | Thursday | Plans, fantasy picks, bets |
| Practice data | Friday | First signal of pace |
| Qualifying | Saturday (Friday on sprint weekends) | Sets the grid |
| Race start | Sunday | The main event |
| Results | Sunday, after the flag | Was the prediction right |
| Off week | No race | Nothing happens; the product must not pretend it does |

For a non-sports product the calendar is the user's own rhythm: paydays,
Monday planning, month end, a class schedule. If there is no real rhythm,
say so; the loop then keys off the user's own last action.

## Step 2: the four parts, per calendar moment

For each moment worth a loop, fill all four. A part left empty is where the
loop leaks.

1. **Trigger**. External (notification, email, widget, Live Activity) or
   internal (the user already wonders "who will win"). External triggers
   fade in value; the goal is to attach the product to the internal one.
2. **Action**. The smallest thing the user does to get the reward: open the
   prediction, tap a driver, make their own pick. One tap from the trigger.
3. **Variable reward**. Something not fully known in advance: how their pick
   compared, a surprising probability shift after practice, the model's
   verdict against the actual result. Rewards of the hunt (new information),
   the tribe (how friends picked), the self (their own accuracy improving).
4. **Investment**. Something the user puts in that makes the next loop
   better: following drivers, their own picks history, notification
   preferences, a league with friends. Investment is what makes leaving
   costly in a fair way: they would lose their own history, not be punished.

Write each loop as one row: moment, trigger, action, reward, investment,
event names.

## Step 3: the notification plan

Rules that hold for every product:

- **Opt-in with a reason**, asked at the moment the reason is obvious
  ("Get a note before qualifying?" after they open a qualifying prediction),
  never on first launch.
- **Frequency caps**, per user and enforced server side: a default ceiling
  per calendar unit, a lower one for users who have not opened the last
  three. {{app}} default: at most 3 per race weekend, at most 1 in an off
  week, 0 in an off week for users who opted only into session alerts.
- **Quiet hours** in the user's local time zone: default 22:00 to 08:00. A
  session that starts inside quiet hours gets its alert in the evening
  before, not at 04:00, unless the user explicitly opted in to live alerts.
- **Time zones**: schedule in the user's zone from the event's UTC time.
  Never send a notification written for another zone ("tonight" at 09:00).
- **Every notification carries value in the text itself**: the prediction,
  not "New prediction available".
- **Back-off**: three ignored in a row halves the frequency; six ignored
  pauses non-essential sends and says so in settings.
- **Channels per type**, each with its own toggle: session alerts, results,
  weekly digest, product news. Product news is off by default.

Full template with example copy is in `references/notification-plan.md`.

## Step 4: streaks, fairly

- Count in the calendar's unit: race weekends, not days.
- Off weeks do not break a streak. Missing one weekend uses a free "pit
  stop" (one per N weekends), shown before it is needed.
- Show the streak where the user already looks; do not send notifications
  that exist only to protect a streak.
- Never threaten loss ("You will lose your 12-weekend streak!"), never sell
  streak repair. Those belong to the forbidden list in `paywall-and-pricing`.
- Reward accuracy or learning, not only presence, when the product allows
  it: "Your picks beat the model in 4 of the last 6 races."

## Step 5: analytics for every step

Every step in every loop reports entry, success, failure and drop-out, with
the loop and the calendar moment as properties. Use the project's taxonomy;
the shape below is the default.

- Trigger: `notif_scheduled`, `notif_sent`, `notif_suppressed{reason:
  cap|quiet_hours|opt_out|backoff}`, `notif_failed{reason}`, `notif_open`
- Action: `loop_entry{loop, moment, source}`, `loop_action{loop, action}`
- Reward: `loop_reward_view{loop, reward_type}`
- Investment: `loop_invest{loop, kind: follow|pick|league|prefs}`
- Drop-out: `loop_abandon{loop, last_step}`; `notif_opt_out{channel}`
- Streak: `streak_extend{length}`, `streak_saved{length}`,
  `streak_break{length}`

Metrics: weekly active users measured per calendar unit (race weekend
actives), share of users returning for the next moment, notification open
rate by type, opt-out rate per 100 sends (the guardrail), D30 retention by
whether the user invested in week one.

## Output

1. The calendar table.
2. One row per loop with all four parts and the event names.
3. The notification plan: types, default on or off, caps, quiet hours, copy
   for each, back-off rule.
4. Streak rules.
5. The event list, then **Open questions** (data the loop needs that does
   not exist yet, platform limits such as iOS provisional authorization or
   Live Activity update budgets).

Hand the copy to the `ux-copy` skill before it ships. Loops that the owner
has not approved stay a design; do not implement them.
