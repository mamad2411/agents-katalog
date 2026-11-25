---
name: find-contacts
description: Find the recruiter AND the team's hiring manager for jobs, with a free Apollo search and free email building, and add them to the tracker. Triggers on "find contacts", "contacts for my picks", "find HR and hiring manager for [company]", "who should I email at [company]".
---

# Find contacts (recruiter + hiring manager)

Her favourite outreach: email BOTH the recruiter and the hiring manager of the team in the JD.
This skill finds those two people for free. It never sends anything.

## Hard rules
- **Never click "Access email" / "Access Mobile" / any reveal in Apollo** without her explicit OK for that person
  (it spends credits). Searching and reading names and titles is free. An email Apollo already shows unmasked
  (contact saved before) is free to use.
- Hunter / RocketReach only when the free steps fail (step 4). Check their credits first (Hunter `Get-Usage`,
  RocketReach `account`); a tool with 0 credits is skipped. Never Apollo API: Free plan blocks it.
- Never send email from here: drafting and sending is `/send-outreach`, with her approval.

## Which jobs
- Only a company/job she names in chat (or several). The Picks page is NOT used (she wants it unchanged), and no
  scheduled task drives Apollo.

## Step -1: Already applied? (always, before any search or credit)
Run `python .claude/skills/search/scripts/search_tracker.py "<Company>"` (and the job URL). If the company/role is
NOT in the tracker, ASK her first: "Have you already applied to / heard back from <Company> for this role?"
Her own applications aren't always logged (once, 2 Hunter credits were spent finding contacts for a role that had
already been rejected). If she was rejected for this role, stop: log it with `/mark-rejected` / `/new-job`
(status Rejected) instead of searching.
Also read the row's column E: if the person is already there, say so and whether an email is there. Names added
by the LinkedIn people finder have NO email (just a LinkedIn link): tell her "in the tracker, no email yet". When
an email is found for a name already in E, edit that entry to add the email (`add_hr_contact.py` refuses
existing names, so it would otherwise be lost).

## Step 0a: treg first (her rule 2026-11-18)
treg is a prepaid MCP connector that charges per call. Use it as the FIRST search while its balance is above $0.50.

**Cap (her rule 2026-11-23): treg is for 1 or 2 contacts per job, never more**: the recruiter and the team's
hiring manager. At most one `people.search` (plus one with `q` if the first finds nobody) and at most 2
`people.email.find` per job. Want more people? Use the free steps (Apollo browser search, pattern emails).

**Tell her at every switch (her rule 2026-11-23)**, in one line each, then move to the next source in order
treg -> Apollo (in-app browser) -> Hunter -> RocketReach -> LinkedIn search:
- treg balance after the calls (always), and "treg low ($X), switching to Apollo/Hunter" when TREG_LOW.
- "Hunter has 0 credits left, switching to RocketReach" / "RocketReach has no credits, switching to LinkedIn search".
- If every source fails: say so and that the job keeps an empty col E.
1. Read the treg MCP `balance`, then run
   `python ..\routines\treg_credit\treg_credit_alert.py <balance>`.
   - It prints TREG_OK: go to step 2.
   - It prints TREG_LOW: it has emailed her once. Skip treg here, and use it only as the very last step after
     Apollo, Hunter, RocketReach and LinkedIn, or not at all.
2. **People:** call `treg.people.search` with `{"company_domain": "<domain>", "limit": 25}`. This usually goes to
   free providers and costs $0. If they return nobody, add `q` with the job description's team, which costs about
   $0.02. Choose the hiring manager by business unit or team, not by title alone (a "Head of Software Development"
   can sit in a different business unit from the team in the job description).
3. **Emails:** call `treg.people.email.find` with `{"domain", "full_name"}` and these headers:
   - `X-Treg-Route-Domain-Match: strict`
   - `X-Treg-Route-Verify: true`
   - `X-Treg-Route-Max-Cost: 0.05`

   It costs about $0.005-0.013 and returns verdict valid or invalid. If it finds nothing, build the pattern guess
   (step 3 below) and check it with `treg.people.email.verify`, about $0.001 each. A "valid" on a catch-all domain
   is not proof, so tell her.
4. Report the cost of each call. If treg found the people and the emails, skip steps 0 and 2-4 below and go
   straight to step 5 (write back).

## Step 0: Apollo session check (when treg is low or found nobody)
Open https://app.apollo.io/#/home in the in-app browser. If it shows the login page (or the pane is closed/hidden),
stop and ask her to open the browser pane (Ctrl+Shift+B) and sign in; continue once she says done. Don't fall back
to Hunter/RocketReach just because Apollo is signed out: fallback is only for when Apollo finds nobody.

## Steps (per job)
1. **Read the JD** (`python cv_tailor.py jd "<url>"`) to get the team name (e.g. "Payments Risk") and city.
2. **Apollo free search in the in-app browser** (she is signed in to app.apollo.io; if the login page shows,
   ask her to sign in, then continue). If the pane is narrow, the results table is hidden: set the viewport to
   1400x900 with `resize_window`, and reset it to `desktop` when done. Use the people search URL with filters:
   `https://app.apollo.io/#/people?page=1&qOrganizationDomainsList[]=<domain>&personLocations[]=<Paris, France | France>&personTitles[]=...`
   - Recruiter: titles `recruiter`, `talent acquisition`, `talent partner`; Paris, then France, then Europe.
     If none, an HR business partner for tech/IT.
   - Hiring manager: titles `engineering manager`, `head of engineering`, `director of engineering`,
     `software development manager`, `vp engineering`; Paris, then France. Prefer the one whose title names the
     JD's team/product. Read results with `get_page_text`.
3. **Build the email for free** (no credits):
   `..\weekly-hr-agent\.venv\Scripts\python ..\routines\pick_contacts.py email "<Company>" "<Full Name>" --domain <domain> [--known "Name=email@domain"]`
   (run from the project root; pass any real email already seen, e.g. in the tracker's
   column E or unmasked in Apollo, as `--known`). Output `verified: "unverified"` = pattern guess.
4. **Only if step 2 finds nobody or step 3 prints NO_PATTERN / BAD_NAME:** Hunter (Email-Finder / Domain-Search),
   then RocketReach, per the global lead order. Hunter Email-Verifier on a guessed email only if quota allows;
   mark `verified: "valid"` only when Hunter says valid.
5. **Write back** to the tracker column E (if the job is in List.xlsx):
     `python .claude/skills/update-hr/scripts/add_hr_contact.py --company "<Company>" --name "<Name>" --title "<Title>" --email "<email>" --url "mailto:<email>"`
6. **Report** a table: Company | Role | Recruiter (email, verified?) | Hiring manager (email, verified?) | Source.
   Then offer `/send-outreach` drafts (one per person, domain-matched), nothing sent until she approves.
