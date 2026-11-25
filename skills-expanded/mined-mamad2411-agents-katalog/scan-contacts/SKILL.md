---
name: scan-contacts
description: Find contacts at a target company and rank them for outreach — uses Exa search (no LinkedIn login) + a session-side evidence gate and ranking by role proximity, warm-tie, reachability, and personalization surface
argument-hint: "<company-name> [count]"
user-invocable: true
allowed-tools: Read(*), Glob(data/*), Write(data/networking.md), Bash(*)
---

# Scan Contacts — Exa-based Outreach Target Finder

Finds real people at a target company via **Exa web search** (retired the
Selenium LinkedIn scraper — no password, no ban risk, 2026-07-15), then verifies
and ranks them **in-session** for cold outreach. Ranking targets the top role
in `data/goals.md`, not a fixed lane.

Architecture: the tool (`tools/contact_finder.py`) does **deterministic
acquisition only** — Exa fetch, `/in/` filtering, name-from-title extraction,
URL dedup, and a coarse company-mention bucket. It emits **UNRANKED** JSON. This
skill does the judgment layer: an **evidence-span current-employment gate**
(quote-or-drop) and the ranking. There is no in-tool LLM and no
`ANTHROPIC_API_KEY` dependency.

Use after `/research-company` — outreach lands better with a dossier loaded.

## Arguments

- `$ARGUMENTS` (required): company name (quoted if multi-word); optional integer count (default 20).
  - `/scan-contacts "Acme AI"` — ~20 profiles
  - `/scan-contacts "Acme AI" 30`

If no arguments, show the usage block above and stop.

## Prerequisites

Only one secret is needed, in `.env` at the repo root:
- `EXA_API_KEY` — for Exa search (already present for `/research-company`).

No LinkedIn credentials, no Chrome, no chromedriver. (Exa Websets Pro is NOT
required — this uses plain Exa `/search`.)

## Instructions

### Step 1: Profile guard

The tool enforces this itself, but confirm `data/profile.md` and `data/goals.md`
exist with real content. If the tool returns `"error"` mentioning a missing/
placeholder file, relay it and stop (tell the user to run `/import-cv` or fill
`data/goals.md`).

### Step 2: Run the finder

```bash
PYTHONIOENCODING=utf-8 python3 tools/contact_finder.py --company "<company>" --num <count>
```

Parse the JSON. Key fields:
- `exit_reason`: `ok` | `no_results` | `all_filtered` | `exa_error`
- `counts`: `raw_results`, `profile_results`, `candidates_kept`,
  `needs_manual_check`, `dropped_no_name`
- `candidates[]`: people whose bio mentions the company in a work context.
- `needs_check[]`: real `/in/` profiles with a parseable name but no clear
  work-context company mention (ambiguous-name collisions, thin snippets, or
  people the deterministic filter could not confirm).

**Honest-signal handling — do NOT report "no contacts" on a tooling miss:**
- `exit_reason: exa_error` → relay `exa_errors`; it's an API problem, not an
  empty company. Offer to re-run.
- `no_results` / `all_filtered` → say Exa's index returned nothing usable for
  this company (try a more specific or alternate company name), NOT "nobody
  works here."
- If `candidates_kept` is low but `needs_manual_check` is high, the company name
  is probably ambiguous (a common first name, or a same-prefix different
  company). Mine `needs_check` in Step 3.

### Step 3: Evidence-span employment gate (MANDATORY — the fabrication guard)

The tool hands you strangers you cannot sanity-check from memory. Before ranking,
gate every person on **provable CURRENT employment at THIS company**:

1. For each `candidate` AND each `needs_check` record, read `bio_text`.
2. **Quote-or-drop:** keep the person ONLY if you can quote a specific bio
   sentence showing they work at the target company **now** — e.g.
   `"Agent Deployment Strategist - Acme (Current)"` or `"Head of Ops at Acme"`.
   Record that quote as their `evidence`.
3. **Current vs. past:** LinkedIn Experience lists prior employers. A sentence
   showing they *used to* be at the company (a dated past role, "formerly",
   ending date) does NOT pass. Drop it.
4. **Right company:** reject same-prefix different companies (e.g. target "Acme"
   ≠ "Acme Sciences") and people merely *named* like the company.
5. If you cannot produce a current-employment quote, DROP the person — never
   guess, never surface them. This is the never-fabricate rule pointed at people
   the user can't cross-check. (Origin: the role-inference failure family,
   CLAUDE.md Hard Rules.)

Report how many you dropped at this gate and why (one line).

### Step 4: Rank the survivors (session judgment)

Score each gated person 1-10 on four dimensions, reading `data/profile.md` for
the user's background and `data/goals.md` for the target role:

- **role_proximity** — decision authority for the target-role hire (Founder/CEO 10,
  C-suite 8, Head-of-function 6, Director 5, Manager 4, IC 3).
- **warm_tie** — shared institution with the user: cross-reference the schools
  and past employers listed in `data/profile.md` against the person's bio. Folds
  in education prestige. A genuine shared alma mater or employer is the single
  strongest cold-outreach signal. (Do not hardcode the user's institutions here —
  read them from `profile.md` each run.)
- **reachability** — how approachable/open: public reach (`reach` field —
  followers/connections), recent public activity, seniority-approachability.
- **personalization_surface** — how much concrete, specific material the bio
  gives you to write an authentic "why you / why now" (named projects, posts,
  a distinctive path). Low surface = a generic email; high surface = a sharp one.

`aggregate` = sum (max 40). Also give `overall` (1-10) holistic — penalize thin
profiles. Do NOT compute a network-degree or mutuals score; that data is
login-gated and unavailable (it lived in the old Selenium tool).

### Step 5: Display ranked results

```
## Contacts — [Company]
Exa: N raw / M profiles | gated-in: G | dropped at evidence gate: D

Rank | Name | Role | Prox | Warm | Reach | Pers | **Total** | LinkedIn
-----|------|------|------|------|-------|------|-----------|--------
  1  | Jane Smith | Head of Deployment | 6 | 9 | 7 | 8 | **30** | linkedin.com/in/janesmith
```

Then the **Top 3**, each with one line on *why* they rank high AND their
`evidence` quote (proof of current employment). Note the top `overall`.

### Step 6: Offer to add contacts to networking

Ask: `Add any of these to data/networking.md? (names/numbers, or Enter to skip)`

On selection, read `data/networking.md` and add a row per contact:
- **Name**, **Company** (the scanned company), **Role/Title** (from headline)
- **Relationship**: `target` · **Source**: `exa-scan`
- **Last Interaction**: `—`
- **Notes**: `[LinkedIn](url) | Warm: X | Reach: Y/10 | Total: Z/40 | evidence: "<quote>"`

Write the file and confirm: "Added N contact(s) to data/networking.md."

Do NOT write `Deg:`/`Mut:` fields — that login-gated network data no longer
exists.

### Step 7: Suggest next action

```
Top contacts to reach out to:
1. [Name] — [Role] ([Total]/40) → /cold-outreach "[Name]" "[Company]"
...
Run /research-company "[Company]" first if you haven't — outreach lands better with a dossier.
```

## Score interpretation

| Total /40 | Recommendation |
|---|---|
| 32–40 | Priority — reach out now |
| 24–31 | Strong target |
| 16–23 | Moderate — if others are exhausted |
| < 16 | Skip unless a specific reason |

## Notes

- The Selenium scanner (`tools/linkedin-scanner/`) is retired/dormant; see its
  `DEPRECATED.md`. Do not use it.
- Public-repo PII gate: examples here are placeholders; real names appear only at
  runtime. Run `/audit-pii` before committing any change to this skill or tool.
