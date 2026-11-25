---
name: write-requirements
description: Elicit and record requirements as requirement.v1 artifacts with the ambiguity checklist applied — story mapping, Given/When/Then acceptance criteria, measurable non-functional targets, and requirement-to-test traceability. Use before planning or building anything whose success criteria are not yet written down. Not for roadmap sequencing or backlog mechanics.
argument-hint: "[--from docs/notes.md] [--kind nfr] [--check-only]"
user-invocable: true
agent: foundry-pmo:requirements-analyst
model: opus
effort: high
metadata:
  foundry.vertical: management
  foundry.io: "stakeholder intent -> requirement.v1 + docs/requirements/*.md"
license: Apache-2.0
---

# Write requirements

Turn what people say they want into statements that can be proved true or false. Most of the
work is subtraction: removing solutions disguised as requirements, and removing adjectives that
stand in for numbers.

`--check-only` runs the ambiguity checklist over existing requirements and reports, without
authoring anything.

## Step 0 — Read what already exists

```bash
ls -1 docs/requirements/*.md 2>/dev/null | head -50
ls -1 .foundry/blackboard/*/requirements-analyst.json 2>/dev/null
ls -1 docs/adr/*.md 2>/dev/null
grep -rEo '@REQ-[0-9]{4}' --include='*.spec.*' --include='*.test.*' . 2>/dev/null | sort -u | head -50
gh --version >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && echo GH_OK || echo GH_UNAVAILABLE
```

Record: highest existing `REQ-NNNN` (new ids continue from there — never reuse or renumber),
which constraints already exist as ADRs, and which requirement ids are already referenced by
tests. If `gh` is unavailable, say so; do not assert whether something is already tracked.

## Step 1 — Map before you decompose

Delegate the fuzzy front end when possible:

> If the `superpowers` plugin is installed, invoke `superpowers:brainstorming` to open up the
> problem space before narrowing to requirements, then return here. If it is not installed, work
> §1 and §2 of `references/story-mapping.md` manually and say that ideation was unassisted.

Build the story map: a backbone of user activities in **user time order**, and a walking
skeleton — the thinnest slice that touches every activity.

```
Backbone : Discover → Configure → Purchase → Receive → Support
Release 1: exact-name search | default option | one payment method | email confirmation | contact link
Later    : faceted search | bundles | saved cards | tracking | self-service returns
```

A release that completes one activity fully and none of the others cannot be used by anyone.
Cells with deliberately no requirement become entries in the roadmap's `outOfScope`, not silence.

## Step 2 — Strip solutions out of the intent

For each stated intent, ask *why* until you reach a user outcome, then stop.

| Stated | Actually is | Record instead |
|---|---|---|
| "We need Redis caching" | a solution | the latency/throughput NFR that motivated it |
| "Add a country dropdown" | a solution | "the user can state their country from the supported set" |
| "Nightly batch job" | a solution | a freshness NFR: data no older than X |
| "Work like the old system" | not a requirement | enumerate each behaviour that must be preserved |

When the stakeholder genuinely has authority over the solution — a mandated vendor, a corporate
standard, a contract — it is `kind: constraint`, and you cite the source of the authority.

## Step 3 — Acceptance criteria as Given/When/Then

```
Given a registered user with a verified email and no active subscription
When they submit the checkout form with a card that expired last month
Then the payment is not attempted, the form shows "This card has expired", and the
     attempt is recorded with reason CARD_EXPIRED
```

Rules:
- **Given** sets up a concrete state, specific enough to actually build.
- **When** is exactly one action. Two "and"-joined actions are two criteria.
- **Then** is observable from outside — what the actor sees, or what a system can query.
- Cover the happy path, ≥ 1 rejection path and ≥ 1 boundary. Happy path only = half specified.
- No internal implementation details (table names, class names, internal queues). If you cannot
  express the outcome from outside, the requirement is written at the wrong level.
- Error criteria state both the user-visible message class and the recorded system state, so
  logging is specified rather than discovered later during an incident.

Patterns and worked examples: `references/acceptance-criteria.md`.

## Step 4 — Non-functional requirements need four things

Metric, comparator + value + unit, condition, and observation window — plus the measurement
method. Template:

```
<quality> of <what>, measured as <metric>, must be <comparator> <value> <unit>
under <load/condition>, over <observation window>, measured by <method/tool>.
```

```
p95 server response for GET /orders must be ≤ 300 ms at 200 req/s sustained,
over a rolling 1 h window, measured at the load balancer.
```

Cite the standard where one exists — WCAG 2.2 success criterion numbers, OWASP ASVS control ids,
ISO/IEC 25010:2023 characteristics, GDPR articles, RFC numbers. A citation turns an argument
about taste into a check. Catalogue by quality: `references/nfr-catalogue.md`.

## Step 5 — Run the ambiguity checklist

Mechanical, every time, over every requirement and criterion. Full table with the exact
replacement question for each entry: `references/ambiguity-checklist.md`.

```bash
# first-pass scan of requirement documents
grep -rnEi '\b(fast|quick|responsive|snappy|performant|scalable|secure|user-?friendly|intuitive|seamless|reliable|stable|robust|flexible|configurable|extensible|simple|easy|modern|best practice|industry standard|approximately|roughly|around|etc\.?|and so on|improve|optimi[sz]e|enhance|better|minimal|real-?time|as needed|if necessary|where appropriate|should be able to)\b' \
  docs/requirements/ 2>/dev/null
```

The grep finds candidates; judgement confirms them — "secure channel" inside a cited ASVS
control is fine, "must be secure" is not.

Every surviving hit produces one rejection-list line:

```
REQ-0042 — blocked on "fast" in "search must be fast"
  question: At which percentile, for which query type, under what catalogue size, in ms?
  awaiting: M. Bianchi (product)  since: 2026-08-27
```

**Never quantify on the stakeholder's behalf and present it as theirs.** An assumed number
becomes a commitment the moment it is written down.

Structural checks, beyond the word list:
- Dangling comparatives ("better", "more") with no comparison target.
- Unbounded quantifiers ("all files" — of what size, count, format?).
- Passive voice hiding the actor ("the data will be validated" — by whom, where, when?).
- Compound requirements — any "and"/"or" in the title means split it.
- Negative-only requirements ("must not crash") — state the positive behaviour.
- Undefined domain terms — if "account", "order" or "active" is not in a glossary, write a
  `fact.v1` of type `glossary` before proceeding.

## Step 6 — Prioritise honestly

MoSCoW, with a hard constraint: `must` ≤ **60%** of the release's expected effort. Above that,
priority carries no information and there is no contingency.

Test for every `must`: *what does the organisation do if this ships without it?* If the answer
is "ship anyway", it is a `should`. `wont` items are recorded, not deleted — they are the scope
boundary and they prevent re-litigation.

## Step 7 — Traceability

```
REQ-0042
  ├─ adr-0007                                      why the design permits it
  ├─ test:checkout.spec.ts#"declines expired card"  proves criterion 2
  ├─ test:e2e/purchase.spec.ts#"@REQ-0042"          proves criterion 1
  ├─ issue:#318                                     the work item
  └─ release:v1.4.0                                 where it shipped
```

Tag tests with the requirement id so the link survives refactoring, then verify mechanically:

```bash
grep -rEo '@REQ-[0-9]{4}' --include='*.spec.*' --include='*.test.*' . | sed 's/.*@//' | sort -u > /tmp/req-in-tests.txt
grep -hEo 'REQ-[0-9]{4}' docs/requirements/*.md | sort -u > /tmp/req-on-disk.txt
comm -13 /tmp/req-in-tests.txt /tmp/req-on-disk.txt   # coverage gaps: requirements with no test
comm -23 /tmp/req-in-tests.txt /tmp/req-on-disk.txt   # orphan tests: tagged to a dead requirement
```

Report both counts. Target for `priority: must` is zero coverage gaps. If you did not run the
commands, report the matrix as **unverified** — a traceability matrix maintained by hand is a
matrix that is already wrong.

## Step 8 — Emit

```json
{
  "schema": "requirement.v1",
  "producedBy": "requirements-analyst",
  "id": "REQ-0042",
  "kind": "functional",
  "title": "Checkout rejects expired cards before authorisation",
  "userStory": "As a shopper, I want to be told immediately that my card has expired so that I can use another card without waiting for a decline",
  "acceptanceCriteria": [
    { "given": "a registered shopper with a card expiring last month", "when": "they submit checkout", "then": "no authorisation is attempted and the form shows \"This card has expired\"" },
    { "given": "a card expiring this month", "when": "they submit checkout", "then": "authorisation proceeds normally" }
  ],
  "priority": "must",
  "tracesTo": ["adr-0007", "test:checkout.spec.ts#declines-expired-card", "issue:#318"],
  "owner": "M. Bianchi"
}
```

1. Validate each with `mcp__plugin_foundry-core_foundry__contract_validate`.
2. Write via `mcp__plugin_foundry-core_foundry__blackboard_write` to
   `.foundry/blackboard/<wave>/requirements-analyst.json`.
3. Render `docs/requirements/REQ-NNNN-<slug>.md` from `templates/requirement.md`.
4. Write a `fact.v1` of type `constraint` for each discovered constraint, and `glossary` for each
   defined term, via `mcp__plugin_foundry-core_foundry__memory_write` — never by hand.
5. Print the rejection list separately. It is the most useful output of the session.

Then hand off: sequencing to `roadmap`, tracker items to `groom-backlog` / `github-setup`,
failing tests first to `superpowers:test-driven-development`.

## Exit criteria

- [ ] A story map exists with a named backbone and an identified walking skeleton.
- [ ] Every requirement has ≥ 1 Given/When/Then criterion; every `must` also has ≥ 1 rejection
      path and ≥ 1 boundary criterion.
- [ ] Ambiguity checklist run; zero blocked words in accepted requirements; every hit on the
      rejection list with an exact question and a named owner.
- [ ] Every NFR states metric, comparator, value, unit, condition, window and method.
- [ ] Every NFR mapping to a published standard cites it by identifier.
- [ ] No requirement contains a technology, a UI element or a process — unless `kind: constraint`
      with a cited source of authority.
- [ ] `must` ≤ 60% of expected effort, or the overage is explicitly acknowledged by the owner.
- [ ] Every requirement has a named human owner; ids continue from the highest existing.
- [ ] Traceability commands actually run; coverage gaps and orphan tests reported as counts.
- [ ] Every `requirement.v1` validates.

## What this skill deliberately does not cover

- Designing the solution — no architecture, technology choice or data model.
- Estimating effort. Requirements are an input to estimation, not an estimate.
- Sequencing and dates — use `roadmap`.
- Writing the tests. It defines what must be true; TDD writes the tests.
- Legal rulings. It records regulatory obligations and flags them for `foundry-legal`.
- UX research. It can require a usability success rate; it does not run the study.
- Filling in silence. When a stakeholder is unavailable the requirement stays open with its
  question, and never becomes an assumption presented as a decision.

## References

| File | Load when |
|---|---|
| `references/ambiguity-checklist.md` | running step 5, or arguing about a word |
| `references/acceptance-criteria.md` | criteria keep coming out untestable |
| `references/nfr-catalogue.md` | writing a measurable target for a quality attribute |
| `references/story-mapping.md` | building the backbone and the walking skeleton |
| `templates/requirement.md` | rendering `docs/requirements/REQ-NNNN-<slug>.md` |
