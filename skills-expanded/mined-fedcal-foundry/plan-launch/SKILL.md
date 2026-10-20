---
name: plan-launch
description: Plan a public launch that survives contact with strangers — a hard readiness gate run on a pristine checkout before any date is defended, success thresholds agreed in numbers before the date rather than rationalised after it, channels chosen from evidence of where the audience already is with each channel's current rules verified at runtime and dated, a claim ledger where every outbound assertion cites a repository artifact or gets cut, a first-hours protocol, and a 14-day follow-through. Use when a launch date is being discussed, before anything is announced publicly, after a previous launch landed flat, or when someone asks where to post this. Produces docs/growth/launch-plan.md and plan.v1. Concludes "not ready, postpone" when the gate is red.
user-invocable: true
argument-hint: "[--date YYYY-MM-DD] [--channel <name>,<name>]"
agent: foundry-growth:launch-strategist
model: sonnet
effort: medium
metadata:
  foundry.vertical: growth
  foundry.io: "adr.v1 (positioning) -> plan.v1 + docs/growth/launch-plan.md"
license: Apache-2.0
---

# Plan a launch

A launch is a date on which strangers arrive at the project for the first and probably only time.
The deliverable is not enthusiasm: it is `docs/growth/launch-plan.md`, written before the date,
containing a readiness verdict backed by commands whose output was read, the numbers that will
decide afterwards whether it worked, and the channels chosen with the evidence that put them
there.

The order is fixed: **readiness gate → success numbers → audience evidence → channels → claim
ledger → sequence and date → first hours → follow-through**. Every step is invalidated by a
missing upstream one. Picking the date first, then reverse-engineering readiness, is the failure
mode this skill exists to prevent.

**This skill is willing to output "postpone".** A red gate with a remediation plan is a correct
and complete result, not a failure to produce one.

**The arguments are inputs, not permissions.** `--date` is a proposed date that step 1 may
invalidate; it never shortens the gate. `--channel` names candidates, which still enter step 4's
scoring with a provenance line and still have their rules fetched and dated — a channel the
caller asked for is not exempt, and one that fails scoring is written up as rejected rather than
posted to anyway.

## When not to use this

- **The project is not launching, it is being announced repeatedly.** Sustained cadence,
  editorial calendar, search discoverability and vanity-versus-signal measurement belong to
  `build-audience`. A launch is a one-day event; do not use this skill to plan a quarter.
- **The claim itself is undecided.** If nobody can state in one sentence who this is for and what
  it replaces, run `position-project` first — a launch amplifies positioning, it does not create
  it, and launching an unclear claim burns the channel for the next attempt.
- **The people you want are individuals you would approach one by one** (a maintainer, a
  co-author, a design partner) → `find-collaborators`. Broadcast is the wrong instrument.
- **The audience is investors or funders** → `prepare-fundraise`. A launch can be evidence inside
  a raise, but the sequencing, materials and honesty constraints are different.
- **The goal is contributors inside the repository** — CONTRIBUTING, good-first-issue curation,
  triage rotation, governance → `foundry-oss`. This skill brings people to the door; what happens
  after they walk in is not ours.
- **A release has to ship first.** Publishing mechanics, version tagging and the release sequence
  for this repository live in the `publish-release` runbook — read it with the `foundry` MCP tool
  `runbook_get` and follow it. This skill plans the announcement around that release; it does not
  replace it.

## Rules that bind every step

These are not style preferences. A launch plan violating any of them is rejected on review.

1. **No unverifiable external assertion.** Never write down a platform's posting rules, a
   threshold, a "best time to post", a conversion benchmark, an industry average, or a pricing
   tier from memory. Fetch the actual page at plan time and record `checked: YYYY-MM-DD` (ISO 8601)
   next to what you read. Anything you could not fetch is written as `UNVERIFIED — confirm before
   posting`, never as a fact.
2. **No fabricated social proof.** No invented testimonial, no logo of a non-user, no user count
   that was not counted from a named source, no case study that did not happen, no manufactured
   scarcity or deadline. Refusing this is an exit criterion, not a judgement call.
3. **Every claim cites an artifact.** Step 5's ledger. A load-bearing claim without evidence in
   the repository is cut, not softened into a vaguer version of the same untruth.
4. **Consent-respecting outreach only.** Scraped address lists, unsolicited bulk mail and
   identical mass-automated messages are out of scope and are refused by name. Contact-list
   lawfulness, marketing consent, advertising-claims law and sponsorship disclosure go to
   `foundry-legal` — flag and hand over, never improvise.
5. **Prefer the smallest honest version of a tactic.** A single post to one channel where the
   audience genuinely is, with a claim that is exactly true, beats a coordinated push built on a
   number nobody measured.

## Step 1 — the readiness gate, run first

Run it on a **pristine tree**, not on your working copy, because your working copy has untracked
files, local config and a warm cache that a stranger will not have:

```bash
tmp=$(mktemp -d) && git archive HEAD | tar -x -C "$tmp" && echo "$tmp"
```

If that pipeline fails — no commit on the branch yet, a shallow or partial clone, `tar` refusing
the stream — the gate has not run. Do not fall back to the working copy: it is the exact thing the
check exists to exclude. Record the failing command and its stderr, and treat the gate as RED
until a pristine tree can be produced.

Then execute every blocking check in `references/readiness-checklist.md` against `$tmp` and
record, per check, the exact command, its exit status and the observed output — for this
repository that includes `node scripts/validate-assets.mjs`, `node --test
'plugins/*/test/*.test.mjs'`, `(cd site && npm run build)`, the presence of `LICENSE`,
`NOTICE`, `SECURITY.md` and `.github/ISSUE_TEMPLATE/`, and running the install command extracted
verbatim from `README.md` rather than the one you remember writing.

**Gate:** any blocking check RED → the verdict is **NOT READY — POSTPONE**. Write it at the top of
`docs/growth/launch-plan.md`, emit `plan.v1` whose first wave is remediation with one task per red
check, name a re-gate date, and stop. Do not proceed to step 2 with a red gate and a hope.

**Gate:** the first-run path must be walked by a person who has never used the project, from
`$tmp`, with no help. Record who, the date, and every point where they stopped. If no such person
exists, run it yourself in an environment with no project-specific variables set and label the
evidence `self-run, not a stranger` in the plan — that label is what stops the evidence being
overread later.

## Step 2 — agree the numbers before the date

Written down before the announcement, or they are not success criteria — they are post-hoc
narration.

- **One primary number** the launch is for, with the mechanism that will measure it named
  (`gh api repos/{owner}/{repo}/traffic/views`, `traffic/clones`, issue count, subscriber count).
- **Its baseline**, measured now, over an ordinary week, before anything is posted. A number with
  no baseline cannot be moved.
- **Three thresholds**: worked / inconclusive / did not work, as numbers, with the decision each
  one triggers already written next to it.
- **One counter-metric** that would make a "success" a bad outcome — for example arrivals up but
  issue reports of the same broken first-run step up with them.
- **The honest floor**: state explicitly what result would make you conclude there is no demand
  for this, and commit to publishing that conclusion if it happens.

Predicting the numbers is not required. Deciding in advance what they will mean is.

## Step 3 — audience evidence before channel opinions

Do not start from a list of platforms. Start from the evidence of where attention already comes
from, in this order: existing referrer and traffic data (`gh api
repos/{owner}/{repo}/traffic/popular/referrers`), the origin of everyone who has already filed an
issue or asked a question, and where the projects that solve the adjacent problem are discussed.
Record each finding with its source and date. Where there is no evidence at all, say so — a
first-ever launch has none, and pretending otherwise is how a channel gets picked by habit.

## Step 4 — choose channels from fit, then verify their rules at runtime

Score each candidate against the evidence from step 3 using the procedure in
`references/channel-selection.md`, which evaluates fit rather than enumerating platforms.

For every channel that survives scoring, **fetch its current rules page now** — self-promotion
policy, account-age or standing requirements, formatting and link constraints, disclosure
obligations — and record the URL and `checked: YYYY-MM-DD` in the plan. If `WebFetch` and
`WebSearch` are both unavailable, mark the channel `RULES UNVERIFIED` and require a human to
confirm before posting; do not substitute recalled rules.

**Gate:** at most three channels for a first launch, each with a named owner, its rules line and a
check date. A fourth channel is evidence that step 3 produced nothing and the list is aspiration.

## Step 5 — the claim ledger

Every sentence of outbound copy that asserts anything gets a row:

| Claim (verbatim) | Evidence artifact | Verified on | Verdict |
|---|---|---|---|

Evidence is a path in this repository or a command whose output was read — a test run, a
benchmark script with the machine it ran on, a counted list. `README.md` asserting the same thing
is not evidence; it is the same claim in another file.

A claim with no evidence artifact is **cut**. Superiority claims ("fastest", "the only", "better
than X") require a comparison artifact that actually exists, or they do not ship. Numbers about
adoption require the named source that was counted. This ledger is the mechanism that makes rule 2
and rule 3 checkable rather than aspirational.

## Step 6 — sequence and date

Order the work backwards from the date: gate remediation, assets, the pre-launch quiet steps
(people told in advance because they will be asked to help answer questions, not to upvote), the
post itself, and the response window. Assign an owner and a calendar slot to each. The date is
valid only if the response window in step 7 is actually staffed; a launch posted into an
unattended day is a wasted first impression.

Two constraints that are not negotiable: never announce before the release the announcement
points at is actually published, and never set the date so that the first hours fall where the
named owner cannot be present.

## Step 7 — the first-hours protocol

- **Response window**: a named owner, present for a stated block of hours, with a stated maximum
  reply latency for questions in that window.
- **Triage rule**, decided in advance: a reproducible bug becomes an issue with a link back to the
  thread; a feature request becomes a discussion; a factual correction is acknowledged and fixed
  in public; hostility gets one courteous reply and no second one.
- **Erratum protocol**: if a claim in the copy turns out to be wrong, correct it in the thread
  within the response window and fix the source file the same day. Deleting and reposting to hide
  it is not an option.
- **Forbidden, by name**: coordinated upvoting or vote rings, sockpuppet or undisclosed accounts,
  seeded comments presented as organic, reposting to evade a rate limit or a moderation decision,
  and DM blasts to addresses nobody consented to give you. These are refused even if requested,
  and if a request touches consent or disclosure law it goes to `foundry-legal`.

## Step 8 — follow-through and the retrospective

Checkpoints at **24 h**, **72 h** and **14 days**, each recording the primary number, the counter
metric, and the issues that arrived. At day 14 run
`references/post-launch-retrospective.md`, whose whole purpose is to separate **wrong channel**
from **wrong positioning** from **no demand** — three diagnoses with three different remedies,
routinely collapsed into "we should have posted somewhere else".

Write the durable conclusions back as facts through the `foundry` MCP tool `memory_write`
(`type: metric` for the observed baselines, `type: risk` for what nearly went wrong). Never edit
`.foundry/memory/facts/` by hand.

## Step 9 — write it down

`docs/growth/launch-plan.md`, in this order: the readiness verdict with per-check command, status
and date; the success numbers with baselines, thresholds and pre-registered decisions; the
audience evidence with sources and dates; the channel table with rules URLs and check dates; the
claim ledger including the cut rows and why they were cut; the sequence with owners; the
first-hours protocol; the checkpoint schedule; open risks; review date ≤ 90 days.

Emit `plan.v1` to `.foundry/blackboard/<wave>/launch-strategist.json` via the `foundry` MCP tool
`blackboard_write` — waves for remediation, assets, launch day and follow-through, each with a
machine-checkable `gate` — and return to the caller only that path plus a summary of at most 300
tokens. `outOfScope` must name what this launch deliberately does not attempt (channels rejected,
audiences not addressed, claims cut). If the `foundry` MCP server is unreachable, say so, write
the same JSON to that path by hand, and validate it against
`plugins/foundry-core/schemas/plan.v1.schema.json` before claiming the step is done.

## Exit criteria

1. The gate ran on a pristine `git archive HEAD` tree, not on the working copy, and every blocking
   check in `references/readiness-checklist.md` has a recorded command, exit status and date.
2. A first-run walkthrough by a person who has never used the project is recorded with a date and
   the stopping points, or explicitly labelled `self-run, not a stranger`.
3. A red blocking check produced the verdict **NOT READY — POSTPONE**, a remediation wave and a
   re-gate date — with no launch date defended.
4. One primary number, its measured baseline, three numeric thresholds, one counter-metric and one
   stated no-demand condition are written down and dated **before** the launch date.
5. At most 3 channels, each with an evidence row from step 3, a named owner, a rules URL and
   `checked: YYYY-MM-DD`, or an explicit `RULES UNVERIFIED` flag. **Zero is a permitted count**:
   if no candidate clears `references/channel-selection.md`'s eligibility rule, the plan says so
   and routes to `find-collaborators` or `build-audience` instead of posting anyway.
6. Zero unverified external facts in the plan: every external assertion carries a URL and a check
   date, or the `UNVERIFIED` marker.
7. Claim ledger complete: every outbound assertion has an evidence artifact path, or appears in
   the ledger with verdict `cut`. Zero fabricated testimonials, logos, counts or deadlines — count
   is exactly zero, and the ledger shows it.
8. The response window is staffed by a named person for a stated block of hours; the forbidden
   tactics list is present verbatim in the plan.
9. Checkpoints scheduled at 24 h, 72 h and 14 days, with the retrospective procedure named.
10. `docs/growth/launch-plan.md` exists; `plan.v1` validates with a non-empty `outOfScope` and a
    `gate` on every wave.

## Degradation

- **`gh` absent, unauthenticated, or the repository is not on GitHub** → baselines and referrer
  evidence come from the hosting provider's own analytics, read by hand and recorded with the date
  read. Label them `manual reading` so nobody later mistakes them for an API series.
- **A `traffic/*` call returns a non-zero exit or an HTTP error** (the token lacks the access those
  endpoints require) → that metric is recorded `not measurable`, with the command and the error.
  Do not substitute a different number and do not estimate one; a primary metric whose mechanism
  fails at plan time must be replaced by one that actually reads, before the date is set.
- **`WebFetch` and `WebSearch` both absent** → channel rules cannot be verified. Every channel is
  marked `RULES UNVERIFIED`, the plan states that a human must confirm each one before posting,
  and the gate on the launch-day wave includes that confirmation. Recalled rules are never
  written down as fact.
- **`site && npm run build` cannot run** (no network for `npm ci`) → the documentation check is
  RED, not skipped. A launch pointing at documentation nobody verified builds is exactly the
  failure this gate exists for; record it and decide explicitly.
- **No positioning artifact exists** → do not invent the claim here. Stop, run `position-project`,
  and record the dependency in the plan.
- **No audience evidence at all** (first-ever launch) → say so, pick at most two channels, treat
  the launch as a measurement rather than a result, and set the thresholds accordingly.
- **`superpowers` installed** → invoke `superpowers:verification-before-completion` before the
  readiness verdict is written; the gate is a claim of completeness and must be evidenced. If it
  is not installed, apply the same rule by hand: no check is green until its command output has
  been read in this session, and the plan records what was read.

## Deliberately not covered

Financial projections, unit economics and break-even for the launch
(`foundry-economics:business-case-analyst`, `cost-engineer` — growth writes the argument,
economics writes the numbers); grant and public-funding paperwork
(`foundry-economics:funding-analyst`); the contributor funnel, CONTRIBUTING, governance and
release notes inside the repository (`foundry-oss`); README and documentation authoring
(`foundry-research`); roadmap, backlog and delivery reporting (`foundry-pmo`); privacy, marketing
consent, GDPR for any contact list, advertising-claims law and sponsorship disclosure
(`foundry-legal`); and product, architecture or code decisions (`foundry-dev`). Sustained
editorial cadence after the launch day belongs to `build-audience`, not here.

## Bundled references

- `references/readiness-checklist.md` — the blocking and non-blocking checks, each with the exact
  command to run against a pristine checkout, its pass condition, and what a red result means.
- `references/channel-selection.md` — scoring channel fit from evidence rather than from a list of
  platforms, plus the runtime rules-verification protocol and the tactics refused by name.
- `references/post-launch-retrospective.md` — the day-14 procedure that separates wrong channel
  from wrong positioning from no demand, with the discriminating evidence for each.
