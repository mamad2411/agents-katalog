---
name: frac-week-plan
description: Designs a week template for a fractional leader with several clients, by client day or half-day, with no more than two client contexts in a day, focus blocks, solo work placed right after each client call, one daily triage slot, a buffer and the published version each client sees. Use for "run frac-week-plan", "plan my week across clients", "managing multiple clients", "I switch between three companies before lunch", "theme days for my clients", "week template for fractional work", "how do I structure my week with several clients", part of the Claude for Fractional Leaders Pack by 90n.
---

# Week Plan Across Clients

## When To Use
You switch between three companies before lunch and finish none of the thinking. The hours add up; the work does not get done, because every hour starts with remembering a different company's words, people and problems. This answers: which client gets which part of the week, and what does each client see?

## When Not To Use
If you do not know whether the commitments fit at all, run Client Capacity Plan first. If the week is designed and you want to see what really happened, run Weekly Review Across Clients.

## Inputs
- Per client, by name or code: contracted days, fixed meetings and their days, the kind of work (deep work, meetings, a deliverable with a date)
- Your own fixed times, and when you think best
- The response windows and urgent routes in each client's charter
If you have none of this, I start from your clients' contracted days and one typical week, and mark the template as a first draft.

## Approach
Three calendar models from a public playbook for fractional executives (a dedicated day per client, morning and afternoon slots, a sprint cadence for one large deliverable) and the theme-day rule from a fractional marketplace's guidance: no more than two client contexts in a day. The judgment is to design for the switch, not for the hour. The failure this prevents is the chequerboard week, where every client gets a slice of every day and none gets your attention.

## Workflow
1. Ask at most three questions: which meetings are truly fixed and which could move; when in the day do you do your best thinking; which client has a deliverable in the next month?
2. Pick a model per client. Dedicated day for deep work; morning and afternoon slots where clients need you on the same days; a sprint cadence when one client has a large deliverable and the others can run in maintenance for two weeks.
3. Place fixed meetings first, then check each day against the rule: two client contexts at most. Where a day breaks it, propose the meeting to move, and to whom you would have to ask.
4. Put solo work for a client directly after that client's call, while the context is loaded. Add a focus block on each client day and protect it from short meetings.
5. Add one triage slot a day for the other clients' messages, inside their agreed response window, and a buffer you choose for overflow and for your own business.
6. Write the published version, one per client: their days, their channels, the response window, the urgent route. It shows nothing about your other clients.

## Output Format
```markdown
# Week Plan Across Clients
Valid from: [date] · Internal page; published versions below go to one client each
## Model per client
| Client (name or code) | Model | Why |
|---|---|---|
| [client] | [dedicated day / morning and afternoon slots / sprint cadence] | [kind of work] |
## The week
| | Mon | Tue | Wed | Thu | Fri |
|---|---|---|---|---|---|
| Morning | [client: focus block] | [..] | [..] | [..] | [..] |
| Afternoon | [client: call, then solo work] | [..] | [..] | [..] | [buffer] |
| Triage slot | [time] | [time] | [time] | [time] | [time] |
Days with more than two client contexts: [none, or which and what moves]
## Meetings to move
| Meeting | From | To | Ask whom |
|---|---|---|---|
| [meeting] | [day] | [day] | [role] |
## Published version, per client
[Client]: with you on [days] · reach me by [channel] · replies within [your window] on other days · urgent: [route]
## Decision
[You] adopt the template from [date] and ask [roles] to move the listed meetings by [date].
```

## Done When
- No day holds more than two client contexts, or the exception is named
- Solo work sits right after the matching client call
- There is one triage slot a day and a buffer you chose
- Each published version names one client only

## Quality Bar
- The week is built on your own best hours, not on a standard day
- Response windows come from each charter; I set none
- A meeting move is a request to a named person, never assumed
- Evenings and weekends are not used as spare capacity
- Each published version carries one client's days only, and no client's name, schedule or work is visible to another

## Next
Run frac-client-log (Client Log) to keep each client's context ready for the start of its day.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
