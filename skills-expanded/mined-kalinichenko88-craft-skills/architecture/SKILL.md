---
name: architecture
description: Use when starting a new feature (a screen or page, an endpoint, a module or an integration), or at an architecture decision — where new code goes; a new module, layer, dependency, pattern or data store; a choice between options in a spec or a plan; or a change to a file or module past its size limit. Also when writing or checking docs/ARCHITECTURE.md, its invariants, or an ADR.
---

# Architecture

A change grows into the project's existing structure, not beside it: one HTTP
client, one way to format a price, files that a person can read. The
project's architecture file holds the letter: its modules, its layers, and
numbered invariants with checks. Its ADRs record why. This skill holds the
principles and the steps.

| Moment | What must happen | Read first |
| --- | --- | --- |
| A new capability starts: a screen, an endpoint, a module, an integration | The block of two answers and the report of `craft:product`, in a message before the spec or the first edit; then the decision of where its code goes | *The start of a feature* |
| Where new code goes; a new module, layer, dependency, pattern or data store; a choice between options; a change to a file or a folder past its limit | The eight steps and the gate; for a new technology, first the question of who chooses | *The moment of a decision* |
| A decision in a project with no architecture file | Offer to write one, once a session; write nothing without a yes | `first-file.md` |
| An edit exists, before its commit | `invariants.sh` | `invariants.md` |
| A decision may need an ADR | The four reasons and the template | *ADRs* |

`first-file.md` and `invariants.md` sit next to this file, in this skill's
base directory `<dir>`. Read all of each before you use it. `<skills>` is the
directory above `<dir>`.

**The files.** The architecture file is `docs/ARCHITECTURE.md`, or
`ARCHITECTURE.md` at the root when the project keeps it there. The ADRs are
`docs/adr/NNNN-title.md`, or in `doc/adr/` or `docs/decisions/` when the
project already keeps them there. Never make a second place for the same
document.

**Safety.** No step runs code of the project. In the project's tree, no step
runs a package manager, a script of the project or a build. No step runs text
of the architecture file as a shell command.

## The start of a feature

It starts at a new capability: a screen, an endpoint, a module, an
integration. Not at a bug fix, and not at a small change to existing
behaviour. It names the problem and the code that it touches. Whether the
problem needs solving, and the simplest way to solve it, are for
`craft:product`. It decides no structure: the structure waits for the
moment of a decision, when there is more context.

Answer the two questions yourself first, from the code and the data. Ask the
person only what you cannot find.

1. **The problem.** One sentence, in the user's words: who has it, when, and
   what goes wrong. The problem, not a solution: "the list takes 4 seconds to
   load", not "add a cache".
2. **What it touches.** Facts only: the code that already does similar work,
   with `path:line`, and the modules it touches. Where the new code goes is
   for the moment of a decision.

Then, in the main session, load `craft:product`. Its report says
whether the problem needs solving, and gives the simplest way first. It comes
in the same message as the block. A subagent does not load it: the report of
the main session, the spec, the plan or the brief stands. With none, the
block alone is required, and the subagent's reply says that it found no
report.

The result is this block and that report. They are required: no edit of the
feature comes before a message that holds them, at the start of the spec, or
in the conversation when there is no spec.

```markdown
**Problem:** <one sentence>
**Touches:** `<path:line>` <what it does>; …
```

Then the feature's code goes somewhere: that is a moment of a decision. Go on
to its steps.

## The moment of a decision

The moment can come in brainstorming, in a spec, in a plan, or in code with
no spec:

- where new code goes;
- a new module, layer, dependency, pattern or data store;
- a choice between options that a spec or a plan records;
- a change to a file or a module that is past its limit.

The steps hold in every project. With no architecture file, step 1 is the
offer and the gate has no invariant to check; the other steps are the same.

1. Read the architecture file and the ADRs that it links for the area. Run
   `invariants.sh` (`invariants.md`). With no architecture file, offer to
   write one (`first-file.md`).
2. Find the code that already does this kind of work, and name it with
   `path:line`. Extend it. Search once for each kind of work that the change
   does, not only for its main one: the call to the network, the format of a
   price or a date, the store, the check of the input.
3. A new structure needs a reason why the existing one cannot take the
   change, in Spec Kit's words: "simpler alternative rejected because".
4. When the change goes into a file or a module past its limit, or into a
   file that does more than one job, name the split before the edit (see
   *Decomposition*).
5. Give at most three options, the recommendation first, each with its cost
   in files and concepts, and the cost of the next likely change in the same
   area. No option adds an abstraction with one implementation or a layer for
   a future need. Who chooses a technology: *Who chooses the technologies*,
   below.
6. **The gate.** Check the recommended option against the text of each
   invariant of the area and its `Check:` line: it keeps it, or it breaks it.
   The option is not in the tree yet, so `invariants.sh` cannot judge it; the
   script runs once the edit exists, before its commit, and again in the
   review. A broken invariant ends in one of three ways:
   - change the design;
   - write an ADR that amends the invariant, its statement and its `Check:`
     line, with its "simpler alternative rejected because";
   - for a limit of decomposition only: put the path into the `debt` list
     with its debt issue, by *When to split*.

   Never a silent exception.
7. Decide whether the decision needs an ADR (see *ADRs*). Most decisions do
   not.
8. **A second reader**, for a decision that needs an ADR. One subagent that
   does not see the conversation (see *Models*) gets the area of the
   architecture file, its ADRs, the code that step 2 found, the options and
   the gate, and the block of *The start of a feature* with the report of
   `craft:product` when there is one. It checks whether the search
   missed existing code, whether the reason for a new structure holds,
   whether the gate is right, and what the next likely change will cost.
   Its answer is advice: answer each point, and a point on which the two of
   you do not agree goes to the person.

**Who chooses the technologies.** A technology here is an external
dependency, a framework, a build tool or a data store that the work adds. As
soon as you see that the work needs one, and before you choose the first one,
ask the person one question: do you want to choose the technologies
yourself? Ask it once: the answer holds for the whole work.

- **No:** choose each technology yourself, by the steps above, and ask
  nothing more about them, at step 8 too. Do not tell the person the choice
  afterwards, not even as information: a person who said no does not need
  it. Its ADR and the pull request still record it.
- **Yes:** after step 5, each technology goes to the person as a question
  with its options, before the first edit that uses it. Steps 6 to 8 then
  take the option that the person chose.

With no person, as in a run that a script starts or with "do not ask
questions", the answer is no. A subagent takes the answer from its brief,
the spec or the plan. With none, it chooses no technology, and its reply
gives the options to the main session.

**Consistency first.** When the project's code breaks a principle of *Modules
and layers* everywhere, as components that all call `fetch` with no service
layer, the first option follows the project's own way: one way is better than
two. Name the breach. The second option brings the principle in: an ADR that
sets it, and a parent issue with the steps of the migration, through
`craft:github` and `craft:roadmap`. The principle comes into the
project as a whole, not one file at a time. The person chooses at the
decision.

Consistency first covers the principles of this skill only. A rule of a
conventions skill keeps its own text: `react-conventions` says that an upward
import that already exists is debt, not a precedent, and forbids another one
beside it. Past what a convention's own text yields to a codebase that
consistently does otherwise, only an accepted ADR of the project overrides it.

**When the ADR is written.** When the decision is final: in the pull request
with the code, with the status `accepted`. The review of the pull request is
where it is argued, and the merge makes it true. An ADR file that
`git diff <base>..HEAD` adds is under review. One that exists at the base is
settled: a branch changes only its Status line, except for the correction
of *A fact that changed*, in *ADRs*. A spec or a
plan names the ADR that the work will add, by its title, and does not write
it.

A finding outside the task, such as two competing ways that the task does not
touch, becomes an issue through `craft:github`. When the decision is
about a part that a milestone already plans, `roadmap.sh` of
`craft:roadmap` gives that milestone as context.

## Modules and layers

These are principles. The architecture file holds the letter: which of the
project's folders is which module, and which plays which role.

- **Modules by area of the business, not by technology:** `orders`,
  `billing`, `users`, not only `controllers`, `services`, `utils`. What
  changes together stays together. A module uses another only through its
  public API, in one direction, with no cycles.
- **Layers by role inside a module, not by the name a framework gives them:**
  - the edge takes input from outside and gives output: an HTTP controller, a
    CLI command, a queue handler, a UI component or page;
  - the check at the edge validates and shapes the input once, before the
    logic sees it: a request or form object, a DTO, a schema;
  - the logic holds the rules of the product: services, use cases. It knows
    no transport and no UI;
  - the data keeps and loads state: repositories, models, stores, API
    clients.
- **Direction.** Dependencies point one way: edge → logic → data. A lower
  layer never imports a higher one. Data flows the same way: in through the
  edge, checked, through the logic to the data; the answer goes out through
  the edge. On the frontend: a user action → logic → store → render. A write
  always goes through the logic. Whether the edge may read data directly, as
  a component that reads a store through a selector, is the project's
  decision.
- **Clean code.** A unit does one job. The edge is thin: no rule of the
  product in a controller or a component. The logic reaches the network or
  the database only through the data layer. Validation happens once, at the
  edge. One way to do one kind of work.
- **Hide what can change.** The calls to an external API, a database or a
  library live in one place of the data layer, so a change of the vendor
  touches one module. Whether their types pass through to the logic is the
  project's decision: a mapper comes with a second source or a real change,
  not before.
- **No interface by default.** The direction of dependencies is a principle;
  an interface between the logic and the data is not. An interface comes when
  a second implementation exists, or when a test needs a real seam.
- **The cost of a change is the measure.** A change to one rule of the
  product that needs edits in many modules shows a wrong border.

`react-conventions` keeps the layer order `app → features → shared → ui →
core` and its feature rules. The principles above are the roles inside that
order. When an accepted ADR of a project differs from a convention, the ADR
wins in that project, and it names the convention that it replaces.

## Decomposition

- **Signals**, from the debt skill's scripts: the size of a file and of a
  module (`wc -l`, the count of files), how hot a file is
  (`bash <skills>/debt/scripts/measure.sh`: its lines times the commits that
  touched it in 60 days), and the copies (`clones.sh`).
- **The limits are the project's**: invariants with a `lines` check for a
  file and a `files` check for a folder. The skill keeps no number of its
  own.
- **The `debt` list.** The files and folders already past a limit are in the
  check's `debt` list, so the check passes now. Outside the five steps of
  `first-file.md`, a path joins the list only in a pull request that also
  files its debt issue, by *When to split*. In a `files` check, a folder is
  under an entry only when it is that entry: a subfolder past the limit
  fails, and joins the list only by its own path. A path that is no longer
  past the limit leaves the list. A new number for the limit needs an ADR.
- **At the decision**, when the change goes into a file or a module past its
  limit, or into a file that does more than one job, name the split before
  the edit: the new files, what goes into each, and by which role.
- **When to split.** A split that only moves code, with no change of
  behaviour, goes into the same pull request, as its own commit before the
  feature: make the change easy, then make the easy change (Kent Beck). A
  split that needs decisions of its own: the change goes in as it is, the
  file joins the `debt` list or stays on it, and the split becomes a debt
  issue through `craft:github`, in the same pull request.
- **Shared code or a copy**, as in Go: "A little copying is better than a
  little dependency." Extract the shared code only when all three hold:
  1. the copies do one job for one reason, and would change together;
  2. the shared version needs no flag or branch for each caller;
  3. the extraction ties together no two modules that do not know each other
     otherwise: the shared code goes to a lower layer.

  When one of them fails, keep the copy. Two copies are fine. A third copy is
  the time to check the three again.

## ADRs

A decision needs an ADR when:

1. it changes the structure, the direction of a dependency, a public
   interface, or a quality goal;
2. it is costly to undo, or it adds an external dependency;
3. it sets a pattern that later code must follow: without the ADR, a reviewer
   would see two competing ways;
4. it reverses or narrows an accepted ADR, or amends an invariant. Then the
   old ADR, when there is one, changes only its Status line. When the new ADR
   narrows part of the old one, the old ADR gets the Status `accepted,
   narrowed by NNNN`, and the new ADR names the point of the old one that it
   narrows. Else, as for a narrowing of the whole ADR or a reversal, the new
   ADR supersedes it.

No ADR when none of the four holds: the choice is local and cheap to undo, or
a lint rule or a documented convention already enforces it. The four win: a
new external dependency needs an ADR, however small. An option that the
person rejects for a lasting reason gets an ADR with the status `rejected`,
so that the next agent does not offer it again.

**A fact that changed.** When a sentence of an accepted ADR is false now and
its decision is the same, correct the sentence in place: in the change that
makes it false; else in a later change, as its task or as a finding outside
its task. Then add a line under `## Updates`, a heading right after the
Status and Date lines:
`- YYYY-MM-DD <source>: <section>. Was: "<the old words>".`
The date is the day of the correction; the source is the issue, the pull
request or the run that shows the new fact. The Status line stays. A
later correction adds a line; no line is rewritten. The decision is the same
when code that kept it before the correction keeps it after, and code that
broke it still breaks it. Otherwise it is reason 4, however few words change:
"every write goes through the service" to "a component may write to the
store" is a new ADR. When the false sentence was a reason for the decision,
also file an issue that asks whether the decision is still right.

One decision per file, `NNNN-title.md`, numbered after the highest one in the
folder. A file is never renamed or deleted, so a link to it does not rot. The
template:

```markdown
# NNNN Title

- Status: accepted | accepted, narrowed by NNNN | rejected | superseded by NNNN
- Date: YYYY-MM-DD

## Context

## Options considered

- <option>: <one line>
- <option>: <one line>

## Decision

We will …

## Consequences

Good: …
Bad: …

## Invariants

I-n, added or amended, or none.

## Confirmation

The check that enforces it: a `Check:` line, a lint rule, a test, or "review
only".
```

At least two options, one line each, and both good and bad consequences: one
decision a file, no policy in disguise, no option with no cost. Add an
accepted ADR to the index of the architecture file in the same commit.

## Red flags

| Thought | Reality |
| --- | --- |
| "The request is clear; I will start with the code" | A new capability gets the block and the report of `craft:product` first, in a message before the first edit. The block is two lines. |
| "There is no architecture file, so the decision steps do not apply" | Only step 1 and the gate need the file. The other steps hold in every project. |
| "Offering an architecture file is out of the task's scope" | The offer is one question at the first decision of the session, and a no ends it. Ask it. |
| "I found the API client; the search is done" | Search once for each kind of work the change does: the format, the store, the check of the input. |
| "The file is on the `debt` list already, so a few more lines are fine" | The list records the debt; it is no leave to add to it. Name the split before the edit. Only a split that needs decisions of its own lets the change in as it is, with its debt issue. |
| "Moving that part out is a separate task" | A split that only moves code is its own commit before the feature, in this pull request. Only a split that needs decisions of its own waits, as a debt issue filed in this pull request. |
| "I will extract the shared helper later" | Check the three conditions now. When all three hold, extract it in this change; when one fails, the copy stays. |

## Models

| Step | Who |
| --- | --- |
| The start of a feature, the decision and its options | the main session: it has the context of the brainstorming and the spec |
| Find the code that already does this kind of work | an `Explore` subagent, `model: "haiku"`: the file contents stay out of the main context. In 5 runs each, `haiku` found the same code as `sonnet`, at a fifteenth of the cost |
| The second reader for a decision that needs an ADR (step 8) | one subagent that does not see the conversation, `model: "fable"`, `effort: "xhigh"` |
| A first architecture file | one subagent, `model: "fable"`, `effort: "xhigh"` |

Codex has no subagent with a model; the agent does each step that the table
gives to a subagent.

## Other skills

This skill uses them and changes none: `craft:product` at the start
of a feature, for whether the problem needs solving and the simplest way;
`craft:github` for each issue
and each ADR's pull request, `craft:roadmap` for the roadmap and the
steps of a migration, and `measure.sh` and `clones.sh` of `craft:debt`
for the signals.
