---
name: blameless-postmortem-and-root-cause-analysis
description: >
  Guides running a blameless postmortem after an incident — using a
  consistent template (timeline, impact, root cause, contributing
  factors, action items), facilitating without assigning individual
  blame, applying 5-whys/contributing-factor analysis without
  oversimplifying to one root cause, and tracking action items through
  to completion. Use when a user asks to "write a postmortem", "run a
  root-cause analysis", "do a 5-whys on this incident", "make sure this
  incident doesn't get blamed on one person", or "our postmortem action
  items never actually get done."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: site-reliability-engineering
  maturity: stable
---

# Blameless Postmortem and Root Cause Analysis

## Purpose

How an organization writes up its incidents determines whether the next
one gets caught early or hidden until it's worse: a postmortem that names
and blames an individual ("Jane forgot to update the config") teaches
everyone watching that reporting a mistake, a near-miss, or an honest
uncertainty is personally risky — so people quietly stop doing it, and
the organization loses its best source of information about where the
system is actually fragile. A blameless postmortem treats the incident as
evidence about the *system* (its defenses, its defaults, its blind spots)
rather than a verdict on a person, while still producing concrete,
owned, tracked action items — "blameless" is not the same as
"consequence-free" or "toothless." This skill covers the postmortem
template, facilitation practices that keep the discussion blameless
without becoming vague, contributing-factor analysis that resists
collapsing a multi-cause incident into one scapegoat cause, and making
sure action items actually get done instead of accumulating in a backlog
nobody revisits.

## When to use

- After any Sev1/Sev2 incident is resolved and stood down (see
  [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md)).
- An error budget was exhausted (see
  [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md))
  and the policy mandates a postmortem before launches can resume.
- A near-miss occurred — no customer impact, but the system was one step
  away from a real incident — and the team wants to capture the lesson
  before it's forgotten.
- Facilitating a postmortem discussion that's at risk of turning into
  blame ("who pushed that change") instead of systems analysis.
- Reviewing why past postmortem action items never got implemented and a
  similar incident just recurred.

## Prerequisites & environment

- A collected incident record: the scribe's live timeline, relevant
  dashboards/logs, and the incident chat transcript (see
  [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md)
  for how this is captured during the incident itself).
- A shared, versioned template — see
  [references/postmortem-template.md](references/postmortem-template.md)
  in this skill for a ready-to-use starting point.
- An issue tracker (Jira, GitHub Issues, Linear, or equivalent) to hold
  action items as real, assignable, trackable tickets rather than bullet
  points in a document.
- An explicit, stated organizational policy that postmortems are
  blameless — ideally signed off by leadership, since the practice only
  works if people trust in advance that writing an honest account won't
  be used against them individually.
- A facilitator who was not the primary hands-on responder for the
  incident, where staffing allows.

## Step-by-step guidance

1. **Schedule the postmortem within 48-72 hours** of stand-down — soon
   enough that details are fresh, but after acute firefighting has
   stopped so people can think clearly rather than react.

2. **Fill out the template** (see
   [references/postmortem-template.md](references/postmortem-template.md)):
   Summary, Impact, Timeline (UTC timestamps), Root cause, Contributing
   factors, What went well, What went poorly, Where we got lucky, Action
   items (owner + ticket + due date), Lessons. Draft it from the scribe's
   live timeline rather than reconstructing from memory in the meeting.

3. **Facilitate blamelessly, explicitly:**
   - State ground rules at the start of the review meeting: assume good
     intent, focus on "what about the system allowed this," not "who."
   - Rewrite blame-shaped language during the discussion in real time —
     "X forgot to validate the config" becomes "the deploy pipeline had
     no automated step that validated the config before it reached
     production."
   - The facilitator should be someone other than the person most
     centrally involved in causing or fixing the incident, so the
     discussion isn't steered (even unintentionally) by someone with a
     personal stake in a particular narrative.

4. **Run contributing-factor analysis, not single-root-cause analysis.**
   Use 5-whys as a *starting* technique, but explicitly resist stopping
   at the first answer that sounds like "human error":
   ```
   Why did checkout fail?              → A bad config reached production.
   Why did the bad config reach prod?  → No validation step in the pipeline.
   Why was there no validation step?   → It was deprioritized after the
                                          last incident's action item stalled.
   Why did the action item stall?      → No owner/due date was assigned.
   Why was staging traffic too low to
     catch this before prod?           → Staging doesn't mirror production
                                          request volume/shape.
   ```
   Notice this produced *four* independent contributing factors (missing
   validation, a stalled prior action item, no owner/due-date discipline,
   unrepresentative staging) — not one. Stopping after the first "why"
   ("an engineer pushed a bad config") would have produced a single,
   person-shaped "root cause" and missed the systemic gaps that let it
   through and recur.

5. **Categorize each action item** by what it does: *prevent recurrence*
   (fix the proximate cause), *detect faster* (alerting/monitoring gap),
   *reduce impact* (blast-radius/rollback speed), or *process
   improvement* (the meta-level gaps, like the stalled action item
   above). Assign exactly one owner, a tracked ticket, and a due date to
   each — an action item with none of these three will not get done.

6. **Publish broadly and review in a recurring forum.** Post the
   finished postmortem somewhere the whole engineering org can find it
   (internal wiki/doc index), and bring it to a standing "incident
   review" meeting rather than letting it live only in the team that
   experienced it — patterns across teams are often invisible from
   inside a single team's postmortems.

7. **Track action item completion as a program metric.** Report the
   percentage of action items closed within their due date across all
   postmortems on a recurring cadence; escalate stale items instead of
   letting them silently age out. Chronic manual/undone action items are
   a strong signal for the
   [toil-reduction-and-operational-automation](../toil-reduction-and-operational-automation/SKILL.md)
   prioritization framework — many action items are, in effect,
   automation candidates.

8. **If the postmortem was triggered by error-budget exhaustion**, feed
   the finished document back into the
   [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md)
   policy review — leadership sign-off to resume feature launches should
   reference the actual postmortem, not just the calendar.

## Best practices

- "Blameless" means no individual is punished for an honest mistake —
  it does not mean no accountability: every action item still needs a
  named, responsible owner and a deadline.
- Write for a reader who wasn't in the room and doesn't have the
  incident's context — precise UTC timestamps, full service names, no
  inside jokes or unexplained acronyms.
- Publish postmortems for near-misses too, not only incidents that
  paged someone — a near-miss caught before customer impact is the
  cheapest possible lesson.
- Track "time from stand-down to published postmortem" and "% of action
  items closed by their due date" as the two headline health metrics of
  the postmortem program itself.
- Explicitly look for at least two to three independent contributing
  factors before considering the analysis complete — if the discussion
  converges on a single cause quickly, that's usually a sign the
  analysis stopped too early, not that the incident was simple.
- Revisit old postmortems periodically when a new, similar incident
  occurs — a recurrence is direct evidence that either the action items
  weren't implemented or didn't address the real contributing factors.

## Common pitfalls

- **Symptom:** The postmortem draft reads "Jane forgot to update the
  feature flag before the migration," and afterward people are visibly
  more reluctant to volunteer details in incident channels.
  **Fix:** Rewrite in systems language before publishing — describe what
  about the process/tooling allowed the mistake to reach production
  undetected, and have the facilitator explicitly screen drafts for
  named blame before the review meeting.

- **Symptom:** 5-whys stops after one iteration at "the engineer ran the
  wrong command," and three months later a near-identical incident
  happens from a different engineer running a different wrong command.
  **Fix:** Require identifying at least two to three independent
  contributing factors (missing confirmation prompt, no staging parity,
  no peer review on the command) rather than accepting the first
  human-shaped answer as sufficient.

- **Symptom:** A quarterly review of past postmortems shows most action
  items are still open, several past their due date by months, with no
  visible follow-up.
  **Fix:** Every action item needs an owner, a real tracked ticket, and a
  due date at creation time (not "someone should look into this"), plus
  a recurring review that reports the closure rate and escalates stale
  items — don't let the postmortem document itself be the only place the
  action item lives.

- **Symptom:** A well-written postmortem is finished, reviewed once by
  the immediate team, and never looked at again — six months later a
  different team hits the exact same failure mode.
  **Fix:** Publish to a shared, searchable location and bring it to a
  cross-team recurring incident-review forum, not just the originating
  team's internal channel.

- **Symptom:** The postmortem meeting is scheduled two weeks after the
  incident, and the discussion spends most of its time arguing about
  what order things happened in.
  **Fix:** Schedule within 48-72 hours while memory is fresh, and draft
  the timeline from the scribe's live incident-channel log (captured
  during the incident itself) rather than reconstructing it from
  memory in the meeting.

## Worked example

Using [references/postmortem-template.md](references/postmortem-template.md)
for the `payments-api` checkout outage from the incident-response
worked example:

- **Summary:** A config change in `payments-api` v2.14.0 caused checkout
  requests to fail for all customers for ~20 minutes; resolved via
  rollback.
- **Impact:** 100% of checkout traffic affected for 20 minutes (14:05-
  14:22 UTC); ~38 minutes of the service's 30-day error budget consumed
  in a single incident.
- **Root cause:** A feature-flag default was flipped in the same deploy
  as an unrelated dependency bump, disabling the fraud-check bypass path
  for a payment provider that required it.
- **Contributing factors:** (1) no automated check that flags a
  feature-flag default change in a diff not explicitly labeled as a flag
  change; (2) staging traffic volume too low to exercise that payment
  provider's code path before the change reached production; (3) the
  fast-burn SLO alert existed but had no corresponding auto-abort wired
  into the deploy pipeline, so recovery depended on a human noticing and
  rolling back manually.
- **Action items:** add a CI diff-check that flags feature-flag default
  changes (owner, ticket, due date); add synthetic staging traffic for
  that payment provider's path (owner, ticket, due date); wire the
  fast-burn alert to an automatic deploy rollback trigger, not just a
  page (owner, ticket, due date).
- **Outcome:** the postmortem is published to the internal wiki, brought
  to the monthly cross-team incident review, and the error-budget freeze
  from
  [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md)
  is lifted only after the VP confirms the three action items have
  tracked tickets with owners and due dates.

## Cross-references

- [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md) — the scribe's live timeline and severity classification captured during the incident are the raw input to this postmortem.
- [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md) — error-budget exhaustion should trigger a mandatory postmortem, and the finished document feeds the leadership sign-off to lift a launch freeze.
- [toil-reduction-and-operational-automation](../toil-reduction-and-operational-automation/SKILL.md) — recurring manual-fix action items across postmortems are strong candidates for the toil-prioritization framework.
- [chaos-engineering-and-resilience-testing](../chaos-engineering-and-resilience-testing/SKILL.md) — findings from a broken chaos experiment should be run through this same action-item process rather than logged and forgotten.
