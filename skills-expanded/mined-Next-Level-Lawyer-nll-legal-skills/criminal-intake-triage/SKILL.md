---
name: criminal-intake-triage
description: Triage new criminal defense case inquiries by charge severity, custody status, prior record, and urgency, to help decide priority and next steps. Use whenever the user wants to review, score, or prioritize new criminal defense leads/intake, asks which new cases need immediate attention, or wants a custody-status/urgency check across multiple inquiries.
---

# Criminal Defense Intake Triage

Screens new criminal defense inquiries for urgency and case posture — custody status and upcoming deadlines drive priority here more than case "quality" in the way a civil intake would.

## Workflow

1. **Check custody status first, always.** In custody = highest urgency (bail/bond hearing timing matters immediately). Out on bail/summons = lower immediate urgency but still track court dates.
2. **Identify charge severity**: felony vs. misdemeanor, and specific charge category (violent, property, drug, DUI, white-collar, etc.).
3. **Flag upcoming deadlines**: arraignment date, bail hearing, next court date, any suppression motion or speedy trial deadline the user mentions.
4. **Note prior record** if provided (relevant to bail arguments and sentencing exposure) — don't speculate if not given.
5. **Note case-specific red flags/strengths**: search/seizure issues, identification issues, alibi, witness cooperation, evidence quality — flag briefly, don't analyze legal merits in depth (that's discovery-summarizer's job once discovery is in hand).
6. **Produce a triage summary** prioritized by urgency, not alphabetically or by intake order.

## Output format

```
**[Name]** — [Charge(s)] ([felony/misdemeanor])

- **Custody status:** [in custody ⚠️ / released on bail / summons]
- **Next deadline:** [date and event — arraignment/hearing/etc.]
- **Prior record:** [noted if provided, else "not provided"]
- **Initial flags:** [search issue, ID issue, cooperating witness, etc. — or "none noted yet"]
- **Priority:** [Urgent / High / Standard] — [why]
```

Close multi-case triage with a one-line prioritized action list (who needs a call today vs. this week).

## Notes

- Custody status overrides every other factor for urgency ranking — a minor charge with someone in custody outranks a serious charge with someone out on bail, for purposes of immediate action.
- Don't assess guilt, innocence, or case strength beyond noting the specific factual flags provided — this is triage, not case theory development.
