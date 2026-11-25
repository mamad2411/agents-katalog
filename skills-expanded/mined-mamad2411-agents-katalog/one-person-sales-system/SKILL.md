---
name: one-person-sales-system
description: Build an automated pipeline that turns content viewers into paying clients without sales calls, cold outreach, or a sales team. Use when someone has content driving attention but no system converting it into clients, is manually DMing/calling every lead, or asks for a lead-capture-to-close funnel a solo operator can run.
---

# One-Person Sales System

Source: stage 4 of the 5-prompt "Dan Koe-style one-person business system"
carousel (@yourgptguide) reviewed from an uploaded photo batch — see
`one-person-business-idea`'s SKILL.md for the full sourcing note (marketing
hype in the framing, prompt content itself kept).

Stage 4 of 5 (idea → offer → content system → **sales system** → scaling).
Assumes `one-person-content-system` (or equivalent) is already driving
viewers — this skill converts that attention into paying clients.

## What this does

Maps the full path from "sees a piece of content" to "paying client" and
designs each handoff (lead capture, nurture, conversion) so the whole thing
runs without the operator manually chasing every lead or getting on a call.

## How to run it

1. Ask for the offer, content platforms, and current client-acquisition
   method before designing anything.
2. Map the customer journey from first piece of content seen to paying
   client — every step in between, not just the endpoints.
3. Design a lead capture system: how a content viewer becomes an email
   subscriber (or equivalent owned channel).
4. Build a nurture sequence: how a subscriber becomes a buyer without a
   sales call.
5. Create a conversion mechanism: the specific trigger that turns a
   subscriber into a client.

## Rules

- The system must require zero sales calls to function — that's the point
  of a *one-person* sales system.
- Every step must be executable by one person.
- The nurture sequence must deliver real value before it asks for
  anything — sequence the give before the ask.
- The conversion mechanism must feel natural, never pushy or desperate.

## Output

Customer Journey Map → Lead Capture → Nurture Sequence → Conversion
Mechanism → Automated Sales Flow

## Prompt (copy-paste)

The following is the original prompt as sourced, unedited, for use directly
in Claude or another assistant outside this skill:

```text
<role>Act as a one-person sales system architect who builds automated pipelines that attract, nurture, and convert ideal clients — without sales calls, cold outreach, or a sales team.</role>

<task>Build a complete one-person sales system that converts content viewers into paying clients automatically — while I focus on the work I actually want to do.</task>

<steps>
1. Ask for my offer, content platforms, and current client acquisition method before starting
2. Map the customer journey — from first piece of content to paying client
3. Design a lead capture system — how content viewers become email subscribers
4. Build a nurture sequence — how subscribers become buyers without a sales call
5. Create a conversion mechanism — the specific trigger that turns a subscriber into a client
</steps>

<rules>
- System must require zero sales calls to function
- Every step must be executable by one person
- Nurture sequence must deliver value before asking for anything
- Conversion mechanism must feel natural — never pushy or desperate
</rules>

<output>Customer Journey Map → Lead Capture → Nurture Sequence → Conversion Mechanism → Automated Sales Flow</output>
```

## Related skills in this repo

- **outreach-planning** / **outreach-execution** bundle: a much deeper
  cold-outbound system — reach for that bundle instead when the
  acquisition motion is proactive outbound rather than converting inbound
  content viewers, which is this skill's scope.
- **one-person-content-system**: stage 3 — the upstream source of the
  content viewers this system converts.
- **one-person-business-scaling**: stage 5 — scales the revenue this
  system produces without adding hours or headcount.
