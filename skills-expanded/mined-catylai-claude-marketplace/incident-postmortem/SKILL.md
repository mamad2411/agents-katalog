---
name: incident-postmortem
description: "Writes a blameless postmortem from an incident record or notes: timeline, causal chain, owned and dated actions. Use when an incident is resolved or a postmortem or RCA is due. Not for live triage (use observability-core:production-triage) or declaring (use observability-core:incident-declaration)."
argument-hint: "[path to the incident record, or paste it]"
allowed-tools: Read, Glob, Grep, Edit(docs/postmortems/**)
license: MIT
---

# Incident postmortem

Turn a resolved incident into a document that changes the system: what happened, why the
system allowed it, and a short list of owned, dated actions that someone can close.

Blameless means the write-up explains how a reasonable person made each decision with the
information they had at the time. Name systems, gaps and missing guardrails as causes, and
people only as actors in the timeline. A write-up that blames a person teaches the team to hide
the next near-miss.

## Step 1: Gather the incident record

The input is the record `observability-core:incident-declaration` keeps: $ARGUMENTS if given,
otherwise a record, export or notes the user points to or pastes. Map it like this:

| Record field (incident-declaration) | Goes into |
|---|---|
| Incident (symptom as first seen), Detected by | Summary, first timeline rows |
| Severity and its history | Header, as written in the record |
| Impact start, detection, declaration, mitigation and resolution times | Header duration line, timeline |
| Roles (IC, Operations, Comms, Scribe) | Header, and who to ask about gaps |
| Updates: Impact, Known, Trying | Timeline, including what people believed at each step |
| Final blast-radius block | Impact section, copied as is |
| Refuted hypotheses, mitigation, confirmed root cause | Timeline and contributing factors |
| Follow-ups with tracker links | Action table rows, linked rather than refiled |

Severity uses the Sev1–Sev4 scale defined in `observability-core:incident-declaration`. Copy
the final severity and its history from the record rather than re-grading it here. If the
severity was wrong in hindsight, that is a finding for the contributing factors, not an edit.

Check the record's state before writing:

- `resolved` or `closed`: write the postmortem.
- `declared` or `mitigated`: the incident is still live. Say so and point to
  `observability-core:incident-declaration`; offer an outline to fill later rather than a
  finished document.
- No record at all (only chat logs, tickets or memory): reconstruct the timeline from what is
  pasted, mark each reconstructed row `(reconstructed)`, and ask in one question for the
  missing essentials: impact start and end, how it was detected, and what the mitigation was.

**Without a checkout** (web, or no file access): work entirely from pasted notes and return the
postmortem inline.

## Step 2: Build the causal chain

Look for the chain of conditions that let the trigger become an outage, not a single root
cause. Keep asking "why was that possible?" (five whys is a good pace) until each branch ends at
a system or process gap an action could close. Most incidents have one trigger and several
conditions; list the conditions, because they are where the durable fixes live.

Cover three kinds of factor, since each produces a different kind of action:

- **Cause:** why the fault happened and why nothing stopped it (prevent).
- **Detection:** why it took as long as it did to notice (detect).
- **Response:** what slowed mitigation once noticed (mitigate).

<example>
Trigger: a config change set the connection-pool size for `orders-api` to 5 instead of 50.

1. Checkout requests timed out because `orders-api` exhausted its database connection pool.
2. The pool was 5 because the change edited the base config, which every environment inherits,
   while the author believed they were editing the staging overlay.
3. The base and overlay files have the same name in sibling directories, and the review diff
   showed only the file name, so the reviewer believed the same thing.
4. Nothing validates pool size against expected load, so the deploy passed every check.
5. Detection took 38 minutes because the latency alert fires on p50, and p50 stayed flat while
   p99 climbed.

Items 2–5 are conditions; each maps to an action row. "Author edited the wrong file" is the
trigger and gets no action of its own, because the next person will make the same edit while
items 3 and 4 hold.
</example>

## Step 3: Write the postmortem

Use this template. Write times in UTC, noting the original time zone once if the sources used
another.

```markdown
# Postmortem: <short title> (<YYYY-MM-DD>)

**Status:** <draft | in review | final>
**Severity:** <final Sev from the record>. History: <from the record>
**Duration:** impact start <time> → detected <time> → declared <time> → mitigated <time> → resolved <time>
**IC:** <name>   **Author:** <name>   **Incident record:** <link or "pasted">

## Summary
Three sentences: what broke and for whom, how long, and how it was fixed.

## Impact
<the final blast-radius block from the record, unchanged>

## Timeline (UTC)
| Time | Event | What we believed then | Source |
|---|---|---|---|
Detection, each hypothesis (including refuted ones), each action and its observed effect,
mitigation, resolution.

## Contributing factors
A numbered causal chain from trigger to impact, one condition per line. Tag each
cause, detection or response.

## What went well
Things to keep doing, each specific enough to repeat.

## Where we got lucky
Conditions that limited the damage by chance. Each one is a candidate action.

## Action items
| # | Action | Type | Owner | Due | Done when | Tracker | From factor |
|---|---|---|---|---|---|---|---|
Type is one of prevent, detect, mitigate.

## Links
Raw logs, dashboards, chat export.
```

Keep the document under two pages; long logs go under Links.

- **Detection time** is when a person or automation first acted on the signal, not when an
  alert fired unseen. If they differ, the gap is a detection factor.
- **Every "should have"** in the narrative becomes an action row or is deleted, so the
  document never states a lesson that nobody owns.
- **Each action** names one owner (a person, or a team with a named contact), a due date, and a
  "Done when" that someone other than the owner could check. An action nobody can close stays
  open forever and reads as progress.
- **Follow-ups already filed** at close-out are linked in the Tracker column, not filed again.
  An action with no tracker item gets `to file`, and is listed in the hand-back.

<example>
Not closeable: "Improve monitoring of the database." There is no owner, no end state, and no
way to tell when it is done.

Closeable: "Add a p99 latency alert for `orders-api` at 800 ms over 5 minutes, routed to the
payments on-call rotation. Owner: Priya (payments). Due: 2026-10-09. Done when: the alert
exists in the alerting config and fired in a staging load test."
</example>

## Step 4: Hand back

Return the postmortem inline. In a checkout, offer to save it to
`docs/postmortems/<YYYY-MM-DD>-<kebab-title>.md` and write it only if the user agrees. If the
write is denied or fails, keep the inline copy as the result and say it was not saved.

After the document, list in a few lines: actions still marked `unassigned` or `to file`,
timeline rows marked `(reconstructed)`, and any record field that was missing.

## Verify

Before handing back, re-read the document and check:

- Every "should have", "could have" or "we need to" in the text maps to a row in the action
  table. Add the row, or delete the sentence.
- Every action row has an owner and a due date. Any row without them is listed in the hand-back
  and the status stays `draft`.
- Every "Done when" is a check someone else could run, not a restatement of the action.
- Severity and its history match the incident record word for word.
- No sentence names a person as the cause.
- If saved, open the file once to confirm it is at the stated path.
