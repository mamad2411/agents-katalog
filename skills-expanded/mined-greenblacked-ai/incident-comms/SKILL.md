---
name: incident-comms
description: "Communicate outward during and after an incident — status page posts, customer notices, executive briefings and internal channel updates. Covers a dedicated comms role, acknowledging on impact rather than on diagnosis, a next-update promise you keep, severity-to-comms rules agreed in advance, regulatory and SLA clocks that start at detection, and the follow-through after resolution. Use this skill whenever something is broken and someone outside the response has to be told, or told again afterwards — including phrasings like \"what do we put on the status page\", \"customers are asking what is happening\", \"the CEO wants an update\", \"do we have to notify anyone\", or \"write the customer-facing writeup for last week's outage\". Do not use it for technical diagnosis or mitigation (incident-response, or k8s-triage for Kubernetes), the internal blameless analysis (postmortem), routine reporting (status-update), or rehearsing a response (game-day)."
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Incident Comms

Good incident communication means nobody affected has to ask what is happening, and every promise made during the incident — especially the promise of a next update — is kept.

The job is hard for a structural reason: the people who understand the incident are the people fixing it, and they are the worst-placed to communicate it. They are context-switching, they know too much detail, and under load they overpromise. Meanwhile communication that waits until the facts are known always arrives after the customer has already noticed, formed a view, and told someone. The two natural instincts both destroy trust — say nothing until certain, which cedes the narrative and reads as either incompetence or concealment, or promise a fix time, which is wrong roughly half the time and is remembered as a lie rather than an estimate. What replaces both is a separate role, an acknowledgement that goes out on impact, and a cadence commitment instead of a resolution commitment.

## Scope

Use for: the first acknowledgement, ongoing updates, status page discipline, executive and internal briefings, the workaround notice, the all-clear, the customer-facing post-incident write-up, and the follow-through with affected accounts.

Do not use for: diagnosing or mitigating the technical failure, which is `incident-response` (or `k8s-triage` for a Kubernetes workload); the internal blameless analysis of causes and action items, which is `postmortem` and which this skill's public write-up must be consistent with; routine weekly or executive reporting when nothing is on fire, which is `status-update`; or planning a drill, which is `game-day`.

## Hard gates

**A comms owner is named in the first five minutes, and it is not the incident commander or anyone touching the system.** A responder writing a status page update is a responder not fixing the incident. Comms written by the person under load are the ones that overpromise, name an unconfirmed cause, or go out with internal jargon in them. If the team is too small to spare someone, the incident commander delegates comms to the first person to join who is not needed technically, and says so out loud.

**Acknowledge on impact, not on diagnosis.** The first message goes out when you know customers are affected, not when you know why. It has four parts and no more: what is affected, who is affected, that it is being worked, and when the next update comes.

**The next-update time is a promise.** Keep it even when there is nothing new — "still investigating, no new information, next update at 15:30" is a complete and adequate update. A missed update is read as a bigger problem than the outage, because silence is the signal people use to infer that things have got worse or that nobody is in control.

**Never state a cause you have not confirmed.** Early hypotheses are wrong often enough that the retraction costs more than the delay. This includes causes that point at a vendor.

## Workflow

### 1. Stand up the comms role

At declaration, name three roles distinctly, even when two are the same person on a small team: **incident commander** (runs the response), **comms lead** (everything in this skill), **scribe** (timeline for the postmortem later).

The comms lead's first three actions: open the customer-facing channel (status page), open or confirm the internal channel, and start a decision log of every external statement made, with its timestamp. That log is what stops the public write-up contradicting what was said at hour two, and it is the input `postmortem` needs later.

The comms lead pulls facts from the incident commander at agreed intervals rather than reading the technical channel and interpreting. Interpreting is how an internal hypothesis becomes an external statement.

### 2. Decide, against a rule, who gets told

Make this decision against a mapping agreed before the incident, not by whoever is most nervous during it. Fill this table with your own severity definitions and thresholds and get it agreed while nothing is broken.

| Severity | Public status page | Customer notice | Executives | Internal all-staff | Support briefed |
| --- | --- | --- | --- | --- | --- |
| Sev 1 — major outage, most customers, core function | Yes, within 15 min of impact | Yes, proactive email to all affected | Immediately, then hourly | Yes, at declaration | Yes, before the queue fills |
| Sev 2 — significant degradation or a subset of customers | Yes, within 30 min | Yes, to the affected segment only | At declaration, then at resolution | Yes, in the engineering channel | Yes, with a holding line |
| Sev 3 — minor or narrow impact, workaround exists | Judgement — post if support volume is rising or it lasts past an hour | Only accounts that raise it | Summary in the next routine update | No | Yes, macro only |
| Sev 4 — internal only, no customer impact | No | No | No | Only if it affects deploys | No |

Two rules that override the table. Anything with a suspected data or privacy dimension goes to legal immediately regardless of severity, because the clocks in step 6 start on detection. And anything a customer has already posted publicly is already public: the choice is between your account of it and theirs.

### 3. Write for one audience at a time

The same text for all four is what forces it to be vague enough to be useless to each of them.

| Audience | What they need | What they will do with it | Never include |
| --- | --- | --- | --- |
| Customers | What is broken in their terms, who is affected, any workaround, when the next update lands | Decide whether to wait, work around it, or escalate | Internal service names, hypotheses, blame, a fix time |
| Executives | Scope, customer and revenue exposure, regulatory or contractual implications, and the decision you need from them if any | Handle the board, the press, the largest accounts | Technical detail with no decision attached to it |
| Internal staff | Whether to stop deploying, which channel to watch, what to tell anyone who asks, who is running it | Stop making it worse, stop asking responders for updates | Speculation that will leak outward verbatim |
| Support and account teams | A line they can say, a macro they can send, the workaround, and what is explicitly not yet known | Answer the queue without inventing anything | Anything they are not authorised to say |

Executives get the ask stated explicitly, or an explicit "no decision needed from you". An executive update with no ask and no boundary invites intervention, which arrives as a second incident commander.

### 4. Use language that survives being screenshotted

Assume every word is read later by a journalist, a regulator and an angry customer's lawyer, because occasionally one of them is.

| Do not write | Write | Why |
| --- | --- | --- |
| The auth-svc replica set is degraded | Some customers cannot sign in | Nobody outside knows what your services are called; name the symptom in their terms |
| Caused by a bad deploy | We have identified a likely contributing change and are validating | Causes stated early are wrong often enough that the retraction costs more than the delay |
| Our cloud provider is having an outage | We are investigating a fault in part of our infrastructure | You own the service you sold, regardless of what is underneath it |
| Fixed by 16:00 | Next update at 15:30 | An estimate is remembered as a commitment |
| A small number of customers were affected | 4% of accounts, all in the EU region, between 09:12 and 10:40 UTC | Minimising language reads as concealment when the real number surfaces |
| Fully resolved | Service restored; monitoring for recurrence before we close | "Fully resolved" followed by a relapse costs more than the second outage |
| An engineer ran the wrong command | A change was applied that our validation did not catch | Naming a person externally is unrecoverable and inconsistent with a blameless postmortem |

Give a time estimate only when you would personally bet on it. Otherwise commit to the next update instead. This is the single hardest instinct to suppress, because everyone in the meeting wants a number, and giving one buys twenty minutes and costs the relationship.

### 5. Keep the status page honest

The status page is the artefact customers, journalists and enterprise buyers check first, and the one they screenshot.

- It must be hosted off your own infrastructure. A status page that goes down with the product is worse than none, because it converts an outage into evidence that you cannot run anything.
- Subscribers get notified on post, so posting is not passive — post before the support queue fills, not after. Support answering ahead of the status page means every answer is bespoke, inconsistent, and unlogged.
- Set the component and the state deliberately: investigating, identified, monitoring, resolved. Moving to "resolved" and back is far more damaging than staying on "monitoring" for an extra hour.
- Every post carries a timestamp with a time zone and the time of the next update.
- Do not use it to explain the architecture. Impact, scope, workaround, next update.

### 6. Start the regulatory and contractual clocks at detection

The clocks that matter run from when you knew, not from when you fixed it. Get legal and account management in the loop before the clock, not after.

| Clock | Typically starts | Who must be told early |
| --- | --- | --- |
| Personal-data breach notification (for example GDPR's 72 hours) | Awareness of the breach, not confirmation of scope | Legal and the data protection officer, at first suspicion |
| Sector-specific reporting duties (financial, health, critical infrastructure) | Detection or classification, depending on regime | Legal and compliance |
| Contractual incident notification in enterprise agreements | Detection, often with a 24-hour or 48-hour window | Account management, per contract |
| SLA credit windows | Impact start, and credits are often forfeited if not claimed in a window | Account management and finance |

The comms lead does not interpret any of these. The job is to notify the people who do, in the first half hour, and to record the detection timestamp precisely, because that timestamp is what every clock is measured from.

### 7. Follow through after resolution

The part everyone skips, and the only part that converts an outage into trust.

- **Contact the accounts that were hurt, before they contact you.** The named list from the impact analysis, reached by their account owner with the specifics of their exposure, not a bulk email.
- **Honour credits without being asked.** A customer who has to discover, calculate and claim a credit remembers the process, not the credit.
- **Publish the customer-facing write-up within a week**, or say publicly when it will land.
- **Close the loop when the remediation actually ships.** A short message to the accounts you contacted saying the specific fix is now in production. Almost nobody does this, which is exactly why it is worth doing.

## Templates

### Initial acknowledgement

```markdown
[Investigating] [Plain-language description of the symptom] — [HH:MM TZ]

We are investigating an issue affecting [customer-visible capability]. Customers
[on which plan, in which region, using which feature] may experience [what they see].

Our team is actively working on this. Next update by [HH:MM TZ, no more than 30
minutes out for a Sev 1].
```

No cause, no estimate, no apology paragraph. It goes out on impact.

### Ongoing update

```markdown
[Investigating | Identified | Monitoring] [Same title as the first post] — [HH:MM TZ]

What we know: [Impact and scope in customer terms. Any change since the last update.]
What we are doing: [The action in progress, at a level a customer understands.]
What you can do: [Workaround, or "no action needed".]

Next update by [HH:MM TZ].
```

Post it on schedule even when nothing has changed, and say that nothing has changed.

### Workaround available

```markdown
[Identified] [Title] — [HH:MM TZ]

A workaround is available while we complete the fix.

[Numbered steps, exact, tested by someone who is not the author.]

Limitations: [What the workaround does not cover, and anything the customer will
need to undo afterwards.]

Next update by [HH:MM TZ].
```

Test the workaround before publishing it. A workaround that does not work costs more than none, because the customer has now spent time as well as being broken.

### Resolution

```markdown
[Resolved] [Title] — [HH:MM TZ]

[Capability] was [degraded or unavailable] for [customers affected] between
[HH:MM] and [HH:MM TZ], a duration of [N minutes]. Service is restored and we have
confirmed normal operation for [period].

[If applicable: what customers should do now — retry, re-run, re-check, nothing.]

We are completing a full review and will publish a detailed write-up by [date].
```

State the duration and the scope in the resolution notice. Withholding them until the write-up reads as reluctance, and the numbers will come out anyway.

### Public post-incident write-up

```markdown
# [Date] — [Plain description of what was broken]

## What happened
[Two or three sentences a non-customer could follow. No internal service names.]

## Impact
[Who, how many, which capability, exact start and end times with time zone, and
what the customer experienced. Numbers, not "a small number of customers".]

## Why it happened
[The contributing conditions, described in system terms. Enough that a technical
reader believes you understand it; not so much that it becomes an architecture
tour or exposes an attack surface. No individuals named, ever. No vendor blamed.]

## What we have done
[Immediate fix, already shipped, with dates.]

## What we are doing next
[Remediation with real dates. Only commitments you will actually fund — this
paragraph will be quoted back to you.]

## Credits and next steps for affected customers
[What is being applied automatically and who to contact.]
```

The public write-up is not the internal postmortem with names removed — it is a different document for a different reader. It carries less internal detail, no individuals, no blame, and a clear statement of impact and remediation. What it must never do is contradict the internal one. Write the internal `postmortem` first, then derive this from it, and have the same person check both. A customer who later sees a leaked internal document that disagrees with the public one has learned something about you that no remediation fixes.

## Anti-patterns

**Waiting for facts.** By the time you are certain, the customer has already noticed, formed a view and posted about it. You are now correcting their narrative instead of setting yours, from behind.

**A promised fix time.** Wrong roughly half the time, and remembered as a lie rather than an estimate. Commit to the next update instead; it is the one promise you can always keep.

**One message for four audiences.** Forced to be vague enough to suit all of them, so it is actionable for none. The executive cannot find the decision, the customer cannot find the workaround, and support invents a line.

**Naming a cause you have not confirmed.** The retraction is more expensive than the delay would have been, and it teaches everyone to distrust the next update too.

**A missed next-update.** Silence is read as escalation. Customers infer that it got worse or that nobody is in control, and both inferences are more damaging than any true status.

**A public write-up that contradicts the internal one.** The gap is what gets quoted when either one leaks, and it converts an operational failure into a credibility failure.

**Blaming a vendor.** You sold the service; the customer bought it from you. Pointing at a provider reads as an admission that you do not control your own product, and it is the sentence that ends up in the trade press.

**Silence after resolution.** No proactive contact, credits only for those who ask, and no word when the remediation ships. The outage is then the last thing the customer heard from you, which is exactly the memory you did not want to leave.

## Reference files

- `references/audience-messages.md` — one incident's facts written five ways (status page, customer email, executive brief, internal channel, support macro), with the translation rules and the phrases to strike. Read it when the same incident has to reach more than one audience.
