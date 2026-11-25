---
name: audit-personal-brand
description: A reproducible audit of what a stranger actually finds when they look you up, run against one named audience and one named decision — surface enumeration in two passes (an unpersonalised one you run, a logged-out one the person runs), a claim ledger in which every assertion is either backed by an artifact a reader can open or cut, an inventory of the strongest evidence you own that is currently invisible, the NDA and private-repository case, and a prioritised list of at most five actions. Use before a job search, a funding round, a CFP submission or a collaboration approach, when what a stranger finds no longer matches what you can do, or when your best work is invisible. Produces docs/growth/personal-brand.md.
allowed-tools: Read Grep Glob Bash Write Edit WebFetch WebSearch mcp__plugin_foundry-core_foundry__blackboard_write mcp__plugin_foundry-core_foundry__contract_validate mcp__plugin_foundry-core_foundry__memory_search mcp__plugin_foundry-core_foundry__memory_write
argument-hint: "[--for hiring|clients|collaborators|speaking]"
user-invocable: true
agent: foundry-growth:personal-brand-strategist
model: sonnet
effort: medium
metadata:
  foundry.vertical: growth
  foundry.io: "requirement.v1 -> review.v1 + docs/growth/personal-brand.md"
license: Apache-2.0
---

# Audit a personal brand

An audit, not a rewrite. The deliverable is a dated record of what a stranger finds, a ledger in
which every public claim is either evidenced or cut, and **at most five actions** ranked by what
they change for one named decision. A run that ends with forty tasks has produced a backlog, not
an audit, and the backlog will not be done.

The order is fixed: **audience and decision → surface enumeration → claim extraction → claim
verification → invisible-evidence inventory → prioritisation → write-up**. Every step done out of
order inverts the rule this skill exists to protect: the evidence decides the copy, never the
reverse. Write a bio before the ledger and you have written a claim looking for a justification.

**The binding rule.** Every claim on every surface ends this run in exactly one of two states:
`EVIDENCED` — a URL a stranger can open, without an account, that substantiates it — or `CUT`.
There is no third state. "Soften it" is not available: a vaguer version of an unsupported
assertion is the same assertion, harder to falsify.

## When not to use this

- **The subject did not ask for it.** This audits the identity of the person running it, or of
  someone who requested the audit and is in the session to answer for their own claims. It is not
  a profiling tool. Do not run it on a third party, do not collect anyone's contact details, and do
  not assemble a file on a person who has not asked for one. Reading what a stranger would see
  about *yourself* is the method; assembling the same about someone else is a different activity
  and this skill refuses it by name rather than scoping it down.
- **There is no work yet.** An audit of someone with nothing to point at produces copy hunting for
  evidence. Say so and stop; the next action is shipping one publishable artifact, not editing a
  profile.
- **The subject is a project, not a person** — its claim, its non-audience, its alternatives →
  `position-project`; announcing it → `plan-launch`; keeping people reading it → `build-audience`.
- **The ask is one CV or cover letter for one application.** Route the dates, titles and employers
  through the claim ledger here first, then hand the document itself to
  `foundry-research:technical-writer`.
- **The ask is capital, not credibility** → `prepare-fundraise`. The ask is a co-founder or a
  contractor → `find-collaborators`.
- **The question is what a contract lets you publish** — NDA, non-compete, IP assignment,
  publication consent → `foundry-legal`, unread and undebated. Do not reason about enforceability.
- **The audit ran recently and nothing changed.** Re-run only the surfaces whose `checked on` date
  precedes the next decision date; a repeat of an unchanged audit is not a finding.

## Step 1 — one audience, one decision, one date

`--for` selects the lens; it does not replace the statement. Write, in `docs/growth/personal-brand.md`:

```
AUDIENCE: <named roles or organisations — not "the industry", not "everyone in tech">
DECISION: <the decision they make about this person: interview / shortlist / accept the talk / reply>
BY:       <YYYY-MM-DD — the date the decision is made or the deadline falls>
```

The lens changes what counts as evidence, so choose deliberately:

| `--for` | The stranger | Surface the audit weights first | The failure this lens must rule out |
|---|---|---|---|
| `hiring` | a hiring manager or recruiter screening a list | the code host profile and the CV | a title that contradicts the record; a dead link |
| `clients` | a buyer with a budget and a deadline | a site you own, and its work section | no evidence of shipped, finished work for someone else |
| `collaborators` | a peer deciding whether to spend months with you | a repository, a review, a design document | over-claimed credit on shared work |
| `speaking` | a programme committee reading proposals | the proposal itself, then the speaker field | no evidence you did the thing you propose to talk about |

The third column is a **working assumption about where to start the audit, not a claim about how
anyone reads**. Confirm it against one person who has actually made this decision recently — ask
which surface they opened, record the answer and the date — and re-rank if they contradict it.
Never write the assumption into the deliverable as if it were known, and never assert an ordering,
a screening time, a rejection rate or a review policy you have not read on a page you fetched.

**Gate:** if `AUDIENCE` cannot be written as a list of roles or organisations, stop. Steps 2–7 do
not run against "everyone", because every prioritisation decision below is made by asking which
of two actions matters more *to that audience*, and there is no answer for an unnamed one.

## Step 2 — enumerate the surfaces, in the stranger's order

Not an impression. A procedure with a dated record, repeatable in six months as a diff.

**Two instruments, and every row records which one produced it.** Do not conflate them:

- **What you run.** `WebSearch` on each query in the set, then `WebFetch` on every result you
  intend to record. This returns an unpersonalised result set — closer to a stranger's view than
  the person's own signed-in browser, and *not identical to it*: it varies by region and by day.
  Write that limitation into the deliverable. Never present your result set as "what everyone
  sees", and never record a result you did not open.
- **What the person runs.** The same query list, from a logged-out browser in a clean profile, in
  the region their audience is in, pasting back anything you did not see. Theirs is the pass that
  catches personalisation and region skew; yours is the pass that is reproducible in six months.

Until the second pass arrives, its rows are absent and every criterion depending on them is marked
`UNVERIFIED` — not estimated, not inferred from the first pass.

Per-surface procedure, what to record for each, and the query set to run:
`references/surface-audit-procedure.md`.

The repository-side half is cheap and exact — run it first:

```bash
git log --all --format='%an <%ae>' | sort -u          # identities used in THIS repository, not all of them
command -v gh >/dev/null && gh auth status >/dev/null 2>&1 || echo 'gh unavailable — see Degradation'
gh api users/<login> --jq '{name,bio,blog,company,public_repos,created_at}'
gh api users/<login>/repos --paginate \
  --jq '.[] | select(.fork==false) | [.name,.pushed_at,(.description//"")] | @tsv' | sort -k2
```

Record one row per surface found, in the order the stranger meets them (search result rank first,
then platform-internal search, then anything linked from those):

| # | surface | URL | found by | mine? | last updated | what it claims about me | helps / harms / neutral for the DECISION |
|---|---|---|---|---|---|---|---|

Five findings this table must surface explicitly, because each forces a different action:

1. **A dead top result** — an abandoned profile ranking above the live one. Usually the cheapest
   fix in the audit, because it is an edit to an account the person already controls.
2. **A contradiction across surfaces** — two titles, two specialities, two date ranges. Resolve it
   to one true version everywhere. You do not get to assume the reader resolves it in your favour,
   and you will not be there to explain which one was current.
3. **A claim with no reachable artifact.** Counted in step 3; this count is the headline metric.
4. **A stale artifact behind a live claim** — a linked repo whose last commit predates the claim,
   a demo returning an error, a paper behind a paywall with no accepted-manuscript copy.
5. **Nothing at all.** An empty result set is a finding, not a blank slate: it means the decision
   will be made from a CV alone, and the audit's actions all become "create one surface".

Record the exact queries and the date. **Never assert a platform's ranking behaviour, field
limits, algorithm or posting rules** — read the page now and cite it as `(checked <URL> on
YYYY-MM-DD)`, or say nothing.

## Step 3 — extract every claim into the ledger

Read each surface and split its text into atomic claims. A claim is any sentence a stranger could
try to check: a role, a duration, a technology used in anger, an outcome, a number, a credential,
an affiliation, an award, a client, a talk, a publication. Adjectives that assert standing
("senior", "lead", "expert", "trusted by") are claims. Adjectives about taste are not.

Write `docs/growth/personal-brand.md` § claim ledger, one row per claim:

| id | surface | claim verbatim | type | evidence URL | evidence kind | verdict |
|---|---|---|---|---|---|---|
| `C-01` | code host bio | "led the payments migration" | role | — | — | pending |

`type` ∈ role / duration / outcome / metric / credential / affiliation / artifact.
`evidence kind` ∈ runnable / readable / third-party record / measured result — the four ranks in
`references/portfolio-evidence.md`, listed strongest first. A measured result is admissible only
with the measurement artifact attached; without it the row has no evidence kind and is `CUT`.

**Gate:** the ledger is complete when the number of rows equals the number of checkable sentences
across all surfaces in step 2. Undercounting here is how an unsupported claim survives the audit,
so extract from the raw text rather than from your summary of it.

## Step 4 — the verification pass, one row at a time

For each row, find the artifact a stranger can open **without an account and without asking**. Then
check it, on this run, and record the result:

```bash
curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' -L "<evidence-url>"   # non-2xx: not evidence
```

**2xx is necessary, not sufficient.** A login wall, a consent interstitial and a paywall all return
200. Fetch the body too and confirm the artifact itself is in it; where the second, logged-out pass
of step 2 covers this URL, confirm there as well. A link that opens only for someone with an
account, or only for you, is `CUT` like any other unreachable claim.

For a `runnable` claim, clone into a clean directory and execute the documented command; record the
command and its exit status. A README that has never been followed on a clean machine is a claim,
not evidence.

Then assign the verdict:

- **`EVIDENCED`** — the URL returns 2xx, the body served to someone without an account contains the
  artifact, and what the artifact contains substantiates *this* claim. A repo that exists does not
  evidence "led"; the commit history, the design document or the release notes might.
- **`CUT`** — no artifact, or the artifact does not support the claim. Delete the sentence. Record
  the deletion with its date and what would restore it.
- A **rewritten** claim is a `CUT` plus a new row that must itself reach `EVIDENCED`. The identity
  `EVIDENCED + CUT == total` therefore holds at the end of every run, and is checkable by grep.

Five categories are cut on sight, without negotiation, and each removal is a `finding.v1`:

- **Inflated title** — "lead" for work you did as one of five, "architect" for a design you
  implemented but did not shape, "founder" of something with no other participants. If the commit
  history, the contract or the payslip disagrees with the bio, the bio changes.
- **Uncounted metric** — a user count nobody counted, a latency gain nobody measured, "used at
  scale". A number ships only with the artifact that produced it and the date it was produced.
- **Unverifiable credential** — a degree, certification, membership or award the issuing body will
  not confirm. "Studied X" is not "certified in X".
- **Sole credit for shared work** — first-person singular is for what you personally did;
  everything else says "we", names the team and links the record.
- **Fabricated social proof** — invented testimonials, logos of non-users, a case study that did
  not happen, a manufactured deadline or scarcity. Refusing to produce these is an exit criterion
  below, not a preference.

**Never assert an external fact from memory anywhere in the deliverable**: a platform's rules, a
conference's deadline or review policy, a certification's terms, an award's criteria, a
conversion benchmark, an industry average, a follower threshold. Fetch it now, quote it, date it,
or leave the sentence out. Every date written by this skill — audit run dates, `checked on` dates,
`done-when` dates, the re-run date — is ISO 8601 `YYYY-MM-DD`, no other format, so the file diffs
and sorts.

## Step 5 — the invisible evidence inventory

The common failure is not over-claiming; it is that the strongest evidence a person owns is
invisible. Run the sweep **before** asking the person what they have done: enumerate mechanically,
count it, then compare against their self-report. Where the two differ, the gap is itself a row in
the inventory — it is the reason this step exists rather than a conversation.

Sweep for evidence that exists but is not linked from any surface in step 2:

```bash
git log --author="<email>" --since="3 years ago" --name-only --pretty=format:'%h %ad %s' --date=short
ls docs/adr/ docs/ 2>/dev/null                      # design documents, decision records, post-mortems
gh search prs --author=<login> --state=merged --limit 100 --json repository,title,url
```

Then the sources no command reaches: merged contributions to other people's repositories,
published packages, internal design documents you could generalise, incident write-ups, reviews
you wrote, conference or meetup talks already given, teaching or mentoring records, answers others
still link to. For each, one row: what it evidences, which claim id it could back, and whether
publishing it is permitted.

**The hard case — work under NDA or inside a private repository.** This is the normal case for
employed engineers, and the wrong answers are (a) describing the work specifically enough to
breach the obligation and (b) gesturing at it to imply more than can be shown. The route that
works, in full, is `references/portfolio-evidence.md` § invisible work. In short: state capability
generally without identifying the employer's system; extract the *transferable* problem and
rebuild a small public artifact that demonstrates the same skill on data and code you are free to
publish; prefer the reproduction you can hand over to the anecdote you cannot. Any doubt about
what the obligation permits goes to `foundry-legal` — do not read the contract and do not reason
about whether anyone would notice.

## Step 6 — prioritise down to at most five actions

Rank every candidate action by `harm-or-gain for the DECISION` divided by `cost in hours`, then
**keep the top five and cut the rest**. The cut list is part of the deliverable: an action that is
not in the top five is written under `## Deliberately not doing now`, with the date the decision
was made, so nobody re-derives it next month.

A default ordering, to be overridden by what this audit actually found — it is a prior, not a
result, and if the deliverable reproduces it unchanged the prioritisation was not done:

1. Remove or update a dead surface ranking above the live one. Cheap when the account is still
   yours; estimate the cost yourself rather than inheriting a number from this list.
2. Cut every claim the ledger marked `CUT` — no cost but the deletion, and it removes the risk
   that one falsified sentence discredits the true ones next to it.
3. Fix the one broken link behind a load-bearing claim.
4. Publish the strongest invisible artifact found in step 5, with the four questions answered.
5. Reconcile the contradiction across surfaces to one true version.

Each action is written as `owner · what · done-when` where `done-when` is checkable by a command
or a URL, never by a feeling:

```
A-1 · <person> · replace the abandoned profile bio with the reconciled one
      done-when: curl -s <url> | grep -q "<the new title>"     · by 2026-09-05
```

**Gate:** `count(actions) <= 5`. If six feel necessary, the sixth is not necessary; it is the
audit refusing to make a judgement. Prefer the smallest honest action over the most impressive
one — a corrected sentence that survives a reference check is worth more than a new site that
restates an unevidenced claim more beautifully.

## Step 7 — write it down

`docs/growth/personal-brand.md`, in this order: the audience/decision/date block; the surface table
with the exact queries, the run date, which pass produced each row, and the stated limits of the
instrument that ran it; the claim ledger with verdicts; the cut list with dates and restoration
conditions; the invisible-evidence inventory including the NDA route where it applies; the ≤ 5
prioritised actions with their `done-when` checks; `## Deliberately not doing now`; anything handed
to `foundry-legal`; and a re-run date ≤ 90 days or the `BY` date, whichever is earlier.

The file is about one person and is written for them. It holds no dossier on a homonym, no contact
details for anyone, and nothing about a third party beyond the rank-and-URL collision rows.

The vertical's `growth-claim-substantiation` gate (`hooks/guard-claims.mjs`) fires on every write
to this file and asks about borrowed credibility, uncounted metrics and unearned social proof. It
is advisory, and on this deliverable it is a second reader of the ledger: an entry it flags that
you cannot answer with the evidence URL already in the row is a `CUT` you have not made yet.

Emit `review.v1` to `.foundry/blackboard/<wave>/personal-brand-strategist.json` via
`blackboard_write` — the agent's file, per AUTHORING.md §6 and the agent's own output contract;
do not open a second file under the skill's name. Fill every required field:

- `target` — the primary identity handle under audit. `dimension` — `personal-brand`.
- `verdict` — `block` while any claim marked `CUT` is still published or any row is still
  `pending`; `pass-with-comments` when the cuts are applied and actions remain open; `pass` only
  when every action in step 6 has met its `done-when` check.
- `metrics` — `surfacesFound`, `surfacesStale`, `claimsTotal`, `claimsEvidenced`, `claimsCut`,
  `invisibleArtifacts`, `actions`, `auditDate`.
- `findings` — one `finding.v1` per cut claim, per stale surface and per contradiction, each with
  `severity` and `confidence`, and a `failureScenario` naming the checker and the check ("a hiring
  manager opens the linked repo and finds the last commit three years older than the claim"). A
  claim cut for being unverifiable is `confidence: high` — the absence of the artifact is the
  evidence, and nothing about it is speculative.
- `summary` — the schema caps it at 900 characters, which is well inside the 300-token firewall.

Return to the caller **only** the artifact path plus a summary of ≤ 300 tokens. Never paste profile
text, search results or draft bios into the parent context.

Write the audience statement and the audit date as a `domain` fact via `memory_write` so
`find-collaborators` and `prepare-fundraise` do not redo step 1.

## Exit criteria

1. `docs/growth/personal-brand.md` exists and its first block matches `AUDIENCE:` / `DECISION:` /
   `BY:` with a named role or organisation — the count of the words "everyone" or "the industry"
   in the `AUDIENCE` line is **0**.
2. The surface table lists every surface found, each with a URL, a `found by` value naming the
   instrument that produced it, a `mine?` value, a last-updated date and a helps/harms/neutral
   verdict; the exact queries and the run date are recorded. The count of rows missing a URL, a
   `found by` or a verdict is **0**, and the count of rows recorded without opening the page is
   **0**.
3. Claim ledger complete, and `claimsEvidenced + claimsCut == claimsTotal` — verifiable by grep of
   the verdict column; the count of rows still `pending` is **0**.
4. Every `EVIDENCED` row carries a URL that returned 2xx on the audit date, with the status code
   recorded, **and** a note that the fetched body contained the artifact rather than a login wall,
   consent interstitial or paywall; every `runnable` evidence row records the executed command and
   its exit status. The count of `EVIDENCED` rows resting on a status code alone is **0**.
5. The count of surviving claims of inflated title, uncounted metric, unverifiable credential or
   sole credit for shared work is **0**, and each removal appears in the cut list with a date.
6. The count of testimonials, logos, named clients, case studies or user counts lacking a named
   real source and a recorded permission date is **0**. Nothing of that kind is generated by this
   run under any framing.
7. Every sentence depending on an external rule (platform behaviour, CFP deadline, review policy,
   certification terms) carries `(checked <URL> on YYYY-MM-DD)`; the count of external assertions
   without one is **0**.
8. The invisible-evidence inventory has at least one row, or states explicitly that the sweep of
   `git log`, merged PRs and `docs/` returned nothing publishable and why.
9. Where work is under NDA or private, the deliverable contains a capability statement plus a named
   public reproduction plan, and contains **zero** identifying details of the confidential system.
10. `count(actions) <= 5`, each with an owner, a `done-when` that is a command or a URL check, and
    a date; everything else appears under `## Deliberately not doing now`.
11. A re-run date is recorded, ≤ 90 days and not later than the `BY` date.
12. The audit subject asked for it and is in the session. The count of third parties profiled, of
    contact details collected, and of pages recorded about anyone other than the subject is **0** —
    homonyms excepted, and those are recorded as rank plus URL only (`references/surface-audit-procedure.md`
    § homonyms).
13. `review.v1` written to `.foundry/blackboard/<wave>/personal-brand-strategist.json`, validated by
    `contract_validate` with `target`, `dimension`, `verdict`, `findings` and `summary` populated,
    carrying one finding per cut claim, stale surface and contradiction; the returned summary is
    ≤ 300 tokens.

## Degradation

- **No `WebSearch` / `WebFetch`** → Pass A of step 2 cannot run. Emit the query list and the empty
  table from `references/surface-audit-procedure.md`, ask the person to run Pass B and paste the
  results, and mark every criterion depending on the missing pass `UNVERIFIED`. **Never simulate a
  search result or describe what you expect to rank** — a fabricated audit is worse than no audit,
  because it will be believed.
- **Pass B not returned** (the person has not run the logged-out pass yet) → ship the deliverable
  on Pass A alone, labelled `unpersonalised pass only — region and personalisation unchecked`, and
  leave criterion 2 partially `UNVERIFIED` with the date the request was made. Do not close the
  audit as complete on one instrument.
- **No `gh`** (absent, or `gh auth status` fails) → fetch the public profile and repository pages
  directly, accept the loss of merged-PR search and pagination, and mark the affected counts
  approximate in the artifact.
- **No `curl` and no network** → run steps 3 and 5 from repository artifacts only (`git log`,
  `docs/`, README files), leave every evidence URL `UNCHECKED`, and label the file
  `preliminary — no external verification performed`. Do not promote a `pending` row to
  `EVIDENCED` on the strength of a link that was never opened.
- **The person will not share the underlying work** → produce the audience statement, the surface
  table and the failure-mode review, and state that the evidence layer is unassessable. Do not
  compensate with stronger copy.
- **`foundry` MCP server unavailable** → write the blackboard file at the path yourself and say in
  the summary that it was not schema-validated.
- **`superpowers` installed** → use `superpowers:brainstorming` for step 5 wherever the mechanical
  sweep turns up artifacts the person did not mention, since that gap is the signal that a
  structured interrogation will find more than one question did, and
  `superpowers:verification-before-completion` before reporting any criterion above as met. If
  it is absent, walk the exit-criteria list item by item and paste the command output for each
  check into `docs/growth/personal-brand.md`.

## Deliberately not covered

Project positioning and the one-sentence claim (`position-project`); launch channels and
sequencing (`plan-launch`); editorial cadence, distribution and audience measurement for a project
(`build-audience`); investor targeting, the deck and the data room (`prepare-fundraise`); finding
and contracting the people to work with (`find-collaborators`); salary, rate, equity or any
financial modelling (`foundry-economics:business-case-analyst`, `foundry-economics:cost-engineer`);
grant administration (`foundry-economics:funding-analyst`); CONTRIBUTING, GOVERNANCE, issue triage
and release notes inside a repository (`foundry-oss`); the README, the documentation site and the
CV or bio prose itself (`foundry-research:technical-writer`); roadmap and delivery reporting
(`foundry-pmo`); the portfolio site's own WCAG 2.2 conformance and code
(`foundry-dev:accessibility-engineer`); lawful basis and consent for any contact list
(`foundry-legal:privacy-engineer`); and advertising-claims substantiation, sponsorship and
endorsement disclosure, NDA and non-compete scope (`foundry-legal`) — flagged here, decided there,
and never reasoned about in this skill. Scraped contact data, unsolicited bulk mail, mass-automated
identical outreach and the profiling of anyone who did not ask for this audit are refused by name,
not scoped down.

## Bundled references

- `references/surface-audit-procedure.md` — the per-surface audit: the query set, the logged-out
  protocol, what to record per surface class, homonym collisions, and the six-month diff format.
- `references/portfolio-evidence.md` — what makes a project entry verifiable: the four evidence
  ranks, the four questions every entry must answer, the clean-machine check, and the full route
  for work that is under NDA or inside a private repository.
- `references/cfp-and-first-talk.md` — how programme-committee selection actually works, the
  anatomy of a proposal that gets picked, blind-review handling, and building a first speaking
  record from nothing without claiming one you do not have.
