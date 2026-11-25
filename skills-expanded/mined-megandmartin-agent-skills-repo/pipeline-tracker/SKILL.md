---
name: pipeline-tracker
description: Maintain a lightweight CRM in a local leads.csv (stage, value, next_action, last_touch) using python3 stdlib, and report a pipeline summary on demand. Use when the user asks to "add a lead", "update the pipeline", "move X to negotiation", "what's my pipeline worth", "who needs follow-up", or wants a simple CRM without a SaaS tool. Don't use for researching a lead (lead-research-dossier) or billing a closed-won deal (invoice-runner).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Sales, CRM, Pipeline]
    related_skills: [lead-research-dossier, cold-outreach-sequencer, invoice-runner]
---

# Pipeline Tracker

A zero-dependency CRM: one `leads.csv` in the project folder, edited safely with python3's stdlib `csv` module, plus an on-demand pipeline summary (totals by stage, overdue follow-ups). No SaaS, no lock-in — the file is the database.

## When to Use

- User wants to add, update, or move a lead through stages.
- User asks "what's in my pipeline?", "total pipeline value?", or "who's gone cold?"
- After outreach (`cold-outreach-sequencer`) or a call, to log the touch and next action.
- **Not for:** researching a lead (`lead-research-dossier`) or billing a closed-won deal (`invoice-runner`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Init file (once) | `python3 -c "import csv,os; os.path.exists('leads.csv') or csv.writer(open('leads.csv','w',newline='')).writerow(['name','company','stage','value','next_action','last_touch'])"` |
| View all | `python3 -c "import csv; [print(r) for r in csv.reader(open('leads.csv'))]"` |
| Add / update / summary | python3 heredoc scripts in the Procedure |
| Valid stages | `new → contacted → replied → call → proposal → negotiation → won \| lost` |
| Backup before write | `cp leads.csv leads.csv.bak` |

## Procedure

1. **Precheck** — `command -v python3`; locate `leads.csv` in the working directory (ask the user where it lives if not found). If absent, run the init one-liner from Quick Reference. Success: file exists with the 6-column header.
2. **Backup** — before any write, `cp leads.csv leads.csv.bak`. Cheap insurance.
3. **Add a lead** — run:
   ```bash
   python3 - "$NAME" "$COMPANY" "$VALUE" "$NEXT" <<'EOF'
   import csv, sys, datetime
   name, company, value, nxt = sys.argv[1:5]
   rows = list(csv.reader(open('leads.csv')))
   if any(r and r[0].lower()==name.lower() and r[1].lower()==company.lower() for r in rows[1:]):
       sys.exit(f"DUPLICATE: {name} @ {company} already tracked")
   rows.append([name, company, 'new', value, nxt, datetime.date.today().isoformat()])
   csv.writer(open('leads.csv','w',newline='')).writerows(rows)
   print(f"Added {name} @ {company} (stage=new, value={value})")
   EOF
   ```
   Success: "Added ..." printed; duplicates rejected.
4. **Update a lead** (stage move, new next_action, touch logged) — same pattern: load all rows, match on name+company (case-insensitive), set `stage`/`value`/`next_action`, always refresh `last_touch` to today, rewrite the whole file with `newline=''`. Reject stage values outside the Quick Reference list. Success: script prints the before → after line.
5. **Summary on demand** — run:
   ```bash
   python3 <<'EOF'
   import csv, datetime, collections
   rows = list(csv.DictReader(open('leads.csv')))
   by = collections.defaultdict(lambda: [0, 0.0])
   for r in rows:
       by[r['stage']][0] += 1
       try: by[r['stage']][1] += float(r['value'] or 0)
       except ValueError: print(f"WARN bad value: {r['name']}: {r['value']!r}")
   openv = sum(v for s,(c,v) in by.items() if s not in ('won','lost'))
   print(f"Pipeline: {len(rows)} leads | open value ${openv:,.0f}")
   for s,(c,v) in sorted(by.items()): print(f"  {s:12} {c:3}  ${v:,.0f}")
   today = datetime.date.today()
   stale = [r for r in rows if r['stage'] not in ('won','lost')
            and (today - datetime.date.fromisoformat(r['last_touch'])).days > 7]
   print("Needs follow-up (7+ days):")
   for r in stale: print(f"  {r['name']} @ {r['company']} — {r['next_action']} (last: {r['last_touch']})")
   EOF
   ```
6. **Deliver** — present the summary using the Output Template; on writes, confirm what changed and that the backup exists.

## Output Template

```
## Pipeline Summary — <date>
Total leads: N | Open pipeline value: $X
| Stage | Count | Value |
|---|---|---|
### Needs follow-up (no touch in 7+ days)
- <name> @ <company> — next: <next_action> — last touch <date>
### Changes this session
- <added/updated rows, before → after>
```

## Pitfalls

- **Commas or quotes inside fields corrupt the file** — hand-editing "Acme, Inc." with `echo >>` breaks the column count. Recovery: always write via the `csv` module (it quotes correctly); if the file is already broken, find the bad row with a `len(row) != 6` check and repair from `leads.csv.bak`.
- **Duplicate leads inflate the pipeline** — the same prospect added twice doubles their value in totals. Recovery: the add script's name+company check blocks this; if dupes exist, keep the row with the later `last_touch` and delete the other.
- **Non-numeric `value` breaks the summary** — "$5k" or "TBD" won't `float()`. Recovery: the summary warns instead of crashing; store plain numbers (5000, not $5k) and fix flagged rows immediately.
- **Invalid stage names fragment reporting** — "Negotiating" vs "negotiation" become two buckets. Recovery: validate against the canonical stage list on every write; normalize to lowercase before saving.

## Verification

- [ ] `leads.csv` still parses: every row has exactly 6 columns
- [ ] All stages in file are from the canonical list; all values are numeric
- [ ] `last_touch` updated to today on every row touched this session
- [ ] `leads.csv.bak` exists from before this session's writes
- [ ] Summary totals match a manual spot-check of 2–3 rows
