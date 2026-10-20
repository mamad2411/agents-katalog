---
name: build-audience
description: Turn work that already happened into a publishing cadence that survives — measure the real hours available, mine the repository for artifacts that are already 70% written (ADRs, reverts, incidents, benchmarks, deletions, hard bugs), convert that inventory into a dated editorial backlog, size the cadence to the worst recent week and refuse to plan beyond it, pick one signal metric per objective with the question it cannot answer written next to it, verify the owned site's discoverability by command output, and treat the email list as a consent obligation handed to foundry-legal. Use when a project has shipped and nobody knows it exists, when publishing started and then stopped, when someone asks what to write about, or when nobody can say which number would prove the publishing is working. Produces docs/growth/audience-plan.md and plan.v1.
allowed-tools: Read Grep Glob Bash Write Edit WebFetch WebSearch mcp__plugin_foundry-core_foundry__blackboard_write mcp__plugin_foundry-core_foundry__contract_validate mcp__plugin_foundry-core_foundry__memory_search mcp__plugin_foundry-core_foundry__memory_write mcp__plugin_foundry-core_foundry__runbook_list mcp__plugin_foundry-core_foundry__runbook_get
user-invocable: true
argument-hint: "[--hours-per-week N] [--horizon 12w] [--no-list]"
agent: foundry-growth:audience-builder
model: sonnet
effort: medium
metadata:
  foundry.vertical: growth
  foundry.io: "adr.v1 (positioning) -> plan.v1 + docs/growth/audience-plan.md"
license: Apache-2.0
---

# Build an audience

Sustained attention over months, not a spike over a day. The deliverable is
`docs/growth/audience-plan.md`: a backlog of pieces whose subject matter already exists in this
repository, a cadence priced in hours somebody actually has, and one metric per objective with its
baseline recorded before the first piece ships.

The order is fixed: **hours → inventory → backlog → cadence → metrics → owned surfaces → list →
compounding split → stop condition**. Every step is invalidated by a missing upstream one. Choosing
a cadence first and finding topics for it afterwards is the failure this skill exists to prevent —
it produces an enthusiastic month and a publicly dated dead blog.

**This skill is willing to output "publish less" or "stop publishing".** A plan of one piece a
month, held for two years, is a better result than a weekly plan abandoned in week five, and a
recommendation to fix the funnel instead of feeding it is a complete answer.

## When not to use this

- **There is a launch date.** A one-day event — readiness gate, channel rules, first-hours
  protocol, 14-day follow-through — is `plan-launch`. This skill plans the quarter that follows,
  and it is the wrong instrument for a date.
- **Nobody can state the claim.** Without `docs/growth/positioning.md` the cadence produces a
  stream of unrelated posts that build no memory in anyone's head. Run `position-project` first and
  record the dependency; do not invent an audience here.
- **The people you want are individuals you would approach one at a time** — a maintainer, a
  co-author, a design partner → `find-collaborators`. Broadcast is the wrong instrument for six
  named people.
- **The audience is funders** → `prepare-fundraise`. Published work is evidence inside a raise, but
  the sequencing and the honesty constraints are different.
- **The subject is the person, not the project** — portfolio, profile, talks, CFPs →
  `audit-personal-brand`.
- **The goal is contributors already inside the repository** — CONTRIBUTING, good-first-issue
  curation, triage, release notes → `foundry-oss`. This skill brings people to the door.
- **The bottleneck is not attention.** Run step 9 first if there is any doubt: publishing into a
  broken funnel multiplies zero, and more visits is the most expensive wrong answer available.

## Rules that bind every step

A plan violating any of these is rejected on review. They are not style preferences.

1. **No unverifiable external assertion.** A platform's posting rules, a "best time to post", a
   follower threshold, a conversion benchmark, an industry average, a pricing tier, an engine's
   ranking behaviour: never from memory. Fetch the page at plan time and write
   `source: <url>, checked: YYYY-MM-DD`. What could not be fetched is written `UNVERIFIED —
   confirm before relying on it`, never as a fact.
2. **No fabricated social proof.** No invented testimonial, no logo of a non-user, no user count
   that was not counted from a named source, no case study that did not happen, no manufactured
   scarcity or deadline. Refusing this is exit criterion 8, not a judgement call.
3. **Every claim cites an artifact.** A load-bearing claim without a path, a command output or a
   dated export in this repository is **cut, not softened**. "Loved by teams everywhere" reduced to
   "loved by many teams" is the same fabrication with a smaller number.
4. **Consent-respecting outreach only.** Scraped addresses, unsolicited bulk mail and identical
   mass-automated messages are refused by name. Lawful basis for a contact list, marketing consent,
   advertising-claims law and sponsorship disclosure go to `foundry-legal` — flag and hand over.
5. **Prefer the smallest honest version of a tactic.** One piece a month that is exactly true beats
   a weekly cadence padded with generated filler, and the plan says so where a reader expects the
   opposite advice.

## Step 1 — the hours budget, before anything else

`--hours-per-week N` is a claim, not a measurement. Ask for the **four most recent calendar weeks**
and write down the actual hours spent on publishing-shaped work in each.

- `H_sustained` = the **minimum** of those four weeks, never the mean and never the best. A cadence
  sized to the mean is missed in every bad week, and bad weeks are the ones that end the habit.
- Reserve **20% of `H_sustained`** for distribution and for replying to people. A piece nobody is
  told about is a diary entry; a comment unanswered for a week teaches readers the channel is
  abandoned.
- `H_writing = H_sustained × 0.8` is the entire budget the rest of this plan may spend.

**Gate:** if fewer than four weeks of actual data exist, set `H_sustained = 1 hour/week`, mark the
budget `assumed`, and make measuring the real number the gate of wave 1. Never assume more.

**The refusal:** if the requested cadence costs more than `H_writing`, the plan is written at the
affordable cadence and the difference is recorded as a `risk.v1` (`category: people`, the risk
being abandonment). Do not write the requested plan with a note hoping for more time.

`risk.v1` requires `impactEur`, and this skill does not own monetary valuation. Use the caller's own
stated hourly rate if they gave one; otherwise set `impactEur: 0`, say in `detection` that no rate
was supplied, and name `foundry-economics:business-case-analyst` as the owner of the euro figure.
Never invent a rate to satisfy a required field.

## Step 2 — inventory what already exists

Do not propose a single topic before reading the output of these. The best pieces are already in
the repository, undocumented:

```bash
ls docs/adr/*.md 2>/dev/null | tail -20                       # decisions already argued
git log --since='90 days ago' --no-merges --date=short --pretty='%ad %h %s' | head -60
git log --since='18 months ago' -i --grep='revert\|rollback\|regress' --oneline | head -20
git log --since='18 months ago' --diff-filter=D --name-only --pretty=format: | sort -u | head -30
git log -i --grep='perf\|latency\|throughput\|benchmark' --date=short --pretty='%ad %h %s' | head -20
git branch -a --sort=-committerdate --format='%(committerdate:short) %(refname:short)' | head -20
find . -path ./node_modules -prune -o \( -iname '*bench*' -o -iname '*postmortem*' \) -print | head -20
```

Runbooks are retrieved through the `foundry` MCP tool `runbook_list`, and durable project facts
through `memory_search` — never by reading `.foundry/memory/facts/` or `.foundry/runbooks/`
directly. `gh` is usable only when all three of these hold, and the third is the one that fails
silently — `git remote -v` exits `0` on a repository with no remote at all:

```bash
command -v gh >/dev/null && gh auth status >/dev/null 2>&1 && git remote -v | grep -q . \
  && echo GH_OK || echo GH_UNAVAILABLE
```

On `GH_OK`, add the questions strangers actually asked:

```bash
gh issue list --state all --limit 50 --json number,title,labels
gh api repos/{owner}/{repo}/traffic/popular/paths    # which pages already get read
```

The traffic endpoints need push access and return `403` without it, and they cover a rolling window
the host documents rather than full history — read that documentation if the window matters to the
plan, and record the date. A `403` or an empty body is written down as "traffic data not available"
with the date, never turned into an assumption about which pages are read.

Write the raw inventory to `.foundry/scratch/<session>/inventory.md`. It is working material, not a
deliverable, and it does not go into the parent context.

## Step 3 — inventory into an editorial backlog

Each surviving row becomes a backlog item with five fields, and a row missing any of them is
deleted rather than filled in with an assumption:

```
id | source artifact (commit range, ADR id, runbook slug, benchmark path) | piece class | the one
question a reader has that it answers | evidence that must ship with it
```

The artifact-type → piece-type mapping, the artifacts that must **not** become pieces (unshipped
roadmap items, a security fix before its advisory, anything naming a customer without written
permission, a benchmark you cannot rerun), the four ways this goes dishonest and the redaction pass
are in `references/artifact-to-piece.md`. Apply the redaction pass to the draft, not to the source
artifact.

**Gate:** at most **20% invented topics**. If more than one item in five cannot name the artifact it
was mined from, this is a content-marketing plan competing with the engineering work rather than
resting on it, and it will be abandoned first.

**Gate:** the backlog holds **≥ 6 items** before a cadence is set. Fewer means the inventory step
was skipped, not that the repository is empty.

## Step 4 — size the cadence to the hours, and write the miss rule

- `C_class` = measured median hours per piece class (note / piece / deep piece, defined in
  `references/artifact-to-piece.md`), taken from the **first three pieces the person actually
  produces**. Until those exist it is `assumed` and the plan says so. Never price a piece from
  someone else's claim about how long a piece takes.
- Cadence = `floor(H_writing / C_class)` per week, and "one piece per month" is a legitimate,
  frequently correct answer.
- Schedule each backlog item into a dated slot across the horizon (`--horizon`, default 12 weeks).
  Unscheduled items stay in the backlog; they are not a commitment.
- Total scheduled cost across the horizon must be `≤ H_writing × horizon_weeks`. Print both numbers
  in the plan next to each other.

**The revision rule, written into the plan as a wave gate:** count missed slots per cycle. Two
consecutive misses **halve the cadence** automatically, with no discussion and no guilt language —
a missed schedule is a planning defect, never a character defect. Three consecutive halvings mean
publishing is not the right investment now; go to step 9.

## Step 5 — one signal metric per objective

The discipline is not "avoid vanity metrics". It is: for each metric, state the exact question it
can answer, the exact question it cannot, and the decision that changes when it moves.

| Metric | Can answer | Cannot answer |
|---|---|---|
| Impressions, views | whether distribution happened at all | whether anyone read past the title |
| Reactions, stars | whether the framing landed on the day | usage, retention or value. It is a cumulative counter, so it detects arrival and not decline; before quoting it anywhere, read what the platform's own current documentation says it counts and record the date |
| Read-through, scroll depth | comparatively, whether an opening loses people | comprehension or agreement |
| Email open rate | only what your sending provider's current documentation says it counts — read that page, record the date | engagement of any kind; gate no decision on it in either direction |
| Referrer breakdown | which channel actually delivers people — where the next hour goes | anything about the no-referrer bucket; report its size alongside |
| Replies and inbound naming the piece | whether it reached people with the problem | scale, ever |
| Confirmed subscribers (double opt-in) | how many people asked to hear from you again | whether they still want it in six months |
| The target action, 14 days after vs 14 days before | whether this piece moved the actual thing | why |

Rules, all checkable:

- **Exactly one signal metric per objective**, chosen and written down **before** the first piece
  ships, with its baseline value and the date it was read. A metric selected after seeing the
  numbers is a story.
- **Every number carries provenance**: `1,240 [source: repo traffic API, window as the endpoint
  documents it, read 2026-08-28]`. Tool, window, read date — three parts, always, and the window
  comes from the tool's own documentation rather than from memory.
- **Vanity metrics appear only when labelled `vanity`** and paired with the question they cannot
  answer. They diagnose distribution; they are never evidence of value.
- **A number nobody measured never appears in outbound copy.** See rule 3 above.

The full catalogue — what each metric mechanically counts, how to collect it, and the claim rule
attached to it — is `references/metrics-signal-vs-vanity.md`.

## Step 6 — fix the owned surfaces before amplifying into rented ones

Traffic sent to a page that cannot be found again is spent, not invested. Run the local checks
against the built output and the live checks against the deployed origin in
`references/site-discoverability.md`, and record the **observed output** of each — never the
intention. For this repository the built surface is `site/dist/` after `(cd site && npm run
build)`, and the site is bilingual, which makes `hreflang` reciprocity a real check.

The minimum recorded set, each with its date:

```bash
SITE=https://example.org ; BASE=                  # BASE is the path prefix, empty at origin root
for p in "$BASE/" /robots.txt "$BASE/sitemap-index.xml"; do
  printf '%s ' "$p"; curl -sS -o /dev/null -w '%{http_code}\n' "$SITE$p"
done
curl -sS "$SITE/robots.txt"                       # read it; a staging Disallow: / is invisible
```

Read the base path out of the build config before running this, do not guess it: this repository's
site sets `base: '/foundry'` in `site/astro.config.mjs`, so pages and the sitemap are served under
`/foundry/` while `robots.txt` is only ever read from the **origin root** (RFC 9309). On a
path-hosted deploy the origin root usually belongs to someone else, and the honest record is
"`robots.txt` is not under this project's control at `<origin>`", not a pass and not a failure.

Pass conditions: the page and sitemap URLs return `200`; `robots.txt` blocks nothing you want read
(RFC 9309) and names the sitemap (sitemaps.org protocol 0.9); duplicate `<title>` across sampled
pages `= 0`; exactly one `rel="canonical"` per page (RFC 6596); every moved URL resolves in one
`301` hop to a `200`. Accessibility conformance target is **WCAG 2.2 Level AA** — a failure is a
reader defect first. The conformance work itself is `foundry-dev:accessibility-engineer`, a
docs-structure failure is `foundry-research:docs-architect`, and the published accessibility
statement is `foundry-legal:accessibility-statement`. This skill records the finding and hands it
over; it does not remediate.

Keyword density, doorway pages, bought links, `meta name="keywords"` and bulk generated pages are
refused by name in that reference, with the reason to give the caller.

## Step 7 — the email list, the only channel you own

Every social channel is rented: its terms are set by its owner and can be changed. Whether you can
leave with the audience is a per-platform question with a per-platform answer — if the plan depends
on exporting contacts from a channel, read that platform's current export documentation, write
`source: <url>, checked: YYYY-MM-DD` next to it, and assume nothing in either direction. A list
whose addresses you hold yourself does not depend on that answer, and it is the surface here with
real legal weight. If `--no-list` is passed, record the absence and skip to step 8.

What the plan must specify, or the list is removed from the plan:

- **Double opt-in.** Stored per subscriber: timestamp, source page, the exact wording consented to,
  and the confirmation event. That record cannot be reconstructed later.
- **One-click unsubscribe in every send**, honoured immediately: the `List-Unsubscribe` header
  (RFC 2369) with one-click support (RFC 8058), plus a visible link in the body.
- **Separate purposes, separate consent.** Someone who subscribed to release notes did not
  subscribe to a fundraising announcement.
- **Ownership, written down before the first send**: who controls the export, where it lives, what
  happens to it if the project ends or the maintainer leaves, and the retention period. A list
  nobody can export is the platform's asset, not yours.
- **Never import** from a badge scan, a repository scrape, a purchased file or a CRM export of
  people who did not opt in to *this* list. Say no by name; do not look for the narrow reading.

Instruments to cite, not to interpret: GDPR Art. 6(1)(a) and Art. 7 (consent and its conditions),
Art. 13 (information at collection), Directive 2002/58/EC Art. 13 (unsolicited communications).
**Confirm the current text before relying on any of them.** Lawful basis, notice wording, retention
and record-keeping design belong to `foundry-legal:privacy-engineer` — raise a `handoff.v1` the
moment a list, a contact form, or analytics that set identifiers enter the plan, and do not
improvise the answer while waiting. The schema carries no recipient field: name
`foundry-legal:privacy-engineer` in `summary`, put the specific questions in `openQuestions[]`, and
set `status: blocked` with `blockedBy` naming that agent when the plan cannot proceed without them.

## Step 8 — compounding versus decaying

| Compounding — keeps earning | Decaying — a day, sometimes an hour |
|---|---|
| A reference page that definitively answers a recurring question | A post about a release |
| A benchmark with its reproduction command, kept current | A status update |
| A small useful tool with a stable URL | A comment thread |
| The write-up that becomes the link people send each other | An announcement of an announcement |

At least **25% of `H_writing`** goes to compounding assets, and at least one exists in every plan.
Compounding assets carry maintenance cost: a stale benchmark or reference page becomes a liability,
so each one carries a **review date** in the plan.

## Step 9 — the stop condition

Publishing is sometimes the wrong work. The audience is **not** the bottleneck when any of these is
measurably true, and each is a number the plan can check:

- The last **5** pieces produced visits and **zero** instances of the target action.
- The visit → target-action rate is below the threshold recorded in step 5, over a window of
  **≥ 8 weeks** and **≥ 5 pieces**.
- Existing users leave faster than new ones arrive — retention is the failing stage
  (`foundry-dev`, `foundry-oss`).
- Inbound already exceeds what the project can absorb: unanswered issues, an unfinished first-run
  path, no capacity to reply.

In any of those cases the recommendation is: pause the cadence, name the actual bottleneck, route
it to its owner, and say so in the plan. Recommending "post more" into a broken funnel is the
expensive mistake this skill prevents.

## Step 10 — write it down

`docs/growth/audience-plan.md`, in this order: the hours budget with the four measured weeks and
`H_sustained`; the inventory summary with the commands run and their date; the backlog table with
source artifact, class, reader question and required evidence per row; the dated schedule with
total cost against `H_writing × horizon`; the miss rule; the metric table with baselines, provenance
and the decision each feeds; the discoverability results table with observed output and dates; the
list section or its explicit absence; the compounding split with review dates; the stop condition;
open risks; review date ≤ 90 days.

Emit `plan.v1` to `.foundry/blackboard/<wave>/audience-builder.json` via the MCP tool
`blackboard_write`, `producedBy: audience-builder` — one wave per publishing cycle, each with a
machine-checkable `gate` (a count of pieces shipped, a named file that must exist, a metric read
from a named tool's output). Put the hours cost of each task in `waves[].tasks[].estimateHours`:
that is what makes the budget check in exit criterion 2 arithmetic rather than opinion. Return to
the caller only that path plus a summary of at most 300 tokens (AUTHORING.md §2 context firewall);
never paste the backlog or draft copy into the parent context.

`outOfScope[]` must name, verbatim, every refused tactic: engagement bait,
undisclosed paid promotion, AI-generated bulk content posted as authored, reposting without
attribution, scraped personal data, unsolicited bulk mail, mass-automated identical messages.

Durable conclusions go back through the `foundry` MCP tool `memory_write` (`type: metric` for
observed baselines, `type: risk` for what nearly went wrong). Never write memory files by hand.

## Exit criteria

1. `H_sustained` derived from **4 weeks of actual recorded hours** using the **minimum** week, or
   set to 1 h/week and labelled `assumed` with measurement as wave 1's gate.
2. Total scheduled cost across the horizon is **≤ `H_writing` × horizon_weeks**, with both numbers
   printed in the plan. A requested cadence exceeding it produced a `risk.v1`, not a larger plan.
3. Backlog holds **≥ 6 items**, and **≥ 80%** cite the commit range, ADR id, runbook slug or
   benchmark path they were mined from. Invented topics **≤ 20%**.
4. Every backlog row names exactly one reader question and the evidence that must ship with it; a
   row answering two questions was split or deleted.
5. The mining commands in step 2 were **run**, and their date is recorded in the plan.
6. **Exactly one** signal metric per objective, each with a baseline value and the date it was read,
   recorded **before** the first piece ships. Every vanity metric is labelled `vanity` and paired
   with the question it cannot answer.
7. **Zero** outside-world facts asserted from memory: no platform rule, posting time, follower
   threshold, conversion benchmark, industry average or ranking claim appears without
   `source: <url>, checked: YYYY-MM-DD` or the `UNVERIFIED` marker.
8. **Zero fabricated social proof**: the count of testimonials, logos, user counts and deadlines
   without a named evidence artifact plus a date is exactly zero, and the plan shows the claims
   that were **cut** rather than reworded.
9. Discoverability results recorded as observed command output with HTTP codes and dates: the
   landing page and the sitemap at `200`; `robots.txt` at `200` **or** recorded as not under this
   project's control at that origin; duplicate `<title>` count `= 0`; canonical count `= 1` per
   sampled page; every check without observed output explicitly marked `unverified`.
10. If a list is in the plan: double opt-in, the consent-record design, ownership and retention,
    `List-Unsubscribe` (RFC 2369 / RFC 8058) on every send, and a `handoff.v1` to
    `foundry-legal:privacy-engineer` — otherwise the list is removed.
11. **≥ 1** compounding asset, **≥ 25%** of `H_writing` allocated to compounding, each with a review
    date.
12. The miss rule (two consecutive misses halve the cadence) and the numeric stop condition are both
    present as wave gates.
13. `docs/growth/audience-plan.md` exists; `plan.v1` at
    `.foundry/blackboard/<wave>/audience-builder.json` passes `contract_validate` with a non-empty
    `outOfScope` listing every refused tactic verbatim; the caller summary is ≤ 300 tokens.
14. No required schema field was filled with an invented value — in particular `risk.v1.impactEur`
    is either the caller's own stated rate applied to measured hours, or `0` with the reason in
    `detection`.

## Degradation

- **`WebFetch` and `WebSearch` both absent** → no external channel rule can be verified. Commit only
  to the owned surfaces (site and list, both verifiable locally), list external channels as
  candidates the person must check before first submission, and mark them `rules unverified`. Never
  substitute recalled rules.
- **`gh` absent, unauthenticated, or no resolvable remote** — check all three with the `GH_OK`
  expression in step 2, because `command -v gh` succeeding proves none of them. With no remote
  (`git remote -v` printing nothing, the normal state of a fresh or vendored checkout)
  `gh api repos/{owner}/{repo}/…` fails with `unable to expand placeholder in path` and
  `gh issue list` with `no git remote found`. Mine from local `git log`, `git branch` and `docs/`
  only, and state in the plan that issue- and traffic-derived topics were not searched.
- **`curl` absent, or the site is not deployed yet** → run the local checks against the built output
  only, mark every live criterion `unverified` rather than passing it, and make "run these against
  the deployed origin" the gate of the next wave.
- **No analytics, or analytics blocked by consent choices** → prefer metrics that survive blocking:
  confirmed subscribers, unprompted inbound naming the piece, and the target action counted
  server-side. State that percentage traffic figures are unreliable here rather than reporting them
  as if they were not.
- **No positioning artifact** → stop, run `position-project`, record the dependency. Do not invent
  the audience or the claim in this skill.
- **`foundry` MCP server unavailable** → runbook and memory mining are skipped and recorded as
  skipped; write the artifact to the blackboard path directly and state in the summary that it was
  not schema-validated.
- **`superpowers` installed** → use `superpowers:writing-plans` to structure the waves and
  `superpowers:brainstorming` to widen the inventory **before** cutting it to the hours budget. If
  absent, use the step order above unchanged and cut with the step 3 gates; nothing here depends on
  it.

## Deliberately not covered

Launch dates, launch channels and first-hours protocol (`plan-launch`); the claim, the audience
definition and differentiation (`position-project`); the individual's portfolio, talks and CFPs
(`audit-personal-brand`); investor narrative, deck and data room (`prepare-fundraise`); one-to-one
outreach to named individuals (`find-collaborators`); revenue, CAC, break-even and any financial
projection (`foundry-economics:business-case-analyst`, `cost-engineer` — growth writes the
argument, economics writes the numbers); grant paperwork and milestone reporting
(`foundry-economics:funding-analyst`); the contributor funnel inside the repository, CONTRIBUTING,
triage and release notes (`foundry-oss`); README, documentation site structure and technical
writing (`foundry-research`); roadmap, backlog and delivery reporting (`foundry-pmo`); lawful basis
for a contact list, marketing consent, advertising-claims law and sponsorship disclosure
(`foundry-legal`); and product, architecture or code decisions (`foundry-dev`).

## Bundled references

- `references/artifact-to-piece.md` — the repository-artifact → piece-type mapping with the command
  that finds each one, the artifacts that must not become pieces, the four ways this goes dishonest,
  the redaction pass, and the three cost classes.
- `references/metrics-signal-vs-vanity.md` — what each metric mechanically counts, the question it
  answers, the question it cannot, how to collect it, and the claim rule attached to it.
- `references/site-discoverability.md` — local checks against the built output and live checks
  against the deployed origin, with pass conditions, bilingual `hreflang` reciprocity, URL
  stability, WCAG 2.2 AA criteria, and the tactics refused by name.
