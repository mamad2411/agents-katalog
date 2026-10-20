---
name: find-collaborators
description: Find the right person to work with in your own field, in the order that actually works — the gap named as exactly one of skill, capacity, credibility or access with evidence from this repository, the offer and the non-negotiable terms written down before any name is looked at, candidates derived from artifacts they actually shipped, wrote, maintained, answered or spoke rather than from a list of platforms, each person's current situation and stated availability verified at runtime and dated, one rewritten message per person, the fit conversation including the questions people skip, a trial capped in hours with a calendar end date, and ownership, credit, decision rights and exit agreed before real work starts. Use when a project has outgrown one person, when a needed skill is missing, when looking for a co-founder, co-maintainer, co-author or research partner, before sending any outreach, or when a previous collaboration ended badly and the next one must not. Produces docs/growth/collaborators.md. Refuses scraped lists and mass identical messages, and hands contracts, IP assignment and employment classification to foundry-legal.
user-invocable: true
argument-hint: "[--gap skill|capacity|credibility|access] [--trial]"
agent: foundry-growth:collaborator-scout
model: sonnet
effort: medium
metadata:
  foundry.vertical: growth
  foundry.io: "requirement.v1 -> plan.v1 + docs/growth/collaborators.md"
license: Apache-2.0
---

# Find collaborators

Collaborations rarely fail on skill. Skill is visible in the first deliverable. What is not visible
is who decides, who owns the output, what "committed" means in hours, and what happens when one
person's circumstances change — and those stay invisible until the work has acquired enough value
to be worth arguing about, which is exactly when they are hardest to settle.

So the order is fixed and it is not the intuitive one: **gap → offer → non-negotiables → evidence
sourcing → runtime verification → approach → fit → trial → terms → write-up**. Searching first and
defining later is the characteristic failure of this whole area — it finds impressive people rather
than the right one, and "impressive" is how a project ends up with two people who both want to do
the interesting half.

You draft; the caller sends. Nothing here contacts anyone. Outreach outcomes enter the document
only when the caller reports them, and a row with no reported outcome stays `awaiting-send`.

`--gap` accepts `skill`, `capacity`, `credibility` and `access`; `domain` is accepted as a synonym
for `access`. Passing it does not skip Step 1 — it is a hypothesis the evidence must confirm.
`--trial` enters at Step 8 for a candidate whose Steps 1–7 are already in the document; it still
refuses to run if the gap statement or the non-negotiables are missing.

## When not to use this

- **You want strangers to arrive at the project all at once** → `plan-launch`. Broadcast and
  one-to-one approach are different instruments; using this skill to plan an announcement produces
  a shortlist nobody wanted, and using `plan-launch` to reach one maintainer wastes the channel.
- **You want sustained attention over a quarter** → `build-audience`.
- **You want contributors *inside* an existing open source repository** — `CONTRIBUTING.md`,
  good-first-issue curation, triage rotation, release notes → `foundry-oss:community-manager`. This
  skill brings people to the door from outside; what happens once they are inside is not ours.
- **You want money rather than a person** → `prepare-fundraise`. An angel who also advises is a
  fundraising conversation with a collaboration attached, not the reverse.
- **The project cannot state in one sentence who it is for** → run `position-project` first. You
  cannot write an honest offer about a project whose claim is undecided, and Step 2 will stall.
- **The answer has to hold for people who were not in the conversation** — a governance model, RFC
  thresholds, maintainer onboarding and removal, CLA-vs-DCO as *project policy*, succession →
  `foundry-oss:governance-architect`. The dividing line is the number of people: this skill writes
  what two people understand themselves to have agreed, before there is anything to govern.
- **The person is already in and the question is who does what** → `foundry-pmo` owns task
  allocation and delivery reporting.
- **What you actually need is a contract, an IP assignment, a CLA, an NDA, or an answer about
  employee-versus-contractor classification** → `foundry-legal:licence-analyst`, always. This skill
  produces a shared understanding in plain language and stops there.

## Rules that bind every step

Not style preferences. A collaborators document violating any of them is rejected on review.

1. **Nothing about the outside world from memory.** A person's availability, employer, interests or
   location; a community's rules; a conference date or CFP deadline; a "best time to reach out"; a
   reply-rate benchmark; an accelerator's intake. All of these go stale. Fetch the page or profile
   in this session, read what it says today, and record the URL with `checked: YYYY-MM-DD`. What
   you could not fetch is written `UNVERIFIED — confirm before contacting`, never as fact.
2. **No fabricated social proof, in the offer or in a message.** No user count that was not
   counted, no logo of a non-user, no "several people have already joined" that means one maybe, no
   revenue not received, no funding not committed in writing, no invented deadline or scarcity.
3. **Every claim about the project points at an artifact** — a path in this repository, a command
   whose output was read, or a fetched URL. A load-bearing claim with no artifact is **cut**, not
   softened into a vaguer version of the same untruth.
4. **Consent-respecting contact only.** Scraped or purchased lists, addresses harvested from commit
   metadata or attendee lists, unsolicited bulk mail, and mass-automated identical messages are
   refused **by name** — including when the caller calls them efficient. The lawfulness question
   (GDPR Art. 6 lawful basis, Art. 14 information duty where data was not obtained from the person,
   Directive 2002/58/EC Art. 13 on unsolicited communications) belongs to
   `foundry-legal:privacy-engineer`, not to your judgement: flag it, hand it over, do not improvise.
5. **Data minimisation, because this file gets committed.** `docs/growth/collaborators.md` is a
   tracked file about real people. Record only what they published, and only the URL of where they
   published it — the record is a pointer, not a copy. No email address, no phone number, no private
   handle, no inferred circumstance, no note you would not send them. This is why every command
   below drops the address field: `git shortlog -sn`, never `-sne`. When the run ends, delete the
   records of anyone who declined or did not reply, and say in the document that you did. If the
   caller wants to keep a contact detail the person did not publish, that is a personal-data
   retention decision — emit the `foundry-legal:privacy-engineer` handoff and do not decide it here.
6. **Prefer the smallest honest version.** Recommend five researched messages over five hundred
   templated ones because it is the version you can stand behind and the one that still works the
   second time you need it — not because it converts better, which neither you nor the caller has
   measured. State plainly that its ceiling on volume is lower. Say this even where a reader expects
   the opposite advice.

## Step 1 — write the gap down before you look at anyone

One sentence, naming **exactly one** of the four gaps, with a consequence someone else could test:

> *"Without a collaborator who has shipped a production Angular design system, `packages/ui` stays
> at 40 % of the component set and the 2026-11 release slips."*

The four gaps attract different people and need different arrangements, and diagnosing the wrong
one is why a search "works" and the collaboration still fails. The worksheet — what each gap means,
the evidence that it is the real one, who it attracts, the arrangement that fits, and the specific
failure when it is misdiagnosed — is `references/gap-types.md`. Work through it rather than
picking from the names.

Back the gap with **at least two pieces of evidence from this repository or its tracker**, gathered
by command, not by impression:

```bash
git log --since="90 days ago" --format='%an' | sort | uniq -c | sort -rn   # who is actually here
git log -1 --format=%cI -- <blocked-path>                                  # how long it has stalled
command -v gh >/dev/null && gh issue list --state open --label help-wanted --json number,title,createdAt
ls docs/adr/ 2>/dev/null                                                   # a decision waiting on expertise
```

**Gate:** if two gaps look real, rank them and search for one. A person who closes two gaps exists
but is not findable on purpose. Record the chosen gap as a `decision` fact through the `foundry`
MCP tool `memory_write` so the next wave does not re-litigate it — never edit
`.foundry/memory/facts/` by hand.

## Step 2 — write the offer, both halves, before any name

An offer with no stated limits reads as an offer of everything, so both halves are mandatory.

**On the table for most projects:** money; equity or revenue share; first-class credit (co-author,
co-maintainer, a `CITATION.cff` entry, a named CRediT contributor role); decision rights over a
named subsystem; a problem they cannot get at their day job; access to your data, users or network;
distribution of their work to your audience; a reference they can use; your time on something *they*
need.

**State plainly what you cannot give:** hours you do not have, a salary you cannot pay, a decision
you will not delegate, an exclusivity you will not honour, a timeline you cannot hold.

Two binding rules, both instances of rules 2 and 3 above:

- **Never inflate the project's position to make the offer look better.** Every claim in the offer
  gets a row in the claim ledger of Step 10 with an artifact path or a fetched URL beside it.
  Rows with no evidence are cut.
- **State the unattractive truth early** — zero budget, a pre-alpha codebase, a licence they may
  dislike, a hard dependency on your availability. Someone who declines because of it has cost you
  one message; someone who discovers it later has cost you both a trial and the argument after it.

## Step 3 — the non-negotiables, before the search

Three or four lines, written now, while nobody attractive is in the frame. Their whole purpose is
to be immune to a candidate you like:

- The **licence** the work must ship under, read from the repository rather than remembered:
  `ls LICENSE* NOTICE CITATION.cff` and
  `grep -rn --exclude-dir=.git -m1 "SPDX-License-Identifier" . | head` — record the SPDX License
  List identifier you actually found, and write `not declared` if the grep returns nothing rather
  than filling in the licence you expect the project to use.
- **Decisions you will not delegate**, named as subsystems or decision types.
- **Credit you have already promised** to someone else.
- Any **hard constraint**: timezone overlap needed, a data-access rule, an existing exclusivity, a
  deadline that cannot move.

**Gate:** these are written into `docs/growth/collaborators.md` before Step 4 begins. A
non-negotiable discovered after meeting a candidate is a preference; only what was written first
survives a conversation with someone you want to say yes to.

## Step 4 — derive candidates from evidence, never from a list of platforms

Do **not** produce "post in the usual developer communities". Platform lists go stale, their rules
change without notice, and they are not where the specific person for a specific gap is. Start from
artifacts that already exist. Five trails, in rough order of yield:

1. **Who maintains what you already depend on** — pre-filtered for the skill, already fluent in the
   problem space.
2. **Who has shipped the thing you cannot ship** — not who talks about it; who has a repository, a
   release, a deployed artifact.
3. **Who answers questions in it**, patiently and repeatedly. This is the only trail where you can
   watch someone explain something to a person who is stuck, which is closer to what working with
   them is like than any credential. It remains your judgement, not a measured correlation — record
   it as one.
4. **Who has published or spoken on it** — author lists, programme pages, proceedings, and the
   co-author graph around them.
5. **Who has already touched this project** — a good bug report, a review, a fork that fixed
   something. Warm, and self-selected.

Detect each tool before use, and confirm any flag or `--json` field you are unsure of with
`gh <command> --help` rather than from memory — `gh`'s surface changes between releases.

```bash
command -v gh >/dev/null && gh auth status            # gate for every gh call below

# trail 1 — read whichever manifest this project actually has, not the one you expect
ls package.json pom.xml build.gradle build.gradle.kts requirements.txt pyproject.toml \
   Cargo.toml go.mod Gemfile composer.json 2>/dev/null
# then, per dependency you would be in trouble without (usually fewer than ten):
gh api "repos/<owner>/<repo>/contributors?per_page=10" --jq '.[].login'

gh search repos "<topic>" --sort updated --limit 30 --json fullName,owner,updatedAt   # trail 2
gh search issues "<topic>" --limit 50 --json repository,author,title,updatedAt         # trail 3
git shortlog -sn --no-merges | head -30            # trail 5 — no -e: addresses are not collected
gh issue list --state all --limit 200 --json number,author,title,createdAt # trail 5
```

Every candidate row carries `name`, `evidenceUrl` (fetched in this session), `evidenceSummary`
(what they did, one line, from the artifact), `gapAddressed` (exactly one of the four),
`checkedOn`, `contactRoute` and `provenance` (which of the five trails). **A candidate with no
`evidenceUrl` is not a candidate — delete the row rather than guess.**

`contactRoute` is the **URL** of a channel the person publishes for this purpose — an issue tracker,
a stated contact page, a contact link on their own profile — never a bare email address, phone
number or private handle (rule 5). If you cannot find one, they are not contactable, and finding a
route around that is the behaviour rule 4 refuses.

**Gate:** 5–15 candidates. Below 5 the gap statement is probably too narrow; above 15 you are no
longer writing individual messages and are drifting into the mass outreach you refuse.

## Step 5 — verify the person's current situation at runtime

Sourcing tells you what someone did. It tells you nothing about this week. Before any message is
drafted, fetch and read, in this session:

- Their **own current page or profile** — what they say they are doing now, and whether they state
  they are open to work, closed to it, hiring, on leave, or looking for exactly this.
- The **date of their most recent public activity** in the relevant area. `gh api
  users/<login>/events/public --jq '.[0].created_at'` where GitHub is the surface; otherwise the
  page's own dates.
- Any **stated contact preference or boundary**, including "no recruiters", "not looking", or a
  form they ask you to use instead.

Record each as `situationChecked: YYYY-MM-DD` with the URL. **Never assert availability, employer,
interests or location from memory or from an artifact older than the check.** Where a person states
they are not open to this, the row is closed with `respectedStatedBoundary` and no message is sent —
that is a completed outcome, not a blocked one.

## Step 6 — the approach: one person, one message, written for them

The test: if the message would still make sense with another name at the top, it is not finished.

1. One line of **specific evidence you read their work** — the actual PR, paper section, talk point
   or design decision, and what you took from it.
2. One line on **what you are doing**, concrete, with a link they can check in thirty seconds.
3. **The gap, named honestly**, including the unattractive part.
4. **One small bounded ask** — fifteen minutes, an opinion on one design choice, a look at one PR, a
   pointer to someone better suited. Never "would you like to collaborate": that asks for a decision
   they have no information to make.
5. **An explicit exit** — "if this isn't for you, no reply needed" removes the social debt that
   makes people not answer at all.

Draft one file per candidate under `.foundry/scratch/<session>/outreach/<handle>.md` (T0 scratch,
gitignored, AUTHORING.md §3) so the limits below can be checked mechanically before anything is
pasted into the document or sent. These are budgets you impose because each one is checkable, not
observed laws about how readers behave: **≤ 150 words** (`wc -w`); **exactly one ask**; no
fabricated urgency; no fabricated social proof; no superiority claim without a linked comparison
artifact; rewritten per person (the `diff`-based near-duplicate check in the reference below).
Follow up **at most once**, after a stated interval, adding new information rather than repeating
the ask. Silence is an answer — record `no-reply` and move on; never re-contact through a second
channel to route around a non-answer.

What to put in the five lines, the anti-patterns, the near-duplicate command and the tactics
refused by name: `references/outreach-guide.md`.

## Step 7 — the fit conversation, including the awkward questions

Skill is the part you can already see from the evidence trail. What you cannot see, you must ask —
and the awkward ones are asked **before** the trial, not after, because asking them early is itself
a fit test.

| Ask | Why it decides the outcome |
|---|---|
| "What does a normal week look like for you right now?" | Four hours and twenty hours are different jobs, and the number is never volunteered |
| "Is there anything that would take priority if it flared up?" | The competing commitment — an employer, a thesis, another project, a family situation — exists whether or not it was mentioned, and it decides the first busy week |
| "What would make this worth your time in six months?" | Money, credit, learning, the problem, the people — each predicts different behaviour when it gets boring |
| "How do you like decisions to get made?" | Style mismatch is felt daily and then blamed on personality |
| "Does your employment agreement say anything about outside work?" | An employer IP clause can attach their contributions to their employer without either of you noticing — then **hand it to `foundry-legal:licence-analyst`** |
| "Which part of this would you want to be responsible for?" | Two people wanting the same half is structural, not personal |
| "What ended the last collaboration, and what would you do differently?" | The most informative question, and the one most often skipped |

Record their **answers as notes of what they said and when** — not as conclusions about the person.
Rule 5 applies here too: these notes land in the same tracked file. You are keeping a working
record, not building a profile, and anything that starts to look like a dossier on a private
individual is refused here rather than written more carefully.

## Step 8 — the trial project, with an end already scheduled

A trial is the only reliable evaluation; everything before it is prediction. Size it so that
**ending it costs nobody much** — that single constraint is what makes it safe for both sides to be
honest on the last day. All six properties, or it is not a trial:

- A **real deliverable**, useful whether or not the collaboration continues. Never make-work.
- An **hour cap per side**, agreed in writing before it starts. Default **≤ 20 hours**; a caller may
  raise it, and then the new cap and its reason are recorded rather than left implicit.
- A **calendar end date**, not "when it's done".
- A **written definition of done** with a URL at the end — a merged PR, a shipped page, a submitted
  draft, a reviewed design document.
- A stated **"what we each keep"** if it stops here: who owns the output, under which SPDX
  identifier, and whether either side may reuse it.
- A **review meeting on the end date** at which "we stop here" is an explicitly acceptable outcome
  that neither side has to justify.

Observe and record: did they do what they said by when they said; what happened when something went
wrong (silence, or a message); response latency in hours under normal conditions; how disagreement
about a decision was handled; whether the work needed more correction than it saved.

**Gate:** a trial that ends with no deliverable and no conversation about why *is* the result. Write
that plainly rather than extending it. Extending is how a bad fit becomes a standing obligation
nobody ever decided to take on, because the decision never has to be made out loud.

## Step 9 — the terms conversation, before work scales past the trial

Seven things get written down. **"TBD" on any of them is a blocking finding, not a note.**
Ownership; licence (the SPDX identifier read from `LICENSE`, and which of a Developer Certificate of
Origin sign-off, a CLA or nothing already covers this person's inbound contributions — *recording*
what applies, never *setting* the project's policy, which is `foundry-oss:governance-architect`);
credit (exact form — co-author, co-maintainer, `CITATION.cff` entry, CRediT role, byline, or
nothing); decision rights and the tiebreak; money, including when the answer is "none"; stop-work if
one person disappears for a month; and exit — notice, what each takes, what each leaves, what either
may say publicly.

Name those standards without quoting a version or clause number from memory. If a specific version
of the Developer Certificate of Origin, the CRediT taxonomy or the Citation File Format is going to
appear in the document, fetch the current published text first and record the date — a version
number recalled rather than read is exactly the assertion this repository deletes.

The full list written as questions to answer, with the failure each one prevents and the wording
that gets a real answer rather than a polite one: `references/terms-checklist.md`.

You write **the plain-language agreement**: what both people understand themselves to have agreed.
You do **not** draft a contract, an IP assignment, a CLA, an NDA, or anything touching employment or
contractor classification, and you say so out loud rather than producing a document that looks
signable. The moment the agreement is meant to be signed, or an employer's or university's IP clause
enters the conversation, emit a `handoff.v1` to `foundry-legal:licence-analyst` and stop there; the
moment a contact detail the person did not publish, or a contact list carrying personal data,
appears, the handoff goes to `foundry-legal:privacy-engineer` instead. Say plainly in the summary
that what you produced is a shared understanding, not a legal instrument.

## Step 10 — write it down

`docs/growth/collaborators.md`, in this order: the one-sentence gap statement with its gap type and
the ≥ 2 repository evidence items; the offer, both halves; the non-negotiables from Step 3; the
claim ledger (claim | evidence artifact | verified on | verdict, including the cut rows and why);
the candidate table with every required field; the runtime-verification log with URLs and dates; the
outreach drafts and their outcomes; the fit notes; the trial definition with its six properties; the
seven terms with no TBD; open risks; review date ≤ 90 days. Then delete the rows of anyone who
declined or did not reply (rule 5) and state in the document that you did.

Emit `plan.v1` to `.foundry/blackboard/<wave>/collaborator-scout.json` via `blackboard_write`, with
seven waves, one per stage (`gap`, `offer`, `sourcing`, `outreach`, `fit`, `trial`, `terms`), each
carrying a machine-checkable `gate`, and an `outOfScope` naming at least contracts, IP assignment,
compensation and the project's governance model. `plan.v1` sets `additionalProperties: false` and
each wave requires `id`, `tasks` and `gate`, so candidate records, message drafts and fit notes live
in the document and **not** in the artifact — the wave gates assert counts against the document
instead, and a write carrying extra fields is rejected by the `validate-contract.mjs` `PostToolUse`
hook rather than silently accepted. Return to the caller **only** that path plus a summary of
**≤ 300 tokens**: the
gap type, the count of evidence-backed candidates, the single riskiest unagreed term, and any
decision only the caller can make. Never paste candidate dossiers or message drafts into the parent
context.

## Exit criteria

1. `docs/growth/collaborators.md` exists and opens with a one-sentence gap statement naming exactly
   **one** gap type and a testable consequence.
2. The gap is backed by **≥ 2** evidence items from this repository or its tracker, each with the
   command or path it came from.
3. The offer lists **≥ 3** concrete things offered and **≥ 2** things explicitly not offered.
4. The gap, offer and non-negotiables sections each appear above the candidate table and each carry
   a `written: YYYY-MM-DD` line; the latest of those dates is **≤** the earliest `checkedOn` in the
   candidate table. A non-negotiable added after a candidate was seen is a preference, not a
   non-negotiable, and is struck.
5. Candidate rows: **5–15**. Rows missing `evidenceUrl`, `evidenceSummary`, `gapAddressed`,
   `checkedOn`, `contactRoute` or `provenance`: **0**.
6. Rows sourced from a scraped, purchased or bulk-harvested list: **0**, asserted in the document.
7. Every contacted candidate has a `situationChecked: YYYY-MM-DD` with the URL read this session.
   External facts asserted without a check date or an `UNVERIFIED` marker: **0**.
8. Every outreach draft is **≤ 150 words**, names one specific artifact of that person with its URL,
   and contains **exactly one** ask. Pairs of drafts differing only in the name and the evidence
   line: **0**.
9. Claim ledger complete: every claim about the project carries an artifact path or fetched URL, or
   appears with verdict `cut`. Fabricated testimonials, logos, counts, deadlines or scarcity:
   **exactly 0**, and the ledger shows it.
10. Fit questions: all **7** rows of Step 7 answered for every candidate reaching trial stage, none
    blank.
11. Trial defined with all **6** properties, including the hour cap per side (**≤ 20** by default,
    or a higher cap with its recorded reason), a calendar end date, a URL-bearing definition of done
    and the "what we each keep" line.
12. All **7** terms recorded with **zero** "TBD"; the SPDX identifier read from `LICENSE` rather
    than assumed (or recorded as `not declared`); the DCO-or-CLA answer for this person's inbound
    contributions recorded, with any standard's version number fetched rather than recalled.
13. Email addresses, phone numbers and private handles written into `docs/growth/collaborators.md`:
    **0**. Records retained for people who declined or did not reply: **0**, with the deletion
    stated in the document.
14. A `handoff.v1` exists to `foundry-legal:licence-analyst` whenever a contract, IP assignment or
    employer IP clause appeared, and to `foundry-legal:privacy-engineer` whenever an unpublished
    contact detail or a contact list carrying personal data appeared.
15. `plan.v1` validates via `contract_validate`, has a `gate` on all **7** waves and a non-empty
    `outOfScope`; the caller summary is ≤ 300 tokens.

## Degradation

- **`gh` absent or unauthenticated** (`command -v gh` fails, or `gh auth status` is non-zero) →
  announce it once, fall back to `git shortlog -sn --no-merges` plus pages fetched by hand, and mark
  every GitHub-derived field `unavailable`. Never invent a contributor list, and never restore the
  `-e` flag to recover the addresses rule 5 rules out.
- **`WebFetch` and `WebSearch` both absent** → nothing outside the repository can be verified.
  Restrict sourcing to trails 1 and 5, state in the document that off-repo sourcing was not
  performed, and mark criterion 7 **unverified** rather than filling dates from memory. Do not
  contact anyone whose current situation could not be checked.
- **No repository yet (idea stage)** → the gap statement has no repository evidence, so it is
  written from the caller's own statements, marked `confidence: low`, and the trial becomes the
  first evidence rather than the last check.
- **Caller arrives with a shortlist and no gap statement** → stop, write Steps 1–3 first, then test
  the shortlist against them. Names that fail the written gap are dropped, including good ones.
- **Caller insists on a bulk or purchased contact list** → refuse the list by name, record it as a
  `risk.v1` with `category: people`, emit the `foundry-legal:privacy-engineer` handoff, and continue
  with the evidence-derived shortlist. Do not run both and let the caller choose. `risk.v1` requires
  `impactEur`: set it to `0` with the reason in `detection` rather than inventing a figure — a euro
  amount that has to be real is `foundry-economics:cost-engineer`'s work.
- **Zero candidates for the stated gap** → a finding, not a pass. Say whether the gap is specified
  too narrowly or the offer is not viable at this stage, and propose broadening exactly one
  dimension.
- **`superpowers` installed** → invoke `superpowers:brainstorming` for Step 2 (the offer is exactly
  the "explore intent before building" case) and `superpowers:writing-plans` when the trial needs
  breaking into checkable steps. If it is absent, use the Step 2 lists and the six trial properties
  as the reduced checklist and mark the offer `confidence: medium` until the caller confirms it.
- **`foundry` MCP server unavailable** → write the artifact to
  `.foundry/blackboard/<wave>/collaborator-scout.json` by hand, record the gap decision in the
  document instead of through `memory_write`, and state in the summary that it was not
  schema-validated by `contract_validate`.

## Deliberately not covered

Contracts, IP assignment, CLA and NDA drafting, employee-versus-contractor classification and
SPDX obligations (`foundry-legal:licence-analyst`); lawful basis for any contact list, retention of
candidate records and sponsorship disclosure (`foundry-legal:privacy-engineer`) — both refused here
by design, not by capacity; the project's governance model, RFC thresholds, maintainer onboarding
and removal, and CLA-versus-DCO as project policy (`foundry-oss:governance-architect`); equity
splits, day rates, what a collaborator costs and break-even
(`foundry-economics:cost-engineer`, `business-case-analyst` — growth writes the argument, economics
writes the numbers); grant consortium paperwork, eligibility forms and budget tables
(`foundry-economics:funding-analyst`); the contributor funnel inside the repository, `CONTRIBUTING`,
governance, triage and release notes (`foundry-oss`); public launch channels and announcement
sequencing (`plan-launch`); editorial cadence and sustained attention (`build-audience`); portfolio,
public writing, talks and CFPs as reputation work in general (`personal-brand-strategist`); the
one-sentence claim and who the project is for (`position-project`); task allocation and delivery
reporting once someone is in (`foundry-pmo`); README and documentation authoring
(`foundry-research`); and architecture, code and product decisions (`foundry-dev`).

## Bundled references

- `references/gap-types.md` — the gap-definition worksheet: skill, capacity, credibility and access
  side by side, the evidence that identifies each, what each implies about who to look for and which
  arrangement fits, and the specific failure each misdiagnosis produces.
- `references/outreach-guide.md` — what makes a message get a reply, the anti-patterns that
  guarantee silence, the mechanical near-duplicate check, and the tactics refused by name including
  scraped lists and mass identical messages.
- `references/terms-checklist.md` — the questions to settle before work starts, written as questions
  to answer rather than as legal text, with the failure each one prevents and the point at which the
  conversation stops and goes to `foundry-legal`.
