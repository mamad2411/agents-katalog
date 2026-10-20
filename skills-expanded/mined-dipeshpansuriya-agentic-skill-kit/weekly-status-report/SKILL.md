---
name: weekly-status-report
description: Turn weekly notes, trackers or exports into a RAG status report with metrics and week-over-week carry-over. Use when the user asks for a weekly report, weekly status update, or W-number progress summary for a manager, leadership or client.
---

# Weekly Status Report (Advanced)

## 0. Inputs this skill accepts
- Rough notes (pasted text, half-sentences)
- Tracker exports: Excel/CSV, Jira/Azure DevOps lists
- Emails or chat threads pasted in
- **Last week's report** (optional, used for week-over-week comparison)

If more than one source is given, merge them. When sources disagree, the most recent one wins, and the conflict is flagged under "Needs input".

## 1. Before writing: settle 3 things
| Setting | Default if not stated | Options |
|---|---|---|
| **Audience** | Manager | Manager · Leadership · Team · Client (see `references/audiences.md`) |
| **Channel** | Email | Email · Teams/Slack · Document |
| **Week** | Current ISO week | Run `python scripts/week_info.py [YYYY-MM-DD]` for week number + date range |

Ask **one** short question only if the audience is unclear *and* it changes the content (e.g. a client report). Otherwise use the defaults and state them at the top.

## 2. Steps
1. Read every input once before writing anything.
2. Extract each item into: **Done · In progress · Blocked/Risk · Next week · Metric · Decision needed**.
3. For each item capture: owner, date/ETA, IDs (ticket, AWB, PO), numbers, exactly as written.
4. Merge duplicates across sources; drop chit-chat.
5. Assign **RAG status** per workstream and overall, using `references/rag-rules.md`.
6. If last week's report is provided, compare:
   - Items promised last week under "Next week": delivered, slipped, or dropped?
   - Metrics: show change (▲/▼ and value)
   - Risks: new, still open, or closed
7. Adapt depth and tone to the audience (`references/audiences.md`).
8. Write using `templates/report-template.md`, then format for the channel (step 4).
9. Run the self-check (step 5) and fix before returning.

## 3. Rules
- **Branding only on request:** use plain, neutral formatting by default. Apply a company or brand design skill (colours, fonts, logo, templates) only when the user names that skill or brand in the request; never pick one automatically.
- **Never invent** owners, dates, numbers or status. Use "TBD" and list the gap under *Needs input*.
- Keep IDs, names and figures **exactly** as given.
- Length: Manager/Team ≤ 1 page (~350 words); Leadership ≤ 150 words; Client ≤ 250 words.
- Lead with outcomes, not activity ("Cut dwell time 12%", not "Worked on dwell time").
- Every Red/Amber item must have: impact + owner + next action + date.
- Slipped items from last week must appear, not silently disappear.
- Client audience: no internal names of blockers, no internal tooling, no blame.
- Empty section: write "None". Never delete a section.
- Plain language, active voice, no filler ("it was discussed that…").

## 4. Channel formatting
- **Email:** Subject line `[Status] <Team>, W<nn>: <Overall RAG> | <one-line headline>`, then the report.
- **Teams/Slack:** TL;DR + RAG line + max 5 bullets; full detail collapsed or linked.
- **Document:** Full template with tables.

## 5. Self-check (must pass before returning)
- [ ] Every input item appears somewhere or was deliberately dropped as noise
- [ ] No invented owners/dates/numbers
- [ ] Every Red/Amber has impact + owner + action + date
- [ ] Last week's "Next week" items all accounted for (if provided)
- [ ] Length within the audience limit
- [ ] RAG matches `references/rag-rules.md`
- [ ] "Needs input" lists every TBD

## 6. Output
After edits, rerun `evals/test-cases.md` (see benchmark-skill).

Return the report, then a short **"Assumptions & Needs input"** block (defaults used, TBDs, conflicts) *outside* the report so the user can fix gaps before sending.
