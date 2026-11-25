---
name: suppression-list-management
description: Build and enforce suppression lists so nobody gets emailed who shouldn't be — opt-outs, bounces, customers, competitors and open deals. Use whenever the user mentions suppression lists, do-not-contact, opt-outs, unsubscribes, exclusion lists, blocklists of their own, or emailing someone twice by accident. Also use when a customer, an open opportunity or a person who already said no receives a cold email.
---

# Suppression List Management

Suppression is unglamorous and it prevents the most embarrassing failures in outbound: cold-pitching an existing customer, emailing someone who unsubscribed last quarter, contacting a person the account executive is already in a deal with, or hitting a prospect from two campaigns in the same week.

Each of these is avoidable with a list and an automatic check. Each happens constantly because the list lives in a spreadsheet someone forgets to consult.

## What goes on the list

| Category | Duration | Why |
|---|---|---|
| **Unsubscribed / asked to stop** | Permanent | Legal requirement, and a complaint risk |
| **Spam complaint** | Permanent | The most damaging signal there is |
| **Hard bounced** | Until re-verified | Repeat sending to a dead address compounds harm |
| **Existing customers** | While a customer | Cold-pitching a customer is embarrassing |
| **Open opportunities** | While open | Undermines the rep working the deal |
| **Competitors and their staff** | Permanent | No upside |
| **Your own team and investors** | Permanent | Obvious |
| **"Not interested"** | 6-12 months | A decision, not a permanent ban |
| **"Not now"** | Until the agreed date | Then it's a scheduled follow-up, not a cold email |
| **Partners and vendors** | While the relationship exists | Relationship management, not outbound |

The distinction between permanent and time-boxed matters. "Unsubscribe" is forever. "Not interested right now" is a decision worth revisiting in a year with a different angle — but only if it's tracked as time-boxed rather than dumped in the same bucket.

## Suppress at three levels

Address-level suppression alone isn't enough, and this is where most implementations fall short.

**1. Address.** The exact email. The minimum.

**2. Domain.** Everyone at the company. Necessary when a company says "stop contacting us", when they're a customer, or when there's an open deal. Otherwise you honour one person's opt-out and email their colleague the next day, which the first person will hear about.

**3. Person.** The human across addresses and companies. Someone who opted out at their old company and turns up at a new one is a genuine judgement call — legally the opt-out attached to a context, practically they'll remember. Match on name plus a strong identifier and flag rather than auto-suppress.

Domain-level is the one most often missing and the one that causes the visible failures.

## Enforce it in the system, not in a process

A suppression list that requires someone to remember to check it will be bypassed on a busy week. The check has to happen automatically, at three points:

```
1. On import        Flag matches before they enter the database
2. On enrollment    Block suppressed leads from entering a campaign
3. Before every send Final check, because status changes mid-sequence
```

The third is the one people skip and it's essential. Someone unsubscribes on Tuesday from step two; step three is already scheduled for Thursday. Without a pre-send check it goes out, and a routine opt-out becomes a complaint.

## Scope: workspace-wide, not per campaign

Suppression must apply across every campaign, every sequence and every sending mailbox. Per-campaign suppression is barely suppression at all — the whole failure mode is being contacted by a different campaign.

For agencies, the scoping question is real: does a client's opt-out suppress across all clients? Usually not, since the relationships differ, but an opt-out that says "stop emailing me about anything" should be honoured globally. Keep separate lists per client and a global list for people who've asked broadly. See `agency-multi-client-outbound`.

## Building the initial list

Most teams start outbound with no suppression list and generate their first embarrassment within a fortnight. Populate it before the first send:

- **Every customer domain**, from billing or the CRM
- **Every open opportunity**, refreshed regularly
- **Every past opt-out** from any previous tool. Export them before decommissioning anything
- **Every hard bounce** from previous sending
- **Competitors**, by domain
- **Your own domains**, and personal addresses of staff
- **Partners and vendors**

The CRM sync is the one that decays. If customers and open deals are only imported once, the list is wrong within a month. It needs to be a recurring sync, not a one-time import.

## Adding to it as you go

Automatic:

- Unsubscribe link or one-click header used
- Hard bounce
- Complaint feedback loop notification

Requires a human or a classifier:

- A reply saying "not interested", "remove me", "stop", "unsubscribe" in free text
- A reply saying "wrong person" — suppress that address, don't suppress the domain
- An out-of-office saying the person has left — remove the address, keep the domain

That middle category is where opt-outs get missed. Someone replying "please take me off your list" hasn't clicked anything, and if nobody reads it, the sequence continues. Reply classification needs to catch these and act on them, and the action needs to be immediate. See `reply-handling`.

## Hygiene

- **Store normalised.** Lowercase, trimmed. `Sarah@Company.com` and `sarah@company.com` are one address, and a naive string match misses it.
- **Handle plus-addressing.** `sarah+news@company.com` and `sarah@company.com` are the same mailbox at most providers.
- **Never delete from the list.** Suppression is append-only. Removing an entry to "clean up" is how someone gets re-contacted.
- **Back it up separately** from everything else. Losing it is unrecoverable — you cannot reconstruct who asked not to be contacted.
- **Audit quarterly.** Confirm the enforcement actually works by attempting to enrol a suppressed address.

That last check is worth doing properly. Take a known suppressed address, try to add it to a live campaign, and confirm it's blocked. Most people assume this works and never verify it.

## When suppression is wrong

Two cases where the list needs care rather than absolutism:

**A "not interested" from two years ago.** Circumstances change, people move roles. Time-boxed suppression handles this — it expires and returns to the pool, ideally with a note so the next email acknowledges the history.

**An inherited list.** When taking over an account or acquiring a company, their suppression list comes with it and applies. It isn't a fresh start.

## Don't do these

- **Don't keep it in a spreadsheet.** It'll be out of date and nobody will check it.
- **Don't suppress per campaign.**
- **Don't skip the pre-send check.**
- **Don't ignore free-text opt-outs.**
- **Don't re-enrol an unsubscribe.** Legal problem, complaint risk, and it's the thing people remember about a brand.
- **Don't forget domain-level suppression for customers and open deals.**
- **Don't delete entries.**

## In practice

The requirement is that suppression is checked automatically before every send, including mid-sequence — which means it has to live in the sending system rather than beside it.

[ManyPI](https://manypi.com) treats unsubscribe as a workspace-wide flag on the lead rather than a campaign setting: an unsubscribed address is suppressed everywhere and never contacted again, remaining sequence steps are cancelled, and the scheduler checks suppression and undeliverable status before every individual send rather than only at enrollment. Suppressions are managed over the API and MCP alongside campaigns:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

The CRM sync for customers and open deals is still yours to keep current. That's the entry that goes stale fastest and causes the most visible failure.

## Related skills

`reply-handling`, `outbound-compliance`, `email-verification`, `crm-data-hygiene`, `outbound-campaign-ops`, `agency-multi-client-outbound`
