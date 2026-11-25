---
name: tw-brief-intake
description: "a new prompt arrives and the team must understand its whole intention before decomposing it: deep-research the request, then rewrite it into a systematic, comprehensive, actionable brief with acceptance criteria, frozen interfaces and a lane split"
kind: workflow
---

# tw-brief-intake

Owner role: **ceo** (created 2026-11-13). Every instance of the role runs it.

Use this skill when: a prompt arrives - the first one for a project, or a new
milestone-sized request inside one - and the team is about to decompose it.

## Why this exists

A prompt is a request, not a specification. Decomposing it directly turns the
user's ambiguity into parallel rework: every lane invents its own reading of the
same sentence, the interfaces disagree, and the first review fail is the
discovery that the team built the wrong thing quickly. The intake costs one
lane and one document, and every later lane reads that document instead of
re-reading the prompt.

Two rules hold it together. **The original is kept verbatim** - a paraphrase is
already an interpretation, and the only ground truth for an intent dispute is
what the user actually wrote. **The rewrite clarifies and never widens** -
anything the user did not ask for is marked `added:` so it can be rejected.

## Steps

1. **Record the prompt verbatim.** Paste it unchanged into `docs/Team/Project.md`
   -> `## Brief` -> `### Original prompt (verbatim)`. No cleaning, no
   translation, no summarising, no "improved" wording. Keep the whole text,
   including the parts that look like chatter: constraints hide there.
2. **Research the intention in parallel - one or more rounds.** Five probes,
   independent, each with its own evidence. The first three are minutes of
   reading; the fourth is the one that needs sources. Run a **second round** when
   the first leaves a fact unresolved, a term contested, or a choice only the
   user can make; record each round with its evidence (`prompt record --round`).
   - **Ask** - map every verb and noun in the prompt to a deliverable or a
     constraint. Anything that maps to nothing is a question or a non-goal.
   - **Why** - the job behind the request: what the user does today, what hurts,
     what "good" looks like when it is finished. A brief that cannot name the
     job is a list of tasks, not an intention.
   - **Context** - the repository, the environment, the licence, the existing
     behaviour that must not break, the budget and the deadline. Read it, do not
     assume it.
   - **State of the art** - 3 to 5 comparable solutions, how each solves it,
     what it costs, and the gap that justifies this work. Every claim carries a
     URL and an access date; unverified stays marked `UNVERIFIED`. When a
     Product Manager is staffed this probe is that lane's, recorded in
     `Research.md`.
   - **Misreading** - name the most plausible wrong build: the one that
     satisfies every word and misses the point. Then name the criterion that
     catches it. This probe is what turns a brief from a restatement into a
     defence.
3. **Enhance the prompt, then rewrite the brief.** First improve the user's own
   request with the detail the research found - same intent, precisely stated,
   every addition marked `added:` - and record it with
   `prompt record --original ... --round ... --enhanced ...`. The first
   acceptance criterion is refused until that record exists. Then write the ten
   parts below, in order, in `docs/Team/Project.md` -> `## Brief` ->
   `### Rewritten brief`. Each part is one fact per line, a table where a table
   is shorter, and no prose that the part above already carries.
4. **Ask, do not guess.** Every ambiguity that changes what gets built becomes a
   recorded question with 2-5 concrete options and a recommendation:
   `ask add --question '<it>' --option '<a>' --option '<b>' --recommend 1`. A
   blocking question holds `loop` at CONTINUE until a person answers it. Grilling
   the user once is cheaper than a lane building the wrong reading; a silent
   guess is the failure this skill exists to prevent.
5. **Freeze.** The acceptance criteria become machine records
   (`criteria add --id AC-1 --text '<verifiable statement>' --owner <role>`), the
   interfaces become the frozen contracts in `Architecture.md`, and the proposed
   lanes become the task graph in `Plan.md`. Nothing dispatches before this
   freeze: a lane that starts on a moving interface re-does its work.
6. **Independent read.** The brief is a deliverable like any other: an
   independent role - the Product Manager when staffed, otherwise the Reviewer -
   reads the original prompt and the brief and answers four questions. Is any
   intention lost? Is anything invented that the user did not ask for? Is every
   criterion verifiable by a named command and owned by exactly one role? Does
   any lane start on an interface that is not frozen? Findings return to the
   CEO; the brief is fixed before decomposition, not after the first review fail.

## The brief template (ten parts)

| # | Part | What it must contain |
|---|---|---|
| 1 | Objective | one sentence, one measurable outcome, no adjectives |
| 2 | User and job | who asks, who it is for, what they do today, what "good" looks like |
| 3 | Deliverables | named artifacts with a path each - code, docs, assets, records |
| 4 | Acceptance criteria | `AC-n` statements, each with the command or artifact that proves it |
| 5 | Non-goals | what the team deliberately does not build, and why |
| 6 | Constraints and invariants | platform, licence, budget, deadline, behaviour that must not break |
| 7 | Interfaces to freeze | the contracts each lane builds against, and who owns each |
| 8 | Lanes | the proposed split: owner, artifact, file boundary, dependency, parallel-ready or not |
| 9 | Unknowns and assumptions | every ambiguity, its resolution owner, and the test that settles it |
| 10 | Evidence plan | which test layer proves which criterion, and which role runs it |

Part 8 is what makes the team parallel: a lane is only dispatchable when it has
an owner, one artifact, a file boundary no other lane writes, and a dependency
that is either done or frozen. Everything else stays a single lane until it is.

## Rewrite rules

| Rule | Bad | Good |
|---|---|---|
| An adjective becomes a measurement, or it is deleted | "make it fast" | "p95 < 200 ms over 10k rows, proved by `pytest tests/perf -q`" |
| A vague noun becomes a named artifact with a path | "a dashboard" | "the Dashboard component, the /dashboard route, and the UI test that pins it" |
| Every "and" is a candidate lane boundary | "build the API and the docs" | two lanes, two owners, one frozen contract between them |
| One owner and one independent verifier per criterion | "we check it" | `criteria add ... --owner developer`; a different role verifies it |
| Never widen the scope; mark anything added | "the brief now includes a CLI" | "`added:` a CLI, because criterion AC-3 needs a non-UI entry point" |
| An unknown becomes an assumption with an owner, never a silent guess | nothing | "assumed the licence permits redistribution; owner: ceo; settled by `LICENSE` read + a written answer" |
| An external fact carries a URL and an access date | "most tools do this" | "title, direct URL, accessed YYYY-MM-DD" |
| Quote the user's own words where a criterion comes from them | "users want it simple" | AC-2 keeps the prompt's phrase "one command" verbatim |
| Shorter per fact, not longer per sentence | a five-paragraph restatement | one table row per fact |

The rewrite is finished when a lane that never saw the prompt can start its
first task from the brief alone, and a Reviewer can fail that task against a
criterion the brief names.

## Failure modes this catches

| Symptom | What it means |
|---|---|
| Two lanes implemented two readings of one sentence | the ambiguity was never listed as an assumption |
| A lane builds an interface another lane does not consume | part 7 was not frozen, or part 8 split on a noun instead of a contract |
| The first review fail is "this is not what was asked" | the intention was never researched; only the words were |
| The brief is longer than the prompt and says the same thing | the rewrite restated instead of specifying - no measurement, no path, no owner |
| A criterion nobody can verify | it named an adjective, not an observable outcome |
| The team built a feature the user did not request | scope widened without an `added:` marker the user could reject |
| A question reaches the user twice | the ambiguity was asked instead of recorded as an assumption with an owner |

## Evidence

Every run records the command, the revision and the observed result, as the team
requires. The intake's own record is the brief in `docs/Team/Project.md` plus the
criteria records it produced: `teamwork.py criteria list` at the revision that
landed it.

### Verdict on this skill

verdict: no observed effect

- **What was compared:** step 1 of `references/Bootstrap.md` before this skill
  existed - two bullets, "restate the prompt as objective + non-goals +
  constraints" and "record the acceptance criteria" - against the five-step flow
  this file encodes.
- **On which task and revision:** ceo T-0025 at the commit that adds this file.
  There is no run yet that reads this skill and is then reviewed, so the honest
  label is `no observed effect`.
- **Why not `helped`:** an extraction is not evidence that the flow got better;
  the first intake run after it is the observation. `confounded` would be wrong
  because the contrast is two revisions of the same document, not two tasks.
- **What would overturn it:** an intake that reads this file, produces a brief,
  and is failed by the independent read for an intention that the five probes
  would have caught - or an intake that is passed on the first round, which
  would justify `helped`.

## Guardrails

- This skill does not replace `AGENTS.md`, the red lines or the quality gates.
  If it conflicts with them, they win and this file must be fixed.
- It never bypasses self-check, independent review, the PR or the Reviewer-only
  merge, and it never weakens a test layer.
- The brief is a deliverable: it goes through the normal branch, commit, PR and
  review path, and it is never edited on `main`.
- The verbatim original is never rewritten, trimmed or "cleaned" after the fact.
  When the user changes the request, record the new prompt as a new block and
  date both; an edited original is a fabricated record.
