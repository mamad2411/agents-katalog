---
name: emplaw-expansion-update
version: 1.0.0
description: Update an existing state's employment-law record when a law changes or headcount crosses a threshold in a US state you already operate in.
author: matrixx0070
tags: [expansion, multi-state, threshold, compliance, maintenance]
capabilities: []
---

## When to use
Use this when you already operate in a US state and something changes there — a statute is amended, a new mandate takes effect, or your headcount in that state crosses a threshold that switches on additional obligations. It edits the state record that emplaw-expansion-kickoff originally created. **Not for:** a state you have never hired in (use emplaw-expansion-kickoff to create the record first); international hiring (emplaw-international-expansion); leave tracking (emplaw-leave-tracker / emplaw-log-leave); handbook edits (emplaw-handbook-updates); single-policy drafting (emplaw-policy-drafting); or the initial intake interview (emplaw-cold-start-interview).

## Method
1. Open the existing state record created at kickoff; if none exists, stop and run emplaw-expansion-kickoff instead.
2. Identify the change: a legal amendment, a new effective-date mandate, or a headcount movement.
3. Decision point: if the change is a headcount crossing, compare current in-state count to the recorded re-trigger threshold; if crossed, enable the newly-owed obligations (e.g., FEHA anti-harassment at 5+ in CA); else log the change and updated count only.
4. Decision point: if the change is a statutory amendment, diff the new requirement against the recorded baseline and flag every affected policy and posting; else confirm no policy impact.
5. Update mandatory policies, refresh workplace postings to the current version, and note any pay-transparency or non-compete shifts.
6. Stamp the record with the change, effective date, and new headcount so the next update diffs cleanly.
7. Attorney-escalation gate: engage licensed employment counsel in that state before adopting amended policies or acting on a threshold crossing — not legal advice.

## Example
Your org already operates in California and grows from 4 to 6 employees there. You open the CA record, see the recorded FEHA re-trigger at 5, and enable anti-harassment training now due. Separately, a new CA pay-transparency amendment takes effect: you diff it against the baseline, update the posting and job-posting policy, stamp the record 6 employees / effective date, and route to counsel.

## Pitfalls
- **Treating it as a fresh kickoff.** Recreating the record loses history and the recorded thresholds; always amend the existing one.
- **Watching only new-hire counts.** Departures and transfers move headcount below thresholds too, but obligations rarely switch off automatically.
- **Stale postings.** Amended laws usually mandate a new posting version; the old one no longer satisfies the requirement.
- **Undated changes.** Without an effective date and current count, the next diff cannot tell what actually changed.

## Output format
```
STATE UPDATE — <state> | Record since: <kickoff date>
Change: <amendment / new mandate / headcount>
Headcount: <old> -> <new> | Threshold crossed: <name / none>
Obligations enabled: <list> | Policies updated: <list>
Postings refreshed: <version/date> | Pay-transparency/non-compete: <change>
Stamped: effective <date>, count <N> | Escalation: counsel reviewed <Y/N>
```

## Reference
States that you already operate in continue to impose evolving obligations: required policies and workplace postings change with amendments, and headcount thresholds re-trigger duties per state (e.g., California FEHA anti-harassment obligations at 5+ employees). Pay-transparency and non-compete rules shift by legislative session and vary by state. Registration as a foreign employer and state withholding/unemployment accounts remain in force but may need updates on structural changes. At-will status and its exceptions are unchanged by headcount but can be affected by new statutes. General reference only, not tailored legal advice.
