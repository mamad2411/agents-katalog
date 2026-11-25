---
name: personal-crm
description: Maintains a relationships.csv personal CRM — logs touches, surfaces overdue follow-ups by cadence, and drafts warm check-in messages for the user to send. Use when the user says "log that I talked to X", "who am I overdue with", "personal CRM", "help me keep in touch", "follow-up check", or after meeting someone worth staying connected to. Don't use for sales pipelines — use pipeline-tracker — or for cold prospecting — use cold-outreach-sequencer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Relationships, CRM, Networking]
    related_skills: [pipeline-tracker, cold-outreach-sequencer, meeting-notes-actions]
---

# Personal CRM

Keeps the relationships that matter from silently expiring, using nothing fancier than `relationships.csv`: who they are, the context that makes the relationship real, when you last touched, how often you intend to, and what's next. The skill logs touches, computes who's overdue, and drafts check-ins that sound like a human who remembers — **drafts only; the user sends every message personally**, because outsourced warmth isn't warmth.

## When to Use

- After a call, coffee, or good conversation: "log that I caught up with Sarah".
- "Who am I overdue with?", "who should I ping this week?".
- Adding someone new worth staying in touch with; drafting a check-in.
- **Not for:** deal tracking — use `pipeline-tracker`. Not for messaging strangers at scale — use `cold-outreach-sequencer`. Not a contacts-app replacement (no phone numbers/emails needed here — context is the payload).

## Quick Reference

| Action | Command / Call |
|---|---|
| File format | `relationships.csv` header: `name,context,last_touch,cadence,next` (cadence in days; dates ISO) |
| Initialize | `echo "name,context,last_touch,cadence,next" > relationships.csv` (only if missing) |
| Look someone up | `grep -i "sarah" relationships.csv` |
| Log a touch | update that row's `last_touch` to today and `next` to the new intention |
| Overdue scan | python3 stdlib script (Procedure step 4) |
| Cadence guide | inner circle 30 · strong ties 60 · warm network 90–180 |

## Procedure

1. **Precheck** — locate `relationships.csv` (ask once, remember). If missing, offer to create it and seed it with 5–10 people the user names. This file is personal data: it stays local, never gets pasted into other tools, and rows are only removed at the user's explicit request.
2. **Log a touch** — grep for the person (fuzzy: try first name, last name). Update their row: `last_touch` = today (`date +%F`), and refresh `next` with the concrete follow-up the conversation produced ("intro to Dana promised", "ask about the fundraise in Oct"). If they're not in the file, gather `context` — how you met + what you talked about + why they matter — the field that makes a future check-in warm instead of generic. Show the updated row before writing.
3. **Confirm the write** — `grep` the row back; echo it in one line.
4. **Overdue scan** — run:

   ```bash
   python3 - <<'EOF'
   import csv, datetime as dt
   today = dt.date.today()
   rows = sorted(csv.DictReader(open('relationships.csv')),
                 key=lambda r: dt.date.fromisoformat(r['last_touch']))
   for r in rows:
       due = dt.date.fromisoformat(r['last_touch']) + dt.timedelta(days=int(r['cadence']))
       over = (today - due).days
       if over >= 0:
           print(f"OVERDUE {over:>3}d  {r['name']} — last {r['last_touch']} (cadence {r['cadence']}d) — next: {r['next']}")
       elif over >= -7:
           print(f"soon   {-over:>3}d  {r['name']}")
   EOF
   ```

   Success: overdue people ranked by how overdue, plus a "due within 7 days" preview.
5. **Draft check-ins (drafts only)** — for the top overdue people (cap at 5 per session — sending 20 check-ins in one day reads as a mail merge), draft a short personal message built from their `context` and `next` fields: reference the specific last thread ("did the Dana intro land?"), offer something or ask one real question, no "just checking in" filler. **The agent never sends these** — output as paste-ready text; the user personalizes and sends from their own accounts.
6. **Deliver** — the template: what was logged, who's overdue, drafts, and one nudge for the week.

## Output Template

```
# Personal CRM — {date}

**Logged:** {Name} — touched {today}, next: {follow-up}

## Overdue ({n})
| Who | Overdue by | Last touch | The thread to pick up |
|---|---|---|---|
| {Name} | {n}d | {date} | {next field} |

## Check-in drafts (you send — I don't)
### {Name}
> {2–4 sentence draft referencing their specific context and open thread}

Due soon: {names, days}.
**This week's one move:** {single highest-value reconnection and why}.
```

## Pitfalls

- **Generic check-in drafts** — "Hi X, just checking in, hope you're well!" is worse than silence. Recovery: every draft must reference something only this relationship contains (from `context`/`next`); if those fields are too thin to write a specific message, the draft step becomes "enrich the row first".
- **The file becomes a guilt list** — 40 overdue rows and the user stops opening it. Recovery: cap drafts at 5, lead with the single best reconnection, and suggest honest pruning — moving someone to a 180-day cadence (or removing them at the user's request) is maintenance, not failure.
- **Date/cadence corruption breaks the scan** — a `7/14` date or `monthly` in the cadence column throws `ValueError`. Recovery: catch it, `grep -n` the offending row, fix the format (ISO dates, integer days) with the user, rerun; never skip rows silently.
- **Agent sends the check-ins** — relationship messages from a robot in the user's name is the fastest way to burn trust. Recovery: no send calls, ever; drafts are text output only.
- **Overwriting a row loses history context** — careless edits blank the `context` field. Recovery: show the before/after row at every update; `context` only ever grows or is deliberately edited by the user.

## Verification

- [ ] Updated row echoed back and matches what the user reported
- [ ] Overdue list comes from the python3 scan output, not estimation
- [ ] Every draft cites a specific detail from that person's `context`/`next` fields
- [ ] Zero messages sent; drafts delivered as text only; ≤5 drafts this session
- [ ] Header intact and no rows removed without an explicit user request
