---
name: reopened-tickets
description: Triage and work through reopened Linear tickets on the Leap Engineering board. Use when asked what is reopened, to triage reopened tickets, to work through the reopened queue, or to pick up a specific reopened ticket. Produces a scannable table of what is back, why, and what should happen, then fixes tickets one at a time with a PR each. Covers challenging a QA note that does not warrant work, criteria QA structurally cannot test, and the traps specific to this codebase.
---

# Working through reopened tickets

Two modes. **Triage** is read-only and produces the table. **Fixing** takes rows
off that table one at a time, each as its own PR against `main`.

Never start fixing during triage. Reporting is the job; deciding is Luke's.

## Triage

Sweep every Engineering ticket in the **Reopened** status **assigned to Luke**.

```
list_issues(team: "Engineering", state: "Reopened", fields: ["title","url","status","assignee","updatedAt","labels"])
```

Somebody else's reopened ticket is not ours to triage: their QA notes are
addressed to them. List those as a one-line tally under the table, identifiers
and assignees only, and say nothing about what should happen to them.

For each ticket, in this order:

1. `get_issue` for the **current** A/Cs. Never work from a copy read earlier;
   they get edited mid-flight and half of all reopens are caused by exactly that
2. `list_comments` for everything since it last moved into Reopened. That is the
   tester's note and it is the reason it is back
3. The merged PRs, to see what shipped against what was asked
4. `gh pr view <n> --json state,mergedAt` on each. **A ticket tested before the
   merge deployed is a false reopen**, and the recommendation is to say so rather
   than change code

Then report the table below. Order rows by what Luke has to decide: **Challenge**
and **Clarify** first, since nothing proceeds on those without him, then **Fix**
rows with release-blocking ones first. Add one line above the table naming the
row to start with when severity disagrees with that order.

### The table

| Ticket | What it was | Why it's back | Recommended | Size |
|---|---|---|---|---|
| [ENG-1234](url) | One line on what it set out to do | • **A/C 3 failed.** "verbatim quote" (Tester, 4 Sep)<br>• **New:** "second quote" | • **Fix.** The actual cause and the change<br>• **Split.** Own ticket, this one closes | M |

- **The bullets pair one to one.** Third bullet in "Why" is answered by the third
  in "Recommended". Same order, same count, every row
- **Quote the tester verbatim**, with who and when. Never paraphrase a note into
  a conclusion: "totals still show gross" is actionable, "totals are wrong" is not
- **Label each finding** `A/C n failed` (a criterion the code does not meet) or
  `New` (found nearby, no criterion covers it). They lead to different answers
- **Every recommendation opens with one of five verdicts**, bolded:
  - **Fix** — a real defect. Name the cause and the change, never "investigate"
  - **Challenge** — the note or the criterion does not warrant work
  - **Split** — real but new. Own ticket, this one closes
  - **Clarify** — Luke or the tester must answer before it can be written
  - **Reproduce first** — plausible, not yet reproduced. Say what is needed
- **Size** is `S` (under an hour), `M` (half a day), `L` (bigger than the
  original ticket, and probably should not be a reopen)
- Anything too long for a cell goes in a short block under the table

## Before writing any code, check whether the criterion is stale

**This is the single highest-value check in the whole process.** In the sweep
this skill came from, of eighteen reopens only five were straightforward
defects. Six were criteria the implementation had deliberately moved past, and
the code usually said so in a comment.

So for each failing criterion, read the code that implements it and look for:

- **A superseded design.** A stage bar described as "the eleven statuses" that
  ships as five work-derived stages; a "primary action button" deleted on purpose
  with the reasoning in the file. Struck and restated, not rebuilt
- **A criterion amended to match the build**, which then cannot fail and is a
  record rather than a test. QA measuring against the pre-amendment wording is
  the commonest false reopen
- **An already-implemented criterion the tester could not trigger**, because the
  fixture they used was the wrong shape. Name the fixture, do not write code
- **Two criteria that contradict each other across sibling tickets.** Say so and
  ask; building either one breaks the other

Where the code comment justifying a decision rests on a false premise, that is
the real bug. "A client sees their own workspace's drafts because they wrote
them" is sound until an agency user writes one.

## Criteria QA cannot test

An unticked checkbox is an instruction to test. A criterion nobody can observe
through the interface, left unticked, guarantees the ticket comes back.

Legitimately code-level: internal thresholds and heuristics, "no calculation
changed", cross-agency isolation in a single-agency environment, script or job
output, resolver scoping and guard coverage.

**Not** code-level: anything visible given the right data. If QA cannot reach the
state, that needs a **named fixture**, not a dev sign-off. Find one in the real
data if you can, and hand over a URL:

- Query the warehouse (BigQuery, project `tech-aip-media`) for a row exhibiting
  the state, then resolve ids to slugs and titles through Mongo
- One concrete URL beats any amount of "needs a plan where…"

Ticking a code-level criterion requires the evidence in the comment: the file and
the test name. Same bar as QA, checked by a different person against different
material. Say explicitly that nobody exercised it through the interface, so
nobody later reads the tick as a UI pass.

Never point a criterion at a handoff document, brief or spec. A tester has no
access, so it can only ever come back blocked.

## Fixing a row

Full detail in `CLAUDE.md` under "Starting work". What is specific to a reopen:

- **Branch fresh from `origin/main`.** The original worktree was removed at
  clean-up when the PR merged. Do not resurrect the old branch, and do not build
  on anybody's in-flight branch unless told to
- **Check for a pre-existing worktree first.** `ls -d /Users/luke/dev/leap/*/`
  and look for `app-eng-1234`, `api-eng-1234`, `llm-api-eng-1234`,
  `mcp-server-eng-1234`. Several hold **staged, uncommitted work from earlier
  sessions**, sometimes exactly the fix being asked for. Preserve it before
  doing anything: `git -C <worktree> diff --cached > /tmp/eng-1234-staged.patch`,
  then apply only the parts wanted onto a fresh branch. Never touch that
  worktree's index
- **If the ticket's `V<version>` release has shipped**, the fix note goes in the
  current draft at clean-up. Never edit a shipped release note
- The handoff A/C table gets a row per criterion, and a line mapping each reopen
  bullet to what was done about it, so the tester retests exactly what they raised
- **End every ticket by re-printing the next row from the table**, re-fetched
  rather than repeated. Revise the recommendation if the re-fetch changed the
  picture, and say what changed

## Traps in this codebase

- **A new test must be seen to fail without its fix.** Revert the change, watch
  it fail, restore. This caught two tests in one sweep that asserted nothing: one
  queried a Radix menu while it was shut, one mocked `UserDisplay` as an empty div
- **Never `git checkout <file>` to undo a probe.** It reverts to HEAD and takes
  the whole fix with it. Copy the file to `/tmp` first and copy it back
- **`fireEvent.click` does not open a Radix menu.** Use `userEvent`, and assert a
  control item is present so an absence is a real absence
- **Baseline the suite before blaming the branch.** `app` carries known failures;
  the number moves as others merge. Run the same specs in a throwaway
  `origin/main` worktree and compare, rather than trusting a remembered count.
  `api`, `llm-api` and `mcp-server` are usually fully green, so a failure there
  deserves more suspicion
- **`type-check` is not covered by vitest.** Run `npm run type-check` **after**
  writing tests, not before. A spec with a type error ships green otherwise
- **An API worktree needs a plain `.env`, not the symlink.**
  `printf 'NODE_ENV=test\n' > .env`, or every DB-backed spec hangs with no output
- **`rg -r` means replace.** Use `rg -n` and quote the pattern
- `mcp-server` is Rust: `cargo test --bin leap-mcp`, `cargo fmt --check`,
  `cargo clippy`. There is no lib target
- Spanning both app and API: **merge the API first**, and say so in the PR

## Moving the ticket

Comment first, then set the status. The comment is for the tester and carries the
implementation detail; the description stays for QA and product.

Address the tester by name and tell them plainly:

- What was fixed, and what the cause turned out to be
- **Where they were right.** They usually were, even when the verdict is Challenge
- What is **not** fixed and is shipping anyway, in those words, with the reason
- Exactly what to retest, and what to leave alone
- The fixture or URL they need, if the criterion needs one

Then: `Pull Request` when a PR is open, `QA` when it needs retesting, `Release
Candidate` when it is accepted as done. Never edit or tick a criterion beyond
what Luke asked for, and never quietly close a gap: an unmet criterion that is
being accepted stays unticked, named in the comment.
