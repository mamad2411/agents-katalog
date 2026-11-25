---
name: tw-learn
description: "Study an external target - an article, a repository, a file, a design doc or a block of code - comprehensively and systematically, compare how it does things against how this team does them, and adopt the mechanism rather than the expression. Use when asked to 'learn from this repo/article/code', 'study how X does it', 'compare us against Y', 'what should we adopt from Z', or to bring an outside idea into the system without copying it."
---

# tw-learn - study an outside system, adopt its mechanism

Owner: CEO. This is the learning procedure: how the team reads something built by
someone else, decides what is genuinely better, and integrates the idea into its
own system without copying a line of it.

Related, read alongside: the tw skill's own `SKILL.md`, and its
`references/Roles.md`, `references/Evidence.md` and `references/Testing.md`.

Those four documents sit in the **teamwork skill's directory** - at the repository
root when you read this file from the checkout, and beside this skill when it is
installed. They are named rather than linked, and the names carry no path at all:
this file ships at two different depths, so a relative link that resolves in one
layout is dead in the other, and a path spelled for one layout is wrong in the
other. A name that makes no location claim cannot be wrong in either.

## 1. The two hard rules

**No copying.** A target is *material under inspection*, never a source to paste.
You study the mechanism, write your own expression, and prove the difference. A
pasted block is a licence defect, a maintenance defect and a review fail at once.

**Evidence or `UNVERIFIED`.** Every claim about the target carries a direct URL, a
revision or a `path:line`, and an access date. A claim you cannot point at is not
a finding, and a comparison built on one is fiction.

The rest of this skill is the procedure that keeps those two rules true.

## 2. When to use it, and when not

| Use it when | Do not use it when |
|---|---|
| a repo, article or design describes a mechanism we lack | the target is our own code (that is `tw-self-evolve`) |
| a review finding says "their approach is better" | the target is a library we can simply depend on |
| a new prompt cites an external system to learn from | the question is a fact lookup (`knowledge search` first) |
| a competitor's feature is named as the bar | the work is a straight port of a specification we must follow |

A **dependency** is not learning. If `pip install` solves it, that is a vendor
decision for the CTO and the CFO, not this procedure.

## 3. Step 0 - name one target and one question

One target, one question, one deliverable. "Study their whole repo" is not a unit;
"how do they decide when a build is allowed to fail?" is.

Record it as a task so the work is on the board and has an owner:

```sh
tw task add developer "Study <target> for <one question>" --priority P2 \
    --body "target: <URL|repo@sha|path@sha>  question: <one sentence>"
```

A target with no question produces a book report. A question with no target
produces an opinion.

## 4. Step 1 - capture the target so the finding survives it

A URL rots and a branch moves. Pin what you read, before you read it:

| Target | What you record |
|---|---|
| article | the direct URL, the title, the author, the access date |
| repository | `url@<full-sha>` (never a branch name), the access date, the licence file |
| one file | `url@<sha>#path:line` or a local `path@<sha>:line` |
| a block of code | the same, plus the licence header it carries |

Record the licence **before** you study the code, not after you want to use it.
A licence that forbids reuse does not forbid reading: it forbids the expression.
The mechanism is still fair game; the words are not.

```sh
tw knowledge add --by ceo --topic "learn:<target>" \
    --statement "read <target>@<sha> for <question>" \
    --evidence "<direct URL> - accessed YYYY-MM-DD" --tags learn,<area> --importance 2
```

## 5. Step 2 - research in rounds, five probes each

One round is five probes, run in parallel, each recorded with what it found and
where it found it. A second round is required when the first leaves a term
contested, a mechanism unread, or a claim you cannot point at.

| Probe | The question it answers | The failure it prevents |
|---|---|---|
| **what** | what does it actually do, in one sentence, with no adjectives? | admiring a description instead of a mechanism |
| **how** | which part of the tree or text implements it, at `path:line`? | describing a README as if it were behaviour |
| **why** | what did it trade away to get this - cost, latency, complexity, a gate? | adopting a benefit whose price you did not see |
| **context** | what is true of *their* system that is not true of ours? | transplanting a solution to a problem we do not have |
| **misreading** | what is the plausible wrong lesson, and what would show it is wrong? | cargo-culting the visible half |

Record each round, and name the files you read so the next reader does not repeat
the crawl:

```sh
tw knowledge add --by <role> --topic "learn:<target>:how" \
    --statement "<the mechanism, in one sentence>" \
    --evidence "<url>@<sha>#<path>:<line> - accessed YYYY-MM-DD" --tags learn --importance 3
```

Use the sparse reader, never a whole-file crawl: `tw read <path> --query '<needle>'`.
A repository is read by the file that answers the question, not by cloning it.

## 6. Step 3 - extract the mechanism, not the feature

The feature is what they built. The mechanism is the invariant that makes it work.
Only the mechanism transfers.

Write it in this shape, and refuse to move on until each line is filled:

```text
invariant   : <the rule that must hold for their approach to work>
mechanism   : <the smallest moving part that enforces it>
precondition: <what must be true of the host system>
price       : <what it costs, measured or named>
falsifier   : <the observation that would show the mechanism is not the cause>
```

"Their CI is fast" is a feature. "They scope the job set to the change set, and
fail closed when the change set cannot be measured" is a mechanism - and it
transfers to any repository, including one that has never seen their code.

## 7. Step 4 - the comparison, on one axis at a time

Compare on the same axis, in the same units. A table with a row per axis and a
verdict per row; a row you cannot fill is a row you have not researched.

| Axis | Theirs | Ours | Gap | Verdict |
|---|---|---|---|---|
| <the invariant> | <what they do, cited> | <what we do, `path:line`> | real / none | adopt / adapt / improve / reject |

The four verdicts mean exactly this:

| Verdict | It means | It forbids |
|---|---|---|
| **adopt** | our system lacks the invariant and their mechanism fits our preconditions | claiming it fits without naming our precondition |
| **adapt** | the invariant is right, the mechanism does not fit our host | porting their shape because it looks familiar |
| **improve** | we have it, theirs is measurably better on one axis | "better" with no number |
| **reject** | the price is higher than the benefit here, or the precondition is false | a rejection with no reason recorded |

**A reject is a result.** Record it, with the reason, so the next agent does not
re-run the study. An unrecorded rejection is a study the team pays for twice.

## 8. Step 5 - decide, with evidence and a falsifier

Every non-trivial adoption is a decision record. The four fields are not optional:

```sh
tw decision add --by ceo --kind technical \
    --decision "adopt <mechanism> from <target>@<sha>: <one sentence>" \
    --why "<from the comparison: which axis, which measurement, which precondition>" \
    --evidence "<cmd @rev -> result | url@sha#path:line - accessed YYYY-MM-DD>" \
    --falsify "<the measurement that would show this was the wrong adoption>"
```

Then ask the one question that kills most adoptions: **what does this replace?**
An adopted mechanism that adds a second way to do the same thing is a defect, not
an improvement. Name the thing it retires, or do not adopt it.

## 9. Step 6 - integrate as our own, not as theirs

The deliverable is our code, our names, our tests, our docs. Nothing about the
target survives into the tree except the idea and the citation.

| Rule | Why |
|---|---|
| write it from the mechanism, never from their source | a paste is a licence defect and a comprehension debt |
| no borrowed identifier, comment or comment-block | a copied comment is the clearest evidence of a copied block |
| our naming, our structure, our error messages | a transplanted shape reads as foreign for years |
| a test that fails without the mechanism | an adoption with no failing-before test is unproven |
| the citation in the commit `Why`, with the access date | the trail must show where the idea came from |
| a line in `docs/Team/Decisions.md` by id | the next agent finds the reason without re-reading the study |

The integration is ordinary teamwork from here: a task, a branch, a self-check, an
independent review, the archive. `tw-brief-intake` if the adoption is large enough
to need a brief.

```sh
tw task add <role> "Integrate <mechanism>: <the invariant it enforces>" --priority P1 \
    --body "source: <target>@<sha>  decision: D-<id>  replaces: <what it retires>"
```

## 10. Step 7 - prove it moved, or say it did not

An adoption claim needs a contrast and a verdict. Name what was compared, on which
task and revision, and label it:

| Label | It means |
|---|---|
| `helped` | the metric moved, on the named comparison |
| `hurt` | it moved the wrong way; revert and record why |
| `no observed effect` | measured, unchanged - keep it only if it removes something |
| `confounded` | more than one variable changed; re-measure, never relabel |

```sh
tw tests run <TS-id> --by <role> --result pass --rev <sha> \
    --baseline "<the state before>" \
    --evidence "<cmd> @<sha> -> <result>  (before: <cmd> @<sha> -> <result>)" \
    --replay "<the command another agent reruns>"
```

`no observed effect` is a real, publishable outcome. A mechanism that changes
nothing and removes nothing is code the team now maintains for free.

## 11. Step 8 - record, and retire what it replaced

- `knowledge add` the durable fact: the mechanism, its precondition, its price.
- `decision add` the adoption, with the falsifier (step 5).
- The archive entry comes from the review pass, as for any deliverable.
- Retire the thing it replaces **in the same task**: a superseded path, a dead
  flag, a second way to do the same thing. An adoption that leaves both is a
  regression with a citation.
- If the study produced a repeatable flow, `skill create --kind workflow` it, so
  the next target costs a skill run instead of a re-crawl.

## 12. Pitfalls - the six ways this goes wrong

| Pitfall | What it looks like | The guard |
|---|---|---|
| **cargo cult** | the visible half is copied, the invariant is not | step 3: fill all five lines, including the falsifier |
| **licence contamination** | their code, our tree | step 1 records the licence before the study; step 9 forbids the paste |
| **novelty bias** | "they are newer, so they are better" | step 4: one axis, one unit, one number |
| **precondition blindness** | it works there, so it works here | step 5: name the precondition and test it here |
| **duplicate path** | both systems now exist | step 5: "what does this replace?" |
| **book report** | a long summary, no verdict | step 7: a label, a contrast, a revision |

The one-line test for the whole procedure: **can you state the invariant without
naming the target?** If you cannot, you studied the artifact and not the mechanism,
and nothing here is ready to adopt.

## 13. Verification

```sh
tw knowledge search "learn:<target>"          # the study is findable
tw decision list --kind technical             # the adoption has a record and a falsifier
tw task list ceo                              # the integration has an owner and a branch
tw tests plan                                 # the layer that proves it is recorded
tw trace <T-id>                               # the chain runs end to end
tw audit                                      # no provenance gap, no orphan
```

A finished study has: a pinned target with an access date, at least one research
round recorded, a comparison table with a verdict per axis, a decision with a
falsifier, an integration task that names what it replaces, and a measurement
labelled `helped`, `hurt`, `no observed effect` or `confounded`.

Anything less is a summary, and a summary is not a deliverable.
