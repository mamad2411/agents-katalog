---
name: position-project
description: Decide who a project is for, the one sentence that claims it, what it is deliberately not, how it differs from the real alternatives including doing nothing, and the messaging hierarchy underneath — starting from what the repository actually does rather than what its author says it does, and ending with every superiority word traced to an evidence artifact or cut. Use before a landing page, launch, pitch or README rewrite, when the current description would fit three other projects, or when two people on the team answer "who is this for" differently. Produces docs/growth/positioning.md and an adr.v1.
argument-hint: "[--against <alternative>] [--audience <segment>]"
user-invocable: true
agent: foundry-growth:positioning-strategist
model: sonnet
effort: medium
metadata:
  foundry.vertical: growth
  foundry.io: "repository + requirement.v1 -> adr.v1 + docs/growth/positioning.md"
license: Apache-2.0
---

# Position a project

One project, one sentence, and a written record of everything that sentence had to give up.
The deliverable is not a slogan. It is a decision document that a landing page, a launch plan, a
pitch deck and a README can all be derived from without any of them contradicting the others.

The order is fixed: **repository first, author's description second, alternatives third, claim
fourth, non-goals fifth, name checks sixth, hierarchy seventh, evidence audit last**. It mirrors
the order of work `positioning-strategist` refuses to reverse. Writing the claim before reading
the repository produces a sentence about the project someone wishes they had built. Running the
evidence audit before the claim exists gives it nothing to audit.

## When not to use this

- **A positioning document already exists and nothing material changed.** Re-run only the steps
  affected by the change — a new competitor is step 4, a pivot is step 1 onward. Regenerating from
  scratch throws away the record of what was previously rejected and why.
- **The project has no working artifact yet**, only an idea. There is nothing in the repository to
  read, so step 1 has no input and every claim would be aspiration. Use
  `superpowers:brainstorming` to shape the idea first, come back when something runs.
- **You need the launch itself** — channels, sequencing, timing, the asset set → `plan-launch`.
  Positioning is its input, not its replacement.
- **You need sustained attention rather than a definition** → `build-audience`.
- **You need the README or the docs site written** → `foundry-research`. This skill decides what is
  true and who it is for; that vertical writes it up for users.
- **The real question is which features to build** → `foundry-dev` and `foundry-pmo`. Positioning
  describes the project that exists and names what it will never be; it does not set a roadmap.

## Step 1 — read the repository before reading the pitch

The primary source is the code and its history, not the author's summary. Establish what the
project **actually does today**, with file paths, before anyone's description is in your context.

```bash
git log --oneline -n 200 | cat
git log --since="6 months ago" --name-only --pretty=format: | sed '/^$/d' | sort | uniq -c | sort -rn | head -20
git log --format='%ad' --date=format:'%Y-%m' | sort | uniq -c | tail -18
find . -maxdepth 2 \( -name 'README*' -o -name 'CHANGELOG*' -o -name 'docs' \) -not -path './node_modules/*'
```

Record, each with the path or command it came from:

- The **top 20 changed files of the last six months** with their commit counts. That list is where
  the project's real effort went, whatever the README foregrounds.
- The **entry points a user actually touches**: CLI commands, HTTP routes, exported functions,
  plugin manifests, published packages. Name them.
- The **capability inventory**: what a user can do end-to-end today, one line each, each backed by
  a file path or a command that demonstrates it.
- **Commit cadence by month** — an active project and a dormant one need different claims, and the
  dormancy is a fact the reader will discover anyway.
- **Who arrived and what they came for**, from the issue tracker:
  `gh issue list --state open --limit 40 --json number,title,author,labels` and
  `gh issue list --state closed --limit 20 --json number,title,author,closedAt`. Read the titles —
  the words users pick for the problem are the category slot they already have. If `gh` is absent
  or unauthenticated, see Degradation.

Anything you cannot point at is not a capability. Roadmap items, half-merged branches and
"coming soon" belong in step 6, not here.

## Step 2 — compare with what the author says, and report the gap

Only now read the README, the site copy, the bio, the last pitch, any `docs/growth/*.md`. Build a
two-column table: **claimed** vs **found in step 1**, one row per claim, each row classified:

| Class | Meaning | What happens to it |
|---|---|---|
| `backed` | claimed and demonstrable from step 1 | eligible for the messaging hierarchy |
| `overstated` | real but smaller or narrower than claimed | rewritten to the demonstrable size |
| `absent` | claimed, nothing in the repository does it | cut from all copy until it exists |
| `undersold` | present and substantial, absent from the copy | candidate for the claim itself |

The `undersold` rows are the most valuable output of this step and the reason it is not optional:
a project's strongest true claim is very often something its author considers routine.

Report the gap explicitly to the user before continuing. If every row is `backed`, say so in one
line — a clean comparison is a finding, not a reason to stay silent.

## Step 3 — the audience, named narrowly enough to exclude someone

Write the audience as a **situation**, not a demographic: what is the person doing, with what,
when this project becomes relevant. "Developers" is not an audience. "A maintainer of a
multi-plugin repository who needs every asset to satisfy one contract" is.

- Name **who this is explicitly not for**, at least two segments, and why they are better served
  elsewhere. An audience nobody is excluded from is not an audience.
- Ground the audience in evidence where any exists: issue authors, stars, forks, referrers,
  support threads, actual conversations. Cite the source and the date checked (ISO 8601,
  `YYYY-MM-DD`). Read these as aggregate patterns only — do not assemble the names, handles or
  addresses behind them into a contact list. Building one is outreach, it is not positioning, and
  the consent question it raises belongs to **foundry-legal**.
- Where no evidence exists, label the audience **hypothesis** in the document and say what
  observation would confirm or kill it. Do not invent a persona and then reason from it as fact.
- Never invent a user count, an adoption figure or a testimonial to make the audience look real.
  If nobody uses it yet, the honest positioning is for a project with no users, and that document
  is still useful.

`--audience <segment>` pins a segment the user has already decided on. It does not exempt the
segment from evidence: it still gets a tier and a date, and if the repository evidence contradicts
it, say so in step 2's gap report rather than quietly positioning for a segment that is not there.

## Step 4 — the real alternatives, including doing nothing

The alternatives are what your audience does **today instead**, which is usually not a competitor.
Enumerate at least four candidates across these classes, and always include the last one:

1. A direct substitute — another tool aimed at the same job.
2. An indirect substitute — a general-purpose tool bent to the job (a spreadsheet, a shell script).
3. Building it in-house.
4. **Doing nothing** — living with the problem. This is the most common choice and the one most
   positioning documents omit, which is why they lose to it.

For each, follow the procedure and the do-nothing rubric in
`references/alternatives-analysis.md`. Two rules bind here:

- **Verify at runtime, never from memory.** Fetch the alternative's actual page or repository now
  and read it; record the URL and the date checked. Never state a competitor's pricing, feature
  set, limits, funding, popularity or roadmap from recollection — those go stale and being wrong
  about a competitor in public is unrecoverable. If you cannot fetch it, write
  `unverified — no source fetched` in that cell rather than a plausible guess.
- **Steelman before differentiating.** Write the honest case for each alternative first, including
  the cases where it is the right choice and yours is not. A differentiation that only survives
  against a strawman will not survive a reader who already uses the strawman.

`--against <alternative>` forces a named alternative into the table even if you would not have
picked it — typically the one the user keeps being compared to.

## Step 5 — the claim

One sentence, **≤ 25 words**, containing: the audience situation, the change the project produces,
and the property that makes it different from the alternatives in step 4. Template, with worked
good and bad examples and the rewrite that fixes each: `references/statement-template.md`.

Three tests, all of which must pass before the sentence leaves this step:

- **Substitution test.** Swap in the two nearest alternatives from step 4. If the sentence is still
  true of them, it says nothing; rewrite until it is false for them.
- **Evidence test.** Every load-bearing word maps to a row from step 1 or step 2 classified
  `backed` or `undersold`. A claim resting on an `absent` row is cut, not softened.
- **Inversion test.** State the opposite. If no sane project would claim the opposite ("secure",
  "fast", "easy to use"), the word is a non-differentiator and buys nothing.

Prefer the smaller true claim over the larger unprovable one, even when the larger one would
convert better. A claim that a first user disproves in ten minutes costs more than it earned.

## Step 6 — non-goals

At least **five**, each a thing a reasonable person would expect this project to do, with one line
on who or what covers it instead. Non-goals are the cheapest trust you will ever buy and the
strongest defence against the description that fits three other projects. Include:

- Adjacent capability deliberately not built, and the tool that does it.
- Audience segment deliberately unserved (from step 3).
- A scale, platform or environment out of scope.
- Anything currently `absent` from step 2 that is not on any plan — say it plainly.

## Step 7 — the name, checked at runtime or not claimed at all

`positioning-strategist` treats name checks as a mandatory stage of its order of work, so this
skill has to give their results somewhere to land. Run this step when the name is not yet public,
or when a collision has been raised. When the name is settled and nobody is questioning it, write
the single line `name settled on <YYYY-MM-DD>, not re-checked` and move on — that is a legitimate
outcome, an undated silence is not.

```bash
curl -s -o /dev/null -w '%{http_code}\n' "https://registry.npmjs.org/<name>"
curl -s -o /dev/null -w '%{http_code}\n' "https://pypi.org/pypi/<name>/json"
gh search repos "<name>" --limit 20 --json fullName,description,stargazerCount
```

Record the status codes and the repository list verbatim. Do not translate a code into a verdict
in your head and write only the verdict down — the next reader needs to see what the registry
actually returned on that date, and what a given code means is the registry's business, not yours.

Add a plain web search for the name next to the category word, because the collision that hurts is
a project users already associate with the term, not a squatted package. Record for each check:
what was queried, the literal result, and the date. Three binding rules:

- **Never write that a name is "free", "available" or "unused".** What you can write is
  "not found in the sources queried on `YYYY-MM-DD`", listing them. A registry gap is not
  clearance, and that wording difference is the whole point of the step.
- **Trademark registrability, infringement risk and any use of someone else's mark** go to
  **foundry-legal**. Do not read a registry search as a legal opinion, and do not cite a class
  number or a statute you have not read in this session.
- **Every check you could not run is named**, not dropped — it goes into the ADR's
  `consequences.risks` as an unverified name check, so the risk stays visible after the document
  looks finished.

## Step 8 — messaging hierarchy

Exactly one claim; **three** supporting pillars; under each pillar at most three proof points.
Every proof point carries an **evidence pointer**: a file path, a command whose output can be read,
a document in the repository, or a measured number with its method and the date it was measured.
A pillar that cannot field one backed proof point is not a pillar — replace it.

Then produce, all derived from the same hierarchy so they cannot drift apart:

- One sentence (the claim), for a bio line or a directory entry.
- One paragraph (≤ 60 words), for a README opening or a submission form.
- Three bullets (the pillars), for a landing page or a slide.
- The "what it is not" list from step 6, verbatim.

Copy for a specific channel is `plan-launch` and `build-audience`; this hierarchy is what they
both consume, and neither may introduce a claim that is not in it.

## Step 9 — the claim-evidence audit

Final pass over every word of every artifact produced in step 8. Work
`references/claim-evidence-audit.md` line by line. In short: every comparative, superlative,
quantity, adoption signal and safety/performance word gets a row in an audit table with its
evidence pointer, an evidence tier and a status of `backed`, `qualified` or **`unbacked`**. The
document does not ship with an `unbacked` row in it — the word is cut, not hedged into a weaker
version of itself.

Find the words with the trigger greps in step A of that reference rather than by rereading your
own prose, and record the match count in the document even when it is zero. You know what you
meant, so you will read past the overclaim; `grep` will not.

Refuse, by name and in writing, if asked for any of these: an invented testimonial; a logo of a
user who is not a user; a "trusted by N teams" where N was not counted; a benchmark not run; a
case study that did not happen; a deadline or scarcity that is not real. These are the failure
mode this skill exists to prevent, and producing one voids the whole document.

Two hand-offs are mandatory, not discretionary. Anything that touches a contact list, consent,
personal data, sponsorship disclosure or advertising-claims law goes to **foundry-legal** — flag
it, name it in the document, do not improvise a legal position and do not cite an article number
you have not read. A compliance adjective in particular is never a writer's choice: "GDPR-ready",
"SOC 2", "ISO 27001" and "certified" are licensed only by a `compliance-check.v1` artifact
produced by an assessment, and without one the word is cut. Any number describing money, unit
economics, break-even or projections goes to **foundry-economics** — positioning writes the
argument, economics owns the figures.

## Step 10 — write it down

`docs/growth/positioning.md`, in this order: date and the commit SHA the analysis was run against;
capability inventory with paths (step 1); the claimed-vs-found gap table (step 2); audience and
non-audience with evidence or the `hypothesis` label (step 3); the alternatives table with URLs
and dates checked, do-nothing included (step 4); the claim and its three test results (step 5);
non-goals (step 6); the name checks with their queries, literal results and dates, or the
`not re-checked` line (step 7); the messaging hierarchy with evidence pointers and the four
derived formats (step 8); the audit table with its trigger-grep match count (step 9); open
questions; hand-offs
raised to foundry-legal and foundry-economics; the named owner; review date ≤ 90 days.

Emit `adr.v1` to `.foundry/blackboard/<wave>/positioning-strategist.json` via `blackboard_write`,
with `options` holding **at least three** positioning candidates that were weighed, each with its
`pros` and `cons` — the schema floor is two, `positioning-strategist` requires three, and the
stricter rule wins — `decision` holding the claim, `consequences.negative` naming the audience and
use cases this positioning gives up, and `consequences.risks` carrying every unverified name check
from step 7. Check it with `contract_validate` against `adr.v1` before you call the step done.
Record the chosen claim as a `decision` fact with `memory_write` so later launch, audience and
fundraising work inherits it instead of re-deriving a different one.

## Exit criteria

1. Step 1 ran against the repository: top 20 changed files with commit counts, the entry-point
   list, and a capability inventory in which **every** line carries a file path or a command.
2. The claimed-vs-found table exists with every claim classified `backed`, `overstated`, `absent`
   or `undersold`, and the gap was reported to the user — or the line "no discrepancy found".
3. Audience written as a situation; **≥ 2** explicitly excluded segments; every audience assertion
   either carries an evidence source with a `YYYY-MM-DD` date checked or is labelled `hypothesis`
   with its falsifying observation.
4. **≥ 4** alternatives analysed, one of which is doing nothing; each row carries a URL and a date
   checked, or the literal string `unverified — no source fetched`.
5. The claim is ≤ 25 words and passes all three tests in step 5, each result written down.
6. **≥ 5** non-goals, each naming who or what covers it instead.
7. Step 7 recorded either **≥ 3** name checks, each with its query, its literal result and a
   `YYYY-MM-DD` date, or the single line `name settled on <date>, not re-checked`. The
   name-availability grep in `references/claim-evidence-audit.md` step A returns no unaudited hit.
8. Hierarchy is exactly 1 claim / 3 pillars / ≤ 3 proof points per pillar, and every proof point
   has an evidence pointer that resolves.
9. The trigger greps in `references/claim-evidence-audit.md` were run against
   `docs/growth/positioning.md`, the match count is recorded, every match has an audit row with an
   evidence tier, and the table has **zero** rows with status `unbacked`.
10. The document contains **zero** fabricated social proof: no testimonial, logo, user count,
    benchmark, case study or deadline that is not traceable to a real artifact.
11. Every legal-adjacent and every financial-figure item is listed under hand-offs to
    foundry-legal and foundry-economics respectively, with none answered inside this document.
12. `docs/growth/positioning.md` exists; the `adr.v1` passes `contract_validate` with `options`
    ≥ 3 and a non-empty `consequences.negative`; owner named; review date ≤ 90 days.

## Degradation

- **`gh` absent or unauthenticated** → skip the issue survey; state in the document that audience
  evidence is repository-only, and lower the audience rows to `hypothesis` rather than presenting
  weaker evidence as equivalent.
- **`WebFetch` / `WebSearch` absent, or the network is unavailable** → do **not** fill the
  alternatives table from memory. Write `unverified — no source fetched` in every unfetched cell,
  keep the alternative in the table, and record the verification as an open question with an
  owner. A table of remembered competitor facts is worse than an incomplete one. The same rule
  binds step 7: an unrunnable name check is recorded as `not checked` and raised as a risk, never
  answered from recollection of what was on npm the last time you looked.
- **The `foundry` MCP server is not connected** (`blackboard_write`, `memory_write` and
  `contract_validate` unavailable) → still write `docs/growth/positioning.md`, which is the
  artifact a human reads. Write the ADR body as a fenced `adr.v1` JSON block at the end of that
  document, state in one line that it was not written to the blackboard and not validated, and
  list re-emitting it as the first open question. Do not hand-write `.foundry/memory/facts/` —
  AUTHORING.md §3 reserves that path for `memory_write`.
- **Shallow clone or no git history** (`git log` fails or returns one commit) → substitute a
  directory-level capability inventory from `find` and the entry points, and say in the document
  that effort distribution could not be established.
- **No README or written description** → step 2 has one column; record "no stated description
  exists" and treat every step 1 capability as `undersold` by default.
- **Solo project, nobody to disagree with** → run the "who is this for" question against the last
  five issues or conversations instead of against a team, and mark the consensus check as not
  performed.
- **`superpowers` installed** → use `superpowers:brainstorming` before step 5 when more than one
  credible claim survives step 4, and `superpowers:verification-before-completion` before the
  document is called done, so the exit criteria are checked against output rather than intent. If
  it is not installed, walk the numbered exit criteria above by hand and record pass/fail per item
  in the document — the discipline is what matters, not the plugin.

## Deliberately not covered

Channel choice, launch sequencing and launch-day mechanics (`plan-launch`); editorial cadence and
distribution over time (`build-audience`); funder targeting and the pitch narrative
(`prepare-fundraise`); the author's own reputation as distinct from the project's
(`audit-personal-brand`); finding people to work with (`find-collaborators`). Outside this
vertical: financial projections, pricing and unit economics (`foundry-economics`); grant paperwork
and reporting (`foundry-economics:funding-analyst`); the contributor funnel, `CONTRIBUTING` and
governance once someone is already inside the repository (`foundry-oss`); the README, docs site
and technical writing (`foundry-research`); roadmap and backlog (`foundry-pmo`); consent, personal
data, trademark registrability or infringement, and advertising-claims law (`foundry-legal`); the
measurement behind any performance proof point (`foundry-quality:performance-engineer` — this
skill cites a measurement, it never produces one); what to build (`foundry-dev`).

## Bundled references

- `references/statement-template.md` — the positioning-statement template, four worked examples
  (two good, two bad) with the rewrite that fixes each, and the three tests applied in full.
- `references/alternatives-analysis.md` — how to enumerate the four alternative classes, the
  runtime-verification rules, the steelman procedure, and the rubric for evaluating "do nothing".
- `references/claim-evidence-audit.md` — the word list that triggers an audit row, the evidence
  strength ladder, the fabricated-social-proof refusal list, and the hand-off triggers.
