---
name: review-loop
description: Use when a change is reviewed, before or after its pull request opens — running /code-review or /security-review in Claude Code or /review in Codex, sending a review subagent, choosing a review level, deciding whether another round is needed, or handling the findings a review or a person's review comments return. Also at the builder check of superpowers:brainstorming and after the self-review of superpowers:writing-plans.
---

# Review loop

A review runs in rounds. Before them, `craft:product` checks whether a
capability that the branch adds is worth it: on someone else's branch that
changes code or behaviour, always; on the person's own when no report exists
for it. An over-engineering review comes next, when its skill is installed.
Then a change to a screen is walked once in the app, and the agent looks at
each screen. The first round reads the whole branch. Each later round reads
only the fixes of the round before. The loop stops at the first round that
confirms no defect, and at the latest after round 3. A defect is a wrong
result that real use reaches, or data loss or a security hole on any input,
also in a fix of the loop; a test, a comment or wording is a nit, fixed with
no round. A finding that needs a particular input is counted against real
data first, and a count of zero declines it, except for data loss or a
security hole. When the loop had more than one round, one last pass reads
the whole branch again, once. At `xhigh` in Claude Code, Codex reads the
whole branch once too. At `high` and `xhigh`, and for a change to tests
only, one review reads the tests of the whole branch once. In a project with
an architecture file or ADRs, one review reads the branch against them once,
beside round 1, at `high` and `xhigh` and for a change to that file or an
ADR. It reads a TypeScript or React change against the conventions skills
too. A security review comes last.
A change to documents only gets one round and no security review. In Claude
Code, Codex reads it once when it changes the text of a skill, a prompt or a
spec. The agent fixes and decides by itself, except for a change to business
logic and a choice for a finding outside the task, and writes a summary. When
the task is an issue taken into work, or the person asked for a pull request,
the push and the pull request follow in the same turn, on the conditions in
*The pull request* of `summary.md`. In each command and prompt, `<dir>` is
this skill's base directory.

| Moment | What must happen | Read first |
| --- | --- | --- |
| The change is documents only, or it changes the text of a skill or a prompt | One review subagent reads that text, in place of `/code-review` or beside it | `documents.md` |
| Before round 1, when *The walk* says that the change is walked | Its six steps in the app | `walk.md` |
| Round 1 starts, and *A review of the architecture* says that its step runs | Its subagent and its prompt, beside round 1 | `architecture-and-tests.md` |
| The last pass starts, or the only round of the loop confirms no defect: at `high` or `xhigh`, or for a change to tests only | The review of the tests | `architecture-and-tests.md` |
| At `xhigh` in Claude Code: the last pass starts, the only round of the loop confirms no defect, or step 4 of *The rounds* stops the rounds | Codex reads the whole branch | `codex.md` |
| The review ends, or the person answers the merge question | The check, the summary, and on its conditions the pull request and the merge question | `summary.md` |
| In Claude Code, the checks of superpowers on a spec and on a plan | Two readers of the spec and one of the plan, with no rounds | `spec-and-plan.md` |

A file in the last column sits next to this one, in `<dir>`. Read all of it
before the first step of that moment: its row is a summary, not its rules.

Why the rounds stop: on one project, nine rounds of `/code-review high`, each
over the whole branch, gave 68 findings and 25 fixes. No fix went into the
product code. One declined alternative came back in eight of the nine rounds.
On 42 merged pull requests of this plugin, the rounds after round 1 confirmed
24 defects that normal use reaches and 44 in the fixes of their own loop,
against 237 edge cases that real use does not produce, tests and wording. In
the six of them where the person said to go on after round 3, no later run
found a defect that normal use reaches.

## The level

Pick the level of `/code-review` by the weight of the change, and give the
reason in one sentence: "Why high: it changes the token refresh, which every
request goes through."

| Level | The change |
| --- | --- |
| `low` | Wording in code, or a fix in one file that adds no logic, when no test file changes. |
| `medium` | A change to tests only, or a fix in one file that adds no logic, with its tests; UI over static data with no new state rules; a move that a script or a test proves unchanged. |
| `high` | New state rules or reducer logic, a new page, route or endpoint, and any change the other rows do not name. |
| `xhigh` | Security, data loss, concurrency, or architecture across modules or apps. |

`medium` is not a default: each level needs its own reason. `max` and `ultra`
run only when the person asks; `ultra` is billed. A change to a test file is
never `low`: `/code-review low` skips test files.

A change to documents only takes no `/code-review`: one review subagent reads
the text the range changes. The text of a skill or a prompt, as a `SKILL.md`
or `rules.md`, counts as a document, though it is the product. `documents.md`
gives the prompt of that subagent, the one round of such a change, and which
review reads each range when that text comes with code.

A review subagent and Codex's `/review` have no levels.

## Worth first

Before the over-engineering review and round 1, load `craft:product`:

- on someone else's branch or pull request that changes code or behaviour,
  always, at the full depth. Their spec and description are the decisions to
  check;
- on the person's own branch that adds a capability for the product's users,
  or changes what the product does for them, when no report exists for it.
  *The trace* of `craft:product` says where a report is found.

Skip it for documents only, for a dependency bump, and for a move that a
script or a test proves unchanged. The text of a skill or a prompt that the
product ships or sends to a model, as a `SKILL.md`, is no document here: it
changes behaviour. On the person's own branch, skip it also for a bug fix that
changes no business logic.

A capability that is not worth it gets no review. A verdict other than
`do it` goes to the person before round 1, with its options, and the review
waits for the answer. With no person, the review goes on, and the question
stays open in the summary, and on the person's own branch in the pull
request's description. The report
goes where *The trace* of `craft:product` says, so that a later review
finds it.

## Over-engineering first

When the ponytail plugin's `ponytail-review` skill is in your skill list,
commit the work and run it once on the whole branch, before the first round.
It lists what to delete, replace with the standard library or shorten, and
changes nothing. Its findings go through *The findings*, and its cuts are one
commit, so the first round reads the shorter code. Its list does not end the
turn: go on to the first round. Skip it for documents only, and for a move
that a script or a test proves unchanged. When the skill is not
installed, skip it and say so in the summary.

## The walk

After the cuts of *Over-engineering first*, and before round 1, walk a
change that alters what a user sees or does on a screen: a component, a
page, a style, or logic whose result renders, as a store, a reducer or an
endpoint that a screen reads. Walk it once in a review, at any level. Skip
it for a backend that no screen reads, for documents only, for tests only,
and for a move that a script or a test proves unchanged.
`walk.md` gives the steps of the walk.

## The rounds

1. **Commit the work, and the docs it makes false.** Find those docs as
   *Docs move with the change* in the global prompt says, so that round 1
   reads them. The first round reads the whole branch:
   `/code-review <level> <base>..HEAD`, where `<base>` is
   `git merge-base origin/<default branch> HEAD`, or
   `git merge-base <default branch> HEAD` where there is no `origin`. Name the
   range: with no target, `/code-review` reads only the commits ahead of the
   upstream, and after a push that is not the whole branch. In Codex:
   `/review`, *Review against a base branch*.
2. **The fixes of a round are one commit.** The next round reads only that
   commit: `/code-review <level> <sha>^..<sha>`. In Codex: `/review`, *Review a
   commit*. Inside the loop, never send the whole branch again.
3. **Stop at the first round that confirms no defect**, whatever that round
   declines, for the first time or again. A round whose report says it read
   no file of its range confirms nothing and does not count. When its level
   skipped the files, run that range again one level up, in its place.
   Otherwise correct the range, and run it again. A defect is a confirmed
   finding of one of two kinds:
   - a wrong result, a crash or a broken contract, on an input or a state
     that the project's real use reaches;
   - data loss or a security hole, on any input.

   Both kinds hold in the code that a fix of this loop wrote too: most of
   the defects that later rounds find are there.
   In the text of a skill or a prompt, a defect is a rule that, followed as
   written, gives a wrong result in a case that real use reaches. When the
   only proof that a review subagent, `/code-review`, `/review` or Codex
   gives for a finding is its guess of what a model does in a case that the
   text does not name, the finding is a defect only when a run or a
   real session outside the review has already shown a wrong result there,
   or when the case is data loss or a security hole. Else decline it, as no
   defect and no nit, on the **Declined** line with "no failing run" as its
   reason, and make no run for it. Every other
   confirmed finding is a nit: a missing or redundant test, a comment, a
   name, wording, line wrapping. A nit starts no round. The nits of a round
   with a defect join its fix commit. The nits of a round with no defect are
   one commit, and no round reads it.
4. **The third round still confirms a defect:** stop the rounds, and skip
   what is left of step 5. Do not fix that defect: its fix needs a fourth
   round, and only the person can start one. The nits of round 3 are one
   commit, and no round reads it. When the change is at `xhigh`, in Claude
   Code, and the Codex step has not run in this review, Codex then reads the
   whole branch, as `codex.md` says. Then go to
   the security review, or to the summary when the security review has
   already run. The summary's **Rounds:** item names the findings of round 3
   and of a Codex read at this stop, each defect as confirmed and not fixed:
   these are the defects that step 4 leaves open. The merge
   question in *The pull request* of `summary.md` then has one more answer.
   When the person asks for more rounds, up to three more run, and this step
   stops them at the third.
5. **The last pass reads the whole branch once**, as in step 1, at the same
   level, when the loop had more than one round. A round on one commit cannot
   see how a fix fits the rest of the branch; this pass can. It waits for the
   answers to open questions, unless nobody can answer. There is never a
   second whole-branch pass: the rounds that reread the whole branch are the
   ones that did not stop.

### A review of the architecture

This step needs an architecture file or an ADR folder on the branch, where
`craft:architecture` finds them: `docs/ARCHITECTURE.md` or
`ARCHITECTURE.md` at the root, and `docs/adr/`, `doc/adr/` or
`docs/decisions/`. Then one review subagent reads the range of round 1 once,
beside round 1: at `high` or `xhigh`, and for any change whose range touches
the architecture file or an ADR, also a change to documents only.
When the text of a skill or a prompt comes with code, use the level of the
code alone. Skip it for a move that a script or a test proves unchanged,
unless the range touches the architecture file or an ADR.
`architecture-and-tests.md` gives the subagent, its prompt and the rest of
the step.

With no architecture file and no ADR folder, the step does not run. Then the
summary says once per pull request that `craft:architecture` can
write the first file, unless the project's `CLAUDE.md` says "This project
keeps no `docs/ARCHITECTURE.md`."

### Fixes from other places

Each of these starts a new count of rounds: the last pass, the Codex review,
the review of the tests, the security review, and each set of a person's
review comments, before or after the pull request opens. The Codex review
at a step 4 stop starts no count of rounds, as `codex.md` says. When more
than one of the last pass, the Codex review and the
review of the tests find defects, their fixes are one commit. A count of
rounds here does not start the Codex review or the review of the tests
again. For each of them:

- Its fixes are one commit. When they fix a defect, as step 3 says, that
  commit goes through steps 2 to 4. A commit of nits only gets no round.
- Its rounds run at the level that the loop's round 1 used. In a new session,
  take that level from the pull request's `## Review`. A fix to security code
  runs at `xhigh`, whatever found it.

The fix for an answer to a question joins the next fix commit. When no rounds
are running, it starts a new count, as above. A person's review comments go
through *The findings* below, and the reply names the fix commit.

A change to documents only has no such rounds, unless the person asks for
more: see `documents.md`.

## The findings

1. **Verify each finding before acting on it.** Reproduce it against the real
   code or in a browser. Reviewers report findings that are wrong, stale, or
   right for the wrong reason, and a confident wrong fix is worse than the
   defect. A finding that does not survive is declined, with the reason.

   A finding that fails only on a particular input or state needs a count
   too: how many of a sample of the real source carry that shape, as *The
   input comes from the source, not from your head* in the global prompt
   says. A count of zero declines the finding in the same round. Give the
   count as its reason on the summary's **Declined** line, so that
   `## Review` carries it to later reviews and sessions. A zero
   count does not decline a finding of data loss or a security hole: an
   attacker can make the input, and the test of its fix uses the input of
   the finding. With no real source to sample, the count declines nothing,
   and the test of the fix uses the input of the finding.
2. **Fix every obvious one now, without asking:** real bugs, dead code,
   accessibility and contrast failures, code that contradicts its own
   documentation, wrong numbers in documents.
3. **Decide every other one yourself:** a trade-off, a name, a structure, the
   look of a screen. Take the choice that fits the code around it, and write
   down the reason for the summary.
4. **Ask only about a change to business logic:** what the product does for
   its users — a rule, a calculation, a state, a permission, the data it keeps
   or deletes. Give the options and a recommendation, and keep the rest of the
   round going while the person answers. When nobody can answer, as in a run
   with no person, the question stays open in the summary. A finding that
   shows that the capability gives its users nothing, as a policy that blocks
   every result the feature finds, is such a question, not a defect to fix:
   do not rebuild the feature. Run `craft:product` at the light depth,
   with the finding as its new proof, and ask with its options.
5. **Fix at the root.** When the same defect is in sibling call sites or in a
   shared token, fix it there, and count the places.
6. **A finding outside the task goes by `craft:github`**, not by steps
   2 to 4: an issue, unless the Boy Scout Rule or the person's choice
   takes it in, or that skill gives it no issue.

## The security review

After the last pass, the Codex review, the review of the tests and their
rounds, `/security-review` runs once, on the final branch. It reads the branch
against origin's default branch and takes no target, so it never runs inside
the loop. A change to documents only gets none, unless the person asks for
it. Its findings go through *The findings*, and its fixes through
*Fixes from other places*. In Codex: `/review` with the custom instructions
"Find security defects on this branch against origin/<default branch>:
injection, authentication, authorization, secrets and data exposure." Where
there is no `origin` remote, say so in the summary.

In Claude Code, send one `general-purpose` subagent with no `model`, with
this prompt, and do not run `/security-review` in the session:

```
Run /security-review with the Skill tool, and return its report. Change no file.
```

After its report and the rounds on its findings, read `summary.md` and go on
to *The summary*, then to the conditions of *The pull request*.

Why a subagent: the prompt of `/security-review` ends "Your final reply must
contain the markdown report and nothing else." Run in the session, the agent
ended its turn on the report, with no push and no pull request: on #61, and
twice on #167, after #83 added a sentence against it here. In a subagent, that
line holds for the subagent's reply.

