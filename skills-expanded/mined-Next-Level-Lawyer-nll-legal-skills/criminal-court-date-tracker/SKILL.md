---
name: criminal-court-date-tracker
description: Parse court notices, minute orders, and scheduling emails to track upcoming criminal case deadlines and flag hearing prep needs. Use whenever the user pastes a court notice, minute order, or scheduling email for a criminal case and wants deadlines tracked, or wants a consolidated view of upcoming court dates across multiple clients.
---

# Criminal Court Date Tracker

Parses scheduling notices into a tracked deadline list, flagging what prep each upcoming date requires.

## Workflow

1. **Extract from each notice**: case name, hearing type (arraignment, pretrial, motion hearing, trial, sentencing), date/time, and any conditions attached (e.g., "defendant must appear," filing deadlines tied to the hearing).
2. **Map hearing type to prep needs**:
   - Arraignment → plea entry, bail argument prep
   - Pretrial → discovery review status, motion filing deadlines
   - Motion hearing → brief filed? response due?
   - Trial → witness list, exhibit prep, motions in limine
   - Sentencing → sentencing memo, mitigation materials
3. **Flag any filing deadline that precedes the hearing** (e.g., motions due 10 days before a hearing date) as its own tracked item, not folded into the hearing date.
4. **If tracking multiple clients**, sort output by soonest date first, not alphabetically.

## Output format

```
## Upcoming Court Dates

| Date | Client/Case | Hearing Type | Prep Needed | Filing Deadlines |
|---|---|---|---|---|
```

Followed by, for the soonest 1-2 dates, a short prep checklist:
```
### [Client] — [Hearing type] on [date]
- [ ] [specific prep item]
```

## Notes

- Don't assume standard local filing deadline windows (e.g., "10 days before hearing") unless the user confirms the local rule — flag that it should be verified against local court rules if not stated.
- Always sort by urgency (soonest date) when tracking multiple cases — that's the point of this skill.
