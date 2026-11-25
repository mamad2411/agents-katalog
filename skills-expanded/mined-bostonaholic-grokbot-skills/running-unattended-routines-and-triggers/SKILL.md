---
name: Running unattended routines and triggers
description: >-
  Use when creating or editing a scheduled routine or event trigger that runs
  while nobody is watching, so it never stalls on an approval, never fires on
  noise, and is tested before it is trusted.
---
# Running unattended routines and triggers

Approvals raised by a routine, trigger, or another bot expire after about ten minutes and the action never runs. Design every unattended job to end in a draft, a file, or a report, and move the permission step to when a person is there.

## The line every routine prompt carries
```
This run is unattended. Never request an approval during it.
If you reach a step that needs one, stop there, write what you would
have done and why, and put it in the report under "waiting for
approval". Then continue with the steps that do not need one.
```

## Creating a routine
1. **Schedule.** Write it in plain words and confirm the time zone back before saving. Reads and prep run nightly, summaries weekly; hourly only when the source really changes hourly.
2. **Inputs.** If an input is missing or a source is unreachable, report the failure. Never substitute older data as today's.
3. **Idempotent.** Every step must be safe to run twice. Before any step that creates or sends something, check whether it already happened; if a step can't be made safe, stop before it and flag it.
4. **Output.** Name the exact destination (file, issue, draft, report line). Stay quiet when nothing changed, but log the run so a silent run and a failed run can be told apart.
5. **Test run.** Run it once against safe inputs and read the full output before trusting the schedule. Test runs do real work.

## Creating a trigger
1. Fire only when ALL are true: a specific source (one channel, repo, or label), a specific phrase or sender, and not already handled in the last N hours.
2. One action when it fires, read-only or draft-only. Then stop; no chaining into other work.
3. Before saving, estimate how many times it would have fired in the last 7 days. More than 10 means narrow the match.

## Done checklist
- [ ] Unattended line is in the prompt
- [ ] Time zone confirmed
- [ ] Missing-input and failed-check paths report instead of guessing
- [ ] Every create/send step checks for a prior success first
- [ ] Test run output read and test-run note recorded (format in starting-a-routine-skill-first step 8)
- [ ] Trigger fire estimate is 10 or fewer per week

## Circuit breaker (bot-skills#39, Adam GO Nov 2, 2026)
After 3 consecutive failures from the same source, pause the routine and tell Charles in one line naming the routine and the error, so he can resume it. Kill rule: if no pause fires in 30 days, remove this block.
