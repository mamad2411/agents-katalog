---
name: job-search
description: Finds open job postings across thousands of company career pages at once through the public Greenhouse, Ashby, Lever (and optionally Workable) job-board APIs plus remote-only boards, then filters them against the job seeker's exact role, seniority and location constraints. Use when someone is job hunting and wants openings found systematically, is tired of checking career pages one by one, has strict location limits (remote only, one city, cannot relocate, visa), keeps finding roles that turn out to be US-only or in the wrong city, or wants a weekly alert for new matching roles.
license: MIT
metadata:
  version: "1.1.0"
  repository: https://github.com/gagangulyani/job-search-skill
---

# Job Search

## Overview

Opening company career pages one at a time is hours of mechanical work. Most
startups and scale-ups host their jobs on a few ATS vendors that publish free,
unauthenticated JSON for every board, so a script can read thousands of
companies unattended. This skill pairs those scripts with the judgment the
scripts lack.

**Core principle: the filter is only as good as the bar, and the bar comes from
the job seeker, not from you.** A wrong bar produces confident wrong leads. An
empty result against the right bar is a finding, not a failure.

## Step 1: Intake (before any scanning)

Ask, in batches (use `AskUserQuestion` where available). Do not scan until every
row is answered. See [references/intake.md](references/intake.md) for ready-to-ask
wording and options.

| Must establish | Why it bites |
|---|---|
| Role family, and what it is **not** | "Head of Design" means UX/product design at most tech companies. A brand designer will drown in false hits. |
| Seniority words that count | Decides `require_any_seniority`. |
| **Exact** location bar: which cities onsite, remote from which regions | "In my country" is not "in my city". A past run ranked a wrong-city role as the best lead because the bar was the country. |
| Can they relocate? Even within their country? | Decides whether same-country cities are `onsite_ok` or `home_region`. |
| Work authorization, visa, languages | Becomes `extra_lock_phrases`. |
| Compensation floor, employment type (full-time, contract) | Postings rarely list pay; this guides manual review. |

If no human can answer (batch or subagent run): write the open questions to
`job-search/open-questions.md`, say you are blocked, and stop. Never fill a bar
with a plausible guess.

## Step 2: Write the config and test it on titles

Work in a folder the user owns, e.g. `./job-search/`. Copy
`assets/example-config.json` to `job-search/config.json` and replace every list
with the intake answers. Before a full scan, dry-run it on 10-15 real titles
and locations you expect to pass and fail, and show the user the output:

```bash
python3 SKILL_DIR/scripts/check_titles.py --config job-search/config.json \
  --titles "Lead Product Designer" "Product Designer" "Lead Graphic Designer" \
  --locations "Remote - Europe" "Porto, Portugal" "Remote (US)"
```

Fix the config until every line is what the user would say.

`SKILL_DIR` is the directory containing this SKILL.md (if your agent does not
say where that is, search the skills folders for `job-search/SKILL.md`). Run
every script through `python3` (Python 3.9+, no installs needed).

## Step 3: Scan

```bash
python3 SKILL_DIR/scripts/build_yc_list.py --out job-search/companies_yc.csv
python3 SKILL_DIR/scripts/scan_ats.py --config job-search/config.json \
  --companies job-search/companies_yc.csv --out job-search/results_yc.csv
python3 SKILL_DIR/scripts/scan_remote_boards.py --config job-search/config.json \
  --out job-search/results_remote.csv
```

Add the user's own target companies as another CSV (`name,slug_hint,website`;
template in `assets/companies-template.csv`) and scan it the same way.

The scanner is rate-limited on purpose (2 requests/second per vendor, 1 for
Lever). Workable is off by default because it rate-limits quickly; add
`--with-workable` (1 request per 3s) only for short lists of companies the user
names. The first run over the ~4,400-company YC list takes about two hours,
because it has to discover each company's board; it saves `board_cache.json`
and later runs take minutes. Run it in the background. Never lower the delays,
and if it prints a WARNING about refusals, wait a day before re-running.
If the scan exits with a connectivity ERROR, report that, not a result.

## Step 4: Verify every reviewable lead

Only three verdicts deserve a human's time: `ONSITE_OK`, `REMOTE_OK`,
`REMOTE_UNCLEAR`. Read the `reason` column first: it names the phrase that made
a role unclear (often pay-range boilerplate like "United States only"). For
each lead, **open the posting** and check (Ashby and Lever pages render with
JavaScript; if a fetch returns little text, read the job from the board API
URL instead):

- Still live (not 404 / "no longer accepting applications").
- Residency, citizenship, timezone or language requirements in the body text.
  "Remote" postings are often country-locked only in the body.
- The role is actually the user's role family, not a title collision.

Label every lead in what you hand over: **verified** (posting opened, date,
what you checked) or **unverified scan hit**. Never present a scan hit as
confirmed.

## Step 5: Report with coverage

Always state: companies scanned, how many had a live board, how many could not
be checked (errors), title matches by verdict, how many leads you verified, and
the blind spots in
[references/channels.md](references/channels.md). Then list leads, best first.

**When nothing clears the bar:** say so plainly, with the coverage numbers that
make it a real result and the closest near-misses (with the exact reason each
fails). Then offer structurally different channels from
[references/channels.md](references/channels.md) and hand the trade-off (relax
location, widen role, change channel) back to the user. Do not quietly loosen
the bar to make results appear.

## Step 6 (optional): Weekly monitor

`scripts/new_leads.py` diffs results against every lead seen before and appends
only new ones to `leads_log.md`. Durable scheduling (cron, launchd, GitHub
Actions) is in [references/monitoring.md](references/monitoring.md). Weekly is
enough: posting turnover, not scan frequency, is the limit.

## Hard rules

- **Never script LinkedIn, Indeed, Naukri, Glassdoor or similar.** They need an
  account, forbid scraping, and ban accounts. Recommend their native saved-search
  alerts instead.
- Keep `config.json`, results and logs out of any public repo. They describe a
  real person's job search.
- Adding an ATS or board: follow [references/extending.md](references/extending.md).

## Red flags: stop

- Scanning before the location bar is exact
- Treating "same country" as "same city" for someone who cannot relocate
- Presenting a `REMOTE_UNCLEAR` or `REMOTE_OK` hit without opening the posting
- Loosening the title or location filter because results came back empty
- Reporting zero results without coverage numbers
- Reporting a scan that printed network errors as a real result
- About to automate a login-walled job site

## Rationalizations

| Excuse | Reality |
|---|---|
| "I'll scan first and ask later" | You will anchor on the wrong bar. A real run crowned a wrong-city role "best lead". |
| "It says remote, so it works" | Remote roles are routinely US-only or EU-only in the body text. Open it. |
| "Bare 'Head of Design' is close enough" | At tech companies it is product/UX. Require the qualifier the user's craft needs. |
| "Zero results means the script is broken" | Check coverage numbers. Thousands scanned with zero hits is a market finding. |
| "LinkedIn has the most jobs, just scrape it" | It bans the user's account. Use its own alerts. |
| "No salary listed, can't judge" | Say so; suggest AmbitionBox/Levels.fyi/Glassdoor manually. Do not guess. |
