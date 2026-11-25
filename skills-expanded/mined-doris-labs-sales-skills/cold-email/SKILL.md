---
name: cold-email
description: "Write a cold outreach email that earns a reply — one problem, a real relevance hook, brevity, and a single low-friction ask. Use for first-touch prospecting into a new account or persona. Triggers on: cold email, write outreach, first touch email, break in, cold outreach."
---

# Cold Email

## Purpose
Write a first-touch email a busy stranger actually replies to: one problem, one
relevance hook grounded in a real trigger, and one low-friction ask — not a pitch.

## Inputs
- Who you're emailing (name, role, company)
- A real trigger or reason-to-reach-out-now (hire, funding, launch, post, mutual context)
- The one problem you solve for this persona
- A proof point you can cite (a similar customer, a result, a relevant pattern)

## Method
1. **One problem per email.** Pick the single pain that matters most to *this*
   persona and write only about that. A second idea halves the reply rate — save it
   for the follow-up.
2. **Open with a real relevance hook.** The first line must prove you're writing to
   *them*, not a list — anchored to a trigger they'd recognise (a hire, a launch, a
   stage change, something they said publicly). No "Hope you're well" or "I came
   across your profile."
3. **Brevity.** Under 90 words, 5 sentences or fewer. It must be readable on a phone
   lock screen without scrolling. Every sentence earns its place or gets cut.
4. **Single low-friction ask.** Ask for *interest or a reply*, not a 30-minute meeting.
   "Worth a look?" / "Open to me sharing how?" beats "Do you have 30 mins Tuesday?"
   The ask is a yes/no, not a calendar negotiation.
5. **No feature-dumping.** Name the outcome, not the toolset. One proof point, stated
   as a customer + result, beats a feature list. Lead with their world, not your product.
6. **Subject-line rules:** 2–4 words, lowercase or sentence case, no caps, no emoji, no
   "Quick question," no "{Company} <> {YourCompany}." Make it look like an internal note
   from a colleague — reference their problem or trigger, never your product name.

**Cold email skeleton:**
```
Subject: <2–4 words, their problem/trigger>

Hi <name>,

<relevance hook tied to a real trigger — proves this isn't a blast>.

<the one problem this persona feels, in their language>.

<one proof point: similar customer + concrete result>.

<single low-friction yes/no ask>?

<first name>
```

### Variant A — VP Sales (trigger: just hired 5 AEs)
```
Subject: ramping the new AEs

Hi Dana,

Saw the 5 AE hires on the team page — congrats on the build-out.

The usual tax on a hiring spree is ramp time: new reps guess at what "good" looks
like on calls for a quarter before it clicks.

We cut that for {Customer} by turning their best calls into a live playbook reps
follow in real time — ramp dropped from ~5 months to under 3.

Worth a quick look at how?

Frazer
```

### Variant B — RevOps lead (trigger: messy CRM / forecast pain)
```
Subject: forecast vs reality

Hi Sam,

Most RevOps leads I talk to don't distrust the forecast — they distrust the CRM
data underneath it, because reps update stages from memory.

We close that gap by reading what was actually said on calls and flagging where the
CRM contradicts it, so the number you roll up is evidence-backed.

{Customer} caught a slipping six-figure deal three weeks earlier this way.

Open to me sending a 2-minute example?

Frazer
```

### Variant C — Founder / CEO (trigger: recent funding round)
```
Subject: post-raise pipeline

Hi Alex,

Congrats on the Series A — the pressure now flips to predictable pipeline.

At this stage the risk is your top rep's instincts living in their head instead of
in a repeatable motion the next ten hires can run.

We helped {Customer} turn their founder-led selling into a system before they scaled
the team, so quota wasn't a coin flip.

Worth 10 minutes to compare notes?

Frazer
```

## Tool binding
This skill works from a name and a trigger alone. It gets sharper when connected to
your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, ground the personalization and the
proof point in real data instead of guessing:
- `ontology_resolve("account", id, expand=["deals","contacts","activity","sentiment"])`
  — pull the account's open/closed deals, known contacts, recent activity, and sentiment
  to find a genuine, current relevance hook instead of a generic one.
- `ontology_resolve("person", id, expand=["company","deals"])` — resolve the specific
  contact's role and any prior deal context so the email reads one-to-one.
- `ontology_search(...)` — pull proof points from similar wins (a comparable customer
  and a concrete result) so the one cited proof line is real, not invented.
Prefer Doris-sourced triggers and proof points over assumptions — a wrong hook reads
worse than no hook.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → look up the contact, their role, account history, and
  any prior touches so you don't re-pitch or contradict an existing relationship.
- Gmail/Outlook MCP → check the thread/inbox for prior contact, then draft (or send) the
  email in the real thread rather than handing back copy to paste.

### With nothing connected
Ask the user for the prospect (name, role, company) and one real trigger or
reason-to-reach-out-now. From that, output 3 variants tuned to plausible angles, each
with its own subject line, all under 90 words, each with a single low-friction ask.
Hand back ready-to-send copy the user can paste into any client.

## Works without Doris
Fully functional from a name plus a trigger — Doris only replaces guesswork with real
account/contact context and evidence-backed proof points.

## Common mistakes
- Two problems in one email — the second idea kills the reply rate.
- A generic opener ("Hope you're well") instead of a real relevance hook.
- Asking for 30 minutes up front instead of a low-friction yes/no.
- Feature-dumping the product instead of naming one outcome + one proof point.
- A subject line that looks like marketing (caps, emoji, "{A} <> {B}", product name).
