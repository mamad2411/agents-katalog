---
name: incident-postmortem
version: 1.0.0
description: Turn raw incident notes into a blameless postmortem - quantified impact, gap-honest timeline, a root-cause chain, what worked, and action items that actually block recurrence.
triggers:
  - postmortem
  - incident report
  - write up this incident
  - root cause analysis
  - RCA
capabilities: []
inputs:
  - name: notes
    required: true
    description: Raw incident notes - timeline fragments, log excerpts, chat snippets, who did what.
  - name: severity
    required: false
    description: Severity level and user impact if known.
---

# Incident Postmortem

## When to use
Use this after an incident, when you have raw material - timeline fragments, log excerpts, chat snippets, who did what - and need the document that makes the same failure impossible or survivable next time, without turning anyone into the villain.

**Not for:** live incident response (during the fire you need a status update and a mitigation, not a retrospective); performance reviews or assigning blame; or "incidents" that are really feature requests. If the notes are so thin there is no timeline and no observed impact, gather more before writing - a postmortem built on guesses is worse than none.

## Method
1. **Assemble the timeline first.** Every timestamped fragment, in UTC, in order. *Decision point:* where the notes have holes, write "gap - unknown between X and Y" rather than smoothing it over.
2. **Quantify impact.** Duration, users or requests affected, data lost, money if known. *Decision point:* if impact was never measured, write "impact not measured" and make measuring it an action item - never write "some users were affected".
3. **Walk the why-chain to systemic causes.** Ask why at least three times: trigger -> why it broke -> why that was possible -> why it was not caught. A one-line "root cause: bad config" is a failure.
4. **Frame everything blamelessly:** systems and roles, not names-as-fault. "The deploy script allowed prod pushes without CI," not "Alex skipped CI."
5. **Record what went well** - detection, escalation, tooling - so it survives the next reorg.
6. **Write action items sorted prevent > detect > mitigate.** Each names a SYSTEM change, an owner, and how you will verify it happened. Write the two-line summary last.

## Example (abridged)
**Root cause chain:** cron restarted the daemon mid-deploy (trigger) -> daemon served half-old, half-new code -> possible because deploys do not pause the remediation cron -> not caught because health checks test liveness, not version consistency.

**Action items:**
- [ ] Deploy script acquires a lock the remediation cron respects - owner: infra, verify: cron logs show skip during next deploy
- [ ] Health check includes build hash; alert on mixed hashes - owner: platform, verify: staged mixed-version test fires the alert

## Pitfalls
- **Single-cause thinking.** Stopping at the trigger ("bad config") instead of asking why the system let bad config reach prod.
- **Blame smuggled in.** Naming a person as the cause; the fix is always a system change, not "be more careful".
- **Timeline spackling.** Inventing plausible events to fill gaps instead of marking them unknown.
- **Unverifiable action items.** "Improve monitoring" with no owner and no way to check it landed - it never lands.

## Output format
```
# Postmortem: <title> (<date>)

**Summary:** <two lines, plain language>
**Severity / Impact:** <duration, blast radius, data/money; or "not measured">

**Timeline (UTC):**
- HH:MM  <event>
- HH:MM  gap - unknown until HH:MM

**Root cause chain:** trigger -> broke because -> possible because -> not caught because

**What went well:** <detection / escalation / tooling that worked>

**Action items:**
- [ ] <systemic change> - owner: <name/team>, verify: <check>
```
