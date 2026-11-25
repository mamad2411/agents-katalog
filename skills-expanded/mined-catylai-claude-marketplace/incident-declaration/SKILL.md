---
name: incident-declaration
description: "Declares an incident at confirmed production impact, before root cause, and runs it to close-out. Use when prod is degraded or someone asks 'is this an incident?'. Not for postmortems (use ops-workflows:incident-postmortem); not for vendor calls (use datadog-observability:*, gcp-observability:*)."
license: MIT
---

# Incident Declaration

Open the incident record the moment production impact is confirmed, with nothing but the
symptom, and amend it as evidence arrives. Root cause and the fix come later.

Declaring early is cheap and reversible: an incident opened on a symptom that turns out benign
is downgraded and closed in a minute. Declaring late cannot be undone. The minutes between "we
noticed" and "we declared" are minutes in which nobody else could help, nobody was paged and no
timeline was kept.

The usual failure is momentum, not laziness. An engineer confirms impact, forms a hypothesis and
starts investigating, and the investigation absorbs all the attention. The diagnosis comes out
sound and the record of the event barely survives the session. So:

- Put a diagnosis in the incident record first, then in chat, tickets or summaries, so the
  record stays the source everyone else reads.
- File a work item for the fix and keep the incident as well. The item records the fix; the
  incident records the event (detection, what was tried, when impact started and stopped). A
  production defect gets both.

## Before you start

Read the `## Observability capabilities` section of the project's `CLAUDE.md` for the incident
record, comms channel and work tracker. If it is missing, ask for those three in one question
and continue; `references/capabilities.md` has the section template to offer afterwards.

## Step 1: Apply the confirmation test

Declare when any of these is true:

- A user-facing request path is failing, hanging or returning wrong results.
- An error rate, latency percentile or success-rate metric has crossed its alert threshold and a
  person has confirmed the signal is real.
- Data is being lost, duplicated or written incorrectly.
- A security-relevant control has failed open.
- You are about to tell someone outside the team that production is broken.

If you are debating whether it qualifies, declare at Sev4 and adjust. The debate costs more than
the declaration.

## Step 2: Set severity from the measured population

Severity answers how badly users are hurt right now. Measure first with the `blast-radius`
skill, then read severity off this table. The cause does not move severity: a config typo and a
deep race condition get the same severity when they break the same number of users, because the
cause decides the fix, not the response.

| Sev | Customer impact | Response posture |
|-----|-----------------|------------------|
| Sev1 | Core function unusable for most users, or any confirmed data loss or security exposure. No workaround. | Page immediately, around the clock. All hands. Continuous comms. |
| Sev2 | Core function broken for a significant subset (a region, a tenant tier, a major feature), or severe degradation for most. Painful workaround. | Page in and out of hours. Dedicated responders. Regular comms. |
| Sev3 | Narrow or intermittent impact: a secondary feature, a small tenant set, or degradation users can route around. | Business-hours response. Named owner. Update on change. |
| Sev4 | No current customer impact: a near-miss, internal-only breakage, or a control that failed silently and was caught. | Normal schedule. Record it so it is not forgotten. |

Severity is a live field. Re-evaluate it when the blast-radius number moves, when a mitigation
lands, or when a new affected population turns up. Raising it late is normal and is recorded in
the severity history, not treated as an error.

## Step 3: Name the roles

Assign each role to a named person at declaration. On a small incident one person may hold
several; say which.

- **Incident Commander (IC).** Owns the response, not the fix: severity, assignments,
  checkpoints, escalation, and the call to move state. An IC who starts debugging hands the role
  over, because nobody is then watching the whole incident.
- **Operations.** Investigate and ship changes, reporting findings to the IC and telling the IC
  before any mitigation ships.
- **Communications lead.** Owns stakeholder and customer updates on the cadence below, so
  responders are not switching context to write status posts.
- **Scribe.** Keeps the timeline as events happen: detection, each hypothesis, each action and
  its observed effect. A timeline rebuilt from chat afterwards loses what people believed at the
  time, which is the part a postmortem needs.

## Step 4: Post the declaration and keep the cadence

Use this template for the declaration and for every update. The first update is the
declaration. Write times in UTC.

```markdown
**Incident:** <short symptom, e.g. "Checkout failing in eu-west">
**State:** <declared | mitigated | resolved | closed>
**Severity:** <Sev1 | Sev2 | Sev3 | Sev4>. History: <e.g. "Sev3 at 14:02, Sev2 at 14:20 (EU tenants affected)">
**Declared:** <time>   **Impact start:** <time, or unknown>   **Detected by:** <alert | customer report | engineer | other: …>
**Roles:** IC <name> · Operations <names> · Comms <name> · Scribe <name> (write `unassigned` for an empty role)

### Update <n>: <time>
- **Impact:** <current numbers; paste the blast-radius block from the blast-radius skill>
- **Known:** <confirmed facts only>
- **Trying:** <hypothesis, labelled "hypothesis", and the action under way>
- **Next update:** <time> (cadence: <from the table below>)
```

State is a closed set. Move forward only, and record each move in an update.

| State | Means | Who moves it |
|---|---|---|
| `declared` | Impact is confirmed and the response is running. | Whoever confirms impact |
| `mitigated` | User impact has stopped; the underlying cause may still be present. | IC, after checking at the symptom |
| `resolved` | The cause is fixed and the symptom metric has stayed at baseline. | IC |
| `closed` | The record is complete, follow-ups are filed, and the postmortem is handed off. | IC, after the close-out checklist |

| Sev | Internal update | Stakeholder or customer update |
|-----|-----------------|--------------------------------|
| Sev1 | Every 15–30 min, including "no change" | At declaration, then at least hourly, plus at mitigation and resolution |
| Sev2 | Every 30–60 min | At declaration, then on material change |
| Sev3 | On material change | On resolution, or sooner if a customer asks |
| Sev4 | On resolution | Usually none |

Send "no change" updates on schedule: silence reads as either "resolved" or "abandoned", and both
readings cause harm. Publish the symptom and a labelled hypothesis until the root cause is
confirmed, so no one has to retract a public explanation.

## Step 5: Call the scope-reset checkpoint when fixes stop working

After two consecutive mitigations to the same layer with no movement in the top-line symptom,
the IC calls a scope-reset checkpoint before a third ships. Say it in the channel: "Scope-reset
checkpoint: no third fix until we answer 1, 2 and 3." It takes about fifteen minutes and answers
three questions in writing:

1. **Has the symptom moved?** Compare the top-line signal (error rate, failed request count,
   latency percentile) with its value at declaration. If two deploys have not moved it, the layer
   being fixed is not the cause.
2. **What is the working hypothesis, and what would falsify it?** One sentence, then a specific
   query, log or metric whose result would prove it wrong. If nothing could falsify it, reset.
3. **Which layers outside the hypothesis are unchecked?** At minimum: shared telemetry and
   gateway infrastructure; upstream (auth, ingress, DNS, CDN); downstream (database, cache,
   queue); and config or infrastructure changes in adjacent repositories in the last 24 hours,
   not only the one being fixed.

Ship the third mitigation once all three are answered. If the answers point outside the current
layer, hand the incident to the team that owns that layer and stop changing the original one.
This is a rule rather than advice because under pressure a second failed fix produces more
conviction, not less: sunk effort reads as evidence.

## Step 6: Close out

Resolving impact is not closing the incident. Before moving to `closed`, confirm the record
holds each of these, and write "not known: <why>" for any you cannot fill, because an empty
field reads a quarter later exactly like no incident at all:

- [ ] Symptom as first seen, and how it was detected
- [ ] Corrected detection and impact-start times
- [ ] Severity history
- [ ] Affected services and populations (the final blast-radius block)
- [ ] Timeline, including hypotheses that were refuted
- [ ] Mitigation and confirmed root cause
- [ ] Follow-ups, each linked to a tracker item

Every follow-up becomes an owned item in the work tracker, because a checkbox inside the
incident record disappears from view when the incident closes. Create each in the tracker's
intake state with a named owner (default: the IC, who may reassign) and link it from the
incident. Where an existing item already covers the follow-up, link that item instead, and leave
its owner as it is; the IC default applies to new items.

Then hand off the blameless write-up (timeline format, five whys, contributing factors, action
items) to `ops-workflows:incident-postmortem`, passing it the record.

## When something is unavailable

- **No access to the incident tool.** Print the declaration template filled in, ask the user to
  post it, and say the incident is not yet recorded until they confirm. Keep printing each
  update in the same form.
- **No telemetry access** (no credentials, tool denied, or a web session). Declare on the
  confirmed symptom anyway; declaration does not wait for numbers. Ask for pasted exports or
  counts, and mark each blast-radius dimension you cannot measure `NOT MEASURED`.
- **No tracker access at close-out.** List the follow-ups as ready-to-file items, keep the
  incident at `resolved`, and name the follow-ups as the only thing blocking `closed`.

## Verify

Before posting each update, and again before closing, check the text you are about to post:

- State and severity are values from the two tables above, and the severity history is present.
- Every role shows a name or `unassigned`.
- The next-update time is set and matches the cadence for the current severity.
- The impact section contains the blast-radius block, with every dimension a number or
  `NOT MEASURED`.
- At `closed`: every close-out box is ticked or marked "not known: <why>", and every follow-up
  has a tracker link and an owner. Open each link once to confirm it resolves.
