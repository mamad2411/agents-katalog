---
name: buying-committee
description: Detective — maps who else matters at a target account (signer, hands-on user, fan, skeptic) from the people Pastel already found there, so outreach reaches more than one person. Use for "who else should I talk to at [company]", key or high-value accounts, or when a single contact went quiet.
---

# Buying committee — Detective

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Deals rarely hang on one person. When one lead at an account looks promising, find who else is part of the decision — among the people Pastel already knows.

## Steps

1. **Everyone Pastel knows at the account:** `pastel_query_leads(search="<company name>")`, then `pastel_get_details` for the matches. Pastel can't search LinkedIn for people it hasn't found — say so when the committee is incomplete, and suggest `market-map` to add an agent watching that company's team.
2. **Give each person a seat:**
   - **Signer** — the budget is theirs;
   - **Hands-on user** — does the work our product changes;
   - **Fan** — already reacted to something in public (their Pastel signal);
   - **Skeptic** — owns the tool or process we'd replace, and has most to lose.
3. **Order of approach:** start with whoever has the freshest signal, then work toward the signer. Talk to the skeptic before they hear about us secondhand. Explain the order in one line for this account.
4. **One angle per seat:** the signer hears about the business result, the hands-on user about their week, the fan about what they already said, the skeptic about what stays the same for them. Each angle goes to `message-writer` with the seat noted.
5. **No pile-on:** at most one first message per account per week, so two colleagues don't compare identical notes.

## Output

```
# Buying committee — [company]

| Seat | Person | Headline | Signal | Angle | Order |

Missing seats: [who we'd need and don't have]
Open questions:
```
