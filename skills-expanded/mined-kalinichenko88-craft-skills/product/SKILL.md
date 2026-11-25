---
name: product
description: Use when a feature starts (a new capability, or a change of what the product does for its users), when a bug fix changes business logic, when a branch or pull request is reviewed (someone else's that changes code or behaviour, or one's own that adds a capability or changes what the product does, with no report of its worth), when brainstorming asks a question that chooses between ways, when a decision concerns the whole project (the licence, open source or not, distribution, pricing, the money model, the hosting), when a task may be deferred or closed for its worth, or when PRODUCT.md or a PDR is written or checked.
---

# Product

A task is worth its cost, or it is not. This skill asks that before the work,
from outside the code: who gains and how many, the money, the direction of
the project, the law, the client, and what fails when a part fails. Another
way, a deferral or a close is a good answer. The person decides.
`craft:architecture` decides how the code does it; this skill decides
whether to build it, and what.

| Moment | Depth | Read first |
| --- | --- | --- |
| A feature starts: a new capability, or a change of what the product does for its users | full; none when a report for it exists (*The trace*) | *The run* |
| A bug fix that changes business logic: a rule, a calculation, a state, a permission, the data | light | *The run* |
| A review of someone else's branch or pull request that changes code or behaviour | full, always | *The trace* |
| A review of one's own branch that adds a capability or changes what the product does | none when a report for it exists; else the depth of its start | *The trace* |
| A review finding that shows the capability gives its users nothing | light, with the finding as its proof, also when a report exists | *The run* |
| A question in brainstorming that chooses between ways | light; full for a decision about the whole project | *In brainstorming* |
| A decision about the whole project: the licence, open source or not, distribution, pricing, the money model, the hosting | full | *The run* |
| A project with no store, or the person asks for one | the offer | `store.md` |

One's own bug fix that changes no business logic gets no run, nor does someone
else's change of documents only, a dependency bump or a move that a script or
a test proves unchanged. The text of a skill or a prompt that the product
ships or sends to a model, as a `SKILL.md`, is no document here: it changes
behaviour. `reader.md` and `store.md` sit next to this file, in this skill's
base directory `<dir>`. Read `reader.md` before the first run: it holds the
criteria, the checks and the shape of the report, for the readers of the panel
and for the light depth. Read `store.md` before the first read or write of the
store.

**Light.** The main session alone, with no web search. It reads the index of
`PRODUCT.md` and the PDRs that the task touches. The report has the verdict
and its reason, and another field only when it has content.

**Full.** The panel (*The panel*): two readers in parallel, each with a web
search, and neither sees the other's answer. The main session merges them.

## The trace

The person's own work gets no second report: a report exists when a message of
this session about this work, the spec of the work, the pull request's
description or the issue holds a `**Verdict:**` line, or when the branch adds
a PDR for this work. The report of a fork in brainstorming is no report of the
feature. The test is the trace, not the author: the person's branch with no
report at its start gets one at the review.

Someone else's work that changes code or behaviour gets the full depth
always, with a report or without one, and their spec and description are the
decisions to check. Someone
else's work is a pull request whose author is not the account that `gh` is
logged in as, or, with no pull request, a branch whose commits have another
author's email than `git config user.email`.

A report with no spec, or at a review of one's own branch, goes into the pull
request's description, or into it when it opens, so that the next review
finds it. On someone else's pull request, it goes in a comment through
`craft:github`, after the person's yes.

## In brainstorming

Besides the start of a feature, whose report comes where *The start of a
feature* of `craft:architecture` says, the skill runs only at a fork: a
question that chooses between ways, as "fetch it on each request, or download
it once". Never at a question that asks the person to describe.

At a fork, the report comes in the message that asks the question, before
its options, and its options become the options of the question. It may show
that the conversation went the wrong way: say so plainly, with the proof.
The answer stays the person's.

## The run

1. **Find the store** (`store.md`), and the PDRs that its index shows the
   task touches. With no store, go on without one, and make the offer of
   `store.md` once a session; in brainstorming, after the person answers the
   fork. At the full depth, send the panel now (*The panel*), and wait for
   its readers before step 7.
2. **Understand the task:** who has the problem, how many of them by real
   data, and how others solve it. At the full depth, with a web search.
3. **Collect the three sides:** the client (what they ask, and the goal
   behind it), the law (the rules that apply, with the primary source), and
   the project (its direction in `PRODUCT.md`, its milestone, the decisions
   that the task touches).
4. **Show the conflicts** between the three sides. Do not smooth them.
5. **The criteria and the checks** of `reader.md`.
6. **Each accepted decision that the task touches** (*Accepted decisions*).
7. **The report** (`reader.md`), then the person's decision (*The person
   decides*), then the store.

The report goes in a message before the work that it judges: with a spec, at
the spec's start, after the block of *The start of a feature*; at a review,
before round 1, and then where *The trace* says.

## Accepted decisions

An accepted decision is a hypothesis that won once. When the task touches
one, check three things:

- Does its *Rests on* still hold? At the full depth, search for a change: a
  new law, a new price, a new limit.
- Did its *Revisit when* condition come?
- Did it get in the way: does the task have to go around it? Then a line goes
  into its *Got in the way* after the person decides. With two lines there,
  propose to revisit it.

The report names the decision in **Touches decisions:**, with what changed.
Only the person changes its status.

## The person decides

The skill never refuses or cancels the work. A verdict other than `do it` is
a question to the person, and the work that it judges waits for the answer.

With no person, as in a run that a script starts or with "do not ask
questions", the work goes on as it was asked. Then the last message of the
turn starts with the report, its `**Verdict:**` line first, and its
questions marked `open`. The report then goes where *The trace* says; on
someone else's pull request, with no yes, it stays in that message.

After the answer:

- The decision goes into the store, by `store.md`: a new PDR, or a line in
  *Got in the way* or *Checked* of an existing one.
- `defer until <condition>`: after a yes, the issue goes to Later with
  `plan.sh later` of `craft:roadmap`, and the condition goes into the
  issue's text.
- `close`: after a yes, the issue closes as not planned through
  `craft:github` (`gh issue close <n> --reason "not planned"`), with
  the report in its comment.

## The panel

Send both readers in one message, in the background:

- **Fable:** an `Agent` call with `subagent_type: "general-purpose"` and
  `model: "fable"`.
- **Codex,** from the working tree of the task. Write the prompt to a new
  file with the Write tool, in the session's scratchpad directory, or in a
  new folder from `mktemp -d` when there is none, with this last line: "You
  are one reviewer that another agent runs: start no skill, change no file,
  and file nothing." The prompt never goes into a shell
  command: the brief holds text from outside, and that text can hold a
  line that ends it.

  ```bash
  bash <dir>/../review-loop/scripts/time-limit.sh 1200 codex --search exec -s read-only --ephemeral - < <file>
  ```

  `--search` goes before `exec`.

The prompt of each is the text of `<dir>/reader.md`, then the brief:

- the task: the issue, the spec or the pull request, with its text; at a
  review, also the branch and its range `<base>..HEAD`;
- the store: `PRODUCT.md`, or the project's own decisions file, or "no
  store";
- the decisions that the task touches;
- the **Touches:** line of the block of *The start of a feature*, when there
  is one;
- for someone else's work, their spec and description, as the decisions to
  check.

Not the conversation: a reader that sees it argues from it.

**The merge**, in the main session. Join the points that say the same thing,
and drop none, except a risk with no number and no source. A point that goes
against what the conversation agreed goes to the person as it is: the main
session sees the task through the conversation, and this rule guards against
that. Where the readers disagree, the **Readers disagree:** line says so, with
each reader's side.

**Fallbacks.** With no `codex` command, when `codex login status` fails, or
when the run fails: Fable alone, and the report says so. When the Fable call
fails: Codex alone; with neither reader, the main session alone, with its
own web search. The report says so. When Codex returns
no source URL, it had no search: the report says that its points rest on no
web search. Codex as the host has no subagent with a model and does not call
itself: the main session does the full depth alone, with its own web search,
and the report says so.

## Other skills

- `craft:architecture` sends here at the start of a feature. Its block
  keeps **Problem:** and **Touches:**; this skill's report answers whether
  the problem needs solving and the simplest way. When a PDR changes, the
  ADRs that name it go to the architect (`store.md`).
- `craft:review-loop` sends here before round 1 (*Worth first*), and
  at a finding that shows that the capability gives nothing.
- `craft:github` closes an issue, and `craft:roadmap` puts one
  off to Later.

## Red flags

| Thought | Reality |
| --- | --- |
| "The person asked for it, so it is worth doing" | A request names a solution. Count who gains first, from the real data. |
| "The benefit is small, but the task is clear, so I build it" | A small benefit is the finding. Give the count and the cheaper way, and ask. |
| "The architect checked the task" | The architect checks where the code goes, not whether to build it. |
| "I can check it myself; the panel is too much here" | The table sets the depth. A feature start is full: send both readers, and wait for them. |
| "I will widen a limit to make it work: a CSP, a quota, a permission" | A limit that blocks the feature is a decision of the product. It goes in the report, and the person decides. |
| "A general risk is better than none" | A risk with no number and no source for this task is noise. Leave it out. |
| "The decision is accepted, so it is settled" | An accepted decision is a hypothesis that won once. Check its *Rests on*. |
| "The verdict is close, so I stop the task" | The person decides. Ask, and wait for the answer. |
| "No one can answer, so the report can wait" | The last message of the turn starts with the report, and *The trace* says where else it goes. |
